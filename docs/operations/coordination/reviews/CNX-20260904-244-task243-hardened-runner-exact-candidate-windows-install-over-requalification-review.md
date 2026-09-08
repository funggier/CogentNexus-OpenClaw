# Independent Review — CNX-20260904-244

## Verdict

`ACCEPT_FAIL_CLOSED_PRESTART_ACTION_BINDING_BLOCK__NO_INSTALLER_OR_PRODUCT_EXECUTION__FRESH_MANIFEST_BOUND_SUCCESSOR_AUTHORIZED`

## Reviewed evidence

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Task-244 report HEAD: `2da9be61abd1da7ea36c508af640e1732853e2b1`
- Exact executable candidate: `18a51b15768fb3d2196e65f1ef470c34aeef7f36`
- Candidate plugin fingerprint: `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`
- Immutable public `v0.9.3`: `26ce64a624255278a3a0266ad38746e0e6ed2e31`

Fresh compare from Task-244 authority `edc44bb6a03f573aa715bc04281dcb65a0f9fc41` to report HEAD contains only the Task-244 report. No product/source/test/workflow drift was introduced.

Report-head Actions are all GREEN:

```text
PS5.1 Acceptance Smoke        33872664615 = SUCCESS
Windows Installer Pack Smoke 33872664619 = SUCCESS
Validate                      33872664669 = SUCCESS
```

Fresh exact-candidate Actions remain GREEN as required by Task 244.

## Accepted findings

Task 244 correctly proved the fresh live preflight:

```text
controller = passthrough
generation = 39
provider = ollama
installed plugin fingerprint = e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
candidate already exact = false
pendingRollover = false
mode = upgrade
installPlugin = true
rolloverPlugin = true
```

The candidate therefore still requires a real plugin upgrade/rollover; Task-230 already-exact assumptions do not apply.

Task 244 also regenerated and qualified a fresh hardened runner and recorded its frozen SHA-256:

`f7287251437688cc7ff529d2810e8f2af12a1f2ce922d8c50da2a0e5fa5fc706`

The direct harmless qualifications proved both deterministic child nonzero exit propagation (`37`) and child-launch-exception capture. Rehash after qualification matched the frozen identity.

## Failure classification

The registered installer Scheduled Task failed the mandatory pre-start binding gate because the nested `-ChildArguments` rendering bound the nested `-File` argument to `powershell.exe` rather than to the detached candidate `scripts/install.ps1`.

The task was not started.

Authoritative effect boundary:

```text
installer Scheduled Task registrations = 1
installer Scheduled Task starts = 0
installer child invocations = 0
scripts/install.ps1 invocations = 0
rollover prepare/finalize = 0
plugin mutation = 0
controller/Gateway/lifecycle mutation = 0
manual DB writes = 0
semantic submissions/sends = 0
```

This is therefore an operator harness/action-definition defect and not an installer, rollover, plugin, runtime, database, or semantic product failure.

The fail-closed behavior is accepted: Task 244 detected the wrong binding before start and did not update, unregister, re-register, directly invoke, or otherwise bypass the one-shot gate.

## Successor requirement

A successor may make one new bounded installer attempt because the actual installer start/invocation budget was never consumed. It must not reuse or mutate the Task-244 registered task.

The successor must eliminate the nested Task Scheduler `-ChildArguments` construction that caused Task 244. Use a simple scheduler binding to a fresh frozen hardened runner plus a fresh frozen launch manifest (or an equivalently unambiguous immutable launch description).

Required launch topology:

```text
Scheduled Task action
  -> powershell.exe
  -> frozen hardened runner
  -> frozen launch manifest
  -> child executable = Windows PowerShell 5.1
  -> child argument vector contains -File
  -> value immediately following -File = exact detached candidate scripts/install.ps1
```

Before registration, the successor must create, hash, and directly qualify the runner with harmless fixtures. It must persist and hash the production launch manifest separately. After registration and before start it must read back the Scheduled Task action, re-read the frozen manifest, and prove all hashes/paths are unchanged and that the resolved child `-File` target is exactly the detached candidate installer path.

If any readback differs, STOP without start. Do not repair or re-register the task in the same successor.

## Preserved fences

- Fresh Windows read-only evidence wins over this review.
- Preserve Task-223/237/241/242/243/244 evidence and registered task definitions.
- No reset/uninstall/reinstall sequence.
- No direct/manual plugin replacement or rollover mutation.
- No semantic Dashboard/Discord/API sends in the installer successor.
- No provider/model substitution.
- No force push/history rewrite.

## Independent disposition

`TASK244_ACCEPTED_FAIL_CLOSED__INSTALLER_UNEXECUTED__ACTION_BINDING_DEFECT_ISOLATED__ONE_FRESH_MANIFEST_BOUND_INSTALLER_SUCCESSOR_ALLOWED`
