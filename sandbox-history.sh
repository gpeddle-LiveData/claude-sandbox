#!/bin/bash
# sandbox-history.sh - View execution history from sandbox logs
#
# Usage:
#   ./sandbox-history.sh [options]
#
# Options:
#   --recent N     Show last N executions (default: 10)
#   --failed       Show only failed executions
#   --success      Show only successful executions
#   --since DATE   Show executions since DATE (YYYY-MM-DD)
#   --container NAME  Show specific container
#   --json         Output raw JSON
#   --stats        Show aggregate statistics

set -euo pipefail

LOG_DIR="logs"
RECENT=10
SHOW_FAILED=false
SHOW_SUCCESS=false
SHOW_JSON=false
SHOW_STATS=false
SINCE_DATE=""
CONTAINER_FILTER=""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --recent)
            RECENT="$2"
            shift 2
            ;;
        --failed)
            SHOW_FAILED=true
            shift
            ;;
        --success)
            SHOW_SUCCESS=true
            shift
            ;;
        --since)
            SINCE_DATE="$2"
            shift 2
            ;;
        --container)
            CONTAINER_FILTER="$2"
            shift 2
            ;;
        --json)
            SHOW_JSON=true
            shift
            ;;
        --stats)
            SHOW_STATS=true
            shift
            ;;
        --help|-h)
            cat <<EOF
Usage: $0 [options]

View execution history from sandbox logs.

Options:
  --recent N         Show last N executions (default: 10)
  --failed           Show only failed executions
  --success          Show only successful executions
  --since DATE       Show executions since DATE (YYYY-MM-DD)
  --container NAME   Show specific container
  --json             Output raw JSON
  --stats            Show aggregate statistics

Examples:
  # Show last 10 executions
  ./sandbox-history.sh

  # Show last 20 executions
  ./sandbox-history.sh --recent 20

  # Show only failed executions
  ./sandbox-history.sh --failed

  # Show statistics
  ./sandbox-history.sh --stats

EOF
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Check if logs directory exists
if [ ! -d "$LOG_DIR" ]; then
    echo "No logs directory found. Run some sandbox executions first."
    exit 1
fi

# Count log files
LOG_COUNT=$(find "$LOG_DIR" -name "*.json" 2>/dev/null | wc -l | tr -d ' ')

if [ "$LOG_COUNT" -eq 0 ]; then
    echo "No execution logs found."
    exit 0
fi

# Show statistics
if [ "$SHOW_STATS" = true ]; then
    echo -e "${CYAN}=== Sandbox Execution Statistics ===${NC}"
    echo ""

    TOTAL=0
    SUCCESS=0
    FAILED=0
    TOTAL_DURATION=0

    for log_file in "$LOG_DIR"/*.json; do
        if [ -f "$log_file" ]; then
            # Extract completion events
            while IFS= read -r line; do
                if echo "$line" | grep -q '"event":"complete"'; then
                    TOTAL=$((TOTAL + 1))

                    # Check if successful
                    if echo "$line" | grep -q '"success":"true"'; then
                        SUCCESS=$((SUCCESS + 1))
                    else
                        FAILED=$((FAILED + 1))
                    fi

                    # Sum duration
                    DURATION=$(echo "$line" | grep -o '"duration_seconds":[0-9]*' | cut -d':' -f2 || echo "0")
                    TOTAL_DURATION=$((TOTAL_DURATION + DURATION))
                fi
            done < "$log_file"
        fi
    done

    echo "Total Executions: $TOTAL"
    echo -e "Successful: ${GREEN}$SUCCESS${NC}"
    echo -e "Failed: ${RED}$FAILED${NC}"

    if [ $TOTAL -gt 0 ]; then
        SUCCESS_RATE=$((SUCCESS * 100 / TOTAL))
        AVG_DURATION=$((TOTAL_DURATION / TOTAL))
        echo "Success Rate: ${SUCCESS_RATE}%"
        echo "Average Duration: ${AVG_DURATION}s"
        echo "Total Runtime: ${TOTAL_DURATION}s"
    fi

    exit 0
fi

# Show execution history
echo -e "${CYAN}=== Sandbox Execution History ===${NC}"
echo ""

# Find and sort log files by modification time
LOG_FILES=$(find "$LOG_DIR" -name "*.json" -type f | sort -r | head -n "$RECENT")

for log_file in $LOG_FILES; do
    CONTAINER=$(basename "$log_file" .json)

    # Apply container filter
    if [ -n "$CONTAINER_FILTER" ] && [[ ! "$CONTAINER" =~ $CONTAINER_FILTER ]]; then
        continue
    fi

    # Parse log file
    START_TIME=""
    COMMAND=""
    EXIT_CODE=""
    DURATION=""
    SUCCESS=""

    while IFS= read -r line; do
        # Skip empty lines
        [ -z "$line" ] && continue

        if [ "$SHOW_JSON" = true ]; then
            echo "$line"
            continue
        fi

        EVENT=$(echo "$line" | grep -o '"event":"[^"]*"' | cut -d'"' -f4)

        if [ "$EVENT" = "start" ]; then
            START_TIME=$(echo "$line" | grep -o '"timestamp":"[^"]*"' | cut -d'"' -f4)
            COMMAND=$(echo "$line" | grep -o '"command":"[^"]*"' | cut -d'"' -f4)
        elif [ "$EVENT" = "complete" ]; then
            EXIT_CODE=$(echo "$line" | grep -o '"exit_code":[0-9]*' | cut -d':' -f2)
            DURATION=$(echo "$line" | grep -o '"duration_seconds":[0-9]*' | cut -d':' -f2)
            SUCCESS=$(echo "$line" | grep -o '"success":"[^"]*"' | cut -d'"' -f4)
        fi
    done < "$log_file"

    # Apply success/failed filter
    if [ "$SHOW_FAILED" = true ] && [ "$SUCCESS" = "true" ]; then
        continue
    fi
    if [ "$SHOW_SUCCESS" = true ] && [ "$SUCCESS" = "false" ]; then
        continue
    fi

    # Skip if no completion event
    if [ -z "$EXIT_CODE" ]; then
        continue
    fi

    # Print execution summary
    if [ "$SUCCESS" = "true" ]; then
        STATUS="${GREEN}✓ SUCCESS${NC}"
    else
        STATUS="${RED}✗ FAILED${NC}"
    fi

    echo -e "${YELLOW}Container:${NC} $CONTAINER"
    echo -e "  Status: $STATUS (exit code: $EXIT_CODE)"
    echo -e "  Started: $START_TIME"
    echo -e "  Duration: ${DURATION}s"
    echo -e "  Command: $COMMAND"
    echo ""
done
