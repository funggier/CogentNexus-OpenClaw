# CNX-20260829-124 — v0.9.3 Remaining Real-Windows Lifecycle Acceptance

## Verdict

**FAIL — executor-side recovery-harness confirmation boundary; product recovery behavior was not tested.**

The exact remaining lifecycle sequence completed reset, uninstall, exact-candidate fresh reinstall, stop, start, and restart once each. The exact recovery harness then failed before its first disruptive scenario because its interactive `Read-Host 'Type y to continue'` confirmation received no input in the non-interactive invocation. The harness recorded `Disruptive suite cancelled.` and exited `1`. No recovery scenario was replayed.

This is not evidence of a product failure. The recovery suite's disruptive scenarios remain unproven and require a separately authorized successor task with an explicit, supported confirmation boundary.

## Frozen candidate and artifact identity

- Source candidate: `01d08cd7c82f542c821e3a60f7fffa036efb1d75`
- Artifact ID: `9691451156`
- Artifact digest: `sha256:9db9290e14646575586a42160b79cfea691e35f3a0ca7d294f7f941dcae0c87a`
- ZIP SHA256: `8e06b186e425170a22bfce06fa3505a7cdac3b097d4bfdc4ccc4d810d502cac1`
- tar.gz SHA256: `6a14cb665ca6148ce2912970df62027533aef34fb0c871a2e542d1b149e94f31`
- Payload file count: `178`
- Installed plugin fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`

## Evidence

Fresh retained evidence root:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx124-lifecycle-20260829`

Additional deterministic direct-probe evidence:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx123-readonly-attestation-20260829-direct`

Recovery harness evidence:

- Log: `C:\Users\CDQ-P\Downloads\CNXCLAW_V093_OLLAMA_RECOVERY_V3_20260829-061026.txt`
- JSON: `C:\Users\CDQ-P\Downloads\CNXCLAW_V093_OLLAMA_RECOVERY_V3_20260829-061026.json`
- Exact harness: `cnx121-attested-20260828\candidate\cogentnexus-openclaw-v0.9.3\scripts\test-v093-ollama-recovery-windows-v3.ps1`

## One-shot ledger

- Task-121 install-over: **1 / 1 consumed; not replayed**
- Task-124 reset: **1 / 1**
- Task-124 uninstall: **1 / 1**
- Task-124 fresh reinstall: **1 / 1**
- Task-124 stop: **1 / 1**
- Task-124 start: **1 / 1**
- Task-124 restart: **1 / 1**
- Task-124 recovery harness: **1 / 1 attempted; failed before scenario execution**

No completed or failed phase was replayed.

## Phase results

### Fresh sanity fence

Task-123 deterministic direct probe was run before reset and exited `0`. It confirmed the coherent managed state, exact installed fingerprint, ownership, Gateway/Ollama readiness, and SQLite integrity.

### Reset — one attempt

- Command: explicit `C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd reset`
- Confirmation: one literal `y`
- Evidence: `b01-reset.txt`
- Exit code: `0`
- Result: `COGENTNEXUS-OPENCLAW RESET: PASS`

The post-reset deterministic proof exited `0`; managed fresh-install state, provider status, recovery `READY`, ownership, exact fingerprint, and SQLite `ok` were confirmed.

### Uninstall — one attempt

- Command: explicit `C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd uninstall`
- Confirmation: one literal `y`
- Evidence: `c01-uninstall.txt`
- Exit code: `0`
- Result: `COGENTNEXUS-OPENCLAW UNINSTALL: PASS`

The supported uninstall reported native OpenClaw handoff, provider preservation, and successful CNX removal. No manual cleanup was performed.

### Preservation proof

- Evidence: `c02-preservation-proof.txt`
- Exit code: `0`
- OpenClaw `2026.7.1-2` remained present.
- Ollama REST/models remained present and unchanged.
- Gateway listener remained present.
- CNX-owned plugin/skill/state were absent as expected after supported uninstall.

### Fresh reinstall — one attempt

- Exact candidate installer: `C:\Users\CDQ-P\AppData\Local\Temp\cnx121-attested-20260828\candidate\cogentnexus-openclaw-v0.9.3\scripts\install.ps1`
- Command: provider-neutral installer with the exact workspace
- Evidence: `d01-fresh-reinstall.txt`
- Exit code: `0`
- Result: installation completed successfully.

Post-reinstall deterministic proof exited `0` and reconfirmed the exact fingerprint, ownership, managed state, healthy Gateway/Ollama, and SQLite `ok`.

### Stop — one attempt

- Command: explicit `C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd stop`
- Evidence: `e01-stop.txt`
- Exit code: `0`
- Result: stop passed; Gateway and Ollama were stopped under the supported lifecycle command.

Post-stop proof: `e02-post-stop-proof.txt`, exit `0`; Gateway listener `0`, Ollama listener `0`, and stopped/maintenance state was coherent.

### Start — one attempt

- Command: explicit `C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd start`
- Evidence: `e03-start.txt`
- Exit code: `0`
- Result: start passed.

The output and subsequent deterministic proof confirmed Gateway and Ollama healthy, provider `ollama`, exact fingerprint, and SQLite integrity.

### Restart — one attempt

- Command: explicit `C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd restart`
- Evidence: `e04-restart.txt`
- Exit code: `0`
- Result: restart passed.

The output confirmed Gateway and Ollama healthy after restart.

### Recovery harness — one attempt

- Command: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test-v093-ollama-recovery-windows-v3.ps1 -Scenario all -RunDisruptive`
- Evidence: `f01-recovery-harness.txt` plus the retained log/JSON above
- Exit code: `1`
- First failing boundary: before `gateway-crash`, `provider-crash`, or `operator-stop` began
- Exact failure: `Disruptive suite cancelled.`

Prechecks passed: OpenClaw version, OpenClaw config validation, and Ollama version. The harness then entered `Confirm-Disruptive`, which requires interactive `Read-Host 'Type y to continue'`. The invocation supplied no interactive confirmation, so the suite cancelled. Its best-effort cleanup-start passed and restored healthy managed state; no harness replay was attempted.

The harness source confirms this exact boundary at `function Confirm-Disruptive`: it throws `Disruptive suite cancelled.` unless the interactive answer is exactly `y`.

## Final state and safety

The cleanup-start evidence in the harness JSON recorded healthy managed state with Gateway listening on `127.0.0.1:18789`, Ollama listening on `127.0.0.1:11434`, recovery `READY`, provider `ollama`, and SQLite integrity previously confirmed `ok`. No final disruptive scenario was run.

There was:

- no Task-121 install-over replay;
- no candidate/artifact substitution;
- no source edit or ad-hoc live repair;
- no manual cleanup or normalization;
- no OpenClaw update/rebaseline;
- no provider/model/endpoint/timeout change;
- no credential or secret access;
- no Dashboard semantic Send;
- no reboot or generic process-tree kill outside the exact reviewed harness contract;
- no merge, tag, release, or force push.

## Successor scope

A successor task would need to define an explicit non-interactive confirmation mechanism for the reviewed recovery harness, or explicitly authorize a controlled interactive invocation. It must not replay any completed Task-124 phase and must not infer product recovery results from this cancelled run.
