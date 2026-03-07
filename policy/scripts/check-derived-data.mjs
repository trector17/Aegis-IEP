#!/usr/bin/env node
/**
 * check-derived-data.mjs
 *
 * Scans source files for patterns that indicate derived/computed data is being
 * persisted, which violates the Aegis derived-data governance rule.
 *
 * Each pattern in config.derived_data_patterns is a named regex with a message.
 * Matches are reported with file path, pattern name, message, and line number.
 *
 * Config precedence:
 *   1. policy/config/policy.config.json  (local, gitignored)
 *   2. policy/config/policy.config.example.json  (committed example)
 */

import { existsSync, readFileSync, readdirSync, statSync } from 'fs'
import { resolve, relative, extname, join } from 'path'

const ROOT = process.cwd()

function loadConfig() {
  const localPath = resolve(ROOT, 'policy/config/policy.config.json')
  const examplePath = resolve(ROOT, 'policy/config/policy.config.example.json')

  if (existsSync(localPath)) {
    console.log('[derived-data] Loading config: policy/config/policy.config.json')
    return JSON.parse(readFileSync(localPath, 'utf8'))
  }

  if (existsSync(examplePath)) {
    console.log('[derived-data] Loading config: policy/config/policy.config.example.json (fallback)')
    return JSON.parse(readFileSync(examplePath, 'utf8'))
  }

  console.error('[derived-data] ERROR: No policy config found.')
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

function main() {
  const config = loadConfig()
  const extensions = config?.scan?.extensions ?? ['.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs']
  const ignoreDirs = config?.scan?.ignore_dirs ?? ['node_modules', '.git', 'dist', 'build']
  const patterns = config?.derived_data_patterns ?? []

  if (patterns.length === 0) {
    console.log('[derived-data] No derived_data_patterns configured. Skipping check.')
    process.exit(0)
  }

  const compiledPatterns = patterns.map(p => ({
    name: p.name,
    message: p.message,
    re: new RegExp(p.pattern, 'g')
  }))

  const files = collectFiles(ROOT, extensions, ignoreDirs)
  const violations = []

  for (const filePath of files) {
    let source
    try {
      source = readFileSync(filePath, 'utf8')
    } catch {
      continue
    }

    const lines = source.split('\n')

    for (const { name, message, re } of compiledPatterns) {
      for (let i = 0; i < lines.length; i++) {
        re.lastIndex = 0
        if (re.test(lines[i])) {
          violations.push({
            file: relative(ROOT, filePath).replace(/\\/g, '/'),
            line: i + 1,
            patternName: name,
            message
          })
        }
      }
    }
  }

  if (violations.length > 0) {
    console.error('[derived-data] FAIL: Derived data persistence patterns detected:')
    for (const v of violations) {
      console.error(`\n  File:    ${v.file}:${v.line}`)
      console.error(`  Pattern: ${v.patternName}`)
      console.error(`  Message: ${v.message}`)
    }
    process.exit(1)
  }

  console.log(`[derived-data] PASS: No derived data persistence patterns found. (${files.length} files scanned)`)
}

main()
