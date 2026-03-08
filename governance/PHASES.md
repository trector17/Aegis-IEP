# Aegis Phase Definitions

**Version:** 0.1.0
**Status:** Active

---

## Governing Rule

No product work begins before Phase 0 exit criteria are fully met. Phase 0 is a prerequisite for all subsequent phases in every repo powered by Aegis. This is not negotiable.

Only one phase may be active at a time. Cross-phase work in a single PR is forbidden.

---

## Phase 0 — Aegis Foundation

**Status:** Active
**Branch prefix:** `phase-0/...`
**Patch prefix:** `patch-0.1.x/...`

### Purpose

Bootstrap the Aegis Project Kit. Establish governance, policy enforcement, CI gates, PR template, runbooks, and reusable templates as a self-contained, stack-agnostic kit that any downstream repo can adopt.

### Deliverables

| File | Description |
|---|---|
| `governance/ENGINEERING_CONTRACT.md` | Binding engineering rules and doctrine |
| `governance/AI_WORKFORCE_CONTRACT.md` | AI agent role definitions and handoff protocol |
| `governance/PHASES.md` | Phase definitions and exit criteria (this file) |
| `governance/PATCH_TEMPLATE.md` | Standard patch documentation format |
| `governance/PATCH_LOG.md` | Patch history log |
| `policy/config/policy.config.example.json` | Default policy configuration (committed) |
| `policy/scripts/check-repo-baseline.mjs` | Validates required kit files exist |
| `policy/scripts/check-layer-drift.mjs` | Detects forbidden cross-layer imports |
| `policy/scripts/check-derived-data.mjs` | Detects persisted derived values |
| `policy/scripts/run-all.mjs` | Stable CI entrypoint for all policy checks |
| `policy/README.md` | Policy system documentation |
| `templates/PRD_TEMPLATE.md` | Product requirements document template |
| `templates/ARCHITECTURE_TEMPLATE.md` | Architecture documentation template |
| `templates/ADR_TEMPLATE.md` | Architecture decision record template |
| `runbooks/BOOTSTRAP_NEW_PROJECT.md` | How to create a new Aegis-powered repo |
| `runbooks/ADOPT_AEGIS.md` | How to bring Aegis into an existing repo |
| `.github/pull_request_template.md` | PR template with all required governance fields |
| `.github/workflows/pr-gates.yml` | CI workflow that runs policy checks on every PR |
| `.gitignore` | Standard ignores including policy.config.json |
| `LICENSE` | MIT License |
| `README.md` | Project overview and getting started |

### In-Scope

- Creating the Aegis Project Kit (all files listed above)
- Making CI gates runnable in the Aegis repo itself
- Documenting exact GitHub settings required for merge-blocking posture
- Documenting the required GitHub status check name (`pr-gates`)

### Out-of-Scope

- Any client or product repo
- Advanced SAST/DAST or automated secret scanning
- "Only allowed files changed" enforcement
- Demo sandbox applications
- Any feature work beyond the kit itself

### Exit Criteria

Phase 0 is complete when **all** of the following are true:

1. **CI gates pass locally:** `node policy/scripts/run-all.mjs` exits 0 from the repo root
2. **CI gates pass in GitHub Actions:** The `pr-gates` workflow completes successfully on a PR targeting `main`
3. **Runbooks are clear and repeatable:** A new contributor can follow `BOOTSTRAP_NEW_PROJECT.md` and `ADOPT_AEGIS.md` without external help
4. **README explains Aegis adoption:** The root `README.md` explains how future repos become powered by Aegis
5. **Merge-blocking posture is documented:** The runbook documents the exact GitHub branch protection settings required
6. **Required GitHub status check name matches workflow job name:** The workflow job name is exactly `pr-gates`, matching what branch protection will require

### GitHub Branch Protection Requirements

To enforce merge-blocking on the Aegis repo itself, configure the following in **Settings → Branches → Branch protection rules** for `main`:

| Setting | Value |
|---|---|
| Require a pull request before merging | Enabled |
| Require status checks to pass before merging | Enabled |
| Required status check name | `pr-gates` |
| Require branches to be up to date before merging | Enabled |
| Do not allow bypassing the above settings | Enabled |

The required status check name (`pr-gates`) must exactly match the `jobs.<job-id>` key in `.github/workflows/pr-gates.yml`.

---

## v1 Readiness Gate

Phase 0 hardening patches may continue after Phase 0's initial exit criteria are met. All hardening patches follow the same patch process and are tracked in `governance/PATCH_LOG.md`.

No product work begins — in this repo or in any Aegis-powered downstream repo — until Aegis v1.0 readiness is formally declared. See [governance/V1_READINESS.md](governance/V1_READINESS.md) for the full checklist and declaration criteria.

---

## Future Phases

Future phases are defined when Phase 0 exits cleanly and v1 readiness is declared. They are not scoped here. Each phase will follow the same structure: deliverables, in-scope, out-of-scope, exit criteria.
