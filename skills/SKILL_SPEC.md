# Aegis Skill Specification

**Version:** 1.1.0-b
**Status:** Draft — Skills System Foundation

---

## What a Skill Is

A **skill** is a packaged, governed implementation of one or more capabilities from the Aegis Capability Catalog. Skills are the concrete layer between abstract capability definitions and the agents that invoke them at runtime.

A skill:
- Has a stable identifier and a versioned specification document (`SKILL.md`)
- Declares which capability or capabilities it implements
- Defines its inputs, outputs, workflow, and guardrails explicitly
- Is owned by a named team or role
- Is subject to governance constraints inherited from the capabilities it implements

Skills are the **implementation layer** of the Capability Graph. They give capabilities concrete, repeatable behavior.

---

## What a Skill Is Not

A skill is **not**:

- A capability — capabilities are abstract; skills are concrete
- An agent — agents are runtime actors that invoke skills; a skill is a packaged unit of behavior an agent may use
- A product feature — product features may be composed of one or more skills, but skills are platform-level units
- A script or function — skills may reference scripts, but the skill itself is the governed specification, not the code
- A runbook — runbooks describe human-executed processes; skills describe agent-invocable, governed behaviors

---

## How Skills Relate to Capabilities

Every skill must implement at least one named capability from `capabilities/CAPABILITY_CATALOG.md` or a product-approved extension catalog.

The relationship is:

```
Capability (abstract)   →   Skill (implements)   →   Agent (invokes)
```

- A capability may be implemented by multiple skills (e.g., different skills implement `generate-artifact` for different artifact types).
- A skill may implement multiple capabilities if its workflow composes them (e.g., a skill that both `retrieve-context` and `plan-work`).
- The `implements` metadata field in `SKILL.md` must list every capability the skill fulfills.

---

## How Downstream Products Should Create and Organize Skills

### Skill Location

Each skill lives in its own subdirectory under `skills/`:

```
skills/
  <skill-name>/
    SKILL.md              # required — governed specification
    references/           # optional — supporting docs, ADRs, policies
    templates/            # optional — output templates the skill uses
    scripts/              # optional — automation scripts invoked by the skill
```

Aegis core provides the specification standard and example. Downstream products define their own skills in their own `skills/` directories following this standard.

### Skill Naming

Skill directory names must:
- Use kebab-case
- Be descriptive of the skill's primary behavior
- Not duplicate a core Aegis capability identifier (skills and capabilities are distinct layers)

Examples: `classify-incoming-request`, `generate-prd-draft`, `validate-repo-baseline`

### Skill Versioning

Each `SKILL.md` carries a `version` field. Skill versions follow semver. Incrementing the major version signals a breaking change to inputs, outputs, or behavior.

---

## Required Metadata Fields

Every `SKILL.md` must begin with a YAML-style metadata block (using Markdown table or fenced block format). The following fields are required:

| Field | Description |
|---|---|
| `name` | Human-readable skill name |
| `version` | Semver version string (e.g., `1.0.0`) |
| `description` | One-sentence summary of what the skill does |
| `implements` | One or more capability identifiers from the Capability Catalog (comma-separated or list) |
| `owner` | Team or role responsible for maintaining this skill |
| `status` | `draft`, `active`, or `deprecated` |
| `governance_sensitivity` | `standard` or `sensitive` — sensitive skills require patch log entries on change |
| `inputs` | Summary of required inputs (detailed in the Inputs section) |
| `outputs` | Summary of produced outputs (detailed in the Outputs section) |

---

## Required Body Sections

Every `SKILL.md` must contain the following sections in order:

### Purpose

One to three sentences describing why this skill exists and what problem it solves.

### When to Use

Specific conditions or triggers under which an agent should invoke this skill.

### When Not to Use

Conditions under which this skill must not be used, including scope limits and exclusions.

### Inputs

Enumerated list of inputs the skill requires, including:
- Input name
- Type or format
- Whether required or optional
- Description

### Outputs

Enumerated list of outputs the skill produces, including:
- Output name
- Type or format
- Description

### Capability Mapping

Explicit table mapping each step or output of the skill to the capability node it fulfills. Every implemented capability must appear here.

### Workflow

Step-by-step description of how the skill executes. Steps should be numbered and reference capability nodes where applicable.

### Guardrails

Explicit constraints on what the skill may and may not do. This section enforces the governance boundaries inherited from the implemented capabilities and the AI Workforce Contract.

### Validation

How the skill's output is verified before delivery. References `validate-output` or `validate-structure` capability where applicable.

### Dependencies

Other skills, capabilities, or external systems this skill depends on. List each dependency with a brief rationale.
