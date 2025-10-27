#!/bin/bash
# Test script for Project 1.1: Hello World

set -euo pipefail

PROJECT_NAME="1.1-hello-world"
WORKSPACE="$(pwd)/workspace"

echo "=== Testing: ${PROJECT_NAME} ==="

# Setup workspace
mkdir -p "${WORKSPACE}"

# TODO: Run sandbox with prompt
# ./run-sandbox.sh "${WORKSPACE}" < prompt.txt > output.log 2>&1

# Validate outputs
echo "Checking for hello.py..."
if [ -f "${WORKSPACE}/hello.py" ]; then
    echo "✅ hello.py created"
else
    echo "❌ hello.py not found"
    exit 1
fi

echo "Running hello.py..."
if python3 "${WORKSPACE}/hello.py" | grep -q "Hello from the sandbox"; then
    echo "✅ Script output correct"
else
    echo "❌ Script output incorrect"
    exit 1
fi

echo ""
echo "✅ Test passed: ${PROJECT_NAME}"
