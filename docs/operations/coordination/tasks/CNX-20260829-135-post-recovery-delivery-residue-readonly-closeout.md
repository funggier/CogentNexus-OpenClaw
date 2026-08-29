# CNX-20260829-135 — Post-Recovery Delivery Residue Read-Only Closeout

- Status: `READY_FOR_HERMES`
- Execution mode: `LIVE_WINDOWS_READONLY_DELIVERY_BASELINE_ONLY`
- Owner / independent reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-29 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Close the single publication gap left after the independently accepted Task-134 full real-Windows recovery PASS: publish a deterministic **read-only Ticket/workflow/outbox/delivery residue baseline** before any Dashboard semantic Send is authorized.

Task 134 recovery is accepted and its one-shot ledger is consumed. **Do not rerun Task 134 or any recovery/lifecycle scenario.**

This task authorizes no semantic message, Ticket creation, workflow execution, delivery retry, outbox mutation, lifecycle operation, provider/config mutation, or database write.

## Accepted prerequisite

Task-134 report:

`docs/operations/coordination/reports/CNX-20260829-134-v093-real-windows-recovery-final-reacceptance-sequenced.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-134-v093-real-windows-recovery-final-reacceptance-sequenced-review.md`

Accepted recovery result:

- exact candidate `1424d6fbee2c458c8c30440616783d2fa1bc1201`;
- exact harness blob `a4138e00e2056db89b0a9eceed1b54e001c4e319`;
- one-shot suite `1 / 1 PASS`, consumed;
- baseline PASS;
- Gateway crash PASS;
- provider crash PASS;
- provider→operator carried incident boundary PASS;
- intentional stop/no-auto-recovery/start PASS;
- post-start strict `READY` PASS;
- final runtime/provider/listener/model/SQLite state coherent;
- no Dashboard semantic Send.

Task-134 Phase 3 required `outbox/status residue classification`, but that item was not published. Task 135 closes only that gap.

## Authoritative live paths

Use the installed launcher only:

`C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd`

Freshly read/hash/parse the launcher and require the same explicit state root:

`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw`

Authoritative SQLite expected from that root:

`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\runtime\cogentnexus-openclaw.sqlite3`

If launcher/root/database authority is different, ambiguous, or missing, stop `BLOCKED`. Do not normalize or initialize anything.

## Phase 0 — fresh authority and no-mutation fence

1. Fresh-fetch branch HEAD, `ACTIVE.md`, and `STATUS.md`; confirm Task 135 remains authoritative and unsuperseded.
2. Create a fresh evidence directory under `%LOCALAPPDATA%\Temp`.
3. Record timestamp, Windows identity, PowerShell version, literal current working directory, installed launcher path/hash/text, parsed CLI/root.
4. Confirm no Task-135 report already exists.
5. Do not run any command that can create, dispatch, retry, cancel, acknowledge, delete, or mutate Ticket/workflow/outbox state.

## Phase 1 — authoritative read-only runtime/delivery status

Through the exact installed launcher, using direct argument-safe calls only, collect:

- `cnxclaw.cmd status`;
- `cnxclaw.cmd check delivery --json` (or exact supported equivalent if global `--json` placement differs; record literal command and exit code);
- `cnxclaw.cmd check recovery --json` read-only sanity confirmation.

Require runtime remains:

- mode `managed`;
- desired Gateway/provider `running`;
- selected provider `ollama`;
- recovery exact `READY`;
- Gateway/Ollama healthy.

From the status/delivery surfaces, publish every available Ticket/delivery count, including `pendingOutbox` if present.

The source contract for `ticket_snapshot(root)` reports:

- ticket counts grouped by status;
- `pendingOutbox` = count of `ticket_outbox` rows where `delivery_status='pending'`.

Do not run any command whose implementation may repair or suppress residue. Inspection only.

## Phase 2 — SQLite URI-mode read-only residue inventory

Open the authoritative SQLite file with URI `mode=ro`. Do not permit SQLite to create a new database. Record `PRAGMA integrity_check` and require exact `ok`.

Read-only schema inspection is allowed (`sqlite_master`, `PRAGMA table_info`). Do not use DDL/DML/transaction writes.

### Tickets

If table `tickets` exists:

- publish counts grouped by `status`;
- classify nonterminal rows as statuses outside the accepted terminal set `completed`, `failed`, `cancelled`;
- publish nonterminal count;
- for nonterminal rows, publish only non-semantic identifiers/state metadata needed for diagnosis (ticket ID, status, timestamps/attempt counters where columns exist), not prompt/message/body content.

Required clean baseline for Dashboard advancement:

`nonterminalTickets = 0`

Historical terminal Tickets may remain and are not a blocker if unambiguously terminal.

### Ticket outbox

If `ticket_outbox` exists:

- publish counts grouped by `delivery_status`;
- publish exact pending count;
- inspect table columns first and publish only non-semantic delivery metadata for pending/nonterminal rows: row/outbox ID, ticket ID, delivery status, attempt count, created/updated/attempt/ack timestamps where present;
- do not read or reproduce semantic payload/message bodies unless unavoidable to distinguish identity; prefer hashes/lengths over content.

Required clean baseline:

`pendingOutbox = 0`

Historical acknowledged/sent/terminal delivery rows are allowed if classified as historical and not active.

### Workflow / delivery state

Inspect only existing tables whose names clearly correspond to workflow/delivery/recovery state (for example names containing `workflow`, `outbox`, `delivery`, or the known direct-recovery table). Use `sqlite_master` and `PRAGMA table_info` rather than assuming a schema.

For each relevant table:

- publish table name;
- status/state counts when an obvious `status` or `state` column exists;
- classify rows that are clearly active/nonterminal using repository-defined terminal semantics where known;
- publish non-semantic IDs/timestamps for any active row;
- do not infer terminal semantics for an unfamiliar table without source/schema evidence—mark it `INDETERMINATE` instead.

Specifically inspect `cnx_direct_recovery` if present and prove there is no active recovery row that could dispatch old work after the Dashboard baseline.

## Phase 3 — cross-surface reconciliation

Reconcile launcher/status and SQLite results:

1. `status.pendingOutbox` (if exposed) must equal the direct SQLite pending count.
2. Delivery check must not report an active/pending unsafe delivery condition.
3. No nonterminal Ticket may be present.
4. No active workflow/direct-recovery row may be present, or any retained nonterminal-looking row must be proven inert by repository semantics.
5. SQLite integrity must be `ok`.
6. Runtime must remain managed/Ollama/READY without any lifecycle action.

If counts disagree, state is active, or semantics are ambiguous, verdict is `BLOCKED` / `INDETERMINATE`. **Do not clean up, retry, cancel, ack, delete, or normalize anything.**

## Dashboard advancement criterion

Task 135 may recommend opening the final Dashboard durable-delivery acceptance only if all of the following are proven read-only:

- `pendingOutbox = 0`;
- `nonterminalTickets = 0`;
- no active workflow/direct-recovery/delivery residue;
- all retained delivery rows are historical/terminal or otherwise inert with clear semantics;
- runtime remains managed/Ollama/READY;
- SQLite integrity `ok`;
- no mutation or semantic Send occurred during Task 135.

This task itself **must not** open or send the Dashboard message.

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260829-135-post-recovery-delivery-residue-readonly-closeout.md`

Include:

- exact coordination HEAD at execution start;
- evidence root;
- installed launcher hash/text/parsed root;
- literal read-only commands and exit codes;
- runtime/recovery status;
- authoritative SQLite path and read-only integrity result;
- ticket status counts and `nonterminalTickets`;
- outbox status counts and exact `pendingOutbox`;
- relevant workflow/delivery/direct-recovery tables and active-state classification;
- reconciliation between status/check surfaces and direct SQLite;
- explicit statement that semantic payload bodies were not read/published except if strictly unavoidable;
- explicit no write/no cleanup/no lifecycle/no recovery/no Dashboard Send;
- verdict `PASS`, `BLOCKED`, `FAIL`, or `INDETERMINATE`;
- recommendation: either `READY_FOR_FINAL_DASHBOARD_DURABLE_DELIVERY_ACCEPTANCE` or the exact next read-only diagnosis needed.

Then STOP for independent ChatGPT review. Do not automatically open the Dashboard task.

## Hard fence

Forbidden under Task 135:

- Dashboard/UI semantic Send;
- Ticket create/dispatch/retry/cancel/delete;
- workflow create/run/resume/cancel;
- outbox retry/ack/delete/update;
- any SQLite write/DDL/migration/initialization;
- install/install-over/reset/uninstall/reinstall;
- start/stop/restart/enable/disable;
- recovery suite/crash injection/process kill;
- provider/model/OpenClaw/config mutation;
- task/service mutation;
- cleanup/normalization;
- reboot;
- credentials/secrets;
- source/runtime repair;
- merge/tag/release;
- force push.