# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Execution mode:** `TASK256_CANONICAL_IDENTITY_RECONCILED_WINDOWS_INSTALL_OVER_REQUALIFICATION`
**Updated:** 2026-09-05 ICT
**Transport:** GitHub repository / Actions authoritative; Task256 authorizes one live installer requalification with reconciled canonical identity through the Task254 streaming runner; semantic acceptance remains unauthorized
**Active task:** `CNX-20260905-256`
**Parent:** `CNX-20260905-255`
**Parent umbrella:** `CNX-20260831-188`
**Disposition:** `TASK255_ACCEPTED_BLOCKED__CANONICAL_VS_CRLF_CONTRACT_DEFECT_PROVEN__TASK256_RECONCILED_AUTHORIZED`

## Accepted Task-255 result

Reviewed report HEAD:

`df2cf38b27dbb1c5beefcde6f46739d3cb37f7b9`

Independent review:

`docs/operations/coordination/reviews/CNX-20260905-255-task254-streaming-runner-exact-candidate-windows-install-over-requalification-review.md`

Independent review verdict:

`ACCEPT_BLOCKED_PREFLIGHT_DRIFT__FAIL_CLOSED_CORRECT__IDENTITY_CONTRACT_DEFECT_CANONICAL_VS_CRLF_PROVEN__SUCCESSOR_AUTHORIZED_SEPARATELY`

Task255 correctly never started the installer. Cardinality proven zero across
registration/start/target-start/retry and semantic sends. The mismatch is proven
to be canonical-LF (`9d53a427...`, `31983` B) vs CRLF-materialized (`c0779d...`,
`32568` B, `+585`) variance — not product content drift.

Final executable candidate (unchanged):

`6822af464fe7a5cb3f93305d0263dfc86b56ac68`

Task254 TDD lineage remains valid:

```text
cc4d062... opening authority
-> e09c2e8335aeec7ce43ee88a7907c0f8faaabc57 test-only RED
-> 6822af464fe7a5cb3f93305d0263dfc86b56ac68 target-identity repair (runner only)
-> 6fe7e19f22ac586120be351e0ef68e658bf5642e report only
-> 04cfa3e independent review
-> 1da7174/25e54ac/7cd240d Task255 open/activate/align
-> df2cf38 Task255 report (BLOCKED_PREFLIGHT_DRIFT, fail-closed correct)
```

Reconciled identities (canonical authoritative):

```text
streaming runner SHA-256 (canonical) = 729fba4552e28cd6f53e62f10c8f3bd098d5ca5dfb8d0e3bf4ba3ba1a6250f3e
scripts/install.ps1 SHA-256 (canonical triple-proven) = 9d53a42794e0052a817a9f7dd60d0e5895b75882f62261e08427ee414e17b57b
scripts/install.ps1 SHA-256 (CRLF-materialized, diagnosis only) = c0779d9bae69d850a44073134e7799a48a1856935b09aae1ae8c7da9f57e0629
plugin fingerprint = 1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f
```

Exact candidate workflows are terminal SUCCESS (re-verified via Checks API,
nine check-runs; HEAD workflows green).

Task255 remained fail-closed with all prohibited live effects zero.

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Active Task 256

Execute:

`docs/operations/coordination/tasks/CNX-20260905-256-task255-canonical-identity-reconciled-windows-install-over-requalification.md`

Task256 performs one live install-over attempt through the exact Task254
streaming runner under the reconciled canonical gate. This is a new authority,
not a Task255 retry.

Mandatory topology:

```text
Task Scheduler
-> Windows PowerShell 5.1
-> exact scripts/manifest-streaming-runner.ps1
-> frozen launch manifest
-> direct Windows PowerShell 5.1 target PID
-> exact detached candidate scripts/install.ps1 (canonical 9d53a427...)
```

The evidence root must be durable/non-temp from the beginning. Read back exact
runner, manifest, Scheduled Task action, principal, and settings before start.
Require `core.autocrlf=false` triple proof and dual recording (canonical gate +
materialized note).

Keep the known scheduler contract:

```text
ExecutionTimeLimit = PT45M
AllowHardTerminate = true
```

Do not increase timeout. If Task251-like stall recurs, the streaming runner must
preserve the last proven stage and actual target PID before the scheduler
terminal boundary.

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

On success, prove installed candidate/fingerprint and managed convergence. On
nonzero exit, Task250 attestation mismatch, or PT45M termination, preserve
evidence and STOP without retry.

## Stop boundary

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260905-256-task255-canonical-identity-reconciled-windows-install-over-requalification.md`

Then STOP for independent review. Semantic Dashboard/Discord acceptance remains
a separate task even after installer PASS.
