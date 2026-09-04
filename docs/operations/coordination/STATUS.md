# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK245_TASK244_MANIFEST_BOUND_EXACT_CANDIDATE_WINDOWS_INSTALL_OVER_REQUALIFICATION`  
**Updated:** 2026-09-04 ICT  
**Transport:** GitHub repository / Actions authoritative; Task 245 authorizes one fresh manifest-bound exact-candidate installer attempt with zero semantic budget  
**Active task:** `CNX-20260904-245`  
**Parent:** `CNX-20260904-244`  
**Runner qualification parent:** `CNX-20260904-243`  
**Installer evidence parents:** `CNX-20260904-241`, `CNX-20260904-244`  
**Candidate-validation parent:** `CNX-20260904-240`  
**Parent umbrella:** `CNX-20260831-188`  
**Disposition:** `TASK244_ACCEPTED_FAIL_CLOSED__INSTALLER_UNEXECUTED__ACTION_BINDING_DEFECT_ISOLATED__ONE_FRESH_MANIFEST_BOUND_INSTALLER_SUCCESSOR_ALLOWED`

## Task-244 accepted result

Reviewed report HEAD:

`2da9be61abd1da7ea36c508af640e1732853e2b1`

Independent review verdict:

`ACCEPT_FAIL_CLOSED_PRESTART_ACTION_BINDING_BLOCK__NO_INSTALLER_OR_PRODUCT_EXECUTION__FRESH_MANIFEST_BOUND_SUCCESSOR_AUTHORIZED`

Task 244 proved the candidate/live preflight remained suitable for a real upgrade, but its registered Scheduled Task was deliberately not started because pre-start readback showed the nested child `-File` binding pointed at `powershell.exe` rather than the detached candidate installer.

Accepted effect boundary:

```text
installer Scheduled Task registrations = 1
installer Scheduled Task starts = 0
installer child invocations = 0
scripts/install.ps1 invocations = 0
rollover/plugin/runtime mutation = 0
semantic actions = 0
```

Report-head Actions are GREEN:

```text
PS5.1 Acceptance Smoke        33872664615 = SUCCESS
Windows Installer Pack Smoke 33872664619 = SUCCESS
Validate                      33872664669 = SUCCESS
```

Task 244 is therefore an accepted fail-closed operator action-binding block, not a product failure.

## Exact executable candidate

```text
candidate SHA = 18a51b15768fb3d2196e65f1ef470c34aeef7f36
plugin fingerprint = 1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f
public v0.9.3 = 26ce64a624255278a3a0266ad38746e0e6ed2e31 (immutable)
```

Task 245 must fetch the three exact-candidate Actions fresh and recompute the fingerprint before any live mutation.

## Active Task 245

Execute:

`docs/operations/coordination/tasks/CNX-20260904-245-task244-manifest-bound-exact-candidate-windows-install-over-requalification.md`

Required topology:

```text
Scheduled Task
-> Windows PowerShell 5.1
-> frozen manifest-aware hardened runner
-> frozen production launch manifest
-> child PowerShell executable + distinct child argument array
-> unique child -File target = exact detached candidate scripts/install.ps1
```

Do not pass the nested installer argument vector through Task Scheduler.

Required flow:

```text
fresh GitHub/candidate authority
-> fresh detached source
-> fresh read-only live state
-> re-derive installer classifier/resolver
-> fresh runner + direct harmless qualification
-> freeze/hash runner
-> production launch manifest + schema/path validation
-> freeze/hash manifest
-> one unique installer Scheduled Task registration
-> pre-start task readback
-> runner/manifest rehash
-> re-prove unique child -File exact binding
-> one start only if every gate passes
-> hardened evidence classification
-> exit 0 only: plugin/rollover/runtime/DB convergence proof
-> report
-> STOP for independent review
```

## One-shot installer budget

```text
successful Task-245 installer task registrations: 1 maximum
Task-245 installer task starts: 1 maximum
installer child invocations: 1 maximum
retries after start: 0
```

Registration failure before creation => prove `TaskPresent=false` and STOP. Post-registration binding mismatch => STOP without task update, unregister, repair, or re-registration.

## Preserved evidence/live boundary

Fresh Windows evidence wins. Task-244 observed old installed plugin fingerprint `e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`, candidate not installed, and `pendingRollover=false`; Task 245 must not assume this remains true.

Do not mutate/delete Task-223/237/241/242/243/244 evidence or task definitions. Retained Task-237 token: `c6aaf93db7c34f718d01302477a292e1`.

## Semantic zero-effect budget

```text
Dashboard semantic submissions: 0
Discord semantic submissions: 0
direct Discord/API sends: 0
semantic retries: 0
recovery replay/resend: 0
```

## Hard fences

No reset/uninstall/reinstall sequence, second installer attempt, direct installer fallback, manual plugin replacement, manual rollover prepare/finalize, manual controller/Gateway/lifecycle normalization, manual Ticket/outbox/recovery/SQLite writes, provider/model substitution, process termination to coerce outcome, historical evidence cleanup, release/tag/asset mutation, force push/history rewrite, or semantic message.

## Stop boundary

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260904-245-task244-manifest-bound-exact-candidate-windows-install-over-requalification.md`

Then stop for independent ChatGPT review. Semantic durable-delivery requalification remains a separate successor even if installer PASSes.
