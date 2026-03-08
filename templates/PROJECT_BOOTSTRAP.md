# Project Bootstrap Checklist

**Repo:** [your-repo-name]
**Generated from:** Aegis IEP
**Date:** YYYY-MM-DD

---

## Purpose

This checklist guides the first engineer to set up a newly created Aegis-powered repo. Complete every step before opening the first feature PR.

---

## What This Repo Inherited from Aegis

| Area | What you got |
|---|---|
| `governance/` | Engineering Contract, AI Workforce Contract, Phase definitions, Patch template, Patch log |
| `policy/` | Three enforcement scripts + example config + README |
| `templates/` | PRD, Architecture, ADR, and this bootstrap checklist |
| `runbooks/` | Bootstrap and adoption runbooks |
| `.github/` | PR template, CI workflow (`pr-gates`), reusable gate workflow |

---

## Immediate Setup Steps

### 1 — Create a local policy config

```bash
# Git Bash
cp policy/config/policy.config.example.json policy/config/policy.config.json
```

```powershell
# PowerShell
Copy-Item policy/config/policy.config.example.json policy/config/policy.config.json
```

`policy.config.json` is gitignored. It must never be committed.

### 2 — Tune layers and forbidden dependencies

Edit `policy/config/policy.config.json`:

- **`baseline.required_paths`** — update to match the files this repo must always contain
- **`layers`** — set `path_prefix` values to match your directory structure
- **`forbidden_dependencies`** — define the cross-layer imports your architecture forbids
- **`derived_data_patterns`** — add regex patterns for computed values in your domain model

### 3 — Run all policy checks locally

```bash
node policy/scripts/run-all.mjs
```

Expected: all three checks pass, exit 0. Fix any failures before proceeding.

### 4 — Push the repo to GitHub

```bash
git remote add origin https://github.com/your-org/your-repo.git
git branch -M main
git push -u origin main
```

### 5 — Enable branch protection on main

In GitHub: **Settings → Branches → Add branch protection rule** for `main`:

| Setting | Value |
|---|---|
| Require a pull request before merging | Enabled |
| Require status checks to pass before merging | Enabled |
| **Required status check name** | **`pr-gates`** |
| Require branches to be up to date before merging | Enabled |
| Do not allow bypassing the above settings | Enabled |

### 6 — Open a test PR

Create a branch, make a trivial change, push, and open a PR against `main`.

Confirm:
- The `pr-gates` workflow triggers automatically
- All three checks pass in GitHub Actions
- The PR shows a green `pr-gates` status check

Once confirmed, you may merge and delete the test branch.

---

## First-Adoption Checklist

- [ ] `policy/config/policy.config.json` created locally and tuned
- [ ] `node policy/scripts/run-all.mjs` exits 0
- [ ] Repo pushed to GitHub
- [ ] Branch protection active on `main` with `pr-gates` required
- [ ] Test PR opened and `pr-gates` CI passed
- [ ] `policy/config/policy.config.json` is NOT in git history (verify with `git log --all --full-history -- policy/config/policy.config.json`)
- [ ] No secrets committed (verify with `git log -p | grep -i "secret\|token\|password\|key"` — expect no results)
- [ ] Team has read `governance/ENGINEERING_CONTRACT.md`
- [ ] First real PR uses the `.github/pull_request_template.md` format
- [ ] Bootstrap patch entry added to `governance/PATCH_LOG.md` including:
  - Aegis version adopted (from `governance/VERSION.md` in the Aegis repo)
  - Adoption date
  - Initial governance/policy customizations (layers defined, forbidden deps configured, derived data patterns added)

---

## Governance Discipline Notes

**Follow Minimal Diff Doctrine from commit one.** Every PR must modify only the files required for the stated task. No opportunistic refactors, no speculative abstractions.

**Phase hygiene:** Define your Phase 1 scope in `governance/PHASES.md` before writing any product code. No code merges to `main` without a phase or patch designation.

**Initial patch hygiene:** The bootstrap itself is patch-0.1.0 (already logged in `governance/PATCH_LOG.md`). Any structural change you make before your first product phase should be logged as a patch entry using `governance/PATCH_TEMPLATE.md`.

**Governance changes require a documented patch.** Any modification to documents in `governance/` must follow the patch process and pass Codex verification before merge.
