# Review — CNX-20260827-097

Decision: `ACCEPT`

Disposition:

`ACCEPT_BLOCKER_STATE_UNVERIFIED_UI_RETRY_DUPLICATED_FRESH_SESSION_ENTRY`

## Independent review

Task 097 publication fence is valid: coordination execution HEAD `f3a6bb9783d508a2b7d57162728018b7955d4b81` -> report HEAD `41a119b686daa4fc64b8f8481329a1be78462641` is exactly one commit and adds only the Task-097 report.

The report establishes that the authenticated Dashboard/control surface was reachable and visibly ready before the New Session interaction. MANAGED generation 24, installed fingerprint `df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`, SQLite integrity, Ticket count 1, outbox 0, event count 7 and retired Task-092 evidence were stable before the interaction.

The decisive blocker is operational input correlation, not semantic/provider behavior. The first background New Session click returned `unverifiable`; an immediate foreground re-issue was then performed under the task's escalation ladder. Fresh state subsequently showed two newly created `agent:main:dashboard:...` sessions, demonstrating that the first event was delayed rather than absent and that the re-issue duplicated the state transition.

The strict Task-097 contract authorized one New Session transition only, so the readiness token cannot be issued from this run. No message was sent, no provider inference occurred, no Ticket/outbox/event mutation attributable to Task 097 occurred, and live MANAGED/plugin/SQLite state remained unchanged.

This does not justify a product-source repair by itself. It does justify revising the coordination retry policy so transient or `unverifiable` UI/tool results are not immediately re-issued when the first attempt may still be in flight.

## Retry-policy design gate

A successor may use a bounded retry only after operator approval of a state-gated retry policy. The recommended rule is:

- read-only operations may retry up to two additional times when they have no mutation side effect;
- state-changing but low-impact operations may retry at most once, only after a bounded grace period and a fresh state probe proves the first attempt produced no effect;
- if the first attempt's side effect is observed, treat it as completed and never retry;
- if state is ambiguous or partially mutated, stop rather than retry;
- semantic sends, provider calls, install/uninstall/reset, irreversible cleanup and other externally visible/non-idempotent effects remain single-attempt unless a task-specific idempotency proof explicitly authorizes otherwise;
- every retry must record attempt number, reason, pre-retry state and proof of retry eligibility.

No final semantic attempt is authorized by this review. The two empty sessions created by Task 097 remain untouched; no cleanup is authorized merely to normalize the evidence.
