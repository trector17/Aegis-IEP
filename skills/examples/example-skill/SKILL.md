# Skill: Generate Structured Document

---

## Metadata

| Field | Value |
|---|---|
| **name** | Generate Structured Document |
| **version** | 1.0.0 |
| **description** | Produces a new, governance-conformant document from a template and provided context. |
| **implements** | `apply-template`, `generate-artifact`, `validate-structure` |
| **owner** | platform-team |
| **status** | draft |
| **governance_sensitivity** | standard |
| **inputs** | Template identifier, context object (key-value pairs), target output path |
| **outputs** | Populated document file conforming to the template's required structure |

---

## Purpose

This skill takes a named template and a set of context values, populates the template, validates the result against its required structure, and produces a ready-to-use document artifact. It is the canonical way for agents to produce structured platform documents without ad-hoc generation.

---

## When to Use

- When an agent needs to produce a new document that must conform to a known template (e.g., a patch log entry, an ADR, a PRD section).
- When the output must be validated for required fields before delivery.
- When a consistent, governed output format is required regardless of the requesting agent or context.

---

## When Not to Use

- When no template exists for the desired document type — create the template first, or use `generate-artifact` directly.
- When the output is raw code, not a structured document — this skill is for document artifacts only.
- When the document is intended to be ephemeral (e.g., an intermediate computation result that will not be committed or delivered).

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `template_id` | string | yes | Identifier of the template to use (e.g., `patch-log-entry`, `adr`) |
| `context` | key-value map | yes | Values to populate into the template's variable slots |
| `output_path` | string | yes | Relative path where the generated document should be written |
| `validate` | boolean | no | Whether to run structure validation after generation (default: true) |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `document` | file | The populated, validated document written to `output_path` |
| `validation_report` | object | Pass/fail result and any structural violations found during validation |

---

## Capability Mapping

| Skill Step | Capability Fulfilled |
|---|---|
| Locate and load the named template | `retrieve-context` |
| Populate template slots with context values | `apply-template` |
| Write the populated content to the output path | `generate-artifact` |
| Check the output against required structure | `validate-structure` |

---

## Workflow

1. **Resolve template** — Look up the template by `template_id` from the available template registry. Fail fast if the template does not exist. *(retrieve-context)*
2. **Validate context** — Confirm that all required slots defined by the template are present in the provided `context` map. Return a structured error listing missing keys if any are absent.
3. **Populate template** — Substitute context values into the template slots to produce the draft document. *(apply-template)*
4. **Write artifact** — Write the populated document to `output_path`. Create intermediate directories if needed. *(generate-artifact)*
5. **Validate structure** — If `validate` is true (default), check that the produced document contains all required sections as defined by the template's structural contract. *(validate-structure)*
6. **Return result** — Return the `document` path and `validation_report` to the invoking agent.

---

## Guardrails

- This skill must not overwrite an existing committed document without explicit confirmation from the invoking agent or user.
- This skill must not modify any file outside of the declared `output_path`.
- This skill must not invent or hallucinate template slot values. All values must come from the provided `context` input.
- If structure validation fails, the skill must surface the `validation_report` and must not silently deliver a non-conformant document.
- This skill operates on documents only. It must not generate or modify code files.

---

## Validation

After step 4 (write artifact), the skill runs structure validation (step 5) unless `validate` is explicitly set to false. Validation checks:
- All required sections defined by the template are present in the output.
- No required metadata fields are empty or contain placeholder text.

If validation fails, the skill returns the `validation_report` with the specific violations and does not mark the output as ready for delivery.

---

## Dependencies

| Dependency | Type | Rationale |
|---|---|---|
| Template registry | Internal | The skill requires a resolvable source of named templates. In Aegis core, this is `templates/`. |
| `validate-structure` capability | Capability | Used in step 5 to confirm output conformance. |
| `retrieve-context` capability | Capability | Used in step 1 to locate the template source. |
