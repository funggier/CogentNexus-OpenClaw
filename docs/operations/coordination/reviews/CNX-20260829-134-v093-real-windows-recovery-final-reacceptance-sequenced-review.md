# Independent Review — CNX-20260829-134 v0.9.3 Real-Windows Recovery Final Re-Acceptance (Sequenced Harness)

## Verdict

**ACCEPTED RECOVERY PASS — the Task-133 exact candidate completed the newly authorized one-shot real-Windows recovery suite through baseline, Gateway crash, provider crash, the repaired provider→operator carried-incident boundary, intentional operator stop/no-auto-recovery, and strict post-start READY convergence. The live recovery acceptance itself is accepted. Dashboard durable-delivery advancement remains gated only by a missing Task-134 Phase-3 publication item: explicit read-only outbox/status residue classification. Do not rerun recovery and do not send a Dashboard semantic message until that residue is published.**

## Accepted live result

Task 134 started from exact coordination HEAD `ac27df1308b9573ec83d8944b097e5eeee71b2f9` and used accepted source candidate `1424d6fbee2c458c8c30440616783d2fa1bc1201` with recovery harness blob `a4138e00e2056db89b0a9eceed1b54e001c4e319` from an isolated candidate checkout. The live installed launcher/root authority remained `C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd` → `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw`.

The report establishes all material recovery gates:

- already-safe preflight: managed / running / running, Ollama selected, recovery exact `READY`, installed fingerprint exact, OpenClaw `2026.7.1-2`, one loaded/enabled plugin, Gateway/Ollama healthy, SQLite URI-mode read-only integrity `ok`;
- true interactive PowerShell PTY and exactly one lowercase `y` after the literal prompt;
- exact harness process launched once, exit `0`, suite `PASS`, no rerun;
- baseline PASS under strict ordinary `READY`;
- Gateway crash PASS, PID `14620` → `11788`, exact PID only, no process-tree kill, strict convergence `READY`;
- provider crash PASS, PID `18180` → `5220`, circuit closed, convergence `READY_WITH_WARNINGS` with exactly one allowed open/circuit-closed provider incident WARN and every other recovery check PASS;
- carried incident ID `ollama:3`, classification `provider_unreachable`, accepted at `operator-before` only in the directly following same-process provider→operator boundary;
- harness-owned intentional stop PASS, maintenance/stopped desired state observed, Gateway remained stopped during the intentional observation, no automatic recovery occurred;
- harness-owned start PASS and post-start convergence returned through the strict ordinary path to exact `READY`;
- final managed/running/Ollama state, no active provider incident, listeners healthy, unchanged model inventory, SQLite integrity `ok`;
- no installer replay, no standalone lifecycle outside the harness, no manual normalization, no provider/model/OpenClaw/config mutation outside the harness, no Dashboard semantic Send.

This is the first reviewed live suite in this stabilization sequence that exercises and passes the complete provider-crash → operator-stop continuation with the repaired carried-incident contract.

## Repository / execution integrity

The executor publication commit `f9fb834a923591534a529d3e7a3b0fe9bef78cc9` has parent exactly `ac27df1308b9573ec83d8944b097e5eeee71b2f9` and changes only the required Task-134 report. No source, harness, test, workflow, package, or coordination drift was inserted by the live executor.

The Task-134 one-shot ledger is therefore consumed and closed:

- suite `1 / 1`;
- confirmation `1 / 1`;
- Gateway crash `1 / 1 PASS`;
- provider crash `1 / 1 PASS`;
- operator stop/start sequence `1 / 1 PASS`;
- reruns `0`.

Never replay this ledger.

## Remaining publication gap before Dashboard

Task 134 Phase 3 explicitly required `outbox/status residue classification` in the deterministic final read-only snapshot. The published report includes runtime/provider/listener/model/SQLite/task evidence but does not publish:

- `pendingOutbox` from the authoritative ticket snapshot/status;
- read-only `ticket_outbox` status counts or equivalent delivery residue;
- classification of any nonterminal Ticket/workflow/delivery state that could contaminate a one-message durable-delivery acceptance baseline.

This omission does **not** invalidate the recovery scenarios that already passed and must not cause a recovery rerun. It is, however, material to the next Dashboard test because the next test must distinguish exactly one newly created semantic message/Ticket/workflow/outbox attempt/ack from pre-existing residue.

Repository source already exposes the relevant read-only ticket snapshot semantics: `ticket_snapshot(root)` counts tickets by status and reports `pendingOutbox` from `ticket_outbox WHERE delivery_status='pending'`. A direct SQLite URI `mode=ro` query may supplement that status output without mutating state.

## Required next step

Open a narrowly scoped **post-recovery delivery-residue read-only closeout**. It should use the same installed launcher/root authority and authoritative SQLite database to publish a deterministic baseline of Ticket/workflow/outbox/delivery residue. It must not send a message, create/cancel/retry a Ticket, execute a workflow, manipulate outbox rows, run lifecycle/recovery operations, normalize state, or write the database.

If the residue is clean (or all retained rows are terminal and unambiguously historical, with `pendingOutbox=0` and no active/nonterminal delivery work), independently accept that closeout and then open a separate final Dashboard durable-delivery task authorizing exactly one fresh semantic nonce/message Send.

If residue is nonzero or ambiguous, fail closed and diagnose it read-only before any Dashboard Send.

Final merge/tag/release remains unopened.