#!/usr/bin/env python3

import json
import pathlib
import re
import subprocess
import sys
from io import BytesIO

from lxml import etree


def run_marlin_x():
    """Run 'Marlin -x' and return stdout as bytes"""
    result = subprocess.run(
        ["Marlin", "-x"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    return result.stdout


def extract_xml(raw_output: bytes) -> bytes:
    """Strip non-XML lines (e.g. INFO log lines) from Marlin -x stdout.

    Marlin -x mixes XML with log messages such as:
        PersistencyIO    INFO  +++ Set Streamer to dd4hep::OpaqueDataBlock
    These lines are identified by a log-level keyword with surrounding spaces
    and discarded. Everything else from the <?xml declaration onward is kept.
    """
    log_line_re = re.compile(r"^\S+\s{2,}(INFO|WARNING|ERROR|DEBUG|MESSAGE|SILENT)\s")

    lines = raw_output.splitlines(keepends=True)
    xml_lines = []
    in_xml = False
    for line in lines:
        decoded = line.decode("latin-1")
        if not in_xml and decoded.lstrip().startswith("<?xml"):
            in_xml = True
        if not in_xml:
            continue
        if log_line_re.match(decoded):
            continue
        xml_lines.append(line)
    return b"".join(xml_lines)


def is_comment(node) -> bool:
    """Return True if the lxml node is a comment node."""
    return callable(node.tag)


def comment_text(node) -> str:
    """Return stripped text content of an lxml comment node."""
    return (node.text or "").strip()


# Matches commented-out parameters, e.g.:
#   <!--parameter name="Verbosity" type="string">DEBUG </parameter-->
_COMMENTED_PARAM_RE = re.compile(
    r"<!--\s*parameter\s+name=\"([^\"]+)\"\s+type=\"([^\"]+)\"[^>]*>([^<]*)</parameter\s*-->"
)


def parse_processors(xml_bytes: bytes) -> dict:
    """Parse processor definitions from Marlin -x XML output and return a json
    dictionary
    """
    root = etree.parse(BytesIO(xml_bytes)).getroot()
    processors = {}

    for proc_elem in root.iter("processor"):
        proc_type = proc_elem.get("type")
        if proc_type is None:
            continue

        # Processor-level description: the first comment child
        proc_description = ""
        for child in proc_elem:
            if is_comment(child):
                proc_description = comment_text(child)
                break

        # Build properties by walking children in order.
        # The pattern in the XML is:
        #   <!-- param description -->
        #   <parameter name="..." ...>default</parameter>
        # or for optional/commented-out params:
        #   <!-- param description -->
        #   <!--parameter name="..." ...>default</parameter-->
        properties = {}
        prev_comment = ""
        skip_first_comment = True  # first comment is the processor description

        for child in proc_elem:
            if is_comment(child):
                text = comment_text(child)

                if skip_first_comment:
                    skip_first_comment = False
                    continue

                # Check if this comment encodes a commented-out parameter
                raw = f"<!--{text}-->"
                m = _COMMENTED_PARAM_RE.match(raw)
                if m:
                    param_name = m.group(1)
                    param_type = m.group(2)
                    param_value = m.group(3).strip()
                    if param_name not in properties:
                        properties[param_name] = {
                            "type": param_type,
                            "value": param_value,
                            "description": prev_comment,
                        }
                    prev_comment = ""
                else:
                    # Regular descriptive comment preceding a parameter
                    prev_comment = text

            elif child.tag == "parameter":
                param_name = child.get("name", "")
                param_type = child.get("type", "")
                param_value = (child.text or "").strip()
                if param_name and param_name not in properties:
                    properties[param_name] = {
                        "type": param_type,
                        "value": param_value,
                        "description": prev_comment,
                    }
                prev_comment = ""
            else:
                prev_comment = ""

        processors[proc_type] = {
            "lib": "",
            "package": "",
            "description": proc_description,
            "properties": properties,
        }

    return processors


def main(args):
    raw = run_marlin_x()

    xml_bytes = extract_xml(raw)
    if not xml_bytes:
        print("ERROR: No XML content found in Marlin output.", file=sys.stderr)
        sys.exit(1)

    processors = parse_processors(xml_bytes)

    with open(args.outputfile, "w") as outfile:
        json.dump(processors, outfile)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description=(
            "Collect information about all available Marlin processors in the "
            "current environment by running 'Marlin -x' and parsing its XML output."
        )
    )
    parser.add_argument(
        "-o",
        "--outputfile",
        help="Output JSON file (default: marlin_processors.json)",
        type=pathlib.Path,
        default="marlin_processors.json",
    )
    args = parser.parse_args()
    main(args)
