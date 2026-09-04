# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK245_TASK244_MANIFEST_BOUND_EXACT_CANDIDATE_WINDOWS_INSTALL_OVER_REQUALIFICATION`
Current disposition: `TASK244_ACCEPTED_FAIL_CLOSED__INSTALLER_UNEXECUTED__ACTION_BINDING_DEFECT_ISOLATED__ONE_FRESH_MANIFEST_BOUND_INSTALLER_SUCCESSOR_ALLOWED`
Task ID: `CNX-20260904-245`
Parent task: `CNX-20260904-244`
Runner qualification parent: `CNX-20260904-243`
Installer evidence parents: `CNX-20260904-241`, `CNX-20260904-244`
Candidate-validation parent: `CNX-20260904-240`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-04 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / independent reviewer: ChatGPT

## Accepted Task-244 boundary

Independent review verdict:

`ACCEPT_FAIL_CLOSED_PRESTART_ACTION_BINDING_BLOCK__NO_INSTALLER_OR_PRODUCT_EXECUTION__FRESH_MANIFEST_BOUND_SUCCESSOR_AUTHORIZED`

Reviewed Task-244 report HEAD:

`2da9be61abd1da7ea36c508af640e1732853e2b1`

Task 244 registered one installer Scheduled Task but deliberately did not start it because pre-start readback proved the nested `-ChildArguments` binding was wrong: the nested `-File` target resolved to `powershell.exe` instead of the exact candidate `scripts/install.ps1`.

Accepted effect boundary:

```text
installer task registrations = 1
installer task starts = 0
installer child invocations = 0
scripts/install.ps1 invocations = 0
plugin/rollover/runtime mutation = 0
semantic actions = 0
```

The old live plugin remained `e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`; candidate remained not installed; `pendingRollover=false`; fresh Task-245 preflight must re-prove all live state.

## Exact executable candidate

```text
candidate SHA = 18a51b15768fb3d2196e65f1ef470c34aeef7f36
plugin fingerprint = 1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f
public v0.9.3 = 26ce64a624255278a3a0266ad38746e0e6ed2e31 (immutable)
```

Task 245 must fresh-prove all three exact-candidate Actions before live mutation.

## Active Task 245

Execute:

`docs/operations/coordination/tasks/CNX-20260904-245-task244-manifest-bound-exact-candidate-windows-install-over-requalification.md`

Required flow:

```text
fresh GitHub/candidate authority
-> fresh detached exact source
-> fresh read-only live inventory
-> derive current installer state machine
-> create fresh manifest-aware hardened runner
-> direct harmless nonzero + launch-exception qualification
-> freeze/hash runner
-> create/hash/freeze production launch manifest
-> manifest proves child -File == exact candidate scripts/install.ps1
-> register one unique installer Scheduled Task
-> pre-start task readback + runner/manifest rehash
-> re-prove manifest child -File binding
-> start once only if every gate passes
-> classify hardened runner/scheduler result
-> if exit 0, prove plugin/rollover/runtime/DB convergence
-> report
-> STOP for independent review
```

## Manifest-bound topology

Do not pass the nested installer argument vector through Task Scheduler. Scheduler action may reference only:

```text
Windows PowerShell 5.1
+ frozen runner
+ frozen launch manifest
+ evidence root
```

The production launch manifest owns the child executable and distinct child argument array. The unique `-File` value must equal the exact detached candidate `scripts/install.ps1` before start.

## One-shot installer budget

```text
successful Task-245 installer task registrations: 1 maximum
Task-245 installer task starts: 1 maximum
installer child invocations: 1 maximum
retries after start: 0
```

If registration fails before task creation, prove `TaskPresent=false` and STOP. If post-registration binding/readback differs, STOP without update, unregister, repair, or re-registration.

## Semantic zero budget

```text
Dashboard semantic submissions: 0
Discord semantic submissions: 0
direct Discord/API Sends: 0
semantic retries: 0
recovery replay/resend: 0
```

## Preserved evidence

Do not mutate or clean Task-223/237/241/242/243/244 evidence or registered task definitions. Retained Task-237 token: `c6aaf93db7c34f718d01302477a292e1`.

## Hard fences

No reset/uninstall/reinstall sequence, second installer attempt, direct installer fallback, manual plugin replacement, manual rollover prepare/finalize, manual controller/Gateway/lifecycle normalization, manual Ticket/outbox/recovery/SQLite writes, provider/model substitution, process termination to coerce outcome, historical evidence cleanup, release/tag/asset mutation, force push/history rewrite, or semantic message.

## Stop boundary

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260904-245-task244-manifest-bound-exact-candidate-windows-install-over-requalification.md`

Then stop for independent ChatGPT review. Semantic durable-delivery requalification remains a separate successor even if installer PASSes.
