# Claude Code Sandbox

**Created:** 2025-10-27
**Platform:** macOS (primary), Windows (secondary), Linux (supported)
**Status:** Research & Design Phase

## Overview

A reusable, production-ready sandbox framework for running Claude Code under `--dangerously-skip-permissions` safely and securely.

This project develops a comprehensive sandboxing solution that allows Claude Code to work autonomously while maintaining strict security boundaries and complete observability.

### Core Requirements

- **Cohesive**: All features work together seamlessly with minimal configuration
- **Observable**: Sandbox state can be inspected in real-time, with comprehensive logging
- **Secure**: Strict filesystem, network, and resource isolation with no escape paths

### Key Features

- ✅ Cross-platform support (macOS, Windows, Linux)
- ✅ VM-level security with container-level performance
- ✅ Real-time monitoring and logging
- ✅ Resource limits (CPU, memory, disk, network)
- ✅ Automated testing framework with 8 sample projects
- ✅ Adversarial escape testing

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

**Primary Solution: Docker Desktop + gVisor**

- ✅ Works on macOS, Windows, and Linux
- ✅ VM-level security (gVisor intercepts all syscalls)
- ✅ Container-level performance (~10-20% overhead)
- ✅ Mature ecosystem (monitoring, logging, orchestration)
- ✅ Industry-standard (used at Google for untrusted workloads)

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
- **3.1: Static Site Generator** ⚠️ - Complex workflow (placeholder)
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

### ⏳ Phase 1: Proof of Concept (Week 1)
- [ ] Install Docker Desktop + gVisor
- [ ] Create basic Dockerfile
- [ ] Implement run-sandbox.sh wrapper
- [ ] Test Projects 1.1 and 1.2

### Phase 2: Observability (Week 2)
- [ ] Add structured logging
- [ ] Implement monitoring dashboard
- [ ] Real-time status viewer
- [ ] Filesystem snapshot capability

### Phase 3: Hardening (Week 3)
- [ ] Run Project 4.4 (escape attempts)
- [ ] Verify all escapes fail
- [ ] Tune resource limits
- [ ] Performance optimization

### Phase 4: Production (Week 4)
- [ ] Cross-platform testing (Windows)
- [ ] Complete placeholder projects
- [ ] Documentation and runbooks
- [ ] Release v1.0

## Quick Start

### Prerequisites

- Docker Desktop (macOS/Windows/Linux)
- gVisor runtime (runsc)
- Git

### Installation (macOS)

```bash
# 1. Clone repository
git clone https://github.com/gpeddle-LiveData/claude-sandbox.git
cd claude-sandbox

# 2. Install Docker Desktop
# Download from: https://www.docker.com/products/docker-desktop

# 3. Install gVisor
brew install gvisor

# 4. Configure Docker to use gVisor
cat <<EOF > ~/.docker/daemon.json
{
  "runtimes": {
    "runsc": {
      "path": "/usr/local/bin/runsc"
    }
  }
}
EOF

# 5. Restart Docker Desktop
```

### Running Tests

```bash
# Run individual project test
cd sample-projects/1-trivial/1.1-hello-world
./test.sh

# Run all tests
cd sample-projects
./run-all-tests.sh
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

## Resources

### Analysis Documents
- [Sandbox Options Analysis](analysis/reviews/sandbox-options.md) - 735-line evaluation of 5 technologies
- [Sample Projects Specification](analysis/sample-projects.md) - 611-line project definitions

### Sample Projects
- [Sample Projects README](sample-projects/README.md) - Testing framework overview
- Individual project READMEs in each project directory

### Task History
- [.air/tasks/](.air/tasks/) - Complete audit trail of all work

## Security Considerations

### Isolation Boundaries

1. **Filesystem**: Read-only root, writable workspace only
2. **Network**: Disabled by default (or strict egress filtering)
3. **Resources**: Hard limits on CPU, memory, disk I/O, processes
4. **Syscalls**: gVisor intercepts all syscalls, limiting kernel exposure

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

[To be determined]

## Acknowledgments

- Built with Claude Code (claude.ai/code)
- Inspired by Docker, gVisor, systemd sandboxing approaches
- AIR framework for task tracking

---

**Next Step:** Implement Docker+gVisor sandbox (Phase 1)
