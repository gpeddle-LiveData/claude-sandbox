#!/bin/bash
set -euo pipefail

PROJECT_NAME="3.1-static-site-generator"
WORKSPACE="$(pwd)/workspace"

echo "=== Testing: ${PROJECT_NAME} ==="

# Copy data to workspace
mkdir -p "${WORKSPACE}"
cp -r data/content "${WORKSPACE}/"
cp -r templates "${WORKSPACE}/"

# Check if output was generated
if [ -d "${WORKSPACE}/output" ] && [ -f "${WORKSPACE}/output/index.html" ]; then
    echo "✅ Site generated"

    # Check for post files
    post_count=$(find "${WORKSPACE}/output" -name "post*.html" | wc -l | tr -d ' ')
    if [ "$post_count" -ge 2 ]; then
        echo "✅ Posts generated: $post_count"
    else
        echo "❌ Expected at least 2 posts, found $post_count"
        exit 1
    fi

    echo "✅ Test passed: ${PROJECT_NAME}"
else
    echo "❌ Site not generated"
    exit 1
fi
