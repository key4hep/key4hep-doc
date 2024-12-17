#!/usr/bin/env bash
# Script that tries to automatically fetch further documentation from other
# github repositories, where it simply assumes that they are available under the
# same name. Runs through our ususal suspects of github organizations while
# trying to do so

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
      if ! ls "${file_to_fetch}" > /dev/null 2>&1; then
        echo "${line} does not exist. Trying to fetch it from github"
        local outputdir=$(dirname ${file_to_fetch})
        mkdir -p ${outputdir}  # make the directory for the output

        # Try a few github organizations
        for org in key4hep HEP-FCC AIDASoft iLCSoft; do
          echo "Trying to fetch from github organization: '${org}'"
          if try_fetch ${org} ${line} ${file_dir}; then
            echo "Fetched succesfully from organization '${org}'"
            break
          fi
        done
      fi

      # Check again if we hav succesfully fetched the file
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
