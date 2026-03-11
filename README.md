# Aegis — Internal Engineering Platform

Aegis is a reusable, AI-governed engineering infrastructure that produces high-quality software projects with startup-grade discipline from day one.

**Aegis is the platform. Individual applications are products powered by Aegis.**

---

## Mission

Every repo powered by Aegis ships with:

- Binding governance documents that define how the team works
- Mechanical policy enforcement that catches architectural drift before it merges
- A structured AI workforce model that keeps each agent in its lane
- PR and patch templates that make every change reviewable and traceable
- Runbooks that make bootstrapping and adoption repeatable

Aegis is stack-agnostic. It requires only Node.js 20+ for its policy scripts and has no external dependencies.

---

## What the Project Kit Includes

| Area | Contents |
|---|---|
| `governance/` | Engineering Contract, AI Workforce Contract, Phase definitions, Patch template, Patch log |
| `policy/` | Policy scripts, example config, README |
| `templates/` | PRD template, Architecture template, ADR template, Project bootstrap checklist |
| `runbooks/` | Bootstrap new project, Adopt Aegis into existing repo |
| `.github/` | PR template, CI workflow (`pr-gates`), reusable gate workflow for downstream repos |

---

## Where Governance Lives

All governance rules are in `governance/`. These documents are version-controlled and binding:

- [governance/ENGINEERING_CONTRACT.md](governance/ENGINEERING_CONTRACT.md) — the law: Minimal Diff Doctrine, phase gating, layer boundaries, derived data rule, security baseline
- [governance/AI_WORKFORCE_CONTRACT.md](governance/AI_WORKFORCE_CONTRACT.md) — AI agent roles, boundaries, and handoff protocol
- [governance/PHASES.md](governance/PHASES.md) — phase definitions and exit criteria
- [governance/PATCH_TEMPLATE.md](governance/PATCH_TEMPLATE.md) — how to document any structural change
- [governance/PATCH_LOG.md](governance/PATCH_LOG.md) — record of every patch applied
- [governance/GOVERNANCE_SENSITIVE_FILES.md](governance/GOVERNANCE_SENSITIVE_FILES.md) — files that require explicit documentation when changed

---

## How Policy Enforcement Works

Three policy scripts enforce architectural invariants on every PR:

| Script | What it checks |
|---|---|
| `check-repo-baseline.mjs` | All required kit files are present |
| `check-layer-drift.mjs` | No forbidden cross-layer imports |
| `check-derived-data.mjs` | No derived/computed values are persisted |

All three run via a single stable entrypoint:

```bash
node policy/scripts/run-all.mjs
```

This is also the CI command. The GitHub Actions workflow `pr-gates` runs this on every pull request targeting `main`. The workflow job name is exactly `pr-gates` — this is the name configured in GitHub branch protection as a required status check.

Policy rules are configured in `policy/config/policy.config.json` (local, gitignored) or `policy/config/policy.config.example.json` (committed default). See [policy/README.md](policy/README.md) for full details.

---

## What "Powered by Aegis" Means

"Powered by Aegis" is a governance status — not a label applied at file copy time. A repo qualifies only when governance artifacts are adopted, policy enforcement is active in CI, branch protection is merge-blocking, and the adopted Aegis version is recorded.

The formal definition and minimum requirements are in [governance/POWERED_BY_AEGIS.md](governance/POWERED_BY_AEGIS.md).

---

## How Future Repos Become Powered by Aegis

There are two adoption paths:

**New repo:** Use the Aegis repo as a GitHub Template Repository. See [runbooks/BOOTSTRAP_NEW_PROJECT.md](runbooks/BOOTSTRAP_NEW_PROJECT.md).

**Existing repo:** Copy the Aegis kit folders in and enable enforcement incrementally. See [runbooks/ADOPT_AEGIS.md](runbooks/ADOPT_AEGIS.md).

Both paths result in:
1. The Aegis governance and policy kit present in the repo
2. CI gates running on every PR
3. GitHub branch protection requiring `pr-gates` to pass before merge
4. A local `policy/config/policy.config.json` tuned to the repo's layer structure

---

## Versioning

Aegis is versioned governance infrastructure. The current version is tracked in [`governance/VERSION.md`](governance/VERSION.md).

When a downstream repo adopts Aegis, it should record the adopted version, adoption date, and any local policy customizations. This creates a clear reference point for future governance upgrades.

Future Aegis updates should be applied intentionally — reviewed, documented as a patch, and verified — not copied ad hoc.

---

## Capability Layer (v1.1)

Aegis v1.1 introduces a **Capability Graph** — the abstraction layer between Aegis core, skills, agents, and downstream products. The capability layer defines the platform language of work: every skill, agent, and product integration is described in terms of named, stable capability identifiers.

- [`capabilities/CAPABILITY_MODEL.md`](capabilities/CAPABILITY_MODEL.md) — what capabilities are, node types, and the core-vs-extension model
- [`capabilities/CAPABILITY_CATALOG.md`](capabilities/CAPABILITY_CATALOG.md) — the initial core capability vocabulary
- [`capabilities/GRAPH_RULES.md`](capabilities/GRAPH_RULES.md) — allowed relationships, routing principles, and extension rules

---

## v1.0.0 — Formally Declared Stable

Aegis v1.0.0 is formally declared stable as of 2026-03-09. Aegis-powered product repos may now begin using the bootstrap runbook.

- Formal declaration: [governance/V1_DECLARATION.md](governance/V1_DECLARATION.md)
- Readiness criteria: [governance/V1_READINESS.md](governance/V1_READINESS.md)
- Declaration template: [governance/V1_DECLARATION_TEMPLATE.md](governance/V1_DECLARATION_TEMPLATE.md)

---

## Phase 0 Scope

Phase 0 establishes the Aegis Project Kit. It is the prerequisite for all product work.

**In-scope:** Governance docs, policy scripts, CI gates, PR template, runbooks, templates.

**Out-of-scope:** Any product or client application, advanced SAST/DAST, secret scanning automation.

**Exit criteria:** All policy checks pass locally and in GitHub Actions. Runbooks are clear and repeatable. Merge-blocking posture is documented and active.

See [governance/PHASES.md](governance/PHASES.md) for full exit criteria and GitHub branch protection settings.

---

## Running Checks Locally

```bash
# All checks (matches CI)
node policy/scripts/run-all.mjs

# Individual checks
node policy/scripts/check-repo-baseline.mjs
node policy/scripts/check-layer-drift.mjs
node policy/scripts/check-derived-data.mjs
```

Node.js 20+ is required. No npm install needed.

---

## Platform Metadata

Aegis includes a machine-readable platform metadata file at [`aegis.json`](aegis.json). It records the platform name, current version, and status. This supports downstream tooling and platform identification without parsing governance documents.

CI initialization test