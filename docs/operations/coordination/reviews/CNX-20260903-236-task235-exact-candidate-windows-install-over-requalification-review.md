# CNX-20260903-236 — Independent Review

## Verdict

`ACCEPT_BLOCKED_PREFLIGHT_DRIFT__COORDINATION_SOURCE_BINDING_CONTRACT_DEFECT_CONFIRMED__SUCCESSOR_REQUIRED`

Task 236 correctly stopped fail-closed before any installer registration or product mutation. The reported blocker is real, but the defect is in the Task-236 coordination instruction, not in the exact candidate installer implementation.

## Reviewed authority

- Task-236 report HEAD at review start: `1e7c139bb361364fed12bda05144a9fa6dbc3440`
- Exact accepted candidate: `ffb0dd4ed47affe2e496c17b74ca74d358905bd7`
- Expected candidate plugin fingerprint: `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`
- Public `v0.9.3`: `26ce64a624255278a3a0266ad38746e0e6ed2e31`
- Parent umbrella: `CNX-20260831-188`

Fresh compare `ffb0dd4... -> 1e7c139...` is coordination-only. No product/source/test/workflow drift was introduced after the accepted candidate.

Exact candidate Actions were freshly rechecked and are terminal SUCCESS:

- Validate `33773085803`
- Windows Installer Pack Smoke `33773085772`
- PS5.1 Acceptance Smoke `33773085907`

The report-head docs-triggered Actions were not all terminal at review time: Windows Installer Pack Smoke `33821083360` and PS5.1 Acceptance Smoke `33821083361` were SUCCESS, while Validate `33821083374` remained in progress. This does not change the root-cause adjudication because the only report-head delta from the candidate is coordination documentation.

## Independent findings

### 1. Hermes complied with the fail-closed boundary

The report proves Task 236 stopped before:

```text
installer task registration: 0
installer start: 0
installer invocation: 0
plugin mutation: 0
manual lifecycle/Gateway mutation: 0
Dashboard semantic submissions: 0
Discord semantic submissions: 0
direct operator Discord/API Sends: 0
recovery replay/resend: 0
manual durable-state writes: 0
```

The live preflight itself was coherent: managed runtime, Ollama selected, Gateway healthy, Delivery READY/pending 0, Recovery READY, SQLite integrity OK, and the prior installed plugin fingerprint remained the accepted earlier payload. The Task-233 interrupted lineage remained untouched.

Therefore no installer retry budget or semantic/effect budget was consumed.

### 2. Task 236 required a nonexistent installer parameter

Task 236 explicitly required:

```text
--install-source-commit ffb0dd4ed47affe2e496c17b74ca74d358905bd7
```

However exact candidate `scripts/install.ps1` declares only:

```text
[string]$Workspace
[switch]$SkipPlugin
[switch]$SkipGatewayRestart
[switch]$SkipAgentsPolicy
[switch]$LinkPlugin
```

There is no `InstallSourceCommit` parameter or equivalent source-commit override in the exact candidate installer contract.

The installer binds its source operationally through `$PSScriptRoot` / repository root. Therefore passing the Task-236 argument would have been an unsupported invocation, and Hermes was correct not to attempt it.

### 3. This is a coordination-contract defect, not a production-source defect

Task 230 already established the correct exact-source execution topology:

```text
materialize exact detached source commit
-> verify exact HEAD / clean source
-> invoke scripts/install.ps1 from that exact source path
```

Task 230 explicitly authorized a disposable exact-first checkout and required the installer task action to use the exact repaired source path. It then completed one successful installer invocation without any source-commit override flag.

Therefore Task 236 incorrectly invented an additional installer argument instead of reusing the proven source-binding mechanism.

No production change is justified by this blocker. Adding a new production installer parameter solely to satisfy the erroneous Task-236 instruction would be unnecessary scope expansion.

## Correct successor contract

A successor may reattempt the same exact-candidate live install-over only after correcting the coordination contract as follows:

1. fresh-fetch repository authority and ensure no newer product/source/test/workflow drift;
2. materialize `ffb0dd4ed47affe2e496c17b74ca74d358905bd7` into a disposable detached checkout;
3. prove exact source binding before any scheduler mutation:
   - `git rev-parse HEAD` equals exactly `ffb0dd4...`;
   - detached HEAD / no branch ambiguity;
   - clean worktree / no local source mutation;
   - source plugin fingerprint equals exactly `1ff69c459...`;
   - required Task-226 fail-closed ownership repair remains present;
4. use the exact `scripts/install.ps1` path from that verified checkout;
5. do **not** pass `--install-source-commit`, `-InstallSourceCommit`, or any invented source override;
6. preserve the Task-236 installer-only and semantic-zero fences;
7. preserve exactly-one installer start/invocation and zero execution retries after start;
8. after terminal success, prove exact installed candidate identity, managed convergence, quiet Delivery/Recovery, SQLite integrity, and unchanged retained evidence;
9. stop again for independent review before any semantic acceptance turn.

## Disposition of Task 236

Task 236 itself is not a PASS because no installer execution occurred.

Its `BLOCKED_PREFLIGHT_DRIFT` disposition is accepted as the nearest allowed fail-closed classification, with the more precise independent diagnosis:

`COORDINATION_SOURCE_BINDING_CONTRACT_DEFECT`

The live system remained preserved and no cleanup/rollback is required before the successor beyond a fresh read-only preflight.

## Authorization

Authorize one successor for:

`TASK236_SOURCE_BINDING_CONTRACT_CORRECTION__EXACT_CANDIDATE_WINDOWS_INSTALL_OVER_REQUALIFICATION`

No semantic submission, Discord send, stale-evidence cleanup, reset, uninstall, fresh reinstall, Release/tag mutation, or production/source/test/workflow edit is authorized by this review.
