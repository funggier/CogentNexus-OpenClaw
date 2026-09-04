# CNX-20260904-237 — Task236 Source-Binding Contract Correction + Exact-Candidate Windows Install-Over Requalification

Status: `READY_FOR_HERMES`  
Executor: Hermes / authenticated Windows operator  
Coordinator / independent reviewer: ChatGPT  
Parent task: `CNX-20260903-236`  
Parent review verdict: `ACCEPT_BLOCKED_PREFLIGHT_DRIFT__COORDINATION_SOURCE_BINDING_CONTRACT_DEFECT_CONFIRMED__SUCCESSOR_REQUIRED`  
Repository/TDD parent: `CNX-20260903-235`  
Installer safety / attestation repair parent: `CNX-20260902-226`  
Known-good exact-source installer precedent: `CNX-20260902-230`  
Historical installer failure lineage: `CNX-20260902-223`  
Parent umbrella: `CNX-20260831-188`  
Updated: 2026-09-04 ICT

## Objective

Perform the exact-candidate Windows install-over that Task 236 was authorized to perform, but with the source-binding contract corrected to match the real installer implementation.

Task 236 did not start the installer and consumed no live mutation budget. Its blocker was an erroneous coordination requirement for a nonexistent `--install-source-commit` / `-InstallSourceCommit` installer parameter.

Task 237 therefore does **not** change production source. It binds installer authority by materializing and proving an exact detached checkout, then invoking `scripts/install.ps1` directly from that verified checkout.

This remains an installer-only task. It stops before semantic/durable-delivery acceptance.

## Exact candidate authority

Exact source commit:

`ffb0dd4ed47affe2e496c17b74ca74d358905bd7`

Expected installed plugin payload fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Public `v0.9.3` must remain immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Task-236 report:

`docs/operations/coordination/reports/CNX-20260903-236-task235-exact-candidate-windows-install-over-requalification.md`

Task-236 independent review:

`docs/operations/coordination/reviews/CNX-20260903-236-task235-exact-candidate-windows-install-over-requalification-review.md`

Exact candidate Actions freshly verified SUCCESS:

- Validate `33773085803`
- Windows Installer Pack Smoke `33773085772`
- PS5.1 Acceptance Smoke `33773085907`

Fresh GitHub authority supersedes this summary if newer product/source/test/workflow authority appears before execution.

## Corrected source-binding contract

The exact candidate `scripts/install.ps1` derives source from `$PSScriptRoot` / repository root and does not implement an install-source-commit argument.

Therefore Task 237 must use this binding:

```text
fresh fetch
-> disposable detached checkout of exact ffb0dd4...
-> prove exact HEAD and clean source
-> prove exact candidate fingerprint / required repair identity
-> invoke that checkout's scripts/install.ps1 directly
```

### Explicitly prohibited

Do not pass or invent any of:

```text
--install-source-commit
-InstallSourceCommit
InstallSourceCommit
```

Do not modify `install.ps1` merely to add such a parameter.

## Phase A — fresh repository authority

Immediately before Windows live work, capture:

1. current branch HEAD;
2. `ACTIVE.md` / `STATUS.md` naming Task 237 as active `READY_FOR_HERMES`;
3. Task-236 report and independent review;
4. exact candidate `ffb0dd4...` remains an ancestor of current coordination HEAD;
5. compare `ffb0dd4... -> current HEAD` and require no unexpected product/source/test/workflow drift;
6. exact candidate three required Actions remain terminal SUCCESS;
7. public `v0.9.3` remains exactly `26ce64a...`;
8. no newer coordination task supersedes Task 237.

Coordination-only commits after the candidate are expected.

Material product/source/test/workflow drift or ambiguous authority:

`BLOCKED_PREFLIGHT_DRIFT`

## Phase B — exact detached source materialization

Before any scheduler registration or product mutation, create one disposable checkout under `%LOCALAPPDATA%\Temp` from the fetched repository.

Require and record:

```text
git rev-parse HEAD = ffb0dd4ed47affe2e496c17b74ca74d358905bd7
HEAD is detached or otherwise pinned unambiguously to that exact object
working tree clean
git diff --quiet
git diff --cached --quiet
no untracked source mutation relevant to installation
```

Record the exact checkout path.

From that checkout, prove:

- `VERSION` = `0.9.3`;
- candidate plugin fingerprint = exactly `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`;
- `scripts/install.ps1` is the exact file from `ffb0dd4...`;
- `namespace_ownership.py` retains the Task-226 fail-closed `pre-install backup project-tree attestation mismatch` contract;
- accepted Task-235/236 candidate files are present exactly from the checkout.

If exact source binding cannot be proven:

`BLOCKED_SOURCE_BINDING`

No scheduler registration or installer start is authorized after this disposition.

## Phase C — read-only Windows preflight

Capture the live system again because Task 236 intentionally made no mutation:

- controller mode/generation;
- startup policy and startup adapter / `LastTaskResult`;
- Supervisor/doctor;
- AGENTS/managed policy identity;
- installed plugin id/version/path/source/enabled/status/fingerprint;
- live `namespace_ownership.py` identity;
- ownership manifest identity/hash;
- Gateway health/endpoint;
- selected provider and exact configured model, proving Ollama remains selected;
- Delivery state / pending outbox count;
- Recovery state / emittable unresolved recovery;
- SQLite integrity and relevant durable counts/status residue;
- Task-233 interrupted lineage state without modifying it;
- relevant OpenClaw/CogentNexus/Ollama process inventory;
- Task-223 retained transaction/inventory/backup evidence identities/hashes.

The pre-install plugin fingerprint may legitimately remain the previous accepted payload:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

Do not classify that expected prior payload as drift solely because it differs from the new candidate.

## Phase D — delivery/recovery hazard gate

Before installer registration/start require:

```text
Delivery READY
pending outbox = 0
Recovery READY
no emittable unresolved recovery capable of generating a delivery during this task
no unexplained active/nonterminal duplicate semantic lineage likely to emit
```

The known Task-233 interrupted/accepted lineage may remain as historical residue only if read-only evidence proves it is not currently emittable/replaying.

If unsafe or ambiguous:

`BLOCKED_DELIVERY_HAZARD`

Do not repair by editing/deleting Ticket, outbox, recovery, session, or SQLite state.

## Phase E — scheduler / installer execution topology

Use the authenticated Windows Scheduled Task topology proven by Task 230 unless fresh host evidence requires an evidence-driven harmless registration adaptation before start.

The installer task action must invoke **the exact `scripts/install.ps1` path inside the verified Task-237 detached checkout**.

Record:

- checkout path;
- exact `git rev-parse HEAD` immediately before registration and again immediately before start;
- exact installer script path;
- exact PowerShell command line and supported arguments;
- task principal/logon/run-level/settings;
- registration/readback;
- start timestamp;
- earliest installer process/invocation timestamp;
- stdout/stderr/transcript/log paths;
- terminal scheduled-task state / `LastTaskResult`;
- installer exit code and terminal timestamps.

Do not use `-SkipPlugin`, `-SkipGatewayRestart`, `-SkipAgentsPolicy`, or `-LinkPlugin`.

### Installer retry gate

Before installer execution:

- installer-task registration: max 2 attempts total;
- attempt 2 only after genuine tooling/registration failure, with a materially different evidence-driven method and proof the first task did not start;
- installer successful start requests: max 1;
- installer invocation: max 1.

As soon as the installer task/process starts:

`INSTALLER_RETRY_GATE=CLOSED`

After that:

```text
installer execution retries = 0
second installer start = 0
second installer invocation = 0
manual plugin repair = 0
manual lifecycle repair = 0
```

Observer/query failures after start never authorize another product execution.

## Phase F — installer-owned plugin replacement / rollover

Because the live installed fingerprint is expected to differ from the candidate, the installer may legitimately require plugin replacement / generation rollover.

Do not pre-impose rollover cardinality zero.

If installer classification selects rollover/replacement, prove:

- classification and action-resolution evidence;
- all mutation is owned by the single authorized installer invocation;
- Task-226 fail-closed prepare attestation remains active;
- any rollover prepare/finalize succeeds;
- no manual `openclaw plugins install/uninstall/enable/disable` is used;
- no manual copy/delete/rename/manifest repair is used;
- new transaction/inventory/backup artifacts are captured with exact paths, hashes, timestamps, and self-consistency evidence;
- historical Task-223 retained artifacts remain unchanged.

A terminal installer/rollover/finalizer failure after start:

`FAIL_INSTALLER_TERMINAL`

Do not rerun installer.

## Phase G — exact installed identity

After terminal installer success require:

```text
installer exit code = 0
LastTaskResult = 0 where applicable
installation success marker present
installer invocation count = 1
```

Then prove live canonical plugin identity:

- id/version/path/source correct;
- enabled/healthy;
- payload fingerprint exactly `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`;
- live `v091-dashboard-verified-delivery.ts` corresponds to candidate payload;
- live `namespace_ownership.py` retains Task-226 fail-closed attestation repair;
- ownership manifest is coherent with the resulting installation/generation.

If installer reports success but exact identity cannot be proven:

`FAIL_PLUGIN_IDENTITY`

No manual repair.

## Phase H — managed convergence and final health

Allow only normal installer/runtime convergence. Do not manually force lifecycle state.

Prove:

- controller coherently `managed`;
- generation internally coherent;
- startup policy enabled as expected;
- startup adapter installed/Ready with successful result where applicable;
- Supervisor/doctor healthy/coherent;
- Gateway healthy at intended loopback endpoint;
- provider remains Ollama and configured model unchanged;
- Delivery READY, pending outbox = 0;
- Recovery READY, no replay/resend introduced;
- SQLite integrity OK;
- no unexpected duplicate/nonterminal Ticket/session/run residue introduced;
- relevant process inventory coherent;
- historical Task-223 and Task-233 evidence preserved;
- no semantic turn occurred.

If exact plugin identity is correct but managed convergence fails:

`FAIL_MANAGED_CONVERGENCE`

If final runtime health is materially unhealthy:

`FAIL_POST_INSTALL_HEALTH`

## Read-only retry policy

Read-only observer/query/evidence collection may use up to 2 additional attempts per logical observation only for tooling/transport/query/quoting/transient evidence-collection failures.

Every retry must materially change method or directly address the observed failure.

Required attempt ledger columns:

```text
logical operation
attempt number
UTC time
method
result/error
could product/semantic state change?
remaining retry budget
next rationale / changed method
```

Final retry classification exactly one of:

- `RETRY_POLICY_EFFECTIVE`
- `RETRY_POLICY_NOT_NEEDED`
- `RETRY_POLICY_EXHAUSTED_WITHOUT_RECOVERY`
- `RETRY_POLICY_STOPPED_BY_PRODUCT_BOUNDARY`

## Effect / mutation budget

```text
Dashboard human semantic submissions: 0
Discord-origin semantic submissions: 0
direct operator Discord/API Sends: 0
semantic retries/resubmissions: 0
manual durable delivery: 0
manual Ticket/outbox/recovery/SQLite mutation: 0
manual provider/model substitution: 0
manual process termination: 0
manual Gateway/lifecycle repair: 0
manual plugin install/copy/delete/rename/manifest repair: 0
reset: 0
uninstall: 0
fresh reinstall: 0
installer successful starts: <= 1
installer invocations: <= 1
installer execution retries after start: 0
Task-223 retained forensic evidence mutation: 0
Task-233 replay/settlement/deletion: 0
Release/tag/asset mutation: 0
production/source/test/workflow edits: 0
force push/history rewrite: 0
```

Installer-owned plugin replacement/rollover and normal installer-owned lifecycle/convergence are the only authorized live product mutations.

## PASS cardinality

A PASS requires:

```text
exact detached source checkout: 1
source HEAD = ffb0dd4...: proven immediately before installer registration/start
installer invocation lineage: exactly 1
installer execution retry after start: 0
manual plugin mutation: 0
Dashboard semantic submissions: 0
Discord semantic submissions: 0
direct operator Discord/API Sends: 0
semantic acceptance effects: 0
operator recovery replay/resend: 0
```

## Allowed dispositions

- `PASS_EXACT_CANDIDATE_WINDOWS_INSTALL_OVER_REQUALIFIED`
- `BLOCKED_PREFLIGHT_DRIFT`
- `BLOCKED_SOURCE_BINDING`
- `BLOCKED_DELIVERY_HAZARD`
- `FAIL_INSTALLER_REGISTRATION`
- `FAIL_INSTALLER_TERMINAL`
- `FAIL_PLUGIN_IDENTITY`
- `FAIL_MANAGED_CONVERGENCE`
- `FAIL_POST_INSTALL_HEALTH`
- `BLOCKED_EVIDENCE`

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260904-237-task236-source-binding-contract-correction-exact-candidate-windows-install-over-requalification.md`

Include:

- fresh authority;
- exact detached checkout path + source-binding proofs;
- preflight + hazard gate;
- scheduler/installer attempt ledger;
- exact supported installer command and timestamps;
- classification / installer-owned replacement-rollover evidence;
- terminal task/result/exit/log evidence;
- exact installed fingerprint/live identity;
- new rollover artifacts if any;
- Task-223/Task-233 evidence preservation;
- managed convergence/final health;
- mutation/effect/cardinality ledger;
- retry classification;
- explicit semantic/direct-send counts = 0;
- final disposition.

Then **STOP for independent ChatGPT review**.

Even on PASS, do not proceed to Dashboard semantic acceptance, Discord semantic testing, replay/settlement of Task 233, stale-evidence cleanup, reset/uninstall/fresh reinstall, or public Release/tag/asset mutation without a separate successor.