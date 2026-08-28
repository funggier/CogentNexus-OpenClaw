# CNX-20260829-125 — v0.9.3 Recovery-Reality Interactive Confirmation Acceptance

## Verdict

**FAIL — provider-crash recovery did not reach durable READY within the reviewed recovery fuse.**

The exact recovery harness was executed once using a true PTY. The exact interactive confirmation prompt appeared and received exactly one lowercase `y` followed by Enter. The harness recorded `explicit-disruptive-confirmation=PASS` and completed the gateway-crash scenario successfully. It then injected the provider-crash scenario and failed at `converge-provider-after` because durable READY was not observed within `RecoveryFuseSeconds` (420 seconds). The operator-stop scenario did not execute. The harness was not replayed.

This report does not infer a broader product failure beyond the observed provider-crash recovery convergence failure. The exact failure boundary and all retained harness evidence are recorded below.

## Frozen candidate and artifact identity

- Source candidate: `01d08cd7c82f542c821e3a60f7fffa036efb1d75`
- Artifact ID: `9691451156`
- Artifact digest: `sha256:9db9290e14646575586a42160b79cfea691e35f3a0ca7d294f7f941dcae0c87a`
- ZIP SHA256: `8e06b186e425170a22bfce06fa3505a7cdac3b097d4bfdc4ccc4d810d502cac1`
- tar.gz SHA256: `6a14cb665ca6148ce2912970df62027533aef34fb0c871a2e542d1b149e94f31`
- Payload file count: `178`
- Installed plugin fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- Recovery harness blob: `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`

## Evidence

Pre/final deterministic direct-probe evidence:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx123-readonly-attestation-20260829-direct`

Task-125 harness evidence:

- Log: `C:\Users\CDQ-P\Downloads\CNXCLAW_V093_OLLAMA_RECOVERY_V3_20260829-062300.txt`
- JSON: `C:\Users\CDQ-P\Downloads\CNXCLAW_V093_OLLAMA_RECOVERY_V3_20260829-062300.json`
- PTY process session: `proc_b176d1c62e37`
- Exact command used native absolute path to avoid MSYS path conversion:
  `powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:/Users/CDQ-P/AppData/Local/Temp/cnx121-attested-20260828/candidate/cogentnexus-openclaw-v0.9.3/scripts/test-v093-ollama-recovery-windows-v3.ps1 -Scenario all -RunDisruptive`

## Ledger

Previously consumed and not replayed:

- Task-121 install-over: `1 / 1`
- Task-124 reset: `1 / 1`
- Task-124 uninstall: `1 / 1`
- Task-124 fresh reinstall: `1 / 1`
- Task-124 stop: `1 / 1`
- Task-124 start: `1 / 1`
- Task-124 restart: `1 / 1`

Task 125:

- fresh deterministic read-only fence: `PASS`
- exact recovery harness execution: `1 / 1`
- interactive confirmation: `1 / 1`, exact lowercase `y` + Enter
- gateway-crash scenario: `PASS`
- provider-crash scenario: injected; convergence `FAIL`
- operator-stop scenario: `0 / 1`, not reached because of fail-stop
- harness replay: `0`

No lifecycle phase from Task 124 was replayed.

## Execution results

### Fresh deterministic fence

Task-123 direct-probe discipline was run before disruption and exited `0`. It confirmed the installed exact candidate, managed CNX state, ownership/fingerprint, OpenClaw/Gateway, Ollama readiness, and SQLite evidence. No lifecycle control was used to repair the precondition.

### Harness prechecks

All passed:

- OpenClaw version: `2026.7.1-2 (0790d9f)`, exit `0`
- OpenClaw config validation: passed, exit `0`
- Ollama version: `0.32.15`, exit `0`

### Interactive confirmation

The harness prompt appeared in the true PTY:

```text
Type y to continue:
```

Exactly one lowercase `y` plus Enter was submitted. The JSON evidence records:

```json
{
  "name": "explicit-disruptive-confirmation",
  "status": "PASS",
  "confirmation": "y",
  "scenarios": ["gateway-crash", "provider-crash", "operator-stop"]
}
```

### Gateway-crash

The gateway-crash scenario completed `PASS`. The harness observed recovery and proceeded to the provider-crash scenario.

### Provider-crash — first failure boundary

The harness injected the reviewed provider crash and then entered durable convergence polling. It failed with:

```text
converge-provider-after did not observe durable READY convergence inside RecoveryFuseSeconds.
```

- Harness result: `FAIL`
- Exit code: `1`
- Recovery fuse: `420` seconds
- Failure timestamp: `2026-08-29T06:32:05.5117908+07:00`
- Evidence step: `converge-provider-after`
- Exact JSON result: `result: FAIL`

The operator-stop scenario was not executed due to the required fail-stop boundary. No recovery scenario was manually rerun.

### Harness cleanup

The harness ran its own cleanup-start path after the failure and recorded `cleanup-start`, `status-cleanup`, `provider-cleanup`, and `recovery-cleanup` as `PASS`, each with exit `0`. This cleanup was part of the exact reviewed harness contract; no manual cleanup or normalization was performed.

## Safety and scope

- No install/install-over, reset, uninstall, or reinstall was run by Task 125.
- No standalone stop/start/restart was run by Task 125.
- No source or harness edit was made.
- No alternate confirmation mechanism, pipe, stdin synthesis, or wrapper was used.
- No candidate/artifact substitution occurred.
- No provider/model/endpoint/timeout/configuration change occurred.
- No credentials or secrets were accessed.
- No Dashboard semantic Send occurred.
- No reboot or generic process-tree kill occurred; disruptive process targeting was confined to the exact reviewed harness contract.
- No merge, tag, release, or force push occurred.

## Successor scope

Any successor diagnosis or acceptance task must begin from the retained post-harness evidence, distinguish provider-crash convergence from the already-passed gateway-crash scenario, and must not replay Task-124 lifecycle phases or this Task-125 recovery suite without new explicit authorization.
