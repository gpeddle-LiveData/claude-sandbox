#!/bin/bash
set -euo pipefail

PROJECT_NAME="2.1-csv-processing"
WORKSPACE="$(pwd)/workspace"

echo "=== Testing: ${PROJECT_NAME} ==="

mkdir -p "${WORKSPACE}/data"
cp data/sales.csv "${WORKSPACE}/data/"

# TODO: Run sandbox

if [ -f "${WORKSPACE}/summary.txt" ]; then
    echo "✅ Summary file created"
    echo "✅ Test passed: ${PROJECT_NAME}"
else
    echo "❌ Summary file not found"
    exit 1
fi
