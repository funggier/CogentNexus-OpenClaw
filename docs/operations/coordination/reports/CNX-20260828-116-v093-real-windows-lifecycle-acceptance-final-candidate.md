# CNX-20260828-116 — v0.9.3 Real-Windows Lifecycle Acceptance

## Verdict

`FAIL` — Phase 0 read-only reconciliation passed, but the single authorized install-over attempt failed before lifecycle execution with root exit code `1`. Per the hard fence, no retry and no later destructive phase was performed.

## Frozen provenance

- Source candidate: `47b069daed90f54feae2c9eb26f38c438493f3c8`
- Detached pinned source HEAD: verified exact
- Recovery harness blob: `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`
- Artifact: `9687249771`
- Outer SHA256: `c009450560176ce89c8a5a6ef65aec5ce9f821e75053617d56de212cf6093fdf`
- Inner ZIP SHA256: `8771869962babe591c6ba4431b8f4737b716f2258cfcfc6fd45eec4f582b2fc5`
- tar.gz SHA256: `057cc016becd91ba4baf49a3c59152ce9ff467ff0a30b758e8e460e43f6ee2c5`
- Package version: `0.9.3`
- Payload count: `178`
- Payload fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- `PACKAGE_IDENTITY.json`, `PAYLOAD_IDENTITY.json`, and `SHA256SUMS.txt` matched; packaged installer contract was verified from the frozen artifact.

Evidence root:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw-Acceptance-Evidence\CNX-20260828-116\20260828-210020`

## Phase 0 — read-only machine reconciliation

### Baseline

- Windows 10 Pro, build `19045`
- PowerShell `5.1.19041.6456`
- Node `v22.23.2`
- npm `12.0.2`
- Python `3.11.15`
- OpenClaw `2026.7.1-2 (0790d9f)` — exact required baseline
- Ollama `0.32.15`

### CNX/provider/Gateway

- CNX mode: `passthrough`
- Generation: `25`
- Desired Gateway: `running`
- Selected provider: `ollama`
- Provider: installed, reachable, healthy, ready
- CNX openclaw check: `READY`, exit `0`
- CNX Gateway check: `READY`, exit `0`
- CNX recovery check: `READY`, exit `0`
- CNX delivery check: `READY`, exit `0`; pending terminal deliveries `0`
- CNX resources check: `READY`
- Gateway: healthy, loopback `127.0.0.1:18789`, runtime PID `15824`, connectivity `ok`
- `ollama ps`: `qwen3.5:9b` active
- OpenClaw Gateway Scheduled Task: present, `Ready`, last result `0`
- No matching CNX/OpenClaw/Ollama Supervisor task was found

### Ownership/classification

The pinned ownership script was run against the live workspace and the real `openclaw plugins list --json` output. Classification returned:

```json
{
  "mode": "upgrade",
  "pendingRollover": false,
  "pluginAlreadyExact": true,
  "interruptedRolloverReentry": true,
  "manifestPluginPath": "c:\\users\\cdq-p\\.openclaw\\npm\\projects\\openclaw-plugin-cogentnexus-openclaw__openclaw-generation__g-8e5adec878a7c4e3\\node_modules\\openclaw-plugin-cogentnexus-openclaw",
  "replacementPluginPath": "c:\\users\\cdq-p\\.openclaw\\extensions\\cogentnexus-openclaw",
  "legacy": []
}
```

The active replacement is the canonical direct extension. The manifest-owned retired path is absent. No additional product evidence or legacy namespace was reported. The live ownership manifest, skill, launcher, state root, install transaction, backup, and staging residue were preserved.

### Durable database

Read-only SQLite check on:

`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\runtime\cogentnexus-openclaw.sqlite3`

returned:

```text
PRAGMA integrity_check = ok
```

## Phase 1/2 — install-over result

Pre-mutation evidence was created before the attempt. The exact task command was attempted once from the hash-verified pinned artifact extraction:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

Observed result:

```text
Cannot validate argument on parameter 'Provider'. The argument "3D Objects" does not belong to the set "ollama" specified by the ValidateSet attribute. Supply an argument that is in the set and then try the command again.

ROOT_EXIT_CODE=1
```

This is a PowerShell parameter-binding failure before the installer body could execute. No second install-over attempt was made. Reset, uninstall, fresh reinstall, stop, start, restart, and recovery harness were not run.

## Post-failure read-only evidence

The post-failure snapshot `c01-post-failure-readonly.txt` confirms:

- CNX remains `passthrough`, generation `25`
- Gateway remains healthy and loopback-only
- OpenClaw remains exactly `2026.7.1-2`
- Ollama remains selected, healthy, and active
- SQLite integrity remains `ok`
- delivery outbox remains empty
- ownership manifest and product residue remain present
- no live cleanup or normalization was performed

## Failure boundary and next action

The failure is attributable to the installer invocation's provider argument resolution: the value `3D Objects` was supplied where the installer parameter requires the ValidateSet value `ollama`. This task does not authorize editing the live configuration, re-entering credentials, changing provider/model settings, or retrying the destructive phase.

A successor source/installer diagnosis task is required to determine why the exact command resolved the provider parameter to `3D Objects`. Any future lifecycle retry must be separately authorized and must begin with a fresh read-only preflight; this failed install-over must not be replayed in Task 116.

No Dashboard semantic nonce/message/Send occurred. No OpenClaw or Ollama update/reconfiguration occurred. No manual repair, cleanup, delete, rename, or normalization occurred.

Per the coordination contract, stop after publishing this `FAIL` report for independent review.
