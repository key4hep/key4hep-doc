#!/usr/bin/env bash
# Script that generates an overview table of existing algorithms or processors
# from the environment in which it is run.

set -euo pipefail

ITEM_LABEL="algorithm"
PROPERTY_LABEL="property"
FILTER_CONFIG=""

display_usage() {
    echo "Usage: $(basename $0) COLLECT_SCRIPT PLACEHOLDER [--json-output FILE] [--filter-config FILTER_CONFIG] [--item-label ITEM_LABEL] [--property-label PROP_LABEL]"
}

if [[ $# -eq 1 && ( "$1" == "-h" || "$1" == "--help" ) ]]; then
    display_usage
    echo "Positional:"
    echo "COLLECT_SCRIPT     Python script that collects component info and writes JSON"
    echo "PLACEHOLDER        Markdown file with page title and intro text; the generated"
    echo "                   table is appended and the file is updated in-place"
    echo ""
    echo "Optional:"
    echo "  --json-output      Path for the intermediate JSON file (default: temp file)"
    echo "  --item-label       Singular label for each item (default: algorithm)"
    echo "  --property-label   Singular label for each property (default: property)"
    echo "  --filter-config    YAML file with filter rules passed to generate_overview_table.py"
    exit 0
fi

if [[ $# -lt 2 ]]; then
    display_usage
    exit 1
fi

COLLECT_SCRIPT="$1"
PLACEHOLDER="$2"
shift 2

JSON_OUTPUT=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --json-output)     JSON_OUTPUT="$2"; shift 2 ;;
        --item-label)      ITEM_LABEL="$2"; shift 2 ;;
        --property-label)  PROPERTY_LABEL="$2"; shift 2 ;;
        --filter-config)   FILTER_CONFIG="$2"; shift 2 ;;
        *)
            echo "Unknown argument: $1";
            display_usage
            exit 1 ;;
    esac
done

JSON_TMP=""
if [[ -z "${JSON_OUTPUT}" ]]; then
    JSON_TMP=$(mktemp --suffix=.json)
    JSON_OUTPUT="${JSON_TMP}"
fi

TABLE_TMP=$(mktemp --suffix=.md)
trap 'rm -f "${TABLE_TMP}" "${JSON_TMP}"' EXIT

python3 "${COLLECT_SCRIPT}" -o "${JSON_OUTPUT}"

TABLE_ARGS=(
    -i "${JSON_OUTPUT}"
    -o "${TABLE_TMP}"
    --item-label "${ITEM_LABEL}"
    --property-label "${PROPERTY_LABEL}"
)
if [ -n "${FILTER_CONFIG}" ]; then
    TABLE_ARGS+=(--filter-config "${FILTER_CONFIG}")
fi

python3 scripts/generate_overview_table.py "${TABLE_ARGS[@]}"

COMBINED_TMP=$(mktemp --suffix=.md)
cat "${PLACEHOLDER}" "${TABLE_TMP}" > "${COMBINED_TMP}"
mv "${COMBINED_TMP}" "${PLACEHOLDER}"
