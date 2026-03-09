# Aegis Version

**Version:** 0.1.7
**Status:** Pre-v1
**Release date:** YYYY-MM-DD

---

## What This Version Includes

- Full Phase 0 kit: governance docs, policy scripts, CI gates, PR template, runbooks, templates
- `templates/PROJECT_BOOTSTRAP.md` — bootstrap checklist for newly created Aegis-powered repos
- `.github/workflows/reusable-pr-gates.yml` — reusable gate workflow for downstream repos

---

## Path to v1.0

The current version is pre-v1.0. Aegis is progressing toward a stable v1.0 declaration through Phase 0 hardening patches. v1 readiness criteria are defined in [governance/V1_READINESS.md](governance/V1_READINESS.md).

Meeting the readiness criteria does not automatically declare v1.0. A formal declaration artifact must be produced using [governance/V1_DECLARATION_TEMPLATE.md](governance/V1_DECLARATION_TEMPLATE.md) and committed as `governance/V1_DECLARATION.md` via a standalone governance patch. This file's version field is incremented to `1.0.0` only at that point.

No Aegis-powered product repo begins before v1.0 is formally declared.

---

## Versioning Notes

**For downstream repos:** Record the Aegis version you adopted at bootstrap time (see `templates/PROJECT_BOOTSTRAP.md` and the adoption runbooks). This creates a clear reference point for any future governance upgrades.

**For governance upgrades:** Future updates to Aegis governance should be applied deliberately — reviewed, documented as a patch, and verified before adoption. Do not copy changes ad hoc. Each upgrade is a governance event and should be treated as one.
