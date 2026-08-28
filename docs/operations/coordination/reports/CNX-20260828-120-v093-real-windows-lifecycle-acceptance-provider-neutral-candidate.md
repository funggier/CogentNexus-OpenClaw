# CNX-20260828-120 — v0.9.3 Real-Windows Lifecycle Acceptance — Provider-Neutral Candidate

## Verdict

**BLOCKED — fresh read-only ownership classification was not coherent; no destructive phase was started.**

This was a new Task-120 attempt, not a replay of Task 116. The hard fence stopped execution before install-over because ownership could not be proven from the fresh machine state.

## Exact candidate provenance

- Source SHA: `01d08cd7c82f542c821e3a60f7fffa036efb1d75`
- Package version: `0.9.3`
- Artifact ID: `9691451156`
- Artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-01d08cd7c82f542c821e3a60f7fffa036efb1d75`
- Artifact digest: `sha256:9db9290e14646575586a42160b79cfea691e35f3a0ca7d294f7f941dcae0c87a`
- ZIP SHA256: `8e06b186e425170a22bfce06fa3505a7cdac3b097d4bfdc4ccc4d810d502cac1`
- tar.gz SHA256: `6a14cb665ca6148ce2912970df62027533aef34fb0c871a2e542d1b149e94f31`
- Payload count: `178`
- Payload V2 fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`

`PACKAGE_IDENTITY.json`, `PAYLOAD_IDENTITY.json`, and `SHA256SUMS.txt` from the exact artifact agree with these values. No candidate substitution occurred.

## Fresh read-only evidence

Evidence root:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw-Acceptance-Evidence\CNX-20260828-120\20260828-154611`

Primary evidence:

- `a01-fresh-readonly-reconciliation.txt`
- `a02-phase1-blocked-summary.txt`

Observed read-only facts:

- Windows 10 Pro build `19045`
- PowerShell `5.1.19041.6456`
- OpenClaw `2026.7.1-2 (0790d9f)`
- CNX mode `passthrough`, generation `25`, desired provider `unchanged`
- Gateway healthy at loopback `127.0.0.1:18789`; scheduled task Ready; last task result `0`
- Ollama selected, installed, reachable, healthy, and ready; four models visible
- CNX system checks reported `SYSTEM READINESS: READY` and `No state was changed.`
- Plugin inventory diagnostics were empty
- Fresh read-only residue listing preserved existing backups, staging, transaction, and SQLite surfaces

## Phase 1 classification failure

The pinned read-only classifier did not return a coherent classification:

```text
RuntimeError: ownership manifest pluginPath does not match verified installed payload:
C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw
ROOT_EXIT_CODE=1
```

Because ownership proof and current installed payload attribution were ambiguous, the task required stopping before mutation. This report does not claim that the failure originated in the installer body; no installer body or lifecycle phase was executed.

## Phase execution ledger

| Phase | Result | Mutation count |
|---|---|---:|
| Exact provenance | PASS | 0 |
| Fresh read-only reconciliation/classification | BLOCKED | 0 |
| Install-over | NOT STARTED | 0 |
| Reset | NOT STARTED | 0 |
| Uninstall | NOT STARTED | 0 |
| Fresh reinstall | NOT STARTED | 0 |
| Stop/start/restart | NOT STARTED | 0 |
| Recovery harness | NOT STARTED | 0 |
| Final lifecycle snapshot | NOT APPLICABLE | 0 |
| Dashboard semantic Send | NOT PERFORMED | 0 |

No retry, manual cleanup, normalization, provider/runtime change, OpenClaw change, credential access, or Task-116 replay occurred.

## Required commands not executed

The authorized install-over command was not executed because Phase 1 failed closed:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

Reset, uninstall, reinstall, lifecycle controls, and the recovery harness were likewise not executed.

## Remaining work

A successor diagnosis/acceptance task must resolve the ownership-manifest versus installed-payload attribution mismatch using fresh, read-only evidence before authorizing any mutation. Any future lifecycle attempt must use a new explicit authorization and must not replay this blocked funnel blindly.
