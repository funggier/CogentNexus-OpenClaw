# CNX-365 — Path-bound controlled requalification preflight

## Preflight result

`PATH_BOUND_PREFLIGHT_PASS`

This report is limited to the authorized read-only path-bound preflight. It does not claim OpenAI PASS, CURRENT_RED, semantic requalification, or runtime repair.

## GitHub authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Exact HEAD at checkout and remote branch read: `4b2d00d49bca443ae8eeda3c6983d6db23d49741`
- Worktree: clean before report publication; report is the only intended publication change.
- Historical `generation`: observed as `103`; it was recorded only as evidence and was not a gate.

## Exact current canonical path identities

All paths below were read from the live Windows host without editing or normalizing runtime state.

| Identity | Exact path | SHA-256 | Size |
|---|---|---:|---:|
| Canonical state root | `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw` | directory identity bound by manifest and launcher | directory |
| Controller | `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\host\controller.json` | `8d8b8bd2629325fdff33acbfa47277ab9cfde8ed32417525513d5fb151a05187` | 251 bytes |
| Ownership manifest | `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\ownership.json` | `25b83fc79dc48e10ad2451b43377f50282c4d0e8d777f9981f759d15cdc8cd88` | 804 bytes |
| Launcher | `C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd` | `6f7962b2a431d346a22cb90397ed93cf289f732f4ba623234089149b12dcac16` | 273 bytes |
| Installed plugin manifest | `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\package.json` | `3c3738f51eb82fc3c90ce658c5cd8bde295a6593f44f619d59f3c93f808fedd9` | 1051 bytes |
| Installed plugin entry | `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js` | `da8e810e88547ef866e2279fde86195f02557a9ca0a35a8771a0e646a1f6a7ef` | 8734 bytes |

## Controller and state-root relationship

The ownership manifest explicitly binds:

- `workspace`: `c:\\users\\cdq-p\\.openclaw\\workspace`
- `stateRoot`: `c:\\users\\cdq-p\\.openclaw\\workspace\\.cogentnexus-openclaw`
- `pluginId`: `cogentnexus-openclaw`
- `pluginPath`: `c:\\users\\cdq-p\\.openclaw\\extensions\\cogentnexus-openclaw`
- `launcherPath`: `c:\\users\\cdq-p\\.openclaw\\workspace\\cnxclaw.cmd`
- `installedVersion`: `0.9.5`
- `migrationSource`: `null`

The launcher bytes explicitly invoke the owned interpreter and skill, and pass:

`--root "C:\\Users\\CDQ-P\\.openclaw\\workspace\\.cogentnexus-openclaw"`

The controller was read at the exact bound location within that root: `stateRoot\host\controller.json`. This proves the controller ↔ state-root relationship at test time by independent manifest and launcher bindings; no `generation=103` assumption was used.

Controller fields observed: `schemaVersion=2`, `cnxMode=active`, `desiredGateway=running`, `providerOwnership=openclaw`, `generation=103`, `updatedAt=2026-09-15T16:16:32.390846+00:00`.

## Installed plugin/candidate identity

`package.json` identifies package `openclaw-plugin-cogentnexus-openclaw`, version `0.9.5`, with the OpenClaw extension entry `./dist/v091-release-entry.js`. The installed entry exists at the exact path above and has the recorded SHA-256. The ownership manifest independently binds the same plugin ID, version, and plugin path.

## Runtime/process authority context

Read-only process enumeration captured the physical host authority at inspection time:

- OpenClaw Gateway process: PID `20244`; executable `C:\Program Files\nodejs\node.exe`; command line `"C:\Program Files\nodejs\node.exe" C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\dist\index.js gateway --port 18789`.
- The launcher-bound root is the canonical root above; the launcher also binds the owned runtime interpreter at `C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\runtime\python\Scripts\python.exe`.
- Hermes processes were separately visible, including gateway/serve processes under `C:\Users\CDQ-P\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe`; they are executor authority, not the OpenClaw plugin runtime.
- No runtime lifecycle action, installer, or process-control action was performed.

This establishes which physical canonical root and which OpenClaw Gateway process were inspected, while preserving the distinction between the OpenClaw runtime and Hermes executor processes.

## Hard-fence accounting

- Dashboard requests: **0**
- Model/OpenAI requests: **0**
- Runtime mutations: **0**
- Controller edits: **0**
- Provider/auth/routing/hooks/main changes: **0**
- Enable/disable/start/stop/restart/reinstall actions: **0**
- Historical CNX-360 through CNX-364 records modified: **0**
- Force-push/history rewrite: **0**

## Decision and next boundary

All required current path-bound identities were present, mutually consistent, and bound at test time. Preflight result is `PATH_BOUND_PREFLIGHT_PASS`.

STOP. No semantic execution is authorized by this report. The next authorization boundary is a later explicit task/operator authorization that names and permits the semantic requalification execution, including any Dashboard/model request. Until that authority exists, no Dashboard request, model request, or runtime mutation may occur.
