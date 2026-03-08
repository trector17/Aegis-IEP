#!/usr/bin/env node
/**
 * run-all.mjs
 *
 * Stable policy entrypoint. Runs all Aegis policy checks in order:
 *   1. check-repo-baseline      — required kit files exist
 *   2. check-layer-drift        — no forbidden cross-layer imports
 *   3. check-derived-data       — no persisted derived/computed values
 *   4. check-governance-files   — governance-sensitive changes are documented in PR
 *
 * Stops on first failure. Exits non-zero if any check fails.
 * Exits zero only when all checks pass.
 *
 * Use this as the CI entrypoint:
 *   node policy/scripts/run-all.mjs
 */

import { spawnSync } from 'child_process'
import { resolve } from 'path'

const SCRIPTS_DIR = resolve(process.cwd(), 'policy/scripts')

const CHECKS = [
  { name: 'baseline',           script: 'check-repo-baseline.mjs'    },
  { name: 'layer-drift',        script: 'check-layer-drift.mjs'      },
  { name: 'derived-data',       script: 'check-derived-data.mjs'     },
  { name: 'governance-files',   script: 'check-governance-files.mjs' }
]

function run(check) {
  const scriptPath = resolve(SCRIPTS_DIR, check.script)
  console.log(`\n==> Running check: ${check.name}`)
  console.log(`    ${scriptPath}\n`)

  const result = spawnSync(process.execPath, [scriptPath], {
    stdio: 'inherit',
    cwd: process.cwd()
  })

  return result.status ?? 1
}

let allPassed = true

for (const check of CHECKS) {
  const exitCode = run(check)
  if (exitCode !== 0) {
    console.error(`\n[run-all] FAIL: Check "${check.name}" failed with exit code ${exitCode}. Stopping.`)
    allPassed = false
    process.exit(exitCode)
  }
}

if (allPassed) {
  console.log('\n[run-all] PASS: All policy checks passed.')
  process.exit(0)
}
