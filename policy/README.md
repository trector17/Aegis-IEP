# Aegis Policy Scripts

This directory contains the Aegis policy enforcement layer — a set of plain Node ESM scripts (zero external dependencies) that validate structural and architectural invariants in any repo that adopts Aegis.

---

## Scripts

### `scripts/check-repo-baseline.mjs`

Validates that all required Aegis kit files exist in the repository. Required paths are defined in `config.baseline.required_paths`.

Fails with a list of missing paths. Use this as the first gate to confirm the repo structure is intact.

### `scripts/check-layer-drift.mjs`

Scans source files and enforces cross-layer import rules. Rules are defined in `config.forbidden_dependencies`.

For each source file, the script:
1. Determines the file's layer from its path prefix (using `config.layers`)
2. Extracts all import/require statements via regex
3. For path-like imports (starting with `./`, `../`, or `/`), resolves the import to an absolute path
4. Determines the target layer from that resolved path
5. Flags any import that violates a forbidden dependency rule

Bare npm package specifiers are ignored. No bundler resolution is performed — detection is purely path-prefix based and deterministic.

### `scripts/check-derived-data.mjs`

Scans source files for patterns that indicate derived or computed values are being persisted. Patterns are defined in `config.derived_data_patterns` as named regex rules with messages.

Fails with file path, line number, pattern name, and message for each match.

### `scripts/run-all.mjs`

The **stable policy entrypoint**. Runs all three checks in order:
1. `check-repo-baseline`
2. `check-layer-drift`
3. `check-derived-data`

Stops on the first failure and exits non-zero. Exits zero only when all three checks pass.

Always use `run-all.mjs` as the CI entrypoint — never call individual scripts directly in CI. This ensures the check order and stop-on-failure behavior remain consistent across environments.

---

## Config Precedence

All scripts load config in this order:

1. `policy/config/policy.config.json` — local, repo-specific tuning (gitignored, never committed)
2. `policy/config/policy.config.example.json` — the committed example/default (fallback)

The local file is intentionally gitignored so each downstream repo can tune its layer definitions and forbidden dependency rules without affecting the Aegis kit itself.

---

## Setting Up a Local Config

To customize policy enforcement for your repo:

```bash
# Git Bash
cp policy/config/policy.config.example.json policy/config/policy.config.json
```

```powershell
# PowerShell
Copy-Item policy/config/policy.config.example.json policy/config/policy.config.json
```

Then edit `policy/config/policy.config.json` to:
- Set `baseline.required_paths` to the files your repo must always contain
- Set `layers` with path prefixes that match your repo structure
- Set `forbidden_dependencies` with your architecture's boundary rules
- Set `derived_data_patterns` with regex patterns specific to your domain model

`policy.config.json` is gitignored and will never be committed. It is purely local.

---

## Running Checks Locally

```bash
# Run all checks (recommended — matches CI behavior)
node policy/scripts/run-all.mjs

# Run individual checks
node policy/scripts/check-repo-baseline.mjs
node policy/scripts/check-layer-drift.mjs
node policy/scripts/check-derived-data.mjs
```

All scripts must be run from the repository root.
