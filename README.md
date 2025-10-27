# claude sandbox

**Created:** 2025-10-27
**Mode:** mixed

## Overview

This is a project for developing a sandbox approach to working with Claude Code under `--dangerously-skip-permissions`.

Ww will set a goal, review options, and then work to build the project interatively. Claude (with permission prompts NOT skipped) will be responsible for running the sandbox and testing its functionality.

The sandboxed project is meant to be a reusable strategy, not a one-off. As such, the initial project we choose may be trivial, but the framework for sandboxing claude must be cohesive, observable, and secure.

- Cohesive: all features are well designed and work well together
- Observable: the sandbox environment can be inspected so that the developers can understand what is happening, even as claude is allowed to iterate without supervision.
- Secure: the sandbox environment will have no (or limited) access to the internet and local resources. *this* may be the important area to allow some access under supervision.

## Project Mode: mixed

This is a **mixed-mode** project supporting both review and development workflows.

**Review Workflow:**

1. Review external resources in `repos/`
2. Create analysis in `analysis/reviews/`

**Development Workflow:**

1. Work on this project's code directly
2. Track work in .air/tasks/
3. For external repos with DEVELOPER relationship, create contributions and submit via `air pr`

## Getting Started

### Link Repositories

```bash
# Link review-only resources
air link add ~/repos/service-a --name service-a
air link add ~/repos/service-b --name service-b

# Link development resources (for contributing back)
air link add ~/repos/documentation --name docs --writable

```

### Validate Structure

```bash
air validate
```

### Check Status

```bash
air status
```

## Project Structure

```text
claude-sandbox/
├── README.md              # This file
├── CLAUDE.md              # AI assistant instructions
├── .air/
│   └── air-config.json    # Project configuration
├── repos/                 # Linked repositories (symlinks)
├── analysis/              # Your analysis
│   ├── SUMMARY.md         # Executive summary
│   └── reviews/       # Analysis of reviewed repos
├── contributions/         # Proposed improvements to external repos
├── .air/                  # AI task tracking
│   ├── tasks/             # Task files
│   ├── context/           # Architecture, conventions
│   └── templates/         # Custom templates
```

## Commands

**Note**: The `air` CLI is optional. If not installed, you can still work with this project using manual task file creation (see `.air/README.md`).

**If you have `air` installed** (`pip install air-toolkit`):

```bash
# Project management
air init [name]            # Create new project
air link add             # Link repositories (interactive)
air validate               # Validate structure
air status                 # Show project status

# Task tracking
air task new <desc>        # Create task file
air task list              # List tasks
air task summary           # Generate summary

# Contributions (for DEVELOPER relationship repos)
air pr <resource>          # Create pull request

# Utilities
air version                # Show version
```

**Without `air` installed:**

- Manually create task files in `.air/tasks/` using the format in `.air/README.md`
- Edit `.air/air-config.json` directly to manage configuration
- Use standard git/development tools

## Goals

<!-- Add your assessment goals here -->

- [ ] Review external repositories
- [ ] Develop this project
- [ ] Track all work in .air/tasks/

## Resources

<!-- Linked repositories will be listed here -->

## Notes

<!-- Add project-specific notes here -->