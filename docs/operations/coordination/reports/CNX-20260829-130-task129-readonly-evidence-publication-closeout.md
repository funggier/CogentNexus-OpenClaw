# CNX-20260829-130 — Task-129 Read-Only Evidence Publication Closeout

## Verdict

**PASS — evidence closeout complete.** The retained evidence plus one narrowly scoped read-only metadata probe supports the Task-129 classification:

- `LAUNCHER_OR_ROOT_MISMATCH`
- paired with `SQLITE_PATH_OR_STATUS_PROBE_DEFECT` for the Task-128 preflight layer

No live runtime, provider, model, controller, ownership, database, task, service, installer, or user-data mutation occurred. No recovery/lifecycle action and no Dashboard semantic Send occurred.

## A. Coordination and provenance

Task-130 was confirmed authoritative by a fresh fetch before evidence work.

- Branch: `agent/v0.9.3-full-stabilization`
- Task-130 start HEAD: `b3a86cc95c9dce605ac3545b32ce2a1613543174`
- Prior Task-129 report commit: `e107e6408bbd7ad91e9d93f6c9b21349fd902597`
- Accepted candidate: `1b922bf400fdbccb1f9c7019b89b69fd67f44070`
- Exact recovery harness blob: `622f70b339fea0f2ef7c564253aa3c6bf90ffc97`
- Primary evidence root: `C:\Users\CDQ-P\AppData\Local\Temp\cnx129-authority-20260829T083000Z`
- Capture time retained in `b15-capture-time.txt`: `2026-08-29T09:12:12.5108077+07:00`

Retained evidence was preferred. The only new probe was `cli-metadata-probe.ps1`, run solely to correct the retained collector's directory-path bug for `cnxclaw.py` and `host_control_v092.py`; it performed only `Get-Item` and `Get-FileHash`.

Evidence inventory retained:

- `b01-launcher.txt`
- `b02-metadata.json`
- `b03-launcher-parsed.json`
- `b04-status.txt`
- `b05-provider-status.json`
- `b06-recovery.json`
- `b07-probe-exits.jsonl`
- `b09-competing-roots.txt`
- `b10-relevant-env.json`
- `b11-scheduled-tasks.json`
- `b12-cli-db-authority.json`
- `b13-sqlite-readonly.txt`
- `b14-cwd.txt`
- `b15-capture-time.txt`
- `b16-installed-cli-metadata.json` (narrow read-only closeout probe)

## B. Installed launcher authority

Path: `C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd`

Retained metadata (`b02-metadata.json`):

- exists: `true`
- size: `278` bytes (filesystem metadata; `b01-launcher.txt` is 283 bytes because it includes newline representation)
- creation: `2026-08-28T23:03:41.2766638Z`
- last write: `2026-08-28T23:03:41.2766638Z`
- SHA256: `f53df28f2a7ee7fc43c65ba2c48770ed9b7ed3e7b14d3c762f957bd017b90f10`

Complete launcher text from `b01-launcher.txt`:

```bat
@echo off
"C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\runtime\python\Scripts\python.exe" "C:\Users\CDQ-P\.openclaw\workspace\skills\cogentnexus-openclaw\scripts\cnxclaw_v093.py" --root "C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw" %*
exit /b %ERRORLEVEL%
```

Parsed launcher authority (`b03-launcher-parsed.json`):

- Python: `C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\runtime\python\Scripts\python.exe`
- CLI: `C:\Users\CDQ-P\.openclaw\workspace\skills\cogentnexus-openclaw\scripts\cnxclaw_v093.py`
- explicit root: `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw`
- `%*` forwarding: `true`

`Get-Command cnxclaw.cmd -All` was not retained successfully; no PATH-resolution conclusion is made from that missing artifact. The explicit installed launcher path remains authoritative.

## C. Installed CLI identity

The installed file metadata is retained in `b16-installed-cli-metadata.json`. The probe was read-only.

| File | Exists | Bytes | SHA256 |
|---|---:|---:|---|
| `C:\Users\CDQ-P\.openclaw\workspace\skills\cogentnexus-openclaw\scripts\cnxclaw_v093.py` | true | 3718 | `9d9e71c9034b116d2fbfd04a9ee17a5e79c5470d338ef03e198f50117922ee0f` |
| `C:\Users\CDQ-P\.openclaw\workspace\skills\cogentnexus-openclaw\scripts\cnxclaw.py` | true | 16537 | `2c629ae5caee33a8328d5d448bd786bf12e839d23c5b440b8944ba297b2c96cc` |
| `C:\Users\CDQ-P\.openclaw\workspace\skills\cogentnexus-openclaw\scripts\host_control_v092.py` | true | 5594 | `6abde8644467d351b88949d29a4d22be3e5de8f891e11d756231820d9109ea16` |

`b12-cli-db-authority.json` independently retains the latter two hashes and the authoritative runtime root/database path. An exact candidate-file hash comparison for all three installed CLI files was not captured; no equality to the accepted source candidate is inferred.

## D. Authoritative state-root chain

Installed launcher root and controller root agree:

```text
C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw
```

Controller: `host\controller.json` (`b02-metadata.json` and direct read-only inspection):

- exists: `true`
- size: `433` bytes
- SHA256: `4cf382c85da8258ce800e2b183aef32869e42f5791e3d951be8b0426f9bf98d7`
- mode: `managed`
- selectedProvider: `ollama`
- desiredGateway: `running`
- desiredProvider: `running`
- generation: `21`
- updatedAt: `2026-08-28T23:32:29.765543+00:00`
- providerTransition: `null`
- providerSelection: `selectedAt=2026-08-28T23:32:29.765543+00:00`, `selectionSource=explicit`, `lastVerifiedAt=2026-08-28T23:32:29.765543+00:00`

Ownership metadata:

- `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\ownership.json`
- exists: `true`
- size: `804` bytes
- SHA256: `fed272829401591e29ab9b80d1198e77ef5313d4d56d5828eb3c9eb0fd157534`

The retained runtime JSON path was absent; no runtime JSON identity is asserted.

Authoritative database (`b12-cli-db-authority.json`, `b13-sqlite-readonly.txt`):

```text
C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\runtime\cogentnexus-openclaw.sqlite3
```

- exists: `true`
- read method: Python SQLite URI with `mode=ro`
- exact `PRAGMA integrity_check`: `ok`
- retained table count: `12`
- no write/migration/initialization was attempted

## E. Exact installed-launcher read-only commands

The retained `b07-probe-exits.jsonl` records these literal commands and exit codes, invoked through the explicit installed launcher path:

```text
C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd status
exitCode=0

C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd provider status --json
exitCode=0

C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd check recovery --json
exitCode=0
```

Results:

- status: authoritative `managed`, selected provider `ollama`
- provider status: coherent provider selection/status
- recovery: `READY`, `readOnly=true`, `stateChanged=false`, provider incident closed and circuit closed

These were read-only checks; no lifecycle command was run.

## F. Competing-root inventory

`b09-competing-roots.txt` is a bounded recursive inventory. It contains the live authoritative root:

```text
C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw
```

It also contains many historical/test fixture roots under `C:\Users\CDQ-P\AppData\Local\Temp\`, including `cnx-admission-*`, `cnx104-release-harness-*`, `cnx067-cli-smoke`, and `pytest-of-CDQ-P` fixture trees. No retained launcher/task/service evidence references those temporary roots. They are not installed authority.

The Task-128 wrong root was:

```text
C:\Users\CDQ-P\.openclaw\workspace
```

It is the workspace parent, not the explicit launcher/controller root. Its absence of the authoritative controller/database caused the false `passthrough`, null-provider, and missing-SQLite observations.

No second installed live root was found in the bounded inventory.

## G. Scheduled-task/service authority

Retained `b11-scheduled-tasks.json`:

### CogentNexus-OpenClaw-Supervisor

- state: `Ready`
- last run: `2026-08-29T09:11:11.0000000+07:00`
- last result: `0`
- executable: `C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\runtime\python\Scripts\pythonw.exe`
- arguments: `"C:\Users\CDQ-P\.openclaw\workspace\skills\cogentnexus-openclaw\scripts\host_control_v092.py" --root "C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw" supervisor tick --execute-safe`
- working directory: not configured/retained (`null`)

### OpenClaw Gateway

- state: `Ready`
- last run: `2026-08-29T06:24:24.0000000+07:00`
- last result: `0`
- executable: `C:\Users\CDQ-P\.openclaw\gateway.vbs`
- arguments: `null`
- working directory: not configured/retained (`null`)

The Supervisor task independently resolves to the same installed script and explicit authoritative state root. Gateway working-directory/argument detail is unproven beyond the retained action entry.

## H. Non-secret environment overrides

Retained `b10-relevant-env.json` records all relevant checked values as null:

- `OPENCLAW_CONFIG_PATH=null`
- `CNX_WORKSPACE=null`
- `COGENT_ROOT=null`
- `COGENTNEXUS_ROOT=null`

No credentials, tokens, API keys, passwords, or connection strings were accessed or published.

## I. Task-125 to current timeline

Current authoritative controller evidence is exact:

- mode: `managed`
- provider: `ollama`
- generation: `21`
- updatedAt: `2026-08-28T23:32:29.765543+00:00`

The retained Task-125 recovery output establishes the historical cleanup/final healthy state, but does not retain a controller generation/timestamp pair sufficient for an exact numerical generation comparison. Therefore:

- generation advanced/reset versus Task 125: **cannot be proven from retained evidence**;
- an exact durable post-Task-125 mutating transition actor: **not inferred**;
- current evidence shows coherent managed state, not authoritative drift;
- the Task-128 mismatch is explained by its wrong probe root.

The historical Task-125 provider-crash convergence failure remains a separate old-harness live-behavior result. This closeout does not reclassify it and does not claim Task-128 recovery acceptance.

## Execution ledger and hard fence

- recovery suite/crash scenario: `0`
- confirmation `y`: `0`
- lifecycle mutation: `0`
- install/install-over/reset/uninstall/reinstall: `0`
- provider/model/config change: `0`
- controller/runtime/ownership/database/log edit: `0`
- task/service run/change: `0`
- process kill/cleanup/normalization/reboot: `0`
- Dashboard semantic Send: **not performed**

Task-128 repaired-harness suite remains unlaunched: `0 / 1`.

## Final classification

The evidence supports:

```text
LAUNCHER_OR_ROOT_MISMATCH
SQLITE_PATH_OR_STATUS_PROBE_DEFECT
```

The second classification is limited to the Task-128 acceptance-probe layer: SQLite existed at the installed launcher’s authoritative root and passed read-only integrity; the missing-SQLite result came from deriving the path beneath the wrong root.

Task-130 is complete. Stop for independent ChatGPT review. Do not open recovery re-acceptance or Dashboard acceptance automatically.
