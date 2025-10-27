# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Goal**: Develop a reusable sandbox framework for running Claude Code under `--dangerously-skip-permissions` safely.

This project creates a cohesive, observable, and secure sandbox environment where Claude Code can iterate autonomously while developers maintain visibility and control.

### Core Requirements

- **Cohesive**: All features work together seamlessly with minimal configuration
- **Observable**: Sandbox state can be inspected in real-time with comprehensive logging
- **Secure**: Strict filesystem, network, and resource isolation with no escape paths

### Current Status

**Phase:** Research & Design Complete ✅

**Completed:**
- ✅ Technology evaluation (5 options analyzed)
- ✅ Selected Docker Desktop + gVisor (cross-platform solution)
- ✅ Defined 8 sample test projects
- ✅ Created test infrastructure (204 files)
- ✅ All work documented in `.air/tasks/`

**Next:** Phase 1 - Proof of Concept (Docker+gVisor implementation)

## Project Structure

```
claude-sandbox/
├── README.md                      # Project overview
├── CLAUDE.md                      # This file
├── .air/                          # Task tracking framework
│   ├── tasks/                     # All work documented here
│   │   ├── 20251027-1038-research-sandbox-options.md
│   │   ├── 20251027-1048-define-sample-projects.md
│   │   └── 20251027-1053-create-sample-projects.md
│   └── context/                   # Architecture, conventions
├── analysis/                      # Research documents
│   ├── reviews/
│   │   └── sandbox-options.md     # 735-line technology evaluation
│   └── sample-projects.md         # 611-line project specs
├── sample-projects/               # 8 test projects (5 complete, 3 placeholder)
│   ├── 1-trivial/                 # 1.1: Hello World, 1.2: Calculator
│   ├── 2-simple/                  # 2.1: CSV Processing, 2.2: Doc Generator
│   ├── 3-moderate/                # 3.1: Site Generator, 3.2: Log Analyzer
│   └── 4-complex/                 # 4.1-4.3: Production, 4.4: Escape Attempts
└── repos/                         # External repos (optional, via AIR)
```

## Key Technical Decisions

### Sandbox Technology: Docker Desktop + gVisor

**Why:**
- Only solution that works on macOS, Windows, and Linux
- VM-level security (gVisor intercepts all syscalls)
- Container-level performance (~10-20% overhead)
- Industry-standard (Google production use)

**See:** `analysis/reviews/sandbox-options.md` for full evaluation

### Sample Projects

8 projects test different aspects of the sandbox:

1. **1.1: Hello World** ✅ - Basic execution
2. **1.2: Calculator** ✅ - Multi-file + pytest
3. **2.1: CSV Processing** ✅ - File I/O (1000 rows)
4. **2.2: Doc Generator** ✅ - Template processing
5. **3.1: Site Generator** ⚠️ - Complex workflow (placeholder)
6. **3.2: Log Analyzer** ⚠️ - Stress test 100MB (placeholder)
7. **4.1-4.3** ⚠️ - Production scenarios (placeholder)
8. **4.4: Escape Attempts** ✅ - **Security validation (adversarial)**

**See:** `analysis/sample-projects.md` and `sample-projects/README.md`

## Task Tracking

**REQUIRED**: Document all work in `.air/tasks/` using timestamped markdown files.

### Quick Task Creation

```python
from datetime import datetime, timezone
from pathlib import Path

timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")
description = "task-description"  # kebab-case
filename = f".air/tasks/{timestamp}-{description}.md"

content = f"""# Task: Brief Description

## Date
{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}

## Prompt
[User's exact request]

## Actions Taken
1. [What you did]

## Files Changed
- `path/to/file` - [What and why]

## Outcome
⏳ In Progress / ✅ Success / ⚠️ Partial / ❌ Blocked

[Summary]
"""

Path(filename).write_text(content)
```

## Development Workflow

### 1. Starting New Work

1. Create task file (using Python snippet above)
2. Review existing task files for context
3. Check `README.md` for current project status
4. Plan your approach
5. Implement iteratively

### 2. Sandbox Implementation Work

When implementing the Docker+gVisor sandbox:

**Reference Documents:**
- `analysis/reviews/sandbox-options.md` - Implementation guidance
- `sample-projects/README.md` - Testing requirements

**Key Files to Create:**
- `Dockerfile.claude-sandbox` - Container definition
- `run-sandbox.sh` - Wrapper script
- Configuration for gVisor runtime

**Testing:**
- Start with Project 1.1 (Hello World)
- Progress through complexity levels
- End with Project 4.4 (Escape Attempts)

### 3. Sample Project Development

When implementing placeholder projects (3.1, 3.2, 4.1, 4.2, 4.3):

**Each project needs:**
- Detailed `prompt.txt` for Claude
- Test data in `data/`
- Expected outputs in `expected/`
- Working `test.sh` validation script

**See:** Completed projects (1.1, 1.2, 2.1, 2.2) as examples

### 4. Completing Work

- Update task file with outcome (✅/⚠️/❌)
- Add comprehensive summary to task file
- Commit task files with related code changes
- Use semantic commit messages

## Sandbox Development Guidelines

### Design Principles

1. **Isolation**: Sandboxed processes cannot access unauthorized resources
2. **Monitoring**: All sandbox activities logged for observability
3. **Resource Limits**: Clear boundaries on compute, memory, network
4. **Escape Prevention**: Security boundaries cannot be bypassed
5. **Developer Experience**: Easy to inspect sandbox state

### Security Requirements

**Must Have:**
- Read-only root filesystem (except workspace)
- No network access (or strict egress filtering)
- CPU/memory limits to prevent DoS
- Process isolation (separate PID namespace)
- Syscall filtering (via gVisor)

**Testing:**
Project 4.4 validates security by attempting:
- ❌ Read `/etc/passwd` from host (must fail)
- ❌ Write outside workspace (must fail)
- ❌ Make network connections (must fail)
- ❌ Exhaust memory limits (must fail)
- ❌ Fork bomb (must fail)

**If ANY escape succeeds, the sandbox is broken.**

### Performance Targets

- Startup time: < 5 seconds
- Overhead: 10-20% vs native execution
- Memory footprint: Reasonable for resource limits
- No bottlenecks for typical Claude Code workloads

### Observability Requirements

**Must provide:**
- Real-time stdout/stderr streaming
- Resource usage metrics (CPU, memory, disk I/O)
- Filesystem access logs
- Network activity logs (if enabled)
- Exit status and error diagnostics

**Tools:**
- `docker logs` for output
- `docker inspect` for state
- `docker stats` for resources
- Volume mounts for file inspection

## Implementation Phases

### ✅ Phase 0: Research & Planning (Complete)

- [x] Research sandbox technologies
- [x] Define sample projects
- [x] Create test infrastructure

### ⏳ Phase 1: Proof of Concept (Next)

- [ ] Install Docker Desktop + gVisor on macOS
- [ ] Create `Dockerfile.claude-sandbox`
- [ ] Implement `run-sandbox.sh` wrapper
- [ ] Test Projects 1.1 and 1.2
- [ ] Verify basic isolation works

### Phase 2: Observability

- [ ] Add structured logging
- [ ] Implement monitoring dashboard
- [ ] Real-time status viewer
- [ ] Filesystem snapshot capability

### Phase 3: Hardening

- [ ] Run Project 4.4 (escape attempts)
- [ ] Verify all escapes fail
- [ ] Tune resource limits
- [ ] Performance optimization

### Phase 4: Production

- [ ] Cross-platform testing (Windows)
- [ ] Complete placeholder projects
- [ ] Documentation and runbooks
- [ ] Release v1.0

## Commands Reference

### Testing

```bash
# Run individual project test
cd sample-projects/1-trivial/1.1-hello-world
./test.sh

# Run all tests
cd sample-projects
./run-all-tests.sh
```

### Task Management (Optional AIR CLI)

If `air` is installed:

```bash
air task new "description"     # Create task
air task list                  # List tasks
air status                     # Project status
air validate                   # Validate structure
```

### Docker Commands (Once Implemented)

```bash
# Build sandbox image
docker build -t claude-sandbox:latest -f Dockerfile.claude-sandbox .

# Run sandbox
./run-sandbox.sh ./workspace "task description"

# Inspect running container
docker ps
docker logs <container-id>
docker stats <container-id>
docker exec -it <container-id> /bin/bash
```

## Important Notes

- **Always track work**: Every piece of work needs a task file
- **AIR is optional**: Framework works without `air` CLI
- **Security first**: This is sandbox development - be security-conscious
- **UTC timestamps**: Always use UTC for task files
- **Test thoroughly**: Run sample projects after changes
- **Document decisions**: Update `.air/context/` as needed

## Resources

### Analysis Documents
- [Sandbox Options](analysis/reviews/sandbox-options.md) - Technology evaluation
- [Sample Projects](analysis/sample-projects.md) - Project specifications

### Sample Projects
- [Projects README](sample-projects/README.md) - Testing framework
- Individual project READMEs in each directory

### Task History
- [.air/tasks/](.air/tasks/) - Complete audit trail

### External References
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [gVisor](https://gvisor.dev/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)

---

**Current Focus:** Phase 1 - Implement Docker+gVisor sandbox and test with Projects 1.1 & 1.2
