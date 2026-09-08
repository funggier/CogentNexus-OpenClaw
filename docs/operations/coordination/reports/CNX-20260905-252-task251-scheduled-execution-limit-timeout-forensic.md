# CNX-20260905-252 — Task-251 Scheduled Execution-Limit Timeout Forensic

## Authority and fence

Fresh authority was fetched from `origin/agent/v0.9.3-full-stabilization` at the start of this task. The remote active task was `CNX-20260905-252-task251-scheduled-execution-limit-timeout-forensic.md`, marked `READY_FOR_HERMES`. Candidate `9c3c4e0fe0afbedf9233c25c0dd36e4209fb9d96` remained the investigation candidate and public tag `v0.9.3` remained `26ce64a624255278a3a0266ad38746e0e6ed2e31`.

All work was read-only against live product and Task-251. Evidence was written only under:

`C:/Users/CDQ-P/AppData/Local/CogentNexus-OpenClaw/forensics/CNX-20260905-252/`

## Task-251 evidence preservation

The Task-251 evidence root was copied byte-identically into the Task-252 evidence root. Inventory captured `37,133` files. Key surviving artifacts and SHA-256 values:

- `runner-started.json`: present, `e5ae285276d3a3227bf295b40c20ec09de7d62fb1376acaf53f6ffe11bf3cb99`
- `task-start.json`: present, `46f279c728dd07e330aef0818e9c7ab75e27193a47ef23bca091e3769e459037`
- `launch-manifest.json`: present, `99ecda84424c08be52a42678b74a6d7adeed3a916f591c0e6fdf5b6573fa8bcb`
- `task-registration.json`: present, `ad64f3f802c0d7265ef338113dde79f961230690320e47716c4ca5d99282dccc`
- `task-readback.json`: present, `a280c307b4bb2794792210f16da95b1a071d3e3ba60960cb1915eead8d3f80c7`
- `runner-result.json`: absent
- `child-stdout.txt`: absent
- `child-stderr.txt`: absent
- `runner-transcript.txt`: absent

The Task-251 detached candidate checkout is not currently available at its original path. That path was reset to the later report-publication tip `be6be78760fa1071ba2d4749db5ecd20025ac312` during parent report publication. It was not recreated or overwritten by Task 252. The preserved Task-251 launch manifest and runner artifacts remain the authoritative execution binding evidence; candidate-checkout availability is recorded as a provenance limitation.

## Scheduler termination proof

Read-only export and task readback show:

- task: `CogentNexus-OpenClaw-Task251-Installer-1`
- action: `C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe`
- arguments: `-NoLogo -NoProfile -ExecutionPolicy Bypass -File "...CNX-20260904-251\\runner\\manifest-runner.ps1" -LaunchManifest "...CNX-20260904-251\\launch-manifest.json" -EvidenceRoot "...CNX-20260904-251"`
- working directory: `C:/Windows/System32`
- principal readback: `CDQ-P`, logon type `3`, run level `0`
- `ExecutionTimeLimit`: `PT45M`
- `AllowHardTerminate`: `true`
- `RestartCount`: `0`
- task state after observation: `Ready`
- `LastTaskResult`: `267014` decimal = `0x41306`
- Task Scheduler Operational query in the bounded window: no matching event retained

Task-251 recorded runner child start at `2026-09-04T17:22:05.7455411Z`. The terminal result was observed after the configured 45-minute limit. `0x41306` is scheduler timeout evidence; it is not a child exit code.

## Runner observability semantics

The preserved runner source has SHA-256:

`0c2da0cb5877ca9493e4921c3a7b5492dd884841a2bd68c3fb63032b6e42eb98`

The retained Task-248 runner has the same SHA-256. Static line-level inspection shows:

1. The runner creates the result/output path variables and writes `runner-started.json` before launching the child.
2. It launches the child with redirected stdout and stderr.
3. It calls `StandardOutput.ReadToEnd()` and `StandardError.ReadToEnd()`, followed by `WaitForExit()`.
4. Only after child completion does it write `child-stdout.txt`, `child-stderr.txt`, `runner-transcript.txt`, and `runner-result.json`.
5. The `finally` block can write fallback/result data only if the outer PowerShell process reaches `finally`; forced Scheduler termination can prevent all of those writes.

This exactly explains the observed absence pattern without proving a child exit code. It also shows no material runner-topology difference from the retained Task-248 runner. The runner buffers output rather than streaming it durably.

## Residue and last provable stage

Read-only inventory found no new Task-251 `runner-result`, child output, transcript, or terminal installer artifact. The canonical ownership manifest remained the predecessor installation; postflight remained `passthrough`, generation `39`, Ollama, Delivery/Recovery READY, pending delivery `0`, and SQLite integrity `ok`.

| Installer stage | Required predecessor evidence | Task-251 evidence | Classification |
|---|---|---|---|
| ticket-db-bootstrap | installer invocation and writable runtime preconditions | invocation is proven by runner-started marker; no stage result | unresolved |
| plugin-npm-pack | successful bootstrap and candidate plugin source | no pack result or durable output | unresolved |
| plugin-rollover-prepare | successful pack and attestation inputs | no prepare result, transaction, or diagnostic | unresolved |
| plugin-rollover-finalize | successful prepare transaction | no finalize result or transaction | proven not reached in retained evidence |
| managed convergence | successful finalize and postconditions | predecessor identity and `passthrough` generation 39 remain | proven not reached |

No timestamp-only inference is used. The last installer stage is therefore unproven. No Task-251 generation rollover backup can be attributed from the surviving evidence, and no retained artifact was completed, deleted, renamed, or repaired.

## Historical events and process evidence

Bounded event collection found no matching TaskScheduler Operational, System, or WER event. Windows PowerShell records were collected but do not provide a reliable stage/exit correlation. Post-terminal process inventory found no surviving Task-251 runner/installer process. This absence does not prove that a process never existed; it only establishes that none survived the scheduler termination.

## Causal boundaries

- Scheduler termination mechanism: configured `PT45M` limit with hard termination, followed by task result `0x41306`.
- Runner evidence-loss mechanism: buffered `ReadToEnd()`/`WaitForExit()` and post-completion file writes; outer termination prevented durable terminal artifacts.
- Last provable installer stage: none beyond the runner child-start boundary; stage remains unresolved.
- Underlying reason the child did not return before the limit: unproven. No conclusion is made about npm, hashing, attestation, or another installer operation.

## Effect budget

All values are zero unless noted:

- `scripts/install.ps1` invocations: `0` in Task 252
- Task-251 starts: `0` in Task 252
- new installer task registrations: `0`
- rollover prepare/finalize invocations: `0`
- plugin install/copy/delete/rename: `0`
- retired-project or historical-backup mutation: `0`
- controller/Gateway/provider/model lifecycle mutation: `0`
- Ticket/outbox/recovery/SQLite mutation: `0`
- Dashboard, Discord, and direct API semantic sends: `0`
- recovery replay/resend: `0`
- manual process termination: `0`
- production/source/test/workflow edits: `0`
- release/tag/history mutation: `0`

## Final disposition

`BLOCKED_TASK251_CHILD_STAGE_UNPROVEN__STREAMING_DIAGNOSTIC_HARNESS_REQUIRED`

The forensic evidence proves scheduler timeout and explains why the existing buffered runner lost terminal evidence, but it cannot prove the last installer stage or the underlying child stall cause. The smallest next step is a separately authorized repository-only streaming-diagnostic harness qualification; no installer retry, runner execution, live repair, task re-registration, semantic acceptance, recovery action, or release operation is authorized by this report.

STOP for independent ChatGPT review.
