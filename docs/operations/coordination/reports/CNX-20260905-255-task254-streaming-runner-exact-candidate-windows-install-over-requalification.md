# CNX-20260905-255 — Task-254 Streaming-Runner Exact-Candidate Windows Install-Over Requalification

## Final disposition

`BLOCKED_PREFLIGHT_DRIFT`

The authorized one-shot installer execution was **not started**. The required exact candidate checkout did not satisfy the Task255 installer-byte identity gate. No registration, Scheduled Task start, installer target start, or live mutation occurred.

## Fresh authority

Fresh remote authority was fetched from `origin/agent/v0.9.3-full-stabilization`. Opening remote HEAD was:

`7cd240d04f6e4ec6017ca314b7c4c36bdbaf05ee`

`ACTIVE.md` and `STATUS.md` both stated `READY_FOR_HERMES` with active task `CNX-20260905-255`. The task authorized one exact-candidate Windows install-over through the Task254 streaming runner, with semantic acceptance still forbidden.

Public tag identity was verified unchanged:

`v0.9.3 = 26ce64a624255278a3a0266ad38746e0e6ed2e31`

## Exact candidate and CI preflight

Required candidate:

`6822af464fe7a5cb3f93305d0263dfc86b56ac68`

A fresh detached clone was created at:

`C:/Users/CDQ-P/AppData/Local/Temp/cnx255-exact-candidate-6822af4`

The clone was checked out with `core.autocrlf=false`, then verified detached, exact, and clean:

```text
HEAD=6822af464fe7a5cb3f93305d0263dfc86b56ac68
VERSION=0.9.3
CANDIDATE_STATUS=clean
```

GitHub Checks API was queried for the exact candidate. All nine observed check-runs were terminal `success`:

| Check | Check-run ID | Conclusion |
|---|---:|---|
| `npm-pack` | `101247485728` | success |
| `package dry-run (no publish)` | `101247485892` | success |
| `serializer` | `101247485787` | success |
| `validate (macos-latest, 3.11)` | `101247486008` | success |
| `validate (macos-latest, 3.14)` | `101247486052` | success |
| `validate (ubuntu-latest, 3.11)` | `101247486003` | success |
| `validate (ubuntu-latest, 3.14)` | `101247486019` | success |
| `validate (windows-latest, 3.11)` | `101247486029` | success |
| `validate (windows-latest, 3.14)` | `101247486055` | success |

## Identity gate and blocker

Required Task255 identities:

```text
required runner SHA-256    = 729fba4552e28cd6f53e62f10c8f3bd098d5ca5dfb8d0e3bf4ba3ba1a6250f3e
required installer SHA-256 = c0779d9bae69d850a44073134e7799a48a1856935b09aae1ae8c7da9f57e0629
required plugin fingerprint = 1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f
```

Observed in the exact detached candidate checkout:

```text
runner SHA-256    = 729fba4552e28cd6f53e62f10c8f3bd098d5ca5dfb8d0e3bf4ba3ba1a6250f3e
installer SHA-256 = 9d53a42794e0052a817a9f7dd60d0e5895b75882f62261e08427ee414e17b57b
```

The installer digest was independently confirmed three ways:

- detached checkout working-tree bytes: `9d53a427...e17b57b`;
- `git show 6822af4:scripts/install.ps1` bytes: `9d53a427...e17b57b`;
- raw GitHub bytes at the exact candidate commit: `9d53a427...e17b57b`.

This is a real candidate-content mismatch, not a line-ending conversion artifact. The required `c0779d...` installer identity is not present in candidate `6822af4...`. Per Task255, any identity mismatch is `BLOCKED_PREFLIGHT_DRIFT`; no alternate candidate, source selector, installer parameter, or retry was permitted.

Identity proof was retained at:

`C:/Users/CDQ-P/AppData/Local/CogentNexus-OpenClaw/forensics/CNX-20260905-255/preflight-identity.txt`

The runner and installer copies/hashes were retained under the same durable evidence root. The expected and observed values are recorded verbatim there.

## Registration/start cardinality

The identity gate failed before live preflight/registration. Read-only check of the intended task name returned:

```text
TaskPresent=False
```

Counts:

```text
successful installer Scheduled Task registrations = 0
installer Scheduled Task starts = 0
actual scripts/install.ps1 target starts = 0
installer retries after start = 0
```

No manifest was frozen for execution and no Scheduled Task action/principal/settings readback was attempted, because the exact executable identity prerequisite was unsatisfied.

## Live/product and semantic effect ledger

No product mutation was performed:

- `scripts/install.ps1` live invocations: `0`
- installer task registration/start: `0`
- rollover prepare/finalize: `0`
- plugin/retired-tree/backup mutation: `0`
- controller/Gateway/provider/model lifecycle mutation: `0`
- Ticket/outbox/recovery/SQLite mutation: `0`
- Dashboard/Discord/direct API semantic sends: `0`
- recovery replay/resend: `0`
- release/tag mutation: `0`
- force-push/history rewrite: `0`

Task248/251 retained forensic evidence was not modified. No process was manually terminated.

## Report publication

This report is the only repository path changed for the publication step. It is published at:

`docs/operations/coordination/reports/CNX-20260905-255-task254-streaming-runner-exact-candidate-windows-install-over-requalification.md`

The live installer requalification must not be retried from this task. A fresh successor authority with reconciled exact installer identity is required.

STOP for independent ChatGPT review.
