# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK249_TASK248_RETIRED_PROJECT_TRANSIENT_MUTATION_FORENSIC`  
**Updated:** 2026-09-04 ICT  
**Transport:** GitHub repository / Actions authoritative; Task 249 is read-only forensic of the Task-248 retired-project tree mismatch; installer and semantic retries are unauthorized  
**Active task:** `CNX-20260904-249`  
**Parent:** `CNX-20260904-248`  
**Parent umbrella:** `CNX-20260831-188`  
**Disposition:** `TASK248_ACCEPTED_FAIL__EXACT_ATTESTATION_MISMATCH_PROVEN__MUTATION_ACTOR_UNPROVEN__READ_ONLY_FORENSIC_REQUIRED`

## Accepted Task-248 result

Reviewed report HEAD:

`06b7bc01161efe2c8bbb97fe0e0511d79ff8d62b`

Independent review verdict:

`ACCEPT_FAIL_INSTALLER_TERMINAL__TASK247_DIAGNOSTIC_REPAIR_PROVEN__TASK226_FAIL_CLOSED_ATTESTATION_TRIGGERED__TRANSIENT_RETIRED_TREE_MUTATION_ACTOR_UNPROVEN__READ_ONLY_MUTATION_FORENSIC_REQUIRED`

Task 248 proved:

```text
exact candidate = 6c11a5e8f417300835e85441b88e0f37e3897353
installer registration/start/invocation = 1/1/1
retry after start = 0
terminal stage = plugin-rollover-prepare
exact exception = RuntimeError: pre-install backup project-tree attestation mismatch
candidate installed = no
live plugin = disabled predecessor e3bcce04...
controller = passthrough generation 39
semantic sends = 0
```

Task-247 native stderr preservation worked and retained the complete relevant traceback. The failed full-tree attestation is intentional Task-226 fail-closed behavior and must not be weakened.

Post-failure Task-248 external rollover backup and current retired project both later hashed to:

`900ac13f85a6de75e40a632a534f2b0ceef53def1e8387fc3530c02a7413de58`

This post-failure equality does not identify the historical changed path or actor. `_project_tree_sha256()` does not hash mtime, so mtime-only drift is not an explanation for the mismatch.

Task-248 report-head Actions are GREEN:

```text
PS5.1 Acceptance Smoke        33891454875 = SUCCESS
Windows Installer Pack Smoke 33891454855 = SUCCESS
Validate                      33891454905 = SUCCESS
```

## Active Task 249

Execute:

`docs/operations/coordination/tasks/CNX-20260904-249-task248-retired-project-transient-mutation-forensic.md`

Task 249 must use read-only evidence to identify the transient changed path and, if possible, the process/actor. It may inspect bounded NTFS/USN evidence, Windows logs, OpenClaw/npm logs, retained Task-248 evidence, current per-path hashes/metadata, and may perform a bounded passive read-only hash observation if historical evidence is insufficient.

It must not call the installer or rollover prepare/finalize, modify the retired tree or Task-248 backup, or weaken the fail-closed attestation.

## Hard fences

```text
scripts/install.ps1 = 0
installer task registration/start = 0
prepare_plugin_rollover_transaction = 0
rollover prepare/finalize = 0
retired-project writes = 0
Task248 rollover-backup writes/deletes/renames = 0
plugin/controller/Gateway/provider/model/DB mutation = 0
Dashboard/Discord/API semantic sends = 0
recovery replay/resend = 0
process termination = 0
production/source/test/workflow edits = 0
release/tag/history mutation = 0
```

If the actor cannot be proven from retained/read-only evidence, Task 249 should end blocked and recommend a separate repository-only TDD mismatch-instrumentation successor. Do not implement instrumentation in Task 249.

## Stop boundary

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260904-249-task248-retired-project-transient-mutation-forensic.md`

Then stop for independent ChatGPT review. Installer retry and semantic acceptance remain unauthorized.
