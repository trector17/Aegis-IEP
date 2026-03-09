# Runbook: Bootstrap a New Aegis-Powered Project

This runbook describes how to create a brand-new repository that is governed by Aegis from day one.

> **Prerequisite:** Do not bootstrap a product repo before Aegis v1.0 readiness is formally declared. See [governance/V1_READINESS.md](governance/V1_READINESS.md).

---

## Recommended Path: GitHub Template Repo

The cleanest approach is to use the Aegis repo as a GitHub Template Repository. This copies the full Aegis kit into a new repo with a clean git history.

### Step 1 — Enable Template on the Aegis Repo

In the Aegis GitHub repo: **Settings → General → Template repository** → enable.

### Step 2 — Create a New Repo from the Template

In GitHub: **Use this template → Create a new repository**. Give it a name and choose visibility.

This copies all committed Aegis kit files into the new repo with a fresh history.

### Step 3 — Clone and Verify

```bash
git clone https://github.com/your-org/your-new-repo.git
cd your-new-repo
node -v   # confirm Node 20+
node policy/scripts/run-all.mjs
```

Expected: all three checks pass with exit 0.

---

## Alternative Path: Manual Copy-In

If you cannot use GitHub Template Repos, copy the Aegis kit folders into a fresh repo manually.

### Step 1 — Initialize a new repo

```bash
git init your-new-repo
cd your-new-repo
```

### Step 2 — Copy Aegis kit folders

Copy the following from the Aegis repo root into your new repo root:

```
governance/
policy/
templates/
runbooks/
.github/
.gitignore
LICENSE
README.md
```

Do not copy `policy/config/policy.config.json` if it exists — that file is local and gitignored.

### Step 3 — Verify

```bash
node policy/scripts/run-all.mjs
```

Expected: exit 0.

---

## Step 4 — Create a Local Policy Config

The committed `policy/config/policy.config.example.json` is the default. Create a local override to tune it for your repo:

```bash
# Git Bash
cp policy/config/policy.config.example.json policy/config/policy.config.json
```

```powershell
# PowerShell
Copy-Item policy/config/policy.config.example.json policy/config/policy.config.json
```

Edit `policy/config/policy.config.json`:

- **`baseline.required_paths`** — update to match the files your repo must always contain
- **`layers`** — update `path_prefix` values to match your directory structure
- **`forbidden_dependencies`** — define the cross-layer imports your architecture forbids
- **`derived_data_patterns`** — add regex patterns for computed values specific to your domain

`policy.config.json` is gitignored and will never be committed.

---

## Step 5 — Enable GitHub Branch Protections

In your new repo: **Settings → Branches → Add branch protection rule** for `main`:

| Setting | Value |
|---|---|
| Require a pull request before merging | Enabled |
| Require status checks to pass before merging | Enabled |
| **Required status check name** | **`pr-gates`** |
| Require branches to be up to date before merging | Enabled |
| Do not allow bypassing the above settings | Enabled |

The status check name `pr-gates` is the exact `jobs` key in `.github/workflows/pr-gates.yml`. It must match exactly.

---

## Branch Naming Conventions

| Branch type | Convention |
|---|---|
| Phase work | `phase-0/short-description` |
| Phase work | `phase-1/short-description` |
| Governance patches | `patch-0.1.x/short-description` |
| Bug fixes | `fix/short-description` |

---

## Step 6 — Record the Adopted Aegis Version

In your new repo, note the following in your first `governance/PATCH_LOG.md` entry:

- **Aegis version adopted:** (check `governance/VERSION.md` in the Aegis repo at adoption time)
- **Adoption date:** YYYY-MM-DD
- **Major local customizations:** list any layer definitions, forbidden dependency rules, or derived data patterns you configured in `policy.config.json`

This record is your baseline for any future governance upgrade.

---

## First PR Checklist

Before merging the first PR into `main` on your new repo, verify:

- [ ] `node policy/scripts/run-all.mjs` exits 0 locally
- [ ] GitHub Actions `pr-gates` workflow passes in CI
- [ ] Branch protection rule is active and requires `pr-gates` to pass
- [ ] `policy/config/policy.config.json` is NOT committed (check `git status`)
- [ ] No secrets or env values are committed
- [ ] PR uses the `.github/pull_request_template.md` format
- [ ] `governance/PATCH_LOG.md` has an entry for the bootstrap patch with Aegis version recorded

When all items above are verified, the repo meets the minimum requirements to be considered Powered by Aegis. See [governance/POWERED_BY_AEGIS.md](governance/POWERED_BY_AEGIS.md) for the full definition.
