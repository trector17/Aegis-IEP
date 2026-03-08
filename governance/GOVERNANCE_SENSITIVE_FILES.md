# Aegis Governance-Sensitive Files

**Version:** 0.1.3
**Status:** Active

---

## Purpose

Certain files in an Aegis-powered repo carry higher risk when changed. Modifications to these files can silently weaken enforcement, alter governance rules, or break the contract between the platform and the teams using it. This document classifies those files and defines the required change discipline.

---

## Governance-Sensitive File Areas

| Area | Why it is sensitive |
|---|---|
| `governance/**` | Contains the binding engineering contract, AI workforce contract, phase definitions, patch process, and version record. Changes directly alter governance rules. |
| `policy/**` | Contains the enforcement scripts and config schema. Changes can alter or disable what the policy engine checks. |
| `.github/workflows/pr-gates.yml` | The active CI gate. Changes can weaken or disable merge-blocking enforcement. |
| `.github/workflows/reusable-pr-gates.yml` | The reusable gate for downstream repos. Changes affect all repos that call it. |
| `.github/pull_request_template.md` | Defines the required structure for every PR. Changes alter what reviewers are expected to evaluate. |

---

## Why These Files Require Extra Discipline

A change to a governance-sensitive file is not just a code change — it is a governance event. Weakening a policy check, removing a required PR field, or silently modifying an enforcement rule can propagate to every downstream repo and every PR that follows.

Because these files define the rules of the platform, they must be changed with the same care as the rules themselves.

---

## Required Change Discipline

Any PR that touches a governance-sensitive file must:

1. **Explicitly call it out in the patch scope** — the Scope section must name the governance-sensitive area being changed
2. **Assess the risk explicitly** — the Risk Assessment section must address what weakens or breaks if this change is wrong
3. **Document governance impact** — the Governance Impact section must describe the before/after of any rule or enforcement change
4. **Provide explicit verification** — the Verification Steps section must include commands confirming no enforcement regression
5. **Keep changes minimal** — governance-sensitive files are not a place for opportunistic cleanup or reformatting

Changes to governance-sensitive files should be rare, intentional, and reviewed as standalone PRs whenever possible.

---

## Future Enforcement

Future Aegis versions may add mechanical enforcement — for example, a policy check that flags PRs touching governance-sensitive files without a matching governance impact entry. For now, this is process-enforced by reviewers using the patch template and PR template.
