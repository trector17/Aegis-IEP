# Aegis Capability Catalog

**Version:** 1.1.0-a
**Status:** Draft — Capability Graph Foundation

This catalog defines the core Aegis capability vocabulary. All entries are stable platform-level capabilities. Downstream products may extend this catalog but must not redefine these entries.

---

## Categories

| Category | Description |
|---|---|
| **platform** | Capabilities that manage platform operations, governance, and cross-cutting concerns |
| **engineering** | Capabilities that operate on code, repositories, and technical artifacts |
| **execution** | Capabilities that process input, transform data, and produce output |

---

## Platform Capabilities

### `classify-request`

| Field | Value |
|---|---|
| **Category** | platform |
| **Description** | Determine the type, intent, and scope of an incoming request before routing or processing it. |
| **Example uses** | Categorizing a user prompt as a code change vs. a documentation update; routing a work item to the correct agent lane; identifying whether a request requires governance review. |

---

### `retrieve-context`

| Field | Value |
|---|---|
| **Category** | platform |
| **Description** | Fetch and assemble relevant context from available sources to inform downstream work. |
| **Example uses** | Loading prior decisions from a patch log; pulling ADRs related to a requested change; gathering repository metadata before proposing a patch. |

---

### `plan-work`

| Field | Value |
|---|---|
| **Category** | platform |
| **Description** | Decompose a request or goal into an ordered set of steps, tasks, or sub-capabilities. |
| **Example uses** | Generating a step-by-step implementation plan for a feature request; producing a task list for a governance upgrade; outlining a patch sequence before execution. |

---

### `document-decision`

| Field | Value |
|---|---|
| **Category** | platform |
| **Description** | Record a decision, change, or governance event in a durable, traceable artifact. |
| **Example uses** | Writing a patch log entry after a structural change; creating an ADR for an architectural decision; recording a governance exception with justification. |

---

### `verify-boundaries`

| Field | Value |
|---|---|
| **Category** | platform |
| **Description** | Confirm that a proposed or completed action stays within defined governance, layer, or capability boundaries. |
| **Example uses** | Checking that a proposed code change does not cross forbidden layer dependencies; validating that an agent request does not exceed its authorized scope; confirming that a product extension does not redefine a core capability. |

---

### `enforce-governance`

| Field | Value |
|---|---|
| **Category** | platform |
| **Description** | Apply binding governance rules to block, flag, or require remediation of non-compliant work. |
| **Example uses** | Blocking a PR that modifies a governance-sensitive file without documentation; requiring a patch log entry before merging a structural change; flagging an agent action that violates the AI Workforce Contract. |

---

### `prepare-bootstrap`

| Field | Value |
|---|---|
| **Category** | platform |
| **Description** | Assemble and configure the minimal set of artifacts needed to initialize a new product or environment under Aegis governance. |
| **Example uses** | Generating an initial policy config from the example template; populating a new repo with required governance files; running the bootstrap checklist for a new Aegis-powered product. |

---

## Engineering Capabilities

### `inspect-repo`

| Field | Value |
|---|---|
| **Category** | engineering |
| **Description** | Read and analyze repository structure, contents, and metadata to understand current state. |
| **Example uses** | Scanning a repo for required baseline files; reading an existing architecture doc before proposing changes; identifying layer structure from directory layout. |

---

### `assess-drift`

| Field | Value |
|---|---|
| **Category** | engineering |
| **Description** | Detect deviations between the current repo state and the expected or declared governance baseline. |
| **Example uses** | Identifying files that have drifted from their declared layer; detecting missing required paths; comparing current policy config against the adopted Aegis version's requirements. |

---

### `propose-patch`

| Field | Value |
|---|---|
| **Category** | engineering |
| **Description** | Formulate a concrete, minimal change to code, configuration, or documentation that addresses a specific need. |
| **Example uses** | Drafting a targeted code fix following Minimal Diff Doctrine; generating a governance document update; producing a policy config diff for a structural change. |

---

### `apply-template`

| Field | Value |
|---|---|
| **Category** | engineering |
| **Description** | Populate a structured template with context-specific content to produce a conformant artifact. |
| **Example uses** | Filling in a PRD template for a new feature; generating a patch log entry from the patch template; producing an ADR from the ADR template. |

---

### `generate-artifact`

| Field | Value |
|---|---|
| **Category** | engineering |
| **Description** | Produce a new document, file, or structured output that did not previously exist. |
| **Example uses** | Creating a new capability definition file; generating a runbook for a new adoption path; producing a bootstrap checklist for a product. |

---

### `validate-structure`

| Field | Value |
|---|---|
| **Category** | engineering |
| **Description** | Check that a document, file, or configuration conforms to its expected structure, schema, or format. |
| **Example uses** | Verifying that a patch log entry contains all required fields; confirming that a policy config matches the required shape; checking that a capability catalog entry includes category, description, and example uses. |

---

## Execution Capabilities

### `ingest-input`

| Field | Value |
|---|---|
| **Category** | execution |
| **Description** | Accept and normalize raw input from a user, system, or external source for downstream processing. |
| **Example uses** | Reading a user prompt and normalizing it before classification; accepting a webhook payload and preparing it for routing; ingesting a file upload before parsing. |

---

### `parse-document`

| Field | Value |
|---|---|
| **Category** | execution |
| **Description** | Extract structured information from an unstructured or semi-structured document. |
| **Example uses** | Reading a Markdown governance document to extract key rules; parsing a JSON config file; extracting version information from a VERSION.md file. |

---

### `transform-data`

| Field | Value |
|---|---|
| **Category** | execution |
| **Description** | Convert data from one form, schema, or representation to another. |
| **Example uses** | Converting a raw patch description into a structured patch log entry; mapping user input to a capability identifier; normalizing version strings across formats. |

---

### `validate-output`

| Field | Value |
|---|---|
| **Category** | execution |
| **Description** | Confirm that a produced output meets correctness, completeness, and conformance requirements before delivery. |
| **Example uses** | Checking that a generated document is non-empty and well-formed; verifying that a proposed patch does not introduce forbidden imports; confirming that a bootstrap artifact contains all required sections. |

---

### `package-output`

| Field | Value |
|---|---|
| **Category** | execution |
| **Description** | Assemble and format a final output for delivery to a user, system, or downstream process. |
| **Example uses** | Bundling a set of generated files into a reviewable PR diff; formatting a plan output for display; assembling a structured response for an API caller. |

---

### `call-external-system`

| Field | Value |
|---|---|
| **Category** | execution |
| **Description** | Invoke an external API, service, or tool on behalf of a skill or agent, subject to governance authorization. |
| **Example uses** | Calling the GitHub API to create a PR; invoking an external documentation system; triggering a CI run via API after a patch is applied. |
