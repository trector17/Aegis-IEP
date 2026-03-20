# Aegis Patch Log

This file records every governance patch applied to the Aegis Project Kit. Entries are append-only. Never modify or delete a past entry.

---

## patch-0.1.1

**Date:** 2026-03-18
**Phase:** Phase 0 — Foundation
**Summary:** Adds four Dev Engine doctrine files that complete the governance layer: MINIMAL_DIFF.md, FILE_SCOPE_POLICY.md, DEPENDENCY_POLICY.md, and REFACTOR_POLICY.md. Adds cross-references in README.md under "Where Governance Lives."
**Scope:** `governance/MINIMAL_DIFF.md` (new), `governance/FILE_SCOPE_POLICY.md` (new), `governance/DEPENDENCY_POLICY.md` (new), `governance/REFACTOR_POLICY.md` (new), `README.md` (cross-reference addition only)
**Verification status:** Pending — `node policy/scripts/run-all.mjs` must pass locally and in CI
**Notes:** All four files are net-new governance doctrine. No existing governance, policy, runbook, template, capability, or skill files were modified beyond the minimal README cross-reference.

---

## patch-0.1.0

**Date:** YYYY-MM-DD
**Phase:** Phase 0 — Foundation
**Summary:** Initial creation of the Aegis Project Kit. Establishes the full Phase 0 foundation including governance documents, policy scripts, CI gates, PR template, runbooks, and project templates.
**Scope:** All 21 files in the Phase 0 deliverables list (see `governance/PHASES.md`)
**Verification status:** Pending — CI gates must pass locally and in GitHub Actions before Phase 0 exits
**Notes:** This is the bootstrap patch. No prior state exists. All files are net-new.
