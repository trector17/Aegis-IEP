# Aegis Capability Model

**Version:** 1.1.0-a
**Status:** Draft — Capability Graph Foundation

---

## What a Capability Is

A **capability** is a named, discrete unit of work that the Aegis platform can perform or delegate. Capabilities are abstract — they describe *what* is done, not *how* it is done or *who* does it.

A capability has:
- A stable, kebab-case identifier (e.g., `classify-request`)
- A category that groups related capabilities
- A description of its intent
- Example uses that clarify its boundaries

Capabilities form the **platform language of work**. Every skill, agent, and product integration in the Aegis ecosystem is described in terms of the capabilities it uses, exposes, or extends.

---

## What a Capability Is Not

A capability is **not**:

- A skill — skills are concrete implementations that fulfill one or more capabilities
- An agent — agents are runtime actors that invoke skills and capabilities
- A product feature — product features are downstream concerns; they may map to capabilities but are not defined here
- A policy rule — governance rules constrain capabilities but are separate artifacts
- A function or API endpoint — capabilities are abstract; they have no runtime signature

---

## The Abstraction Layer

The Capability Graph is the **abstraction layer** between Aegis core and downstream products.

```
Governance
    │
    ▼
Capability Graph  ◄─── This layer (defined here)
    │
    ├── Skills (future: skills/)
    │
    ├── Agents (future: agents/)
    │
    └── Products (downstream repos)
```

Aegis core defines capabilities. Downstream products consume, extend, and compose them. This separation ensures that governance remains product-agnostic and that platform evolution does not require per-product rewrites.

---

## Node Concepts

The Capability Graph is composed of five node types. Each node type has a defined role and permitted relationships.

### Governance Nodes

Governance nodes represent binding platform rules. They constrain what capabilities may do, how agents may be composed, and what products may override.

- Source: `governance/` documents
- Authority: highest — governance nodes override all other nodes
- Examples: `ENGINEERING_CONTRACT.md`, `AI_WORKFORCE_CONTRACT.md`

### Capability Nodes

Capability nodes are the core vocabulary of the platform. Each capability node is a named unit of work as defined in `capabilities/CAPABILITY_CATALOG.md`.

- Source: `capabilities/CAPABILITY_CATALOG.md` (core), downstream catalogs (extensions)
- Authority: platform-level — stable across products
- Examples: `classify-request`, `plan-work`, `validate-structure`

### Skill Nodes

Skill nodes are concrete implementations that fulfill one or more capability nodes. A skill may implement a single capability or compose several.

- Source: `skills/` (future directory, not yet created)
- Authority: implementation-level — product-specific behavior lives here
- Examples: (none yet defined)

### Agent Nodes

Agent nodes are runtime actors. An agent is configured to invoke a set of skills, observe governance constraints, and operate within a defined scope.

- Source: `agents/` (future directory, not yet created)
- Authority: operational — agents are governed by capability and governance nodes
- Examples: (none yet defined)

### Product Nodes

Product nodes represent downstream repos that adopt Aegis. They may extend the capability catalog, define their own skills, and configure their own agents — but they may not redefine core Aegis capability meanings.

- Source: downstream repos
- Authority: product-level — scoped to the product; cannot override Aegis core
- Examples: any "Powered by Aegis" repo

---

## Core vs. Product Extension Model

**Core capabilities** are defined in this repository under `capabilities/`. They are stable, versioned, and governed. Products must not change their meaning.

**Product extensions** are capability entries defined in a downstream repo's own `capabilities/` directory (or equivalent). They may:
- Add new capability identifiers not defined in Aegis core
- Map product-specific work to Aegis core capabilities
- Restrict or specialize a core capability's scope within their product

Product extensions **must not**:
- Redefine the description or intent of a core Aegis capability
- Remove or shadow a core Aegis capability identifier
- Claim Aegis core authority for a product-specific capability

---

## Summary

| Concept | Role | Defined In |
|---|---|---|
| Governance node | Constrains all other nodes | `governance/` |
| Capability node | Names and defines units of work | `capabilities/CAPABILITY_CATALOG.md` |
| Skill node | Implements capabilities | `skills/` (future) |
| Agent node | Invokes skills at runtime | `agents/` (future) |
| Product node | Extends and consumes the graph | Downstream repos |
