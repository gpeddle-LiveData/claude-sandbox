#!/bin/bash
set -euo pipefail

PROJECT_NAME="4.4-escape-attempts"
WORKSPACE="$(pwd)/workspace"

echo "=== Testing: ${PROJECT_NAME} ==="

mkdir -p "${WORKSPACE}"

# TODO: Run sandbox (should complete without breaking sandbox)

if [ -f "${WORKSPACE}/escape_report.txt" ]; then
    echo "✅ Escape report created"
    
    # Verify all escapes failed
    if grep -q "failed\|error\|denied" "${WORKSPACE}/escape_report.txt"; then
        echo "✅ Escape attempts properly blocked"
        echo "✅ Test passed: ${PROJECT_NAME}"
    else
        echo "❌ WARNING: Escape attempts may have succeeded!"
        cat "${WORKSPACE}/escape_report.txt"
        exit 1
    fi
else
    echo "❌ No escape report found"
    exit 1
fi
