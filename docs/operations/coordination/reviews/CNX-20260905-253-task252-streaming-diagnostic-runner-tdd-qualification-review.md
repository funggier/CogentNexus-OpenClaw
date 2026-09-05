# CNX-20260905-253 — Independent Review

## Reviewed authority

Reviewed report HEAD:

`92870320e10f2a53f477561f5c4c4d24e6439875`

Task report:

`docs/operations/coordination/reports/CNX-20260905-253-task252-streaming-diagnostic-runner-tdd-qualification.md`

Reviewed implementation candidate:

`cc35ce506b6a9ffee3223ec79ddb0373a898e4a5`

Test-only RED commit:

`bb66b67ff9fe5dec344a59b4d130e0d2a55988d2`

## Findings

### 1. TDD ordering is structurally valid

The RED commit changes only:

`tests/test_task253_manifest_streaming_runner.py`

The production streaming runner does not exist in that commit. The later implementation commit adds only:

`scripts/manifest-streaming-runner.ps1`

The report records the focused RED as `5 failed` and focused GREEN as `5 passed`. The repository history therefore preserves test-only RED -> production implementation ordering.

### 2. Durable streaming behavior is materially proven

The focused suite covers live stdout/stderr visibility while the synthetic target remains alive, preservation of already-emitted markers after outer-runner termination, normal nonzero exit propagation, invalid-target classification, and manifest argument delivery with a path containing spaces.

The implementation also pre-creates stdout/stderr evidence files and uses an OS redirection boundary rather than the Task251 `ReadToEnd()`/post-completion buffering pattern. This closes the specific Task252 evidence-loss mechanism.

### 3. Exact candidate CI gates are green

GitHub Checks for exact candidate `cc35ce506b6a9ffee3223ec79ddb0373a898e4a5` show terminal SUCCESS for all six Validate matrix jobs, Windows Installer Pack Smoke `npm-pack`, package dry-run, and PS5.1 Acceptance Smoke `serializer`.

The report's PS5.1 run-id annotation contains a documentation error: serializer job `101231503736` belongs to run `33938651865`, not `33938651855`. `33938651855` is the Validate run. This is a reporting defect, not the blocking implementation defect below.

### 4. Blocking contract defect: `child-started.json` does not identify the target child PID

Task253 explicitly requires durable child-start metadata after **successful child launch** containing at minimum the **child PID** and executable identity.

The candidate instead launches `%ComSpec%` / `cmd.exe` as the .NET `Process` and then writes:

```text
pid         = $proc.Id
launcherPid = $proc.Id
executable  = manifest target executable
transport   = cmd.exe-redirection
```

`$proc.Id` is the `cmd.exe` redirection launcher PID, not the manifest target process PID. The report explicitly acknowledges this.

This is not a cosmetic naming issue. A future live stall forensic needs a process identity that can be correlated to the actual installer process, Windows process events, lifetime, termination behavior, and any surviving process after the Scheduled Task boundary. The current artifact binds a launcher PID to a different executable identity.

### 5. Blocking contract defect: target launch failure can still create `child-started.json`

The runner writes `child-started.json` immediately after `cmd.exe` starts successfully. Only after `cmd.exe` exits with `9009` does the runner revise the terminal result to:

```text
outcome = child_launch_exception
childStarted = false
```

Therefore an invalid/missing target executable can leave a durable `child-started.json` even though the target child never started. That contradicts the Task253 requirement that child-start metadata be written **after successful child launch** and weakens forensic interpretation of the artifact.

The current regression checks only the final `runner-result.json`; it does not assert that the durable child-start artifact corresponds to an actually-started target process.

### 6. Required runner SHA-256 is omitted from the report

Task253 required the final streaming-runner SHA-256 to be recorded. The implementation computes and embeds `runnerSha256` at runtime, but the published report does not state the final file SHA-256. This is a report-completeness gap. It is secondary to the target-PID contract defect and does not independently justify live execution.

### 7. Hard fences were preserved

The report records zero live installer invocation, zero installer Scheduled Task registration/start, zero rollover invocation, zero live plugin/runtime/database mutation, zero semantic sends, zero recovery replay/resend, and zero release/history mutation. No evidence reviewed contradicts that ledger.

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Disposition

`REJECT_PASS_STREAMING_RUNNER_TARGET_PID_CONTRACT_NOT_MET__DURABLE_STREAMING_PROVEN__TDD_IDENTITY_BINDING_REPAIR_REQUIRED`

Task253 successfully proves the new durable streaming mechanism, but the runner is **not yet qualified as the live forensic boundary** because `child-started.json` does not prove the actual manifest target child identity/PID and can be emitted for a target that never started.

Do not run the live installer from candidate `cc35ce506b6a9ffee3223ec79ddb0373a898e4a5` using this runner.

## Required successor

Open a repository/test-only successor to repair and qualify target-process identity binding. The successor must use TDD and preserve the already-proven durable streaming behavior.

Minimum acceptance:

1. a synthetic target records its own PID; `child-started.json.pid` must equal that exact target PID;
2. the durable child-start executable identity must correspond to the same target process, not a launcher process;
3. invalid/missing target executable must not leave a target `child-started.json` claiming successful child launch;
4. launcher metadata, if retained, must be separately named and must not masquerade as target-child identity;
5. live stdout/stderr must still be visible before target exit;
6. already-emitted stdout/stderr must remain after forced outer-runner termination;
7. normal exit `23`, launch failure classification, and argument binding remain GREEN;
8. synthetic processes must be deterministically cleaned up after forced-termination tests;
9. exact final runner SHA-256, installer SHA-256, plugin fingerprint, public tag, and exact-SHA Actions must be recorded and independently reviewable.

Live installer retry and semantic acceptance remain unauthorized.
