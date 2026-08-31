# CNX-20260829-131 — v0.9.3 Real-Windows Recovery Re-Acceptance with Authoritative Root

## Verdict

**FAIL — the exact one-shot repaired-harness suite passed baseline, gateway-crash, and provider-crash, but failed before the operator-stop scenario because the provider recovery incident remained active under the harness's strict operator-before baseline.** The suite was not rerun. The built-in harness cleanup completed and the final read-only snapshot is healthy.

This is a live acceptance result, not a harness-contract replay or a Task-128 replay.

## Authorization and provenance

- Task: `CNX-20260829-131`
- Start coordination HEAD: `9d09f485d3f3325c25487b91c79accf2241423d5`
- Accepted Task-127 candidate: `1b922bf400fdbccb1f9c7019b89b69fd67f44070`
- Exact harness: `scripts/test-v093-ollama-recovery-windows-v3.ps1`
- Exact harness blob: `622f70b339fea0f2ef7c564253aa3c6bf90ffc97`
- Package proof artifact: `9706878201`
- Package digest: `sha256:c5dcbda0858a08362daa3218c2912ddd4a36c259e61a05be28d7b1d4114b104c`
- Payload count: `178`
- Installed plugin fingerprint expected/observed: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- Installed launcher: `C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd`
- Authoritative state root: `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw`
- Fresh preflight evidence root: `C:\Users\CDQ-P\AppData\Local\Temp\cnx131-recovery-20260829T093000Z`
- Harness evidence text: `C:\Users\CDQ-P\Downloads\CNXCLAW_V093_OLLAMA_RECOVERY_V3_20260829-111830.txt`
- Harness evidence JSON: `C:\Users\CDQ-P\Downloads\CNXCLAW_V093_OLLAMA_RECOVERY_V3_20260829-111830.json`

The candidate checkout was isolated and verified clean at the exact candidate SHA. The execution-copy harness hash matched the accepted blob. No installed runtime/plugin/installer deployment or source edit was performed.

## Corrected authoritative preflight

All CNX live probes used the explicit installed launcher, never the workspace parent as `--root`.

```text
C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd status
exitCode=0

C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd provider status --json
exitCode=0

C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd check recovery --json
exitCode=0

C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd check system
exitCode=0

C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd check provider ollama
exitCode=0
```

Fresh preflight passed:

- mode `managed`
- desired gateway/provider `running`
- selected provider `ollama`
- recovery `READY`
- no active provider incident/circuit
- supervisor health `healthy`
- ownership verification exit `0`
- exact plugin fingerprint exit `0`
- plugin installation check exit `0`
- OpenClaw `2026.7.1-2`
- Gateway listener healthy on `127.0.0.1:18789`, PID `16228`
- Ollama listener healthy on `127.0.0.1:11434`, PID `14476`
- authoritative SQLite exists and read-only `PRAGMA integrity_check` returned `ok`
- scheduled tasks were Ready with last result `0`
- model inventory captured: `qwen3.5:9b`, `muse-glimmer:30b`, `qwen3.6:27b`, `qwen3.8:27b`

The installed launcher SHA256 was freshly recorded as:

`f53df28f2a7ee7fc43c65ba2c48770ed9b7ed3e7b14d3c762f957bd017b90f10`

It explicitly forwards `%*` and targets the authoritative `.cogentnexus-openclaw` root.

## Exact one-shot interactive execution

Literal command:

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\CDQ-P\AppData\Local\Temp\cnx128-recovery-20260829T081500Z\candidate\scripts\test-v093-ollama-recovery-windows-v3.ps1 -Scenario all -RunDisruptive
```

- Execution channel: true interactive PowerShell PTY
- Prompt observed literally: `Type y to continue:`
- Confirmation sent: exactly one lowercase `y` followed by Enter
- Harness process session: `proc_c0ba3413b62b`
- Process exit code: `1`
- Suite authorization consumed: `1 / 1`
- Suite/scenario reruns: `0`

No alternate confirmation, wrapper, harness edit, or candidate substitution was used.

## Scenario results

### Baseline — PASS

The managed/Ollama baseline passed before disruption. Gateway and Ollama were reachable, selected provider was coherent, and recovery was exact `READY`.

### Gateway-crash — PASS

- validated before Gateway PID: `16228`
- recovered Gateway PID: `14620`
- listener returned on `127.0.0.1:18789`
- durable convergence passed
- ordinary recovery remained strict `READY`
- no process-tree kill was used; only the harness's exact validated listener PID action was used

### Provider-crash — PASS under repaired contract

- validated before Ollama PID: `14476`
- recovered Ollama PID: `18180`
- listener returned on `127.0.0.1:11434`
- provider circuit remained closed
- recovery convergence passed under the repaired provider-incident contract
- observed recovery verdict was `READY_WITH_WARNINGS`
- allowed warning was the singular open provider incident `ollama:2`, classification `provider_unreachable`, `circuitOpen=false`; provider event adapter was PASS with `expected=false`
- recovery convergence observation: `attempts=1`, `elapsedSeconds=3.552`

The provider-crash result is a PASS under the explicitly accepted fail-closed warning exception. It does not claim strict `READY` while the incident remains open.

### Operator-stop — NOT REACHED / FAIL STOP

The first failure occurred at:

```text
2026-08-29T11:21:13.3316738+07:00 FAIL :: Managed Ollama baseline failed at operator-before.
```

At `recovery-operator-before`:

- command exit code: `1`
- verdict: `READY_WITH_WARNINGS`
- provider: `ollama`
- incident ID: `ollama:2`
- incident open: `true`
- classification: `provider_unreachable`
- circuit open: `false`
- recovery attempts: `1`
- Gateway and Ollama listeners were healthy
- mode remained `managed`
- selected provider remained `ollama`

The harness's operator-before assertion requires a managed Ollama baseline with strict ordinary recovery readiness. Because the provider incident from the preceding provider-crash scenario remained open, the operator-stop scenario was not launched. No operator-stop command or separate lifecycle operation was performed.

## Built-in cleanup and final read-only snapshot

After the first failure, only the harness's built-in best-effort cleanup ran naturally. No manual lifecycle repair, normalization, process kill, or cleanup command was issued afterward.

Harness cleanup evidence:

- `cleanup-start`: exit `0`
- cleanup returned managed/Ollama state
- final harness evidence recorded generation `24`
- final harness recovery check: `READY`, exit `0`

Final read-only probes through the same installed launcher/root authority recorded:

- mode `managed`
- selected/desired provider `ollama` / `running`
- desired Gateway `running`
- recovery `READY`, exit `0`
- incident closed, circuit closed, recovery attempts `0`
- supervisor snapshot `healthy`
- Gateway listener `127.0.0.1:18789`, PID `14620`
- Ollama listener `127.0.0.1:11434`, PID `18180`
- OpenClaw `2026.7.1-2`
- plugin fingerprint unchanged: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- SQLite read-only integrity: `ok`
- model inventory still contains exactly the four preflight models
- outbox empty in status evidence

Final read-only files are retained as `30-final-*`, `31-final-system.txt`, `32-final-fingerprint.txt`, `33-final-listeners.json`, and `34-final-sqlite.txt` under the fresh evidence root.

## Failure classification

```text
FAIL — operator-before strict managed Ollama baseline rejected READY_WITH_WARNINGS
```

The gateway-crash and provider-crash scenarios passed. The operator-stop acceptance remains unproven because the exact one-shot suite fail-stopped before it could begin. The result does not justify a recovery replay, manual normalization, reinstall, or Dashboard acceptance.

## Ledger and hard-fence confirmation

- Task-131 recovery suite: `1 / 1` consumed
- confirmation: `1 / 1`, exactly one lowercase `y`
- baseline: PASS
- gateway-crash: PASS
- provider-crash: PASS
- operator-stop: not reached
- installer/lifecycle replay: `0`
- source/harness edits: `0`
- alternate confirmation: `0`
- manual cleanup/normalization: `0`
- generic process-tree kill: `0`
- credential/secret access: `0`
- Dashboard semantic Send: **not performed**

Task 131 is complete as a failed one-shot acceptance. Any retry or further recovery scenario requires independent diagnosis/review and a new explicit task authorization. Stop for independent ChatGPT review.
