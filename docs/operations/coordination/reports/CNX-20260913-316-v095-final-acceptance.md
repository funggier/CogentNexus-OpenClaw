# CNX-20260913-316 — v0.9.5 Final Acceptance Evidence

## Result

```text
Automated Validation      PASS on repaired candidate
Provider Switch           INDETERMINATE
Idle Quiescence           INDETERMINATE
Controlled Wake           INDETERMINATE
Finalization              BLOCKED
Merge                     None
Tag                       None
Release                   Not published
```

## Candidate history

The original frozen candidate was:

```text
a986f3261b1570d1bcb1574d2458fe7068207a9c
```

A real installer defect was reproduced during the authorized exact-candidate install. The installer selected the legacy `cnxclaw_v093.py` facade. That facade appended `--provider ollama` to `enable`; the v0.9.5 canonical CLI rejected the legacy option before any route/lifecycle transition.

Root cause was identified in:

```text
scripts/install.ps1
scripts/install.sh
skills/cogentnexus-openclaw/scripts/cnxclaw_v093.py
skills/cogentnexus-openclaw/scripts/cnxclaw.py
```

A test-first repair was made:

```text
b2c7b0bb  test: cover v0.9.5 installer CLI boundary   # RED test commit
c1401f56  fix: use provider-neutral CLI during v0.9.5 install
434b2718  test: update installer wiring for v0.9.5 CLI
```

The repaired candidate is:

```text
434b27185f7afd17d8cffeede9c016378df0a6aa
```

It is on branch:

```text
fix/v0.9.5-final-acceptance-installer-cli
```

The original candidate branch and PR #38 were not modified.

## Requalification of repaired candidate

```text
Python pytest:       668 passed, 5 skipped, 38 subtests passed
npm test:            337 passed across 75 test files
plugin:validate:     PASS
```

The repaired candidate was pushed and independently verified at the exact SHA above.

## Exact install evidence

Environment:

```text
OS: Windows 10.0.19045 x64
PowerShell: Windows PowerShell 5.1.19041.6456
OpenClaw: 2026.7.1-2
Candidate installed version: 0.9.5
```

First install attempt against `a986f3261b1570d1bcb1574d2458fe7068207a9c`:

```text
Result: FAIL
Failure: Host enable rejected injected --provider ollama
Transcript: %LOCALAPPDATA%/Temp/cnx316-20260912T194927Z/install-transcript.log
Result: %LOCALAPPDATA%/Temp/cnx316-20260912T194927Z/install-result.json
Transcript SHA-256: c2fcb4ee5ec9d92beef19f44b70e5a4de2f8bad9c33a34d7faa5a5c3a77d5fa5
Result SHA-256: 000b832dd13aff478a23862ec8b6664564d03feb52c7d56d010bb837c526c759
```

Repair-candidate install attempt against `434b27185f7afd17d8cffeede9c016378df0a6aa`:

```text
Result: FAIL
Failure: transactional enable failed because OpenClaw gateway restart timed out
Installer exit code: 1
Rollback: native passthrough rollback executed
Transcript: %LOCALAPPDATA%/Temp/cnx316-20260912T194927Z/repair-install-transcript.log
Result: %LOCALAPPDATA%/Temp/cnx316-20260912T194927Z/repair-install-result.json
Transcript SHA-256: e780c9eb2cf3d3a16e9ee758469805bd614396ce376c09c63688c6c9f484b9c6
Result SHA-256: 2cf55b6524fb39b3790d3f38b48aec9151af80b200924aafe699d66f7b9527f
```

The installer reported:

```text
Command ... openclaw.CMD gateway restart timed out after 60 seconds
priorMode=passthrough
currentMode=passthrough
authorityCommitted=True
host-state-rollback mode=passthrough generation=94
```

## Post-state

Read-only postflight observed:

```text
installedVersion: 0.9.5
cnxMode: disabled
providerOwnership: openclaw
generation: 94
plugin: disabled
Gateway process: running and owns port 18789
Gateway connectivity probe: failed / timeout
```

The failed gateway probe and disabled plugin mean the acceptance preconditions are not satisfied. No provider-switch, idle-quiescence, or controlled-wake evidence was collected. Those gates remain `INDETERMINATE`, not PASS.

## Release state

```text
Repository: funggier/CogentNexus-OpenClaw
PR: #38 — open, still points to a986f3261b1570d1bcb1574d2458fe7068207a9c
Merge SHA: None
Tag v0.9.5: None
GitHub Release: Not published
```

This task stops here under the authority hard fence. No merge, tag, release, or retry was performed.

## Remaining blockers

1. The repaired candidate `434b27185f7afd17d8cffeede9c016378df0a6aa` is not the head of PR #38.
2. The acceptance machine's OpenClaw gateway restart/probe is timing out; the runtime is left in safe native passthrough with CNX disabled.
3. Provider Switch Acceptance is unproven.
4. Idle Quiescence Acceptance is unproven.
5. Controlled Actionable Wake Acceptance is unproven.
6. A successor authority is required before any retry, PR update, or further live mutation.
