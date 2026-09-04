# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK251_TASK250_EXACT_CANDIDATE_WINDOWS_INSTALL_OVER_REQUALIFICATION`
Current disposition: `TASK250_ACCEPTED_PASS__EXACT_HASH_INPUT_SNAPSHOT_DIAGNOSTIC_GREEN__ONE_LIVE_INSTALL_REQUALIFICATION_AUTHORIZED`
Task ID: `CNX-20260904-251`
Parent task: `CNX-20260904-250`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-04 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / independent reviewer: ChatGPT

## Accepted Task-250 result

Independent review verdict:

`ACCEPT_PASS_EXACT_HASH_INPUT_SNAPSHOT_DIAGNOSTIC_TDD__TASK226_FAIL_CLOSED_PRESERVED__EXACT_CANDIDATE_READY_FOR_ONE_LIVE_INSTALL_REQUALIFICATION`

Reviewed report HEAD:

`e6e971211cec36af80c66ca3c1f8726ec89d2392`

Review commit:

`86f7596f7f2836744b2f653b1deda0174090fe5d`

Exact candidate:

`9c3c4e0fe0afbedf9233c25c0dd36e4209fb9d96`

Expected plugin fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Exact candidate deployment gates are terminal SUCCESS:

```text
Validate                      33896622009
Windows Installer Pack Smoke 33896622084
PS5.1 Acceptance Smoke        33896621985
```

Task 250 preserves Task-226 fail-closed full-tree attestation and adds bounded per-path diagnostic evidence from the exact source/backup snapshots that produced the compared hashes.

## Active Task 251

Execute:

`docs/operations/coordination/tasks/CNX-20260904-251-task250-exact-candidate-windows-install-over-requalification.md`

Required flow:

```text
fresh GitHub authority
-> exact detached checkout of 9c3c4e0...
-> prove clean exact source + installer hash + plugin fingerprint
-> read-only Windows preflight + delivery/recovery hazard gate
-> register/start authenticated Scheduled Task
-> exactly one installer invocation
-> retry gate closes at product start
-> if attestation mismatch recurs, preserve complete Task250 diagnostic and STOP
-> if install succeeds, prove exact installed identity + managed convergence + health
-> report
-> STOP for independent review
```

## Hard fences

```text
installer successful starts <= 1
installer invocations <= 1
installer retries after start = 0
manual plugin/lifecycle/DB repair = 0
Dashboard/Discord/API semantic sends = 0
recovery replay/resend = 0
reset/uninstall/fresh reinstall = 0
release/tag mutation = 0
production/source/test/workflow edits = 0
force push/history rewrite = 0
```

Installer-owned rollover/plugin replacement and normal installer-owned lifecycle convergence are the only authorized live mutations.

Do not weaken or bypass a full-tree mismatch. If the mismatch recurs, retain the exact `diagnostic=` JSON emitted by Task 250 and do not rerun the installer.

## Stop boundary

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260904-251-task250-exact-candidate-windows-install-over-requalification.md`

Then STOP for independent ChatGPT review. Semantic durable-delivery acceptance remains a separate future task even if Task 251 passes.
