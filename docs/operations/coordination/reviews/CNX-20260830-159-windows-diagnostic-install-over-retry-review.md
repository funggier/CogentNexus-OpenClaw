# CNX-20260830-159 — Windows Diagnostic Install-Over Retry Review

Disposition: `ACCEPT`

Reviewer: `ChatGPT`

Executor: `Hermes on the operator's real Windows/OpenClaw environment`

Review type: `post-execution evidence review`

## Scope

Review the Task-159 single real-Windows diagnostic install-over retry and determine whether the repaired/diagnostic candidate is now proven installed and healthy enough to unblock the next, separate Dashboard durable-delivery reacceptance checkpoint.

Task:

`docs/operations/coordination/tasks/CNX-20260830-159-windows-diagnostic-install-over-retry.md`

Report:

`docs/operations/coordination/reports/CNX-20260830-159-windows-diagnostic-install-over-retry.md`

Report/evidence publication commit:

`5615b8beda31ba4da0636f4cde7a51a2e197afc9`

Pre-Hermes coordination HEAD:

`d6f376e9e2ba80d41aaaa777e6819634e04e949d`

Accepted production lineage required by Task 159:

- Dashboard durable-authority repair: `1ec8cfc81b8a21a178200c33816427f9abfd31b9`
- installer observability repair: `2e8ff49da2573d87236fa7a004bc156d8c94b880`

## Evidence reviewed directly

In addition to the Hermes report, ChatGPT directly inspected the durable raw evidence published by Task 159:

- recovered original Task-157 installer log:
  `docs/operations/coordination/reports/CNX-20260830-159-task157-original-install-over-log.txt`
- Task-159 diagnostic installer stdout:
  `docs/operations/coordination/reports/CNX-20260830-159-diagnostic-install-over-stdout.txt`
- Task-159 diagnostic installer stderr:
  `docs/operations/coordination/reports/CNX-20260830-159-diagnostic-install-over-stderr.txt`

The report/evidence publication commit was compared with the pre-Hermes coordination HEAD. The publication delta is confined to Task-159 coordination report/evidence artifacts; no new production/source modification was introduced by the executor report commit.

## Findings

### 1. The Task-157 raw-evidence gap is closed

Task 158 had to carry an explicit limitation because ChatGPT did not then possess the complete Task-157 live installer capture.

Task 159 recovered and published the original Task-157 raw installer log. ChatGPT inspected the complete durable copy. It ends after the established database snapshot region and does not expose a concrete product/source/install-contract defect that would have made the Task-159 unchanged logical retry unsafe.

The old evidence is therefore consistent with the earlier `BLOCKED` classification: Task 157 lacked enough completion/process evidence to accept the install-over, but the newly recovered log does not convert that checkpoint into a proven source failure.

Result: `PASS`.

### 2. Candidate/provenance gate is satisfied

The live retry used the branch/candidate lineage containing both accepted production repairs, including installer observability SHA `2e8ff49da2573d87236fa7a004bc156d8c94b880`.

The post-install installed plugin fingerprint matches the authorized Task-159 candidate fingerprint. The Task-159 report/evidence publication itself introduced no new product/source delta after the pre-Hermes coordination HEAD.

Result: `PASS`.

### 3. Exactly one install-over process was used

Task 159 used one uniquely tracked installer execution rather than repeating the Task-157 opaque foreground-call pattern. The report/process evidence establishes that no second install-over was launched as a response to observation/orchestration boundaries.

This satisfies the Task-159 process-uniqueness safety requirement.

Result: `PASS`.

### 4. Installer-owned stage diagnostics prove completion of every critical late substage

The Task-159 stdout contains the expected machine-searchable diagnostic records for all seven required critical stages:

1. `ticket-db-bootstrap`
2. `plugin-npm-pack`
3. `plugin-rollover-prepare`
4. `plugin-install-local-package`
5. `plugin-disable-post-install`
6. `plugin-rollover-finalize`
7. `owned-runtime-ensure`

Every stage has both START and COMPLETE, and every captured child exit code is `0`.

The longest observed stage was `plugin-rollover-prepare` at approximately 231 seconds. This explains why the earlier fixed observation window was capable of becoming operationally misleading without itself proving a source defect.

Result: `PASS`.

### 5. Successful install completion is corroborated across independent evidence layers

The detached parent installer's numeric exit code was not directly retained by the wrapper. This is an evidence limitation and must not be silently represented as a captured `exit 0` for the parent process.

However, the limitation is not sufficient to block acceptance because multiple independent evidence layers converge:

- the single installer process was observed through termination;
- all seven critical child stages returned and recorded exit code `0`;
- the complete stdout reaches the installer's explicit successful-completion boundary;
- post-install installed fingerprint equals the authorized candidate fingerprint;
- post-install CogentNexus state reconciles to `managed`;
- the plugin is enabled/loaded;
- gateway/health evidence is healthy.

Taken together, these prove the successful install-over substantially more strongly than a parent exit code alone would.

Result: `PASS`, with the parent-exit-code limitation retained as a review note.

### 6. Installed identity and live health are accepted

Post-install evidence proves the authorized candidate is installed rather than merely built or staged.

The live machine returns to the expected managed state with the CogentNexus-OpenClaw plugin enabled/loaded and relevant gateway/health checks healthy. No relevant package/schema/plugin-loader failure was found in the inspected post-install evidence.

Result: `PASS`.

### 7. stderr warning is non-blocking

The durable stderr includes a Node `DEP0190` warning concerning shell execution / unsanitized argument handling. It is not accompanied by installer failure, stage failure, provenance mismatch, or post-install health failure in this checkpoint.

It remains observable technical debt but does not invalidate Task-159 install acceptance.

Result: `PASS` for this checkpoint.

### 8. Task fence was preserved

Task 159 performed the authorized single install-over and evidence collection only.

The evidence reports:

- Dashboard semantic Sends: `0`
- no Dashboard semantic acceptance interaction
- no reset
- no clean uninstall
- no fresh reinstall after uninstall
- no manual Ticket/workflow/outbox/delivery/database semantic mutation
- no source repair on the live machine
- no dependency upgrade
- no OpenClaw source patch
- no retry/timeout/rollback/kill behavior redesign
- no merge/tag/release/promotion
- no force push

Result: `PASS`.

## Disposition

`ACCEPT`

Task 159 resolves the live repaired-candidate install-over checkpoint that Task 157 left `BLOCKED`.

The accepted candidate is now proven installed on the real Windows/OpenClaw environment with matching provenance and healthy managed/plugin/gateway state.

This review does **not** itself complete Phase P. No Dashboard semantic message has yet been used to reaccept durable delivery on the newly installed repaired candidate.

## Required successor

The next checkpoint must remain separate: one tightly scoped real Dashboard durable-delivery reacceptance task.

That successor may authorize exactly **one** semantic Dashboard Send, must collect durable Ticket/run/result/delivery evidence for that one Send, must not silently retry a failed or ambiguous Send, and must stop after publishing evidence for ChatGPT review.
