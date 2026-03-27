#!/usr/bin/env python3

import fnmatch
import html
import json
import pathlib
import yaml
from collections import defaultdict

from jinja2 import Environment, FileSystemLoader

DEFAULT_TEMPLATE = (
    pathlib.Path(__file__).parent / "templates" / "algorithm_overview.md.jinja2"
)


def _matches_any(value, patterns):
    """Return True if value matches any of the glob patterns (case-sensitive)."""
    return any(fnmatch.fnmatchcase(value, p) for p in patterns)


def load_filter_config(config_path):
    """Load and return the exclude lists from a YAML filter config file."""
    if config_path is None:
        return {"packages": [], "libs": [], "properties": []}

    with open(config_path) as f:
        config = yaml.safe_load(f)

    exclude = config.get("filter", {}).get("exclude", {})
    return {
        "packages": exclude.get("packages", []),
        "libs": exclude.get("libs", []),
        "properties": exclude.get("properties", []),
    }


def is_algorithm_excluded(cfg, exclude):
    """Return True if the algorithm should be excluded based on package or lib."""
    return _matches_any(cfg["package"], exclude["packages"]) or _matches_any(
        cfg["lib"], exclude["libs"]
    )


def filter_properties(properties, exclude):
    """Remove properties whose names match any pattern in exclude['properties']."""
    if not exclude["properties"]:
        return properties
    return {
        k: v
        for k, v in properties.items()
        if not _matches_any(k, exclude["properties"])
    }


def load_algorithms(input_path):
    with open(input_path) as f:
        return json.load(f)


def apply_filters(algorithms, filter_config):
    result = {}
    for name, info in algorithms.items():
        if is_algorithm_excluded(info, filter_config):
            continue
        result[name] = {
            **info,
            "properties": filter_properties(info["properties"], filter_config),
        }
    return result


def group_by_package(algorithms):
    groups = defaultdict(list)
    for name, info in algorithms.items():
        groups[info["package"]].append(
            {
                "name": name,
                "lib": info["lib"],
                "description": info.get("description", ""),
                "properties": info["properties"],
            }
        )
    for pkg in groups:
        groups[pkg].sort(key=lambda a: a["name"])
    return dict(sorted(groups.items(), key=lambda item: (item[0] == "", item[0])))


def _render_prop_value(value):
    """Render a property value as an HTML snippet (returned unescaped)."""
    if value is None:
        return "<em>none</em>"
    if isinstance(value, (list, dict)):
        return f"<code>{html.escape(json.dumps(value, ensure_ascii=False))}</code>"
    return f"<code>{html.escape(str(value))}</code>"


def render_page(template_path, packages, total_algorithms):
    env = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        autoescape=False,
    )
    env.filters["render_prop_value"] = _render_prop_value
    template = env.get_template(template_path.name)
    return template.render(
        packages=packages,
        total_algorithms=total_algorithms,
        total_packages=len(packages),
    )


def main(args):
    algorithms = load_algorithms(args.input)

    if args.filter_config:
        filter_config = load_filter_config(args.filter_config)
        algorithms = apply_filters(algorithms, filter_config)

    packages = group_by_package(algorithms)
    total_algorithms = sum(len(algs) for algs in packages.values())

    output = render_page(args.template, packages, total_algorithms)

    with open(args.output, "w") as f:
        f.write(output)

    print(
        f"Generated {args.output} with {total_algorithms} algorithms "
        f"in {len(packages)} packages"
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate an algorithm overview page from collected algorithm JSON data"
    )
    parser.add_argument(
        "--input",
        "-i",
        help="Input JSON file with algorithm information",
        type=pathlib.Path,
        required=True,
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output MyST markdown file path",
        type=pathlib.Path,
        required=True,
    )
    parser.add_argument(
        "--template",
        help="Path to the Jinja2 template",
        type=pathlib.Path,
        default=DEFAULT_TEMPLATE,
    )
    parser.add_argument(
        "--filter-config",
        help="Path to a YAML file with filter rules (packages, libs, properties to exclude)",
        type=pathlib.Path,
        default=None,
    )

    args = parser.parse_args()
    main(args)
