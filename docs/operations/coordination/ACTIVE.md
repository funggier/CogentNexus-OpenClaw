# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_BOUNDED_INPUT_ROOT_CAUSE_AND_FINAL_SEMANTIC_ACCEPTANCE`
Current authorization: `TASK100_ACCEPTED_OPERATOR_AUTHORIZED_BOUNDED_INPUT_REPAIR_AND_TEST`
Task ID: `CNX-20260827-101`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Task 100 reviewed

Task 100 report:

`8ad8377750f72fcee69c78fa26a199233f997b5f`

Independent decision: `ACCEPT`

Disposition:

`ACCEPT_BLOCKER_WINDOWS_FOREGROUND_INPUT_OWNERSHIP`

Review:

[`reviews/CNX-20260827-100-dashboard-foreground-input-target-readiness.md`](reviews/CNX-20260827-100-dashboard-foreground-input-target-readiness.md)

Publication fence is valid: execution `0ac2655418cee76c7de8058f77cd22c29cf931cd` -> report `8ad8377750f72fcee69c78fa26a199233f997b5f` is one report-only commit.

Task 100 proved the target session/window/composer identity but could not safely deliver keyboard input because the exact Firefox/OpenClaw window was not the verified Windows foreground input owner. Semantic send count remained 0 and no new Ticket/provider/delivery effect occurred.

Accepted root-cause class:

`WINDOWS_FOREGROUND_INPUT_OWNERSHIP_NOT_DETERMINISTIC`

## Active Task 101

[`tasks/CNX-20260827-101-focus-independent-dashboard-input-and-final-semantic-acceptance.md`](tasks/CNX-20260827-101-focus-independent-dashboard-input-and-final-semantic-acceptance.md)

Task 101 must diagnose and test the input boundary rather than stop at the first focus failure.

Pre-authorized method ladder:

1. focus-independent UI Automation / Accessibility direct edit of the exact `Message Assistant` composer;
2. deterministic Win32 foreground/input-thread handoff with exact `GetForegroundWindow == target HWND` proof before any global keystroke;
3. controlled dedicated-new-Firefox-window positive-control fallback reproducing the earlier successful natural-focus condition, again requiring exact foreground proof before typing.

Each method uses a unique non-sent sentinel first, may have at most one state-gated retry inside the same method family, must clear the composer, and must prove zero Ticket/provider effect before moving on.

If a method fails, Task 101 must report the exact boundary, evidence-based hypothesis/fix and result of the next bounded method. It must include:

`Input method diagnosis and results`

If one method passes, it must additionally include:

`Known-working Dashboard input method`

and issue:

`DASHBOARD_INPUT_METHOD_REPRODUCIBLY_PROVEN`

## Final semantic continuation

Only after one input method is proven and the composer/durable baseline are clean:

- generate one new `CNXSEM5-...` nonce;
- enter the full prompt using the proven method;
- verify the full prompt in the exact composer;
- Send exactly once;
- no resend under any result;
- prove exactly one Ticket accepted/routed before one correlated `ollama/qwen3.5:9b` inference;
- allow read-only observation of an active correlated provider call for up to 25 minutes because the historical positive-control call was slow;
- prove durable Task-093 final-payload staging before native delivery;
- prove exactly one visible nonce;
- prove `response_ready -> delivery_confirmed -> completed` for the exact Ticket/run/session;
- reject duplicate Ticket/route/provider/staging/outbox/reply/promotion effects;
- after completed only, prove New Session continuity with zero additional semantic/provider effect.

Required final PASS token:

`PASS_FINAL_AUTHENTICATED_FRESH_SESSION_SEMANTIC_ACCEPTED`

## Accepted live baseline

Exact installed source:

`32212a4331e1f32b5a130bd30d271d4cbc56f6c1`

Exact plugin fingerprint:

`df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`

Live baseline remains MANAGED generation 24 with accepted startup/Supervisor/Gateway/SQLite/Ollama health and `NO_FLASH_MULTI_TICK_REPROVEN`.

## Hard fence

No sent sentinel, second final semantic Send, historical nonce reuse, CLI/channel substitute, direct provider probe, synthetic Ticket, install/reset/repair/cleanup, product/runtime/config/SQLite mutation, session normalization, provider/model/timeout change, restart/reboot, merge/tag/release or force push is authorized.

Ephemeral UIA/Win32 diagnostic helpers outside product source are allowed; do not commit them as maintained product code.

Credentials remain private and must not be read, copied, printed, logged, requested or re-entered by the executor.
