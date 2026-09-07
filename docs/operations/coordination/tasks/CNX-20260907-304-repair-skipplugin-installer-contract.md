# CNX-20260907-304 — Repair Staging Installer SkipPlugin Contract

## Status

`READY_FOR_HERMES`

Parent: `CNX-20260907-303`  
Executor: `Hermes`  
Reviewer: `ChatGPT`

## Authority

Hermes may independently diagnose and repair the installer control-path defect found in Task303, choose the minimal implementation, add or revise tests, update documentation, and run repository/CI validation without micro-confirmation.

## Objective

Repair the supported staging installer contract so `-SkipPlugin` does not evaluate a null plugin fingerprint and correctly reports a valid non-plugin staging postcondition. Preserve plugin-enabled behavior and all existing rollback/identity guarantees.

## Requirements

- Start with TDD RED and finish GREEN.
- Cover `-SkipPlugin`, normal plugin path, null/absent fingerprint, failure/rollback, and idempotent rerun behavior.
- Keep the repair minimal and repository-scoped until tests pass.
- Report exact method, files, tests, workflow results, and any remaining live preconditions.
- After repository GREEN, stop before retrying the live installer or invoking `cnxclaw enable`; propose the exact next bounded task.

## Allowed autonomy

Hermes may modify installer code, tests, documentation, and CI contracts; may make bounded technical decisions needed to preserve compatibility; and may continue through related repository defects discovered by the tests when they are within this installer contract.

## Prohibited

No live installer retry, no `cnxclaw enable`, no plugin install/replace, no service/Scheduled Task mutation, no semantic send, no replay/redelivery/disposition, no manual Ticket/SQLite/session/transcript mutation, no protected-state mutation, no release promotion, and no force push.
