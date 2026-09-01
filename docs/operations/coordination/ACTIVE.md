# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK210_TASK205_SUPPORTED_CANCELLATION_AND_TASK207_WINDOWS_DISCORD_REQUALIFICATION`
Current disposition: `TASK209_EXECUTABLE_RECOVERY_ACCEPTED__SUPPORTED_CANCELLATION_THEN_LIVE_REQUALIFICATION`
Task ID: `CNX-20260901-210`
Parent task: `CNX-20260901-209`
Repair parent: `CNX-20260831-198`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-01 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Published authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No Release/tag/asset mutation is authorized.

## Current repaired product candidate

Task-207 repository-GREEN candidate:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Validated package proof:

```text
artifact ID: 9790881384
artifact digest: sha256:1733897690890f9adcb12176b79db2b43e27799a4022743c4597fad44d2d5a34
payload-v2: d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b
zip SHA-256: 0321028fc6214e18dbc965ad79a6d04328a05a84dce6a9efc058fb1122237986
```

## Task 209 accepted result

Report:

`reports/CNX-20260901-209-task205-recovery-executability-adjudication.md`

Review:

`reviews/CNX-20260901-209-task205-recovery-executability-adjudication-review.md`

Accepted review disposition:

`ACCEPT_BLOCKED_EXECUTABLE_RECOVERY__SUPPORTED_CANCELLATION_REQUIRED`

Task 209 proved the historical Task-205 direct-redelivery recovery is currently executable under exact production scheduler authority:

```text
Ticket: CNXT-f23e2c11-e630-4319-84c2-c57ed7e7edf6
run: b79dbb65-15eb-4b3e-8ffb-4084125e6cb5
owner session: agent:main:discord:channel:1531199905673252946
Ticket status: accepted
session: active / generation 0
recovery: redeliver / pending / owner_generation 0
all dueDirectRecovery predicates: true
production-equivalent exact-Ticket query: selected
```

Same-session inventory also proved there is no unrelated emittable work: exactly one nonterminal Ticket and one recovery, both belonging to Task 205; no pending assistant delivery, outbox, or active/recovering model call.

## Active Task 210

Hermes must execute:

`tasks/CNX-20260901-210-task205-supported-cancellation-and-task207-windows-discord-requalification.md`

Execution order:

1. fresh read-only scope gate proving the same-session inventory is still exactly the Task-205 pair;
2. resolve the currently installed compiled plugin `dist/v090.js` and verify exported `cancelSessionTickets`;
3. invoke that supported function exactly once with historical run `b79dbb65-15eb-4b3e-8ffb-4084125e6cb5` — no raw SQLite edits;
4. prove session generation advanced exactly once, Task-205 Ticket/recovery are cancelled, scheduler query no longer selects them, and no emittable residue remains;
5. verify exact Task-207 artifact/provenance;
6. perform one supported standalone-child install-over of `27fe0181...` with no retry;
7. prove exact installed provenance + managed/startup/plugin/Gateway/Ollama/delivery/recovery/SQLite health;
8. prove numeric Discord channel ID `1531199905673252946`;
9. allocate one fresh `CNX210-*` human Send;
10. prove Task-207 visible-final behavior, allowing at most one same-run bounded revision if first final is bare `NO_REPLY`;
11. require one visible native Discord reply and durable `delivery_confirmed -> completed`.

If a visible reply appears but durable settlement fails, stop as correlation defect; do not self-repair in Task 210.

## Discord budget

Task-210 human Send budget:

`0 / 1 consumed; 1 / 1 available`

No probe/API/bot/injected/second Send.

## Hard fence

No raw/manual SQLite mutation, no second cancellation invocation, no reset/uninstall/fresh reinstall, no installer retry, no provider/model substitution, no source/test/workflow edit, no Release/tag mutation, no force push, and no delivery-correlation repair during Task 210.
