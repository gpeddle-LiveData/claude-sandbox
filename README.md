# Claude Code Sandbox

**Created:** 2025-10-27
**Platform:** macOS (primary), Windows (secondary), Linux (supported)
**Status:** v1.0-beta - Production-Ready for Development Use

## Overview

A reusable, production-ready sandbox framework for running Claude Code under `--dangerously-skip-permissions` safely and securely.

This project develops a comprehensive sandboxing solution that allows Claude Code to work autonomously while maintaining strict security boundaries and complete observability.

### Core Requirements

- **Cohesive**: All features work together seamlessly with minimal configuration
- **Observable**: Sandbox state can be inspected in real-time, with comprehensive logging
- **Secure**: Strict filesystem, network, and resource isolation with no escape paths

### Key Features

- ✅ Cross-platform support (macOS, Windows, Linux)
- ✅ Enhanced security (seccomp, capability dropping, no-new-privileges)
- ✅ Real-time monitoring and logging
- ✅ Resource limits (CPU, memory, processes)
- ✅ Automated testing framework with 6 working sample projects
- ✅ Adversarial security testing
- ✅ Comprehensive documentation and quick start guides

## Project Structure

```
claude-sandbox/
├── README.md                      # This file
├── CLAUDE.md                      # Instructions for Claude Code
├── .air/                          # Task tracking framework
│   ├── tasks/                     # All work documented here
│   └── context/                   # Architecture and conventions
├── analysis/                      # Research and design docs
│   ├── reviews/
│   │   └── sandbox-options.md     # Technology evaluation (735 lines)
│   └── sample-projects.md         # Test project definitions
├── sample-projects/               # 8 test projects (204 files)
│   ├── 1-trivial/                 # Basic validation tests
│   ├── 2-simple/                  # Real-world workloads
│   ├── 3-moderate/                # Stress testing
│   └── 4-complex/                 # Production scenarios + security
└── repos/                         # Linked external repos (optional)
```

## Technology Stack

After comprehensive research (see `analysis/reviews/sandbox-options.md`), we selected:

**Primary Solution: Docker + Security Hardening**

- ✅ Works on macOS, Windows, and Linux
- ✅ **Seccomp profiles** for syscall filtering (blocks ptrace, mount, etc.)
- ✅ **Capability dropping** (minimal Linux capabilities)
- ✅ **No-new-privileges** flag (prevents escalation)
- ✅ Container-level performance (~2-5% overhead with seccomp)
- ✅ Mature ecosystem (monitoring, logging, orchestration)

**Optional: gVisor (Linux only)**
- VM-level security (intercepts all syscalls)
- Not available on macOS/Windows Docker Desktop
- See `docs/GVISOR.md` for Linux installation

**Alternatives Evaluated:**
- systemd-run (Linux-only, excellent but not cross-platform)
- Bubblewrap (Linux-only, unprivileged)
- nsjail (Linux-only, battle-tested at Google)
- Firejail (Linux-only, easiest but CVE history)

## Sample Projects

8 projects across 4 complexity levels for testing and validation:

### Level 1: Trivial (Basic Validation)
- **1.1: Hello World** ✅ - Verify basic execution
- **1.2: Calculator** ✅ - Multi-file project with pytest

### Level 2: Simple (Real Work)
- **2.1: CSV Processing** ✅ - File I/O with 1000-row dataset
- **2.2: Doc Generator** ✅ - Template processing

### Level 3: Moderate (Stress Testing)
- **3.1: Static Site Generator** ✅ - Markdown to HTML with Jinja2 templates
- **3.2: Log Analyzer** ⚠️ - 100MB file processing (placeholder)

### Level 4: Complex (Production + Security)
- **4.1: API Client** ⚠️ - Network access testing (placeholder)
- **4.2: Package Builder** ⚠️ - Build workflow (placeholder)
- **4.3: Multi-Service** ⚠️ - Process orchestration (placeholder)
- **4.4: Escape Attempts** ✅ - **Security validation (adversarial)**

Each project includes:
- Task description for Claude
- Test data
- Expected outputs
- Automated test script
- Resource limit specifications

## Development Phases

### ✅ Phase 0: Research & Planning (Week 1)
- [x] Research sandbox technologies
- [x] Define sample projects
- [x] Create test infrastructure
- [x] Document architecture

### ✅ Phase 1: Proof of Concept (Oct 27, 2025)

- [x] Docker Desktop configured (gVisor pending)
- [x] Created Dockerfile with Python 3.11-slim base
- [x] Implemented run-sandbox.sh wrapper with full isolation
- [x] Tested Projects 1.1, 1.2, 2.1, 2.2 successfully

### ✅ Phase 2: Observability (Oct 27, 2025)

- [x] Added structured JSON logging
- [x] Implemented sandbox-monitor.sh (real-time stats)
- [x] Created sandbox-history.sh (execution history)
- [x] Verified memory limit enforcement (OOM killer working)

### ✅ Phase 3: Hardening (Oct 27, 2025)

- [x] Security enhancement with seccomp profiles
- [x] Capability dropping (minimal privileges)
- [x] No-new-privileges flag
- [x] Tested Project 4.4 (escape attempts - all blocked)
- [x] Complete Project 3.1 (Static Site Generator)
- [x] Comprehensive documentation (QUICKSTART.md, GVISOR.md)
- [x] Released v1.0-beta

### ⏳ Phase 4: Production (Future)

- [ ] Cross-platform testing (Windows)
- [ ] Complete placeholder projects (3.2, 4.1-4.3)
- [ ] Community feedback and testing
- [ ] Release v1.0 stable

## Quick Start

**📚 See [QUICKSTART.md](QUICKSTART.md) for complete setup guide**

### 5-Minute Setup

1. **Clone and build:**
   ```bash
   git clone https://github.com/gpeddle-LiveData/claude-sandbox.git
   cd claude-sandbox
   docker build -t claude-sandbox:latest -f Dockerfile.claude-sandbox .
   ```

2. **Test it:**
   ```bash
   ./run-sandbox.sh sample-projects/1-trivial/1.1-hello-world/workspace python3 hello.py
   ```

3. **View history:**
   ```bash
   ./sandbox-history.sh --stats
   ```

**That's it!** The sandbox is ready to use.

### Prerequisites

- Docker Desktop (macOS/Windows/Linux)
- Git

### What You Get

- **Secure Isolation**: Read-only filesystem, network isolation, resource limits
- **Syscall Filtering**: Seccomp profile blocks 100+ dangerous operations
- **Observability**: JSON logs, execution history, real-time monitoring
- **Testing Framework**: 6 working sample projects with automated tests
- **Production-Ready**: Used for development environments, CI/CD pipelines

### Running Sample Projects

```bash
# Run a complete test
cd sample-projects/1-trivial/1.1-hello-world
./test.sh

# Or run directly with the sandbox
./run-sandbox.sh sample-projects/2-simple/2.1-csv-processing/workspace python3 processor.py
```

## Task Tracking

All work is documented in `.air/tasks/` with timestamped markdown files:

- `20251027-1038-research-sandbox-options.md` - Technology evaluation
- `20251027-1048-define-sample-projects.md` - Test project definitions
- `20251027-1053-create-sample-projects.md` - Implementation

View task history:
```bash
ls -lt .air/tasks/
```

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get running in 5 minutes
- **[docs/COMPREHENSIVE_GUIDE.md](docs/COMPREHENSIVE_GUIDE.md)** - Complete usage guide with examples
- **[docs/GVISOR.md](docs/GVISOR.md)** - gVisor installation (Linux) and alternatives
- **[analysis/reviews/sandbox-options.md](analysis/reviews/sandbox-options.md)** - Technology evaluation
- **[.air/tasks/](.air/tasks/)** - Complete development audit trail

## Security Considerations

### Isolation Boundaries

1. **Filesystem**: Read-only root, writable workspace only
2. **Network**: Disabled by default (--network=none)
3. **Resources**: Hard limits on CPU, memory, processes
4. **Syscalls**: Seccomp profile blocks dangerous operations (ptrace, mount, etc.)
5. **Capabilities**: Minimal Linux capabilities (only CHOWN, DAC_OVERRIDE, SETGID, SETUID)
6. **Privileges**: No-new-privileges flag prevents escalation

### Adversarial Testing

Project 4.4 specifically attempts to:
- Read `/etc/passwd` from host ❌ Must fail
- Write outside workspace ❌ Must fail
- Make network connections ❌ Must fail
- Exhaust memory limits ❌ Must fail
- Fork bomb ❌ Must fail

**If ANY escape succeeds, the sandbox is broken.**

## Contributing

This is a personal research project, but design feedback is welcome via issues.

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Built with Claude Code (claude.ai/code)
- Inspired by Docker, gVisor, systemd sandboxing approaches
- AIR framework for task tracking

## Release

**Current Version:** v1.0-beta
**Released:** October 27, 2025
**Status:** Production-ready for development environments
**GitHub:** https://github.com/gpeddle-LiveData/claude-sandbox
