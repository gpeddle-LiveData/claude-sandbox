#!/bin/bash
# Run all sample project tests

set -euo pipefail

echo "========================================"
echo "Claude Sandbox - Sample Project Tests"
echo "========================================"
echo ""

FAILED_TESTS=()
PASSED_TESTS=()
SKIPPED_TESTS=()

run_test() {
    local project_path="$1"
    local project_name=$(basename "$project_path")

    echo "Testing: $project_name"
    echo "----------------------------------------"

    if [ ! -f "$project_path/test.sh" ]; then
        echo "⚠️  No test.sh found, skipping"
        SKIPPED_TESTS+=("$project_name")
        echo ""
        return 0
    fi

    cd "$project_path"

    if ./test.sh 2>&1; then
        echo "✅ PASSED"
        PASSED_TESTS+=("$project_name")
    else
        echo "❌ FAILED"
        FAILED_TESTS+=("$project_name")
    fi

    cd - > /dev/null
    echo ""
}

# Run tests by level
for level in 1-trivial 2-simple 3-moderate 4-complex; do
    if [ -d "$level" ]; then
        for project in "$level"/*; do
            if [ -d "$project" ]; then
                run_test "$project"
            fi
        done
    fi
done

# Summary
echo "========================================"
echo "Test Summary"
echo "========================================"
echo "Passed:  ${#PASSED_TESTS[@]}"
echo "Failed:  ${#FAILED_TESTS[@]}"
echo "Skipped: ${#SKIPPED_TESTS[@]}"
echo ""

if [ ${#FAILED_TESTS[@]} -gt 0 ]; then
    echo "Failed tests:"
    for test in "${FAILED_TESTS[@]}"; do
        echo "  ❌ $test"
    done
    exit 1
fi

if [ ${#PASSED_TESTS[@]} -eq 0 ]; then
    echo "⚠️  No tests were run"
    exit 1
fi

echo "✅ All tests passed!"
