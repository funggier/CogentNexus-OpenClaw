# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK251_TASK250_EXACT_CANDIDATE_WINDOWS_INSTALL_OVER_REQUALIFICATION`  
**Updated:** 2026-09-04 ICT  
**Transport:** GitHub repository / Actions authoritative; Task 251 authorizes one bounded exact-candidate Windows install-over only; semantic acceptance remains unauthorized  
**Active task:** `CNX-20260904-251`  
**Parent:** `CNX-20260904-250`  
**Parent umbrella:** `CNX-20260831-188`  
**Disposition:** `TASK250_ACCEPTED_PASS__EXACT_HASH_INPUT_SNAPSHOT_DIAGNOSTIC_GREEN__ONE_LIVE_INSTALL_REQUALIFICATION_AUTHORIZED`

## Accepted Task-250 result

Reviewed report HEAD:

`e6e971211cec36af80c66ca3c1f8726ec89d2392`

Independent review commit:

`86f7596f7f2836744b2f653b1deda0174090fe5d`

Independent review verdict:

`ACCEPT_PASS_EXACT_HASH_INPUT_SNAPSHOT_DIAGNOSTIC_TDD__TASK226_FAIL_CLOSED_PRESERVED__EXACT_CANDIDATE_READY_FOR_ONE_LIVE_INSTALL_REQUALIFICATION`

Exact candidate:

`9c3c4e0fe0afbedf9233c25c0dd36e4209fb9d96`

Expected installed plugin payload fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Exact candidate installer SHA-256:

`c0779d9bae69d850a44073134e7799a48a1856935b09aae1ae8c7da9f57e0629`

Required exact-SHA Actions are terminal SUCCESS:

```text
Validate                      33896622009
Windows Installer Pack Smoke 33896622084
PS5.1 Acceptance Smoke        33896621985
```

Task-250 TDD chronology is accepted: test-only RED `ea5d8446...` is a direct child of the opening authority and production commit `9c3c4e0...` is its direct child. Production changes are limited to `namespace_ownership.py` and preserve Task-226 fail-closed semantics while adding a deterministic bounded delta from the same captured hash-input snapshots.

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Active Task 251

Execute:

`docs/operations/coordination/tasks/CNX-20260904-251-task250-exact-candidate-windows-install-over-requalification.md`

Task 251 must use the Task-237 exact-source topology:

```text
fresh fetch
-> disposable detached checkout exact 9c3c4e0...
-> prove clean exact source/fingerprint/installer hash
-> read-only live preflight and delivery/recovery hazard gate
-> authenticated Scheduled Task
-> exactly one installer invocation
-> close installer retry gate at product start
```

If the Task-248 attestation mismatch recurs, Task 251 must retain the complete raw child diagnostics and exact Task-250 `diagnostic=` JSON generated from the compared snapshots, then stop without installer retry or tree mutation.

If installation succeeds, Task 251 must prove exact installed fingerprint, coherent ownership/generation, managed convergence, Gateway/Ollama health, Delivery READY/pending 0, Recovery READY, SQLite integrity, and semantic submissions = 0.

## Accepted prior live boundary

Tasks 249–250 were read-only/repository-only, so the accepted pre-Task251 live boundary remains the Task-248 failed-install state until fresh Task-251 preflight proves otherwise:

```text
controller = passthrough generation 39
candidate installed = no
live canonical plugin = predecessor e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
Task248 failure = pre-install backup project-tree attestation mismatch
```

Task-249 later found current retired tree and retained Task-248 backup equal at `900ac13f...`, but that was post-failure evidence and must not be treated as proof of historical equality.

## Hard fences

```text
installer successful starts <= 1
installer invocations <= 1
installer execution retries after start = 0
manual plugin/lifecycle/DB repair = 0
Dashboard semantic sends = 0
Discord semantic sends = 0
direct API semantic sends = 0
recovery replay/resend = 0
reset/uninstall/fresh reinstall = 0
release/tag mutation = 0
production/source/test/workflow edits = 0
force push/history rewrite = 0
```

Installer-owned plugin replacement/rollover and normal installer-owned lifecycle convergence are the only authorized live mutations.

## Stop boundary

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260904-251-task250-exact-candidate-windows-install-over-requalification.md`

Then STOP for independent ChatGPT review. Even on PASS, do not perform Dashboard/Discord semantic acceptance, replay/settlement, reset/uninstall/fresh reinstall, or release/tag mutation without a separate successor task.
