#!/usr/bin/env node
/**
 * check-layer-drift.mjs
 *
 * Scans source files and enforces forbidden cross-layer import rules defined in config.
 *
 * Layer detection:
 *   - Source layer: determined by the file's path prefix matching a configured layer.path_prefix
 *   - Target layer: determined by the import string's prefix matching a configured layer.path_prefix
 *   - Only path-like imports are checked (starts with '.', '..', or '/')
 *   - Bare npm package specifiers are skipped
 *
 * Config precedence:
 *   1. policy/config/policy.config.json  (local, gitignored)
 *   2. policy/config/policy.config.example.json  (committed example)
 */

import { existsSync, readFileSync, readdirSync, statSync } from 'fs'
import { resolve, relative, extname, dirname, join } from 'path'

const ROOT = process.cwd()

function loadConfig() {
  const localPath = resolve(ROOT, 'policy/config/policy.config.json')
  const examplePath = resolve(ROOT, 'policy/config/policy.config.example.json')

  if (existsSync(localPath)) {
    console.log('[layer-drift] Loading config: policy/config/policy.config.json')
    return JSON.parse(readFileSync(localPath, 'utf8'))
  }

  if (existsSync(examplePath)) {
    console.log('[layer-drift] Loading config: policy/config/policy.config.example.json (fallback)')
    return JSON.parse(readFileSync(examplePath, 'utf8'))
  }

  console.error('[layer-drift] ERROR: No policy config found.')
  process.exit(1)
}

function collectFiles(dir, extensions, ignoreDirs, results = []) {
  let entries
  try {
    entries = readdirSync(dir)
  } catch {
    return results
  }

  for (const entry of entries) {
    const fullPath = join(dir, entry)
    let stat
    try {
      stat = statSync(fullPath)
    } catch {
      continue
    }

    if (stat.isDirectory()) {
      if (!ignoreDirs.includes(entry)) {
        collectFiles(fullPath, extensions, ignoreDirs, results)
      }
    } else if (stat.isFile() && extensions.includes(extname(entry))) {
      results.push(fullPath)
    }
  }

  return results
}

const IMPORT_RE = /(?:import\s+(?:.+?\s+from\s+)?['"](.+?)['"]|require\s*\(\s*['"](.+?)['"]\s*\))/g

function extractImports(source) {
  const imports = []
  let match
  IMPORT_RE.lastIndex = 0
  while ((match = IMPORT_RE.exec(source)) !== null) {
    const specifier = match[1] || match[2]
    if (specifier) imports.push(specifier)
  }
  return imports
}

function isPathLike(specifier) {
  return specifier.startsWith('./') || specifier.startsWith('../') || specifier.startsWith('/')
}

function resolveImportPath(fileDir, specifier) {
  if (specifier.startsWith('/')) return specifier
  return resolve(fileDir, specifier)
}

function detectLayer(absPath, layers) {
  const rel = relative(ROOT, absPath).replace(/\\/g, '/')
  for (const layer of layers) {
    if (rel.startsWith(layer.path_prefix)) {
      return layer.name
    }
  }
  return null
}

function main() {
  const config = loadConfig()
  const extensions = config?.scan?.extensions ?? ['.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs']
  const ignoreDirs = config?.scan?.ignore_dirs ?? ['node_modules', '.git', 'dist', 'build']
  const layers = config?.layers ?? []
  const forbidden = config?.forbidden_dependencies ?? []

  if (layers.length === 0) {
    console.log('[layer-drift] No layers configured. Skipping layer drift check.')
    process.exit(0)
  }

  if (forbidden.length === 0) {
    console.log('[layer-drift] No forbidden_dependencies configured. Skipping layer drift check.')
    process.exit(0)
  }

  const files = collectFiles(ROOT, extensions, ignoreDirs)
  const violations = []

  for (const filePath of files) {
    const sourceLayer = detectLayer(filePath, layers)
    if (!sourceLayer) continue

    let source
    try {
      source = readFileSync(filePath, 'utf8')
    } catch {
      continue
    }

    const imports = extractImports(source)
    const fileDir = dirname(filePath)

    for (const specifier of imports) {
      if (!isPathLike(specifier)) continue

      const resolvedImportPath = resolveImportPath(fileDir, specifier)
      const targetLayer = detectLayer(resolvedImportPath, layers)
      if (!targetLayer) continue

      for (const rule of forbidden) {
        if (rule.from === sourceLayer && rule.to === targetLayer) {
          violations.push({
            file: relative(ROOT, filePath).replace(/\\/g, '/'),
            import: specifier,
            rule: `${rule.from} must not import ${rule.to}`,
            reason: rule.reason
          })
        }
      }
    }
  }

  if (violations.length > 0) {
    console.error('[layer-drift] FAIL: Forbidden cross-layer imports detected:')
    for (const v of violations) {
      console.error(`\n  File:   ${v.file}`)
      console.error(`  Import: ${v.import}`)
      console.error(`  Rule:   ${v.rule}`)
      console.error(`  Reason: ${v.reason}`)
    }
    process.exit(1)
  }

  console.log(`[layer-drift] PASS: No forbidden cross-layer imports found. (${files.length} files scanned)`)
}

main()
