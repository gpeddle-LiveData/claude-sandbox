#!/bin/bash
set -euo pipefail

PROJECT_NAME="1.2-calculator"
WORKSPACE="$(pwd)/workspace"

echo "=== Testing: ${PROJECT_NAME} ==="

mkdir -p "${WORKSPACE}"

# TODO: Run sandbox
# ./run-sandbox.sh "${WORKSPACE}" < prompt.txt > output.log 2>&1

# Validate
if [ -f "${WORKSPACE}/calculator.py" ] && [ -f "${WORKSPACE}/test_calculator.py" ]; then
    echo "✅ Files created"
    cd "${WORKSPACE}"
    pytest test_calculator.py -v && echo "✅ Tests passed" || (echo "❌ Tests failed"; exit 1)
else
    echo "❌ Files not found"
    exit 1
fi

echo "✅ Test passed: ${PROJECT_NAME}"
