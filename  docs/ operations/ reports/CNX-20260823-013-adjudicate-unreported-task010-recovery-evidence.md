# CNX-20260823-013 — Evidence Adjudication

- Task ID: `CNX-20260823-013`
- Start HEAD: `5fd9a452a9157e99a515178e6e6f4d91fc956ccf`
- ACTIVE verification: `READY_FOR_CODEX`; `AUTO`; exact Task 013
- Evidence read: only the two named TXT/JSON files after identity verification
- Primary adjudication: `PARTIAL_RECOVERY_EVIDENCE_ACCEPTABLE`

## Commands and exit codes

1. `git fetch --no-tags origin agent/v0.9.3-recovery-reality-tests` — exit `0`.
2. `git show FETCH_HEAD:docs/operations/coordination/{CODEX_BOOTSTRAP.md,WATCH_MODE.md,SIGNALS.md,ACTIVE.md}` — exit `0`.
3. `git show FETCH_HEAD:docs/operations/coordination/tasks/CNX-20260823-013-adjudicate-unreported-task010-recovery-evidence.md` — exit `0`.
4. Matching-report duplicate fence (`git cat-file -e FETCH_HEAD:<matching report>`) — absent; exit `1` for the existence check.
5. `Get-Item` plus `Get-FileHash -Algorithm SHA256` for each exact evidence path — exit `0`; both matched.
6. `Get-Content <exact JSON> | ConvertFrom-Json` and read-only task-field extraction; `Select-String` on the exact TXT — exit `0` (the bounded extraction command timed out after producing output, with no side effect; the focused extraction completed exit `0`).

## Evidence identity

| File | Bytes | SHA256 | Verdict |
|---|---:|---|---|
| `C:\Users\CDQ-P\Downloads\CNX_V093_OLLAMA_RECOVERY_V3_20260823-003808.txt` | 1802394 | `FBA88FF64D236DF58C9A287BDE7B996D9D35A1D71E3976D7FF1C177553F9705F` | PROVEN |
| `C:\Users\CDQ-P\Downloads\CNX_V093_OLLAMA_RECOVERY_V3_20260823-003808.json` | 5900085 | `4F86AA70B88129E9CCB258CEB780B5243D9B0E515362BEC69A40E4F099A90D1F` | PROVEN |

## Provenance and invocation

JSON schema `4`; suite `v0.9.3-ollama-recovery-reality-windows-v3`; provider `ollama`; start `2026-08-23T00:38:08.2829337+07:00`; failure `2026-08-23T00:48:11.3607026+07:00`; duration approximately `603.078 s`. Tested source/harness provenance is recorded in the evidence, including the v3 harness path and harness process metadata. The redacted invocation proves `-Scenario all -RunDisruptive`; the evidence contains an explicit confirmation step, and the text records lowercase `y` at that gate. Final result: `FAIL`; exact error: `converge-provider-after did not observe durable READY convergence inside RecoveryFuseSeconds.`

## Scenario and step matrix

| Area | Evidence result | Supporting facts |
|---|---|---|
| Baseline | PASS / executed | `scenario-baseline`; recovery verdict `READY`; managed Gateway/Ollama healthy and ready. |
| Gateway crash | PASS / executed | Target PID `37500`; exact-PID `Stop-Process`; replacement PID `27560`; later durable recovery verdict `READY`; `scenario-gateway-crash` completed with two convergence observations. |
| Provider/Ollama crash | FAIL / executed | Target PID `55264`; replacement PID `46240`; runtime/listener became healthy, but every provider convergence observation remained `READY_WITH_WARNINGS`; final fuse failed. |
| Operator stop | SKIPPED / not executed | Scenario list names `operator-stop`, but no operator-stop execution/result step is represented before the provider failure. |
| Operator start | SKIPPED / not executed | No operator-start execution/result step is represented. |
| Cleanup | PASS / executed after failure | Cleanup/reconcile ran; recovery verdict `READY`; final managed health was restored. |
| Final health | PASS / evidenced by cleanup | Final cleanup checks report managed/Ollama/`READY`. |

Named scenarios were not treated as PASS without execution/result evidence.

## Exact-PID and no-tree-kill safety

| Injection | Verdict | Evidence |
|---|---|---|
| Gateway | PROVEN | Listener target resolved to PID `37500`; executable/process identity and command line validated; harness PID/ancestor and protected-process rejection gates recorded; active-operation/target persistence recorded; `Stop-Process` exact PID only; replacement PID `27560`; no process-tree kill action recorded. |
| Ollama/provider | PROVEN | Listener target resolved to PID `55264`; `ollama.exe` and `ollama.EXE serve` identity validated; harness PID/ancestor and protected-process rejection gates recorded; active-operation/target persistence recorded; `Stop-Process` exact PID only; replacement PID `46240`; no process-tree kill action recorded. |

No safety invariant violation is proven. Any field not present in the evidence would remain unproven; the recorded gates above are the gates explicitly evidenced.

## Provider incident and convergence

The provider was healthy/ready before injection. The exact-PID Ollama stop caused listener unreachability; the supervisor opened incident `ollama:3` with classification `provider_unreachable`. A replacement Ollama listener PID `46240` appeared and provider health became reachable/healthy, but recovery checks remained `READY_WITH_WARNINGS` with an active provider incident/maintenance marker. No stable-success observation satisfying durable `READY` occurred before the `RecoveryFuseSeconds` timeout. Cleanup then reconciled the state and produced recovery `READY`.

Classification: `RUNTIME_RECOVERED_DURABLE_STATE_STUCK`.

The timeout is an observation fuse, not recovery authority. It proves failure to observe durable convergence within the bounded window, not that the runtime could never converge.

## Gate verdicts

- Healthy MANAGED/Ollama baseline — `PROVEN`
- Gateway exact-PID crash and automatic runtime recovery — `PROVEN`
- Gateway durable-state convergence — `PROVEN`
- Ollama exact-PID listener crash and runtime recovery — `PROVEN`
- Provider incident lifecycle — `PROVEN`
- Provider durable-state convergence — `FAILED`
- Intentional `cnx stop` remains stopped — `SKIPPED`
- Explicit `cnx start` returns to healthy MANAGED state — `SKIPPED`
- Final cleanup/health — `PROVEN`

## Remaining uncertainty and narrow next step

The evidence does not prove operator stop/start behavior, nor does it establish whether the durable marker would have cleared after the fuse. Do not repeat the disruptive suite. The narrow next step is offline review of the provider incident/maintenance-marker transition logic and the existing evidence boundary, followed by a separately authorized task if a new runtime experiment is required.

