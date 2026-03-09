# Aegis v1.0 Declaration Template

Use this template to formally declare Aegis v1.0. Copy this file, fill in all sections, and commit the completed declaration as `governance/V1_DECLARATION.md` via a standalone governance patch.

A completed declaration artifact is required before any Aegis-powered product repo begins.

---

## Declaration Title

Aegis v1.0 — Formal Readiness Declaration

## Version

`1.0.0`

## Date

YYYY-MM-DD

## Readiness Criteria Reference

All v1 readiness criteria are defined in [governance/V1_READINESS.md](governance/V1_READINESS.md). This declaration affirms that every item in that checklist has been verified.

---

## Readiness Evidence Summary

Provide a brief, concrete summary of how each readiness area was verified.

**Governance Baseline:**

(Describe: which governance docs are complete and stable, when they were last reviewed)

**Mechanical Enforcement Baseline:**

(Describe: policy check results, CI run link or confirmation, branch protection status)

**Adoption Baseline:**

(Describe: runbook verification — was BOOTSTRAP_NEW_PROJECT.md followed? Was ADOPT_AEGIS.md reviewed?)

**Operational Baseline:**

(Describe: confirmation that run-all.mjs exits 0 locally and in GitHub Actions, PATCH_LOG.md is current)

---

## Deferred / Post-v1 Items Acknowledged

The following items were reviewed and confirmed deferred to post-v1.0 per [governance/V1_READINESS.md](governance/V1_READINESS.md):

- Automated secret scanning
- Advanced SAST/DAST integration
- "Only allowed files changed" mechanical enforcement
- Mechanical enforcement of patch log entries
- Multi-repo governance sync tooling

(Add or remove items as appropriate to reflect what was actually deferred at time of declaration)

---

## Formal Declaration Statement

Aegis version 1.0.0 is hereby declared stable and adoptable.

All v1 readiness criteria defined in `governance/V1_READINESS.md` have been met. The deferred items listed above are acknowledged as intentional exclusions from v1 scope. Aegis-powered product repos may now begin using the `runbooks/BOOTSTRAP_NEW_PROJECT.md` runbook.

This declaration is version-controlled, patch-documented, and binding. It may not be revoked without a subsequent governance patch.

---

## Signoff / Approval

| Role | Name / Agent | Date |
|---|---|---|
| Architect | | YYYY-MM-DD |
| Builder | | YYYY-MM-DD |
| Verifier | | YYYY-MM-DD |
