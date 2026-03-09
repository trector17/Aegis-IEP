# Aegis v1.0 — Formal Declaration

## Declaration Title

Aegis v1.0 — Formal Readiness Declaration

## Version

`1.0.0`

## Date

2026-03-09

## Readiness Criteria Reference

All v1 readiness criteria are defined in [governance/V1_READINESS.md](governance/V1_READINESS.md). This declaration affirms that every item in that checklist has been verified.

---

## Readiness Evidence Summary

**Governance Baseline:**

All governance artifacts are present, committed, and stable: `ENGINEERING_CONTRACT.md`, `AI_WORKFORCE_CONTRACT.md`, `PHASES.md`, `PATCH_TEMPLATE.md`, `PATCH_LOG.md`, `GOVERNANCE_SENSITIVE_FILES.md`, `VERSION.md`, `V1_READINESS.md`, `V1_DECLARATION_TEMPLATE.md`, `POWERED_BY_AEGIS.md`. Each document was authored, reviewed, and patch-documented through patches 0.1.0–0.1.8. No open governance gaps exist.

**Mechanical Enforcement Baseline:**

All four policy checks pass locally (`node policy/scripts/run-all.mjs` exits 0): `check-repo-baseline`, `check-layer-drift`, `check-derived-data`, `check-governance-files`. The `pr-gates` GitHub Actions workflow is active and merge-blocking on `main`. Branch protection is configured and requires `pr-gates` to pass before merge. Baseline validates 27 required paths. No known enforcement regressions.

**Adoption Baseline:**

`runbooks/BOOTSTRAP_NEW_PROJECT.md` and `runbooks/ADOPT_AEGIS.md` are complete, include v1 readiness prerequisites, and reference the Powered-by-Aegis definition. `templates/PROJECT_BOOTSTRAP.md` is complete. `.github/workflows/reusable-pr-gates.yml` is available for downstream repos. `policy/config/policy.config.example.json` is stable and covers all 27 kit files. All adoption paths are documented and verified.

**Operational Baseline:**

`node policy/scripts/run-all.mjs` exits 0 from the repo root. The `pr-gates` workflow has run and passed on real PRs throughout the patch series (patches 0.1.1–0.1.8). GitHub branch protection is active on `main`. `governance/PATCH_LOG.md` covers patches through the current series. No open operational gaps.

---

## Deferred / Post-v1 Items Acknowledged

The following items were reviewed and confirmed deferred to post-v1.0 per [governance/V1_READINESS.md](governance/V1_READINESS.md):

- Automated secret scanning
- Advanced SAST/DAST integration
- "Only allowed files changed" mechanical enforcement
- Mechanical enforcement of patch log entries
- Multi-repo governance sync tooling

---

## Formal Declaration Statement

Aegis version 1.0.0 is hereby declared stable and adoptable.

All v1 readiness criteria defined in `governance/V1_READINESS.md` have been met. The deferred items listed above are acknowledged as intentional exclusions from v1 scope. Aegis-powered product repos may now begin using the `runbooks/BOOTSTRAP_NEW_PROJECT.md` runbook.

This declaration is version-controlled, patch-documented, and binding. It may not be revoked without a subsequent governance patch.

---

## Signoff / Approval

| Role | Name / Agent | Date |
|---|---|---|
| Architect / Controller | ChatGPT | 2026-03-09 |
| Builder | Claude Code | 2026-03-09 |
| Verifier | Codex | 2026-03-09 |
