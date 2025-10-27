# Sample Projects for Claude Sandbox Testing

This directory contains 8 sample projects designed to test and validate the Claude Code sandbox environment.

## Project Structure

```
sample-projects/
├── 1-trivial/          # Level 1: Basic validation
│   ├── 1.1-hello-world/
│   └── 1.2-calculator/
├── 2-simple/           # Level 2: Real work
│   ├── 2.1-csv-processing/
│   └── 2.2-doc-generator/
├── 3-moderate/         # Level 3: Stress testing
│   ├── 3.1-static-site-generator/
│   └── 3.2-log-analyzer/
└── 4-complex/          # Level 4: Production-like + security
    ├── 4.1-api-client/
    ├── 4.2-package-builder/
    ├── 4.3-multi-service/
    └── 4.4-escape-attempts/
```

## Project Status

| Project | Status | Description |
|---------|--------|-------------|
| 1.1 | ✅ Complete | Python Hello World - Basic execution test |
| 1.2 | ✅ Complete | Calculator Library - Multi-file with pytest |
| 2.1 | ✅ Complete | CSV Processing - File I/O heavy workload |
| 2.2 | ✅ Complete | Doc Generator - Template processing |
| 3.1 | ⚠️ Placeholder | Static Site Generator - Complex workflow |
| 3.2 | ⚠️ Placeholder | Log Analyzer - 100MB file stress test |
| 4.1 | ⚠️ Placeholder | API Client - Network access testing |
| 4.2 | ⚠️ Placeholder | Package Builder - Build workflow |
| 4.3 | ⚠️ Placeholder | Multi-Service - Process orchestration |
| 4.4 | ✅ Complete | **Escape Attempts - Security validation** |

## Testing Progression

### Phase 1: Basic Validation (Week 1)
**Projects:** 1.1, 1.2
**Goal:** Prove sandbox can execute simple code

### Phase 2: Real Work (Week 2)
**Projects:** 2.1, 2.2
**Goal:** Handle realistic file I/O workloads

### Phase 3: Stress Testing (Week 3)
**Projects:** 3.1, 3.2
**Goal:** Test resource limits and complex workflows

### Phase 4: Advanced Scenarios (Week 4)
**Projects:** 4.1, 4.2, 4.3
**Goal:** Production-like complexity

### Phase 5: Security Validation (Week 4)
**Project:** 4.4
**Goal:** Verify no escapes possible
**CRITICAL:** All escape attempts must fail!

## Running Tests

Each project has its own `test.sh` script:

```bash
cd 1-trivial/1.1-hello-world
./test.sh
```

Or run all tests:

```bash
./run-all-tests.sh
```

## Project File Structure

Each project contains:

```
project-name/
├── README.md          # Project description and requirements
├── prompt.txt         # Task to give to Claude
├── test.sh            # Automated test script
├── data/              # Input files
├── expected/          # Expected output files
└── templates/         # Templates (if needed)
```

## Resource Limits Per Project

| Project | Memory | CPU | Network | Timeout |
|---------|--------|-----|---------|---------|
| 1.1 | 512MB | 1 | None | 1 min |
| 1.2 | 1GB | 2 | None | 2 min |
| 2.1 | 1GB | 2 | None | 5 min |
| 2.2 | 1GB | 2 | None | 5 min |
| 3.1 | 2GB | 2 | None | 10 min |
| 3.2 | 1GB | 4 | None | 5 min |
| 4.1 | 2GB | 2 | Limited | 10 min |
| 4.2 | 2GB | 4 | PyPI | 15 min |
| 4.3 | 4GB | 4 | Localhost | 10 min |
| 4.4 | 4GB | 4 | None | 5 min |

## Next Steps

1. ✅ Create project directories and structure
2. ✅ Implement basic projects (1.1, 1.2, 2.1, 2.2, 4.4)
3. ⏳ Implement Docker+gVisor sandbox
4. ⏳ Run Phase 1 tests
5. ⏳ Complete placeholder projects as needed
6. ⏳ Run full test suite

## Notes

- **Project 4.4** (Escape Attempts) is the ultimate security validation
- Placeholder projects (3.1, 3.2, 4.1, 4.2, 4.3) can be fully implemented during sandbox development
- All tests assume sandbox wrapper script `run-sandbox.sh` exists in project root
