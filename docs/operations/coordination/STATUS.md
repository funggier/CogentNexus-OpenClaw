# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Updated:** 2026-08-27 ICT
**Transport:** GitHub repository history
**Human authority:** operator authorized bounded diagnosis/repair of the Dashboard input-focus boundary and continuation through final authenticated semantic acceptance once a reproducible method is proven
**Execution trigger:** manual Hermes continuation; scheduled execution remains disabled

## Accepted live baseline

Task 096 live deployment remains accepted.

Exact installed source:

`32212a4331e1f32b5a130bd30d271d4cbc56f6c1`

Accepted plugin fingerprint:

`df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`

Live state remains MANAGED generation 24 with one candidate-exact canonical plugin generation, healthy startup/Supervisor/Gateway/SQLite/Ollama, preserved Task-092 retired evidence and accepted `NO_FLASH_MULTI_TICK_REPROVEN`.

## Task 100 result and review

Task 100 report:

`8ad8377750f72fcee69c78fa26a199233f997b5f`

Independent decision: `ACCEPT`

Disposition:

`ACCEPT_BLOCKER_WINDOWS_FOREGROUND_INPUT_OWNERSHIP`

Task 100 publication is one report-only commit from execution `0ac2655418cee76c7de8058f77cd22c29cf931cd`.

Task 100 correctly correlated the target session, Firefox window and accessibility composer but could not safely type the sentinel because the exact Firefox/OpenClaw window did not own Windows foreground input focus. Both sentinel attempts left the composer empty and produced no Ticket/provider/delivery effect.

Root-cause class:

`WINDOWS_FOREGROUND_INPUT_OWNERSHIP_NOT_DETERMINISTIC`

The operator clarified that the earlier successful manual/Codex test occurred while a newly opened Firefox window still naturally owned focus. This explains why the same click/keyboard sequence was timing-dependent.

## Active Task 101

[`tasks/CNX-20260827-101-focus-independent-dashboard-input-and-final-semantic-acceptance.md`](tasks/CNX-20260827-101-focus-independent-dashboard-input-and-final-semantic-acceptance.md)

Execution mode:

`LIVE_BOUNDED_INPUT_ROOT_CAUSE_AND_FINAL_SEMANTIC_ACCEPTANCE`

Authorization:

`TASK100_ACCEPTED_OPERATOR_AUTHORIZED_BOUNDED_INPUT_REPAIR_AND_TEST`

Task 101 must test a bounded method ladder and must report which method works or, for each failure, the exact problem and next tested fix:

1. UI Automation / Accessibility direct-edit of the exact `Message Assistant` composer without global keyboard focus;
2. deterministic Win32 foreground/input-thread handoff, requiring fresh target HWND and exact foreground equality before keystrokes;
3. one controlled dedicated Firefox window as a positive-control fallback reproducing the earlier natural-focus condition, still requiring foreground verification.

Each method may use a unique non-sent sentinel and one state-gated retry. A failed method may advance to the next only after the composer is verified empty and durable semantic state unchanged.

The report must contain:

`Input method diagnosis and results`

For a passing method it must additionally contain:

`Known-working Dashboard input method`

Required input proof token:

`DASHBOARD_INPUT_METHOD_REPRODUCIBLY_PROVEN`

If all bounded methods fail:

`BLOCKED_ALL_BOUNDED_DASHBOARD_INPUT_METHODS`

## Final semantic contract

After and only after an input method is proven:

- create one new `CNXSEM5-...` nonce;
- put the exact complete prompt in the verified composer with the same proven method;
- Send exactly once, no resend;
- exactly one new Ticket and route before provider;
- exactly one correlated `ollama/qwen3.5:9b` call;
- an active correlated provider call may be observed read-only for up to 25 minutes without changing timeout/model or resending;
- exact durable final payload staging must precede/meet native delivery boundary;
- exactly one visible nonce;
- exact lifecycle `response_ready -> delivery_confirmed -> completed`;
- no duplicate semantic effect;
- post-completion New Session continuity with zero additional semantic/provider effect.

Required final PASS token:

`PASS_FINAL_AUTHENTICATED_FRESH_SESSION_SEMANTIC_ACCEPTED`

## Retry policy

Read-only operations may use up to 3 attempts where useful.

Within each low-impact pre-send method family: maximum 2 attempts total, with a grace interval and fresh proof before attempt 2. A late effect is success/no retry; ambiguous partial effect blocks retry.

Final semantic Send is single-attempt for the entire task.

## Hard fence

No sent sentinel, historical nonce reuse, second final semantic Send, CLI/channel owner substitute, direct provider probe, synthetic Ticket, install/reset/repair/cleanup, maintained product-source change, product/runtime/config/SQLite mutation, provider/model/timeout change, restart/reboot, merge/tag/release or force push is authorized.

Ephemeral UIA/Win32 helpers outside the repo are allowed for this operational test and must not expose secrets or be committed as product code.

Credential values remain private and must not be read, copied, printed, logged, requested or re-entered by the executor.
