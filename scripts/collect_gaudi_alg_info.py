#!/usr/bin/env python3

import json
import logging
import re
import tqdm
import pathlib

from collections.abc import Iterable

import Configurables

from Gaudi import Configuration
from GaudiConfig2._db import _DB as _gc2_db
from GaudiKernel.DataHandle import DataHandle
from GaudiKernel.GaudiHandles import (
    ServiceHandle,
    ServiceHandleArray,
    PrivateToolHandle,
    PrivateToolHandleArray,
    PublicToolHandle,
    PublicToolHandleArray,
)

from environment import get_package_from_lib, find_library

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

    if isinstance(value, Iterable) and not isinstance(value, str):
        return [_filter_for_json(v) for v in value]

    return value


def _filter_prop_type(prop_name, properties):
    """Filter the property type to try and make it a bit more readable"""
    if prop_name not in properties:
        return ""

    prop_type = properties[prop_name][0]
    # Remove the std::allocator part from vectors
    prev = None
    while prop_type != prev:
        prev = prop_type
        prop_type = re.sub(
            r"std::vector<(.+?),\s*std::allocator<\1\s*>\s*>",
            r"std::vector<\1>",
            prop_type,
        )

    # Remove the std namespace because it takes up too much unnecessary space otherwise
    prop_type = re.sub(r"std::", "", prop_type)
    return prop_type


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

        cpp_type = comp.getType()
        gc2_props = (
            _gc2_db[cpp_type].get("properties", {}) if cpp_type in _gc2_db else {}
        )

        for name, (_, desc) in properties.items():
            val = prop_vals[name]
            props[f"{name}"] = {
                "type": _filter_prop_type(name, gc2_props),
                "value": _filter_for_json(val),
                "description": desc,
            }

    except (AttributeError, RuntimeError):
        pass

    return props


def main(args):
    """Main"""
    cfgDb = Configuration.cfgDb

    pkgs = {}

    for name, cfg in tqdm.tqdm(cfgDb.items()):
        lib_path = find_library(cfg["lib"])
        lib_stem, pkg = get_package_from_lib(lib_path)
        pkgs[name] = {
            "lib": lib_stem or cfg["lib"],
            "package": pkg or cfg["package"],
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
