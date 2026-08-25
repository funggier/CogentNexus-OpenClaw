# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Updated:** 2026-08-25 18:15 ICT
**Transport:** GitHub repository history
**Human authority:** Task 062 diagnosis accepted; operator authorized definitive owned-runtime/flash fix and clean reinstall successor
**Execution trigger:** manual Hermes continuation; scheduled execution remains disabled

## Task 062 accepted

Task `CNX-20260825-062` result:

`DIAGNOSIS_COMPLETE_ROOT_CAUSE_BOUND`

Report commit:

`13ee5ddb5d88a9deb657f325026611286b1b2e33`

Review decision:

`ACCEPT`

Review disposition:

`ACCEPT_DIAGNOSIS_ROOT_CAUSE_BOUND_WITH_MULTI_REBOOT_SCOPE_CORRECTION`

Review commit:

`28947721cb002304d638536c5c143e919116ad77`

Accepted conclusions:

- F1 is a verification-strip boundary issue, not live AGENTS corruption;
- F2 is `CONFIG_READ_SURFACE_MISMATCH`; full managed config persisted under the plugin entry and survived reboot;
- latest observed boot recovered Gateway/supervisor/plugin health automatically and SQLite remained intact/empty;
- multiple reboot boundaries occurred, so only latest-boot recovery is individually evidenced;
- installed Scheduled Task currently depends on the Hermes-agent venv `pythonw.exe` due registration-time interpreter persistence.

## Active Task 063

[`tasks/CNX-20260825-063-own-supervisor-runtime-and-eliminate-console-flash.md`](tasks/CNX-20260825-063-own-supervisor-runtime-and-eliminate-console-flash.md)

Status: `READY_FOR_HERMES`

Current authorization: `OWNED_RUNTIME_AND_FLASH_FIX_AUTHORIZED`

Execution mode: `SOURCE_FIX_WITH_READ_ONLY_FLASH_DIAGNOSIS`

## Task 063 objectives

Task 063 must solve both related Windows startup defects before any live reinstall:

1. **Runtime ownership:** durable launcher/supervisor execution must use a CogentNexus-owned runtime under the product application-data boundary, not Hermes/Codex/agent venv or ambient PATH Python.
2. **Visible flash:** bind the recurring visible window/console to an exact natural supervisor process-start path and ensure healthy periodic supervision is genuinely background/no-console.

The task uses strict TDD and source/tests only after a bounded read-only live process-start observation.

Required implementation properties include:

- product-owned Python runtime provisioning/manifest;
- generated `cnxclaw.cmd` using the exact owned foreground interpreter, not bare `python`;
- Windows Scheduled Task using product-owned `pythonw.exe` where available;
- no silent fallback to arbitrary registration-time venv;
- Windows supervisor child process creation uses no-console semantics where required;
- reset/uninstall/install-over ownership is updated so the runtime can be safely recreated/removed only within CogentNexus boundaries;
- startup v0.9.2 target remains `host_control_v092.py`.

## Live-state fence

No lifecycle mutation, install-over, uninstall/reinstall, Scheduled Task change/run/end, plugin/config/AGENTS/ownership/SQLite write, Gateway/Ollama/provider change, process kill, merge/tag/release publication, or primary workspace Git mutation is authorized in Task 063.

## Pre-authorized clean reinstall successor

The operator explicitly requested that the defect be fixed definitively and the current installation then be removed and installed fresh.

After ChatGPT accepts a Task 063 PASS, a separate successor may proceed without asking for another confirmation to:

- prepare/use the reviewed fixed release path;
- capture preservation evidence;
- run supported clean uninstall with the command's required confirmation;
- prove only CogentNexus-owned surfaces are removed;
- fresh-install the fixed release;
- prove launcher + supervisor are bound to the CogentNexus-owned runtime and not Hermes/agent state;
- observe multiple natural supervisor ticks with no visible-console child process;
- verify MANAGED/Gateway/Ollama/plugin/ownership/SQLite health.

The successor must still stop and report on any unexpected preservation or safety contradiction rather than deleting foreign state.

## Next gate

Hermes publishes only the matching Task 063 implementation report. ChatGPT reviews source diff, RED/GREEN/full tests, flash trace, ownership semantics, and publication fence before any live reinstall begins.
