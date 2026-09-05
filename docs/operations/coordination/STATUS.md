# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `TASK255_TASK254_STREAMING_RUNNER_EXACT_CANDIDATE_WINDOWS_INSTALL_OVER_REQUALIFICATION`  
**Updated:** 2026-09-05 ICT  
**Transport:** GitHub repository / Actions authoritative; Task255 authorizes one live installer requalification through the Task254 streaming runner; semantic acceptance remains unauthorized  
**Active task:** `CNX-20260905-255`  
**Parent:** `CNX-20260905-254`  
**Parent umbrella:** `CNX-20260831-188`  
**Disposition:** `TASK254_ACCEPTED_PASS__TARGET_CHILD_IDENTITY_AND_DURABLE_STREAMING_QUALIFIED__ONE_SHOT_LIVE_INSTALL_REQUALIFICATION_AUTHORIZED`

## Accepted Task-254 result

Reviewed report HEAD:

`6fe7e19f22ac586120be351e0ef68e658bf5642e`

Independent review commit:

`04cfa3ede2d21855e8ecdbe1c3a6fdaf79c078fc`

Independent review verdict:

`ACCEPT_PASS_TARGET_CHILD_IDENTITY_BINDING_TDD_REPAIRED__DURABLE_STREAMING_FORENSIC_BOUNDARY_QUALIFIED__ONE_SHOT_LIVE_INSTALL_REQUALIFICATION_AUTHORIZED_SEPARATELY`

Final executable candidate:

`6822af464fe7a5cb3f93305d0263dfc86b56ac68`

Task254 TDD lineage is valid:

```text
cc4d062... opening authority
-> e09c2e8335aeec7ce43ee88a7907c0f8faaabc57 test-only RED
-> 6822af464fe7a5cb3f93305d0263dfc86b56ac68 target-identity repair
-> 6fe7e19f22ac586120be351e0ef68e658bf5642e report only
```

Accepted identities:

```text
streaming runner SHA-256 = 729fba4552e28cd6f53e62f10c8f3bd098d5ca5dfb8d0e3bf4ba3ba1a6250f3e
scripts/install.ps1 SHA-256 = c0779d9bae69d850a44073134e7799a48a1856935b09aae1ae8c7da9f57e0629
plugin fingerprint = 1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f
```

Exact candidate workflows are terminal SUCCESS:

- Validate `33944299263`
- Windows Installer Pack Smoke `33944299239`
- PS5.1 Acceptance Smoke `33944299258`

Task254 remained repository/test-only with all prohibited live effects zero.

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Active Task 255

Execute:

`docs/operations/coordination/tasks/CNX-20260905-255-task254-streaming-runner-exact-candidate-windows-install-over-requalification.md`

Task255 performs one live install-over attempt through the exact Task254 streaming runner.

Mandatory topology:

```text
Task Scheduler
-> Windows PowerShell 5.1
-> exact scripts/manifest-streaming-runner.ps1
-> frozen launch manifest
-> direct Windows PowerShell 5.1 target PID
-> exact detached candidate scripts/install.ps1
```

The evidence root must be durable/non-temp from the beginning. Read back exact runner, manifest, Scheduled Task action, principal, and settings before start.

Keep the known scheduler contract:

```text
ExecutionTimeLimit = PT45M
AllowHardTerminate = true
```

Do not increase timeout. If Task251-like stall recurs, the streaming runner must preserve the last proven stage and actual target PID before the scheduler terminal boundary.

## Cardinality / hard fences

```text
successful installer task registration <= 1
installer task start <= 1
scripts/install.ps1 target start <= 1
retry after start = 0
semantic sends = 0
recovery replay/resend = 0
release/tag mutation = 0
force push/history rewrite = 0
```

On success, prove installed candidate/fingerprint and managed convergence. On nonzero exit, Task250 attestation mismatch, or PT45M termination, preserve evidence and STOP without retry.

## Stop boundary

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260905-255-task254-streaming-runner-exact-candidate-windows-install-over-requalification.md`

Then STOP for independent ChatGPT review. Semantic Dashboard/Discord acceptance remains a separate task even after installer PASS.
