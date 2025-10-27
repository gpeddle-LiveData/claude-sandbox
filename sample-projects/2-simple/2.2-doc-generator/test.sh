#!/bin/bash
set -euo pipefail

PROJECT_NAME="2.2-doc-generator"
WORKSPACE="$(pwd)/workspace"

echo "=== Testing: ${PROJECT_NAME} ==="

mkdir -p "${WORKSPACE}"
cp -r data/src "${WORKSPACE}/"

# TODO: Run sandbox

if [ -d "${WORKSPACE}/docs" ] && [ -f "${WORKSPACE}/docs/utils.md" ]; then
    echo "✅ Documentation generated"
    echo "✅ Test passed: ${PROJECT_NAME}"
else
    echo "❌ Documentation not found"
    exit 1
fi
