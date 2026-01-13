#!/usr/bin/env bash
# Script that tries to automatically fetch further documentation from other
# github repositories, where it simply assumes that they are available under the
# same name. Runs through our usual suspects of github organizations while
# trying to do so

# Initialize force option
FORCE=false


# Display usage message
display_usage() {
  echo "Usage: $(basename $0) [--force|-f] [--help|-h]"
}

# Parse command line arguments
for arg in "$@"; do
  case $arg in
    --force|-f) FORCE=true ;;
    --help|-h)
      display_usage
      echo ""
      echo "Options:"
      echo "  --force, -f    Force fetching files even if they already exist"
      echo "  --help, -h     Display this help message"
      exit 0
      ;;
    *)
      echo "Unknown parameter passed: $arg"
      display_usage
      exit 1
      ;;
  esac
done


# Default GitHub organizations to try when fetching external files
GITHUB_ORGS="key4hep HEP-FCC AIDASoft iLCSoft"
FETCH_BRANCHES="main master"

# NOTE: Fetch this late so that setting the customizations for the functions can
# take place
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/utilities.sh"


fetch_for_file docs/index.md
fetch_for_file docs/tutorials/README.md
fetch_for_file docs/how-tos/README.md
fetch_for_file docs/developing-key4hep-software/README.md
