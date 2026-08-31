# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK188_SUBTASK190_TASK189_PHASE_E_HUMAN_SEND_ORCHESTRATION`
Current disposition: `IN_PROGRESS`
Task ID: `CNX-20260831-188`
Execution subtask: `CNX-20260831-190`
Continues: `CNX-20260831-189`
Updated: 2026-08-31 ICT
Executor: Hermes on accepted Windows host + one genuine human Dashboard Send by user
Coordinator / final reviewer: ChatGPT
Human release authority: User

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative for coordination history.

## Active umbrella task

[`tasks/CNX-20260831-188-documentation-payload-convergence-and-proportional-requalification.md`](tasks/CNX-20260831-188-documentation-payload-convergence-and-proportional-requalification.md)

## Current execution subtask

[`tasks/CNX-20260831-190-task189-phase-e-human-send-orchestration-and-evidence-closure.md`](tasks/CNX-20260831-190-task189-phase-e-human-send-orchestration-and-evidence-closure.md)

Task 190 continues the single remaining Phase-E boundary of Task 189.

## Frozen product candidate

`604569c286e930f1a596362ab926b065b56d486e`

Coordination-only commits after this freeze do not redefine the product candidate and must not be installed/tested as a replacement candidate.

Accepted facade SHA-256:

`aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

## Accepted Task-189 state

ChatGPT reviewed Task-189 report commit `e4229bf80051c3eed31b471a9e620dbf10d95f4d` and accepts Phases A-D:

- exact frozen candidate acquisition PASS;
- exactly one supported install-over PASS;
- four changed documentation surfaces installed byte-identically PASS;
- executable facade identity preserved;
- managed Ollama/Gateway/delivery/SQLite health PASS;
- durable state preserved;
- no destructive lifecycle replay required.

Task-189 remains incomplete only because no genuine human Dashboard semantic Send was performed.

## Current objective — Hermes orchestrates Phase E

Hermes must:

1. sync/read Task 190 and current coordination state;
2. capture a minimal read-only pre-send attribution baseline on the accepted Windows host;
3. generate a fresh `CNX189-<UTC timestamp>-<short random suffix>` nonce immediately before instruction;
4. tell the user exactly which one-line prompt to send in the normal OpenClaw Dashboard;
5. require exactly one human Send, with no retry/regenerate/second Send;
6. wait for the user to say `ส่งแล้ว` in the Hermes conversation;
7. immediately collect read-only durable post-send evidence;
8. prove or disprove:
   `1 human Send -> 1 Ticket -> 1 session/run -> 1 Ollama model call -> 1 durable assistant delivery -> 1 logical Dashboard assistant result`;
9. publish the Task-190 report and stop for ChatGPT review.

Hermes must not perform or simulate the Dashboard Send itself.

## Hard fence

No reset, uninstall, fresh reinstall, state deletion, product/runtime/plugin executable edits, tests, dependencies, workflow behavior, provider/runtime semantics, durable-schema changes, release PR merge, Release workflow dispatch, tag/release publication, or force push.

If another human Send or destructive/product mutation appears necessary, stop and report instead of expanding scope.

## Publication fence

Task 188 release publication remains blocked until Task-190 Phase-E evidence is committed and accepted by ChatGPT.
