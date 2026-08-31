# CNX-20260831-175 — Hermes Interactive-STDIN Qualification and Reset Reacceptance

Status: `READY_HERMES`

Execution mode: `WINDOWS_STDIN_QUALIFICATION_THEN_RESET_REACCEPTANCE_HERMES`

Authorization: `CNX-20260831-175_HERMES_STDIN_QUALIFICATION_THEN_RESET_REACCEPTANCE`

Executor: Hermes/Codex

Coordinator / final reviewer: ChatGPT

## Objective

Resolve the Task-174 interactive confirmation blocker without guessing or modifying product source prematurely.

First qualify an interactive Python stdin channel using a harmless disposable prompt through the same executor terminal/process facility intended for the installed reset command. Only if that qualification succeeds may this task perform exactly one newly authorized `cnxclaw.cmd reset` invocation and provide exactly one `y` confirmation.

Task 175 is a new authorization. It does not reopen or retry Task 174 under the old authorization.

## Accepted baseline

The Task-174 blocked attempt did not cross the confirmation boundary and did not mutate reset-owned state.

Accepted identity remains:

- product repair SHA `231761fca24c315e90536955d3e384f55e2e232e`;
- installed plugin fingerprint `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`;
- accepted package SHA-256 `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`;
- installed release `0.9.3`;
- OpenClaw `2026.7.1-2`;
- Task-171 through Task-173 semantic/durable result `PASS — DASHBOARD_NATIVE_DURABLE_DELIVERY_REACCEPTANCE_ACCEPTED`;
- Task-171 Send count permanently frozen at exactly `1`.

Task-174 failure boundary:

- reset invocation count `1`;
- confirmation prompt reached;
- explicit `y` count `0`;
- Python `input()` raised `OSError: [Errno 9] Bad file descriptor`;
- destructive reset phase not reached;
- post-attempt original runtime/durable state remained intact.

## Phase A — fresh authority and non-destructive stdin qualification

Before any reset invocation:

1. read fresh remote branch HEAD, `ACTIVE.md`, and `STATUS.md`;
2. prove Task 175 is still active and this Task-175 report is absent;
3. reconfirm installed fingerprint/release and OpenClaw pin;
4. reconfirm controller/Gateway/Ollama/plugin/ownership/SQLite health and that the pre-reset Task-171 durable state is still present;
5. prove no active reset process exists.

Then qualify stdin with a harmless temporary command that performs no repository, OpenClaw, CogentNexus, model, provider, or durable-state mutation.

Use the **same executor terminal/process facility and stdin-feeding mechanism intended for reset**. Prefer a direct foreground terminal session rather than a detached/capture-only process.

The qualification command must use Python `input()` because Task 174 failed specifically at that boundary. A suitable pattern is equivalent to:

```text
python -c "v=input('CNX-175-STDIN> '); print('CNX-175-STDIN-ACK:'+v)"
```

Generate a unique non-secret probe token immediately before the probe, for example:

`T175-STDIN-<UTC timestamp>-<random suffix>`

After the prompt is visibly reached, send that exact token as one input line.

Qualification PASS requires all of:

- exactly one harmless probe process;
- Python `input()` prompt observed;
- exactly one probe token supplied through the intended stdin channel;
- exact ACK containing the token returned;
- process exits `0`;
- no `OSError`, invalid handle, EOF, or closed-stdin condition;
- no product/runtime/durable-state mutation.

If the qualification fails, **DO NOT RUN RESET**. Publish Task 175 as `BLOCKED — INTERACTIVE_STDIN_CHANNEL_UNQUALIFIED` with evidence and stop.

Do not work around a failed qualification by piping `y`, redirecting a file into reset, passing confirmation as a hidden flag, editing source, or using another unqualified process path.

## Phase B — fresh reset preflight

Only after Phase A passes, repeat the critical reset preflight because the destructive action must be based on current state:

- fresh remote authority remains Task 175;
- installed fingerprint still exact;
- OpenClaw still `2026.7.1-2`;
- plugin/controller/Gateway/Ollama healthy;
- namespace ownership valid;
- SQLite integrity `ok`;
- Task-171 durable state still present before reset;
- no active reset process.

If anything materially changed, do not reset; report `BLOCKED`.

## Phase C — exactly one newly authorized reset

If and only if Phases A and B pass, run exactly one normal installed invocation:

`C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd reset`

through the qualified interactive terminal/process channel.

After the documented prompt `Continue? [y/N]:` is visibly reached, provide exactly one input line:

`y`

Do not pre-pipe `y`; the acceptance target is the documented interactive confirmation boundary.

Record:

- terminal/process facility identity;
- process/PID/session identity where available;
- command start/end timestamps;
- prompt observation;
- `y` send event/count;
- exit code;
- relevant stdout/stderr;
- whether `COGENTNEXUS-OPENCLAW RESET: PASS` appears;
- whether `State     : fresh-install MANAGED` appears.

### Absolute no-retry fence

Once the Task-175 reset process starts, no second reset is authorized under any condition.

Do not issue executor-side `start`, `stop`, `restart`, `enable`, `disable`, Gateway/Ollama restart, installer, uninstall, reinstall, rollback, DB bootstrap, route repair, config repair, recovery/regeneration, or source modification to help it succeed.

Implementation-owned subprocesses/process boundaries inside the one reset command remain authorized.

If reset fails after the stdin channel was qualified, preserve the exact failure state and stop. In particular, if the same `OSError [Errno 9]` recurs despite a proven Python-input channel, report that contradiction for a dedicated product/launcher investigation; do not retry.

## Required post-reset evidence

If the reset process naturally terminates, collect read-only evidence only.

A PASS requires proof of all Task-174 reset contract properties:

1. reset invocation count exactly `1` in Task 175;
2. explicit reset confirmation `y` count exactly `1`;
3. exit code `0` with documented reset PASS/fresh-MANAGED output;
4. installed fingerprint/release unchanged;
5. OpenClaw remains `2026.7.1-2`;
6. controller/policy/ownership/startup/plugin state represents coherent fresh MANAGED operation;
7. Gateway healthy;
8. Ollama healthy and selected route/model coherent;
9. SQLite integrity/schema valid;
10. old reset-owned CogentNexus durable history is gone, including exact Task-171 Ticket `CNXT-b5bf2532-d35d-47db-8951-fcf9f4729abf`, run `8b69bede-030f-4c20-8bb8-0aa99e12422c`, model call `8b69bede-030f-4c20-8bb8-0aa99e12422c:model:1`, and Task-171 `cnx_assistant_delivery` row;
11. no semantic/model/recovery work manufactured by reset;
12. external OpenClaw/Ollama data and unrelated namespaces remain intact within the documented preservation boundary;
13. no second reset/helper lifecycle/installer/uninstall/reinstall/rollback occurred.

The existing native OpenClaw transcript is external OpenClaw data and is not required to be removed by reset.

## Semantic hard fence

Task 175 semantic action budget is `0`.

No Dashboard Send, composer submission, `chat.inject`, alternate semantic input, manual model inference, recovery/regeneration, replacement delivery probe, or new semantic Ticket is authorized.

The harmless stdin probe token is not an OpenClaw/CogentNexus semantic action and must remain isolated from those surfaces.

## Evidence and Reviewer Verification Packet

The report must follow `EXECUTOR_REPORT_CONTRACT.md` and include 5–10 narrow reviewer claims. At minimum include:

1. fresh authority and baseline;
2. harmless Python-input qualification command/token/result;
3. proof the qualification used the same intended terminal/stdin mechanism as reset;
4. whether reset was authorized after qualification;
5. if run, exactly one Task-175 reset process and exactly one `y`;
6. reset exit/PASS/fresh-MANAGED result;
7. installed/OpenClaw provenance preservation;
8. fresh DB and removal of exact Task-171 reset-owned identities;
9. zero semantic/helper/retry actions;
10. report-only publication fence.

## Required report

Publish only after the permitted work is complete:

`docs/operations/coordination/reports/CNX-20260831-175-hermes-stdin-qualification-reset-reacceptance.md`

After report publication, stop for ChatGPT review. Uninstall remains unauthorized until reset acceptance is reviewed and accepted.
