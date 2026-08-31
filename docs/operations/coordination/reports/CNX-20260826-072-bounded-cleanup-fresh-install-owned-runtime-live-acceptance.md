# CNX-20260826-072 — Bounded Cleanup, Fresh Install, Owned Runtime and No-Flash Live Acceptance

Result: `PASS_FRESH_INSTALL_OWNED_RUNTIME_NO_FLASH_VERIFIED`

Executor: Hermes (after the operator's continuation signal)

## Heads

- Fetched coordination HEAD at execution start: `37b5597` (`coord: publish CNX-20260826-072 live acceptance status`)
- Install source HEAD (exactly as required): `9df671670908241486afe2badf8a7f221410c6f8`
- Source worktree clean (`git status --porcelain` empty); no source editing during Task 072
- Report HEAD: this commit (report-only publication fence — no other files touched)
- Evidence directory: `%LOCALAPPDATA%\Temp\cnx072-live-accept-20260826-103719\`
  (a-phaseA-preflight.txt, b-phaseB-cleanup.txt, c-phaseC-install.txt,
  d-phaseD-runtime.txt, e-phaseE-ticks.txt, f-phaseF-health.txt)

## Toolchain used by the installer

node v24.18.0 / npm 11.16.0 (`C:\Program Files\nodejs`, pinned per Task-066 lesson), Python 3.11.15, OpenClaw CLI/Gateway `2026.7.1-2`. No npm downgrade was performed.

## Phase A — preflight re-proof (read-only; hard gate A PASSED)

All checks materially matched the accepted Task-066 state:

| Check | Observed |
|---|---|
| OpenClaw version | `2026.7.1-2` exactly |
| Gateway | running, Ready, loopback 18789, connectivity ok |
| Ollama + models | healthy v0.32.15; exactly `qwen3.5:9b`, `muse-glimmer:30b`, `qwen3.6:27b`, `qwen3.8:27b` |
| Supervisor task / launcher / CNX plugin registration | absent / absent / absent |
| AGENTS managed block | absent; file sha256 `c9a664b73200ae5d6b0da0908de3256cdb4dda8ba6fe99f5e6c5115c3983604c` (= accepted native baseline) |
| `%LOCALAPPDATA%\CogentNexus-OpenClaw` | absent |
| `ownership.json` | absent |
| Residue root 1 `<ws>\.cogentnexus-openclaw` | present: `host\controller.json` (passthrough, generation 1), `host\managed-policy.md`, `install-staging\` — full per-file SHA-256 tree recorded |
| Residue root 2 `<ws>\skills\cogentnexus-openclaw` | present: copied source tree (SKILL.md, assets/, references/, scripts/, templates/) — full SHA-256 tree recorded |
| Unrelated content in residue roots | none found |
| SQLite/native workspace state | readable before cleanup |

No valid ownership manifest, no active launcher/task/plugin, no third-party mutation → gate passed.

## Phase B — one-time bounded cleanup (action ledger)

Deleted exactly once each, nothing else:

1. `<workspace>\.cogentnexus-openclaw`
2. `<workspace>\skills\cogentnexus-openclaw`

Post-clean proof: both roots absent; `<ws>\skills` parent preserved; workspace preserved; `.openclaw` config/state preserved; `%LOCALAPPDATA%` intact. No reset/uninstall used; no markers fabricated.

## Phase C — normal fresh install (exactly once)

Command: `scripts/install.ps1 -Workspace C:\Users\CDQ-P\.openclaw\workspace` with NO skip/link flags. Exit code 0. Log retained at `c-phaseC-install.txt`.

Transaction evidence (new fresh-install path demonstrably in use):

- line 13: fail-closed recovery preflight correctly refused the unowned Task-066 residue (`no valid incomplete install transaction marker`) — proving the fixed installer does not silently adopt pre-marker residue;
- line 14: `Fresh-install transaction started` after classification, before first mutation;
- owned paths recorded (marker `createdPaths`: 4 entries);
- ownership created + exact verify passed, then line 99: `Fresh-install transaction committed; recovery marker retired`;
- final marker state on disk: `committed`; `ownership.json` installedVersion `0.9.3`.

Installer effects: skill installed to `<ws>\skills\cogentnexus-openclaw`, plugin installed from npm-pack then left disabled through the transactional MANAGED authority commit (generation 3 at commit time), Gateway restarted under Host authority.

## Phase D — exact owned runtime authority

Runtime manifest (`runtime\python\runtime-manifest.json`):

- runtimeRoot: `...\AppData\Local\CogentNexus-OpenClaw\runtime\python`
- foregroundInterpreter: `...\runtime\python\Scripts\python.exe` (exists)
- backgroundInterpreter: `...\runtime\python\Scripts\pythonw.exe` (exists)
- baseInterpreter: uv-managed system CPython `...\Roaming\uv\python\cpython-3.11-windows-x86_64-none\python.exe`, Python 3.11.15 — permitted venv-backed-by-verified-base shape

Launcher `<ws>\cnxclaw.cmd`: invokes the exact owned foreground interpreter with the installed v0.9.3 CLI (`cnxclaw_v093.py --root <stateRoot>`). Forbidden-binding scan (hermes/codex/%TEMP%/venv): **no match**.

Scheduled Task `CogentNexus-OpenClaw-Supervisor`: State Ready, **Hidden=true**, trigger repetition **PT1M**, Execute EXACTLY the owned background `pythonw.exe`, arguments target `skills\cogentnexus-openclaw\scripts\host_control_v092.py --root <stateRoot> supervisor tick --execute-safe`. Forbidden scan: **no match**. `LastTaskResult=0`.

Foreground CLI probe via the launcher succeeded (`mode: managed`, provider ollama).

## Phase E — natural PT1M no-flash acceptance

Read-only scheduled-task-info polling over ~5 minutes. **5 distinct natural ticks observed**: 17:52:52, 17:53:53, 17:54:54, 17:55:55, 17:56:56 (PT1M cadence exact). At every tick:

- `LastTaskResult=0`;
- no CNX-causal `conhost.exe` spawn;
- no console `python.exe` trampoline from Hermes/uv/agent venvs;
- no `cmd.exe`/PowerShell wrapper in the chain (task Execute is pythonw directly).

Flash classification: **`NO_FLASH_MULTI_TICK_PROVEN`** (process-chain evidence for 5 natural ticks > required 3). Gateway stayed running/Ready and Ollama kept the same four-model inventory across the window.

## Phase F — final non-semantic MANAGED health

1. controller mode `managed`, desiredGateway/Provider `running` ✓
2. startup/Supervisor enabled, task Ready ✓
3. Gateway native health: Runtime running pid 17116 Ready, Connectivity probe ok ✓
4. Dashboard HTTP 200 ✓
5. Ollama healthy, exactly the four accepted models unchanged ✓
6. Exactly ONE canonical plugin registration: `cogentnexus-openclaw@0.9.3`, enabled=true, rootDir under `.openclaw\npm\projects\openclaw-plugin-cogentnexus-openclaw\node_modules\...` ✓
7. Plugin config contains accepted MANAGED values: ticketFirst, preInferenceAdmission, autoWorkflowCompletion, enforcedMode, autoResume all true; polling intervals 60000ms (dispatch/recovery/outbox/completion) and 30000ms context-maintenance ✓
8. Ownership manifest exists; production `namespace_ownership.py verify --root ... --workspace ...` run via the OWNED foreground interpreter returned the exact verified manifest ✓
9. Launcher + Scheduled Task bind only to owned runtime paths (Phase D evidence re-checked post-window) ✓
10. AGENTS managed block present exactly ONCE (`cogentnexus-openclaw:begin` count = 1); stripping the block via host.py's marker semantics reproduces the accepted native baseline sha256 `c9a664b73200ae5d6b0da0908de3256cdb4dda8ba6fe99f5e6c5115c3983604c` exactly ✓
11. SQLite `integrity_check: ok`; tables include tickets/ticket_events/ticket_outbox/cnx_sessions (+ delivery/context/direct-call tables), all coherent at 0 rows (fresh install; semantic flow is Task 073's scope) ✓
12. Controller generation recorded as actual value: **6** (not forced to 12) ✓
13. Unrelated OpenClaw/plugin/config state from Phase A preserved ✓

## Semantic-smoke prohibition accounting

No real user message was sent through CogentNexus/OpenClaw for LLM inference; no Ollama model activity was induced by this task. Ticket→Ollama→response acceptance remains reserved for Task 073.

## Disruptive-action ledger accounting

Exactly the authorized bounded actions occurred: two one-time residue-root deletions (Phase B), one normal fresh install (Phase C), plus installer-natural lifecycle effects. Nothing was repeated.

## Publication fence

This report-only commit adds exactly one file:
`docs/operations/coordination/reports/CNX-20260826-072-bounded-cleanup-fresh-install-owned-runtime-live-acceptance.md`.
