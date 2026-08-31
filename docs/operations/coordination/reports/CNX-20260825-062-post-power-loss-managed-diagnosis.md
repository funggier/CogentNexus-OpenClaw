# CNX-20260825-062 — Post-Power-Loss MANAGED Diagnosis Report

Result: `DIAGNOSIS_COMPLETE_ROOT_CAUSE_BOUND`

Executor: Hermes (per manual operator continuation signal)
Execution HEAD: `7d2bf73bd1fe8b40f2dd1d42baa2b476cc55b7ef` (remote branch `agent/v0.9.3-recovery-reality-tests`, verified equal after clone)
Publication fence: this commit adds only `docs/operations/coordination/reports/CNX-20260825-062-post-power-loss-managed-diagnosis.md` relative to execution HEAD.
Evidence directory (retained): `%LOCALAPPDATA%\Temp\cnx062-post-power-loss-diagnosis-20260825T110614Z`

## Boot boundary proof (Phase D1)

- Observation time: 2026-08-25T11:06:47Z (18:06:47 +07, SE Asia Standard Time)
- `Win32_OperatingSystem.LastBootUpTime`: **2026-08-25T17:34:12+07:00 (10:34:12Z)**
- Uptime at observation: ~0.54 h
- Task 061 report/review commits and the Task 061 coordination updates (ACTIVE/STATUS updated 2026-08-25 10:07 ICT) predate the current boot; the power loss occurred before the 17:34:12+07 boot.

Conclusion: the current session is demonstrably the post-power-loss boot.

## Fresh post-boot live state (Phase D2)

All reads were direct/read-only; status commands used were observational only.

### Controller / startup policy

- `host/controller.json`: `mode=managed`, `desiredGateway=running`, `desiredProvider=running`, `selectedProvider=ollama`, `providerTransition=null`, `generation=12`, `updatedAt=2026-08-24T20:26:43Z` (pre-power-loss durable value — unchanged by the reboot).
- `runtime/startup-policy.json`: `policy=enabled`, `updatedAt=2026-08-24T20:25:35Z`.

### Scheduled Tasks

Task `\CogentNexus-OpenClaw-Supervisor` (post-power-loss):

- Exists, State=`Ready`, Enabled=`True`, Hidden=`True`
- Execute: `C:\Users\CDQ-P\AppData\Local\hermes\hermes-agent\venv\Scripts\pythonw.exe`
- Arguments: `"C:\Users\CDQ-P\.openclaw\workspace\skills\cogentnexus-openclaw\scripts\host_control_v092.py" --root "C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw" supervisor tick --execute-safe`
- **LastRunTime = 2026-08-25T18:07:07+07 (post-boot), LastTaskResult = 0**, NextRunTime 18:08:08+07 (PT1M repetition)

Task `\OpenClaw Gateway`:

- State=`Ready`; Execute `C:\Users\CDQ-P\.openclaw\gateway.vbs`; LastRunTime 2026-08-25 17:35:35+07 (**~1 minute after boot**), LastTaskResult=0

### Interpreter identity evidence (operator-requested items)

1. Current Scheduled Task Execute/Arguments: as quoted above (captured verbatim in evidence `d2-live-state.txt`).
2. Post-power-loss LastRunTime/LastTaskResult: `18:07:07+07` / `0` (successful autonomous run after boot).
3. `...\hermes-agent\venv\Scripts\pythonw.exe` **exists on disk** (verified `-f` test).
4. Sibling interpreter: venv `pyvenv.cfg` → `home = C:\Users\CDQ-P\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none`, CPython **3.11.15** (`uv = 0.11.32`, `include-system-site-packages=false`). The task therefore runs the Hermes-agent uv-managed Python 3.11.15 venv's windowless launcher.
5. Why `sys.executable` resolved to the Hermes venv: `scripts/startup.py::python_background()` returns `Path(sys.executable).with_name("pythonw.exe")`. The template substitution `{{PYTHON}}` is filled with whatever interpreter executed `startup.py ensure/enable` at registration time. Registration-time backup (`install-backups/20260824-200747-windows-task.xml`) and `startup-policy.updatedAt=2026-08-24T20:25:35Z` show the last registration happened during a session where the executing Python was the Hermes venv. This is **intended behavior of the installer design** ("hidden-background-logon", Hidden=True verified) but it creates an **environment coupling**: the OpenClaw supervisor depends on the Hermes install's venv path remaining valid. It is not an unintended leak of process environment into the task definition — the path is deliberately persisted — but it is an implicit cross-project dependency worth flagging for a successor decision. No action taken under Task 062.

### Runtime health

- Gateway: HTTP probe `http://127.0.0.1:18789/` → **200 OK** (OpenClaw Control page). `openclaw status` evidence inside supervisor health.json confirms Gateway pid/state Ready, loopback bind, CLI/Gateway version 2026.7.1-2.
- Ollama: HTTP 200 on `127.0.0.1:11434/api/tags`; model inventory: `qwen3.5:9b`, `muse-glimmer:30b`, `qwen3.6:27b`, `qwen3.8:27b`.
- Plugin capture (exactly one `openclaw plugins list --json`): `cogentnexus-openclaw` id present, `version=0.9.3`, `enabled=true`, `status=loaded`, root `C:\Users\CDQ-P\.openclaw\npm\projects\openclaw-plugin-cogentnexus-openclaw__openclaw-generation__g-bbc979095f8845a1\node_modules\openclaw-plugin-cogentnexus-openclaw`, entry `dist\v091-release-entry.js`. Bounded unrelated comparison shows bundled plugins in expected enabled/disabled mix (e.g. `ollama` enabled/loaded, `telegram` disabled).
- Ownership manifest: SHA-256 `0667004dc9d6483450a3c99dda6f34bb7f384f0261f43813763019e2c3ba0341`; `pluginPath` matches plugin rootDir above; `namespace_ownership.py verify --root ... --workspace ...` exit 0, manifest consistent.
- `resolve-plugin --version 0.9.3`: plugin resolves to the same installed project (CLI printed unrelated third-party `[plugins] codex` register warning noise; resolution itself succeeded).
- Retired OpenClaw npm project root (`npm/node_modules/openclaw-plugin-cogentnexus-openclaw`): absent ✅
- Registered managed policy `managed-policy.md` SHA-256: `14edead0180690c3d9565e864d2bdaaae60e32df9ef2c64ebd2a1238df5cd8b4`
- Workspace AGENTS.md: 8,941 bytes, SHA-256 `0305C0F4667E9279EA72B8B6E8E28CD84B8F58945536E1B189DAF077A1FA0921`, bare-LF line endings (0 CRLF, ends with newline), one managed block (`<!-- cogentnexus-openclaw:begin -->` … `end -->`, lines 133–151).
- SQLite (read-only URI): `PRAGMA integrity_check = ok`; bounded counts: tickets 0, ticket_events 0, ticket_outbox 0, experiences 0, cnx_sessions 0, cnx_direct_recovery 0, cnx_assistant_delivery 0, cnx_direct_model_call 0, cnx_synthetic_runs 0, cnx_context_maintenance 0.

## Installed operator chain reconstruction (Phase D3)

Byte-for-byte SHA-256 comparison installed vs fresh clone: **all 13 artifacts identical** (12 tracked files listed in the task + installed `cnxclaw.cmd`). No drift.

Installed launcher `cnxclaw.cmd` (SHA `8db1f256…`):

```
python "...\skills\cogentnexus-openclaw\scripts\cnxclaw_v093.py" --root "...\ .cogentnexus-openclaw" %*
```

Actual operator `cnxclaw enable` call graph:

1. `cnxclaw.cmd` → `scripts/cnxclaw_v093.py` (v0.9.3 Ollama-only facade; imports `cnxclaw` as legacy + `provider_v093`)
2. → `scripts/cnxclaw.py` (v0.9.2 facade): provider selection commit (`state["generation"] += 1`), route bookkeeping, `run_host()` which invokes `sys.executable host_control_v092.py` per Host verb (`start`, action, and a Gateway `restart` process boundary when route changed or action == enable)
3. → `scripts/host_control_v092.py` (delegates to `host_control_v091.py` → base `host_control.py` shim chain; `HOST` retarget to `host_stall_v091.py`)
4. → `scripts/host_stall_v091.py` / `scripts/host_v091.py` (v0.9.1 transactional compatibility layer; stages managed settings incl. `60000 ms` poll values)
5. Startup binding: `scripts/startup_v092.py` monkey-patches `startup.host_control_path` to `host_control_v092.py` and delegates to `startup.py`, confirming the current Scheduled Task action target is intentional.

## Generation accounting conclusion (Phase D4)

Generation increment sites on the real enable path: `cnxclaw.py patch_state()` (+1), `cnxclaw.py` provider-selection commit (+1), `host.py` Host transition (+1), plus lifecycle overlays (`lifecycle_v092.py` +1; recovery paths can add more). A layered operator enable legitimately advances generation by more than exactly one. Reported generation `12` (with `updatedAt` frozen at pre-power-loss 2026-08-24T20:26:43Z) is **expected from the layered transition** across Task 060/061-era lifecycle actions; it is not uniquely attributable per single increment from retained evidence, and no unexpected additional lifecycle actor is indicated. Exact final generation is confirmed **not an authoritative invariant**.

## Startup adapter conclusion (Phase D5)

Source proves `startup_v092.py` intentionally binds the adapter to `host_control_v092.py`; the live post-boot task action matches byte-for-byte. Supervisor ran autonomously post-boot (LastRunTime 18:07:07+07, result 0) and refreshed `runtime/health.json` + `supervisor-state.json` at 17:36:11+07 (~90 s after boot); all probes healthy, circuit breakers closed, zero consecutive failures. Autonomous reconciliation demonstrably occurred without any Hermes action.

## F1 — AGENTS byte drift: BOUND

Classification cause: **blank-line boundary handling in the removal algorithm**, not content/newline-style drift.

In-memory-only reproduction against the current AGENTS.md (8,941 bytes):

- Removing only the block text leaves 7,198 bytes, SHA `EC6E95E0…` — does NOT match baseline.
- Removing the block together with its surrounding blank lines (`\n*begin…end\n*` → `\n`) yields **7,196 bytes, SHA `C9A664B73200AE5D6B0DA0908DE3256CDB4DDA8BA6FE99F5E6C5115C3983604C` — exact accepted pre-enable baseline match**.
- Independent confirmation: retained backups `install-backups/AGENTS.pre-host-change-20260824T120921Z.md` and `…T202529Z.md` are each 7,196 bytes with SHA `C9A664B7…`.

Therefore Task 061's strip failed to reproduce the baseline solely because its removal left extra blank-line boundary bytes (2-byte delta). The original baseline bytes ARE reconstructible from evidence; no AGENTS write was performed.

## F2 — managed config persistence: BOUND

Classification: `CONFIG_READ_SURFACE_MISMATCH`.

Current individual bounded reads via `openclaw config get <key>` return "Config path not found" for all 15 keys (top-level config surface). However the raw `openclaw.json` read shows `plugins.entries.cogentnexus-openclaw` containing ALL staged managed values intact post-power-loss:

`ticketFirst=true, preInferenceAdmission=true, autoWorkflowCompletion=true, enforcedMode=true, autoResume=true, workspaceDir=C:\Users\CDQ-P\.openclaw\workspace, ticketDispatchLimit=1, ticketMaximumRunning=1, ticketMaximumAttempts=5, ticketRecoveryPollMs=60000, ticketDispatchPollMs=60000, ticketOutboxPollMs=60000, completionPollMs=60000, contextMaintenancePollMs=30000, hooks.allowConversationAccess=true`

The values were persisted by the transactional enable and survived the power loss. Task 061 observed them "empty" because it read the wrong surface (top-level keys instead of the plugin entry namespace). The `60000 ms` values also independently confirm the v0.9.1 compatibility layer staging described by the review. No key was set or unset.

## Power-loss continuity assessment (Phase D8)

- Survived durably: controller intent (managed/gen 12/desired running), startup policy enabled, plugin registration + full managed config entry, ownership manifest, AGENTS.md managed block, watchdog-compat snapshot, SQLite database (integrity ok).
- Recovered automatically: Gateway (via `OpenClaw Gateway` scheduled task ~1 min after boot), Ollama reachable, supervisor ticks resumed (PT1M, result 0) and reconciled health state, plugin reloaded (`status=loaded`).
- Unhealthy or ambiguous: none found. SQLite work tables are all zero-row, so no Ticket/session/recovery row requires later human-authorized action.
- No synthetic recovery work was created; no component was started/stopped by Hermes.

## Live mutation accounting

Hermes performed zero live mutations: no lifecycle command, no config write, no AGENTS write, no task create/run/end, no process start/stop, no SQLite write, no primary-workspace git mutation. The only writes anywhere were (a) the new isolated clone and evidence files under `%LOCALAPPDATA%\Temp\cnx062-post-power-loss-diagnosis-20260825T110614Z` and (b) this report commit.

## Uncertainty / unproven claims

- Per-increment attribution of generation 12 to specific historical commands is not uniquely provable from retained evidence (causally explained, not itemized).
- Which exact interpreter/session registered the Scheduled Task is inferred from the registration-time XML backup timestamp + `sys.executable` mechanics, not from a logged interpreter path at registration time.
- The `[plugins] codex` register warning during `resolve-plugin` is unrelated third-party plugin noise; not investigated further under this task's boundary.

## Result

`DIAGNOSIS_COMPLETE_ROOT_CAUSE_BOUND`
