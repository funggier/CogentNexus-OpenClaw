# CNX-20260822-008 — Codex Execution Report

Task ID: `CNX-20260822-008`
Status: `BLOCKED`
Repository: `funggier/cogentnexus`
Branch: `agent/v0.9.3-recovery-reality-tests`
Start HEAD: `26cedb9b4c2938cfe68dea536074765d601d14f4`

## Gates

- Literal workflow-fix SHA matched `929fbcc663251941d88f38f09544068a9b3e069d`; object exists and is an ancestor.
- Required ancestors `5a22d9479ad7d62c7a159e4b49e2bc3f79fb6171` and `592a6fbd37da05013b7a8a5875ccd8b17e188cfa` exist and are ancestors.
- Harness object lookup matched required blob `6d4c9347de12bbe4e3e5c428f2fe80333f92757f`.
- Exact-head applicable CI completed successfully: `Windows Installer Pack Smoke` run `32583402908`; `Validate` run `32583402822`; `PS5.1 Acceptance Smoke` run `32583402872`; `PS5.1 Live Runner Smoke` run `32583402804`; `PS5.1 v0.9.3 Gateway Convergence Smoke` run `32583402808`; `PS5.1 v0.9.3 Ollama Recovery V3 Smoke` run `32583402839`; `PS5.1 v0.9.3 Ollama Recovery Reality Smoke` run `32583402830`; `PS5.1 v0.9.3 Ollama Recovery V2 Smoke` run `32583402807`.

## Read-only preflight

`openclaw.cmd --version` exited 0 (`2026.7.1-2`); config validation exited 0. `ollama.exe --version` exited 0 (`0.32.13`). Installed `cnx.cmd` was `C:\Users\CDQ-P\.openclaw\workspace\cnx.cmd`, SHA256 `0B2EB63FD725236BC6B8F9616307F2B454C4FEBE0BF46CE4DE68F32A9C61B637`.

The read-only checks showed managed mode, selected provider `ollama`, healthy Gateway/Ollama, and recovery verdict `READY` (exit 0). Listeners were `127.0.0.1:18789` PID `53896` (`node.exe`, OpenClaw gateway command) and `127.0.0.1:11434` PID `31364` (`ollama.exe serve`).

## Authorized invocation

The exact command was attempted once with one lowercase `y`:

`powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test-v093-ollama-recovery-windows-v3.ps1 -Scenario all -RunDisruptive`

PowerShell exited 1 before loading the harness: `The argument '.\scripts\test-v093-ollama-recovery-windows-v3.ps1' to the -File parameter does not exist.` The isolated worktree contained only the coordination/root files and had tracked-file deletion residue; the harness path was absent from the checkout even though its Git object/blob gate passed. No scenario ran; no process was killed; no `cnx stop`/`cnx start` ran; no evidence files were produced.

## Safety and next step

No runtime mutation or disruptive scenario side effect occurred. The suite was not rerun and no alternate path was substituted. The Task 008 result is blocked by the unusable isolated checkout; a new task should repair/recreate the clean worktree/source checkout before authorizing another single suite invocation.
