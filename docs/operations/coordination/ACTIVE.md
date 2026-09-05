# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TASK256_CANONICAL_IDENTITY_RECONCILED_WINDOWS_INSTALL_OVER_REQUALIFICATION`
Current disposition: `TASK255_ACCEPTED_BLOCKED__CANONICAL_VS_CRLF_CONTRACT_DEFECT_PROVEN__TASK256_RECONCILED_AUTHORIZED`
Task ID: `CNX-20260905-256`
Parent task: `CNX-20260905-255`
Parent umbrella: `CNX-20260831-188`
Updated: 2026-09-05 ICT
Executor: Hermes / authenticated Windows operator
Coordinator / independent reviewer: Musethree

## Accepted Task-255 result

Reviewed report HEAD:

`df2cf38b27dbb1c5beefcde6f46739d3cb37f7b9`

Independent review:

`docs/operations/coordination/reviews/CNX-20260905-255-task254-streaming-runner-exact-candidate-windows-install-over-requalification-review.md`

Independent review verdict:

`ACCEPT_BLOCKED_PREFLIGHT_DRIFT__FAIL_CLOSED_CORRECT__IDENTITY_CONTRACT_DEFECT_CANONICAL_VS_CRLF_PROVEN__SUCCESSOR_AUTHORIZED_SEPARATELY`

Task255 fail-closed is accepted: the one-shot installer was correctly never
started (`registrations = 0`, `starts = 0`, `scripts/install.ps1 starts = 0`,
`retries = 0`, `semantic sends = 0`). The report's "not a line-ending artifact"
sentence is corrected: the mismatch is precisely LF-vs-CRLF variance, proven by
exact in-memory reproduction (`31983` canonical bytes vs `32568` materialized =
`+585` for `585` LF lines).

Reconciled exact executable candidate:

`6822af464fe7a5cb3f93305d0263dfc86b56ac68`

Reconciled identities (canonical Git bytes authoritative):

```text
streaming runner SHA-256 (canonical) = 729fba4552e28cd6f53e62f10c8f3bd098d5ca5dfb8d0e3bf4ba3ba1a6250f3e
scripts/install.ps1 SHA-256 (canonical triple-proven) = 9d53a42794e0052a817a9f7dd60d0e5895b75882f62261e08427ee414e17b57b
scripts/install.ps1 SHA-256 (CRLF-materialized, diagnosis only, never a gate) = c0779d9bae69d850a44073134e7799a48a1856935b09aae1ae8c7da9f57e0629
plugin fingerprint = 1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f
```

Root cause: `c0779d...` was first recorded in Task247 (`8cbbe2d`) from Windows
materialized (CRLF) working-tree bytes and forwarded through Task248/250/253/254
into the Task255 contract. Canonical bytes were stable (`e09c2e8` through
`6822af4` both hash to `9d53a427...`). No product content drift occurred.

## Active Task 256

Execute:

`docs/operations/coordination/tasks/CNX-20260905-256-task255-canonical-identity-reconciled-windows-install-over-requalification.md`

Required flow:

```text
fresh GitHub authority
-> fresh detached exact candidate checkout (core.autocrlf=false)
-> canonical triple proof (git show + working tree + raw GitHub bytes = 9d53a427...)
-> CRLF digest recorded separately, never used as gate
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

This is a new authority with reconciled identity, not a retry of Task255.

Known scheduler settings remain:

```text
ExecutionTimeLimit = PT45M
AllowHardTerminate = true
```

Do not increase the timeout in this task. A repeated stall must be diagnosed by
the Task254 streaming evidence boundary.

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

Do not weaken Task226/250 full-tree attestation. If mismatch recurs, preserve
the exact `diagnostic=` payload and STOP.

## Stop boundary

Hermes must publish:

`docs/operations/coordination/reports/CNX-20260905-256-task255-canonical-identity-reconciled-windows-install-over-requalification.md`

Then STOP for independent review. Even if installer requalification passes,
semantic acceptance requires a separate successor task.
