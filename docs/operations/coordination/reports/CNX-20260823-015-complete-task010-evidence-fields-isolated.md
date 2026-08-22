# CNX-20260823-015 — Execution Report

Status: FAIL  
Executor: Codex  
Human decision required: NO

## Source and ACTIVE verification

- Repository: `funggier/cogentnexus`
- Coordination branch: `agent/v0.9.3-recovery-reality-tests`
- Start HEAD: `fc3234b75f9641a4566a167d3b18655846923804`
- ACTIVE: `READY_FOR_CODEX`, `Execution mode: AUTO`, Task `CNX-20260823-015`
- Matching report at duplicate-fence check: absent
- Exact authorized worktree: `C:\Users\CDQ-P\.openclaw\worktrees\CNX-20260823-015-evidence`
- Worktree collision check: path absent and unregistered; created once, detached at start HEAD

## Commands and exit codes

- `git fetch origin --prune`: exit 0
- `git worktree list --porcelain` collision check: exit 0; no collision
- Evidence size/hash verification: exit 0 for both files
- `git worktree add --detach C:\Users\CDQ-P\.openclaw\worktrees\CNX-20260823-015-evidence origin/agent/v0.9.3-recovery-reality-tests`: exit 0
- Focused read-only JSON/TXT extraction: exit 0 for the successful bounded extraction; one first extraction command timed out/exit 124 after a PowerShell formatting error and was not used as evidence
- No harness, runtime, listener, service, `cnx`, OpenClaw, Ollama, parser, CI, or lifecycle command was executed by this task

## Immutable evidence identity

- TXT: `C:\Users\CDQ-P\Downloads\CNX_V093_OLLAMA_RECOVERY_V3_20260823-003808.txt`; bytes `1802394`; SHA256 `FBA88FF64D236DF58C9A287BDE7B996D9D35A1D71E3976D7FF1C177553F9705F`
- JSON: `C:\Users\CDQ-P\Downloads\CNX_V093_OLLAMA_RECOVERY_V3_20260823-003808.json`; bytes `5900085`; SHA256 `4F86AA70B88129E9CCB258CEB780B5243D9B0E515362BEC69A40E4F099A90D1F`

## Provenance extracted from immutable evidence

- Suite schema: `4`
- Suite: `v0.9.3-ollama-recovery-reality-windows-v3`
- Provider: `ollama`
- Scenarios: `baseline`, `gateway-crash`, `provider-crash`, `operator-stop`
- Invocation start: `2026-08-23T00:38:08.2829337+07:00`
- Failure: `2026-08-23T00:48:11.3607026+07:00`
- Result: `FAIL`
- Error: `converge-provider-after did not observe durable READY convergence inside RecoveryFuseSeconds.`
- Fuse: `420` seconds
- OpenClaw config path recorded: `C:\Users\CDQ-P\.openclaw\openclaw.json`
- Harness path: `scripts/test-v093-ollama-recovery-windows-v3.ps1`
- Harness bytes: `18782`; Git blob: `6d4c9347de12bbe4e3e5c428f2fe80333f92757f`; SHA256: `5F2DBA46602CA88113B21A0DB8B729BC5AB8DA5FC45E9356F4072DDDD31E929F`
- Harness invocation arguments: `Scenario all`, `RunDisruptive`; exact output paths and confirmation text are not recorded in the JSON provenance fields (`NOT_RECORDED`)

## Scenario results and gates

| Gate/scenario | Result | Exact evidence |
|---|---|---|
| Healthy MANAGED/Ollama baseline | PROVEN | `assert-managed-baseline` PASS at `00:38:18.2000424`; mode `managed`, provider `ollama`, recovery `READY`; Gateway PID `37500`, Ollama PID `55264` |
| Gateway exact-PID crash and runtime recovery | PROVEN | target `node.exe` PID `37500`, exact `Stop-Process` action; replacement PID `27560`; listener recovered at `00:39:47.2793271` |
| Gateway durable-state convergence | PROVEN | first `READY_WITH_WARNINGS` at `00:39:57.8919417`; final `READY` at `00:40:07.4961690`; 2 attempts, 20.211 seconds; observation-only |
| Ollama exact-PID listener crash and runtime recovery | PROVEN | target `ollama.exe` PID `55264`; replacement PID `46240`; listener recovered at `00:41:06.4349130` |
| Provider incident lifecycle | PROVEN | incident `ollama:3`, classification `provider_unreachable`, `incident_opened`, then automatic recovery attempt sequence `1` with `success=true`; incident remained open in later observations |
| Provider durable-state convergence | FAILED | every recorded convergence observation remained `READY_WITH_WARNINGS`; final step `converge-provider-after` FAIL at `00:48:11.2880368`; suite failure at `00:48:11.3607026` |
| Intentional `cnx stop` remains stopped | SKIPPED | execution stopped at provider convergence failure; no operator-stop step represented after failure |
| Explicit `cnx start` returns healthy MANAGED | SKIPPED | not represented as an operator scenario; only harness best-effort cleanup occurred after failure |
| Final cleanup/health | PROVEN | `cleanup-start`, `status-cleanup`, `provider-cleanup`, `recovery-cleanup`, `assert-managed-cleanup`, `cleanup-reconcile` all PASS through `00:48:46.7844023` |

## Injection safety

- Gateway endpoint: `127.0.0.1:18789`; target PID `37500`; process `node.exe`, OpenClaw Gateway command identity recorded
- Ollama endpoint: `127.0.0.1:11434`; target PID `55264`; process `ollama.exe`, `serve` identity recorded
- Harness PID: `56220`; ancestors recorded as `[54064,48112,40316,7908,2176,1060,956]`
- Exact kill action: `Stop-Process exact PID only`; both injection steps recorded PASS
- Process-tree kill: not used / no process-tree operation represented
- Protected-target rejection evidence: harness ancestor list and target identity checks recorded; no protected target selected
- Active-operation persistence timestamp: `NOT_RECORDED` in final evidence fields
- Kill exit status: `NOT_RECORDED` as a separate field; injection step itself recorded PASS
- Replacement listener observations: Gateway PID `27560`; Ollama PID `46240`

## Provider incident chronology

- Pre-injection healthy: `00:40:12.2040848`, recovery `READY`, Ollama listener PID `55264`
- Exact injection: `00:40:13.6511335`, PID `55264`, exact PID only
- Listener restored: `00:41:06.4349130`, replacement PID `46240`
- First post-crash recovery verdict: `00:41:06.5292791`, `READY_WITH_WARNINGS`, incident `ollama:3`, `provider_unreachable`, `incidentOpen=true`, `recoveryAttempts=0`
- Automatic recovery event: recorded `success=true`, sequence `1`, provider reachable/healthy after restart, but durable incident remained open
- Subsequent durable observations: recorded through `00:48:09.7365388`, all `READY_WITH_WARNINGS`; no stable `READY` observation
- Fuse expiration/failure: `00:48:11.2880368` / `00:48:11.3607026`
- Cleanup transition: `cleanup-start` PASS at `00:48:42.1215395`; final cleanup baseline PASS at `00:48:46.7100623`
- Incident cleared during convergence: `NOT_RECORDED`; final cleanup recovery was healthy

Classification: `RUNTIME_RECOVERED_DURABLE_STATE_STUCK`

## Corrected adjudication

Primary verdict: `PARTIAL_RECOVERY_EVIDENCE_ACCEPTABLE`

Gateway process recovery and durable convergence are proven. Ollama process recovery is proven, but provider durable-state convergence is failed; operator stop/start was not reached. This is not a safety-invariant violation: exact target identity and exact-PID-only injection were recorded.

## Problem contract

- Problem: Ollama listener and health returned, but the durable provider incident remained active and recovery verdict stayed `READY_WITH_WARNINGS` for the 420-second fuse.
- Evidence: immutable JSON result `FAIL`; `converge-provider-after` failure; repeated observations; cleanup PASS; evidence hashes above.
- Blocker type: product/runtime defect (durable provider recovery-state completion), with possible harness/runtime timing interaction still unproven.
- Safe narrow remediation options: (1) create a read-only diagnostic task to inspect the exact incident-clear transition fields from this immutable evidence and offline state-machine code; or (2) create a narrow offline fix-and-validation task for provider incident closure, with CI before any new disruptive run.
- Recommended method: option (1) first, then a reviewed narrow fix task only if code evidence confirms a missing durable close transition. Do not repeat the crash until ChatGPT reviews this report and authorizes it explicitly.
- Human decision required: NO for the next diagnostic task; YES only if a later task proposes another disruptive runtime run or configuration change.

## Side-effect accounting

- This task performed no runtime side effect and did not rerun the recovery suite.
- The report is an evidence extraction/adjudication of the immutable prior run; no crash, restart, stop, start, or process kill was repeated.
- No evidence files were modified, moved, renamed, searched for substitutes, or deleted.
- No `ACTIVE.md` change or successor task was created.

## Cleanup

The exact Task 015 worktree was created as authorized. It contains the report commit and therefore was not removed in this run; no force removal or prune was attempted. No pre-existing Task 007–014 checkout was inspected or changed.

## Recommended next step

ChatGPT should review this report and publish the narrowest read-only diagnostic or offline provider-state fix task. The provider crash scenario must not be repeated until that reviewed disposition exists.
