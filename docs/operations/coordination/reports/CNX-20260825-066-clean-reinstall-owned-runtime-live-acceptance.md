# CNX-20260825-066 — Clean Reinstall Owned Runtime Live Acceptance

Result: `BLOCKED_FRESH_INSTALL_FAILURE`

Executor: Hermes (fresh resume session)
Report date: 2026-08-26 ICT
Coordination HEAD at execution start: `53348b2` (`coord: record Task 066 Hermes context interruption and resume gate`)
Install source pinned: `21686f70520c5e0263e8aea4d644d2c87324e872` (exact reviewed Task 065 implementation HEAD; tree clean; review commit `f45f3c2` verified ancestor)

## Resume determination

Fresh-session live inspection before any mutation:

- `CogentNexus-OpenClaw-Supervisor` Scheduled Task PRESENT, bound to `...\hermes-agent\venv\Scripts\pythonw.exe` (old Hermes-owned chain), LastResult 0, PT1M repeat.
- No prior `cnx066-clean-reinstall-*` evidence directory existed.
- No Task 066 report existed on the coordination branch.

Conclusion: the interrupted prior session stopped BEFORE any uninstall/install side effect. Task 066 restarted cleanly at Phase A; no disruptive effect was repeated.

## Phase A — preflight/preservation: DONE

Evidence directory: `%LOCALAPPDATA%\Temp\cnx066-clean-reinstall-20260825T162500Z\`

| Item | File | Result |
|---|---|---|
| timestamp | a01-timestamp.txt | 2026-08-25T16:25Z |
| controller status | a02-cnxclaw-status.json | managed, gen 12, provider ollama, gateway healthy |
| boot identity | a03-boot.txt | LastBoot 2026-08-25 17:34 ICT, Win10 Pro |
| Scheduled Task | a04-scheduled-task.txt | PT1M, Execute=Hermes venv pythonw.exe |
| Ollama models | a05-ollama-models.json | 4 models (qwen3.5:9b, muse-glimmer:30b, qwen3.6:27b, qwen3.8:27b) |
| OpenClaw version | a06-openclaw-version.txt | 2026.7.1-2 (0790d9f) |
| plugin inventory | a07-plugins.txt | codex, cogentnexus-openclaw, discord enabled (+bundled) |
| plugin config redacted | a08-plugin-config-redacted.json | CNX MANAGED values incl ticketFirst=true, hooks.allowConversationAccess=true |
| ownership manifest | a09-ownership.txt | verify PASS, installedVersion 0.9.3 |
| AGENTS managed block | a10-agents-managed.json | present exactly once; stripped baseline sha256 `c9a664b73200ae5d6b0da0908de3256cdb4dda8ba6fe99f5e6c5115c3983604c` |
| SQLite | a11-sqlite.txt | integrity ok; tickets 0, outbox 0, durable tables readable |
| tree/hashes | a12-product-root-hashes.txt, a12-skill-hashes.txt | 106 + 85 files hashed |
| unrelated config hash | a13-unrelated-config-hash.txt | plugins-only normalized `5a37d5c2...` (see Phase B) |

No unrelated user state found inside any deletion boundary → uninstall authorized to proceed.

## Phase B — supported clean uninstall: DONE, contract satisfied

Command: old launcher `cnxclaw_v093.py ... uninstall`, product confirmation supplied (`y`). Log: `b01-uninstall.log`.

Post-uninstall verification (`b02-post-uninstall-verification.txt`):

- Supervisor task ABSENT ✅
- `cnxclaw.cmd` ABSENT ✅
- `skills\cogentnexus-openclaw` ABSENT ✅
- `.cogentnexus-openclaw` root ABSENT ✅
- `%LOCALAPPDATA%\CogentNexus-OpenClaw` ABSENT ✅
- plugin config entry REMOVED ✅
- AGENTS managed block removed; stripped file sha256 == preflight baseline ✅
- Gateway healthy/native after restart ✅
- Ollama healthy, 4 models unchanged ✅
- unrelated plugins-only config hash unchanged (`5a37d5c277bbe7ce46d8ca6dab3923fc72fc4a84f290eddd3c7c38f488a97c1a`) ✅
- Residue noted (classified acceptable): empty npm project wrapper dirs under `.openclaw\npm\projects\openclaw-plugin-cogentnexus-openclaw__*` remain (npm-project scaffolding incl pack archives; the plugin payload/dist itself was removed by the supported uninstall).

## Phase C — fresh install: FAILED → BLOCKED

### Defect D1 — reviewed source lockfile out of sync

`scripts/install.ps1` runs `npm ci` in `plugins/cogentnexus-openclaw`. On node v22.23.2 / npm 12.0.2 (the shell-default toolchain):

```
npm error code EUSAGE
npm error Missing: @types/retry@0.12.0 from lock file
```

Root cause: `package-lock.json` pins nested `node_modules/openclaw/node_modules/@types/retry` at **0.12.5**, while `p-retry@4.6.2` declares an exact dependency `"@types/retry": "0.12.0"`. npm ci rejects the lock as out of sync. Reproduced deterministically (2 attempts). No source edit was made (mutation fence).

The previously successful install (log evidence `%LOCALAPPDATA%\npm-cache\_logs\2026-08-24T13_09_58_497Z-debug-0.log`) used **node v24.18.0 / npm 11.16.0** (`C:\Program Files\nodejs`), which accepts this lock.

### Executor contribution (recorded honestly)

The first install attempt did not pin PATH to `C:\Program Files\nodejs`, so it ran under the Hermes-bundled node22/npm12 and failed at `npm ci` AFTER the installer had already copied the skill into the workspace and written a passthrough `host/controller.json`. A second attempt with the correct PATH pinned then failed earlier, at `classify-install`.

### Defect D2 — no recovery path for a partial pre-manifest install (product defect)

Current live state after the failed first attempt:

- `.cogentnexus-openclaw\{host\controller.json (passthrough), host\managed-policy.md, install-staging}` present;
- `skills\cogentnexus-openclaw` present (copy of exact reviewed source);
- `ownership.json` ABSENT (installer creates it later than these artifacts).

Consequence — dead end by design:

- Installer `classify-install` sees `inventory.new` non-empty → mode=`upgrade` → `verify_manifest` fails on missing `ownership.json` → refuses mutation.
- Supported `cnxclaw ... uninstall` requires the same manifest → also refuses (`result: error, stateChanged: false`; log `b03-uninstall-partial-cleanup.log`).

No supported command can clear this partial state, and the Task 066 mutation fence forbids manual deletion/manual manifest repair, so per the task instruction ("If supported uninstall/install reveals a product defect, stop and report instead of masking it with manual cleanup") execution stops here.

## Current live condition (end of task)

- No Supervisor Scheduled Task registered.
- No `cnxclaw.cmd` launcher.
- Plugin unregistered; AGENTS.md at stripped baseline.
- OpenClaw Gateway native, healthy, port 18789; passthrough controller state on disk.
- Ollama healthy, model inventory unchanged.
- Unrelated plugins/config preserved.
- Net effect vs pre-task: the flash-producing Hermes-bound PT1M task is GONE (operator-visible flash should have stopped), but CogentNexus is NOT freshly installed — the machine is in a coherent uninstalled-plus-residue state that only a corrected successor task can complete.

## Required successor scope (for ChatGPT)

1. Authorize bounded cleanup of exactly the two partial-install residue roots created by the failed Task 066 install attempt (`workspace\.cogentnexus-openclaw`, `workspace\skills\cogentnexus-openclaw`) — or provide a supported recovery command in a fix commit.
2. Fix D1 in source (regenerate/sync `plugins/cogentnexus-openclaw/package-lock.json` for `@types/retry@0.12.x`, or pin installer-required node/npm).
3. Fix D2 ordering: create/verify `ownership.json` before any workspace-visible artifact copy, or add crash-recovery to install/uninstall.
4. Re-run Task 066 acceptance (Phases C-F: runtime binding, ≥3 natural tick no-flash proof, post-install MANAGED health).

## Evidence publication fence

- Repository source files changed: NONE.
- Files committed by this report push: ONLY `docs/operations/coordination/reports/CNX-20260825-066-clean-reinstall-owned-runtime-live-acceptance.md`.
- All operational evidence retained outside deletion boundaries at `%LOCALAPPDATA%\Temp\cnx066-clean-reinstall-20260825T162500Z\`.
