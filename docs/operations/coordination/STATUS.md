# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Updated:** 2026-08-27 ICT
**Transport:** GitHub repository history
**Human authority:** operator authorized definitive repair through final live/semantic acceptance and approved heavy comprehensive source work while Hermes/Codex budget is available
**Execution trigger:** manual Hermes continuation; scheduled execution remains disabled

## Accepted semantic source lineage

Task 078/079/080 semantic and delivery hardening remains accepted candidate behavior.

Last accepted production candidate before the new installer-boundary repair:

`70d02e76233ca1084da445d488f88b628455f4aa`

Task 080 remains independently accepted as:

`ACCEPT_CRASH_SAFE_DELIVERY_FENCING_CLOSED`

Provider readiness remains:

`PROVIDER_READY_WITH_FRESH_OWNER_SESSION`

No further direct Ollama probe is authorized or required.

## Task 081 result

Task 081 attempted the required live install-over from exact candidate `70d02e76233ca1084da445d488f88b628455f4aa`.

Reported result:

`BLOCKED_SUPPORTED_INSTALL_OVER`

Report HEAD:

`ade320d2c32dde1143c2e8dc4ffbf8f3580e44a1`

Independent review:

Decision: `ACCEPT`

Disposition:

`ACCEPT_BLOCKER_SUPPORTED_INSTALL_OVER_NPM_PACK_PARSER`

Publication fence was report-only.

The installer was invoked exactly once and was not retried after nonzero exit.

## Task 081 failure boundary

The supported installer successfully reached PASSTHROUGH/native handoff, copied and validated the candidate skill, bootstrapped Ticket DB/package checks, then failed while resolving the result of:

`npm pack --json`

with:

`npm pack did not return exactly one package artifact`

The repository's existing `verify-package-contents.mjs` already documents and handles npm-shape compatibility that the installer parser does not: npm 11 array output versus npm >=12 single-entry object keyed by package name.

Task 081 did not preserve the exact raw pack stdout/npm version at the failing command, so the successor must reproduce that evidence before editing production rather than assuming the exact runtime shape.

## Current live partial state

The failed supported install-over left a bounded partial state that must not be manually normalized before source repair:

- Gateway healthy, dashboard HTTP `200`;
- Ollama healthy, accepted four models unchanged;
- SQLite integrity `ok`, zero Tickets/outbox;
- copied candidate skill tree matches accepted source where measured;
- ownership manifest still verifies;
- controller `passthrough`;
- startup policy disabled;
- Supervisor Scheduled Task absent;
- AGENTS managed block absent;
- previous canonical plugin generation remains registered but disabled;
- launcher remains present on previously owned runtime.

This is not MANAGED acceptance and no no-flash or Dashboard semantic readiness claim is made from this state.

## Active Task 082

[`tasks/CNX-20260827-082-repair-npm-pack-installer-boundary.md`](tasks/CNX-20260827-082-repair-npm-pack-installer-boundary.md)

Status: `READY_FOR_HERMES`

Authorization: `NPM_PACK_INSTALLER_BOUNDARY_REPAIR_AUTHORIZED`

Execution mode: `SOURCE_TDD_NPM_PACK_INSTALLER_BOUNDARY_REPAIR`

Task 082 is source/test-only and must:

- capture exact current Windows PowerShell/Node/npm toolchain and raw `npm pack --json` shape in isolation;
- RED-prove the production parser incompatibility;
- normalize accepted npm 11/npm 12 shapes through one deterministic artifact contract;
- reject malformed/multiple/unsafe artifact metadata fail-closed;
- exercise the production helper/parser through Windows PowerShell 5.1;
- prove the exact generated artifact is selected and exists;
- preserve installer lifecycle/transaction/upgrade ordering;
- rerun npm 11/npm 12 plugin tests+validation, full Python, installer/recovery and semantic/delivery regression gates;
- leave the live partial state untouched.

## Hard live fence

No live install/install-over/uninstall/reset/cleanup or manual restoration is authorized in Task 082. No controller/plugin/startup/Supervisor/AGENTS/config/ownership/runtime repair, no live Ticket/session/SQLite mutation, no Dashboard/WebChat semantic message, no CLI semantic run, no direct Ollama probe, no provider/model/timeout change, no reboot, merge, tag or release.

## Successor logic

If Task 082 is independently accepted, the next live task will perform exactly one supported normal install-over from the corrected source onto the current partial PASSTHROUGH installation, with no uninstall/reset/manual cleanup.

That live recovery must restore MANAGED/startup/Supervisor/AGENTS through installer-supported behavior, prove source/live parity, ownership/runtime/Gateway/Ollama/SQLite health, and observe at least five natural PT1M ticks with no-flash evidence.

Only after that live recovery is independently accepted may the final semantic task send exactly one fresh authenticated Dashboard/WebChat owner message and prove:

`owner message -> Ticket accepted before provider -> Ollama inference -> response_ready -> exact owner/run delivery -> delivery_confirmed -> completed -> visible response`.
