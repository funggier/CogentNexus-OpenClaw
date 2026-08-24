# Review — CNX-20260824-055 Fix Plugin Generation Rollover

Decision: `ACCEPT`

Disposition: `ACCEPT_PLUGIN_GENERATION_ROLLOVER_FIXED`

Reviewed report:

`docs/operations/coordination/reports/CNX-20260824-055-fix-plugin-generation-rollover.md`

Report commit:

`846a58189dea4d8c5ccb137da4bf4c1952eeaaa5`

Implementation HEAD:

`6ad87e6f3ae65327a14bab4b5144dda4416d3645`

Report result:

`PASS_PLUGIN_GENERATION_ROLLOVER_FIXED`

## Publication fence

The report commit is a direct child of the reviewed implementation HEAD and adds exactly the Task 055 report path. The remote report blob is byte-identical to the reviewed local report. No `ACTIVE.md`, `STATUS.md`, runtime, or live-installation mutation is included.

## Accepted findings

- The Task 054 product defect is an ownership-generation rollover defect, not a resolver defect.
- OpenClaw can create a new generation-specific managed npm project while retaining the prior manifest-owned project.
- The existing ambiguity rejection remains intact and continues to fail closed on two canonical payload roots.
- The new recovery primitive proves the exact two-root state, old manifest ownership, active replacement registration, wrapper/package/lock ownership, complete project-tree hashes, inventory identity, and PASSTHROUGH mode.
- Recovery is plan-first and requires the exact reviewed plan SHA-256 plus a freshly captured, byte-identical OpenClaw plugin inventory at apply time.
- Retirement uses a same-volume atomic move into the external `CogentNexus-OpenClaw/plugin-generation-rollover-backups` boundary; broad deletion and cross-filesystem moves are rejected.
- The manifest update is atomic, final ownership is verified, and project/manifest rollback is attempted automatically if final verification fails.
- Windows and POSIX installers use equivalent ordering and do not invoke rollover for fresh, legacy, linked, or `SkipPlugin` paths.
- The replacement PowerShell wrapper retains the process handle, proves numeric exit codes `0` and `7`, rejects null, and preserves difficult argument boundaries.

## Verification accepted

- Final local Python suite: `273 passed, 1 skipped, 4 subtests passed`.
- Focused hardening suite: `24 passed, 1 skipped`.
- Namespace isolation, baseline consistency, singleton validation, compile checks, shell syntax, workflow/runtime self-tests, and changed-path checks passed.
- Independent re-review returned READY with no remaining Critical or Important issue.
- Every GitHub Actions workflow associated with implementation HEAD `6ad87e6f3ae65327a14bab4b5144dda4416d3645` completed successfully, including the Windows PowerShell 5.1 wrapper/runtime coverage.

## Decision

Accept the repository fix and recovery primitive. Task 055 made zero live actions and intentionally left the Task 054 machine state unchanged.

The successor may generate and publish a recovery plan from the live two-root state. Applying that plan requires a separate durable checkpoint containing the exact plan SHA-256 and an additional operator authorization. No installer, uninstall, reset, broad cleanup, or ambiguity weakening is authorized by this review.
