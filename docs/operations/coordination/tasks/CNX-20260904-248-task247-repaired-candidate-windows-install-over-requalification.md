# CNX-20260904-248 — Task-247 Repaired-Candidate Windows Install-Over Requalification

## Purpose

Requalify one live Windows install-over using the exact Task-247 repaired candidate after the Windows PowerShell 5.1 native-stderr capture defect was proven and repaired.

This is an installer-only task. It must either prove successful install-over convergence or preserve the exact terminal diagnostic from the first failing stage. It must not perform semantic acceptance.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Parent task: `CNX-20260904-247`
- Failure lineage: `CNX-20260904-245`, `CNX-20260904-246`
- Harness lineage: `CNX-20260904-243`, `CNX-20260904-244`, `CNX-20260904-245`
- Parent umbrella: `CNX-20260831-188`
- Exact executable candidate: `6c11a5e8f417300835e85441b88e0f37e3897353`
- Expected plugin fingerprint: `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`
- Public `v0.9.3` tag must remain at `26ce64a624255278a3a0266ad38746e0e6ed2e31`.

Task-247 exact-SHA required Actions are accepted GREEN:

- PS5.1 Acceptance Smoke `33884732550` — SUCCESS
- Windows Installer Pack Smoke `33884732528` — SUCCESS
- Validate `33884732569` — SUCCESS on attempt 2, unchanged SHA

## Critical interpretation

Task 247 proved and repaired the PowerShell 5.1 capture defect. It did **not** prove that `prepare_plugin_rollover_transaction()` itself will succeed.

Therefore:

- if `plugin-rollover-prepare` succeeds, continue the normal installer exactly once;
- if it fails, the new capture boundary must preserve the bounded complete child diagnostic, including the Python exception type/message or equivalent exact invariant evidence;
- after any started installer failure, do not retry.

## Phase A — fresh GitHub and live preflight

Before any registration/start:

1. fresh-fetch branch authority, `ACTIVE.md`, `STATUS.md`, Task 248, Task-247 report/review;
2. prove exact candidate/tag/Actions identities above;
3. compare exact candidate to current branch and record product/source/test/workflow drift separately from coordination-only drift;
4. perform read-only live checks:
   - controller mode/generation;
   - Gateway/provider/model/storage/delivery/recovery health;
   - SQLite integrity;
   - installed canonical plugin version/fingerprint/enabled state;
   - ownership manifest state;
   - pending rollover/transaction/inventory residue;
   - Task-245/246 forensic archive preservation;
5. if live state has externally converged to the candidate plugin or materially differs from the expected safe predecessor state, STOP and classify before any installer execution.

Expected safe predecessor state from Task 246 is supporting context only, not authority:

```text
controller = passthrough
generation = 39
installed plugin fingerprint = e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
plugin disabled
Delivery READY / pending 0
Recovery READY / no replay
SQLite integrity ok
```

## Phase B — exact source binding

Create one fresh disposable detached checkout of exact candidate `6c11a5e8...`.

Before using it prove and record:

- `git rev-parse HEAD` exactly equals candidate;
- detached/pinned state is unambiguous;
- worktree clean;
- `git diff --quiet` and `git diff --cached --quiet` pass;
- no relevant untracked source mutation;
- `VERSION` is `0.9.3`;
- candidate plugin fingerprint is exactly `1ff69c...`;
- top-level `scripts/install.ps1` contains the Task-247 `Invoke-NativeInstallerDiagnostic` repair;
- Task-226 ownership-attestation repair remains present.

Do not invent or use `--install-source-commit`, `-InstallSourceCommit`, or equivalent source-binding parameters.

## Phase C — durable hardened runner and manifest

Do not depend on old `%TEMP%` runner/evidence artifacts.

Create a fresh task-specific **non-temp durable evidence root** under:

`%LOCALAPPDATA%\CogentNexus-OpenClaw\forensics\CNX-20260904-248\`

Store there, before start:

- frozen hardened runner source;
- runner SHA-256;
- frozen launch manifest JSON;
- manifest SHA-256;
- exact source/candidate proof;
- preflight snapshots;
- observation log.

The launch manifest must bind:

- child executable = Windows PowerShell 5.1;
- exactly one `-File` argument;
- the value immediately following `-File` = exact detached candidate `scripts/install.ps1`;
- intended Workspace argument only;
- no `SkipPlugin`, `SkipGatewayRestart`, `SkipAgentsPolicy`, or `LinkPlugin` switches.

Scheduled Task action must carry only the simple frozen runner/manifest/evidence-root binding. Do not nest the installer argument vector in Scheduled Task quoting.

Before registration/start:

1. hash runner and manifest;
2. direct-qualify the fresh runner with harmless synthetic success/nonzero child behavior sufficient to prove stdout/stderr/exit/result/finally persistence;
3. rehash runner and manifest and require byte identity;
4. parse/read back manifest and prove exact candidate `-File` binding;
5. after task registration, read back the Scheduled Task action and prove it references the intended runner/manifest only;
6. immediately before start, re-prove runner SHA, manifest SHA, exact candidate HEAD and `-File` binding.

Any pre-start binding mismatch => STOP without start.

## Phase D — one-shot installer execution

Execution cardinality:

```text
successful installer Scheduled Task registrations <= 1
installer task starts <= 1
scripts/install.ps1 child invocations <= 1
installer execution retries after start = 0
second task start = 0
second installer invocation = 0
```

Once the task is started, `INSTALLER_RETRY_GATE=CLOSED` permanently for Task 248.

Observe to terminal state. Capture at minimum:

- Scheduled Task `LastTaskResult`;
- runner-started/result/transcript;
- child stdout/stderr;
- all `CNXCLAW_INSTALL_STAGE_START/COMPLETE` markers;
- exact installer child exit;
- full bounded failure diagnostic if nonzero;
- new rollover token/backup/transaction/inventory identities when present.

### If `plugin-rollover-prepare` fails

STOP after read-only postflight and evidence preservation.

The report must include the **complete Task-247-repaired bounded diagnostic**, especially:

- Python exception type;
- exception message;
- traceback frames available within the bound;
- exact source line/function if present;
- exact child/installer exit codes;
- new backup token/path if created;
- transaction presence/absence;
- external generation-backup inventory and timestamps.

Do not rerun merely because the newly revealed exception looks easy to fix.

### If prepare succeeds

Prove transaction creation and self-consistency, then allow the same single installer invocation to continue naturally through plugin install and rollover-finalize.

If any later installer stage fails, STOP with the same no-retry rule and capture the exact stage diagnostic/evidence.

## Phase E — PASS postflight requirements

PASS requires all of the following, not merely installer exit 0:

- installer child exit 0;
- Scheduled Task result 0 where applicable;
- invocation count exactly 1;
- canonical installed plugin fingerprint exactly `1ff69c...`;
- Task-247 repaired installer source identity proven for the executed source;
- rollover prepare/finalize transaction evidence coherent if rollover occurred;
- ownership manifest coherent;
- controller converged to managed mode with coherent generation;
- startup adapter/service state ready as expected;
- Gateway healthy on loopback;
- provider remains Ollama and configured model selection is unchanged;
- Delivery READY, pending terminal deliveries 0;
- Recovery READY, no replay/emittable residue;
- SQLite integrity `ok`;
- no unexpected duplicate/nonterminal residue;
- Task-245/246 forensic archive preserved unchanged;
- no semantic/direct message effects.

## Hard fences

Forbidden during Task 248:

```text
Dashboard human submissions = 0
Discord-origin submissions = 0
direct Discord/API sends = 0
semantic retries = 0
manual Ticket/outbox/recovery/SQLite mutation = 0
manual durable-delivery mutation = 0
manual provider/model substitution = 0
manual plugin copy/install/delete/rename/manifest repair = 0
manual lifecycle/Gateway repair = 0
process termination as repair = 0
reset/uninstall/fresh reinstall = 0
Task-245/246 forensic evidence deletion/cleanup = 0
production/source/test/workflow edits = 0
release/tag/asset mutation = 0
force push/history rewrite = 0
```

Installer-owned normal writes inside the single authorized invocation are allowed.

## Allowed dispositions

- `PASS_REPAIRED_CANDIDATE_WINDOWS_INSTALL_OVER_REQUALIFIED`
- `BLOCKED_PREFLIGHT_DRIFT`
- `BLOCKED_SOURCE_BINDING`
- `BLOCKED_RUNNER_BINDING`
- `BLOCKED_DELIVERY_HAZARD`
- `FAIL_INSTALLER_REGISTRATION`
- `FAIL_INSTALLER_TERMINAL_DIAGNOSTIC_PRESERVED`
- `FAIL_PLUGIN_IDENTITY`
- `FAIL_MANAGED_CONVERGENCE`
- `FAIL_POST_INSTALL_HEALTH`
- `BLOCKED_EVIDENCE`

## Report and STOP

Publish:

`docs/operations/coordination/reports/CNX-20260904-248-task247-repaired-candidate-windows-install-over-requalification.md`

Then STOP for independent ChatGPT review.

Even on PASS, do not perform Dashboard semantic acceptance in Task 248.
