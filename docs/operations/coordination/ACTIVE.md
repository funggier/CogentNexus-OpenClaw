# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK230_SCHEDULER_IDENTITY_RECOVERY_BOUNDED_RETRY_INSTALLER_REENTRY`
Current disposition: `TASK229_FAIL_CLOSED_PRODUCT_PRESERVED__TOOLING_RETRY_SUCCESSOR_REQUIRED`
Task ID: `CNX-20260902-230`
Parent task: `CNX-20260902-229`
Repair parent: `CNX-20260902-226`
Failure parent: `CNX-20260902-223`
Forensic parents: `CNX-20260902-224`, `CNX-20260902-227`, `CNX-20260902-228`, `CNX-20260902-229`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-02 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Published authority

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

No Release/tag/asset mutation is authorized.

## Accepted source authority

Exact repaired source remains:

`9a8510f1317c8e53c01c233b080ec20357cd22df`

Accepted plugin payload fingerprint:

`e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`

Task-229 report:

`reports/CNX-20260902-229-already-exact-windows-installer-reentry-completion.md`

Task-229 independent review:

`reviews/CNX-20260902-229-already-exact-windows-installer-reentry-completion-review.md`

Review verdict:

`REJECT_COMPLIANCE__ACCEPT_FAIL_CLOSED_PRODUCT_PRESERVATION__BOUNDED_TOOLING_RETRY_SUCCESSOR_REQUIRED`

Task 229 never invoked the installer and preserved product/live state, but its report records multiple scheduler registration attempts despite the old task requiring stop after the first registration failure. Task 230 explicitly authorizes bounded tooling retries so adaptation is finite, auditable and in-contract.

## Active Task 230

Execute:

`tasks/CNX-20260902-230-scheduler-identity-recovery-bounded-retry-installer-reentry.md`

Task 230 must first re-prove the already-exact gate:

```text
mode=upgrade
pendingRollover=false
pluginAlreadyExact=true
installPlugin=false
rolloverPlugin=false
```

Then reconstruct the canonical current Windows scheduler identity from live `WindowsIdentity.Name`, SID, `whoami /user`, and retained Task-215 task XML/readback if available.

A harmless direct Scheduled Task canary must qualify the principal/logon topology before any installer task is started.

## Bounded tooling retry trial

Retries are allowed only before installer start and only for harness/tooling/registration/observer failures.

Key budgets:

```text
read-only probe/observer retries: up to 2 additional attempts per logical observation
harmless canary registration attempts: max 4 total
installer-task registration attempts before start: max 2 total
installer task starts: exactly 1 maximum
installer invocations: exactly 1 maximum
installer retries after start: 0
```

Every tooling retry must change a material hypothesis/method, prove task cleanup/absence as applicable, and be recorded in an attempt ledger with method, identity form, error/HRESULT, cleanup result, remaining budget and rationale for the next method.

Once the installer task starts or an installer process is observed:

`INSTALLER_RETRY_GATE=CLOSED`

It cannot reopen during Task 230.

## Historical evidence boundary

Task-223 transaction, matching inventory, ownership manifest and backup remain immutable forensic evidence. They must not be finalized, edited, moved, renamed, deleted, archived, replaced or reused.

## Runtime / Discord boundary

Task 230 does not permit:

- second installer start/invocation;
- installer retry after start;
- skip/link installer override flags;
- manual plugin/rollover actions;
- manual cnxclaw/Gateway lifecycle repair;
- stale-evidence cleanup/finalization;
- manual SQLite write;
- process termination;
- provider/model substitution;
- Release/tag/asset mutation;
- product/source/test/workflow edit;
- force push/history rewrite;
- Discord Send/API semantic traffic.

Discord budget: `0 Sends`.

## Stop boundary

Hermes must publish:

`reports/CNX-20260902-230-scheduler-identity-recovery-bounded-retry-installer-reentry.md`

The report must include the complete retry/attempt ledger and classify retry usefulness as one of:

- `RETRY_POLICY_EFFECTIVE`
- `RETRY_POLICY_NOT_NEEDED`
- `RETRY_POLICY_EXHAUSTED_WITHOUT_RECOVERY`
- `RETRY_POLICY_STOPPED_BY_PRODUCT_BOUNDARY`

Then stop for independent ChatGPT review before any semantic/durable-delivery acceptance, stale-evidence cleanup or additional live mutation.
