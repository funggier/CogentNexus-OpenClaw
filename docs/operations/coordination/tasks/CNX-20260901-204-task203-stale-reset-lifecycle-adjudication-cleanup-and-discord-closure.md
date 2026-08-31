# CNX-20260901-204 — Task 203 Stale Reset Lifecycle Adjudication, Cleanup, Managed Recovery, and Discord Closure

Status: `READY_FOR_HERMES`
Date: 2026-09-01 ICT
Parent: `CNX-20260901-203`
Repair parent: `CNX-20260831-198`
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Purpose

Adjudicate and, only if safely proven stale, remove the historical reset lifecycle tree that blocked Task 203. Then resume from the already-installed exact repaired candidate through one supported `cnxclaw enable` transition and complete the still-unused one-human-Discord-Send requalification.

This task does not rerun reset or installation and does not change product bytes.

## Immutable authorities

Frozen repaired product candidate:

`9f4eaa429b2540540e7d6f6c2af99067960e45fb`

Expected installed plugin fingerprint:

`f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`

Published `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Discord human Send budget:

`0 / 1 consumed; 1 / 1 available`

## Accepted predecessor facts

Task 203 removed only the exact stale Task-200/202 PowerShell root `11704` and then found this independent reset tree:

```text
PID 9840
PPID 10724
exe: C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\runtime\python\Scripts\python.exe
command: ... host_control_v092.py --root C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw reset --provider ollama
creation: 1788186963.6185184

PID 17360
PPID 9840
exe: C:\Users\CDQ-P\AppData\Roaming\uv\python\cpython-3.11.15-windows-x86_64-none\python.exe
command: ... host_control_v092.py --root C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw reset --provider ollama
creation: 1788186963.6370635
```

Creation time is approximately:

`2026-08-31T14:36:03.6Z / 2026-08-31 21:36:03 ICT`

This is about 1h47m before Task-198 repaired candidate commit `9f4eaa...` and about 1h55m before the later Task-200 orphan PowerShell root. It is therefore not a Task-200 install-over child.

Task-183's accepted reset is also excluded: Task 183 ran earlier, exited `0`, reached RESET PASS/fresh MANAGED and proved no lifecycle residue afterward.

Current best classification is a separate historical reset invocation. Exact human/executor origin and exact internal wait point are not yet proven.

## Hard fence before cleanup

Phase A/B are read-only. Do not:

- send input to the reset process;
- type or inject `y`, Enter, Ctrl+C, or other console input;
- rerun reset;
- rerun installer/install-over;
- invoke enable/disable/start/stop/restart;
- kill any process before the cleanup gate passes;
- mutate state/config/SQLite/Scheduled Tasks;
- change provider/model;
- send Discord;
- edit product/source/test/workflow files;
- mutate Release/tag/assets;
- use broad process-name termination;
- force push.

## Phase A — exact reset-tree identity and origin

Fresh-sync coordination authority and capture current time.

Revalidate PID `9840` and PID `17360` using **PID plus creation time plus executable plus full command line**. Do not trust PID alone.

Capture the recursive parent chain above PID 9840 until a stable user/executor boundary is reached, including PID `10724` if it still exists. For each parent record:

- PID/PPID;
- executable/name;
- command line;
- creation time;
- session ID where available;
- console/terminal relationship where read-only available.

Determine whether `9840 -> 17360` is best classified as one logical reset invocation (venv/launcher to underlying Python) or multiple independent invocations. Use creation-time proximity, parent-child relationship and identical argv. Do not infer two reset actions from process count alone.

If either PID has been reused or command identity no longer matches, stop with `BLOCKED_RESET_PROCESS_IDENTITY` and do not terminate anything.

## Phase B — stale/no-progress adjudication

Take two read-only samples separated by approximately 30-60 seconds.

For PID `9840`, PID `17360`, and any reset-tree descendant record where available:

- CPU user/system time;
- thread count/thread wait state/reason;
- handle count;
- status/responding state;
- memory;
- child process membership.

Also sample relevant product state without mutation:

- controller.json size/hash/mtime/content summary;
- ownership manifest size/hash/mtime;
- SQLite file size/mtime plus `PRAGMA integrity_check` and durable row counts;
- plugin enabled/status;
- startup state;
- Gateway health;
- Ollama readiness;
- delivery/recovery/outbox state.

Explicitly inspect for evidence of a reset confirmation wait when possible without injecting input. Source semantics are:

- reset performs preflight;
- prints warning and `Continue? [y/N]:`;
- destructive mutation begins only after literal `y`.

However, absence of readable prompt evidence does not itself block cleanup if the lifecycle tree is independently proven stale, idle, old, and conflicting with current coherent installed state.

### Cleanup gate

Cleanup is authorized only if all are true:

1. exact PID/create-time/argv identities still match Task 203;
2. the reset tree is at least the same historical invocation from `2026-08-31T14:36:03Z`;
3. CPU/thread/handle/tree and relevant state files show no meaningful progress across the bounded samples;
4. no active child command indicates legitimate lifecycle progress;
5. installed fingerprint remains exact repaired candidate;
6. ownership verify passes;
7. Gateway/Ollama/SQLite/delivery/recovery remain healthy;
8. Host state is still coherent enough to remain `passthrough`/disabled pending recovery;
9. no second lifecycle/install process is active against the same state root.

If the reset process has resumed, state is changing, identity is ambiguous, or another lifecycle process is found, stop with `BLOCKED_RESET_CLEANUP_FENCE`.

## Phase C — identity-fenced stale reset cleanup

If the cleanup gate passes, terminate only the exact historical reset tree.

Preferred order:

1. terminate exact child PID `17360` first after revalidating identity;
2. boundedly observe whether parent PID `9840` exits as a consequence;
3. if PID `9840` remains, revalidate its exact identity again and terminate PID `9840` once;
4. do not terminate parent PID `10724` unless a later task explicitly authorizes it;
5. do not use taskkill/tree-by-name/broad Python kills.

Record exact termination commands, exit/results, post-termination process scan, and prove both reset PIDs are absent.

If cleanup fails or identity changes between steps, stop with `FAIL_STALE_RESET_CLEANUP`. No enable and no Discord Send.

## Phase D — coherent pre-enable gate

After cleanup, verify read-only:

- no reset/uninstall/install/enable/disable lifecycle process remains against the state root;
- installed fingerprint = `f8267417...`;
- ownership verify PASS;
- Host `passthrough`;
- plugin/startup disabled as the safe pre-enable baseline;
- Gateway healthy/listening;
- Ollama selected/reachable/healthy/ready;
- delivery READY / pending outbox `0`;
- recovery READY / no active incident;
- SQLite integrity `ok`;
- durable counts stable except for no unauthorized semantic activity.

If not coherent, stop with `FAIL_PRE_ENABLE_HEALTH`.

## Phase E — exactly one managed recovery

Invoke exactly once:

`C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd enable`

Requirements:

- enable count `1 / 1`;
- no reset/install replay;
- v0.9.3 chooses Ollama deterministically;
- capture root-only process identity/stdout/stderr/duration/exit code using a wait method that does not wait on unrelated descendants;
- no retry on failure or ambiguity.

Managed convergence requires:

1. exit `0`;
2. Host `managed`;
3. desired Gateway/provider running;
4. startup adapter installed/enabled/ready;
5. plugin enabled/activated/loaded/no error;
6. Gateway healthy;
7. Ollama selected and ready;
8. delivery READY/outbox `0`;
9. recovery READY/no unexpected recovery attempt;
10. SQLite integrity `ok`;
11. installed fingerprint unchanged.

If any fails, stop with `FAIL_MANAGED_RECOVERY` and do not Discord Send.

## Phase F — one genuine human Discord Send

Only after managed convergence PASS.

Use owner session:

`agent:main:discord:channel:1531199905673252946`

Generate fresh nonce:

`CNX204-<UTC timestamp>-<short random suffix>`

Tell the user to send manually exactly:

`ตอบกลับข้อความนี้เพียงว่า <NONCE>`

Then wait for user response `ส่งแล้ว`.

Send budget:

- human Send: exactly `1 / 1`;
- Hermes/bot/API/injection: `0`;
- retry/regenerate/second message: `0`.

## Phase G — durable Discord proof

Prove:

`1 human Discord Send -> 1 Ticket -> 1 Direct model call -> response_ready -> 1 native visible Discord result -> delivery_confirmed -> completed`

Capture Ticket/run/model IDs, ordered events, provider/model, response/delivery timestamps, visible nonce result, outbox/recovery deltas and bounded logs.

Required negatives:

- no `before_agent_run hook failed`;
- no duplicate Ticket/model/reply;
- no Direct Recovery attempt;
- no retry/regenerate;
- no pending outbox/delivery residue;
- no provider substitution.

Dashboard observer `missing-run-correlation` / `missing-append-before-deliver` alone is not a failure. A `cnx_assistant_delivery` row is not mandatory for native Discord Direct delivery.

## Phase H — final read-only health

Verify Host managed, startup/plugin healthy, Gateway/Ollama healthy, delivery/recovery ready, SQLite integrity `ok`, exact fingerprint retained, stale reset PIDs absent and no lifecycle residue remains.

## Final dispositions

Use exactly one:

- `PASS`
- `BLOCKED_RESET_PROCESS_IDENTITY`
- `BLOCKED_RESET_CLEANUP_FENCE`
- `FAIL_STALE_RESET_CLEANUP`
- `FAIL_PRE_ENABLE_HEALTH`
- `FAIL_MANAGED_RECOVERY`
- `FAIL_DISCORD_BEFORE_AGENT`
- `FAIL_DISCORD_SEMANTIC_DELIVERY`
- `FAIL_DURABLE_CORRELATION`
- `FAIL_FINAL_HEALTH`
- `BLOCKED_EVIDENCE`

## Report

Publish:

`docs/operations/coordination/reports/CNX-20260901-204-task203-stale-reset-lifecycle-adjudication-cleanup-and-discord-closure.md`

Include exact parent/session lineage, two-sample stale evidence, cleanup identity proof, managed recovery evidence, Discord budget/correlation, mutation ledger, and final disposition. Then stop for ChatGPT review.
