# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK246_TASK245_ROLLOVER_PREPARE_TERMINAL_FORENSIC_EVIDENCE_PRESERVATION`
Current disposition: `TASK245_ACCEPTED_FAIL_INSTALLER_TERMINAL__EXACT_EXCEPTION_UNPROVEN__FORENSIC_REQUIRED_BEFORE_RETRY`
Task ID: `CNX-20260904-246`
Parent task: `CNX-20260904-245`
Harness/action-binding parents: `CNX-20260904-243`, `CNX-20260904-244`
Candidate-validation parent: `CNX-20260904-240`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-04 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / independent reviewer: ChatGPT

## Accepted Task-245 result

Independent review verdict:

`ACCEPT_FAIL_INSTALLER_TERMINAL__MANIFEST_BINDING_AND_ONE_SHOT_EXECUTION_PROVEN__ROLLOVER_PREPARE_EXACT_EXCEPTION_UNPROVEN__READ_ONLY_FORENSIC_REQUIRED_BEFORE_ANY_RETRY`

Reviewed Task-245 report HEAD:

`5984e3dfe3503bee37c218cb1f34eff16a071bef`

Task 245 proved the exact detached candidate was invoked once through a valid frozen manifest-bound runner. `ticket-db-bootstrap` and `plugin-npm-pack` completed, then `plugin-rollover-prepare` terminated with child exit `1`. No retry occurred.

Accepted execution boundary:

```text
installer registrations = 1
installer starts = 1
installer child invocations = 1
installer retries = 0
terminal stage = plugin-rollover-prepare
new Task-245 rollover transaction JSON = not observed
semantic actions = 0
```

The exact Python exception is not yet proven. No installer retry is authorized.

## Critical evidence rule

Task-245 raw runner evidence resides under `%LOCALAPPDATA%\Temp` and may disappear. Task 246 must preserve it byte-identically to a non-temp forensic archive before broad analysis, with source/destination SHA-256 proof.

## Active Task 246

Execute:

`docs/operations/coordination/tasks/CNX-20260904-246-task245-rollover-prepare-terminal-forensic-evidence-preservation.md`

Required flow:

```text
fresh GitHub authority
-> locate Task-245 temp evidence
-> hash + byte-identical preserve to non-temp forensic archive
-> extract full stderr/stdout/transcript/result/manifest evidence
-> inventory plugin-generation-rollover-backups
-> inventory workspace install-backups separately
-> inventory install-staging/transaction residue
-> correlate exact error to prepare_plugin_rollover_transaction invariant order
-> fresh read-only runtime safety checks
-> report
-> STOP for independent review
```

## Zero-effect budget

```text
installer invocations = 0
Scheduled Task registrations/starts = 0
rollover prepare/finalize = 0
plugin/runtime/Gateway/DB mutation = 0
Dashboard/Discord/API semantic sends = 0
recovery replay/resend = 0
production/source/test/workflow edits = 0
historical evidence cleanup = 0
```

Evidence-preservation copy to the designated non-temp forensic archive is the only authorized write outside coordination report publication.

## Stop boundary

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260904-246-task245-rollover-prepare-terminal-forensic-evidence-preservation.md`

Then stop for independent ChatGPT review. Do not open or execute an installer successor from Task 246.
