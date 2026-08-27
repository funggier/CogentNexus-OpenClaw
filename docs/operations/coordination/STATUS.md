# Coordination Channel Status

**State:** `READY_FOR_HERMES`
**Updated:** 2026-08-27 ICT
**Transport:** GitHub repository history
**Human authority:** operator requested a new attempt, clarified Firefox was simply not open during Task 101, and directed the executor to open Firefox when absent before continuing bounded input diagnosis and final authenticated semantic acceptance
**Execution trigger:** manual Hermes continuation; scheduled execution remains disabled

## Accepted live baseline

Task 096 live deployment remains accepted.

Exact installed source:

`32212a4331e1f32b5a130bd30d271d4cbc56f6c1`

Accepted plugin fingerprint:

`df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`

Live state remains MANAGED generation 24 with one candidate-exact canonical plugin generation, healthy startup/Supervisor/Gateway/SQLite/Ollama, preserved Task-092 retired evidence and accepted `NO_FLASH_MULTI_TICK_REPROVEN`.

## Task 101 result and corrected interpretation

Task 101 report:

`d06b1397e032749e5b348d5d1054dc1784d67519`

Task 101 publication is exactly one report-only commit from execution `ef4e71628c4b4906f0a26ed4f6673241bb9999bc`.

Task 101 performed zero sentinel/input attempts and zero semantic Sends because fresh inventory contained no Firefox/OpenClaw window.

The operator clarified that Firefox was **not open** at that time. Therefore the absence of a target is an environment precondition, not evidence that Firefox window lifecycle is broken. Historical Task-101 evidence remains unchanged; only the successor interpretation is corrected.

## Active Task 102

[`tasks/CNX-20260827-102-reestablish-dashboard-target-and-final-semantic-acceptance.md`](tasks/CNX-20260827-102-reestablish-dashboard-target-and-final-semantic-acceptance.md)

Execution mode:

`LIVE_OPEN_FRESH_FIREFOX_TARGET_INPUT_DIAGNOSIS_AND_FINAL_SEMANTIC_ACCEPTANCE`

Authorization:

`OPERATOR_DIRECTED_OPEN_FIREFOX_IF_ABSENT_AND_RETRY_FINAL_ACCEPTANCE`

## Firefox/bootstrap rule

Task 102 first checks for a current Firefox/OpenClaw Dashboard window.

If none exists, the executor must **open Firefox immediately** to the non-secret local OpenClaw Dashboard route using the existing authenticated Firefox profile. Absence itself is not a blocker.

After opening, the executor must rediscover the real live target from fresh state:

- current Firefox processes;
- visible top-level HWND/PID/title/class;
- fresh UIA/accessibility tree;
- exact Dashboard session;
- current `Message Assistant` composer.

Do not reuse stale Task-100 PID/HWND values and do not assume the PID returned by a launch command is the actual browser-window identity.

The exact target must survive a stability re-check before any sentinel.

Required target token:

`DASHBOARD_LIVE_TARGET_READY`

If the existing authenticated profile cannot reach Dashboard without executor credential re-entry, stop without requesting or reading credentials.

## Input diagnosis

After target readiness, use the bounded ladder:

1. focus-independent UIA/accessibility direct edit;
2. deterministic Win32 foreground/input-thread handoff with exact foreground equality before keyboard input;
3. fresh-window natural-focus positive control if still needed and safe.

Each method reports exact capability/failure boundary, tested hypothesis/fix and outcome. Each uses a unique non-sent sentinel and at most one state-gated retry. Moving to the next method requires empty composer and unchanged durable semantic state.

Required report sections:

`Firefox/bootstrap diagnosis and results`

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
- enter and verify the exact complete prompt in the proven composer;
- Send exactly once, no resend;
- require exactly one Ticket and one route before provider;
- require exactly one correlated `ollama/qwen3.5:9b` inference;
- an actively correlated provider call may be observed read-only for up to 25 minutes;
- require exact durable final-payload staging before/at native delivery;
- require exactly one visible nonce;
- require `response_ready -> delivery_confirmed -> completed`;
- reject duplicate semantic effects;
- after completion only, prove New Session continuity with zero additional semantic/provider effect.

Required final PASS token:

`PASS_FINAL_AUTHENTICATED_FRESH_SESSION_SEMANTIC_ACCEPTED`

## Retry policy

Read-only operations may use up to 3 attempts where useful.

Firefox/bootstrap and each low-impact input-method family may use at most 2 state-gated attempts with grace + fresh evidence before attempt 2.

Final semantic Send is single-attempt for the entire task.

## Hard fence

No sent sentinel, historical nonce reuse, second final semantic Send, CLI/channel owner substitute, direct provider probe, synthetic Ticket, install/reset/repair/cleanup, maintained product-source change, product/runtime/config/SQLite mutation, provider/model/timeout change, restart/reboot, merge/tag/release or force push is authorized.

Ephemeral UIA/Win32 helpers outside maintained product source are allowed. Credentials remain private and must not be read, copied, printed, logged, requested or re-entered.