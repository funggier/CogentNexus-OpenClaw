# CNX-20260901-208 — Task 207 Windows Discord Visible-Final Requalification

Date: 2026-09-01 ICT  
Task: `CNX-20260901-208`  
Parent: `CNX-20260901-207`  
Branch: `agent/v0.9.3-full-stabilization`

## Disposition

`BLOCKED_PREEXISTING_TASK205_RECOVERY`

The mandatory pre-install safety gate found a still-pending historical Task-205 direct-redelivery recovery row. Per task authority, it may still emit delayed output. The task therefore stops before install-over and before any new Discord Send.

## Mutation ledger

```text
install-over: 0
installer retry: 0
reset/uninstall/fresh reinstall: 0
lifecycle mutation: 0
process termination: 0
provider/model/config/schema mutation: 0
manual SQLite mutation: 0
Discord probe/API/bot/injected Send: 0
human Discord Send: 0
source/test/workflow mutation: 0
Release/tag/asset mutation: 0
force push: 0
```

## Fresh evidence

Evidence root:

`C:/Users/CDQ-P/AppData/Local/Temp/cnx208-task207-windows-discord-20260901T`

Fresh baseline timestamp:

`2026-09-01T08:11:16Z`

Captured artifacts include:

- `a00-meta.txt` — evidence creation and probe exit ledger;
- `a01-status.json` — read-only host/runtime status;
- `a02-delivery.json` — read-only delivery check;
- `a03-recovery.json` — read-only recovery check;
- `a04-plugins.json` — empty output from an unsuitable probe;
- `a05-schema.json` — SQLite table schemas;
- `a05-sqlite-old-recovery.json` — integrity, counts, and exact historical correlation;
- `a06-process-residue.json` — initial process scan, including collector self-matches.

## Historical Task-205 adjudication

Exact identifiers:

```text
Ticket: CNXT-f23e2c11-e630-4319-84c2-c57ed7e7edf6
run: b79dbb65-15eb-4b3e-8ffb-4084125e6cb5
nonce: CNX205-20260831T190442Z-8cdbed
owner session: agent:main:discord:channel:1531199905673252946
```

Read-only SQLite result:

```text
integrity: ok
matching tickets: 1
matching ticket events: 6
matching model calls: 1
matching deliveries: 0
matching outbox rows: 0
matching recovery rows: 1
```

The exact recovery row is:

```text
ticket_id: CNXT-f23e2c11-e630-4319-84c2-c57ed7e7edf6
mode: redeliver
state: pending
attempt_count: 0
active_run_id: null
next_attempt_at: 2026-08-31T19:08:52.400Z
last_error: Direct response delivery was not confirmed before deadline
owner_generation: 0
created_at: 2026-08-31T19:08:52.400Z
updated_at: 2026-08-31T19:08:52.400Z
```

This is not proven absent, terminal, or superseded. Under the Task-208 safety contract it remains capable of delayed output, so the correct disposition is the pre-existing recovery blocker.

## Read-only host observations

The launcher status probe returned exit `0` and reported:

```text
Host mode: managed
desired gateway/provider: running/running
generation: 32
selected provider: ollama
Gateway: healthy, loopback 127.0.0.1:18789
OpenClaw: 2026.7.1-2
startup adapter: Ready / Enabled
pending outbox: 0
```

Delivery check:

```text
verdict: READY
pending: 0
readOnly: true
stateChanged: false
```

Recovery check:

```text
verdict: READY
readOnly: true
stateChanged: false
```

The global recovery check does not supersede the exact Ticket-level pending redelivery row. The task-level historical recovery gate is therefore BLOCKED despite healthy aggregate runtime checks.

## Harness issues

### SQLite observer schema assumption

The first observer attempt incorrectly assumed a `run_id` column in every queried table and failed with:

```text
sqlite3.OperationalError: no such column: run_id
```

No database write occurred. The observer was corrected by inspecting `PRAGMA table_info` first, then rerunning read-only with schema-bound predicates. The corrected artifact is `a05-sqlite-old-recovery.json`.

Classification: `HARNESS ERROR`; no product impact.

### Plugin inventory probe

The attempted `plugins --json` probe produced an empty output and no semantic JSON artifact. It was not used as evidence of plugin state or drift.

Classification: `HARNESS ERROR`; no product impact. No corrective live action was taken because the Task-208 recovery fence already stopped the task.

### Process scan self-match

The initial process scan matched three Bash observer shells because their command lines contained the evidence-root and collector terms. These are collector self-matches, not proof of a lifecycle process. No process was terminated.

Classification: `HARNESS SELF-MATCH`; no product impact. The scan cannot override the exact SQLite recovery blocker.

## Phases not performed

Because the mandatory pre-install safety gate failed, these phases were intentionally not performed:

- exact artifact hash verification for an install invocation;
- supported install-over of Task-207 candidate `27fe0181...`;
- installer terminal-process observation;
- installed provenance verification;
- post-install managed-health gate;
- exact Discord room proof for the new task;
- fresh `CNX208-*` nonce generation;
- human Discord Send;
- visible-final revision verification;
- native Discord delivery and durable settlement verification.

These are `NOT PERFORMED`, not passed or failed.

## Hard-fence confirmation

No reset, uninstall, reinstall, install retry, provider/model/config/schema mutation, manual SQLite update, process kill, source/test/workflow edit, Release/tag mutation, force push, Discord probe, or Discord Send occurred.

The published `v0.9.3` tag remains immutable. Task-207 candidate `27fe0181b3b65d555a3b0cc8354f6f7945c21c0b` was not installed by this task.

## Required next action

A coordinator-authorized successor must first resolve the historical Task-205 recovery state through a documented, identity-fenced, non-semantic process. Do not manually edit SQLite or bypass the recovery fence. Only after a fresh task proves the old recovery is incapable of delayed output may a new Task-208-style one-send requalification proceed.
