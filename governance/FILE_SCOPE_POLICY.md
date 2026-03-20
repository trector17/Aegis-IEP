# Aegis File Scope Policy

**Version:** 1.0.0
**Status:** Active
**Phase:** 0 — Foundation

---

## Purpose

The File Scope Policy defines which files may be touched in a given change, what constitutes an in-scope vs. out-of-scope file, and the required discipline for touching governance-sensitive file areas. It operationalizes the Minimal Diff Doctrine at the file level.

---

## Core Rule

Every PR must identify its scope boundary before making changes. A file is in scope only if one of the following is true:

1. The file must be created to deliver the task's output
2. The file must be modified because its current state is incorrect or incomplete relative to the task goal
3. The file must be deleted because its continued existence creates a problem the task is solving
4. The file is a governance-required artifact (patch log, version record, etc.) that must be updated as a direct consequence of the change

No other files may be touched.

---

## Governance-Sensitive File Areas

Files in the following areas require additional discipline beyond standard file scope rules:

| Area | Sensitivity |
|---|---|
| `governance/**` | Binding platform rules — changes alter engineering law |
| `policy/**` | Enforcement layer — changes can weaken or disable policy checks |
| `.github/workflows/pr-gates.yml` | Active CI gate — changes can break merge-blocking |
| `.github/workflows/reusable-pr-gates.yml` | Downstream CI gate — changes affect all adopting repos |
| `.github/pull_request_template.md` | Required PR structure — changes alter reviewer expectations |

See `governance/GOVERNANCE_SENSITIVE_FILES.md` for the authoritative list and full change discipline requirements.

Governance-sensitive files must not be touched as a side effect of a non-governance task. If a governance-sensitive file genuinely requires a change, that change must be scoped as a governance patch — not bundled with product or feature work.

---

## File Creation Rules

A new file may only be created when:
- The task explicitly calls for it
- No existing file can reasonably serve the same purpose with minimal modification
- The new file's location follows existing naming and folder conventions

New files must not be created speculatively for future use.

---

## File Deletion Rules

A file may only be deleted when:
- The task explicitly removes the feature, concept, or concern the file represents
- Deletion does not break other in-scope files (or those breaks are also in scope and addressed)
- No governance rule requires the file to remain (e.g., required kit files listed in `baseline.required_paths`)

---

## Cross-Area Touch Restriction

A single PR must not touch both:
- Product code files (source, tests, assets) AND
- Governance files (`governance/**`, `policy/**`, `.github/workflows/**`)

unless the task is explicitly a governance patch that requires both. Changes must be kept to a single concern area.

---

## Relationship to Other Doctrine

- **MINIMAL_DIFF.md** — the parent doctrine; this document operationalizes it at file level
- **REFACTOR_POLICY.md** — defines file scope rules for refactor-class changes specifically
- **DEPENDENCY_POLICY.md** — defines file scope for dependency manifest and lockfile changes
