# CNX-20260830-150 — Runtime Lifecycle Stop/Start/Restart/Disable/Enable Acceptance

## Verdict

`PASS`

The five authorized runtime transitions completed exactly once, in order, on the real Windows installation:

`stop → start → restart → disable → enable`

## Remote authority

- Repository: `https://github.com/funggier/CogentNexus-OpenClaw.git`
- Branch: `agent/v0.9.3-full-stabilization`
- Remote HEAD before execution: `234374c255a181b4ad7114e2c1a72d0a00417ef5`
- State: `READY_FOR_HERMES`
- Task: `CNX-20260830-150`
- Execution mode: `LIVE_WINDOWS_RUNTIME_LIFECYCLE_TRANSITION_ACCEPTANCE`
- Accepted production SHA: `fb5781c1abd68280760bd5b3b4a65fabd8a60e58`
- Matching report was absent before publication.

`ACTIVE.md`, `STATUS.md`, and the complete Task-150 authority were read from the fresh GitHub checkout. GitHub was the coordination authority; no stale local checkout was used for task decisions.

## Evidence

External evidence root:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx150-live-20260829T204031Z/evidence
```

Read-only preflight proved the accepted starting boundary:

- controller `MANAGED`, generation `6`, desired Gateway/provider `running`/`running`;
- selected provider `ollama`;
- one canonical CNX plugin, version `0.9.3`, enabled/loaded;
- ownership verification passed;
- Gateway healthy on `127.0.0.1:18789`;
- OpenClaw `2026.7.1-2`;
- Ollama healthy/ready with four models;
- recovery and delivery `READY`, pending outbox `0`;
- SQLite `integrity_check=ok`;
- semantic counts all zero;
- Dashboard semantic Sends `0`.

The accepted installed provenance was preserved throughout:

- plugin fingerprint: `12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0`;
- installed ownership helper SHA-256: `10dda985e6d4553a73a8cdd3ef7f660937482c3ef0c2d2da8d15bcbfe8d39b66`;
- launcher SHA-256: `f53df28f2a7ee7fc43c65ba2c48770ed9b7ed3e7b14d3c762f957bd017b90f10`.

## Phase A — preflight and verifier correction

All preflight probes were read-only. The first sequence verifier incorrectly treated the expected STOP-phase `READY_WITH_WARNINGS` exit codes from `check system` and `check recovery` as failures, and incorrectly required the static OpenClaw inventory status to change while the STOP contract only requires installed plugin/program/ownership files to remain. It also recorded that the initial verifier stopped before later commands were run.

No lifecycle command was repeated. A corrected read-only verification of the already-consumed STOP output proved the actual STOP contract passed: command exit `0`, mode `maintenance`, desired Gateway/provider `stopped`, active intentional-maintenance marker, and Gateway unhealthy/stopped.

The verifier correction did not alter live state.

## Phase B — STOP

Exact command:

```text
cmd.exe /d /c C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd stop
```

- invocation count: `1`;
- command exit code: `0`;
- controller mode: `maintenance`;
- desired Gateway/provider: `stopped`/`stopped`;
- maintenance marker: active, reason `planned shutdown`, recovery policy `manual`;
- Gateway verified unhealthy/stopped;
- Ollama verified not reachable/stopped;
- delivery remained empty/pending `0`;
- SQLite remained intact;
- Dashboard semantic Sends remained `0`.

STOP passed. The nonzero exit codes of read-only `check system` and `check recovery` reflected the expected `READY_WITH_WARNINGS` intentional-maintenance state and were not product lifecycle failures.

## Phase C — START

Exact command:

```text
cmd.exe /d /c C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd start
```

- invocation count: `1`;
- exit code: `0`;
- controller: `managed`;
- desired Gateway/provider: `running`/`running`;
- Gateway healthy;
- Ollama healthy/ready;
- plugin singular, enabled/loaded;
- recovery/delivery healthy, pending `0`;
- semantic counts unchanged at zero;
- Dashboard semantic Sends `0`.

## Phase D — RESTART

Before restart, the healthy Gateway PID was `21316`. Exact command:

```text
cmd.exe /d /c C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd restart
```

- invocation count: `1`;
- exit code: `0`;
- Gateway PID changed `21316 → 17464`;
- Gateway became healthy again on loopback;
- controller remained `managed` with desired runtime running;
- Ollama remained healthy/ready;
- plugin remained enabled/loaded;
- recovery/delivery remained `READY`, pending `0`;
- semantic counts and Dashboard Sends remained unchanged.

This proves a real Gateway process boundary, not merely a status re-read.

## Phase E — DISABLE

Exact command:

```text
cmd.exe /d /c C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd disable
```

- invocation count: `1`;
- exit code: `0`;
- controller: `passthrough`;
- desired Gateway: `running`;
- CNX plugin inventory: singular, `enabled=false`, `status=disabled`;
- native OpenClaw Gateway healthy;
- Ollama remained healthy/ready and was not uninstalled or destructively altered;
- CNX state/database remained present and structurally valid;
- recovery/delivery and semantic side-effect counts remained clean;
- Dashboard semantic Sends `0`.

The product output recorded the expected managed-policy/runtime boundary transition and native route restoration.

## Phase F — ENABLE

Exact command:

```text
cmd.exe /d /c C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd enable
```

- invocation count: `1`;
- exit code: `0`;
- controller: `managed`;
- desired Gateway/provider: `running`/`running`;
- selected provider: Ollama;
- plugin inventory: singular, `enabled=true`, `status=loaded`;
- Gateway healthy on `127.0.0.1:18789`;
- Ollama healthy/ready;
- startup/supervisor integration coherent;
- recovery/delivery `READY`, pending outbox `0`;
- no stale transition/maintenance residue;
- semantic counts unchanged at zero;
- Dashboard semantic Sends `0`.

## Final read-only proof

Final ownership verification returned exit `0` with the expected product identity and paths. Final plugin fingerprint remained:

```text
12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0
```

Final installed ownership-helper hash remained:

```text
10dda985e6d4553a73a8cdd3ef7f660937482c3ef0c2d2da8d15bcbfe8d39b66
```

Final SQLite was opened with a read-only URI:

- integrity: `ok`;
- `tickets=0`;
- `ticket_events=0`;
- `cnx_direct_model_call=0`;
- `cnx_direct_recovery=0`;
- `cnx_assistant_delivery=0`;
- `ticket_outbox=0`;
- `cnx_sessions=0`;
- pending outbox: `0`;
- transaction/rollover residue: `0`.

## Side-effect accounting

- stop invocations: `1`;
- start invocations: `1`;
- restart invocations: `1`;
- disable invocations: `1`;
- enable invocations: `1`;
- lifecycle retries: `0`;
- reset/uninstall/install/reinstall: `0`;
- Dashboard semantic Sends: `0`;
- manual OpenClaw/Ollama/process/task lifecycle: `0`;
- manual plugin/config/controller/ownership normalization: `0`;
- manual semantic/database mutation: `0`;
- crash/recovery injection: `0`;
- unrelated service/process/task mutation: `0`;
- reboot: `0`;
- credentials/secrets disclosed: `0`;
- merge/tag/release/force-push: `0`.

## Unproven items

None of the Task-150 PASS criteria remain unproven. Dashboard semantic delivery was intentionally not exercised because it is outside this task's authority.

## Completion

All five runtime lifecycle transitions passed in order. This report is the only requested publication. Stop for independent ChatGPT review.
