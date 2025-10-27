# Quick Start Guide

Get up and running with the Claude Code Sandbox in 5 minutes.

## Prerequisites

- Docker Desktop installed and running
- macOS, Windows (WSL2), or Linux
- Basic command line knowledge

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/gpeddle-LiveData/claude-sandbox.git
cd claude-sandbox
```

### 2. Build the Sandbox Image

```bash
docker build -t claude-sandbox:latest -f Dockerfile.claude-sandbox .
```

This creates a secure Python 3.11 environment with:
- Non-root user (claudeuser)
- Read-only root filesystem
- Pre-installed packages (pytest, pandas, jinja2, markdown)

### 3. Test the Installation

```bash
./run-sandbox.sh sample-projects/1-trivial/1.1-hello-world/workspace python3 hello.py
```

You should see:
```
[INFO] Starting sandbox container: claude-sandbox-TIMESTAMP
Hello from the sandbox!
Current timestamp: 2025-10-27 17:07:58
[INFO] Sandbox exited successfully (0s)
```

## Basic Usage

### Run a Python Script

```bash
./run-sandbox.sh <workspace-dir> python3 <script.py>
```

**Example:**
```bash
# Create a test workspace
mkdir -p my-workspace
echo 'print("Hello from sandbox!")' > my-workspace/test.py

# Run it
./run-sandbox.sh my-workspace python3 test.py
```

### Run with Custom Resources

```bash
SANDBOX_MEMORY=2g SANDBOX_CPUS=2 ./run-sandbox.sh my-workspace python3 script.py
```

### Run Interactive Shell

```bash
./run-sandbox.sh my-workspace /bin/bash
```

## Monitoring & Observability

### View Execution History

```bash
# Show last 10 executions
./sandbox-history.sh

# Show statistics
./sandbox-history.sh --stats

# Show only failed executions
./sandbox-history.sh --failed

# Show last 20 executions
./sandbox-history.sh --recent 20
```

**Example Output:**
```
=== Sandbox Execution History ===

Container: claude-sandbox-20251027-130758
  Status: ✓ SUCCESS (exit code: 0)
  Started: 2025-10-27T17:07:58Z
  Duration: 0s
  Command: python3 hello.py
```

### Real-Time Monitoring

```bash
# List all sandbox containers
./sandbox-monitor.sh

# Monitor specific container
./sandbox-monitor.sh claude-sandbox-TIMESTAMP
```

**Interactive Commands:**
- `[l]` - View logs (last 50 lines)
- `[f]` - Follow logs in real-time
- `[s]` - Show live stats (CPU, memory)
- `[i]` - Show detailed container info
- `[e]` - Execute command in container
- `[q]` - Quit

## Example Workflows

### 1. Data Processing

```bash
# Create workspace with data
mkdir -p data-project
echo "date,value
2024-01-01,100
2024-01-02,150" > data-project/data.csv

# Create processor script
cat > data-project/process.py <<'EOF'
import csv

with open('data.csv', 'r') as f:
    reader = csv.DictReader(f)
    total = sum(int(row['value']) for row in reader)
    print(f"Total: {total}")
EOF

# Run in sandbox
./run-sandbox.sh data-project python3 process.py
```

### 2. Testing Code

```bash
# Create test project
mkdir -p test-project
cat > test-project/calculator.py <<'EOF'
def add(a, b):
    return a + b
EOF

cat > test-project/test_calculator.py <<'EOF'
from calculator import add

def test_add():
    assert add(2, 3) == 5
EOF

# Run tests in sandbox
./run-sandbox.sh test-project pytest
```

### 3. Document Generation

```bash
# Run the sample documentation generator
./run-sandbox.sh sample-projects/2-simple/2.2-doc-generator/workspace python3 doc_generator.py

# Check output
ls sample-projects/2-simple/2.2-doc-generator/workspace/docs/
```

## Security Features

The sandbox automatically provides:

### Isolation
- ✅ **Filesystem**: Read-only root, writable /workspace only
- ✅ **Network**: Complete isolation (no external connections)
- ✅ **Process**: Limited to 512 processes
- ✅ **Resources**: 4GB memory, 4 CPUs (configurable)

### Enhanced Security (Automatic)
- ✅ **Seccomp**: Syscall filtering (dangerous calls blocked)
- ✅ **Capabilities**: Minimal Linux capabilities
- ✅ **No New Privileges**: Privilege escalation prevented
- ✅ **OOM Killer**: Memory bombs terminated automatically

### Verify Security

```bash
# Run escape attempt tests
./run-sandbox.sh sample-projects/4-complex/4.4-escape-attempts/workspace python3 escape_tests.py
```

All escape attempts should be blocked:
- ✅ Network isolation working
- ✅ Filesystem protected
- ✅ Memory limits enforced
- ✅ Root filesystem read-only

## Configuration

### Environment Variables

```bash
# Memory limit (default: 4g)
export SANDBOX_MEMORY="2g"

# CPU limit (default: 4)
export SANDBOX_CPUS="2"

# Network mode (default: none)
export SANDBOX_NETWORK="bridge"  # Use with caution!

# Process limit (default: 512)
export SANDBOX_PIDS_LIMIT="256"

# Container name prefix
export SANDBOX_NAME="my-sandbox-$(date +%s)"
```

### Custom Docker Image

To add more packages:

1. Edit `Dockerfile.claude-sandbox`
2. Add your packages to the `RUN pip install` line
3. Rebuild: `docker build -t claude-sandbox:latest -f Dockerfile.claude-sandbox .`

## Troubleshooting

### Docker Not Running

```bash
# Check Docker status
docker info

# Start Docker Desktop (macOS)
open -a Docker
```

### Permission Denied

```bash
# Ensure workspace exists and is readable
ls -la my-workspace

# Check Docker has access to the directory
# On macOS: System Preferences → Privacy & Security → Files and Folders → Docker
```

### Container Exits Immediately

```bash
# Check logs
./sandbox-history.sh --recent 1

# Or view Docker logs
docker logs <container-name>
```

### Memory/Resource Issues

```bash
# Check Docker Desktop resource limits
docker info | grep -i memory

# Reduce sandbox limits
SANDBOX_MEMORY=1g ./run-sandbox.sh ...
```

## Next Steps

- Try the sample projects in `sample-projects/`
- Read `docs/GVISOR.md` for enhanced security on Linux
- Check `docs/ARCHITECTURE.md` for implementation details
- Run `./sandbox-history.sh --stats` to see execution metrics

## Getting Help

- Issues: https://github.com/gpeddle-LiveData/claude-sandbox/issues
- Discussions: https://github.com/gpeddle-LiveData/claude-sandbox/discussions
- Documentation: See `docs/` directory

## Common Use Cases

### Claude Code Integration

When using Claude Code with `--dangerously-skip-permissions`:

```bash
# Instead of running directly:
# claude-code --dangerously-skip-permissions execute script.py

# Use the sandbox:
./run-sandbox.sh workspace python3 script.py
```

### CI/CD Integration

```bash
# In your CI pipeline
docker build -t claude-sandbox:latest -f Dockerfile.claude-sandbox .
./run-sandbox.sh ./test-workspace pytest
```

### Batch Processing

```bash
# Process multiple files
for file in data/*.csv; do
    ./run-sandbox.sh workspace python3 process.py "$file"
done
```

---

**Ready to go!** Start with the sample projects or create your own workspace. 🚀
