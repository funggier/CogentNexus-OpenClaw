# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK255_TASK254_STREAMING_RUNNER_EXACT_CANDIDATE_WINDOWS_INSTALL_OVER_REQUALIFICATION`
Current disposition: `TASK254_ACCEPTED_PASS__TARGET_CHILD_IDENTITY_AND_DURABLE_STREAMING_QUALIFIED__ONE_SHOT_LIVE_INSTALL_REQUALIFICATION_AUTHORIZED`
Task ID: `CNX-20260905-255`
Parent task: `CNX-20260905-254`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-05 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / independent reviewer: ChatGPT

## Accepted Task-254 result

Reviewed report HEAD:

`6fe7e19f22ac586120be351e0ef68e658bf5642e`

Independent review commit:

`04cfa3ede2d21855e8ecdbe1c3a6fdaf79c078fc`

Independent review verdict:

`ACCEPT_PASS_TARGET_CHILD_IDENTITY_BINDING_TDD_REPAIRED__DURABLE_STREAMING_FORENSIC_BOUNDARY_QUALIFIED__ONE_SHOT_LIVE_INSTALL_REQUALIFICATION_AUTHORIZED_SEPARATELY`

Accepted exact executable candidate:

`6822af464fe7a5cb3f93305d0263dfc86b56ac68`

Accepted identities:

```text
streaming runner SHA-256 = 729fba4552e28cd6f53e62f10c8f3bd098d5ca5dfb8d0e3bf4ba3ba1a6250f3e
scripts/install.ps1 SHA-256 = c0779d9bae69d850a44073134e7799a48a1856935b09aae1ae8c7da9f57e0629
plugin fingerprint = 1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f
```

Task254 proved actual target PID binding, invalid-target no-child-start evidence, durable stdout/stderr while target is alive, forced outer-runner termination preservation, exact nonzero exit, and quoting-edge argument binding. Exact candidate Validate / Windows Installer Pack Smoke / PS5.1 Acceptance Smoke are terminal SUCCESS.

## Active Task 255

Execute:

`docs/operations/coordination/tasks/CNX-20260905-255-task254-streaming-runner-exact-candidate-windows-install-over-requalification.md`

Required flow:

```text
fresh GitHub authority
-> fresh detached exact candidate checkout
-> prove runner/installer/plugin identities
-> read-only live preflight
-> create durable non-temp evidence root
-> freeze manifest
-> register one Scheduled Task with runner+manifest only
-> prove action/principal/PT45M readback
-> one start / one installer target start maximum
-> streaming observation
-> success: prove installed candidate + managed convergence
   OR
-> failure/timeout: preserve exact last stage + target PID + streaming evidence and STOP
-> semantic sends remain zero
-> report
-> STOP for independent review
```

Known scheduler settings remain:

```text
ExecutionTimeLimit = PT45M
AllowHardTerminate = true
```

Do not increase the timeout in this task. A repeated stall must be diagnosed by the Task254 streaming evidence boundary.

## Cardinality / hard fences

```text
successful installer Scheduled Task registrations <= 1
installer Scheduled Task starts <= 1
actual scripts/install.ps1 target starts <= 1
installer retries after start = 0
Dashboard/Discord/API semantic sends = 0
recovery replay/resend = 0
release/tag mutation = 0
force push/history rewrite = 0
```

Do not weaken Task226/250 full-tree attestation. If mismatch recurs, preserve the exact `diagnostic=` payload and STOP.

## Stop boundary

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260905-255-task254-streaming-runner-exact-candidate-windows-install-over-requalification.md`

Then STOP for independent ChatGPT review. Even if installer requalification passes, semantic acceptance requires a separate successor task.
