# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `READ_ONLY_DASHBOARD_FOREGROUND_INPUT_TARGET_READINESS`
Current authorization: `TASK099_ACCEPTED_BOUNDED_FOREGROUND_READINESS_APPROVED`
Task ID: `CNX-20260827-100`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Operator approval

The operator explicitly approved the bounded Task-100 design after Task 099 review.

## Task 099 accepted blocker

Task 099 report:

`d5fde8d5f1e5968a1ae5ce11f4017a15d9884dac`

Independent disposition:

`ACCEPT_BLOCKER_DASHBOARD_WINDOW_FOREGROUND_TARGETING_BEFORE_SEND`

Task 099 proved exact fresh target:

`agent:main:dashboard:89992501-1b33-46cf-85f7-eb0c1ef4d311`

It stopped before semantic send because a different Firefox window/process remained foreground. Semantic send count was `0`; no Task-099 Ticket/provider/delivery effect occurred. Task-099 nonce is retired.

## Active Task 100

[`tasks/CNX-20260827-100-dashboard-foreground-input-target-readiness.md`](tasks/CNX-20260827-100-dashboard-foreground-input-target-readiness.md)

Task 100 is readiness-only and sends zero semantic content.

It must prove:

- exact target session still exists, authenticated and empty/staged;
- exact Firefox/OpenClaw Dashboard top-level HWND is uniquely correlated to that target session;
- exact Dashboard HWND becomes the actual Windows foreground input window;
- intended chat composer can be focused/selected while still empty and without typing;
- no Ticket/provider/semantic side effect occurs;
- accepted MANAGED generation 24, exact plugin fingerprint, Gateway and SQLite health remain unchanged.

Required readiness token:

`DASHBOARD_FOREGROUND_COMPOSER_READY_NO_SEND`

Required PASS token:

`PASS_DASHBOARD_FOREGROUND_INPUT_TARGET_READY_NO_SEND`

## Retry policy v1

Read-only operations: maximum 3 attempts total.

Low-impact focus/window-activation actions: maximum 2 attempts total. A second attempt requires at least 3 seconds grace plus fresh foreground/window/session evidence proving attempt 1 did not already take effect.

If attempt 1 takes effect late, count it as success and do not retry. Ambiguous/partial state blocks retry.

Semantic send remains unauthorized in Task 100.

## Accepted live baseline

Exact installed source:

`32212a4331e1f32b5a130bd30d271d4cbc56f6c1`

Exact plugin fingerprint:

`df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`

Live state remains MANAGED generation 24 with one candidate-exact canonical plugin generation, accepted startup/Supervisor/Gateway/SQLite/Ollama health and `NO_FLASH_MULTI_TICK_REPROVEN`.

## Hard fence

No semantic nonce/send, CLI/channel substitute, direct provider/Ollama call, install/reset/repair/cleanup, session deletion/normalization, plugin-generation/controller/startup/Supervisor/AGENTS/config/runtime/SQLite mutation, Task-092/Task-099 evidence rewrite, restart/reboot, merge/tag/release or force push is authorized.

Credential values remain private and must not be read, copied, printed, logged, requested or re-entered by the executor.

## Successor gate

Only independent acceptance of Task 100 PASS may authorize a new final semantic task with a brand-new nonce and exactly one Dashboard send. The semantic send remains single-attempt; state-gated retry applies only to eligible surrounding low-impact/read-only operations.
