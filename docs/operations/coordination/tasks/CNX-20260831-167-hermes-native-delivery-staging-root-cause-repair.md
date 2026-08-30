# CNX-20260831-167 — Hermes/Codex Native Delivery Staging Root-Cause + TDD Repair

Status: `READY_HERMES`

Execution mode: `REPOSITORY_NATIVE_DELIVERY_STAGING_ROOT_CAUSE_REPAIR_HERMES`

Current authorization: `CNX-20260831-167_HERMES_NATIVE_DELIVERY_STAGING_ROOT_CAUSE_REPAIR`

Task ID: `CNX-20260831-167`

Updated: 2026-08-31 ICT

Executor: Hermes/Codex

Coordinator / final reviewer: ChatGPT

Review model: `executor-heavy / reviewer-light`

## Purpose

Investigate and repair the exact repository-level defect exposed by the failed Task-166 live Dashboard acceptance.

Task 166 proved that one semantic Send produced exactly one correct native assistant result and exactly one model execution, but CogentNexus failed to stage/bind its durable direct-result identity before native persistence. The native assistant transcript record contained the correct semantic answer but no CogentNexus delivery marker, no assistant idempotency identity was attached, no `cnx_assistant_delivery` row existed, and the Ticket later failed closed with `durableDelivery:false`.

This task is **repository-only**. It must determine the actual root cause, reproduce it faithfully in automated evidence, implement the smallest CogentNexus repair, and return exact-SHA GREEN evidence. It does not authorize another live semantic test or installation mutation.

## Required standing policy

Read and obey:

- `docs/operations/coordination/EXECUTOR_ANALYSIS_REVIEW_MODEL.md`
- `docs/operations/coordination/EXECUTION_OWNERSHIP.md`
- `docs/operations/coordination/EXECUTOR_REPORT_CONTRACT.md`
- `docs/operations/coordination/CODEX_BOOTSTRAP.md`
- `docs/operations/coordination/PROBLEM_LOOP.md`

Hermes/Codex is the primary technical investigator and implementer. ChatGPT will review the final verification packet rather than reconstructing the whole investigation by default.

## Accepted parent evidence

### Task 164

Accepted repository repair commit:

`80b87dfbe0d9176e421f3748b4cee0827db12d0c`

Intended authority chain:

`terminal assistant candidate -> before_message_write(marker + durable native-write claim) -> native SessionManager append -> onSessionTranscriptUpdate(post-persistence receipt) -> CogentNexus settlement`

Pinned OpenClaw target:

- version: `2026.7.1-2`
- commit: `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c`

### Task 165

Accepted installed candidate fingerprint:

`5b23040f26ab1148c44647429cc5eff0ef89505e2f068b72d41d9a5fb0ee02e5`

### Task 166 live failure

Report:

`docs/operations/coordination/reports/CNX-20260831-166-hermes-dashboard-single-send-durable-delivery-reacceptance.md`

ChatGPT review:

`docs/operations/coordination/reviews/CNX-20260831-166-hermes-dashboard-single-send-durable-delivery-reacceptance-review.md`

Exact live correlation:

- Ticket: `CNXT-1fb84cef-19d1-485e-a032-991da12aa770`
- Run: `2f9ea54b-e9e3-4e50-b012-9ad35b24b778`
- one completed model call;
- one correct visible/native assistant semantic result;
- assistant native transcript marker count: `0`;
- `cnx_assistant_delivery` rows for the execution: `0`;
- `delivery_confirmed_at=null`;
- final Ticket: permanent `failed`, `durableDelivery:false`;
- no retry Send, recovery injection, second inference, or duplicate assistant result.

Treat these as empirical facts to explain, not as proof of a specific source-level cause.

## Objective

Determine exactly why the Task-164 production path did not stage and mark the Task-166 native assistant message on the exact OpenClaw target, then repair that root cause with the smallest safe CogentNexus change.

The repair must restore all of the following without weakening duplicate safety:

1. exact post-model assistant candidate is correlated to the correct CogentNexus run/Ticket;
2. the matching native assistant write reaches the durable staging/marker boundary;
3. a durable direct-result row and bounded native-write claim exist before native append returns;
4. native assistant persistence carries a stable CogentNexus marker/identity;
5. final delivery settlement still occurs only after post-persistence transcript receipt;
6. recovery cannot race the native owner into duplicate output;
7. no second inference/regeneration is introduced;
8. Task-155/Task-162/Task-164 duplicate/recovery guarantees remain intact.

## Mandatory systematic root-cause phase

Do **not** start by editing production code.

First trace the real data path against repository code, exact pinned OpenClaw source, Task-166 evidence, and production-faithful tests.

At minimum investigate and record:

1. actual registration and runtime event shape of `before_agent_finalize` on OpenClaw `0790d9f...`;
2. actual `runId`, `sessionId`, `sessionKey`, `lastAssistantMessage`, and message projection available on that hook;
3. actual registration/context/event shape of `before_message_write` on the native SessionManager append path;
4. whether the Task-164 code keys candidate state by a field whose value/availability differs between the two hooks;
5. whether the `dashboardTicket(path, runId)` predicate can reject the live candidate at finalize time;
6. exact representation of `lastAssistantMessage` versus the assistant message later passed to `before_message_write`;
7. whether strict text equality can fail because of trimming, content projection, thinking/tool parts, metadata, formatting, or message transformation;
8. whether multiple assistant/tool/transcript updates in the same session can overwrite/delete candidate state before the marker-bearing receipt;
9. whether hook priority/lifecycle/registration timing can prevent either hook from seeing the intended live message;
10. whether public hook context uses `sessionKey` consistently on the exact installed version;
11. whether Task-164 automated regression modeled any field or ordering differently from the real Task-166 live path;
12. any other evidence-supported boundary discovered during tracing.

Use a single explicit root-cause hypothesis and test it minimally. If a hypothesis fails, record the contradiction and form a new one. Do not stack speculative fixes.

## Production-faithful RED requirement

Before production repair, create or modify regression coverage so that the real Task-166 failure mechanism is represented faithfully and fails on the current production implementation.

The RED must demonstrate the relevant missing staging/marker behavior, not merely assert implementation details.

Prefer a test that feeds the exact public hook/event/context shapes and ordering proven from pinned OpenClaw source and reproduces the live correlation miss.

Preserve existing historical RED/GREEN coverage. Do not weaken Task-162/Task-164 tests merely because they passed an incomplete model of production.

Record:

- exact RED test path;
- exact RED command;
- observed failing assertion/behavior;
- why this failure corresponds to Task-166 evidence;
- RED commit SHA before production repair, if repository history policy permits a separate test-only commit.

## Minimal repair phase

Only after the root cause and production-faithful RED are established:

- implement the smallest CogentNexus source change that addresses the proven cause;
- keep OpenClaw read-only;
- avoid unrelated refactors;
- do not widen semantic authority beyond the exact correlation needed;
- do not settle delivery at a pre-persistence hook;
- do not replace native persistence authority with transport callbacks;
- do not authorize recovery injection while a native owner can still produce/has produced the same semantic result.

Expected primary production surface remains around:

`plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`

but the executor must follow evidence rather than assume that file alone is sufficient.

## Required GREEN validation

At the exact final repair SHA, run and report at minimum:

1. the new Task-167 production-faithful regression;
2. existing `v162-dashboard-transcript-authority.test.ts`;
3. existing v091 Dashboard verified-delivery regressions;
4. Task-155 duplicate/no-regeneration coverage relevant to this boundary;
5. full CogentNexus-OpenClaw plugin test suite;
6. `npm run build`;
7. `npm run plugin:validate`;
8. baseline consistency validation required by current repository workflow;
9. required package/installer validation appropriate to the changed source;
10. GitHub `Validate` full matrix on the exact repair SHA;
11. Windows Installer Pack Smoke on the exact repair SHA;
12. PS5.1 Acceptance Smoke on the exact repair SHA.

Any production/source change after a validation run invalidates that run for final acceptance and requires fresh exact-SHA validation.

## Repository-write authorization

Hermes/Codex may:

- inspect current GitHub state/history;
- inspect Task-166 report and repository evidence;
- inspect exact pinned upstream OpenClaw source read-only;
- create production-faithful regression tests;
- modify CogentNexus source/tests narrowly to repair the proven root cause;
- run local repository tests/build/package validation;
- commit/push normal fast-forward history to `agent/v0.9.3-full-stabilization`;
- inspect required GitHub Actions;
- publish the matching Task-167 report.

## Hard fence

Task 167 must **not**:

- perform any Dashboard semantic Send;
- use another live semantic OpenClaw surface;
- use `chat.inject` for acceptance;
- install-over, uninstall, reinstall, reset, or mutate the accepted Windows installation;
- restart/mutate live Gateway, Ollama, Supervisor, or OpenClaw runtime;
- manually mutate live Ticket/workflow/result/outbox/delivery/database/transcript state;
- patch/fork/vendor/upgrade OpenClaw;
- upgrade dependencies;
- publish release/tag/package;
- merge to default/release branch;
- force push;
- perform unrelated product repair.

If repository investigation cannot establish a safe root cause or exact pinned source disproves the assumed authority chain, report `BLOCKED`/`REWORK_REQUIRED` with evidence instead of inventing a weaker contract.

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260831-167-hermes-native-delivery-staging-root-cause-repair.md`

The report must comply with `EXECUTOR_REPORT_CONTRACT.md` and include at minimum:

1. disposition;
2. objective/acceptance contract;
3. exact starting authority/HEAD;
4. Task-166 evidence consumed;
5. complete evidence-backed root-cause summary;
6. materially relevant alternatives/hypotheses rejected;
7. production-faithful RED and why it models the live failure;
8. minimal repair rationale;
9. files/commits changed;
10. risk/crash-window/duplicate-safety analysis;
11. targeted/full/local validation;
12. exact-SHA workflow IDs/results;
13. acceptance matrix for every Task-167 criterion;
14. contradictions/anomalies/residual uncertainty;
15. hard-fence compliance;
16. **Reviewer Verification Packet** containing 3–10 critical claims, each with exact evidence pointer and the narrowest independent ChatGPT check;
17. recommended successor gate.

## Successor gate

Even a Task-167 `PASS` does not authorize installation or another Dashboard Send.

ChatGPT must review the Task-167 verification packet first.

If accepted, the next task must be a separate repaired-candidate Windows install-over/provenance/health checkpoint. Only after that checkpoint is accepted may a later exactly-one-Send reacceptance be considered.
