# Patch Template

Use this template for every governance patch, structural change, or cross-cutting modification. Copy this file, fill in all sections, and add the completed entry to `governance/PATCH_LOG.md`.

A patch is required for any change that:
- Modifies governance documents
- Changes policy scripts or config schema
- Introduces a new architectural layer or layer rule
- Modifies CI workflow behavior
- Affects 5+ files or 3+ architectural layers

---

## Patch ID

`patch-X.Y.Z` — increment the patch version from the last entry in PATCH_LOG.md

## Phase

Which phase is this patch targeting? (e.g., Phase 0)

## Scope

What does this patch do? State it precisely and concisely. One paragraph maximum.

## Non-Goals

What does this patch explicitly NOT do? List anything a reader might reasonably expect to be included but is intentionally excluded.

- (item)
- (item)

## Files Changed

List every file created, modified, or deleted by this patch.

| Action | File |
|---|---|
| Created | `path/to/file` |
| Modified | `path/to/file` |
| Deleted | `path/to/file` |

## Risk Assessment

What could go wrong? What is the blast radius if something fails? How reversible is this change?

- **Risk level:** Low / Medium / High
- **Blast radius:** (describe)
- **Reversibility:** (describe how to roll back)

## Rollback Triggers

Under what conditions should this patch be reverted?

- (condition)
- (condition)

## Invariants

What must remain true after this patch is applied?

- (invariant)
- (invariant)

## Verification Steps

Exact commands Codex must run to confirm the patch is correct. All commands run from repo root.

```bash
node policy/scripts/run-all.mjs
# Expected: exit 0
```

Add additional commands specific to this patch.

## Governance Impact

Does this patch change any rules, constraints, or enforcement behavior? If yes, describe the before/after.

- **Before:** (describe)
- **After:** (describe)

## Notes

Any additional context, decisions made, alternatives considered, or follow-up items.
