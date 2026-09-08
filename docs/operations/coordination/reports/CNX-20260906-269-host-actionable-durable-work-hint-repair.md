# CNX-20260906-269 — Host Actionable Durable-Work Hint Repair

## Disposition

**PASS — source repair, regression coverage, local validation, and exact-SHA CI completed.**

The Host supervisor now wakes the heavy reconciliation path for durable work that is actionable under the current ownership, freshness, generation, due-time, and model-call contracts, rather than for stored nonterminal Direct state alone.

## Authority and scope

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Task: `CNX-20260906-269`
- Parent: `CNX-20260905-268`
- Final candidate: `08a25a66b17ccea73f22fde6ca00ccdd63fe15e4`
- Scope: source/tests/docs/CI only
- No installed runtime or live OpenClaw state was changed.

## Root cause

Task268 established that the one-minute supervisor process wave aligned with the user's APPSTARTING cursor symptom. Source review showed that the Host fast path was bypassed whenever `durable_work_hint(root)` returned true.

The old implementation treated any nonterminal Ticket and broad Direct-recovery states as actionable. That disagreed with the accepted Direct-recovery eligibility contract, which requires an accepted Direct-lane Ticket, active exact owner generation, fresh owner session, due retry time, and no active/recovering model call.

The stale live Ticket/recovery was not changed. It remained evidence of the false wake condition.

## Implementation

Changed:

- `skills/cogentnexus-openclaw/scripts/host_v091.py`

The read-only `durable_work_hint()` now:

1. accepts an optional deterministic `now` for testing;
2. preserves explicit workflow actionability;
3. preserves pending outbox, assistant delivery, and context-maintenance signals;
4. evaluates Direct recovery only when:
   - recovery state is `pending`;
   - Ticket status is `accepted`;
   - `workflow_eligible=0` and `workflow_id IS NULL`;
   - owner session is `active`;
   - session generation equals recovery owner generation;
   - session `updated_at` is within 15 minutes;
   - `next_attempt_at` is due or null;
   - no model call for the Ticket is `active` or `recovering`;
5. preserves legacy-schema behavior when the newer ownership columns do not exist;
6. continues to fail toward the bounded recovery path on SQLite lock/schema uncertainty.

The supervisor cadence and hard-hang recovery order were not changed.

## TDD evidence

### RED

Regression tests were added before production repair and committed as:

- RED commit: `518e6aaa401b0031bf630566551bffe994d4ed3e`
- Initial focused result: `9 errors, 1 failure`
- The failures demonstrated the missing `now` contract and, importantly, that stale Direct state still forced the heavy path.

### GREEN

New actionability suite plus existing Host tests:

- focused result: `16/16 passed`
- Host/Direct-recovery surface: `28/28 passed`
- `py_compile`: passed
- `git diff --check`: passed

The first exact-SHA CI run identified one compatibility regression in the pre-existing legacy-schema test. It failed because a `tickets(status)` schema lacks `workflow_eligible` and `workflow_id`, causing the broad SQLite exception fallback to return true for an otherwise terminal database.

The corrective fix preserved the legacy nonterminal fallback and the narrow legacy `awaiting_delivery` fallback, while retaining strict actionability for the current schema.

## Corrective validation

After the compatibility fix:

- local full Python suite: `527 passed, 5 skipped, 4 subtests passed`
- corrective commit: `08a25a66b17ccea73f22fde6ca00ccdd63fe15e4`

## Exact-SHA GitHub Actions

All required workflows completed successfully against the exact final candidate SHA `08a25a66b17ccea73f22fde6ca00ccdd63fe15e4`:

| Workflow | Run | Result |
|---|---:|---|
| Validate | `33983861309` | `success` |
| PS5.1 Acceptance Smoke | `33983861333` | `success` |
| Windows Installer Pack Smoke | `33983861332` | `success` |

The first candidate's failed Validate run was:

- SHA: `454643bf3615f8cec88cc9b64566ae9e243ad2f5`
- Run: `33983265719`
- Result: `failure`
- First failure: `V091IdleRecoveryHintTests.test_terminal_database_is_idle`
- CI summary: macOS `491 passed, 1 failed, 40 skipped`; Windows `528 passed, 1 failed, 3 skipped`

The two non-Validate workflows for that first candidate passed, but the candidate was not accepted. No heartbeat commit was made. The final corrective candidate was pushed and all three workflows passed.

## Safety and hard fences

```text
installer/install-over/uninstall/reset           = 0
Gateway/provider/service lifecycle mutation      = 0
live OpenClaw session delete/reset                = 0
live Discord/Dashboard/API semantic send         = 0
manual live Ticket/session/SQLite mutation       = 0
recovery replay/redelivery/disposition            = 0
Scheduled Task enable/disable/create/delete/run   = 0
stop/kill/restart unrelated live processes        = 0
release/tag/default-branch promotion              = 0
force push/history rewrite                       = 0
```

The installed payload was not updated. The open `ollama:1` recovery incident, old Ticket/recovery boundary, and future live acceptance remain separately gated.

## Required next step

Set `ACTIVE.md` and `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW`, then stop project mutation. ChatGPT must independently review this report. Do not perform installed deployment or live acceptance from this task.

Credentials and secret values are not included in this report.
