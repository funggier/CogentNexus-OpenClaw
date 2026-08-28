# CNX-20260828-121 — v0.9.3 Real-Windows Lifecycle Acceptance — Attested Re-entry

## Verdict

**FAIL — install-over returned exit 0, but the required post-install verification boundary failed due to an invalid non-interactive verification invocation; later disruptive phases were not executed.**

This task used the corrected production-equivalent attested classifier and was not a replay of Task 120.

## Exact candidate provenance

- Source SHA: `01d08cd7c82f542c821e3a60f7fffa036efb1d75`
- Package version: `0.9.3`
- Artifact ID: `9691451156`
- Artifact digest: `sha256:9db9290e14646575586a42160b79cfea691e35f3a0ca7d294f7f941dcae0c87a`
- ZIP SHA256: `8e06b186e425170a22bfce06fa3505a7cdac3b097d4bfdc4ccc4d810d502cac1`
- tar.gz SHA256: `6a14cb665ca6148ce2912970df62027533aef34fb0c871a2e542d1b149e94f31`
- Payload count: `178`
- Payload V2 fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`

The exact package identity and archive hashes were reverified before execution. The candidate plugin was extracted to an isolated boundary, prepared with `npm ci`, and validated with `npm run plugin:validate`; validation reported the mixed-plugin artifact and ticket DB bootstrap as PASS with `packedFileCount: 178`.

## Evidence root

`C:\Users\CDQ-P\AppData\Local\Temp\cnx121-attested-20260828\evidence`

Relevant evidence:

- `a03-candidate-plugin-fingerprint.json`
- `a04-openclaw-plugin-inventory.json`
- `a05-attested-classification.json`
- `b01-install-over-output.txt`
- `b02-post-install-readonly.txt`
- `b03-post-install-harness-block.txt`

Candidate fingerprint command returned the exact expected fingerprint:

```json
{
  "version": "0.9.3",
  "fingerprint": "3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4"
}
```

The corrected attested classifier returned:

```json
{
  "mode": "upgrade",
  "pendingRollover": false,
  "pluginAlreadyExact": true,
  "interruptedRolloverReentry": true,
  "expectedReplacementFingerprint": "3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4",
  "legacy": []
}
```

## Phase ledger

| Phase | Result | Attempts |
|---|---|---:|
| Exact artifact/source provenance | PASS | 1 |
| Candidate plugin preparation/attestation | PASS | 1 |
| Fresh inventory and attested classifier | PASS | 1 |
| Install-over | Exit 0 | 1 |
| Required post-install verification | **FAIL / BLOCKED** | 1 |
| Reset | NOT EXECUTED | 0 |
| Uninstall | NOT EXECUTED | 0 |
| Fresh reinstall | NOT EXECUTED | 0 |
| Stop/start/restart | NOT EXECUTED | 0 |
| Recovery harness | NOT EXECUTED | 0 |
| Final acceptance snapshot | NOT APPLICABLE | 0 |
| Dashboard semantic Send | NOT PERFORMED | 0 |

## Install-over result

The canonical provider-neutral command was executed exactly once from the verified candidate extraction:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

Observed result:

```text
CogentNexus-OpenClaw v0.9.3 installation completed successfully.
ROOT_EXIT_CODE=0
```

The installer performed its supported install-over operation, including backup/staging and runtime handoff. The output showed the existing passthrough state, the provider remained `ollama` as a runtime fact, and the runtime transition/reload returned exit code 0.

## First failure boundary

The required post-install verification harness was incorrectly constructed by the executor:

- it invoked `python` with a script path that was not resolved as an executable script in the live installed layout, causing Python to enter its interactive REPL;
- it invoked `openclaw` commands through a non-interactive PowerShell context where the CLI selected its TUI path and reported `OpenClaw TUI needs an interactive TTY`;
- an `ollama` command likewise opened an interactive UI and the bounded capture timed out.

This is recorded as an executor-side verification harness failure. It is not evidence that the installer body failed, and no unsupported manual repair was attempted. Because a required postcondition could not be verified, the task fail-stop rule prohibits proceeding to reset or any later destructive phase.

A subsequent read-only capture attempt also encountered the same stale interactive probe and timed out; it did not invoke a lifecycle command or perform a manual repair. No further retry was made.

## Safety and preservation

No provider/model/endpoint/timeout change, OpenClaw rebaseline, credential access, Dashboard semantic send, reboot, process-tree kill, manual cleanup, normalization, merge, tag, release, or force push occurred.

Task 120's failed classifier was not replayed. Each Task-121 disruptive phase after install-over ran zero times. Existing installer backups, staging, transaction, runtime, and evidence residue were preserved for review.

## Required successor work

A successor task must provide a verified non-interactive post-install read-only harness with explicit script paths and non-TUI OpenClaw probes before another lifecycle attempt is authorized. It must not replay reset, uninstall, reinstall, or lifecycle controls from this task merely to obtain missing evidence.
