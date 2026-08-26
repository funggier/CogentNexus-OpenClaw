# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_TDD_NPM_PACK_INSTALLER_BOUNDARY_REPAIR`
Current authorization: `NPM_PACK_INSTALLER_BOUNDARY_REPAIR_AUTHORIZED`
Task ID: `CNX-20260827-082`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260827-082-repair-npm-pack-installer-boundary.md`](tasks/CNX-20260827-082-repair-npm-pack-installer-boundary.md)

## Task 081 accepted blocker

Task 081 report:

`docs/operations/coordination/reports/CNX-20260826-081-install-over-semantic-candidate-live-parity.md`

Report HEAD:

`ade320d2c32dde1143c2e8dc4ffbf8f3580e44a1`

Independent review:

Decision: `ACCEPT`

Disposition:

`ACCEPT_BLOCKER_SUPPORTED_INSTALL_OVER_NPM_PACK_PARSER`

Review path:

[`reviews/CNX-20260826-081-install-over-semantic-candidate-live-parity.md`](reviews/CNX-20260826-081-install-over-semantic-candidate-live-parity.md)

## Accepted source candidate lineage

Task 078/079/080 semantic/delivery repairs remain accepted candidate behavior.

Last accepted production candidate before the packaging repair:

`70d02e76233ca1084da445d488f88b628455f4aa`

Preserve:

- owner/session-bound delivery-marker fail-closed behavior;
- admission/routing idempotency;
- one timeout recovery authority;
- direct model-call lease ordering/fencing;
- direct semantic lifecycle convergence;
- workflow schedule/bind/settle atomicity;
- crash-safe complete-record lock publication;
- exact workflow/Ticket delivery-run fencing;
- CLI/subagent negative owner security;
- provider disposition `PROVIDER_READY_WITH_FRESH_OWNER_SESSION`.

The two Task-078 direct Ollama probes are consumed and must not be repeated.

## Current live partial state — do not repair in Task 082

Task 081 invoked exactly one supported install-over and it failed at the `npm pack --json` artifact parser. The installer was not retried.

Accepted post-failure state:

- Gateway remains healthy and dashboard HTTP remains `200`;
- Ollama remains healthy with the accepted four-model inventory;
- SQLite integrity remains `ok`, with zero Tickets and zero outbox rows;
- candidate skill tree copied before failure matches accepted source where measured;
- ownership manifest remains readable and verifies;
- controller is `passthrough`;
- startup policy is disabled;
- Supervisor Scheduled Task is absent;
- AGENTS managed block is absent;
- prior canonical plugin generation remains registered but disabled;
- launcher remains present and references the previously owned runtime.

This state is intentionally left untouched until the installer boundary is repaired and independently accepted.

## Task 082 objective

Repair the production `npm pack --json` artifact-resolution boundary under strict RED/GREEN TDD.

The repository's package verifier already recognizes npm 11 array output and npm >=12 single-entry keyed-object output, while `scripts/install.ps1` currently does not normalize those shapes equivalently.

Task 082 must:

1. capture exact Windows PowerShell/Node/npm versions and raw current-host `npm pack --json` output in an isolated worktree;
2. reproduce the current production parser failure against the exact output or accepted npm-12 keyed fixture;
3. add one deterministic normalization/artifact contract for npm 11 and npm 12;
4. reject zero/multiple/missing/unsafe artifact results fail-closed;
5. exercise the real production parser/helper path under Windows PowerShell 5.1;
6. prove actual generated `.tgz` artifact identity and existence without selecting stale arbitrary tarballs;
7. preserve installer transaction/mode/rollover ordering;
8. rerun npm 11/npm 12 plugin tests+validation, full Python, installer/recovery and Task-078/079/080 semantic/delivery regressions;
9. publish source/tests first and report separately.

## Hard live fence

Task 082 is source/test only.

No live install/install-over/uninstall/reset/cleanup, no manual controller/plugin/startup/Supervisor/AGENTS/ownership/runtime/config repair, no live SQLite/Ticket/session mutation, no Dashboard/WebChat semantic turn, no CLI semantic run, no direct Ollama probe, no model/provider/timeout change, no reboot, merge, tag or release.

## Successor gate

Only after Task 082 is independently accepted may a separate live recovery task perform one supported normal install-over from the exact corrected implementation onto the current Task-081 partial PASSTHROUGH installation.

That recovery task must restore MANAGED/startup/Supervisor/AGENTS through installer-supported behavior only, prove source/live parity and ownership/runtime/Gateway/Ollama/SQLite health, observe at least five natural PT1M no-flash ticks, and prepare the Dashboard/WebChat owner surface without sending a semantic prompt.

Final semantic acceptance remains a separate later task with exactly one fresh Dashboard/WebChat owner message.
