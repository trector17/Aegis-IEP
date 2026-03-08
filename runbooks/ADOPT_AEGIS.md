# Runbook: Adopt Aegis in an Existing Repo

This runbook describes how to bring Aegis governance and policy enforcement into a repo that already has ongoing development. The goal is incremental adoption — add enforcement gates without breaking current work.

---

## Guiding Principle

Start with the minimum footprint. Enable checks one at a time. Validate that each gate passes before enabling the next. Never add all enforcement at once to a repo with existing code — it will produce a wall of violations that is hard to triage.

---

## Step 1 — Copy Aegis Folders into Your Repo

From the Aegis repo, copy the following into your existing repo root:

```
governance/
policy/
templates/
runbooks/
.github/pull_request_template.md
.github/workflows/pr-gates.yml
```

Do not overwrite existing files without reviewing conflicts. If you already have a `.gitignore`, merge the Aegis entries into it (see the Aegis `.gitignore` for the required additions).

Required `.gitignore` additions:
```
.env
.env.*
policy/config/policy.config.json
```

---

## Step 2 — Create a Local Policy Config

```bash
# Git Bash
cp policy/config/policy.config.example.json policy/config/policy.config.json
```

```powershell
# PowerShell
Copy-Item policy/config/policy.config.example.json policy/config/policy.config.json
```

Edit `policy/config/policy.config.json`:

1. Set `baseline.required_paths` to only the governance and policy files you just added (not your product files — start narrow)
2. Set `layers` to match your repo's directory structure
3. Leave `forbidden_dependencies` empty (`[]`) for now — you will add these incrementally
4. Leave `derived_data_patterns` empty (`[]`) for now

`policy.config.json` is gitignored and will never be committed.

---

## Step 3 — Recommended Incremental Rollout

Adopt enforcement in this order. Each step is a separate PR. Do not combine steps.

### 3a — Governance + PR Template Only

Merge the governance docs and PR template. No CI changes yet.

Validate:
- Team members can read and understand the governance contract
- PRs use the new template format

### 3b — Baseline Check

Enable `check-repo-baseline.mjs` in CI by merging the `pr-gates.yml` workflow.

At this stage, `baseline.required_paths` should only list the Aegis kit files you added. Do not yet list every file in your repo.

Validate:
```bash
node policy/scripts/check-repo-baseline.mjs
# Expected: exit 0
```

Fix any missing required paths before merging.

### 3c — Layer Drift Check

Add your layer definitions and first forbidden dependency rules to `policy.config.json`.

Start with the most critical boundary — typically the domain layer must not import infrastructure.

Run the check to see what violations exist:
```bash
node policy/scripts/check-layer-drift.mjs
```

If violations are found, fix them before enabling the check in CI. Each violation is a real architectural boundary breach — fix the imports, not the rules.

Once clean:
```bash
node policy/scripts/run-all.mjs
# Expected: exit 0
```

### 3d — Derived Data Tuning

Add derived data patterns relevant to your domain model. Run the check:

```bash
node policy/scripts/check-derived-data.mjs
```

If violations are found, refactor the code to remove the persisted derived values before enabling this check in CI.

---

## Step 4 — Enable GitHub Branch Protections

Once all three checks pass locally and in CI:

In your repo: **Settings → Branches → Add branch protection rule** for `main`:

| Setting | Value |
|---|---|
| Require a pull request before merging | Enabled |
| Require status checks to pass before merging | Enabled |
| **Required status check name** | **`pr-gates`** |
| Require branches to be up to date before merging | Enabled |
| Do not allow bypassing the above settings | Enabled |

---

## Step 5 — Record the Adopted Aegis Version

In your repo's first governance patch entry (`governance/PATCH_LOG.md`), record:

- **Aegis version adopted:** (check `governance/VERSION.md` in the Aegis repo at adoption time)
- **Adoption date:** YYYY-MM-DD
- **Deviations from baseline:** any governance rules you did not adopt, any layers you renamed, any patterns you skipped

This record is your baseline for any future Aegis governance upgrade. Upgrades should be applied deliberately, not copied ad hoc.

---

## Validation Checklist

- [ ] `node policy/scripts/run-all.mjs` exits 0 locally
- [ ] GitHub Actions `pr-gates` workflow passes on a test PR
- [ ] Branch protection is active and requires `pr-gates` to pass
- [ ] `policy/config/policy.config.json` is gitignored and not committed
- [ ] All layer violations from `check-layer-drift.mjs` have been fixed in code
- [ ] All derived data violations from `check-derived-data.mjs` have been fixed in code
- [ ] Team has reviewed `governance/ENGINEERING_CONTRACT.md`
- [ ] First PR uses the new PR template format
- [ ] Adopted Aegis version and customizations recorded in `governance/PATCH_LOG.md`
