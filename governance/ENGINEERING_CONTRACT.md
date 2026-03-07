# Aegis Engineering Contract

**Version:** 0.1.0
**Status:** Active
**Phase:** 0 — Foundation

---

## 1. Governance Is Version-Controlled Law

This document is the authoritative engineering contract for any repo powered by Aegis. It is committed to the repository and versioned alongside the code. Governance rules are not informal guidelines — they are binding constraints enforced mechanically where possible and by review otherwise.

Any change to this contract requires:
1. A documented patch entry in `governance/PATCH_LOG.md` using the format defined in `governance/PATCH_TEMPLATE.md`
2. A Codex verification pass confirming the patch does not break policy gates
3. An explicit PR with the change scoped to governance only

---

## 2. Minimal Diff Doctrine

Every contribution must modify only the files required to accomplish the stated goal. This is non-negotiable.

**Rules:**
- Do not modify files unrelated to the current task
- Do not refactor, rename, or reorganize code opportunistically
- Do not add features, abstractions, or utilities beyond what the task explicitly requires
- Do not add comments, docstrings, or type annotations to code you did not change
- Do not add backwards-compatibility shims for things that are not being removed
- Three similar lines of code is better than a premature abstraction

Violations of the Minimal Diff Doctrine are grounds for PR rejection without review of the functional change.

---

## 3. Phase Gating and Freeze Rules

Work is organized into phases. Exactly one phase may be active at a time.

**Rules:**
- No code may be merged to `main` without an explicit phase definition or patch designation
- No cross-phase work is permitted in a single PR
- No opportunistic refactoring across phase boundaries
- Completed phases are frozen. Code from a completed phase may not be rewritten unless a new phase explicitly scopes that work
- No product work begins before Phase 0 exit criteria are met in full

Branch naming convention:
- `phase-0/...`
- `phase-1/...`
- `patch-0.1.x/...`

---

## 4. Layer Boundaries Principle

Repos powered by Aegis must define explicit architectural layers and enforce strict one-directional dependency flow. The canonical direction is:

```
UI → API → Application → Domain → Infrastructure → Persistence
```

**Rules:**
- No layer may import from a layer above it
- Domain is the innermost layer. It must not import from Application, Infrastructure, API, or UI
- Infrastructure contains persistence logic only. It must not contain business rules
- Application orchestrates domain objects and infrastructure calls. It must not import UI components
- UI presents data only. It must not call infrastructure directly
- Forbidden dependency directions are defined in `policy/config/policy.config.json` and enforced mechanically by `check-layer-drift.mjs`

---

## 5. Derived Data Must Not Be Stored

Any value that can be computed from source data must never be stored as a persistent field.

**Examples of forbidden persistence:**
- Completion percentage computed from task counts
- Aggregate status computed from child record states
- Counters derived from related record queries

**Rule:** If a value changes when source data changes, it is derived. Compute it at read time. Never write it to the database or persist it in shared state.

Violations are detected mechanically by `check-derived-data.mjs` using regex patterns defined in config.

---

## 6. Ordering Logic Locality Rule

Logic that determines the order of items (move up, move down, reorder) must live in application or domain code — not in database stored procedures, RPC functions, or external services — unless a phase explicitly scopes that migration.

This rule prevents ordering logic from drifting into the database layer where it becomes harder to test, version, and reason about.

---

## 7. Security-First Baseline

The following security rules are non-negotiable and apply to all repos powered by Aegis:

**No Secrets in Git:**
- No API keys, tokens, passwords, connection strings, or credentials may be committed to the repository under any circumstances
- `.env` and `.env.*` are always gitignored
- `policy/config/policy.config.json` is always gitignored (it may contain repo-specific paths or config that is not secret, but the pattern must be enforced to prevent accidents)

**Environment Discipline:**
- All environment-specific values are loaded from environment variables
- No environment-specific values are hardcoded in source files
- Local config files that reference environment values use `.env.local` or equivalent patterns that are gitignored

**Least Privilege:**
- Services and API clients are configured with the minimum permissions required
- No service role keys or admin credentials are exposed to client-side code

---

## 8. Governance Changes Require a Documented Patch

Any modification to this contract or any governance document in `governance/` must:

1. Use the patch template at `governance/PATCH_TEMPLATE.md`
2. Assign a Patch ID and increment the patch version
3. Be logged in `governance/PATCH_LOG.md`
4. Pass Codex verification before merge
5. Be reviewed as a standalone PR — not bundled with feature or bug fix work
