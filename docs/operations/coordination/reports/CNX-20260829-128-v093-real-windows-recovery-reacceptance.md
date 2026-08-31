# CNX-20260829-128 — v0.9.3 Real-Windows Recovery Re-Acceptance

## Verdict

**BLOCKED — the required live preflight was not already safe, so the authorized repaired-harness recovery suite was not launched. No recovery disruption, lifecycle replay, provider mutation, or cleanup was performed.**

## Authority and exact candidate

Task 128 remained authoritative after a fresh fetch of `agent/v0.9.3-full-stabilization`.

- Task: `CNX-20260829-128`
- execution mode: `LIVE_WINDOWS_RECOVERY_ACCEPTANCE_ONLY`
- accepted Task-127 candidate: `1b922bf400fdbccb1f9c7019b89b69fd67f44070`
- exact harness: `scripts/test-v093-ollama-recovery-windows-v3.ps1`
- exact harness Git blob: `622f70b339fea0f2ef7c564253aa3c6bf90ffc97`
- package proof artifact: `9706878201`
- package digest: `sha256:c5dcbda0858a08362daa3218c2912ddd4a36c259e61a05be28d7b1d4114b104c`
- payload count: `178`
- payload fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`

An isolated detached checkout at the accepted candidate was created outside the installed runtime workspace. Its harness hash matched the required blob. The candidate-to-current coordination diff contained only coordination files; no installed runtime/plugin/installer production change requiring deployment was found.

## Fresh evidence root

`C:\Users\CDQ-P\AppData\Local\Temp\cnx128-recovery-20260829T081500Z`

Read-only evidence includes:

- `a01-status.txt`
- `a02-provider-status.json`
- `a03-recovery.json`
- `a04-ownership.txt`
- `a05-fingerprint.txt`
- `a06-recovery-preflight.json`
- `a07-readonly-final-preflight.json`

## Read-only preflight

Passed:

- ownership manifest verification using the verified state root;
- exact installed plugin fingerprint;
- recovery ownership preflight (`OWNERSHIP_PRESENT`);
- OpenClaw version: `OpenClaw 2026.7.1-2 (0790d9f)`;
- Ollama REST `/api/tags`: success, four-model inventory captured;
- Ollama REST `/api/version`: `0.32.15`;
- Gateway listener: `127.0.0.1:18789`, PID `16228`;
- Ollama listener: `127.0.0.1:11434`, PID `14476`;
- relevant scheduled tasks were present and `Ready` with `LastTaskResult=0`.

The captured Ollama inventory includes `qwen3.5:9b`, `muse-glimmer:30b`, `qwen3.6:27b`, and `qwen3.8:27b`. No model/configuration change was made.

## First blocking condition

The first complete status/recovery preflight was not safe for Task 128:

- host mode: `passthrough` (required: `managed`);
- host selected provider: `null` (required: `ollama`);
- provider selected provider: `null` (required: `ollama`);
- recovery verdict: `READY_WITH_WARNINGS`;
- `Supervisor health snapshot`: `WARN`, `No supervisor health snapshot exists yet`;
- provider recovery check reported no selected provider and therefore no authoritative provider recovery incident.

A subsequent read-only filesystem probe also could not verify the SQLite database at the status-reported path (`sqliteExists=false`). Therefore SQLite integrity `ok` could not be established. This is an additional unproven required precondition, not a reason to mutate or normalize the live system.

Because the live state was not already safe, the task's Phase 0 rule required stopping before disruption. No attempt was made to use `start`, `restart`, provider selection, reset, install, or manual normalization to manufacture the precondition.

## One-shot execution ledger

- Task-128 exact recovery suite authorization: `0 / 1 launched`;
- baseline: not started;
- gateway-crash: not started;
- provider-crash: not started;
- operator-stop: not started;
- interactive confirmation: not reached;
- lowercase `y`: not entered;
- no alternate confirmation mechanism used.

The canonical command was therefore **not executed**:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File <exact-candidate-path>\scripts\test-v093-ollama-recovery-windows-v3.ps1 -Scenario all -RunDisruptive
```

## Fences honored

No install/install-over, reset, uninstall, reinstall, standalone lifecycle command, provider/OpenClaw/config/model mutation, process kill, recovery disruption, manual cleanup, normalization, Dashboard semantic Send, credential access, merge, tag, release, or force push occurred.

No final post-suite snapshot is claimed because the suite did not pass and was never launched.

## Required next step

This Task-128 attempt is blocked by the current live precondition. A future continuation requires authoritative review and a new explicit authorization or state correction under the coordination process. This report does not authorize any mutation or recovery replay.
