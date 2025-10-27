#!/bin/bash
# sandbox-monitor.sh - Real-time monitoring of running sandbox containers
#
# Usage:
#   ./sandbox-monitor.sh [container-name-or-id]
#
# Shows real-time resource usage, logs, and status

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

show_usage() {
    cat <<EOF
Usage: $0 [container-name-or-id]

Monitor a running sandbox container in real-time.

If no container specified, shows all claude-sandbox containers.

Commands:
  l - View logs (last 50 lines)
  f - Follow logs (tail -f)
  s - Show stats
  i - Show detailed info
  e - Execute command in container
  q - Quit

Examples:
  # Monitor specific container
  ./sandbox-monitor.sh claude-sandbox-20251027-123456

  # List all sandbox containers
  ./sandbox-monitor.sh

EOF
}

list_containers() {
    echo -e "${CYAN}=== Claude Sandbox Containers ===${NC}"
    docker ps -a --filter "name=claude-sandbox" \
        --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.CreatedAt}}" \
        || echo "No sandbox containers found"
}

monitor_container() {
    local CONTAINER="$1"

    # Check if container exists
    if ! docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
        echo "Error: Container '$CONTAINER' not found"
        list_containers
        exit 1
    fi

    while true; do
        clear
        echo -e "${CYAN}=== Sandbox Monitor: $CONTAINER ===${NC}"
        echo ""

        # Container status
        echo -e "${GREEN}Status:${NC}"
        docker ps -a --filter "name=${CONTAINER}" \
            --format "  ID: {{.ID}}\n  Status: {{.Status}}\n  Created: {{.CreatedAt}}"
        echo ""

        # Resource usage (if running)
        if docker ps --filter "name=${CONTAINER}" --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
            echo -e "${GREEN}Resources:${NC}"
            docker stats --no-stream --format \
                "  CPU: {{.CPUPerc}}\n  Memory: {{.MemUsage}} ({{.MemPerc}})\n  Net I/O: {{.NetIO}}\n  Block I/O: {{.BlockIO}}" \
                "${CONTAINER}" 2>/dev/null || echo "  (Container stopped)"
            echo ""
        fi

        # Recent logs
        echo -e "${GREEN}Recent Logs (last 10 lines):${NC}"
        docker logs --tail 10 "${CONTAINER}" 2>&1 | sed 's/^/  /'
        echo ""

        echo -e "${YELLOW}Commands: [l]ogs [f]ollow [s]tats [i]nfo [e]xec [q]uit${NC}"

        # Wait for input with timeout
        read -t 2 -n 1 cmd || continue

        case "$cmd" in
            l)
                clear
                echo -e "${CYAN}=== Logs: $CONTAINER ===${NC}"
                docker logs --tail 50 "${CONTAINER}" 2>&1 | less
                ;;
            f)
                clear
                echo -e "${CYAN}=== Following Logs: $CONTAINER (Ctrl+C to stop) ===${NC}"
                docker logs -f "${CONTAINER}" 2>&1
                ;;
            s)
                clear
                echo -e "${CYAN}=== Stats: $CONTAINER (Ctrl+C to stop) ===${NC}"
                docker stats "${CONTAINER}"
                ;;
            i)
                clear
                echo -e "${CYAN}=== Detailed Info: $CONTAINER ===${NC}"
                docker inspect "${CONTAINER}" | less
                ;;
            e)
                echo ""
                read -p "Command to execute: " exec_cmd
                docker exec -it "${CONTAINER}" $exec_cmd || echo "Command failed"
                read -p "Press Enter to continue..."
                ;;
            q)
                echo ""
                echo "Exiting monitor"
                exit 0
                ;;
        esac
    done
}

# Main
if [ $# -eq 0 ]; then
    list_containers
    echo ""
    read -p "Enter container name to monitor (or press Enter to exit): " container
    [ -z "$container" ] && exit 0
    monitor_container "$container"
else
    if [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
        show_usage
        exit 0
    fi
    monitor_container "$1"
fi
