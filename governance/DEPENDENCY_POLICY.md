# Aegis Dependency Policy

**Version:** 1.0.0
**Status:** Active
**Phase:** 0 — Foundation

---

## Purpose

The Dependency Policy governs when dependencies may be added, upgraded, downgraded, or removed. Dependency changes carry structural risk: they expand the attack surface, introduce transitive vulnerabilities, affect bundle size, and can silently break reproducible builds. This policy defines the approval posture and constraints required before any dependency change merges.

---

## Scope

This policy applies to all dependency manifests and lockfiles in any Aegis-powered repository:

- `package.json` / `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml`
- `requirements.txt` / `pyproject.toml` / `poetry.lock` / `Pipfile.lock`
- `go.mod` / `go.sum`
- `Gemfile` / `Gemfile.lock`
- `Cargo.toml` / `Cargo.lock`
- Any other ecosystem-specific dependency manifest or lockfile

---

## Rules

### Adding a Dependency

A new dependency may only be added when:

1. The dependency solves a problem that cannot be reasonably solved with existing dependencies or standard library equivalents
2. The dependency is well-maintained, has a license compatible with the project, and has no known critical vulnerabilities at the pinned version
3. The addition is required by the current task — not added speculatively for future use
4. The PR description explicitly states: the dependency name, the problem it solves, and why existing dependencies are insufficient

**Default posture:** Skeptical. The burden of justification is on adding, not on rejecting.

### Upgrading a Dependency

A dependency upgrade is permitted when:

1. The upgrade addresses a known security vulnerability — highest priority, merge with minimal review when no breaking changes are introduced
2. The upgrade is strictly required by the current task (e.g., a new API or bug fix needed for the feature in scope)
3. The upgrade is part of a dedicated dependency maintenance PR scoped to upgrades only

Dependency upgrades must not be bundled with feature or bug fix work unless the upgrade is strictly required to accomplish that work.

### Downgrading a Dependency

A dependency downgrade is a high-risk operation and requires:

1. An explicit explanation of why the current version is unacceptable
2. Confirmation that the downgraded version satisfies the security requirements of the codebase
3. Documentation of any behavior differences between versions and their impact on the repo

### Removing a Dependency

A dependency may be removed when:

1. The code that used it has been removed or replaced as part of the current task
2. A confirmed audit shows no remaining usages in the codebase

Dependency removal should be included in the same PR as the code removal — not deferred to a separate cleanup pass.

---

## Lockfile Discipline

- Lockfiles must always be committed alongside manifest changes
- Lockfile-only changes (e.g., from `npm install` without version changes) must not be silently included in unrelated PRs
- Lockfile changes must represent the expected diff from the stated manifest change — unexplained transitive resolution changes must be investigated before merge

---

## Security Posture

- No dependency with a known critical or high severity CVE may be added
- Existing dependencies with active critical CVEs must be upgraded or replaced in a dedicated patch — deferral is not acceptable
- Dependencies must not be pinned to commit hashes or non-release tags unless a documented exception exists and is recorded in the PR

---

## Relationship to Other Doctrine

- **MINIMAL_DIFF.md** — dependency changes are subject to the same scope constraints; do not upgrade unrelated packages when the task only requires adding a new one
- **FILE_SCOPE_POLICY.md** — manifest and lockfile changes are in scope only when a dependency change is the stated task
- **REFACTOR_POLICY.md** — dependency consolidation (replacing multiple packages with one equivalent) is a refactor-class change and must be scoped accordingly
