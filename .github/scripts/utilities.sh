#!/usr/bin/env bash

# Try to fetch a file from a github repository
try_fetch() {
    local org=${1}
    local file=${2}
    local outputbase=${3}
    local branches=${4:-"main master"}
    local repo=$(echo ${file} | awk -F '/' '{print $1}')
    local repo_file=${file/${repo}/}

    for branch in ${branches}; do
      curl --fail --silent https://raw.githubusercontent.com/${org}/${repo}/${branch}/${repo_file#/} -o ${outputbase}/${file} && break
    done
}

