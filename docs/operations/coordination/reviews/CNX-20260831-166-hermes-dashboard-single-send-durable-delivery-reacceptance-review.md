# CNX-20260831-166 — ChatGPT Review of Dashboard Single-Send Durable-Delivery Reacceptance

## Review disposition

`ACCEPT — FAILURE_CONFIRMED`

Task 166 correctly reports `FAIL`. The live acceptance established that the installed Task-164 candidate can produce exactly one correct native Dashboard assistant reply without duplicate inference or recovery injection, but the CogentNexus durable-delivery authority path did not capture that reply. The failure is therefore actionable repository rework, not a reason to retry the semantic Send.

Reviewer: `ChatGPT`
Review model: `executor-heavy / reviewer-light`

## Reviewed authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Task: `CNX-20260831-166`
- Execution HEAD: `aab5ab2507ca76fa43070014afc559138bd59332`
- Report publication HEAD: `0cb101da4c2e37f189694de08cc4c01932a29c2a`
- Report: `docs/operations/coordination/reports/CNX-20260831-166-hermes-dashboard-single-send-durable-delivery-reacceptance.md`
- Accepted repair ancestor: `80b87dfbe0d9176e421f3748b4cee0827db12d0c`

## Targeted verification

The review intentionally does not reconstruct the complete live investigation. It verifies the claims that determine disposition.

### Claim 1 — Task-166 publication did not mutate product state

Verified by GitHub compare:

`aab5ab2507ca76fa43070014afc559138bd59332 .. 0cb101da4c2e37f189694de08cc4c01932a29c2a`

The only changed path is the matching Task-166 report. Therefore the evidence publication did not repair or alter the candidate after the live failure.

### Claim 2 — The accepted Task-164 repair remained the product candidate at execution

Verified by GitHub compare:

`80b87dfbe0d9176e421f3748b4cee0827db12d0c .. aab5ab2507ca76fa43070014afc559138bd59332`

The repair commit is the merge base and all subsequent changed paths through the execution HEAD are coordination documentation. No `plugins`, `scripts`, `skills`, `package.json`, or `package-lock.json` product drift exists in that interval.

### Claim 3 — The live semantic result succeeded once but durable capture failed before settlement

The executor report correlates one authorized Send to:

- one Ticket: `CNXT-1fb84cef-19d1-485e-a032-991da12aa770`;
- one Run ID: `2f9ea54b-e9e3-4e50-b012-9ad35b24b778`;
- one completed model call;
- one native assistant transcript record containing the exact expected response;
- zero assistant delivery-marker records;
- zero `cnx_assistant_delivery` rows;
- `delivery_confirmed_at=null`;
- final Ticket `status=failed` with `durableDelivery:false`.

This evidence places the acceptance break before or at the marker/staging boundary rather than after a successfully staged durable row.

### Claim 4 — Duplicate safety remained fail-closed

The report records zero retry Sends, zero recovery model calls, zero recovery rows, zero `chat.inject`/manual recovery, and exactly one visible assistant result. The Ticket subsequently failed closed instead of regenerating or injecting a second answer.

This is a safety success but not a durable-delivery success.

## Acceptance-matrix review

| Criterion | Review verdict |
|---|---|
| Exactly one semantic Send | PASS |
| Exactly one model execution | PASS |
| Exactly one visible/native assistant semantic result | PASS |
| Durable direct-result row staged | FAIL |
| Native persisted assistant carries CogentNexus marker/identity | FAIL |
| Post-persistence delivery settlement | FAIL |
| `delivery_confirmed_at` established | FAIL |
| No duplicate/recovery reinference | PASS |
| Runtime remains healthy | PASS |
| Hard fence respected | PASS |

The failed criteria are mandatory Task-166 acceptance requirements, so the executor's `FAIL` disposition is accepted.

## Root-cause boundary

This review does **not** claim the exact source-level root cause. The live evidence narrows the break to the pre-settlement correlation/staging chain, but determining which hook/event field, correlation predicate, candidate lifecycle, message-shape assumption, or integration ordering fails on the exact installed OpenClaw runtime belongs to a fresh systematic repository investigation.

Do not patch based only on the symptom `marker absent`. The next task must trace the real data flow against exact pinned OpenClaw source and reproduce the live miss with a production-faithful RED before changing production code.

## Successor decision

Open Task `CNX-20260831-167` as a repository-only Hermes/Codex root-cause + TDD repair task.

Task 167 must:

1. use Task-166 live evidence as the empirical failing boundary;
2. independently trace the exact `before_agent_finalize -> before_message_write -> staging/marker -> native append -> transcript update` data flow;
3. reproduce the real correlation/staging miss with a production-faithful RED;
4. identify and prove a single root-cause hypothesis before repair;
5. implement the smallest CogentNexus fix;
6. run targeted/full regression, build/package/plugin validation, and exact-SHA CI;
7. publish a report compliant with `EXECUTOR_REPORT_CONTRACT.md`, including an acceptance matrix and reviewer verification packet.

Task 167 must not perform another Dashboard semantic Send, install-over, reinstall, reset, or other live acceptance mutation. A repaired candidate must pass repository review first, then a separate installation checkpoint before any later semantic reacceptance.
