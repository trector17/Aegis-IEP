# Aegis Version

**Version:** 1.0.0
**Status:** Stable
**Release date:** 2026-03-09

---

## What This Version Includes

- Full Phase 0 kit: governance docs, policy scripts, CI gates, PR template, runbooks, templates
- `templates/PROJECT_BOOTSTRAP.md` — bootstrap checklist for newly created Aegis-powered repos
- `.github/workflows/reusable-pr-gates.yml` — reusable gate workflow for downstream repos
- `governance/GOVERNANCE_SENSITIVE_FILES.md` — sensitive file classification and change discipline
- `governance/V1_READINESS.md` — v1 readiness checklist and declaration process
- `governance/V1_DECLARATION_TEMPLATE.md` — template for formal v1 declaration
- `governance/V1_DECLARATION.md` — formal declaration of Aegis v1.0.0 (this release)
- `governance/POWERED_BY_AEGIS.md` — definition of Powered-by-Aegis governance status
- `aegis.json` — machine-readable platform metadata
- `policy/scripts/check-governance-files.mjs` — mechanical enforcement for governance-sensitive changes

---

## v1.0.0 Declaration

Aegis v1.0.0 is formally declared stable and adoptable as of 2026-03-09. The formal declaration artifact is at [governance/V1_DECLARATION.md](governance/V1_DECLARATION.md).

Aegis-powered product repos may now begin using the `runbooks/BOOTSTRAP_NEW_PROJECT.md` runbook.

---

## Post-v1 Work

Aegis v1.1 work has begun. The first patch (v1.1.0-a) introduces the Capability Graph foundation: a formal model, core capability vocabulary, and graph rules that define the abstraction layer between Aegis core, skills, agents, and downstream products. See `capabilities/` for these artifacts.

The second patch (v1.1.0-b) adds the Skills System foundation: a governed specification standard for packaging capability implementations, including folder layout, required metadata fields, required body sections, and an annotated example. See `skills/` for these artifacts.

---

## Versioning Notes

**For downstream repos:** Record the Aegis version you adopted at bootstrap time (see `templates/PROJECT_BOOTSTRAP.md` and the adoption runbooks). This creates a clear reference point for any future governance upgrades.

**For governance upgrades:** Future updates to Aegis governance should be applied deliberately — reviewed, documented as a patch, and verified before adoption. Do not copy changes ad hoc. Each upgrade is a governance event and should be treated as one.
