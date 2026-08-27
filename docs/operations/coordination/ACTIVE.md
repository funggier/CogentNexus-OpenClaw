# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_OPEN_FRESH_FIREFOX_TARGET_INPUT_DIAGNOSIS_AND_FINAL_SEMANTIC_ACCEPTANCE`
Current authorization: `OPERATOR_DIRECTED_OPEN_FIREFOX_IF_ABSENT_AND_RETRY_FINAL_ACCEPTANCE`
Task ID: `CNX-20260827-102`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Operator correction after Task 101

Task 101 report:

`d06b1397e032749e5b348d5d1054dc1784d67519`

Task 101 correctly observed that its fresh inventory contained no Firefox/OpenClaw window and therefore performed zero sentinel/input attempts and zero semantic Sends.

The operator clarified the cause: **Firefox simply was not open at that time.** This must not be treated as evidence of a Firefox window-lifecycle defect.

Task 101 report/publication remains historical evidence and is not rewritten. The successor interpretation is corrected here.

## Active Task 102

[`tasks/CNX-20260827-102-reestablish-dashboard-target-and-final-semantic-acceptance.md`](tasks/CNX-20260827-102-reestablish-dashboard-target-and-final-semantic-acceptance.md)

Key execution rule:

- first inspect current Firefox/OpenClaw windows;
- if none exists, **open Firefox immediately to the non-secret local OpenClaw Dashboard route using the existing authenticated profile**;
- do not stop merely because Firefox was absent;
- after opening, rediscover the actual live HWND/PID/title/class/session/composer from fresh OS/UIA state;
- do not trust stale Task-100 PID/HWND values or a launcher PID as browser-window identity;
- wait and re-check target stability before any sentinel.

Required target token:

`DASHBOARD_LIVE_TARGET_READY`

If credential re-entry would be required by the executor, stop without reading/requesting the credential.

## Input method ladder

After a live exact Dashboard target and empty `Message Assistant` composer are proven:

1. UI Automation / Accessibility direct edit without global keyboard focus;
2. deterministic Win32 foreground/input-thread handoff, requiring exact `GetForegroundWindow == target HWND` before any global keystroke;
3. freshly opened Firefox natural-focus positive control only if still safely needed.

Each method uses a unique non-sent sentinel, may use one state-gated retry, must clear the composer and must prove zero Ticket/provider effect before moving on.

The report must contain:

`Firefox/bootstrap diagnosis and results`

`Input method diagnosis and results`

If a method passes:

`Known-working Dashboard input method`

and token:

`DASHBOARD_INPUT_METHOD_REPRODUCIBLY_PROVEN`

## Final semantic continuation

Only after input proof and a clean durable baseline:

- generate one new `CNXSEM6-...` nonce;
- verify complete prompt in exact composer;
- Send exactly once;
- no resend;
- require one Ticket accepted/routed before one correlated `ollama/qwen3.5:9b` call;
- permit read-only observation of an active correlated provider call for up to 25 minutes;
- require durable final-payload staging before/at native delivery;
- require exactly one visible nonce;
- require `response_ready -> delivery_confirmed -> completed`;
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

No sent sentinel, historical nonce reuse, second final semantic Send, CLI/channel substitute, direct provider probe, synthetic Ticket, install/reset/repair/cleanup, maintained product-source change, product/runtime/config/SQLite mutation, provider/model/timeout change, restart/reboot, merge/tag/release or force push is authorized.

Ephemeral UIA/Win32 helpers outside maintained product source are allowed. Credential values must not be read, copied, printed, logged, requested or re-entered by the executor.