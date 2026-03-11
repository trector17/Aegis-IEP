# Aegis Capability Graph Rules

**Version:** 1.1.0-a
**Status:** Draft — Capability Graph Foundation

These rules govern how nodes in the Capability Graph may relate to one another, how routing decisions are made, and how downstream products may extend the graph without violating Aegis core semantics.

---

## Allowed Relationships

The table below defines which node types may reference or depend on which others.

| From | May reference | May NOT reference |
|---|---|---|
| Governance node | *(all nodes — governance is the authority root)* | — |
| Capability node | Other capability nodes (for composition notes) | Skill nodes, Agent nodes, Product nodes |
| Skill node | Capability nodes | Governance nodes directly (governed via capability contracts) |
| Agent node | Skill nodes, Capability nodes | Governance nodes directly (governed via AI Workforce Contract) |
| Product node | Capability nodes, Skill nodes, Agent nodes | Core Aegis governance nodes (read-only reference, not override) |

**Key invariants:**

1. Governance nodes are the authority root. No other node type overrides them.
2. Capability nodes are abstract. They do not reference runtime implementations.
3. Skills implement capabilities — the reference direction is skill → capability, never the reverse.
4. Agents operate through skills — agents do not bypass capability definitions to act directly.
5. Products consume and extend the graph — they do not redefine the core.

---

## Routing Principles

When a request enters the Aegis platform (via a user prompt, system trigger, or external event), routing proceeds through the following ordered steps:

1. **Classify** — Apply `classify-request` to determine the request type and target capability scope.
2. **Retrieve context** — Apply `retrieve-context` to gather relevant governance, history, and artifact state.
3. **Resolve capability** — Map the classified request to one or more capability nodes from the Capability Catalog.
4. **Select skill** — Identify the skill(s) that fulfill the resolved capabilities (once the `skills/` layer exists).
5. **Invoke agent** — Route to the agent authorized to invoke those skills under the AI Workforce Contract.
6. **Validate and document** — Apply `validate-output` and `document-decision` before delivery or merge.

Routing must always pass through a defined capability node. Ad-hoc agent actions that bypass capability classification are a governance violation.

---

## Extension Rules for Downstream Repos

Downstream repos that adopt Aegis may extend the Capability Graph to describe product-specific work. The following rules apply:

### Permitted Extensions

- **Add new capability identifiers** not present in `capabilities/CAPABILITY_CATALOG.md`.
- **Map product work to core capabilities** by referencing Aegis core identifiers in product documentation.
- **Define product-scoped skill and agent nodes** that implement or extend core capabilities.
- **Restrict a core capability's scope** within the product (e.g., `call-external-system` scoped to a specific approved API set).

### Prohibited Extensions

- **Redefine a core capability's description or intent.** If `plan-work` means X in Aegis core, a product may not declare that `plan-work` means Y in their context.
- **Shadow a core capability identifier** with a product-local definition that conflicts with the core.
- **Claim Aegis core authority** for a product-specific capability (e.g., do not mark a product capability as "platform-level" unless it is contributed back to Aegis core).
- **Remove or deprecate a core capability** within a product extension. Deprecation of core capabilities is an Aegis governance event.

### Extension Namespace Convention

Product-specific capabilities should use a namespaced identifier to prevent collision:

```
<product-slug>/<capability-name>
```

Example: `atlas/generate-client-report`, `vault/encrypt-artifact`

Core Aegis capabilities are always unnamespaced (e.g., `plan-work`, `validate-structure`).

---

## Governance Bindings

Governance nodes constrain the Capability Graph at the following points:

### Capability Definition Governance

- Core capabilities defined in `capabilities/CAPABILITY_CATALOG.md` are governed artifacts.
- Changes to core capability definitions require a patch log entry in `governance/PATCH_LOG.md`.
- `capabilities/CAPABILITY_CATALOG.md` is listed in `governance/GOVERNANCE_SENSITIVE_FILES.md` and subject to the governance-sensitive change discipline.

### Skill Governance (future)

When the `skills/` layer is introduced:

- Each skill must declare which capability nodes it implements.
- A skill may not claim to implement a capability it does not actually fulfill.
- Skills that touch governed data or cross layer boundaries must be reviewed under the Engineering Contract.

### Agent Governance (current)

Agent behavior is currently governed by `governance/AI_WORKFORCE_CONTRACT.md`. As the Capability Graph matures:

- Agents will be required to declare their authorized capability scope.
- An agent may only invoke skills that implement capabilities within its declared scope.
- Capability scope violations are treated as AI Workforce Contract violations.

### Product Governance

Products that extend the Capability Graph must:

- Record the Aegis version from which they derived their capability baseline (per `templates/PROJECT_BOOTSTRAP.md`).
- Not override or shadow core Aegis capabilities without contributing a formal extension proposal to Aegis core.
- Apply the same extension rules to any second-level extensions they define.

---

## Summary of Inviolable Rules

1. Governance nodes have unconditional authority over all other nodes.
2. Capability nodes are abstract — they have no runtime signature or implementation binding.
3. Routing always passes through a capability node; no agent or skill bypasses classification.
4. Products extend; they do not redefine core Aegis capabilities.
5. Extensions use namespaced identifiers to prevent collision with core vocabulary.
6. Changes to core capabilities are governance events and require documentation.
