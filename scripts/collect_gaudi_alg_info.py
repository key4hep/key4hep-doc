#!/usr/bin/env python3

import fnmatch
import json
import logging
import tqdm
import pathlib
import yaml

from collections.abc import Iterable

import Configurables

from Gaudi import Configuration
from GaudiKernel.DataHandle import DataHandle
from GaudiKernel.GaudiHandles import (
    ServiceHandle,
    ServiceHandleArray,
    PrivateToolHandle,
    PrivateToolHandleArray,
    PublicToolHandle,
    PublicToolHandleArray,
)

# Silence some Gaudi logging
logging.getLogger("PropertyProxy").setLevel(logging.CRITICAL)
logging.getLogger("ConfigurableDb").setLevel(logging.CRITICAL)


def _filter_for_json(value):
    """Filter value representation such that it can be dumped to json"""

    if isinstance(value, set):
        # Sets cannot be json serialized and empty sets get converted to 'set()`
        # by turning them to strings`
        if len(value) == 0:
            return "{}"
        return f"{value}"

    if isinstance(
        value,
        (
            DataHandle,
            ServiceHandle,
            ServiceHandleArray,
            PrivateToolHandle,
            PrivateToolHandleArray,
            PublicToolHandle,
            PublicToolHandleArray,
        ),
    ):
        return f"{value}"

    if isinstance(value, Iterable):
        return [_filter_for_json(v) for v in value]

    return value


def _matches_any(value, patterns):
    """Return True if value matches any of the glob patterns (case-sensitive)."""
    return any(fnmatch.fnmatchcase(value, p) for p in patterns)


def get_properties(comp_name):
    """Get all available properties for a given name and try to get their
    default values if available"""
    comp = getattr(Configurables, comp_name)()
    props = {}

    try:
        properties = comp.getPropertiesWithDescription()
        # getPropertiesWithDescription turns falsy values into "<no value>" but we
        # want to have those values properly
        prop_vals = comp.getDefaultProperties()

        for name, (value, desc) in properties.items():
            val = prop_vals[name]
            props[f"{name}"] = {"value": _filter_for_json(val), "description": desc}

    except (AttributeError, RuntimeError):
        pass

    return props


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


def main(args):
    """Main"""
    cfgDb = Configuration.cfgDb

    exclude_cfg = load_filter_config(args.filter_config)

    pkgs = {}

    for name, cfg in tqdm.tqdm(cfgDb.items()):
        if _matches_any(cfg["package"], exclude_cfg["packages"]):
            continue
        if _matches_any(cfg["lib"], exclude_cfg["libs"]):
            continue

        properties = get_properties(name)
        if exclude_cfg["properties"]:
            properties = {
                k: v
                for k, v in properties.items()
                if not _matches_any(k, exclude_cfg["properties"])
            }

        pkgs[name] = {
            "lib": cfg["lib"],
            "package": cfg["package"],
            "properties": properties,
        }

    with open(args.outputfile, "w") as outfile:
        json.dump(pkgs, outfile)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Script to collect information about all available Gaudi algorithms in an environment"
    )
    parser.add_argument(
        "-o",
        "--outputfile",
        help="The name of the output json file containing information about found algorithms",
        type=pathlib.Path,
        default="env_algorithms.json",
    )
    parser.add_argument(
        "--filter-config",
        help="Path to a YAML file specifying filter rules (packages, libs, properties to exclude)",
        type=pathlib.Path,
        default=None,
    )

    args = parser.parse_args()
    main(args)
