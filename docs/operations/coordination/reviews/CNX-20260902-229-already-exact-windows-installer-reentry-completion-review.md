# CNX-20260902-229 — Already-Exact Windows Installer Re-entry Completion Review

Date: 2026-09-02 ICT  
Reviewed report: `docs/operations/coordination/reports/CNX-20260902-229-already-exact-windows-installer-reentry-completion.md`

## Verdict

`REJECT_COMPLIANCE__ACCEPT_FAIL_CLOSED_PRODUCT_PRESERVATION__BOUNDED_TOOLING_RETRY_SUCCESSOR_REQUIRED`

Task 229 did **not** reach the CogentNexus installer. The product/live state remained preserved and the already-exact gate was re-proven. However, Task 229 did not comply with its own Phase-F stop boundary because the report records multiple scheduler registration attempts after the first registration failure.

This is therefore not an installer/product failure and not evidence that the already-exact re-entry contract is wrong. It is a harness/tooling authority failure plus a task-execution compliance issue.

## Accepted evidence

The following evidence is accepted from Task 229:

- exact repaired source remained `9a8510f1317c8e53c01c233b080ec20357cd22df`;
- source and installed plugin fingerprint both remained `e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`;
- already-exact classification/action gate passed:

```text
mode=upgrade
pendingRollover=false
pluginAlreadyExact=true
installPlugin=false
rolloverPlugin=false
skipPlugin=false
```

- installer invocations: `0`;
- Task-229 successful registrations: `0`;
- Task-229 starts: `0`;
- plugin install / rollover prepare / rollover finalize: `0`;
- manual lifecycle/Gateway/SQLite/process/provider/Discord mutations: `0`;
- retained Task-223 transaction/inventory/backup/manifest identities remained unchanged;
- final controller/Gateway/provider/delivery/recovery/SQLite state remained healthy and preserved.

The failure occurred before a temporary task was successfully created. No product repair is justified from this evidence.

## Compliance defect in Task 229 execution

Task 229 explicitly required:

> If registration/readback is not exact, remove only the temporary Task-229 task and stop `FAIL_TASK_REGISTRATION`.

The report nevertheless records three registration attempts before task creation:

1. PowerShell ScheduledTasks attempt failed because `AllowDemandStart` was not accepted by the local PowerShell cmdlet surface.
2. A second PowerShell registration attempt failed with `HRESULT 0x80070057` at `UserId`.
3. A native `schtasks.exe` equivalent was then attempted and also failed at `UserId`.

The report also says near its Decision section that "no retry was attempted", which conflicts with the later attempt history. The mutation ledger correctly reports zero **successful** task registrations, but it does not erase the fact that multiple registration attempts occurred.

This did not damage product state, but it exceeded the authority of Task 229. The successor must not retroactively treat these retries as compliant.

## Root-cause direction

The scheduler evidence points to a harness identity/registration problem, not installer logic:

- Task 215 previously proved the same host can register, start and terminally observe a direct Scheduled Task using an Interactive/Limited principal.
- Task 214 already showed one tooling-enum adaptation was necessary on this host (`InteractiveToken` was invalid to the PowerShell cmdlet surface; `Interactive` succeeded).
- Task 229 now shows another host/tool-surface mismatch: bare/current `UserId` construction is not being accepted by either the PowerShell registration path or the attempted `schtasks.exe` equivalent.

The next task should reconstruct the canonical current-user identity from Windows itself (`WindowsIdentity`, SID and domain-qualified name), qualify it with a harmless canary task, and only then reuse the proven principal/topology for the installer task.

Do not guess or hard-code a bare username from a report display label.

## Tooling retry policy — successor trial

The user explicitly requested a retry mechanism for tool/harness failures so the executor can adapt rather than immediately dead-end. This review approves that idea for the successor under a bounded, fail-closed contract.

Retries are allowed only while **all** of these remain true:

```text
installer invocation count = 0
installer task start count = 0
no installer process observed
no product/live mutation occurred
any temporary task created by a failed attempt is exactly cleaned before the next attempt
failure is attributable to tooling/launcher/observer/registration mechanics, not product behavior
```

Every retry must:

- state the failed hypothesis/tool surface;
- change one material variable or method based on evidence;
- preserve a finite retry budget;
- record command/method, result, error, task-created yes/no, cleanup result and rationale for the next method;
- stop when the retry budget is exhausted.

Once the installer task is started or an installer process is observed, the tooling retry budget closes permanently. No second installer start/invocation is authorized.

## Successor decision

Open a new Task 230 that:

1. keeps Task-223 forensic evidence immutable;
2. re-proves the already-exact gate before mutation;
3. reconstructs the exact current Windows principal from live identity/SID evidence;
4. uses a harmless canary Scheduled Task to qualify registration/readback/start/terminal propagation;
5. permits bounded tooling retries only before installer start;
6. after one canary topology is proven, creates one installer Scheduled Task using the same proven principal/logon model;
7. starts the installer task exactly once;
8. never retries the installer invocation;
9. reports a complete attempt ledger and whether the retry policy improved recovery or merely consumed budget.

Discord budget remains `0 Sends`.

## Review conclusion

Task 229 is accepted only as a **fail-closed product-preservation result**. It is rejected as fully compliant execution because registration retries exceeded the task's stop boundary. The correct next action is a separately authorized, bounded tooling-retry successor—not a product/source repair and not an ad-hoc installer retry.
