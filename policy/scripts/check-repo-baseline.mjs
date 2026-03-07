#!/usr/bin/env node
/**
 * check-repo-baseline.mjs
 *
 * Validates that all required Aegis kit paths exist in the repository.
 *
 * Config precedence:
 *   1. policy/config/policy.config.json  (local, gitignored)
 *   2. policy/config/policy.config.example.json  (committed example)
 */

import { existsSync, readFileSync } from 'fs'
import { resolve } from 'path'

const ROOT = process.cwd()

function loadConfig() {
  const localPath = resolve(ROOT, 'policy/config/policy.config.json')
  const examplePath = resolve(ROOT, 'policy/config/policy.config.example.json')

  if (existsSync(localPath)) {
    console.log('[baseline] Loading config: policy/config/policy.config.json')
    return JSON.parse(readFileSync(localPath, 'utf8'))
  }

  if (existsSync(examplePath)) {
    console.log('[baseline] Loading config: policy/config/policy.config.example.json (fallback)')
    return JSON.parse(readFileSync(examplePath, 'utf8'))
  }

  console.error('[baseline] ERROR: No policy config found. Expected policy/config/policy.config.json or policy/config/policy.config.example.json')
  process.exit(1)
}

function main() {
  const config = loadConfig()
  const requiredPaths = config?.baseline?.required_paths

  if (!Array.isArray(requiredPaths) || requiredPaths.length === 0) {
    console.error('[baseline] ERROR: config.baseline.required_paths is missing or empty.')
    process.exit(1)
  }

  const missing = []

  for (const relPath of requiredPaths) {
    const absPath = resolve(ROOT, relPath)
    if (!existsSync(absPath)) {
      missing.push(relPath)
    }
  }

  if (missing.length > 0) {
    console.error('[baseline] FAIL: The following required paths are missing:')
    for (const p of missing) {
      console.error(`  - ${p}`)
    }
    process.exit(1)
  }

  console.log(`[baseline] PASS: All ${requiredPaths.length} required paths exist.`)
}

main()
