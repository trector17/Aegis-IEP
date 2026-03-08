#!/usr/bin/env node
/**
 * check-governance-files.mjs
 *
 * Detects PRs that touch governance-sensitive files without documenting
 * the change in the "Governance-Sensitive Files Touched" PR description section.
 *
 * Governance-sensitive paths:
 *   governance/
 *   policy/
 *   .github/workflows/pr-gates.yml
 *   .github/pull_request_template.md
 *
 * PR body is read from (in order):
 *   1. .git/PR_BODY
 *   2. GITHUB_EVENT_PATH (GitHub Actions event payload JSON)
 *   3. PR_BODY environment variable
 *
 * Exit 0 = PASS, Exit 1 = FAIL
 */

import { spawnSync } from 'child_process'
import { existsSync, readFileSync } from 'fs'

const SENSITIVE_PREFIXES = ['governance/', 'policy/']
const SENSITIVE_EXACT = [
  '.github/workflows/pr-gates.yml',
  '.github/pull_request_template.md'
]

// --- Get changed files via git diff ---

function getChangedFiles() {
  const strategies = []

  const baseRef = process.env.GITHUB_BASE_REF
  if (baseRef) {
    strategies.push(['git', 'diff', '--name-only', `origin/${baseRef}...HEAD`])
  }

  strategies.push(['git', 'diff', '--name-only', 'origin/main...HEAD'])
  strategies.push(['git', 'diff', '--name-only', 'HEAD~1'])

  for (const [cmd, ...args] of strategies) {
    const result = spawnSync(cmd, args, { encoding: 'utf8' })
    if (result.status === 0 && result.stdout.trim()) {
      return result.stdout.trim().split('\n').filter(Boolean)
    }
  }

  return []
}

// --- Check if a file is governance-sensitive ---

function isSensitive(file) {
  for (const prefix of SENSITIVE_PREFIXES) {
    if (file.startsWith(prefix)) return true
  }
  for (const exact of SENSITIVE_EXACT) {
    if (file === exact) return true
  }
  return false
}

// --- Get PR body ---

function getPRBody() {
  if (existsSync('.git/PR_BODY')) {
    return readFileSync('.git/PR_BODY', 'utf8')
  }

  const eventPath = process.env.GITHUB_EVENT_PATH
  if (eventPath && existsSync(eventPath)) {
    try {
      const event = JSON.parse(readFileSync(eventPath, 'utf8'))
      const prBody = event?.pull_request?.body
      if (typeof prBody === 'string') return prBody
    } catch {
      // ignore parse errors
    }
  }

  if (process.env.PR_BODY) {
    return process.env.PR_BODY
  }

  return null
}

// --- Parse "Governance-Sensitive Files Touched" section ---

function parseSensitiveSection(body) {
  const lines = body.split('\n')
  let inSection = false
  const sectionLines = []

  for (const line of lines) {
    if (/^##\s+governance.sensitive files touched/i.test(line)) {
      inSection = true
      continue
    }
    if (inSection) {
      if (/^##/.test(line)) break
      sectionLines.push(line)
    }
  }

  return sectionLines.join('\n').trim()
}

// --- Main ---

const changedFiles = getChangedFiles()
const sensitiveChanged = changedFiles.filter(isSensitive)

if (sensitiveChanged.length === 0) {
  console.log('[governance-files] PASS: No governance-sensitive files changed.')
  process.exit(0)
}

console.log('[governance-files] Governance-sensitive files changed:')
for (const f of sensitiveChanged) {
  console.log(`  - ${f}`)
}

const body = getPRBody()

if (body === null) {
  console.warn('[governance-files] WARN: Governance-sensitive files changed but no PR body metadata is available.')
  console.warn('  PR-body enforcement requires a PR context (GITHUB_EVENT_PATH, .git/PR_BODY, or PR_BODY env var).')
  console.warn('  This check will be enforced in GitHub Actions / PR verification context.')
  console.warn('[governance-files] SKIP: Exiting 0 — enforcement deferred to CI.')
  process.exit(0)
}

const sectionContent = parseSensitiveSection(body)

if (!sectionContent) {
  console.error(
    '[governance-files] FAIL: PR description is missing the' +
    ' "Governance-Sensitive Files Touched" section.'
  )
  process.exit(1)
}

if (/^[-*]?\s*none\s*$/im.test(sectionContent)) {
  console.error(
    '[governance-files] FAIL: "Governance-Sensitive Files Touched" section' +
    ' says "None" but governance-sensitive files were changed.'
  )
  process.exit(1)
}

console.log('[governance-files] PASS: Governance-sensitive files are documented in the PR description.')
process.exit(0)
