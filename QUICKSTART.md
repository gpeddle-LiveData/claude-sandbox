# Quick Start - Get Running in 5 Minutes

## What This Is

A secure sandbox for running untrusted Python code. Perfect for:
- Testing Claude Code scripts safely
- Running user-submitted code
- CI/CD pipelines
- Development environments

## Prerequisites

- **Docker Desktop** - [Download here](https://www.docker.com/products/docker-desktop)
- **Git** - [Download here](https://git-scm.com/downloads)
- **5 minutes** of your time

## Installation

### Step 1: Get the Code

```bash
git clone https://github.com/gpeddle-LiveData/claude-sandbox.git
cd claude-sandbox
```

### Step 2: Build the Sandbox

```bash
docker build -t claude-sandbox:latest -f Dockerfile.claude-sandbox .
```

This creates a secure Python 3.11 environment with common packages pre-installed.

### Step 3: Test It

```bash
./run-sandbox.sh sample-projects/1-trivial/1.1-hello-world/workspace python3 hello.py
```

You should see:
```
[INFO] Starting sandbox container...
Hello from the sandbox!
Current timestamp: 2025-10-27 17:07:58
[INFO] Sandbox exited successfully (0s)
```

**That's it! You're ready to go.**

## Basic Usage

### Run Your Own Code

```bash
# Create a workspace
mkdir my-workspace
echo 'print("Hello!")' > my-workspace/script.py

# Run it in the sandbox
./run-sandbox.sh my-workspace python3 script.py
```

### Run with Custom Memory Limit

```bash
SANDBOX_MEMORY=2g ./run-sandbox.sh my-workspace python3 script.py
```

### View Execution History

```bash
# Show last 10 executions
./sandbox-history.sh

# Show statistics
./sandbox-history.sh --stats
```

## What's Included

### Security (Automatic)
- ✅ Filesystem isolation (read-only root)
- ✅ Network isolation (no internet access)
- ✅ Memory limits (4GB default, OOM killer active)
- ✅ Process limits (512 max)
- ✅ Syscall filtering (blocks ptrace, mount, etc.)
- ✅ No privilege escalation possible

### Monitoring
- ✅ JSON logs for every execution
- ✅ Real-time monitoring (`./sandbox-monitor.sh`)
- ✅ Execution history and stats
- ✅ Exit codes and duration tracking

### Pre-installed Packages
- pytest, pytest-cov
- requests
- pandas
- jinja2
- markdown
- pillow

## Common Tasks

### Data Processing

```bash
# Create a data processing workspace
mkdir data-project
echo "date,value
2024-01-01,100
2024-01-02,150" > data-project/data.csv

cat > data-project/process.py <<'EOF'
import csv
with open('data.csv') as f:
    total = sum(int(row['value']) for row in csv.DictReader(f))
    print(f"Total: {total}")
EOF

# Run it
./run-sandbox.sh data-project python3 process.py
```

### Running Tests

```bash
# Create test workspace
mkdir test-project
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

### Try the Sample Projects

```bash
# CSV processing (1000 rows)
./run-sandbox.sh sample-projects/2-simple/2.1-csv-processing/workspace python3 processor.py

# Documentation generator
./run-sandbox.sh sample-projects/2-simple/2.2-doc-generator/workspace python3 doc_generator.py

# Static site generator
./run-sandbox.sh sample-projects/3-moderate/3.1-static-site-generator/workspace python3 generator.py
```

## Configuration

### Environment Variables

```bash
# Memory limit (default: 4g)
export SANDBOX_MEMORY="2g"

# CPU cores (default: 4)
export SANDBOX_CPUS="2"

# Process limit (default: 512)
export SANDBOX_PIDS_LIMIT="256"
```

### Add Custom Packages

Edit `Dockerfile.claude-sandbox`, add packages to the pip install line, then rebuild:

```bash
docker build -t claude-sandbox:latest -f Dockerfile.claude-sandbox .
```

## Troubleshooting

### "Docker is not running"

Start Docker Desktop and wait for it to be ready:
- **macOS**: Look for whale icon in menu bar
- **Windows**: Look for whale icon in system tray
- **Linux**: `sudo systemctl start docker`

### "Permission denied"

Make sure Docker has access to your directories:
- **macOS**: System Preferences → Privacy & Security → Files and Folders → Docker
- **Windows**: Docker Desktop settings → Resources → File Sharing

### Container exits immediately

Check what went wrong:
```bash
./sandbox-history.sh --recent 1
```

## Next Steps

- **Try sample projects** in `sample-projects/`
- **Read security details** in `docs/GVISOR.md`
- **Learn monitoring** tools in `docs/` directory
- **Run escape tests** to verify security: `./run-sandbox.sh sample-projects/4-complex/4.4-escape-attempts/workspace python3 escape_tests.py`

## Getting Help

- **Issues**: https://github.com/gpeddle-LiveData/claude-sandbox/issues
- **Full docs**: See `docs/` directory
- **README**: https://github.com/gpeddle-LiveData/claude-sandbox

---

**Questions?** Check the full documentation in `docs/` or open an issue on GitHub.
