# CNX-20260831-166 — Hermes/Codex Dashboard Exactly-One-Send Durable-Delivery Reacceptance

Status: `READY_HERMES`

Execution mode: `WINDOWS_DASHBOARD_SINGLE_SEND_DURABLE_DELIVERY_REACCEPTANCE_HERMES`

Current authorization: `CNX-20260831-166_HERMES_DASHBOARD_SINGLE_SEND_DURABLE_DELIVERY_REACCEPTANCE`

Task ID: `CNX-20260831-166`

Updated: 2026-08-31 ICT

Executor: Hermes/Codex

Coordinator / final reviewer: ChatGPT

## Purpose

Perform the first controlled semantic Dashboard acceptance after the Task-164 native transcript authority repair and the accepted Task-165 Windows install-over/provenance/health checkpoint.

This task authorizes **exactly one semantic Dashboard Send** against the already-proven installed candidate, then requires deep executor-side analysis of the resulting native transcript, Ticket/delivery state, model-call count, recovery behavior, and duplicate-safety evidence.

The executor must use the new standing coordination model:

- `docs/operations/coordination/EXECUTOR_ANALYSIS_REVIEW_MODEL.md`
- `docs/operations/coordination/EXECUTION_OWNERSHIP.md`
- `docs/operations/coordination/EXECUTOR_REPORT_CONTRACT.md`
- `docs/operations/coordination/CODEX_BOOTSTRAP.md`

ChatGPT will review the resulting verification packet rather than reconstruct the entire investigation by default.

## Accepted parent checkpoints

Task 164 repository repair:

- accepted production commit: `80b87dfbe0d9176e421f3748b4cee0827db12d0c`
- repair: native transcript post-persistence authority via `before_agent_finalize` -> `before_message_write` -> native append -> `onSessionTranscriptUpdate` -> CogentNexus settlement

Task 165 Windows provenance/health:

- report: `docs/operations/coordination/reports/CNX-20260830-165-hermes-windows-install-over-provenance-health.md`
- ChatGPT review: `docs/operations/coordination/reviews/CNX-20260830-165-hermes-windows-install-over-provenance-health-review.md`
- accepted installed plugin fingerprint: `5b23040f26ab1148c44647429cc5eff0ef89505e2f068b72d41d9a5fb0ee02e5`
- frozen package SHA-256: `ae4181d1a5c107c5077f40338701aa1b801e362b7f61d6accdadae696f7d23ba`
- intended OpenClaw: `2026.7.1-2`

The current remote branch may contain later coordination-only commits. Verify fresh remote state and product-tree lineage before execution.

## Objective

Use one semantic Dashboard Send to prove on the real installed candidate that:

1. one user Send produces one authoritative assistant result;
2. the result is captured once, not regenerated;
3. the assistant result is persisted through OpenClaw's native transcript path;
4. the persisted message contains the CogentNexus delivery marker associated with the durable direct-result identity;
5. CogentNexus delivery settlement occurs only after the native transcript receipt path;
6. the Ticket reaches the correct completed/delivery-confirmed state;
7. exactly one `delivery_confirmed` event exists for the tested Ticket;
8. no claimable pending delivery remains after settlement;
9. recovery does not inject a duplicate assistant message;
10. the Dashboard shows only one semantic assistant answer for the one Send;
11. the runtime remains healthy after the test;
12. no second Send or manual state mutation is used to rescue the acceptance.

## Executor responsibility

Hermes/Codex is the primary technical investigator for this task. It should independently determine the safest evidence collection sequence inside the hard fence and analyze any anomaly deeply enough to justify PASS/FAIL/BLOCKED/REWORK_REQUIRED.

Do not ask ChatGPT to rediscover routine source/DB/log relationships. Include them in the final report with exact evidence pointers and a reviewer verification packet.

## Preflight gate — read-only

Before the single semantic Send:

1. fetch/synchronize current remote branch and verify exact HEAD;
2. re-read remote `ACTIVE.md`, `STATUS.md`, this Task 166, Task-165 report/review, and the standing report contract;
3. verify Task 166 is still the only active semantic authorization and no matching Task-166 report already exists;
4. prove current product/install/runtime paths have not changed from the Task-165 accepted candidate except coordination-only changes;
5. confirm installed plugin fingerprint still equals `5b23040f26ab1148c44647429cc5eff0ef89505e2f068b72d41d9a5fb0ee02e5`;
6. confirm OpenClaw remains `2026.7.1-2` and CogentNexus plugin is enabled/loaded;
7. confirm controller/Gateway/Ollama/recovery/delivery health is coherent;
8. confirm there is no pre-existing pending terminal delivery that could be confused with the test;
9. capture read-only baseline counts/state sufficient to attribute new Ticket/model-call/delivery/events/transcript changes to exactly this Send;
10. choose a unique nonce/token for correlation before interacting with Dashboard.

If provenance or health has drifted materially, do **not** Send. Report the discrepancy instead.

## Exactly-one semantic Send authorization

Task 166 authorizes exactly one semantic Dashboard submission.

Use a unique, low-side-effect prompt that requires only a short textual assistant response and does not require tools or external actions. The prompt should contain a unique Task-166 nonce so the one user message and one assistant result can be correlated across UI, transcript, logs, Ticket state, model-call state, and delivery records.

Example shape only; generate a unique nonce at execution time:

```text
CNX-166 acceptance <nonce>. Reply with exactly: CNX-166-ACK-<nonce>
```

The executor may choose equivalent wording that avoids tool invocation and ambiguity.

### Absolute one-Send fence

After that submission:

- do not click Send again;
- do not press Enter again to submit semantic content;
- do not retry with a second prompt if the first appears delayed or failed;
- do not use another OpenClaw surface to submit equivalent semantic input;
- do not use `chat.inject` to manufacture or rescue the expected answer;
- do not manually create or edit Ticket/result/outbox/delivery/database rows;
- do not trigger a second model inference/regeneration intentionally.

If the one Send fails, hangs, duplicates, or produces ambiguous evidence, preserve the state and report the actual outcome. One failed Send is evidence; it is not permission for a retry.

## Post-Send investigation requirements

After the one Send, perform read-only observation and analysis sufficient to reconstruct the result path without mutating semantic state.

At minimum correlate:

### A. Dashboard/UI observation

- exact user nonce submitted;
- number of visible assistant semantic answers attributable to the Send;
- answer text/nonce match;
- any visible duplicate, interruption, error, retry, or unexpected intermediate assistant result.

### B. Ticket and model-call state

Identify the exact Ticket/run/session for the Send and establish:

- Ticket creation/route/response-ready/completion state as applicable;
- model-call delta attributable to the Send;
- no second inference/regeneration for the same result;
- relevant Ticket events in ordering.

### C. Durable direct-result and delivery state

Establish:

- durable direct-result identity/idempotency key;
- marker associated with that identity;
- claim/ownership behavior before settlement if observable from captured evidence;
- final delivery status;
- `delivery_confirmed_at` state;
- claim token/expiry cleared after settlement;
- no claimable pending row remains for the tested result;
- exactly one `delivery_confirmed` event exists.

### D. Native transcript authority

Inspect the authoritative OpenClaw transcript/session evidence and prove:

- the tested assistant message was natively persisted;
- exactly one marker-bearing assistant transcript row corresponds to the tested semantic result;
- the marker matches the durable delivery identity;
- transcript persistence precedes/authorizes CogentNexus final settlement under the repaired path;
- no competing recovery-injected semantic duplicate exists.

Use the strongest available native transcript/message identity and ordering evidence. Do not infer persistence solely from UI text equality.

### E. Recovery/duplicate safety

Analyze whether any Host recovery path ran or became eligible and whether it caused semantic injection.

The report must distinguish:

- no recovery activity;
- recovery observation/deduplication only;
- recovery claim with history-marker deduplication;
- actual duplicate injection.

A PASS requires no duplicate semantic assistant result.

### F. Post-test health

Confirm after observation:

- Gateway/CogentNexus runtime is healthy;
- no unexpected pending delivery remains from this test;
- database integrity remains valid;
- no unrelated semantic or lifecycle mutation was introduced by the executor.

## Source/log analysis authority

Hermes/Codex may read repository source, installed runtime source/maps where useful, logs, transcript files, SQLite state, and exact upstream OpenClaw source to explain the observed path.

Task 166 is an acceptance task, not a repair task. Do not modify production source, dependencies, OpenClaw, installer behavior, or live durable state in response to a defect. If a defect is found, analyze it deeply and report the smallest recommended repository repair scope for a successor task.

## Success criteria

Task 166 may report `PASS` only if all are evidenced:

1. preflight confirms the installed accepted Task-165 candidate and healthy runtime;
2. exactly one semantic Dashboard Send occurred;
3. exactly one authoritative semantic assistant answer is observed for that Send;
4. the unique expected nonce/answer correlates correctly;
5. exactly one model inference/result path is attributable to the Send, with no regeneration;
6. one native transcript assistant row contains the correct delivery marker;
7. final CogentNexus settlement is consistent with post-persistence transcript authority;
8. tested Ticket is completed/delivery-confirmed correctly;
9. exactly one `delivery_confirmed` event exists;
10. no claimable pending delivery remains for the tested result;
11. no recovery path produces a duplicate semantic message;
12. runtime/database health remains coherent;
13. no prohibited action or second Send occurred;
14. the final report satisfies `EXECUTOR_REPORT_CONTRACT.md`, including acceptance matrix and reviewer verification packet.

Use `FAIL` when a product/runtime defect is demonstrated.

Use `BLOCKED` when the authorized single Send cannot be performed or required proof cannot be collected safely.

Use `REWORK_REQUIRED` only for evidence/report deficiencies that can be corrected without repeating the semantic Send. **REWORK_REQUIRED never authorizes another Send.**

## Hard fence

Authorized semantic action count: exactly one Dashboard Send.

Not authorized:

- second/retry Dashboard Send;
- semantic input via another live surface;
- manual `chat.inject`;
- manual Ticket/workflow/result/outbox/delivery/database mutation;
- arbitrary transcript/state editing;
- uninstall/install-over/reinstall/reset;
- independent Gateway/Ollama/Supervisor restart unless a pre-existing health incident creates a safety need, in which case stop and report rather than mutating for acceptance convenience;
- OpenClaw source patch/upgrade;
- dependency upgrade;
- production/source repair;
- unrelated feature changes;
- release/tag/package publication;
- default/release-branch merge;
- force push.

Read-only diagnostics, logs, transcript inspection, SQLite reads, process/status checks, repository/upstream source reads, and evidence capture are authorized.

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260831-166-hermes-dashboard-single-send-durable-delivery-reacceptance.md`

Follow `EXECUTOR_REPORT_CONTRACT.md` fully.

The reviewer verification packet should prioritize, at minimum:

- exactly-one Send proof;
- installed-candidate provenance at preflight;
- one model-call/result proof;
- native marker-bearing transcript persistence proof;
- post-persistence settlement proof;
- no duplicate/recovery-injection proof;
- exactly-one `delivery_confirmed` proof;
- no claimable pending delivery and healthy post-state.

## Completion stop

After publishing the matching Task-166 report, stop. Do not send another Dashboard message and do not open or execute a successor task.

ChatGPT will perform targeted review under the new reviewer-light model and decide the next disposition.
