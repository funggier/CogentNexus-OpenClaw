# CNX-20260907-309 — Quiescence release replacement-race repair

## Result

`PASS_SOURCE_REPAIR_EXACT_SHA_CI_GREEN`

Task309 completed its source-only authorization. No installer, managed activation,
Gateway/provider lifecycle, semantic transport, replay/redelivery/disposition,
Ticket/session/database mutation, release/tag/version mutation, or force push was
performed.

## Authority and scope

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Task: `CNX-20260907-309`
- Parent: `CNX-20260907-308`
- Blocked predecessor candidate: `853650ce7f59687fbce172bd96543a38f288e47a`
- Exact repaired candidate: `2215c49a00c6a8fce6f59356c55a80c0a6d25b52`
- Remote branch verification: remote HEAD equals the exact candidate SHA
- Final worktree: clean after report publication

Fresh remote reads of `ACTIVE.md`, `STATUS.md`, and the Task309 specification
confirmed the source-only fence and the report stop gate before publication.

## Root cause and repair

The previous quiescence implementation performed owner/token validation and lease
unlink as separate filesystem operations. A replacement owner could acquire the
lease between those operations, allowing the old owner to unlink the replacement.
The operation lock also originally used unbounded blocking semantics for
`acquire(timeout=...)`, and an absent `release()` created a lock artifact.

The minimal repair in
`skills/cogentnexus-openclaw/scripts/supervisor_quiescence.py`:

- serializes stale reclaim, acquire, owner/token validation, and unlink under a
  cross-process operation lock;
- uses bounded nonblocking platform lock acquisition when `acquire()` has a
  timeout, preserving Busy/Timeout behavior;
- returns from an absent release before creating the lock directory/artifact;
- preserves stale reclaim, idempotent release, owner/token mismatch failure, and
  the existing public return shape.

Production commit summary:

```text
2215c49 fix: serialize quiescence lease operations
1 file changed, 96 insertions(+), 30 deletions(-)
```

## TDD evidence

The genuine RED contract was committed before the repair:

- `49370aa` — `test: reproduce quiescence lease replacement race`
- First RED reproduced the owner-check/unlink replacement race.

Additional regression coverage was kept in separate test-only commits:

- `3b4becd` — bounded lock semantics and absent-release contracts
- `df5b714` — real spawned-process race synchronization
- `821c889` — bounded wait for stale replacement acquisition

Final focused contracts passed:

```text
3 tests in 0.516s — OK
```

The full Python suite passed after the final test correction:

```text
Ran 256 tests in 68.830s
OK (skipped=1)
exit 0
```

The suite emits expected child-process negative-path diagnostics, including an
intentional `unittest ... invalid choice: 'chat.abort'` child diagnostic; the
parent suite remained successful with exit code 0. No test failure was suppressed.

## Independent review

Independent read-only review:

- Delegation: `deleg_bcb3ed31`
- Verdict: `passed=true`
- `security_concerns=[]`
- `logic_errors=[]`
- Reviewer confirmed race closure, bounded positive and zero-timeout behavior,
  side-effect-free absent release, stale reclaim/idempotence, API preservation,
  and Windows/POSIX lock implementation sanity.

A prior review result that reported a replacement `Busy` failure was superseded
by the subsequent test-only correction `821c889`; the fresh full-suite result
above is the authoritative post-correction evidence.

## Local validation

- Focused quiescence contracts: PASS
- Full Python suite: PASS, 256 tests, 1 skipped
- `git diff --cached --check`: PASS
- Production-only secret scan: clean
- Production-only shell/eval scan: clean
- Production source was independently reviewed before commit

## Exact-SHA GitHub Actions

All required workflows were queried by exact `headSha` and reached terminal
success for `2215c49a00c6a8fce6f59356c55a80c0a6d25b52`:

| Workflow | Run | Conclusion | URL |
|---|---:|---|---|
| Validate | 34143434129 | success | https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/34143434129 |
| Windows Installer Pack Smoke | 34143434142 | success | https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/34143434142 |
| PS5.1 Acceptance Smoke | 34143434127 | success | https://github.com/funggier/CogentNexus-OpenClaw/actions/runs/34143434127 |

Fresh final readback showed all three runs `status=completed`,
`conclusion=success`, and the exact repaired candidate in `headSha`.

## Harness anomaly recorded separately

A retained external cross-process probe under
`C:\Users\CDQ-P\AppData\Local\Temp\cnx-release-20260907T134252Z\task309-evidence`
was not used as acceptance evidence after its generated worker invocation
reported an argument-boundary `IndexError`. The repository's actual spawned-process
regression test passed, and the GitHub Windows smoke workflow passed. The anomaly
was retained as harness evidence and did not cause any live mutation or retry.

## Protected/live-state preservation

No protected Ticket or owner session was touched. No semantic send, replay,
redelivery, disposition, `session cancel`, manual SQLite mutation, installer,
`enable`, restart, or release operation occurred after the retained Task308
activation evidence. Task308 live evidence remains predecessor evidence only and
is not being relabeled as proof for the repaired source.

## Stop gate / handoff

Task309 is complete and stops here. A separate successor task must explicitly
authorize fresh exact-candidate supported install and managed activation before
any release work. This report does not authorize those actions.
