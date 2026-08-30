# CNX-20260830-159 — Windows Diagnostic Install-Over Retry + Durable Raw Evidence

Status: `READY_FOR_HERMES`

Execution mode: `LIVE_WINDOWS_DIAGNOSTIC_INSTALL_OVER_RETRY`

Current authorization: `CNX-20260830-159_WINDOWS_DIAGNOSTIC_INSTALL_OVER_RETRY`

Task ID: `CNX-20260830-159`

Updated: 2026-08-30 ICT

Owner / coordinator / reviewer: ChatGPT

Executor: Hermes on the operator's real Windows/OpenClaw environment

## Purpose

Resolve the Task-157 blocked Windows install-over checkpoint with substantially stronger evidence.

Task 157 attempted one authorized repaired-candidate install-over, but the executor observation window ended at roughly 420 seconds without a proven installer completion/exit boundary. The repaired candidate was not proven installed; the installed plugin fingerprint remained the previous one; the machine was left at the established safe transition boundary (`passthrough`, plugin disabled); and Dashboard semantic Sends remained zero.

Task 158 is now `ACCEPT` and adds installer-owned stage diagnostics without changing installer behavior. This task may therefore retry the same logical install-over using the accepted diagnostic candidate, while preserving raw process/log evidence durably.

This task is still **not** Dashboard delivery acceptance and does not authorize a semantic Send.

## Authorization lineage

Accepted Dashboard production repair:

`1ec8cfc81b8a21a178200c33816427f9abfd31b9`

Accepted installer observability production repair:

`2e8ff49da2573d87236fa7a004bc156d8c94b880`

Task-158 report:

`docs/operations/coordination/reports/CNX-20260830-158-windows-install-over-observability-recovery-diagnosis.md`

Task-158 review:

`docs/operations/coordination/reviews/CNX-20260830-158-windows-install-over-observability-recovery-diagnosis-review.md`

Task-158 review disposition: `ACCEPT`.

The Task-159 task was opened after Task-158 review from branch state rooted at coordination HEAD:

`b99d96ae36caa603ee6d67e70b087732237059b4`

Later Task-159 coordination-only commits are expected. Before live mutation, Hermes must prove that the production/source payload being installed contains `2e8ff49da2573d87236fa7a004bc156d8c94b880` and has no later unreviewed production/source delta.

## Critical first step — recover the old Task-157 raw log before any new mutation

Before retrying installation, inspect the original Task-157 raw installer log path recorded in durable evidence:

`C:/Users/CDQ-P/AppData/Local/Temp/cnx157-install-over-20260830T0610/install-over.txt`

If it still exists:

1. compute SHA-256 of the original file;
2. preserve its exact byte length and last-write timestamp;
3. publish a faithful text copy as durable Task-159 evidence if reasonably sized;
4. inspect the complete log, not only its tail;
5. report the last clearly completed installer boundary, the final meaningful output/error, and any child command that can be identified from the raw text.

Expected durable copy path when the file exists and is reasonably sized:

`docs/operations/coordination/reports/CNX-20260830-159-task157-original-install-over-log.txt`

If the original log no longer exists, record that fact exactly and continue only if the new retry remains safely evaluable.

### Old-log stop gate

If the complete Task-157 raw log proves a concrete product/source/install-contract defect that would make an unchanged retry unsafe or predictably invalid, **STOP `BLOCKED` before new install mutation** and publish the Task-159 report. Do not patch or repair source under this task.

If the old log does not establish such a blocker, continue with the diagnostic retry below.

## Objective

Hermes must:

1. capture exact live pre-state and current transitional state;
2. recover/publish the Task-157 raw log if still available;
3. prove the exact Task-159 candidate/provenance before mutation;
4. launch **one and only one** install-over process using the established repository install workflow;
5. ensure the installer process remains uniquely observable independently of any individual Hermes/orchestration call duration;
6. durably capture installer stdout/stderr and process metadata;
7. observe/poll the same installer process until it exits or is explicitly proven terminated;
8. collect all `CNXCLAW_INSTALL_STAGE_START` / `CNXCLAW_INSTALL_STAGE_COMPLETE` records;
9. verify installed identity/provenance and lifecycle/loader/command health if installation completes;
10. publish all required evidence and the Task-159 report, then stop.

## Process-survival / uniqueness requirement

Task 157 must not be repeated as a single opaque foreground call whose orchestration timeout destroys the useful observation boundary.

Hermes may use a PowerShell wrapper / `Start-Process` or equivalent established Windows mechanism to start the installer **once**, with durable stdout/stderr redirection and a recorded PID, provided this does not change installer semantics.

Requirements:

- record wrapper/installer command line exactly;
- record installer PID and start UTC before polling;
- redirect/capture stdout and stderr to durable local files;
- do not launch a second installer while the recorded installer PID is still alive or its termination has not been proven;
- an individual Hermes tool-call timeout is **not** permission to kill/relaunch the installer;
- after any executor interruption, first re-observe the recorded PID/process state and existing log, then continue read-only polling;
- if the recorded process cannot be uniquely re-associated, stop `BLOCKED` rather than guessing or launching another installer;
- do not impose a new installer timeout or kill policy under this task.

A harmless non-mutating child-process observation check may be used before install-over if Hermes needs to prove that its wrapper/polling method survives separate executor calls.

## Candidate/provenance gate

Before install-over, prove all of the following:

- branch is `agent/v0.9.3-full-stabilization`;
- accepted Dashboard repair `1ec8cfc81b8a21a178200c33816427f9abfd31b9` is included;
- accepted diagnostic production repair `2e8ff49da2573d87236fa7a004bc156d8c94b880` is included;
- no later unreviewed production/source delta exists after `2e8ff49...` in the candidate;
- coordination/report/review/task commits after the production repair are distinguished from production changes;
- package/archive/plugin identity is attributable to the exact candidate using existing repository provenance mechanisms;
- the proven artifact is the artifact actually passed to the installer.

If this gate cannot be established, stop `BLOCKED` before mutation.

## Required pre-state evidence

Before mutation record, at minimum:

- date/time, Windows and PowerShell context;
- exact repo branch and HEAD;
- production diff/provenance relation to `2e8ff49...`;
- existing installed CogentNexus-OpenClaw/plugin identity/fingerprint;
- current CogentNexus controller/mode state;
- current plugin enabled/disabled state;
- OpenClaw/gateway status relevant to install;
- established health/status commands that are safe and non-semantic;
- whether Task-157 original raw log exists and its SHA-256/size/timestamp if available.

The known Task-157 transitional state (`passthrough`, plugin disabled) is not by itself a failure. Record actual current state; do not assume it is unchanged.

## Authorized live actions

Only these live actions are authorized:

- read-only state/version/provenance/health/log/process inspection;
- recovery/copy/hash of the existing Task-157 raw log;
- candidate creation/build/package using the existing repository process;
- exactly one Task-159 install-over attempt using the established Windows install-over workflow;
- wrapper/process redirection needed only to make that one installer process durable and observable;
- stop/start/restart lifecycle actions only when the existing install-over workflow performs/requires them or when strictly necessary for post-install health proof;
- read-only post-install validation and log collection;
- writing/pushing Task-159 report/evidence files to GitHub.

Use the smallest live mutation surface necessary.

## Hard fence

Task 159 does **not** authorize:

- Dashboard semantic Send;
- Dashboard click/focus/type/paste for semantic testing;
- any new semantic user message through OpenClaw/CogentNexus;
- manual Ticket/workflow/outbox/delivery/DB/semantic-state mutation;
- reset;
- clean uninstall;
- fresh reinstall after uninstall;
- arbitrary live-state deletion;
- manual source patch on Windows;
- dependency upgrade;
- OpenClaw source patch;
- changing `--force` semantics;
- adding/revising rollback, retry, timeout, or kill behavior;
- alternate package-install mechanism as a product repair;
- any new CogentNexus runtime/product behavior change;
- merge/tag/GitHub Release/package publication/promotion;
- force push.

If a new defect appears, preserve evidence and stop `FAIL` or `BLOCKED` as appropriate. Do not fix it inside Task 159.

## New diagnostic evidence contract

The new Task-159 installer run must produce a raw capture whose full text is durably reviewable by ChatGPT.

Expected durable raw-log copy path:

`docs/operations/coordination/reports/CNX-20260830-159-diagnostic-install-over-log.txt`

The Task-159 report must record for the original local raw log:

- local path;
- SHA-256;
- byte size;
- first/last write or available file timestamps;
- whether the GitHub text copy is faithful to the original capture.

The durable raw capture must include all available:

- installer output;
- installer errors;
- `CNXCLAW_INSTALL_STAGE_START` records;
- `CNXCLAW_INSTALL_STAGE_COMPLETE` records;
- stage `utc`, `elapsed_ms`, and `exit_code` fields;
- output surrounding any failed stage;
- output surrounding any START without COMPLETE.

If stdout and stderr are captured separately, publish both faithfully or combine them only if ordering/provenance remains explicit.

Do not silently truncate relevant failures. If a file is too large for a faithful text copy, preserve/hash the original locally and publish every diagnostic marker plus complete relevant stage/error windows with line counts and explicit omission ranges.

## Process metadata evidence

The report must include:

- exact launch command;
- wrapper PID if one exists;
- installer PID;
- process start UTC;
- every observation/poll timestamp relevant to a long-running stage;
- final process state;
- exact exit code where observable;
- whether the same PID survived across separate Hermes calls;
- proof that no second install-over process was launched.

## Post-install acceptance evidence

If the installer exits successfully, evaluate all of the following rather than trusting exit code alone:

1. install-over completed with exact exit status;
2. installed plugin/package identity changed to the authorized diagnostic candidate as expected;
3. installed payload provenance matches the accepted candidate lineage;
4. CogentNexus/OpenClaw lifecycle state is healthy for the established operating mode;
5. relevant plugin/package/schema/loader logs show no new failure;
6. established non-semantic health/status checks succeed, or exact failures are preserved;
7. all stage diagnostics are internally consistent;
8. Dashboard semantic Sends = `0`;
9. every live mutation stayed inside Task-159 authorization.

## Disposition rules

Use:

- `PASS` only if install-over completes and installed provenance + lifecycle/loader/command health are all proven;
- `FAIL` for a proven installer/product/source failure within the authorized candidate/path;
- `BLOCKED` when external/tool/process observability or missing evidence prevents a trustworthy conclusion.

A missing COMPLETE after a START is evidence of the active stage, but does not automatically distinguish external termination from an internal hang. Preserve process-state evidence and do not overclaim root cause.

## Required report

Hermes must publish exactly:

`docs/operations/coordination/reports/CNX-20260830-159-windows-diagnostic-install-over-retry.md`

The report must include:

- `PASS`, `FAIL`, or `BLOCKED`;
- exact candidate/source/package/artifact identities;
- Task-157 original raw-log recovery result;
- pre-state;
- commands/actions in execution order;
- installer/wrapper PID and timing evidence;
- complete stage marker table;
- exact installer outcome/exit code;
- installed identity/provenance evidence;
- post-state/lifecycle/loader/health evidence;
- all live mutations;
- Dashboard semantic Sends count (`0` required);
- durable raw evidence file paths and SHA-256 values;
- remaining uncertainty;
- exact report/evidence commit SHA after push.

## Stop condition

After report/evidence publication, **STOP**.

Do not proceed to Dashboard durable-delivery reacceptance even if Task 159 is `PASS`.

ChatGPT must fresh-read and review Task-159 evidence first. Dashboard semantic testing requires a separate explicitly authorized task.