# Powered by Aegis

**Version:** 0.1.6
**Status:** Active

---

## Purpose

"Powered by Aegis" is a governance status applied to repos that have fully adopted the Aegis kit and have all required controls actively enforced. It is not a label applied at copy time — it is earned when minimum requirements are met and maintained.

Copying Aegis files into a repo does not make it Powered by Aegis. A repo qualifies only when the controls below are genuinely active.

---

## Minimum Requirements

A repo is Powered by Aegis when **all** of the following are true:

### 1. Governance Artifacts Adopted

- `governance/ENGINEERING_CONTRACT.md` is present and treated as binding
- `governance/AI_WORKFORCE_CONTRACT.md` is present and followed
- `governance/PHASES.md` defines the repo's active phase
- `governance/PATCH_TEMPLATE.md` and `governance/PATCH_LOG.md` are in use for structural changes

### 2. Policy Configuration Active

- `policy/config/policy.config.json` exists locally and is tuned to the repo's layer structure
- `policy/config/policy.config.json` is gitignored and never committed
- `baseline.required_paths` covers the repo's required governance and kit files

### 3. Policy Enforcement Running on Every PR

- `node policy/scripts/run-all.mjs` exits 0 from the repo root
- All four checks pass: `check-repo-baseline`, `check-layer-drift`, `check-derived-data`, `check-governance-files`
- The `pr-gates` CI workflow is active and runs on every PR targeting `main`

### 4. Merge-Blocking Posture Active

- GitHub branch protection is configured on `main`
- The `pr-gates` status check is required before merge
- Bypassing branch protection is disabled

### 5. Bootstrap / Adoption Documented

- The bootstrap or adoption runbook was followed (`BOOTSTRAP_NEW_PROJECT.md` or `ADOPT_AEGIS.md`)
- A `governance/PATCH_LOG.md` entry documents the initial adoption

### 6. Adopted Aegis Version Recorded

- The Aegis version in use at adoption time is recorded in `governance/PATCH_LOG.md`
- Any local deviations from the baseline are documented in that same entry

---

## Local Deviations and Customizations

Local policy customizations are permitted. A repo may define its own layers, forbidden dependency rules, derived data patterns, and required path lists in its local `policy.config.json`.

Any deviation from the Aegis baseline must be:
- Documented in `governance/PATCH_LOG.md` at adoption time
- Intentional — not an oversight or omission

Undocumented deviations are not permitted. A repo that silently omits required controls does not qualify as Powered by Aegis.

---

## Governance Status, Not Template Origin

"Powered by Aegis" reflects the current enforcement posture of a repo, not its history. A repo that copied Aegis files but:
- never configured `policy.config.json`
- never enabled branch protection
- never ran policy checks in CI

is not Powered by Aegis, regardless of how the files arrived.

Conversely, a repo that adopted Aegis incrementally through `ADOPT_AEGIS.md` and meets all requirements above is fully Powered by Aegis.

---

## Maintaining Powered-by-Aegis Status

A repo retains Powered-by-Aegis status as long as:

- All minimum requirements remain active
- Policy checks continue to pass in CI on every PR
- Governance changes are documented as patches
- No enforcement controls are silently disabled
