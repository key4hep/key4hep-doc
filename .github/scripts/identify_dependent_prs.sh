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

# Look for patterns like "org/repo#123" or "https://github.com/org/repo/pull/123"
DEPENDENT_PR_LINE=$(echo "$PR_BODY" | grep "include PR for preview:")
if [ -n "$DEPENDENT_PR_LINE" ]; then
    # Try to match org/repo#pr-number format
    REPO_PR=$(echo "$DEPENDENT_PR_LINE" | grep -oE '[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+#[0-9]+' | head -1)

    if [ -n "$REPO_PR" ]; then
        # Convert org/repo#123 format to full GitHub URL
        REPO_NAME=$(echo "$REPO_PR" | cut -d'#' -f1)
        DEPENDENT_PR=$(echo "$REPO_PR" | cut -d'#' -f2)
        GITHUB_URL="https://github.com/$REPO_NAME/pull/$DEPENDENT_PR"
    else
        # Try to match full GitHub URL format
        GITHUB_URL=$(echo "$DEPENDENT_PR_LINE" | grep -oE 'https://github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+/pull/[0-9]+' | head -1)
    fi

    if [ -n "$GITHUB_URL" ]; then
        echo "Found dependent PR: $GITHUB_URL"

        DEPENDENT_PR_INFO=$(gh pr view "$GITHUB_URL" --json headRepository,headRefName --jq '{repo: .headRepository.nameWithOwner, branch: .headRefName}')
        if [ $? -ne 0 ]; then
            echo "Error: Failed to fetch information for dependent PR $GITHUB_URL" >&2
            exit 1
        fi

        FORK_REPO=$(echo "$DEPENDENT_PR_INFO" | jq -r '.repo')
        BRANCH_NAME=$(echo "$DEPENDENT_PR_INFO" | jq -r '.branch')

        echo "Fork/Repository: $FORK_REPO"
        echo "Branch: $BRANCH_NAME"
    else
        echo "Error: No valid dependent PR format found: '${DEPENDENT_PR_LINE}'"
        exit 1
    fi
else
    echo "No dependent PR found"
fi
