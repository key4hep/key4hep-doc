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

# Try to fetch a file from a github repository
try_fetch() {
    local org=${1}
    local file=${2}
    local outputbase=${3}
    local repo=$(echo ${file} | awk -F '/' '{print $1}')
    local repo_file=${file/${repo}/}

    for branch in main master; do
      curl --fail --silent https://raw.githubusercontent.com/${org}/${repo}/${branch}/${repo_file#/} -o ${outputbase}/${file} && break
    done
}

# process one markdown file with content that potentially needs fetching from an
# external repository
fetch_for_file() {
  local file_to_proc=${1}
  local file_dir=$(dirname $(realpath ${file_to_proc}))

  echo "Fetching external contents for file '${file_to_proc}'"

  while read -r line; do
    # Check if line is non-empty and ends on .md
    if [ -n "${line}" ] && [[ "${line}" == *.md ]] || [[ "${line}" == *.png ]]; then
      # If the file exists do nothing, otherwise pull it in from github
      local file_to_fetch=${file_dir}/${line}
      if [ "${FORCE}" = true ]; then
        echo "Force option enabled. Trying to fetch '${line}' from github"
      elif ! ls "${file_to_fetch}" > /dev/null 2>&1; then
        echo "${line} does not exist. Trying to fetch it from github"
      else
        continue
      fi

      local outputdir=$(dirname ${file_to_fetch})
      mkdir -p ${outputdir}  # make the directory for the output

      # Try a few github organizations
      for org in key4hep HEP-FCC AIDASoft iLCSoft; do
        echo "Trying to fetch from github organization: '${org}'"
        if try_fetch ${org} ${line} ${file_dir}; then
          echo "Fetched successfully from organization '${org}'"
          break
        fi
      done

      # Check again if we have successfully fetched the file
      if ! ls "${file_to_fetch}" > /dev/null 2>&1; then
        echo "Could not fetch file '${line}' from external sources" 1>&2
        exit 1
      fi
    fi
  done < ${file_to_proc}
}

fetch_for_file docs/index.md
fetch_for_file docs/tutorials/README.md
fetch_for_file docs/how-tos/README.md
fetch_for_file docs/developing-key4hep-software/README.md
