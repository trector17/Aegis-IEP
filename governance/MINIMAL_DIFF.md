# Aegis Minimal Diff Doctrine

**Version:** 1.0.0
**Status:** Active
**Phase:** 0 — Foundation

---

## Purpose

The Minimal Diff Doctrine is a binding constraint governing the scope of every change made to an Aegis-powered repository. It exists to protect the integrity of the codebase, keep diffs reviewable, and prevent governance creep from accumulating silently across unrelated changes.

Every contribution — whether from a human or an AI agent — must modify only the files required to accomplish the stated goal.

---

## Rules

1. **Touch only files in scope.** If a file does not need to change to accomplish the task, do not change it.

2. **No opportunistic cleanup.** Do not fix formatting, rename variables, remove unused imports, or improve readability in files unrelated to the current task.

3. **No premature abstraction.** Do not extract helpers, utilities, or shared components when the task does not require them. Three similar lines of code is better than a premature abstraction.

4. **No speculative changes.** Do not add configurations, options, or hooks for hypothetical future requirements unless the current task explicitly requires them.

5. **No annotation creep.** Do not add comments, docstrings, or type annotations to code you did not change as part of the task.

6. **No backwards-compatibility shims.** Do not add rename stubs, re-exports, or compatibility wrappers for things that are not being removed as part of the current task.

7. **No cross-phase bundling.** Do not include cleanup, refactoring, or improvements scoped to a different phase in a phase-scoped PR.

---

## Enforcement

Violations of the Minimal Diff Doctrine are grounds for PR rejection without review of the functional change. The functional change may be acceptable; the extraneous diff is not.

Reviewers must:
- Reject any PR that touches files not explained by the stated task scope
- Reject any PR that includes opportunistic refactoring alongside functional changes
- Require the author to resubmit with extraneous changes removed before functional review begins

AI agents operating under this doctrine must not expand scope beyond the task boundary given to them. If a task description is ambiguous about scope, the agent must apply the narrowest interpretation and surface the ambiguity before acting.

---

## What Minimal Diff Does Not Mean

- It does not mean changes must be trivially small. A large, well-scoped change touching many files is acceptable if every file is necessary.
- It does not prevent new files from being created when a task requires them.
- It does not prevent deleting files when deletion is the correct outcome.
- It does not require artificial splitting of logically atomic changes.

The test is not size — it is whether every file touched is necessary.

---

## Relationship to Other Doctrine

- **FILE_SCOPE_POLICY.md** — operationalizes the file-level boundary rules that enforce this doctrine
- **REFACTOR_POLICY.md** — defines when a dedicated refactor change is permitted and how it must be scoped
- **ENGINEERING_CONTRACT.md §2** — the authoritative summary; this document expands it into full doctrine
