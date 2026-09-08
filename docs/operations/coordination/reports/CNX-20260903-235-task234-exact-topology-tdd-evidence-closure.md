# CNX-20260903-235 — Task-234 Exact-Topology TDD Evidence Closure

## Disposition

`PASS_TASK234_TDD_EVIDENCE_CLOSED__EXACT_TOPOLOGY_GREEN`

Repository/evidence hardening is complete. This task did **not** install the
candidate live, send Dashboard or Discord semantic traffic, replay or settle
Task 233, mutate historical forensic evidence, or mutate release/tag/assets.

## Fresh authority and provenance

- Task: `CNX-20260903-235`
- Parent: `CNX-20260903-234`
- Remote authority at opening: `27e34e9f2a45fa3bb5d265cb9908b9cdcd5dcfc7`
- Candidate final HEAD: `ffb0dd4ed47affe2e496c17b74ca74d358905bd7`
- Candidate final remote HEAD: verified equal after publication
- Public `v0.9.3`: `26ce64a624255278a3a0266ad38746e0e6ed2e31` (unchanged)
- Prior Task-234 candidate: `43fd1d6f988431c7a94d24abc8a6811de46f78fa`
- Prior Task-234 payload fingerprint: `964d471f9e330cfeffd270f2200d563dea8c3e7b9252409660df96f1173f58b7`
- Final source plugin fingerprint: `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`
- Fingerprint changed only because Task-235 added the exact-topology test and
  fail-closed contradictory-ingress production fix; package version remains
  `0.9.3`.

## Exact OpenClaw ingress contract

The exact installed dependency was read from the candidate tree:

```text
openclaw 2026.7.1-2
```

The corresponding installed OpenClaw hook documentation identifies
`ctx.messageProvider`, `ctx.channel`, `ctx.channelId`, `ctx.sessionKey`, and
`ctx.runId` as hook-context fields available to channel-originated runs. The
repair uses provider/channel surface identity, never prompt text, browser URL,
`@Ce`, or owner-session syntax as an ingress discriminator.

The implementation now treats recognized provider/channel aliases as follows:

- both absent/unrecognized: no new Dashboard-on-Discord-owner exception;
- one recognized: that recognized surface is used;
- both recognized and equal: that surface is used;
- both recognized but contradictory: `undefined` / fail closed.

This prevents `messageProvider=discord` plus `channel=webchat` from granting
Dashboard staging. Existing no-provider Discord sentinel behavior remains
covered by the prior regression suite.

## Gap A — corrected predecessor RED reconstruction

Disposable worktree:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx235-predecessor-89a0f-20260903T
```

Exact predecessor production SHA:

```text
89a0f539c02dfef971cec9b6baa98a1929d2fb13
```

The corrected production-shaped test was copied into that disposable checkout;
`git diff` showed no production-file change. It used the exact owner:

```text
agent:main:discord:channel:1531199905673252946
```

Command:

```text
npm test -- --run src/task234-dashboard-discord-ingress.test.ts
```

Result:

```text
1 failed / 1 passed
expected undefined to be defined
```

The Dashboard-origin case failed at the intended durable staging boundary while
the paired true Discord-origin negative case passed. The failure was not caused
by missing schema, an un-awaited async hook, malformed run ID, cleanup race, or
syntax/type/build failure.

This reconstruction is evidence only; predecessor history was not rewritten.

## Gap B — exact-topology regression

Test-only RED commit after rebase:

```text
517d555c test: close exact topology settlement evidence
```

The test first exposed the safety defect where contradictory recognized ingress
aliases were treated as Dashboard. The exact failure was:

```text
expected 'TASK235-NO-DASHBOARD ... delivery marker' not to contain
'cogentnexus-openclaw-delivery:'
```

Minimal production repair commit:

```text
ffb0dd4e fix: fail closed on contradictory ingress context
```

The strengthened regression then passed the complete topology:

```text
Dashboard-origin context
-> exact Discord-associated owner retained
-> before_agent_finalize candidate
-> before_message_write marker + durable direct_result pending
-> recovery cannot claim/regenerate while native ownership is pending
-> native transcript update
-> row delivered
-> Ticket completed
-> exactly one delivery_confirmed
-> no direct_redelivery_timeout
-> duplicate transcript does not duplicate confirmation
```

The same owner with true Discord origin remains outside Dashboard staging, and
contradictory `messageProvider=discord` / `channel=webchat` also remains outside
Dashboard staging.

## Validation on final candidate

- Targeted exact-topology and required boundary suite: **8 files / 25 tests passed**
- Full plugin suite: **58 test files / 284 tests passed**
- Python validation via project dependencies and `PYTHONPATH=.`:
  **504 passed, 5 skipped, 4 subtests passed**
- Python compile and POSIX checks: **PASS**
- `npm run build`: **PASS**
- `npm run evaluation`: **PASS**, all gates true
- `npm run plugin:validate`: **PASS**
- `npm audit --omit=dev`: **0 vulnerabilities**
- `npm pack --dry-run`: **PASS**, package version `0.9.3`, 196 files
- `git diff --check`: **PASS**

No timeout was increased. The previously observed Task-233
`v093-response-ready-boundary` timeout remained non-reproducing.

## Earlier exact candidate CI authority retained

The parent Task-234 candidate Actions were independently verified on exact
SHA `43fd1d6f988431c7a94d24abc8a6811de46f78fa`:

- Validate `33760819493`: **SUCCESS**
- Windows Installer Pack Smoke `33760819324`: **SUCCESS**
- PS5.1 Acceptance Smoke `33760819312`: **SUCCESS**

Task 235 made repository/test hardening changes after those runs. No workflow
was manually dispatched during Task 235. A fresh final-SHA CI run is required
before any future live-install authority; this task stops before that live gate
and does not claim live acceptance.

## Changed files and scope

Relative to remote opening authority `27e34e9f...`, final Task-235 product/test
diff is exactly:

```text
A plugins/cogentnexus-openclaw/src/task235-exact-topology.test.ts
M plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts
```

The coordination report is the only additional file in the later report-only
publication commit.

## Retry and live-mutation ledger

```text
Dashboard semantic Sends: 0
Discord-origin semantic Sends: 0
direct operator Sends: 0
semantic retries: 0
recovery replay/resend: 0
manual Ticket/outbox/recovery/SQLite writes: 0
installer/reset/uninstall/reinstall: 0
manual lifecycle/Gateway mutation: 0
live plugin mutation: 0
provider/model substitution: 0
process termination: 0
Task-223/Task-233 forensic evidence mutation: 0
Release/tag/asset mutation: 0
force push/history rewrite: 0
```

## Stop boundary

Task 235 is complete. Stop for independent ChatGPT review. Do not automatically
install/retest live, send semantic traffic, replay or settle Task 233, clean
historical evidence, mutate public release/tag/assets, or begin another
acceptance turn.
