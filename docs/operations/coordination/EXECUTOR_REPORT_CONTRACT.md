# Executor Analysis and Verification Report Contract

Updated: 2026-08-31 ICT

## Purpose

Define the minimum analysis and evidence interface that Hermes/Codex must provide for delegated CogentNexus-OpenClaw tasks so ChatGPT can perform a targeted, evidence-based review without reconstructing the full investigation.

This contract is mandatory for future delegated tasks unless an active task explicitly requires a stricter report.

## Report quality objective

The report must be detailed enough that a reviewer can answer:

1. What was the exact authorized objective?
2. What state and revision did the executor actually start from?
3. What did the executor investigate and what technical conclusion did it reach?
4. Why is the conclusion supported by evidence rather than assumption?
5. What changed or what live action occurred?
6. What proves the result satisfies each acceptance criterion?
7. What risks, contradictions, or uncertainty remain?
8. Which small set of claims should ChatGPT independently verify before disposition?

A report is not a chronological activity log. It is an auditable technical argument tied to durable evidence.

## Required structure

### 1. Disposition

One of:

- `PASS`
- `FAIL`
- `BLOCKED`
- `REWORK_REQUIRED`

Include a short summary explaining the disposition and the most important limitation, if any.

### 2. Objective and acceptance contract

State:

- Task ID and task path;
- objective in one concise paragraph;
- success criteria actually evaluated;
- any task-specific invariants or hard fences that materially affect the result.

Do not silently replace the task's acceptance criteria with easier ones.

### 3. Authority and starting state

Record as applicable:

- repository;
- branch;
- exact starting remote HEAD;
- active coordination state/task;
- accepted parent/candidate SHA(s);
- upstream version/commit pins;
- local checkout/worktree provenance;
- report-absence/replay fence before side effects;
- whether remote changed during execution and how the race was handled.

### 4. Investigation summary

Explain the technical investigation at a level sufficient for review:

- components/files/systems inspected;
- important observations;
- root cause or causal model when diagnosing a defect;
- exact external/upstream facts relied upon;
- contradictions discovered;
- material assumptions that were tested or remained assumptions.

Do not include hidden chain-of-thought. Provide conclusions and evidence-backed rationale.

### 5. Alternatives considered

List only materially relevant alternatives, especially ones that could change safety or architecture. For each, state briefly why it was rejected or deferred.

This section may be omitted for pure execution/provenance tasks where there was no meaningful implementation choice.

### 6. Chosen implementation or action

For source/repository work, record:

- implementation commit(s);
- exact files changed;
- behavior changed;
- why the change is minimal for the accepted causal model;
- any migration/schema/package impact.

For local/live work, record:

- exact commands/actions;
- side effects intentionally caused;
- start/end observations;
- immutable artifact/provenance identifiers where applicable.

### 7. Risk and uncertainty analysis

Evaluate the risks relevant to the task, such as:

- duplicate or replay behavior;
- crash/restart windows;
- data integrity;
- concurrency/races;
- recovery/liveness;
- version compatibility;
- installer/lifecycle safety;
- semantic side effects;
- regression surface.

State residual uncertainty explicitly. Conservative or fail-closed behavior should be identified as such.

### 8. TDD and validation evidence

When production/source changes occur, report the real test cycle:

- inherited or newly created RED and why it failed;
- minimal fix;
- GREEN result;
- targeted regressions;
- full relevant suites;
- build/package/plugin/schema checks;
- exact-SHA CI workflow run IDs and job conclusions.

Do not report a GREEN-only test as proof of a newly created regression unless the RED behavior was independently demonstrated.

For non-source tasks, provide the equivalent preflight/action/postflight validation matrix.

### 9. Acceptance matrix

Include a compact table:

| Criterion | Verdict | Evidence |
|---|---|---|
| exact task criterion | PASS / FAIL / UNPROVEN | commit/run/hash/path/observation |

Every required success criterion must appear exactly once.

A `PASS` disposition is invalid if a required criterion is `FAIL` or `UNPROVEN`.

### 10. Evidence index

Provide exact identifiers rather than large pasted logs:

- commits and parent lineage;
- workflow run IDs;
- artifact/package hashes;
- installed fingerprints;
- relevant file/function pointers;
- local evidence paths plus SHA-256 hashes when raw machine evidence cannot be committed;
- timestamps when ordering matters.

If raw evidence is intentionally not published, explain why and preserve enough immutable identity for later audit.

### 11. Contradictions and anomalies

Record evidence that did not fit the expected path even if the final disposition remains PASS, for example:

- missing exit-code fields;
- transient warnings;
- unexpected but bounded runtime transitions;
- test harness mistakes corrected during execution;
- stale state discovered and discarded.

Explain why each anomaly does or does not affect the disposition.

### 12. Hard-fence compliance

Explicitly state:

- authorized mutations/side effects performed;
- prohibited actions performed: `none` or exact violation;
- semantic sends/interactions count when relevant;
- destructive lifecycle actions count when relevant;
- manual DB/state mutation count when relevant.

### 13. Residual unproven items

List everything still unproven that could matter to a successor task. `None within this task's acceptance contract` is acceptable only when justified.

### 14. Reviewer verification packet

This is mandatory and is the primary context-reduction interface.

Select approximately 3-10 critical claims that determine the disposition. For each claim provide:

| # | Critical claim | Why it matters | Exact evidence | Suggested reviewer check |
|---|---|---|---|---|
| 1 | concise claim | safety/acceptance impact | SHA/run/hash/path | exact narrow check |

The packet should prioritize claims whose failure would invalidate PASS or create material safety risk.

Examples:

- production repair is present at exact installed fingerprint;
- native delivery settlement occurs only after post-persistence receipt;
- exact-SHA Validate workflow passed;
- no semantic Dashboard Send occurred;
- database counts/integrity remained stable;
- recovery cannot create a duplicate semantic result.

Do not fill the packet with low-value facts merely to reach a count.

### 15. Recommended successor

State the executor's recommended next action and why, but do not open or execute a successor task unless separately authorized.

### 16. Publication state

Record:

- execution/final HEAD before report publication;
- report path;
- report publication commit when known;
- changed-file fence for the report commit if required by the task.

## Reviewer expectations

A compliant report allows ChatGPT to begin at targeted verification rather than full reconstruction. ChatGPT may still expand review when:

- a critical claim lacks durable evidence;
- report and repository state disagree;
- the executor's causal conclusion conflicts with source behavior;
- a high-risk safety invariant is only asserted, not demonstrated;
- live-machine evidence contradicts repository/CI evidence;
- unexplained anomalies could alter the disposition.

## Compactness rule

Detail is required; duplication is not.

Prefer tables and evidence pointers over repeated prose. Avoid pasting complete logs, source files, or workflow payloads when a hash/run ID and a concise excerpt/location are enough. Historical background should be referenced by Task/Report/Review ID rather than rewritten unless necessary to understand the current causal model.

## Compatibility with historical reports

Historical reports remain valid under the contract that existed when they were produced. ChatGPT may review them using the new reviewer-light method when they already contain sufficient evidence, but executors are not required to rewrite completed historical reports solely to match this format.
