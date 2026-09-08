# CNX-20260905-252 — Independent Review

## Verdict

`ACCEPT_BLOCKED_TASK251_CHILD_STAGE_UNPROVEN__SCHEDULER_TIMEOUT_AND_BUFFERED_RUNNER_EVIDENCE_LOSS_PROVEN__STREAMING_DIAGNOSTIC_RUNNER_TDD_REQUIRED`

## Reviewed authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Reviewed Task-252 report HEAD: `c1649f064e22492ac324a1f137fc109cff680c62`
- Reviewed report: `docs/operations/coordination/reports/CNX-20260905-252-task251-scheduled-execution-limit-timeout-forensic.md`
- Parent Task-251 report HEAD: `be6be78760fa1071ba2d4749db5ecd20025ac312`
- Exact installer candidate under investigation: `9c3c4e0fe0afbedf9233c25c0dd36e4209fb9d96`
- Public `v0.9.3`: `26ce64a624255278a3a0266ad38746e0e6ed2e31` unchanged at review time.

Fresh branch authority at review opening was exactly the Task-252 report HEAD above. Compare from the Task-252 opening coordination HEAD `c51d2b53125f280ca9536fb2158a097d958d9dda` to the report HEAD contains exactly one commit and one added report file; no production/source/test/workflow drift is present.

## Findings accepted

Task 252 correctly separates the four causal layers required by its authority.

### 1. Scheduler termination mechanism — proven

Task-251 Scheduled Task readback/export proves:

```text
ExecutionTimeLimit = PT45M
AllowHardTerminate = true
RestartCount = 0
terminal LastTaskResult = 267014 / 0x41306
```

The Task-251 child-start marker precedes terminal observation by the configured limit. `0x41306` is therefore scheduler execution-limit termination evidence, not a child exit code.

### 2. Runner evidence-loss mechanism — proven

The retained Task-251 runner SHA-256 is:

`0c2da0cb5877ca9493e4921c3a7b5492dd884841a2bd68c3fb63032b6e42eb98`

Task 252 proves the runner performs redirected `ReadToEnd()` on stdout/stderr and writes `child-stdout.txt`, `child-stderr.txt`, transcript, and terminal result only after child completion. Forced termination of the outer PowerShell runner can therefore leave `runner-started.json` while losing all terminal child evidence. The same runner SHA was retained for Task 248, so this is not a newly introduced Task-251 runner-byte drift.

### 3. Last installer stage — still unproven

The retained residue does not establish completion of `ticket-db-bootstrap`, `plugin-npm-pack`, or `plugin-rollover-prepare`. No Task-251 rollover transaction or diagnostic can be attributed. `plugin-rollover-finalize` and managed convergence are not reached in retained evidence.

The review accepts the report's discipline not to infer a stage from timestamps or absent files.

### 4. Underlying child stall cause — unproven

No retained Scheduler/System/WER/PowerShell/process evidence identifies whether the child spent the 45 minutes in npm, validation, classification, copy/hash/attestation, or another operation. Increasing the execution limit or retrying the installer at this point would therefore be symptom treatment, not root-cause repair.

## Evidence preservation and live-state discipline

Task 252 copied the surviving Task-251 evidence into a separate forensic root and recorded 37,133 files. It reports zero live installer starts, zero new installer registrations, zero rollover invocations, zero plugin/tree/backup mutation, zero lifecycle/DB mutation, zero semantic sends, zero replay/resend, zero manual process termination, and zero source/test/workflow edits.

The canonical post-Task251 boundary remains predecessor plugin identity with controller `passthrough` generation 39, Delivery/Recovery READY, pending delivery 0, and SQLite integrity OK. Task 252 does not authorize interpreting that safe postflight as installer success.

## Provenance limitation

The original Task-251 detached candidate checkout path was later reset during report publication and is no longer available at the execution SHA. This prevents retrospective source-tree inspection at that path, but does not invalidate the preserved launch-manifest/runner binding evidence. A future live attempt must create a fresh disposable exact checkout and retain its identity independently from report-publication workspace operations.

## CI snapshot

At review time, Task-252 report-head PS5.1 Acceptance Smoke `33920039527` and Windows Installer Pack Smoke `33920039525` are terminal SUCCESS. Validate `33920039533` remains in progress. Because Task 252 is a report-only/read-only forensic commit with no source/test/workflow drift, the pending Validate run does not alter this forensic adjudication and does not authorize deployment. Any future live candidate must independently satisfy its exact-SHA deployment gates.

## Successor requirement

The smallest justified successor is repository-only TDD qualification of a reusable Windows PowerShell 5.1 streaming diagnostic runner.

The runner contract must preserve the existing manifest-bound exact-child semantics while ensuring:

- `runner-started.json` is durable before child launch;
- child PID/start metadata is durable immediately after launch;
- stdout and stderr files are created before/during child execution and contain emitted bytes before child termination;
- output is durably flushed incrementally rather than held until `ReadToEnd()` completes;
- normal child completion still records exact child exit code and terminal result;
- child-launch failure remains distinguishable from child nonzero exit;
- forced termination of the outer runner may prevent a terminal result, but MUST NOT erase already-emitted stdout/stderr evidence;
- manifest argument binding remains deterministic and exact;
- no installer/product execution is used to qualify the runner.

A synthetic long-running child must prove that markers are visible on disk while the child is still alive, and a forced outer-runner termination test must prove those partial markers survive.

## Authorization boundary

This review authorizes only the separate repository/test qualification successor. It does NOT authorize:

```text
live installer retry
Task-251 Scheduled Task restart/re-registration
rollover prepare/finalize
plugin/tree/backup mutation
ExecutionTimeLimit increase as a fix
controller/Gateway/provider/model/DB mutation
Dashboard/Discord/API semantic sends
recovery replay/resend
release/tag mutation
```

Independent review is required after the streaming runner qualification before any live installer requalification can be considered.
