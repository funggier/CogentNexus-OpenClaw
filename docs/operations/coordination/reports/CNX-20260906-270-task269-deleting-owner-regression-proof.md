# CNX-20260906-270 — Task269 Deleting-Owner Regression Proof

## Disposition

`PASS__TEST_CONTRACT_CLOSED`

Task270 closed the single missing Task269 safety-proof case. The change is test-only; production source remains unchanged.

## Scope and authority

- Task: `CNX-20260906-270`
- Parent: `CNX-20260906-269`
- Exact source/test candidate: `6a491d1a95394bba7b70735fbaf9cebf4d619ea6`
- Publication commit: the commit containing this report and coordination handoff
- Executor: `Hermes`
- Independent reviewer: `ChatGPT`

No installer, runtime lifecycle, live DB, session, semantic-send, Scheduled Task, process, release, or force-push action was authorized or performed.

## Implemented proof

Added to `tests/test_host_v091_actionability.py`:

1. `test_deleting_owner_does_not_wake`
   - accepted Direct-lane Ticket (`workflow_eligible=0`, `workflow_id IS NULL`);
   - pending Direct recovery;
   - exact owner generation;
   - fresh owner session;
   - due retry;
   - owner session state `deleting`;
   - asserts `durable_work_hint()` is `False`.

2. `test_supervisor_healthy_deleting_direct_state_stays_idle`
   - uses the same deleting-owner Direct shape;
   - stubs healthy Gateway/provider probes;
   - replaces the legacy heavy supervisor with a failure assertion;
   - asserts `supervisor_tick(...)["result"] == "idle"`.

Production file `skills/cogentnexus-openclaw/scripts/host_v091.py` has no diff in this task. The existing `s.state='active'` predicate therefore remains the production safety boundary, now explicitly covered for the transient `deleting` state.

## Validation

- Focused actionability suite: `12 tests`, all passed.
- Host discovery (`test_host_v091*.py`): `30 tests`, all passed.
- Idle recovery hint suite: `8 tests`, all passed.
- Full Python suite: `529 passed, 5 skipped, 4 subtests passed` in `119.23s`.
- `py_compile tests/test_host_v091_actionability.py`: passed.
- `git diff --check`: passed.
- Production source diff: empty.

## Exact-SHA CI

All runs were bound to `6a491d1a95394bba7b70735fbaf9cebf4d619ea6`:

| Workflow | Run | Result |
|---|---:|---|
| PS5.1 Acceptance Smoke | `33998510050` | success |
| Windows Installer Pack Smoke | `33998510053` | success |
| Validate, initial attempt | `33998510062`, attempt 1 | failure — unrelated `src/ticket-runtime.test.ts` timeout on `windows-latest, 3.14` |
| Validate, bounded rerun | `33998510062`, attempt 2 | success |

The initial Validate failure was not a Task270 test failure: the failed test was the pre-existing `dispatches nothing for a zero or invalid limit and enforces the hard ceiling of 32`, which timed out at 20 seconds. Local full Python validation was green. One bounded rerun of the failed Validate workflow was performed; it passed. No blind repeated reruns were made.

## Hard-fence ledger

```text
installer/install-over/uninstall/reset           = 0
Gateway/provider/service lifecycle mutation      = 0
live OpenClaw session delete/reset                = 0
live Discord/Dashboard/API semantic send         = 0
manual live Ticket/session/SQLite mutation       = 0
recovery replay/redelivery/disposition            = 0
Scheduled Task enable/disable/create/delete/run   = 0
stop/kill/restart unrelated live processes        = 0
release/tag/default-branch promotion             = 0
force push/history rewrite                       = 0
```

Old Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` was not accessed for mutation.

## Handoff

After publication, `ACTIVE.md` and `STATUS.md` are set to `WAITING_FOR_CHATGPT_REVIEW`. Hermes stops mutation and does not independently accept this report.
