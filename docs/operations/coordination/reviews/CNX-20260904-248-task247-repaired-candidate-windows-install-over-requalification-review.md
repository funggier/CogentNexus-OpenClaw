# CNX-20260904-248 — Independent Review

## Verdict

`ACCEPT_FAIL_INSTALLER_TERMINAL__TASK247_DIAGNOSTIC_REPAIR_PROVEN__TASK226_FAIL_CLOSED_ATTESTATION_TRIGGERED__TRANSIENT_RETIRED_TREE_MUTATION_ACTOR_UNPROVEN__READ_ONLY_MUTATION_FORENSIC_REQUIRED`

## Reviewed authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Task-248 report HEAD: `06b7bc01161efe2c8bbb97fe0e0511d79ff8d62b`
- Executed exact candidate: `6c11a5e8f417300835e85441b88e0f37e3897353`
- Expected plugin fingerprint: `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`
- Public `v0.9.3` tag remains immutable at `26ce64a624255278a3a0266ad38746e0e6ed2e31`.

## Independent findings

### 1. The one-shot execution contract was respected

The fresh manifest-bound runner and launch manifest were qualified, hashed, read back, and bound to the exact detached candidate. The Scheduled Task was registered once, started once, and invoked `scripts/install.ps1` once. There was no post-start retry, second start, manual installer invocation, semantic send, recovery replay, or manual product repair.

### 2. Task 247's diagnostic repair is proven effective in live execution

The installer reached `plugin-rollover-prepare` and exited nonzero. Unlike Task 245, the repaired PowerShell 5.1 capture retained the complete relevant Python diagnostic and exact exception:

```text
RuntimeError: pre-install backup project-tree attestation mismatch
```

The traceback localizes the throw to `prepare_plugin_rollover_transaction()` at the full project-tree equality check. This closes the prior observability uncertainty.

### 3. The failed invariant is intentional and must remain fail-closed

The current prepare implementation copies the retired npm project to the external generation-rollover backup and immediately computes full project-tree hashes for the retired project and backup. A mismatch raises `pre-install backup project-tree attestation mismatch` before any rollover transaction is returned or persisted.

Existing Task-225/226 regression coverage explicitly mutates a non-payload source file after the top-level copy and requires this same mismatch to raise. Therefore a successor must not make the mismatch pass by weakening full-tree attestation, hashing only the package payload, retrying until hashes happen to match, or otherwise masking concurrent source mutation.

`_project_tree_sha256()` covers directory names, file relative paths, file sizes and bytes, and symlink state/targets; timestamps are not part of the digest. The Task-248 mismatch therefore cannot be explained by mtime-only drift.

### 4. The lower-level mutation actor/path remains unproven

Task 248 later read-only hashed both the installer-created external rollover backup and the current retired project to the same value:

`900ac13f85a6de75e40a632a534f2b0ceef53def1e8387fc3530c02a7413de58`

and observed no current path-level difference. That post-failure equality does not negate the earlier fail-closed mismatch and does not prove historical equality at the instant of attestation. It instead leaves a transient/concurrent mutation or observation race as a plausible category, while the exact file and actor remain unknown.

No new Task-248 transaction JSON was persisted, which is consistent with prepare throwing before successful return.

### 5. Post-failure state remained safe

The candidate was not installed; the canonical plugin remains the disabled predecessor fingerprint `e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`; controller remains passthrough generation 39; Gateway/provider/model/storage/recovery/delivery checks are READY; SQLite integrity is OK; pending delivery count is zero. Installer-owned backup artifacts are retained and must not be cleaned before forensic closure.

### 6. Report-head CI is GREEN

- PS5.1 Acceptance Smoke `33891454875` — SUCCESS
- Windows Installer Pack Smoke `33891454855` — SUCCESS
- Validate `33891454905` — SUCCESS

The compare from the pre-execution coordination authority to the report HEAD adds only the Task-248 report; no source/test/workflow drift occurred in the reporting step.

## Disposition

Task 248 is accepted as a real terminal installer failure with the exact fail-closed invariant now proven. It does **not** authorize an installer retry or a production change.

The next authorized work should be read-only forensic diagnosis of the retired project tree around the Task-248 execution window. The objective is to identify the path and, where possible, the process/actor responsible for the transient mutation without changing the retired tree or the retained rollover backup.

If historical OS/filesystem evidence cannot identify the actor, the proper successor is a separate repository/TDD instrumentation task that preserves per-path source-vs-backup differences at the mismatch point while keeping the existing fail-closed semantics. It must not be combined with another live installer attempt.

Semantic acceptance remains unauthorized.
