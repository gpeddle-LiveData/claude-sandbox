#!/bin/bash
# run-sandbox.sh - Wrapper script for running Claude Code in Docker+gVisor sandbox
#
# Usage:
#   ./run-sandbox.sh <workspace-dir> [command]
#
# Arguments:
#   workspace-dir: Directory to mount as /workspace in container
#   command: Optional command to run (default: /bin/bash)
#
# Environment Variables:
#   SANDBOX_MEMORY: Memory limit (default: 4g)
#   SANDBOX_CPUS: CPU limit (default: 4)
#   SANDBOX_NETWORK: Network mode (default: none)
#   SANDBOX_RUNTIME: Docker runtime (default: runsc for gVisor)
#   SANDBOX_NAME: Container name (default: claude-sandbox-<timestamp>)

set -euo pipefail

# Configuration
SANDBOX_IMAGE="${SANDBOX_IMAGE:-claude-sandbox:latest}"
SANDBOX_MEMORY="${SANDBOX_MEMORY:-4g}"
SANDBOX_CPUS="${SANDBOX_CPUS:-4}"
SANDBOX_NETWORK="${SANDBOX_NETWORK:-none}"
SANDBOX_RUNTIME="${SANDBOX_RUNTIME:-runsc}"
SANDBOX_PIDS_LIMIT="${SANDBOX_PIDS_LIMIT:-512}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

show_usage() {
    cat <<EOF
Usage: $0 <workspace-dir> [command]

Run Claude Code in a secure Docker+gVisor sandbox.

Arguments:
  workspace-dir    Directory to mount as /workspace in container (required)
  command          Command to run in container (optional, default: /bin/bash)

Environment Variables:
  SANDBOX_MEMORY      Memory limit (default: 4g)
  SANDBOX_CPUS        CPU limit (default: 4)
  SANDBOX_NETWORK     Network mode (default: none)
  SANDBOX_RUNTIME     Docker runtime (default: runsc)
  SANDBOX_PIDS_LIMIT  Process limit (default: 512)

Examples:
  # Interactive shell
  ./run-sandbox.sh ./my-project

  # Run specific command
  ./run-sandbox.sh ./my-project python3 hello.py

  # With custom resource limits
  SANDBOX_MEMORY=2g SANDBOX_CPUS=2 ./run-sandbox.sh ./my-project

EOF
}

# Check arguments
if [ $# -lt 1 ]; then
    log_error "Missing workspace directory argument"
    show_usage
    exit 1
fi

WORKSPACE_DIR="$1"
shift
COMMAND=("$@")

# Default command if none provided
if [ ${#COMMAND[@]} -eq 0 ]; then
    COMMAND=("/bin/bash")
fi

# Validate workspace directory
if [ ! -d "$WORKSPACE_DIR" ]; then
    log_error "Workspace directory does not exist: $WORKSPACE_DIR"
    exit 1
fi

# Convert to absolute path
WORKSPACE_DIR="$(cd "$WORKSPACE_DIR" && pwd)"

# Generate unique container name
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
SANDBOX_NAME="${SANDBOX_NAME:-claude-sandbox-${TIMESTAMP}}"

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    log_error "Docker is not running. Please start Docker Desktop."
    exit 1
fi

# Check if sandbox image exists
if ! docker image inspect "$SANDBOX_IMAGE" >/dev/null 2>&1; then
    log_warn "Sandbox image '$SANDBOX_IMAGE' not found. Building..."

    if [ ! -f "Dockerfile.claude-sandbox" ]; then
        log_error "Dockerfile.claude-sandbox not found in current directory"
        exit 1
    fi

    docker build -t "$SANDBOX_IMAGE" -f Dockerfile.claude-sandbox .
    log_info "Sandbox image built successfully"
fi

# Check if gVisor runtime is available (optional, fallback to runc)
if ! docker info 2>/dev/null | grep -q "Runtimes:.*runsc"; then
    log_warn "gVisor runtime (runsc) not available, falling back to default runtime (runc)"
    log_warn "Install gVisor for enhanced security: brew install gvisor"
    SANDBOX_RUNTIME="runc"
fi

# Run the sandbox
log_info "Starting sandbox container: $SANDBOX_NAME"
log_info "  Workspace: $WORKSPACE_DIR"
log_info "  Memory: $SANDBOX_MEMORY"
log_info "  CPUs: $SANDBOX_CPUS"
log_info "  Network: $SANDBOX_NETWORK"
log_info "  Runtime: $SANDBOX_RUNTIME"
log_info "  Command: ${COMMAND[*]}"

# Docker run options
DOCKER_OPTS=(
    --rm                                    # Remove container after exit
    --name "$SANDBOX_NAME"                  # Container name
    --runtime="$SANDBOX_RUNTIME"            # Use gVisor if available
    --memory="$SANDBOX_MEMORY"              # Memory limit
    --cpus="$SANDBOX_CPUS"                  # CPU limit
    --pids-limit="$SANDBOX_PIDS_LIMIT"      # Process limit
    --network="$SANDBOX_NETWORK"            # Network isolation
    --read-only                             # Read-only root filesystem
    --tmpfs /tmp/claude-tmp:rw,noexec,nosuid,size=1g  # Writable temp
    -v "${WORKSPACE_DIR}:/workspace:rw"     # Mount workspace
    -w /workspace                           # Set working directory
    -it                                     # Interactive + TTY
)

# Run the container
docker run "${DOCKER_OPTS[@]}" "$SANDBOX_IMAGE" "${COMMAND[@]}"

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    log_info "Sandbox exited successfully"
else
    log_error "Sandbox exited with code: $EXIT_CODE"
fi

exit $EXIT_CODE
