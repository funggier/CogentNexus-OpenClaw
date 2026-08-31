# CNX-20260826-075 — Supported Install-Over, Source/Live Parity and No-Flash Acceptance

Result: `PASS_INSTALL_OVER_SOURCE_LIVE_PARITY_NO_FLASH`

Executor: Hermes (after the operator's continuation signal)

## Heads

- Fetched coordination HEAD at execution start: `986bbd0` (`coord: publish CNX-20260826-075 install-over parity status`)
- Install-over source HEAD (exactly as required): `79b51ed06363f6e8862c491ee0a313ddb412c806`
- Source worktree clean (`git status --porcelain` empty); no source editing during Task 075
- Report HEAD: this commit (report-only publication fence)
- Evidence directory: `%LOCALAPPDATA%\Temp\cnx075-install-over-20260826-123255\`
  (a-phaseA-baseline.txt, b-install-over.txt, c-phaseCG-parity-health.txt,
  f-phaseF-ticks.txt)
- Toolchain: node v24.18.0 / npm 11.16.0 (PATH pinned to `C:\Program Files\nodejs`), Python 3.11.15, OpenClaw `2026.7.1-2`

## Phase A — live baseline re-proof (hard gate A PASSED)

Re-proved before mutation; all matched the accepted Task-072 MANAGED state:

| Check | Observed |
|---|---|
| Gateway | running Ready pid 17116, connectivity ok, v2026.7.1-2 |
| Ollama models | exactly `qwen3.5:9b`, `muse-glimmer:30b`, `qwen3.6:27b`, `qwen3.8:27b` |
| Scheduled Task | Ready/Hidden/PT1M, Execute = owned pythonw.exe + host_control_v092.py args, LastTaskResult=0 |
| Launcher | exact owned foreground interpreter + cnxclaw_v093.py CLI/root |
| Controller | mode `managed` |
| CNX plugin | exactly 1 × `0.9.3` enabled at canonical npm-projects root |
| Ownership verify | passed via owned runtime |
| AGENTS managed block | exactly 1 |
| SQLite integrity | ok |
| Installed skill hashes | recorded for post-over comparison |

No third-party topology change → proceed.

## Phase B — one supported install-over

Command: `scripts/install.ps1 -Workspace C:\Users\CDQ-P\.openclaw\workspace`, no flags. **Exit code 0**, log retained (`b-install-over.txt`, ~1670 lines).

Upgrade-mode semantics observed:

- line 4: `Existing CogentNexus-OpenClaw is managed; entering PASSTHROUGH/native boundary before upgrade mutation.` — supported native handoff before replacement;
- existing skill backed up into `.cogentnexus-openclaw\install-backups\cogentnexus-openclaw-20260826-193459`;
- recovery preflight completed successfully against coherent ownership (no fresh transaction begun — upgrade path);
- skill/plugin/runtime updated through supported surfaces; plugin generation rollover executed via ownership-safe plan/apply;
- MANAGED policy + lifecycle enable restored; `installation completed successfully`.

Disruptive-action ledger: exactly ONE install-over; no uninstall/reset/cleanup/repeat.

## Phase C — source/live parity

Full hash comparison of installed `skills\cogentnexus-openclaw` vs source `79b51ed`
(86 files compared, `__pycache__` excluded): **differences: []** — byte-for-byte parity.
`CLEAN_FRESH` semantics present in the live-installed `namespace_ownership.py`
(occurrence count = 1). Live preflight on owned installation correctly reports
`OWNERSHIP_PRESENT` (not CLEAN_FRESH) per task instruction.

## Phase D — ownership-safe plugin generation parity

- Exactly ONE active canonical `cogentnexus-openclaw@0.9.3` registration, enabled,
  root resolving to `.openclaw\npm\projects\openclaw-plugin-cogentnexus-openclaw\node_modules\openclaw-plugin-cogentnexus-openclaw`;
- prior generation retired only through the supported rollover backup boundary
  (`plugin-generation-rollover-backups\`);
- no duplicate load paths / registrations;
- unrelated plugins/config preserved;
- MANAGED config values intact: `ticketFirst/preInferenceAdmission/autoWorkflowCompletion/enforcedMode/autoResume = true`; dispatch/recovery/outbox/completion polls 60000ms; context-maintenance 30000ms.
- Controller generation recorded as actual value (not forced).

## Phase E — exact owned runtime authority after install-over

Runtime manifest verified: root `%LOCALAPPDATA%\CogentNexus-OpenClaw\runtime\python`;
foreground `...\Scripts\python.exe`; background `...\Scripts\pythonw.exe`; base interpreter uv CPython 3.11.15 (permitted venv-backed shape).

Launcher: exact owned foreground interpreter + installed v0.9.3 CLI/root; forbidden scan (hermes/codex/%TEMP%/venv) **match=False**.

Scheduled Task: Execute = exact owned background pythonw.exe; arguments target installed
`skills\cogentnexus-openclaw\scripts\host_control_v092.py --root <stateRoot> supervisor tick --execute-safe`;
Ready/Hidden/**PT1M**; forbidden scan **match=False**.

## Phase F — natural PT1M no-flash re-acceptance

Read-only scheduled-task-info polling over ~5 minutes. **5 distinct natural ticks**: 19:47:47, 19:48:48, 19:49:49, 19:50:50, 19:51:51 (PT1M exact). At every tick:

- `LastTaskResult=0`;
- zero CNX-causal conhost/console-python spawns;
- no cmd/PowerShell wrapper in the chain (task executes pythonw directly);
- Gateway stayed healthy and Ollama kept the same four-model inventory.

Flash classification: **`NO_FLASH_MULTI_TICK_PROVEN`** (5 natural ticks ≥ required 3).

## Phase G — final MANAGED non-semantic health

1. controller mode `managed` ✓ 2. desiredGateway/desiredProvider running ✓ 3. Supervisor Ready healthy ✓ 4. Gateway Ready + dashboard HTTP 200 ✓ 5. Ollama same four models ✓ 6. one canonical v0.9.3 plugin active ✓ 7. plugin config accepted values unchanged ✓ 8. ownership manifest exists; production verify passes through the owned foreground runtime ✓ 9. launcher/task bind only to owned runtime ✓ 10. AGENTS managed block exactly once ✓ 11. SQLite integrity ok, durable tables coherent ✓ 12. unrelated OpenClaw/plugin/config state preserved ✓ 13. installed source hashes match accepted `79b51ed` ✓

## Semantic smoke prohibition accounting

No real user message was sent through CogentNexus/OpenClaw for LLM inference;
no ticket/session data was created or reset by this task. Final Ticket→Ollama→delivery
acceptance remains reserved for Task 076.

## Disruptive-action ledger

Exactly one supported install-over plus its installer-natural lifecycle effects.
No uninstall, no cleanup, no repetition, no provider/model/OpenClaw version change,
no source edit, no reboot, no merge/tag/release.

## Publication fence

This report-only commit adds exactly one file:
`docs/operations/coordination/reports/CNX-20260826-075-install-over-source-live-parity-no-flash.md`.
