#!/usr/bin/env python3

import fnmatch
import yaml


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
