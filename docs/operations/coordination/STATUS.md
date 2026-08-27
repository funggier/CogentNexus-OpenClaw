# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Updated:** 2026-08-27 ICT
**Transport:** GitHub repository history
**Human authority:** operator requested a new attempt and previously authorized bounded diagnosis/fix/testing of Dashboard target/input boundaries through final authenticated semantic acceptance
**Execution trigger:** manual Hermes continuation; scheduled execution remains disabled

## Accepted live baseline

Task 096 live deployment remains accepted.

Exact installed source:

`32212a4331e1f32b5a130bd30d271d4cbc56f6c1`

Accepted plugin fingerprint:

`df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`

Live state remains MANAGED generation 24 with one candidate-exact canonical plugin generation, healthy startup/Supervisor/Gateway/SQLite/Ollama, preserved Task-092 retired evidence and accepted `NO_FLASH_MULTI_TICK_REPROVEN`.

## Task 101 result and review

Task 101 report:

`d06b1397e032749e5b348d5d1054dc1784d67519`

Independent decision: `ACCEPT`

Disposition:

`ACCEPT_BLOCKER_TARGET_WINDOW_LIFECYCLE_NOT_ESTABLISHED`

Task 101 publication is exactly one report-only commit from execution `ef4e71628c4b4906f0a26ed4f6673241bb9999bc`.

Task 101 performed zero sentinel/input attempts and zero semantic Sends. Fresh inventory contained no Firefox/OpenClaw target window; a prior automation window id was stale. Therefore the UIA/Win32 input ladder never started.

Accepted root-cause boundary:

`DASHBOARD_TARGET_WINDOW_LIFECYCLE_NOT_ESTABLISHED`

## Active Task 102

[`tasks/CNX-20260827-102-reestablish-dashboard-target-and-final-semantic-acceptance.md`](tasks/CNX-20260827-102-reestablish-dashboard-target-and-final-semantic-acceptance.md)

Execution mode:

`LIVE_TARGET_LIFECYCLE_REESTABLISHMENT_INPUT_DIAGNOSIS_AND_FINAL_SEMANTIC_ACCEPTANCE`

Authorization:

`TASK101_ACCEPTED_OPERATOR_REQUESTED_NEW_ATTEMPT`

## Target lifecycle correction

Task 102 must establish the browser target independently of stale automation identifiers and launcher process assumptions.

A Firefox launch may route a `-new-window` request into an existing process and the launching process may terminate. Therefore after any launch/bootstrap Task 102 must rediscover the real top-level browser window from current OS state:

- current Firefox processes;
- visible top-level HWNDs;
- current PID/title/class/visibility;
- fresh UIA/accessibility tree;
- exact Dashboard session state;
- current `Message Assistant` composer.

The exact target must survive a second fresh rediscovery after a stability wait before any sentinel is typed.

Target bootstrap is limited to two state-gated attempts total. Late target appearance means success/no relaunch. Multiple candidates must be disambiguated rather than multiplied.

Required target token:

`DASHBOARD_LIVE_TARGET_REESTABLISHED`

## Input diagnosis after target is live

Authorized method ladder:

1. focus-independent UIA/accessibility direct edit;
2. deterministic Win32 foreground/input-thread handoff with exact foreground equality before keyboard input;
3. controlled natural-focus dedicated Firefox positive control if still safely eligible.

Each method must report its exact capability/failure boundary, tested hypothesis/fix and outcome. Each uses a unique non-sent sentinel and at most one state-gated retry. Moving to another method requires empty composer and unchanged durable semantic state.

Required report sections:

`Target lifecycle diagnosis and results`

`Input method diagnosis and results`

For a passing method:

`Known-working Dashboard input method`

Required input proof token:

`DASHBOARD_INPUT_METHOD_REPRODUCIBLY_PROVEN`

If all safe methods fail:

`BLOCKED_ALL_BOUNDED_DASHBOARD_INPUT_METHODS`

## Final semantic contract

After and only after input proof and clean baseline:

- generate one brand-new `CNXSEM6-...` nonce;
- put and verify the exact complete prompt in the proven composer;
- Send exactly once, no resend;
- require exactly one Ticket and one route before provider;
- require exactly one correlated `ollama/qwen3.5:9b` inference;
- an actively correlated provider call may be observed read-only for up to 25 minutes;
- require exact durable final payload staging before/at native delivery;
- require exactly one visible nonce;
- require `response_ready -> delivery_confirmed -> completed`;
- reject duplicate semantic effects;
- after completion only, prove New Session continuity with zero additional semantic/provider effect.

Required final PASS token:

`PASS_FINAL_AUTHENTICATED_FRESH_SESSION_SEMANTIC_ACCEPTED`

## Retry policy

Read-only operations may use up to 3 attempts when useful.

Target bootstrap: maximum 2 attempts total with grace and fresh process/window evidence before attempt 2.

Within each low-impact input-method family: maximum 2 attempts total with grace + fresh UI/session/durable proof before attempt 2.

Final semantic Send is single-attempt for the entire task.

## Hard fence

No sent sentinel, historical nonce reuse, second final semantic Send, CLI/channel owner substitute, direct provider probe, synthetic Ticket, install/reset/repair/cleanup, maintained product-source change, product/runtime/config/SQLite mutation, provider/model/timeout change, restart/reboot, merge/tag/release or force push is authorized.

Ephemeral UIA/Win32 helpers outside maintained product source are allowed. Credentials remain private and must not be read, copied, printed, logged, requested or re-entered.