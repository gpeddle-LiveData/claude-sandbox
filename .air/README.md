# AI Task Tracking

This directory tracks all AI-assisted development work for this project.

## Structure

```
.air/
├── tasks/           # Task files (one per piece of work)
├── context/         # Project context for AI
│   ├── architecture.md
│   └── language.md
└── templates/       # Task templates
```

## Task Files

Format: `.air/tasks/YYYYMMDD-HHMM-description.md`

Example: `.air/tasks/20251003-1430-review-service-architecture.md`

### Task File Format

```markdown
# Task: Brief Description

## Date
YYYY-MM-DD HH:MM UTC

## Prompt
[Exact user prompt]

## Actions Taken
1. [Action 1]
2. [Action 2]
...

## Files Changed
- `path/to/file.ext` - [What changed and why]

## Outcome
⏳ In Progress / ✅ Success / ⚠️ Partial / ❌ Blocked

[Brief summary]

## Notes
[Optional: Decisions, blockers, follow-up]
```

## Creating Task Files

### Using Python (Recommended for AI and when `air` is not installed)

**This method works without installing `air-toolkit`:**

```python
from datetime import datetime, timezone
from pathlib import Path

timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")
description = "task-description"  # kebab-case
filename = f".air/tasks/{timestamp}-{description}.md"

content = f\"\"\"# Task: {description.replace('-', ' ').title()}

## Date
{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}

## Prompt
[User's prompt here]

## Actions Taken
1.

## Files Changed
-

## Outcome
⏳ In Progress

## Notes

\"\"\"

Path(filename).write_text(content)
```

### Using AIR Command (Optional - requires `air-toolkit` installation)

**If you have installed `air-toolkit` (`pip install air-toolkit`):**

```bash
air task new "description of task"
```

**If `air` is not installed:**
- Use the Python method above
- All task tracking functionality works the same
- No errors or warnings will be shown

## Context Files

### architecture.md

Document system architecture, design patterns, and component relationships.

### language.md

Document language-specific conventions (Python, TypeScript, etc.).

## Rules

1. **Always Create Tasks**: Every piece of work gets a task file
2. **Immediate Creation**: Create task file BEFORE starting work
3. **Immutable**: Never edit task files after creation (create new one for corrections)
4. **Commit With Code**: Task files should be committed with related code changes
5. **Use UTC Time**: Always use UTC timestamps

## Task Outcomes

- ⏳ **In Progress**: Work is ongoing
- ✅ **Success**: Completed successfully
- ⚠️ **Partial**: Partially completed (explain in notes)
- ❌ **Blocked**: Cannot complete (explain blocker)

## Benefits

- **Complete Audit Trail**: Every change is documented
- **Context Preservation**: Future developers understand why decisions were made
- **AI Collaboration**: AI assistants can review past work
- **Project History**: Full narrative of project evolution

## Viewing Task History

```bash
# List all tasks
ls -la .air/tasks/

# View recent tasks
ls -lt .air/tasks/ | head -10

# Search tasks
grep -r "keyword" .air/tasks/

# Generate summary
air task summary
```