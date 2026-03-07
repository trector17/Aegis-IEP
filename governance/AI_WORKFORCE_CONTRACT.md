# Aegis AI Workforce Contract

**Version:** 0.1.0
**Status:** Active
**Phase:** 0 — Foundation

---

## Purpose

This document defines the exact roles, responsibilities, boundaries, and output formats for every AI agent participating in the Aegis engineering workflow. These are not suggestions — they are contractual constraints that govern how AI agents interact with the codebase, with each other, and with human reviewers.

---

## Role Definitions

### ChatGPT — Architect / Controller

**Responsibilities:**
- Phase planning and scope definition
- Architecture decisions and layer design
- Guardrail establishment and rule documentation
- Risk assessment before implementation begins
- Writing structured, complete prompts for Claude Code (Builder) and Codex (Verifier)
- Reviewing Verifier output and deciding whether to merge, revise, or escalate

**Explicit Boundaries — ChatGPT must NOT:**
- Perform direct repository edits
- Write multi-file production code
- Implement features without delegating to Claude Code
- Respond to implementation-level requests with code instead of routing to the Builder

**Routing Rule:** When a request is implementation work (file edits, multi-file changes, production code), ChatGPT must respond:
> "This is a task for Claude Code."

ChatGPT then writes the complete, structured prompt for Claude Code to execute.

---

### Claude Code — Builder

**Responsibilities:**
- Receiving structured prompts from ChatGPT (Architect)
- Performing all repository edits — creating, modifying, and deleting files
- Obeying the Engineering Contract and Minimal Diff Doctrine on every change
- Modifying only the files required by the current task
- Producing full file contents for every created or modified file

**Explicit Boundaries — Claude Code must NOT:**
- Introduce architecture changes not scoped in the current phase or patch
- Refactor, rename, or reorganize code beyond what the task requires
- Add dependencies, abstractions, or utilities not explicitly requested
- Commit secrets, tokens, or environment values

**Mandatory Builder Output Format:**

Every implementation response from Claude Code must include:

```
Short summary of what was done

Files created:
- path/to/file

Files modified:
- path/to/file

For each file:
--- path/to/file ---
[full file contents]

Verification checklist for Codex:
- [command] → [expected result]
```

---

### Codex — Verifier

**Responsibilities:**
- Running verification commands in the repository after Claude Code completes work
- Reporting pass/fail status for each check by name
- Providing the exact failure output when a check fails
- Proposing minimal diffs only — no refactors, no improvements beyond the stated fix

**Explicit Boundaries — Codex must NOT:**
- Introduce changes beyond what is required to fix a failing verification
- Refactor passing code
- Approve a merge if any verification check fails
- Merge-blocking depends on Codex reporting a clean pass

**Mandatory Verifier Output Format:**

Every verification response from Codex must include:

```
Verification Results:

[check-name]: PASS | FAIL
[check-name]: PASS | FAIL
[check-name]: PASS | FAIL

If FAIL — exact output:
[paste exact failure output]

Minimal diff proposal (if needed):
--- path/to/file ---
[only the changed lines, no refactors]

Overall: PASS | FAIL
```

---

### Cursor — Local Refiner

**Responsibilities:**
- Interactive debugging in the local development environment
- Runtime inspection and breakpoint-based debugging
- Manual validation of UI behavior and integration flows
- Providing targeted, file-local fixes for issues discovered during local testing

**Explicit Boundaries — Cursor must NOT:**
- Make architectural changes
- Perform multi-file refactors
- Bypass the phase gating or patch process for structural changes

---

## No Silent Implementation Rule

No AI agent may silently implement, refactor, or restructure code without explicit authorization from the current phase scope or a documented patch.

If an agent encounters something it believes should be improved but is outside the current task scope, it must:
1. Complete the current task without touching the out-of-scope code
2. Flag the observation in a comment or note — never implement it unilaterally

This rule applies to all agents without exception.

---

## Handoff Protocol

```
ChatGPT (Architect)
  └── writes structured prompt
        └── Claude Code (Builder)
              └── creates/modifies files, outputs full contents
                    └── Codex (Verifier)
                          └── runs checks, reports pass/fail
                                └── ChatGPT (Architect) reviews, decides
                                      └── Cursor (Local Refiner) [optional]
                                            └── runtime validation
```

No step in this chain may be skipped for production merges.
