# Aegis v1 Readiness

**Status:** In Progress

---

## Purpose

This document defines the criteria that must be met before Aegis is considered v1.0 — stable, adoptable governance infrastructure.

**No Aegis-powered product repo begins before Aegis v1.0 readiness is formally declared.** This is a hard gate, not a guideline.

---

## v1 Readiness Checklist

### Governance Baseline

- [ ] `governance/ENGINEERING_CONTRACT.md` is complete and stable
- [ ] `governance/AI_WORKFORCE_CONTRACT.md` is complete and stable
- [ ] `governance/PHASES.md` defines Phase 0 exit criteria clearly
- [ ] `governance/PATCH_TEMPLATE.md` and `governance/PATCH_LOG.md` are in use and current
- [ ] `governance/GOVERNANCE_SENSITIVE_FILES.md` classifies sensitive files
- [ ] `governance/VERSION.md` tracks the current version
- [ ] `governance/V1_READINESS.md` (this file) defines and tracks v1 exit criteria

### Mechanical Enforcement Baseline

- [ ] `check-repo-baseline.mjs` passes on every PR
- [ ] `check-layer-drift.mjs` passes on every PR
- [ ] `check-derived-data.mjs` passes on every PR
- [ ] `check-governance-files.mjs` passes on every PR (enforced in CI)
- [ ] `run-all.mjs` is the stable CI entrypoint and exits 0
- [ ] GitHub Actions `pr-gates` workflow is active and merge-blocking on `main`

### Adoption Baseline

- [ ] `runbooks/BOOTSTRAP_NEW_PROJECT.md` is complete and verified repeatable
- [ ] `runbooks/ADOPT_AEGIS.md` is complete and verified repeatable
- [ ] `templates/PROJECT_BOOTSTRAP.md` is complete
- [ ] `.github/workflows/reusable-pr-gates.yml` is available for downstream repos
- [ ] `policy/config/policy.config.example.json` is stable and covers all kit files

### Operational Baseline

- [ ] All policy checks pass locally: `node policy/scripts/run-all.mjs` exits 0
- [ ] All policy checks pass in GitHub Actions on a real PR
- [ ] GitHub branch protection is active on `main` in the Aegis repo
- [ ] `governance/PATCH_LOG.md` reflects all applied patches through the current version
- [ ] No open governance gaps or known enforcement regressions

---

## Deferred / Post-v1 Items

The following are explicitly out of scope for v1.0 and may be addressed in later versions:

- Automated secret scanning
- Advanced SAST/DAST integration
- "Only allowed files changed" mechanical enforcement
- Mechanical enforcement of patch log entries
- Multi-repo governance sync tooling

---

## How v1 Readiness Is Declared

Meeting the checklist above does not automatically declare v1.0. Readiness criteria being met is a necessary condition, not a sufficient one. v1.0 becomes official only through a formal declaration artifact.

The declaration process:

1. All checklist items above are marked complete
2. The declaration template at [governance/V1_DECLARATION_TEMPLATE.md](governance/V1_DECLARATION_TEMPLATE.md) is filled out and committed as `governance/V1_DECLARATION.md`
3. A patch increments `governance/VERSION.md` to `1.0.0` and documents the declaration in `governance/PATCH_LOG.md`
4. `node policy/scripts/run-all.mjs` exits 0 from the Aegis repo root
5. The declaration patch passes CI and merges to `main`

After the declaration patch merges, product repos powered by Aegis may begin using the `runbooks/BOOTSTRAP_NEW_PROJECT.md` runbook.
