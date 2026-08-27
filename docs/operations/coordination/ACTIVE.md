# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_TARGET_LIFECYCLE_REESTABLISHMENT_INPUT_DIAGNOSIS_AND_FINAL_SEMANTIC_ACCEPTANCE`
Current authorization: `TASK101_ACCEPTED_OPERATOR_REQUESTED_NEW_ATTEMPT`
Task ID: `CNX-20260827-102`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Task 101 reviewed

Task 101 report:

`d06b1397e032749e5b348d5d1054dc1784d67519`

Independent decision: `ACCEPT`

Disposition:

`ACCEPT_BLOCKER_TARGET_WINDOW_LIFECYCLE_NOT_ESTABLISHED`

Review:

[`reviews/CNX-20260827-101-focus-independent-dashboard-input-and-final-semantic-acceptance.md`](reviews/CNX-20260827-101-focus-independent-dashboard-input-and-final-semantic-acceptance.md)

Publication fence is valid: execution `ef4e71628c4b4906f0a26ed4f6673241bb9999bc` -> report `d06b1397e032749e5b348d5d1054dc1784d67519` is exactly one report-only commit.

Task 101 sent zero semantic messages and never reached its UIA/Win32 input ladder. It stopped earlier because fresh live inventory contained no Firefox/OpenClaw target window and a prior automation window id was stale.

Accepted boundary:

`DASHBOARD_TARGET_WINDOW_LIFECYCLE_NOT_ESTABLISHED`

## Active Task 102

[`tasks/CNX-20260827-102-reestablish-dashboard-target-and-final-semantic-acceptance.md`](tasks/CNX-20260827-102-reestablish-dashboard-target-and-final-semantic-acceptance.md)

Task 102 must first establish a live stable OpenClaw Dashboard target window before any input test.

Key correction:

- do not trust the PID/process handle returned by a Firefox launch as the resulting browser-window identity;
- Firefox may forward `-new-window` into another existing process and the launcher may exit;
- rediscover actual visible top-level Firefox/OpenClaw windows from fresh OS-level `EnumWindows`/PID/title/class evidence after launch;
- then correlate exact Dashboard session and current `Message Assistant` composer using fresh UIA/accessibility state.

Task 102 may use at most two target-bootstrap attempts under state-gated retry. A late appearing window is success/no relaunch. Multiple candidate windows must be disambiguated instead of creating more windows.

Required target token:

`DASHBOARD_LIVE_TARGET_REESTABLISHED`

## Input method ladder after target stability

Only after the exact target window survives fresh rediscovery/stability checks:

1. UI Automation / Accessibility direct composer edit without global keyboard focus;
2. deterministic Win32 foreground/input-thread handoff with exact `GetForegroundWindow == target HWND` proof before any keystroke;
3. controlled natural-focus dedicated Firefox positive control when still eligible.

Each method uses a unique non-sent sentinel, may have one state-gated retry, must clear the composer and must prove zero Ticket/provider effect before moving on.

Report must contain:

`Target lifecycle diagnosis and results`

`Input method diagnosis and results`

If a method passes:

`Known-working Dashboard input method`

and token:

`DASHBOARD_INPUT_METHOD_REPRODUCIBLY_PROVEN`

## Final semantic continuation

Only after an input method is reproducibly proven and the composer/durable baseline are clean:

- generate one new `CNXSEM6-...` nonce;
- verify complete prompt in the exact composer;
- Send exactly once;
- no resend exists;
- require exactly one Ticket accepted/routed before exactly one correlated `ollama/qwen3.5:9b` inference;
- allow read-only observation of a still-active correlated provider call for up to 25 minutes;
- require durable final payload staging before/at native delivery;
- require exactly one visible nonce;
- require `response_ready -> delivery_confirmed -> completed`;
- reject duplicate Ticket/route/provider/staging/outbox/reply/promotion effect;
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

No sent sentinel, historical nonce reuse, second final semantic Send, CLI/channel substitute, direct provider probe, synthetic Ticket, install/reset/repair/cleanup, maintained product-source change, product/runtime/config/SQLite mutation, provider/model/timeout change, restart/reboot, merge/tag/release or force push is authorized.

Ephemeral UIA/Win32 helpers outside maintained product source are allowed. Credential values must not be read, copied, printed, logged, requested or re-entered by the executor.