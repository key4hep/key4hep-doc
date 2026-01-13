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

        DEPENDENT_PR_INFO=$(gh pr view "$GITHUB_URL" --json headRepositoryOwner,headRefName,files --jq '{repo: .headRepositoryOwner.login, branch: .headRefName, files: [.files[].path]}')
        if [ $? -ne 0 ]; then
            echo "Error: Failed to fetch information for dependent PR $GITHUB_URL" >&2
            exit 1
        fi

        FORK_REPO=$(echo "$DEPENDENT_PR_INFO" | jq -r '.repo')
        BRANCH_NAME=$(echo "$DEPENDENT_PR_INFO" | jq -r '.branch')
        PR_FILES=$(echo "$DEPENDENT_PR_INFO" | jq -r '.files[]')
        echo "Fork/Repository: $FORK_REPO"
        echo "Branch: $BRANCH_NAME"
        echo "Files: $PR_FILES"
    else
        echo "Error: No valid dependent PR format found: '${DEPENDENT_PR_LINE}'"
        exit 1
    fi
else
    echo "No dependent PR found"
fi

FETCH_BRANCHES="$BRANCH_NAME"

# Source utilities to use try_fetch function
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/utilities.sh"

TOP_LEVEL_FILES=($(grep "fetch_for_file" "$SCRIPT_DIR/fetch_external_sources.sh" | sed 's/fetch_for_file //' | tr -d ' '))

# Try to fetch all of the files and place them where they should go
if [ -n "$PR_FILES" ]; then
    echo "Processing dependent PR files..."

    for pr_file in $PR_FILES; do
        echo "Processing file: $pr_file"

        # Find which top-level file this PR file belongs to by checking if any top-level file references it
        for top_file in "${TOP_LEVEL_FILES[@]}"; do
            if [ -f "$top_file" ] && grep -q "$pr_file" "$top_file"; then
                file_dir=$(dirname $(realpath "$top_file"))
                echo "Found reference to $pr_file in $top_file, using base directory: $file_dir"

                # Create output directory
                output_file="$file_dir/$pr_file"
                output_dir=$(dirname "$output_file")
                mkdir -p "$output_dir"

                # Try to fetch the file
                if try_fetch "$FORK_REPO" "$pr_file" "$file_dir"; then
                    echo "Successfully fetched $pr_file from $FORK_REPO"
                else
                    echo "Warning: Could not fetch $pr_file from $FORK_REPO"
                    exit 1
                fi
                break
            fi
        done
    done
fi
