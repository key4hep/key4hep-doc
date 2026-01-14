#!/usr/bin/env bash
# Script that tries to identify external PRs from the text of the body by
# "parsing" it for the phrase 'include PR for preview:'
#
# For now we only allow for one such PR

# Read PR number from first argument
PR_NUMBER="$1"

if [ -z "$PR_NUMBER" ]; then
    echo "ERROR: No PR number provided"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/utilities.sh"

# Fetch PR body using GitHub CLI
PR_BODY=$(gh pr view "$PR_NUMBER" --json body --jq '.body')
if [ $? -ne 0 ]; then
    echo "Error: Failed to fetch PR #$PR_NUMBER" >&2
    exit 1
fi

# Look for patterns like "org/repo#123" or "https://github.com/org/repo/pull/123"
EXTERNAL_PR_LINE=$(echo "$PR_BODY" | grep "include PR for preview:")
if [ -n "$EXTERNAL_PR_LINE" ]; then
    # Try to match org/repo#pr-number format
    REPO_PR=$(echo "$EXTERNAL_PR_LINE" | grep -oE '[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+#[0-9]+' | head -1)

    if [ -n "$REPO_PR" ]; then
        # Convert org/repo#123 format to full GitHub URL
        REPO_NAME=$(echo "$REPO_PR" | cut -d'#' -f1)
        EXTERNAL_PR=$(echo "$REPO_PR" | cut -d'#' -f2)
        GITHUB_URL="https://github.com/$REPO_NAME/pull/$EXTERNAL_PR"
    else
        GITHUB_URL=$(echo "$EXTERNAL_PR_LINE" | grep -oE 'https://github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+/pull/[0-9]+' | head -1)
    fi

    if [ -n "$GITHUB_URL" ]; then
        echo "Found external PR: $GITHUB_URL"

        EXTERNAL_PR_INFO=$(gh pr view "$GITHUB_URL" --json headRepositoryOwner,headRefName,files --jq '{repo: .headRepositoryOwner.login, branch: .headRefName, files: [.files[].path]}')
        if [ $? -ne 0 ]; then
            echo "Error: Failed to fetch information for external PR $GITHUB_URL" >&2
            exit 1
        fi

        PR_FORK=$(echo "$EXTERNAL_PR_INFO" | jq -r '.repo')
        PR_BRANCH=$(echo "$EXTERNAL_PR_INFO" | jq -r '.branch')
        PR_FILES=$(echo "$EXTERNAL_PR_INFO" | jq -r '.files[]')
        echo "Fork/Repository: $PR_FORK"
        echo "Branch: $PR_BRANCH"
        echo "Files: $PR_FILES"
    else
        echo "Error: No valid external PR format found: '${EXTERNAL_PR_LINE}'"
        exit 1
    fi
else
    echo "No external PR found"
fi

# Get the top level md files from the "source of truth"
TOP_LEVEL_FILES=($(grep "fetch_for_file " "$SCRIPT_DIR/fetch_external_sources.sh" | sed 's/fetch_for_file //' | tr -d ' '))

if [ -z "$PR_FILES" ]; then
    echo "No PR files to process"
    exit 0
fi

echo "Processing external PR files..."
for pr_file in $PR_FILES; do
    echo "Processing file: $pr_file"

    # Figure out where in the final doc tree this file should go
    for top_file in "${TOP_LEVEL_FILES[@]}"; do
        referenced_file=$(grep "$pr_file" "$top_file" | head -1 | awk '{print $1}')
        if [ -n "$referenced_file" ]; then
            file_dir=$(dirname $(realpath "$top_file"))
            echo "Found reference to $referenced_file in $top_file"

            output_file="$file_dir/$referenced_file"
            output_dir=$(dirname "$output_file")
            mkdir -p "$output_dir"

            if try_fetch "$PR_FORK" "$referenced_file" "$file_dir" "$PR_BRANCH"; then
                echo "Successfully fetched $referenced_file from $PR_FORK, branch: $PR_BRANCH"
            else
                echo "Warning: Could not fetch $referenced_file from $PR_FORK, branch: $PR_BRANCH"
                exit 1
            fi
            break
        fi
    done
done
