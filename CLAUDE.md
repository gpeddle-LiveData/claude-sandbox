# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Goal**: Develop a reusable sandbox framework for running Claude Code under `--dangerously-skip-permissions` safely.

This project aims to create a cohesive, observable, and secure sandbox environment where Claude Code can iterate autonomously while developers maintain visibility and control.

### Key Requirements

- **Cohesive**: All features are well-designed and work together seamlessly
- **Observable**: The sandbox environment can be inspected so developers understand what's happening during unsupervised iteration
- **Secure**: Limited/controlled access to internet and local resources

### Development Approach

- Claude Code **WITHOUT** `--dangerously-skip-permissions` is responsible for building and testing the sandbox
- The sandbox is meant to be a reusable strategy, not a one-off solution
- Initial sandboxed projects may be trivial to focus on framework development

## Project Structure

```
claude-sandbox/
├── CLAUDE.md              # This file
├── README.md              # Project overview and goals
├── .air/                  # Task tracking (optional AIR toolkit)
│   ├── tasks/             # Work documentation
│   └── air-config.json    # AIR configuration
├── .claude/commands/      # Custom slash commands
├── repos/                 # External repos for review/testing
├── analysis/              # Analysis and findings
└── contributions/         # Contributions to external repos
```

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

### Using AIR CLI (Optional)

If `air` is installed (`which air`), you can use:

```bash
# Task management
air task new "description"
air task list
air task summary

# Project status
air status
air validate
```

## Development Workflow

### 1. Starting Work

1. Create a task file (using Python snippet or `/air-task`)
2. Understand the current project state
3. Plan your approach
4. Implement iteratively

### 2. External Repository Review

When reviewing external repos in `repos/`:

- These are READ-ONLY symlinks
- Create analysis in `analysis/reviews/`
- Document findings thoroughly
- Use `/air-analyze` to start structured analysis

### 3. Contributing to External Repos

For repos with DEVELOPER relationship:

- Prepare changes in `contributions/{repo-name}/`
- Match original file structure
- Include clear documentation
- Submit via `air pr {repo-name}` (if available)

### 4. Completing Work

- Update task file with outcome (✅/⚠️/❌)
- Run `air validate` if using AIR
- Commit task files with related code changes

## Sandbox Development Guidelines

When working on the sandbox framework itself:

### Design Principles

1. **Isolation**: Ensure sandboxed processes cannot access unauthorized resources
2. **Monitoring**: Log all sandbox activities for observability
3. **Resource Limits**: Set clear boundaries on compute, memory, network
4. **Escape Prevention**: Validate that sandbox constraints cannot be bypassed
5. **Developer Experience**: Make it easy to inspect sandbox state

### Testing Strategy

- Test with progressively complex workloads
- Verify security boundaries hold under adversarial conditions
- Ensure observability tools provide adequate visibility
- Validate that legitimate use cases work smoothly

### Documentation

- Document architecture decisions in `.air/context/architecture.md`
- Keep language-specific conventions in `.air/context/language.md`
- Maintain comprehensive task history in `.air/tasks/`

## Important Notes

- **Always track work**: Every piece of work needs a task file
- **AIR is optional**: The framework works without `air` CLI installed
- **Read-only repos**: Never modify symlinked repos in `repos/`
- **UTC timestamps**: Always use UTC for task files
- **Security first**: This project involves sandbox development - be mindful of security implications
