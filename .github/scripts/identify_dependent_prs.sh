#!/usr/bin/env bash
# Script that tries to identify dependent PRs from the text of the body by
# "parsing" it for the phrase 'include PR for preview:'
#
# For now we only allow for one such PR

# Read PR number from first argument
PR_NUMBER="$1"

if [ -z "$PR_NUMBER" ]; then
    echo "ERROR: No PR number provided"
    exit 1
fi

# Fetch PR body using GitHub CLI
PR_BODY=$(gh pr view "$PR_NUMBER" --json body --jq '.body')
if [ $? -ne 0 ]; then
    echo "Error: Failed to fetch PR #$PR_NUMBER" >&2
    exit 1
fi

# Search for dependent PR in the body text
DEPENDENT_PR=$(echo "$PR_BODY" | grep -i "include PR for preview:" | sed 's/.*include PR for preview:[[:space:]]*#*\([0-9]\+\).*/\1/')

if [ -n "$DEPENDENT_PR" ]; then
    echo "Found dependent PR: $DEPENDENT_PR"

    DEPENDENT_PR_INFO=$(gh pr view "$DEPENDENT_PR" --json headRepository,headRefName --jq '{repo: .headRepository.nameWithOwner, branch: .headRefName}')
    if [ $? -ne 0 ]; then
        echo "Error: Failed to fetch information for dependent PR #$DEPENDENT_PR" >&2
        exit 1
    fi

    FORK_REPO=$(echo "$DEPENDENT_PR_INFO" | jq -r '.repo')
    BRANCH_NAME=$(echo "$DEPENDENT_PR_INFO" | jq -r '.branch')

    echo "Fork/Repository: $FORK_REPO"
    echo "Branch: $BRANCH_NAME"
else
    echo "No dependent PR found"
fi
