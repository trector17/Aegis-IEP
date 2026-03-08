# Aegis Version

**Version:** 0.1.1
**Status:** Active
**Release date:** YYYY-MM-DD

---

## What This Version Includes

- Full Phase 0 kit: governance docs, policy scripts, CI gates, PR template, runbooks, templates
- `templates/PROJECT_BOOTSTRAP.md` — bootstrap checklist for newly created Aegis-powered repos
- `.github/workflows/reusable-pr-gates.yml` — reusable gate workflow for downstream repos

---

## Versioning Notes

**For downstream repos:** Record the Aegis version you adopted at bootstrap time (see `templates/PROJECT_BOOTSTRAP.md` and the adoption runbooks). This creates a clear reference point for any future governance upgrades.

**For governance upgrades:** Future updates to Aegis governance should be applied deliberately — reviewed, documented as a patch, and verified before adoption. Do not copy changes ad hoc. Each upgrade is a governance event and should be treated as one.
