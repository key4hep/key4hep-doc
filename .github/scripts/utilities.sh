#!/usr/bin/env bash

# Default branches to try when fetching files
FETCH_BRANCHES=${FETCH_BRANCHES:-"main master"}

# Try to fetch a file from a github repository
try_fetch() {
    local org=${1}
    local file=${2}
    local outputbase=${3}
    local repo=$(echo ${file} | awk -F '/' '{print $1}')
    local repo_file=${file/${repo}/}

    for branch in ${FETCH_BRANCHES}; do
      curl --fail --silent https://raw.githubusercontent.com/${org}/${repo}/${branch}/${repo_file#/} -o ${outputbase}/${file} && break
    done
}

