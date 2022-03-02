#!/usr/bin/env bash
# Script that tries to automatically fetch further documentation from other
# github repositories, where it simply assumes that they are available under the
# same name. Runs through our ususal suspects of github organizations while
# trying to do so

# Try to fetch a file from a github repository
try_fetch() {
    local org=${1}
    local file=${2}
    local repo=$(echo ${file} | awk -F '/' '{print $1}')
    local repo_file=${file/${repo}/}

    curl --fail --silent https://raw.githubusercontent.com/${org}/${repo}/master/${repo_file#/} -o ${file}
}

while read -r line; do
  # Check if line is non-empty and ends on .md
  if [ -n "${line}" ] && [[ "${line}" == *.md ]]; then
    # If the file exists do nothing, otherwise pull it in from github
    if ! ls "${line}" > /dev/null 2>&1; then
      echo "${line} does not exist. Trying to fetch it from github"
      mkdir -p  $(dirname ${line}) # make the directory for the output

      # Try a few github organizations
      for org in key4hep HEP-FCC AIDASoft iLCSoft; do
        echo "Trying to fetch from github organization: '${org}'"
        if try_fetch ${org} ${line}; then
          echo "Fetched succesfully from organization '${org}'"
          break
        fi
      done
    fi

    # Check again if we hav succesfully fetched the file
    if ! ls "${line}" > /dev/null 2>&1; then
      echo "Could not fetch file '${line}' from external sources" 1>&2
      exit 1
    fi
  fi
done < README.md
