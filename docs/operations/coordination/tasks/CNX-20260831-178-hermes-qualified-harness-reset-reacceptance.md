# CNX-20260831-178 — Qualified-Harness Reset Fresh-State Reacceptance

Status: `READY_HERMES`

Execution mode: `WINDOWS_QUALIFIED_HARNESS_RESET_REACCEPTANCE_HERMES`

Authorization: `CNX-20260831-178_HERMES_QUALIFIED_HARNESS_RESET_REACCEPTANCE`

Executor: Hermes/Codex

Coordinator / final reviewer: ChatGPT

## Objective

Perform one new, separately authorized live `cnxclaw.cmd reset` attempt on the accepted installed candidate using the Task-177-qualified cmd/batch incremental evidence architecture, provide exactly one `y` only after the real no-newline confirmation prompt is observed and durably recorded, and prove or falsify fresh-state reconstruction without retry or helper repair.

This task is destructive but bounded. Task 174 and Task 175 remain closed historical attempts. Task 178 authorizes exactly one new reset process only.

## Accepted baseline

- product repair SHA: `231761fca24c315e90536955d3e384f55e2e232e`;
- installed fingerprint: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`;
- accepted package SHA-256: `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`;
- installed release: `0.9.3`;
- OpenClaw: `2026.7.1-2`;
- Task-171 through Task-173 durable-delivery result: `PASS — DASHBOARD_NATIVE_DURABLE_DELIVERY_REACCEPTANCE_ACCEPTED`;
- Task-177 harness result: `PASS — CMD_BATCH_INCREMENTAL_HARNESS_QUALIFIED`;
- Task-171 semantic Send count remains permanently frozen at exactly `1`.

## Mandatory execution architecture

Task 178 MUST materially reuse the Task-177-qualified architecture:

`outer harness -> cmd.exe /d /c -> installed cnxclaw.cmd reset -> installed Python facade/backend`

Requirements:

1. stdin/stdout/stderr pipes under the outer harness;
2. stdout and stderr drained concurrently from process start;
3. character- or byte-granularity detection of the literal real prompt `Continue? [y/N]: ` without waiting for newline;
4. append-only JSONL event ledger persisted incrementally;
5. flush + fsync each critical event before proceeding;
6. record `prompt_observed` before any confirmation intent;
7. record and fsync `input_send_intent` before writing confirmation;
8. write exactly one `y` line;
9. record and fsync `input_sent` immediately after successful write/flush;
10. close stdin after the one confirmation;
11. continue concurrent stream drain through natural process exit;
12. record exit/result/orphan state incrementally and finalize a result artifact.

Do not use a result design that first writes all evidence only after child completion.

## Executor observation boundary

Do not repeat the Task-175 failure mode by relying on a short one-shot outer terminal timeout as the sole source of truth.

The reset harness must preserve its ledger independently while the reset is active. Use an executor process/session mechanism that allows read-only observation of the ledger/process without relaunching reset. If an observer times out or disconnects, that does NOT authorize a second reset, a second `y`, a kill, or a helper lifecycle action.

A timeout/uncertain completion must be reported from the retained ledger/process/postflight evidence. Do not manufacture a clean result by retrying.

## Fresh preflight before destructive action

Before starting reset, perform and retain read-only evidence for:

1. fresh remote branch HEAD, ACTIVE and STATUS still authorize Task 178;
2. Task-178 report path absent;
3. accepted installed fingerprint/release unchanged;
4. OpenClaw still `2026.7.1-2`;
5. controller/plugin/Gateway/Ollama/route currently coherent enough for reset preconditions;
6. namespace ownership valid;
7. delivery pending outbox `0`;
8. no active recovery/provider incident;
9. SQLite integrity `ok`;
10. pre-reset Task-171 durable history still present and identifiable;
11. no pre-existing reset/uninstall process;
12. no conflicting newer coordination authorization.

If any material prerequisite fails, DO NOT RESET. Publish `BLOCKED` and stop.

## Exactly-one reset authorization

If and only if preflight passes, start exactly one installed command through the qualified harness:

`C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd reset`

The harness must wait until the literal prompt is observed in captured output. Only then:

- persist `prompt_observed`;
- persist `input_send_intent` with send count target `1`;
- send exactly one line: `y`;
- persist `input_sent` with send count `1`.

No pre-piped confirmation is accepted. No second confirmation is authorized.

## Absolute no-retry / no-helper fence

After the Task-178 reset process starts, under no condition may Hermes/Codex issue:

- a second reset;
- a second `y`;
- `start`, `stop`, `restart`, `enable`, or `disable`;
- manual Gateway restart/reload;
- manual Ollama/provider restart;
- supervisor/startup repair;
- route/config repair;
- manual DB bootstrap;
- installer/install-over;
- uninstall/reinstall/rollback;
- process kill merely to obtain a cleaner result;
- recovery/regeneration;
- semantic Dashboard Send/model action;
- manual durable/config/transcript mutation;
- source/product/test/workflow/dependency changes.

Implementation-owned subprocesses/process boundaries inside the single reset invocation remain authorized.

If reset fails, hangs, times out, rolls back, or leaves uncertain state, preserve that state and report it. Do not repair it in this task.

## Required live evidence

### A. Action/evidence ledger

Retain hashes and contents sufficient to prove:

- one Task-178 harness invocation;
- one reset child command;
- one reset process identity/process tree as available;
- prompt observed exactly once for the confirmation event used;
- `input_send_intent` exactly once;
- `input_sent` exactly once;
- confirmation line exactly `y`;
- no second send/retry;
- stdout/stderr captured incrementally;
- process natural exit or exact unresolved boundary;
- orphan/process scan after terminal observation.

### B. Command result

For PASS, prove:

- reset exit code `0`;
- `COGENTNEXUS-OPENCLAW RESET: PASS` present;
- `State     : fresh-install MANAGED` present;
- no executor-side helper was required.

### C. Installed provenance preservation

After reset prove:

- fingerprint exactly `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`;
- installed release remains `0.9.3`;
- OpenClaw remains `2026.7.1-2`;
- installed program payload was not replaced/upgraded.

### D. Fresh MANAGED reconstruction

Prove reset itself produced coherent fresh managed state:

- controller/state present and managed;
- policy/ownership/startup state coherent;
- plugin loaded/enabled/activated;
- Gateway healthy;
- Ollama reachable/healthy/ready;
- selected route/model coherent with managed Ollama operation;
- no unresolved provider transition or unexplained loader/runtime error.

### E. Fresh durable-state reconstruction

Prove:

- SQLite integrity `ok`;
- expected fresh schema exists;
- fresh baseline counts are coherent;
- no pending outbox/recovery/delivery/model work was manufactured;
- old reset-owned Task-171 durable identity is absent, including at minimum:
  - Ticket `CNXT-b5bf2532-d35d-47db-8951-fcf9f4729abf`;
  - run `8b69bede-030f-4c20-8bb8-0aa99e12422c`;
  - model call `8b69bede-030f-4c20-8bb8-0aa99e12422c:model:1`;
  - Task-171 `cnx_assistant_delivery` row.

The native OpenClaw transcript is external OpenClaw data and is not required to be deleted.

### F. External preservation

Prove within the captured anchors that OpenClaw/Ollama data and unrelated namespaces remain intact, excluding documented reset-owned CNX fields/state.

### G. Semantic fence

Task 178 semantic action count is `0`.

Prove no Dashboard Send, Enter semantic submission, composer input, `chat.inject`, manual model call, recovery/regeneration injection, or new semantic acceptance Ticket occurred.

## PASS contract

Task 178 may report `PASS` only if all are proven:

1. valid fresh authority/preflight;
2. Task-177-qualified harness architecture materially reused;
3. exactly one Task-178 reset invocation;
4. real prompt observed before confirmation;
5. exactly one `y` intent/send event, durably recorded incrementally;
6. no retry/helper/kill/repair;
7. reset naturally exits `0` with documented PASS / fresh-MANAGED markers;
8. accepted fingerprint/release/OpenClaw pin preserved;
9. reset itself reconstructs healthy fresh MANAGED runtime;
10. fresh DB integrity/schema passes;
11. exact old Task-171 reset-owned durable identities are absent;
12. no semantic/model/recovery work manufactured;
13. external OpenClaw/Ollama/unrelated namespaces preserved within contract;
14. report publication introduces no product/source/test/workflow drift.

Any false or materially unproven required criterion invalidates PASS. Report `FAIL`, `BLOCKED`, or `UNPROVEN` and stop without retry.

## Acceptance matrix

Include at minimum:

| Criterion | Verdict | Evidence |
|---|---|---|
| Fresh authority/preflight | PASS/FAIL/BLOCKED | authority + baseline |
| Qualified harness architecture reused | PASS/FAIL | harness hash/design |
| Exactly one reset invocation | PASS/FAIL | ledger/process |
| Prompt before input | PASS/FAIL/UNPROVEN | incremental ledger |
| Exactly one `y` | PASS/FAIL/UNPROVEN | intent/send ledger |
| No retry/helper/kill | PASS/FAIL | action/process ledger |
| Exit 0 + reset PASS/fresh MANAGED | PASS/FAIL/UNPROVEN | captured output/result |
| Installed fingerprint/release preserved | PASS/FAIL | pre/post hashes |
| OpenClaw pin preserved | PASS/FAIL | pre/post version |
| Fresh MANAGED runtime healthy | PASS/FAIL/UNPROVEN | status/provider/gateway/plugin |
| Fresh DB/schema valid | PASS/FAIL/UNPROVEN | SQLite evidence |
| Old Task-171 durable state removed | PASS/FAIL/UNPROVEN | exact-ID pre/post queries |
| Zero semantic/model/recovery manufacture | PASS/FAIL | counters/ledger |
| External preservation | PASS/FAIL/UNPROVEN | anchors |
| Report-only publication fence | PASS/FAIL | compare commit |

## Reviewer Verification Packet

Include 5–10 narrow claims, with exact evidence pointers, prioritizing:

1. harness/process identity;
2. prompt-before-input event ordering;
3. exactly-one `y` intent/send;
4. no retry/helper;
5. exit/PASS/fresh-MANAGED result;
6. installed/OpenClaw provenance;
7. fresh runtime health;
8. fresh DB + exact Task-171 removal;
9. zero semantic/model/recovery manufacture;
10. publication fence.

## Required report

Publish only after the single authorized attempt and permitted read-only postflight:

`docs/operations/coordination/reports/CNX-20260831-178-hermes-qualified-harness-reset-reacceptance.md`

After report publication, stop for ChatGPT review. Uninstall is not authorized by Task 178.
