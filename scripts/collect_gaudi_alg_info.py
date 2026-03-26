#!/usr/bin/env python3

import json
import logging
import tqdm
import sys
import pathlib

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


def main(args):
    """Main"""
    cfgDb = Configuration.cfgDb

    pkgs = {}

    for name, cfg in tqdm.tqdm(cfgDb.items()):
        pkgs[name] = {
            "lib": cfg["lib"],
            "package": cfg["package"],
            "properties": get_properties(name),
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

    args = parser.parse_args()
    main(args)
