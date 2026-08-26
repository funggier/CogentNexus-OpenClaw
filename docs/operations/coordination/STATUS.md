# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Updated:** 2026-08-26 17:21 ICT
**Transport:** GitHub repository history
**Human authority:** operator authorized definitive repair through clean reinstall/live acceptance
**Execution trigger:** manual Hermes continuation; scheduled execution remains disabled

## Task 071 review

Task 071 result:

`PASS_UPGRADE_LEGACY_MODE_ISOLATION_PROVEN`

Production candidate HEAD:

`9df671670908241486afe2badf8a7f221410c6f8`

Test-only implementation HEAD:

`7a55980e662b50f2d2979eb77a3ac1f89da7912f`

Report HEAD:

`d1c8382690d1e06e60ef335e26ba19cdde9152df`

Independent review:

Decision `ACCEPT`

Disposition:

`ACCEPT_UPGRADE_LEGACY_MODE_ISOLATION_PROVEN`

Review commit:

`3943fb9988c44fecf407b5cb2375bc9adcaf5746`

### Accepted Task-071 evidence

- coherent upgrade fixture uses production `build_manifest`, `write_manifest`, `verify_manifest`, and `classify_install` and returns `upgrade` without creating a fresh marker;
- valid legacy fixture satisfies production `prove_legacy_ownership` with three identities and production `classify_install` returns `legacy` without a fresh marker;
- upgrade and legacy executable harnesses derive freshness from production classification and prove ordinary non-fresh failure propagation without fresh rollback/plugin inverse;
- fresh caught-failure rollback regression remains green;
- report records full pytest `347 passed, 2 skipped`, PowerShell syntax clean, npm 11/npm 12 install/validate/test gates passing, exact OpenClaw `2026.7.1-2`, plugin `0.9.3`, baseline consistency PASS;
- publication fence is test-only implementation followed by report-only publication.

## Accepted production source

The exact source for the live successor is:

`9df671670908241486afe2badf8a7f221410c6f8`

No Task-071 production change was required.

## Current live baseline

Task 066's supported uninstall already removed the old Hermes-bound supervisor/runtime installation. The machine was left in native OpenClaw operation with no CNX task/launcher/plugin registration and with exactly two unowned partial failed-install workspace roots predating the new transaction marker. Those roots have remained intentionally untouched through Tasks 067-071.

## Active Task 072

[`tasks/CNX-20260826-072-bounded-cleanup-fresh-install-owned-runtime-live-acceptance.md`](tasks/CNX-20260826-072-bounded-cleanup-fresh-install-owned-runtime-live-acceptance.md)

Status: `READY_FOR_HERMES`

Authorization: `BOUNDED_RESIDUE_CLEANUP_AND_FRESH_INSTALL_LIVE_ACCEPTANCE_AUTHORIZED`

Execution mode: `LIVE_BOUNDED_RESIDUE_CLEANUP_FRESH_INSTALL_OWNED_RUNTIME_NO_FLASH`

Task 072 must:

- re-prove the exact Task-066 live baseline and two residue roots before mutation;
- perform one-time deletion of exactly those two roots only;
- fresh-install exact accepted source `9df6716...` through the normal Windows installer;
- prove the new fresh transaction contract is used and completes coherently;
- prove durable launcher/Scheduled Task runtime authority is `%LOCALAPPDATA%\CogentNexus-OpenClaw\runtime\python\Scripts\python.exe/pythonw.exe`, with no Hermes/Codex/temp binding;
- observe at least three natural PT1M ticks and prove no causal conhost/console-python trampoline;
- finish MANAGED/OpenClaw/Ollama/plugin/config/ownership/AGENTS/SQLite health acceptance;
- perform no product semantic user-message/LLM smoke.

## Disruptive-action boundary

Task 072 is authorized for exactly:

- deletion once of each proven Task-066 residue root;
- one normal fresh install and its installer-required lifecycle effects.

Do not uninstall again, reboot, mutate HermesAgent, change providers/models, broaden cleanup, or repeat completed effects after interruption.

## Next gate

If Task 072 reports `PASS_FRESH_INSTALL_OWNED_RUNTIME_NO_FLASH_VERIFIED`, ChatGPT must independently review residue attribution/cleanup, exact source/install transaction, owned-runtime bindings, three-plus natural PT1M process chains, flash classification, final MANAGED health, unrelated-state preservation, semantic-smoke prohibition, and report-only publication fence.

Only after acceptance may Task 073 perform the separate semantic Ticket -> Ollama LLM -> result/delivery acceptance.
