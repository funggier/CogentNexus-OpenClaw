# CNX-20260918-413 — Bootstrap Retirement, Repaired Install, and Live Attestation Report

## Final classification

`FAIL_INSTALLER_TERMINAL`

The one authorized old-runtime bootstrap lifecycle invocation succeeded and retired the exact stale `healthy-runtime` marker. The subsequent one authorized installer invocation terminated unsuccessfully at `ticket-db-bootstrap`. Per the task fence, the installer was not retried, no manual Gateway/lifecycle repair was performed, and the runtime-attestation RPC was not called.

## Fresh GitHub authority and exact source binding

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Fresh starting local/remote HEAD: `bbd02adab6e70da01a95283efe3b84cebc5b1d26`
- ACTIVE/STATUS/task authorization: `READY_FOR_HERMES`, task `CNX-20260918-413`
- Exact repaired candidate: `368073d67e75cc89b9b04b21b0ee002e76f7e82f`
- Candidate was proven an ancestor of the starting remote HEAD.
- Candidate-to-HEAD drift was limited to coordination task/report/review documentation.
- Detached candidate checkout: `C:\Users\CDQ-P\cnx413-candidate-20260918T070559Z`
- Candidate checkout HEAD: exact candidate SHA, detached and clean.
- Installer: `C:\Users\CDQ-P\cnx413-candidate-20260918T070559Z\scripts\install.ps1`
- Installer SHA-256: `6fc4dd5d570172ba2e45ef06df6889d84e427f52174fa6bbdc78baf13c012dce`

## Read-only bootstrap preflight

Before mutation:

- OpenClaw CLI/Gateway: `2026.7.1-2`
- Gateway: healthy/reachable, PID `3452`, port `18789`, Scheduled Task state `Ready`
- Controller: `cnxMode=active`, derived `mode=managed`, desired Gateway `running`, generation `105`
- Maintenance marker: active; `recoveryPolicy=healthy-runtime`; reason `CogentNexus-OpenClaw external supervisor confirmed an unresponsive Gateway`
- Recovery: `READY_WITH_WARNINGS` only because that exact marker was present
- Delivery: `READY`; pending outbox `0`
- Provider recovery incident: closed (`incidentOpen=false`)
- SQLite read-only integrity: `ok`
- Read-only Supervisor tick: `idle`, `durableWorkPending=false`, `heavyPath=false`, Gateway healthy
- Durable counts: tickets `23`, ticket events `864`, outbox `0`, assistant deliveries `14`, direct model calls `20`, direct recoveries `5`, inference attempts `3`, sessions `58`
- Ticket status counts: accepted `3`, cancelled `4`, completed `16`; supported Supervisor classification established no actionable durable work.
- Provider/model selection: `ollama/qwen3.8:27b`
- Installed old-runtime `runtime.py` SHA-256: `f65adfd0583675cb125ebfbf417921e0a2efbef31396b74afab88c30fb5653b3`

The required bootstrap hazard gate passed: Gateway healthy, exact stale marker policy/reason matched, outbox zero, no active provider incident, SQLite OK, and no actionable durable delivery/recovery work.

## One-time supported bootstrap retirement

Exact command shape, invoked once through the installed production runtime:

```text
C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\runtime\python\Scripts\python.exe C:\Users\CDQ-P\.openclaw\workspace\skills\cogentnexus-openclaw\scripts\runtime.py --root C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw lifecycle start
```

- Start UTC: `2026-09-18T07:08:52Z`
- End UTC: `2026-09-18T07:08:59Z`
- Exit code: `0`
- Invocation count: `1`
- Retry count: `0`
- `--provider`: absent
- Public `cnxclaw start`: not used
- Gateway was already healthy and remained on PID `3452`; the lifecycle result reported Gateway start skipped as already healthy.

Immediate post-bootstrap evidence:

- maintenance marker: absent
- recovery: `READY`
- delivery: `READY`
- pending outbox: `0`
- provider incident: not active
- SQLite integrity: `ok`
- durable table counts: unchanged
- provider/model selection: unchanged at `ollama/qwen3.8:27b`

## Exact installer attempt ledger

The exact detached candidate installer was invoked once with:

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\CDQ-P\AppData\Local\Temp\cnx413-evidence-20260918T070559Z\run-installer-once.ps1
```

The wrapper invoked exactly:

```text
C:\Users\CDQ-P\cnx413-candidate-20260918T070559Z\scripts\install.ps1 -Workspace C:\Users\CDQ-P\.openclaw\workspace
```

- Installer start UTC: `2026-09-18T07:10:15.0352574+00:00`
- Installer finish UTC: `2026-09-18T07:11:47.3597983+00:00`
- Exit code: `1`
- Installer invocation count: `1`
- Installer retry count: `0`
- Retained transcript SHA-256: `543e80b66fbd2dd83aa251a843f714bab37fe3e20fcc3e4e86ff31a83b04b0dc`

The installer completed the ownership-safe pre-install native handoff, moved the controller to passthrough/disabled generation `106`, restarted the Gateway through the installer-owned flow, backed up the existing skill, installed the candidate skill, and passed skill validation. It then emitted the `ticket-db-bootstrap` stage start and failed at `scripts/install.ps1:443` when direct `node bootstrap-ticket-db.mjs` stderr was promoted by Windows PowerShell 5.1 under `$ErrorActionPreference=Stop`:

```text
node : (node:12524) ExperimentalWarning: SQLite is an experimental feature and might change at any time
FullyQualifiedErrorId : NativeCommandError
```

The bootstrap child had printed a successful database result with pending outbox `0`, but the PowerShell native-stderr boundary terminated the installer before a successful terminal installer result. This is therefore an installer terminal failure, not a successful install.

## Read-only post-failure state

No manual repair followed the failed installer.

- Controller: `cnxMode=disabled`, derived `mode=passthrough`, desired Gateway `running`, generation `106`
- Gateway: healthy/reachable, new installer-owned PID `26416`, state `Ready`
- Recovery: `READY`
- Delivery: `READY`
- Pending outbox: `0`
- SQLite integrity: `ok`
- Durable counts: unchanged from preflight
- Provider/model selection: unchanged at `ollama/qwen3.8:27b`
- Plugin inventory: `cogentnexus-openclaw` version `0.9.5`, currently disabled
- Candidate `host_v091.py` SHA-256: `99906331ab7e406ea6c6b4b2f493902a904dff8a50e8d79272fcbaca8a698d23`
- Installed skill `host_v091.py` SHA-256: `99906331ab7e406ea6c6b4b2f493902a904dff8a50e8d79272fcbaca8a698d23`
- Installed active plugin release-entry remained the prior hash `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`; exact installed candidate identity and managed convergence were not established.

Because the installer failed terminally, Phase E acceptance was not reached. No manual Gateway restart, lifecycle start, enable, plugin copy, marker mutation, Ticket/outbox/recovery/SQLite mutation, or other live workaround was attempted.

## Attestation ledger

`openclaw gateway call cogentnexus.runtimeAttestation --params '{}' --json` was **not called** because the installer did not succeed and natural managed convergence was not established.

Attestation RPC count: `0`.

## Hard-fence accounting

| Action | Count |
|---|---:|
| Web Chat semantic requests | 0 |
| Ollama semantic/model requests | 0 |
| OpenAI semantic/model requests | 0 |
| Any provider/model semantic request | 0 |
| Provider/model selection mutation | 0 |
| Provider credential/auth mutation | 0 |
| Public `cnxclaw start` bootstrap calls | 0 |
| Installed-runtime bootstrap lifecycle starts | 1 |
| Bootstrap retries | 0 |
| Manual maintenance-marker mutations | 0 |
| Installer invocations | 1 |
| Installer retries | 0 |
| Manual Gateway/lifecycle repair after installer | 0 |
| Manual plugin copy/replace | 0 |
| Attestation RPC calls | 0 |
| Manual Ticket/outbox/recovery/SQLite mutation | 0 |
| Release/tag/main changes | 0 |
| Force pushes/history rewrites | 0 |
| CNX-414 creation/start | 0 |

## Final classification

`FAIL_INSTALLER_TERMINAL`

The one-shot installer budget is consumed. Production is left in the installer-owned partial state described above. Further repair or retry requires new reviewed authority.