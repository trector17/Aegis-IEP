# Architecture: [System Name]

**Version:** 0.1
**Status:** Draft | Active
**Phase:** [Phase number and name]
**Date:** YYYY-MM-DD

---

## System Purpose

One paragraph. What does this system do? What problem does it solve? Who uses it?

---

## Repo Structure

```
src/
  domain/          # Business entities, rules, and invariants — no external dependencies
  application/     # Orchestration, use-case services — calls domain + infrastructure
  infrastructure/  # Persistence, external services — implements domain interfaces
  app/
    api/           # HTTP route handlers — thin, delegates to application services
  components/      # UI components — presentation only
```

Adjust this structure to match the actual repo. Include only layers that exist.

---

## Layer Definitions

| Layer | Path Prefix | Responsibility |
|---|---|---|
| domain | `src/domain/` | Business entities, rules, validation, derived computations. No external dependencies. |
| application | `src/application/` | Use-case orchestration. Calls domain and infrastructure. No UI dependency. |
| infrastructure | `src/infrastructure/` | Persistence and external service clients. Implements domain-defined interfaces. |
| api | `src/app/api/` | HTTP mapping only. Delegates to application services immediately. |
| ui | `src/components/` | Presentation only. Reads from API. No direct infrastructure access. |

---

## Forbidden Dependencies

These import directions are forbidden and enforced mechanically by `check-layer-drift.mjs`.

| From | To | Reason |
|---|---|---|
| domain | infrastructure | Domain must be pure. No persistence knowledge. |
| domain | api | Domain must be framework-agnostic. |
| domain | ui | Domain must have no presentation dependency. |
| application | ui | Application services orchestrate logic, not presentation. |

---

## Persistence Approach

Describe the persistence layer: database type, ORM or raw queries, connection management.

- **Database:** (e.g., PostgreSQL via Supabase)
- **Access pattern:** (e.g., repository pattern — one repository class per aggregate)
- **Soft deletes:** (e.g., all records use `deleted_at` timestamp — no hard deletes)
- **Migrations:** (e.g., versioned SQL files in `supabase/migrations/`)

---

## Derived-Data Policy

Any value that can be computed from source data must never be persisted. This is enforced mechanically by `check-derived-data.mjs`.

**Examples of derived values in this system:**

| Derived Value | Source Data | Computed At |
|---|---|---|
| (example: completion percentage) | (task completion states) | (read time in application layer) |

Never store these values. Never add columns for them. Compute them on demand.

---

## Ordering Logic Locality Rule

Logic that determines the order of records (move up, move down, reorder) lives in application or domain code. It must not be moved to database stored procedures or RPC functions unless a phase explicitly scopes that migration.

---

## Invariants

What must always be true in this system, regardless of input?

- (invariant)
- (invariant)

---

## Operational Notes

- **Environment variables:** All secrets and config live in environment variables. No values are hardcoded. See `.env.example` for required variables.
- **Secrets:** Never committed to git. `.env` and `.env.*` are gitignored.
- **Least privilege:** Service clients are initialized with the minimum required permissions.
