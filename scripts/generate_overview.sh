#!/usr/bin/env bash
# Script that generates an overview table of existing algorithms or processors
# from the environment in which it is run.

set -euo pipefail

display_usage() {
    echo "Usage: $(basename $0) COLLECT_SCRIPT STUB [--json-output FILE] [-- GENERATE_TABLE_ARGS...]"
}

if [[ $# -eq 1 && ( "$1" == "-h" || "$1" == "--help" ) ]]; then
    display_usage
    echo "Positional:"
    echo "COLLECT_SCRIPT     Python script that collects component info and writes JSON"
    echo "STUB               Read-only markdown file with page title and intro text"
    echo ""
    echo "Optional:"
    echo "  --json-output      Path for the intermediate JSON file (default: temp file)"
    echo "  Any other arguments are passed directly to generate_overview_table.py"
    exit 0
fi

if [[ $# -lt 2 ]]; then
    display_usage
    exit 1
fi

COLLECT_SCRIPT="$1"
STUB="$2"
shift 2

JSON_OUTPUT=""
TABLE_EXTRA_ARGS=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --json-output)     JSON_OUTPUT="$2"; shift 2 ;;
        *)                 TABLE_EXTRA_ARGS+=("$1"); shift ;;
    esac
done

if [[ "${STUB}" == *.stub.md ]]; then
    OUTPUT="${STUB%.stub.md}.md"
else
    OUTPUT="${STUB}"
fi

JSON_TMP=""
if [[ -z "${JSON_OUTPUT}" ]]; then
    JSON_TMP=$(mktemp --suffix=.json)
    JSON_OUTPUT="${JSON_TMP}"
fi

TABLE_TMP=$(mktemp --suffix=.md)
trap 'rm -f "${TABLE_TMP}" "${JSON_TMP}"' EXIT

set -x
python3 "${COLLECT_SCRIPT}" -o "${JSON_OUTPUT}"

python3 scripts/generate_overview_table.py \
    -i "${JSON_OUTPUT}" \
    -o "${TABLE_TMP}" \
    "${TABLE_EXTRA_ARGS[@]}"
set +x

echo "Generated "$(wc -l ${TABLE_TMP})" lines of table"
cat "${STUB}" "${TABLE_TMP}" > "${OUTPUT}"
echo "Final document has "$(wc -l "${OUTPUT}")" lines"
