# Task: Define Sample Projects for Sandbox Testing

## Date
2025-10-27 10:48 UTC

## Prompt
Define sample projects that we intend to use the sandbox for. These will serve as use cases to refine the sandbox environment and provide testing cases during development.

## Actions Taken
1. Analyzed different project types and complexity levels
2. Considered security/isolation requirements for each
3. Created progression from simple to complex (4 levels)
4. Documented specific sandbox constraints each project tests
5. Defined resource limits per project
6. Created 5-phase testing progression plan

## Files Changed
- `.air/tasks/20251027-1048-define-sample-projects.md` - This task file
- `analysis/sample-projects.md` - Comprehensive sample project definitions (600+ lines)

## Outcome
✅ Success

## Summary
Defined 8 sample projects across 4 complexity levels:

**Level 1:** Hello World, Calculator (basic validation)
**Level 2:** CSV Processing, Doc Generator (real work)
**Level 3:** Static Site Generator, Log Analyzer (stress testing)
**Level 4:** API Client, Package Builder, Multi-Service, Escape Attempts (production-like + security)

Each project tests specific sandbox requirements with defined resource limits.
Project 4.4 is adversarial testing - the ultimate validation.

## Notes
Projects provide concrete use cases to guide sandbox development.
Includes template structure for organizing projects with automated testing.
Resource profiles defined: memory (512MB-4GB), CPU (1-4 cores), network (none/limited/localhost), disk (10MB-500MB).
