#!/usr/bin/env python3
"""Module for some definitions related to software environments"""

import functools
import os
import re
import pathlib
import logging

logger = logging.getLogger("environment")

_SPACK_PKG_RGX = re.compile(
    r"/cvmfs/sw(?:-nightlies)?\.hsf\.org/key4hep/releases/20[0-9]{2}-[01][0-9]-[0-3][0-9]/x86_64-(?:ubuntu24\.04|almalinux9)-(?:.*?)-(?:opt|dbg)/(.*?)/(.*?)/lib/(.*)"
)
_LCG_VIEW_PKG_RGX = re.compile(
    r"/cvmfs/sft(?:-nightlies).cern.ch/lcg/nightlies/.*?/.*?/(.*?)/.*?/x86_64-(?:el9|ubuntu24)-gcc14-(?:opt|dbg)/lib(?:64)?/(.*)"
)


@functools.lru_cache(maxsize=None)
def get_package_from_lib(lib: str):
    """Get the (lib_stem, package_name) tuple from the library path."""
    logger.debug(f"Getting package name for {lib}")
    if not lib:
        return ("", "")

    lib_path = pathlib.Path(lib)
    lib_stem = lib_path.name
    lib_path = str(lib_path.resolve())

    logger.debug(f"Resolved to {lib_path}")

    lib_match = _SPACK_PKG_RGX.match(lib_path)
    if lib_match:
        logger.debug(f"Matched against spack pattern. package = {lib_match.group(1)}")
        return (lib_stem, lib_match.group(1))

    lib_match = _LCG_VIEW_PKG_RGX.match(lib_path)
    if lib_match:
        logger.debug(f"Matched against LCG pattern. package = {lib_match.group(1)}")
        return (lib_stem, lib_match.group(1))

    # Fall back to the stripped lib name
    pkg_name = re.sub(r"\.so.*$", "", lib_stem)
    pkg_name = re.sub(r"^lib", "", pkg_name)
    logger.debug(f"Not matched against any pattern. Stripped library name = {pkg_name}")

    return (lib_stem, pkg_name)


@functools.lru_cache(maxsize=None)
def find_library(lib_name: str) -> str:
    """Locate the shared library file for the given library stem by searching
    GAUDI_PLUGIN_PATH and LD_LIBRARY_PATH. Returns the full path as a string,
    or an empty string if not found."""
    search_paths = []
    for env_var in ("GAUDI_PLUGIN_PATH", "LD_LIBRARY_PATH"):
        val = os.environ.get(env_var, "")
        if val:
            search_paths.extend(val.split(":"))

    candidates = [f"lib{lib_name}.so", f"{lib_name}.so"]
    for directory in search_paths:
        if not directory:
            continue
        d = pathlib.Path(directory)
        for candidate in candidates:
            p = d / candidate
            if p.exists():
                return str(p)
        # Accept versioned binaries
        for candidate in candidates:
            matches = list(d.glob(f"{candidate}*"))
            if matches:
                return str(matches[0])

    return ""
