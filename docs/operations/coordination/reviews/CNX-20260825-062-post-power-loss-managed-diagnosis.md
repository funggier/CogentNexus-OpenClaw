# CNX-20260825-062 — Review

Decision: `ACCEPT`

Disposition: `ACCEPT_DIAGNOSIS_ROOT_CAUSE_BOUND_WITH_MULTI_REBOOT_SCOPE_CORRECTION`

Reviewed report commit:

`13ee5ddb5d88a9deb657f325026611286b1b2e33`

Accepted result:

`DIAGNOSIS_COMPLETE_ROOT_CAUSE_BOUND`

## Publication fence verification

Independent GitHub comparison from fetched execution HEAD

`7d2bf73bd1fe8b40f2dd1d42baa2b476cc55b7ef`

to the report commit/current branch before this review found exactly one descendant commit and exactly one changed path:

`docs/operations/coordination/reports/CNX-20260825-062-post-power-loss-managed-diagnosis.md`

No source, runtime, installer, ownership, plugin, or other coordination file was changed by the Task 062 executor publication.

## Accepted diagnostic findings

Task 062 satisfies its diagnosis-only boundary and binds the Task 061 blockers without performing live repair:

- controller intent, startup policy, plugin registration/config, ownership, managed AGENTS block, watchdog snapshot, and SQLite survived the observed reboot sequence;
- on the latest observed boot, the bundled OpenClaw Gateway task ran automatically and Gateway became healthy;
- on the latest observed boot, `CogentNexus-OpenClaw-Supervisor` ran autonomously with `LastTaskResult=0` and continued periodic supervision;
- Ollama was reachable with the same four model identities;
- the canonical v0.9.3 plugin was enabled/loaded at the accepted replacement generation;
- ownership manifest remained the accepted SHA-256 `0667004DC9D6483450A3C99DDA6F34BB7F384F0261F43813763019E2C3BA0341` and namespace verification/resolution passed;
- SQLite integrity remained `ok` and all bounded Ticket/session/recovery/work tables were zero-row;
- installed operator-chain artifacts were byte-identical to the fresh clone and the launcher was proven to enter `cnxclaw_v093.py`;
- Task 061's exact `generation=8`, direct base `host_control.py` startup-target, and `5000 ms` interval expectations were not valid invariants for the real layered v0.9.3/v0.9.2/v0.9.1 operator path;
- F1 is bound to the Task 061 verification strip procedure leaving two blank-line boundary bytes. Removing the managed block using the repository-defined boundary semantics reproduces the exact accepted baseline SHA-256 `C9A664B73200AE5D6B0DA0908DE3256CDB4DDA8BA6FE99F5E6C5115C3983604C`; retained pre-host-change backups independently match that baseline;
- F2 is bound to `CONFIG_READ_SURFACE_MISMATCH`. The managed plugin values are present under `plugins.entries.cogentnexus-openclaw`, survived reboot, and contain the v0.9.1 compatibility values including `60000 ms` ticket recovery/dispatch/outbox intervals;
- Hermes performed zero product/live mutations during diagnosis.

## Multi-reboot scope correction

After Task 062 publication, the operator clarified that the machine was powered off/on two additional times after the initial unexpected power loss.

Therefore the report's phrase "the post-power-loss boot" must be read as **the latest observed boot boundary**, whose `LastBootUpTime` was `2026-08-25T17:34:12+07:00`.

The evidence proves that the accepted durable state persisted through the reboot sequence and that automatic Gateway/supervisor/plugin recovery was healthy on the latest observed boot. It does **not** provide enough retained per-boot evidence to reconstruct or separately certify the autonomous behavior of each earlier boot in the sequence.

This limitation is non-material to F1/F2 root-cause binding and does not invalidate the latest-boot recovery observation.

## Startup interpreter defect candidate

Task 062 also bound a separate architectural issue that is not a Task 061 acceptance mistake.

The live Scheduled Task executes:

`C:\Users\CDQ-P\AppData\Local\hermes\hermes-agent\venv\Scripts\pythonw.exe`

and passes the installed `host_control_v092.py` supervisor action.

The report traces this to `startup.py::python_background()`, which derives the persistent Scheduled Task executable from the registration process's `sys.executable`, replacing the filename with `pythonw.exe` when available. Because Task 061 `enable` was executed from the Hermes environment, the CogentNexus startup adapter became durably coupled to the Hermes-agent venv.

The observed task currently succeeds because that venv still exists, so Task 062 does not prove a present runtime failure. However, the dependency is product-external and executor-specific: removing, recreating, or relocating Hermes can break CogentNexus boot supervision even though CogentNexus itself is otherwise intact.

This must be treated as a source-level startup ownership defect candidate before release acceptance. A successor task should create a regression test that reproduces registration from an arbitrary venv, then change startup interpreter selection so the persisted supervisor action uses a stable non-executor-specific Python runtime while preserving hidden/background Windows behavior and existing cross-platform startup semantics.

## Safety disposition

No live repair is accepted or required for F1/F2. Do not rewrite AGENTS or plugin managed configuration for those findings.

The next task should address only the startup-interpreter ownership defect in source/tests first. It must not mutate the live Scheduled Task, reinstall, reset, uninstall, change ownership, or broaden into end-to-end message/release work until the source fix is reviewed.
