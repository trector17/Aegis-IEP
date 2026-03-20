# Aegis Refactor Policy

**Version:** 1.0.0
**Status:** Active
**Phase:** 0 — Foundation

---

## Purpose

The Refactor Policy defines when refactoring is permitted, how it must be scoped, and what guardrails apply. Refactoring is structurally different from feature work and bug fixes — it changes how code is organized without changing what it does. Because refactors touch many files for reasons unrelated to product behavior, they carry special risk under the Minimal Diff Doctrine and require their own governance rules.

---

## Definition

A **refactor** is any change that:
- Renames, moves, or reorganizes existing code without changing its observable behavior
- Extracts shared logic into a helper, utility, or abstraction
- Replaces one implementation pattern with another without altering the interface or outputs
- Consolidates duplicate logic into a single canonical location

A change is **not** a refactor if it:
- Fixes a bug (even if the fix also reorganizes code)
- Adds a new capability, option, or behavior
- Changes error handling, security posture, or performance characteristics

When a change does both — fixes behavior and reorganizes code — the refactor and the functional change must be in separate PRs unless they are genuinely inseparable (e.g., a rename is required to make the fix unambiguous and the two cannot be committed independently without the codebase being broken between commits).

---

## When Refactors Are Permitted

Refactors are permitted only when all of the following conditions are met:

1. **A phase explicitly scopes it.** Refactor work must be declared in `governance/PHASES.md` as a deliverable of the active phase. Opportunistic refactors outside phase scope are not permitted.

2. **The refactor is isolated.** The PR touches only files involved in the refactor. No feature changes, no dependency upgrades, no governance changes may be bundled in.

3. **The refactor is behavior-preserving.** Observable behavior — outputs, side effects, error states, API contracts — must be identical before and after. Tests must pass without modification, or test changes must be limited to reflecting the rename or move (not asserting new behavior).

4. **The scope is declared in advance.** Before a refactor PR is opened, the scope — what is being moved, renamed, or consolidated, and why — must be stated in the PR description. Reviewers must be able to verify the scope claim from the diff alone.

---

## Frozen Phase Prohibition

Code from a completed (frozen) phase may not be refactored unless a new phase explicitly scopes that work. Completed phases are governance artifacts. Rewriting them without explicit phase authorization undermines traceability and violates phase gating rules defined in `ENGINEERING_CONTRACT.md §3`.

---

## Guardrails

- **No refactor during active feature work.** If a feature branch is in progress that depends on shared code, refactoring that shared code must wait until the feature is merged to avoid divergence.
- **No refactor that crosses layer boundaries.** A refactor must not restructure code in a way that changes which architectural layer a module belongs to, unless that layer migration is explicitly the declared task.
- **No scope expansion mid-PR.** If additional cleanup opportunities are discovered while a refactor is underway, they must be filed as separate tasks — not added to the current diff.
- **No silent behavior change.** If a refactor inadvertently changes observable behavior, it is no longer a refactor. Stop, document the behavior change, and treat it as a bug fix in a separate PR.

---

## AI Agent Posture

AI agents operating on Aegis-powered repos must treat refactoring as an explicitly disallowed activity unless the current task is classified as a refactor phase deliverable. Directives such as "clean this up" or "improve this code" do not constitute refactor authorization. The agent must surface the proposed refactor as a distinct task and await explicit scope confirmation before making any changes.

---

## Relationship to Other Doctrine

- **MINIMAL_DIFF.md** — the parent doctrine; opportunistic refactoring is the most common Minimal Diff violation
- **FILE_SCOPE_POLICY.md** — refactors must follow file scope rules; a rename rippling through many files is in scope only if all affected files are part of the declared rename operation
- **DEPENDENCY_POLICY.md** — dependency consolidation is a refactor-class change and must follow this policy
- **ENGINEERING_CONTRACT.md §3** — phase gating rules govern when a refactor phase may be opened
