# Independent Review — CNX-20260904-237

## Verdict

`ACCEPT_FAIL_INSTALLER_TERMINAL__ROLLOVER_PREPARE_EXACT_INVARIANT_UNPROVEN__READ_ONLY_FORENSIC_SUCCESSOR_REQUIRED`

Task 237 correctly fixed Task 236's source-binding contract by materializing and proving a clean detached checkout at exact candidate `ffb0dd4ed47affe2e496c17b74ca74d358905bd7`, then invoking that checkout's `scripts/install.ps1` directly. The source plugin fingerprint was proven as `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`.

The live preflight was coherent and quiet: controller managed generation 38, Ollama/Gateway healthy, Delivery READY pending 0, Recovery READY, SQLite integrity OK, predecessor plugin fingerprint `e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`, and no active replay hazard.

The scheduler/tooling retry policy was followed. Registration attempt 1 failed before task creation due wrapper/parser mechanics; attempt 2 used a materially different file-based method and succeeded. The installer task then started exactly once, invoked the exact installer exactly once, and no installer execution retry occurred after `INSTALLER_RETRY_GATE=CLOSED`.

The installer terminated with exit code 1 / `LastTaskResult=1` during installer-owned `plugin-rollover-prepare`, after native handoff and earlier stages passed. The live result was preserved fail-closed in passthrough generation 39 with the predecessor plugin still installed, Gateway/Ollama healthy, Delivery READY pending 0, Recovery READY, SQLite OK, and zero semantic/direct operator sends. No manual lifecycle/plugin/database repair was attempted.

## Accepted failure classification

`FAIL_INSTALLER_TERMINAL` is accepted. This is no longer a coordination/source-binding blocker.

However, the report does not establish the exact failing invariant inside `rollover-prepare`. The installer captures the command output into `$prepareOutput`, but on nonzero exit throws only the generic message `ownership-safe plugin generation rollover pre-install proof failed`; the captured output is not persisted or emitted by that failure branch. Therefore the exact Python-side exception is not proven by the Task-237 report.

This distinction matters because `prepare_plugin_rollover_transaction()` can fail before backup creation, during copy, at `pre-install backup project-tree attestation mismatch`, or at another boundary. It may also leave a newly created external backup before the transaction JSON is persisted. A second installer invocation is not authorized until the retained Task-237 state is adjudicated.

## Independent source observations

The accepted candidate includes the Task-140 direct-extension ownership-boundary repair via `_retired_storage_root(...)`, so the historical Task-139 direct-path rejection must not be assumed to have recurred without exact evidence.

The accepted candidate also includes the Task-226 fail-closed prepare attestation sequence:

```text
copy retired storage -> hash retired source -> hash backup -> fail if hashes differ
```

A mismatch there would intentionally stop prepare before transaction persistence, potentially leaving a backup directory as forensic evidence. This is a hypothesis only until Task-237 artifacts are correlated.

## Required successor

Open one read-only Windows forensic task before any installer retry or manual managed-state restoration. It must:

1. preserve passthrough generation 39 and all Task-237/Task-223/Task-233 evidence;
2. inspect the Task-237 installer transcript/runner outputs for any Python stderr or hidden prepare diagnostics;
3. recover the Task-237 rollover id / backup token if present;
4. inventory `plugin-generation-rollover-backups` and `install-staging` with creation/modification times and hashes;
5. identify any Task-237-created backup and/or transaction artifact without modifying them;
6. compare any Task-237 backup tree/payload identity to the current retired direct plugin tree and identify exact differing paths/metadata where possible;
7. reconstruct which `rollover-prepare` invariant is the earliest one consistent with the retained evidence;
8. separately classify the installer's swallowed `$prepareOutput` as an observability defect and determine whether TDD repair is required before another live attempt.

No live `rollover-prepare`, installer, plugin lifecycle, Gateway/lifecycle repair, semantic Send, recovery replay, SQLite write, stale-evidence cleanup, reset/uninstall/reinstall, or Release/tag mutation is authorized in that successor.

## CI / repository state

The exact production candidate remains `ffb0dd4...`; compare from that candidate through the Task-237 report head contains coordination documentation only. Public `v0.9.3` remains immutable at `26ce64a624255278a3a0266ad38746e0e6ed2e31`.

At independent-review time, Task-237 report-head PS5.1 Acceptance Smoke and Windows Installer Pack Smoke were SUCCESS; Validate was still in progress and must not be represented as terminal GREEN until freshly observed.
