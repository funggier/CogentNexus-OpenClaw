# CNX-20260901-206 — Task 205 Discord Native Delivery / Hook Forensics

Status: `READY_FOR_HERMES`
Date: 2026-09-01 ICT
Parent: `CNX-20260901-205`
Repair parent: `CNX-20260831-198`
Executor: Hermes / authenticated Windows operator
Coordinator / final reviewer: ChatGPT

## Purpose

Classify the exact live Discord delivery boundary that failed in Task 205 **without sending another Discord message and without mutating runtime state**.

Task 205 already proved:

`human Send -> one Ticket -> one completed direct Ollama model call -> response_ready`

but did not prove native Discord transmission or a delivery receipt bound back to the Ticket.

This task must determine whether the missing settlement is primarily:

1. native Discord send absent/failed;
2. native send succeeded but `message_sent` did not fire;
3. `message_sent` fired without usable `runId`/`sessionKey` correlation;
4. `reply_dispatch` fired without usable run correlation / dispatcher settlement;
5. another precisely evidenced delivery-path condition; or
6. retained evidence is insufficient.

## Immutable authorities

Frozen repaired candidate:

`9f4eaa429b2540540e7d6f6c2af99067960e45fb`

Installed fingerprint expected:

`f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`

Published `v0.9.3` target remains immutable:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Correct Discord channel:

`1531199905673252946`

Task-205 correlation identity:

```text
nonce: CNX205-20260831T190442Z-8cdbed
Ticket: CNXT-f23e2c11-e630-4319-84c2-c57ed7e7edf6
request_key: 09c9121cdac5dec9cb1fdea1a37aeafdacb098ce2e89f26a1b2a2f103fd5ed9f
run_id: b79dbb65-15eb-4b3e-8ffb-4084125e6cb5
call_id: b79dbb65-15eb-4b3e-8ffb-4084125e6cb5:model:1
response_ready: 2026-08-31T19:06:52.333Z
```

## Hard fence

This task is read-only. Do **not**:

- send any Discord message or probe;
- retry/regenerate the Task-205 nonce;
- invoke enable/disable/start/stop/restart/reset/uninstall/install/reinstall/install-over;
- kill processes;
- change provider/model/config;
- mutate SQLite or session files;
- edit product/source/test/workflow files;
- mutate Release/tag/assets;
- force push.

If evidence is insufficient, report `INSUFFICIENT_RETAINED_EVIDENCE`; do not manufacture new traffic.

## Phase A — fresh authority and runtime continuity

Fresh-check GitHub coordination authority and capture current read-only runtime health only to ensure evidence inspection is not being confused by a new lifecycle event:

- installed fingerprint;
- Host mode;
- plugin loaded/enabled;
- Gateway health;
- Ollama health;
- delivery/recovery status;
- SQLite integrity;
- lifecycle residue scan.

Do not repair drift under this task.

## Phase B — exact retained log window

Locate all OpenClaw/Gateway/plugin log files that cover at least:

`2026-08-31T19:05:00Z` through `2026-08-31T19:09:00Z`

Preserve original paths, sizes, mtimes and SHA-256 before extracting bounded excerpts.

Search the retained window for, at minimum:

- `b79dbb65-15eb-4b3e-8ffb-4084125e6cb5`
- `CNXT-f23e2c11-e630-4319-84c2-c57ed7e7edf6`
- `CNX205-20260831T190442Z-8cdbed`
- `1531199905673252946`
- `message_sent`
- `message_sending`
- `reply_dispatch`
- `appendBeforeDeliver`
- `waitForIdle`
- `delivery_confirmed`
- `direct Ticket finalization failed`
- `missing-run-correlation`
- `missing-append-before-deliver`
- `final delivery failed`
- `final delivery cancelled`
- Discord outbound/send error text
- plugin hook error/timeout text.

Do not rely on absence from one file until all relevant retained logs in the window are enumerated.

## Phase C — session/transcript and native outbound evidence

Read-only inspect the exact Discord session / transcript generation that owns:

`agent:main:discord:channel:1531199905673252946`

Determine whether the assistant final corresponding to run `b79dbb65-...` is persisted in the OpenClaw transcript/session history.

Where retained native outbound metadata exists, capture:

- target/channel ID;
- message ID;
- success/failure;
- timestamp;
- content hash or bounded non-sensitive identifying metadata;
- any session key attached to outbound context;
- any run ID attached to outbound context.

Do not expose credentials or full private payload bodies in the repository report.

## Phase D — hook-shape classification

Compare live retained evidence against accepted OpenClaw `2026.7.1-2 (0790d9f)` contracts:

- outbound `message_sent.runId` is optional and baseline documentation says it is not yet plumbed through the outbound path;
- outbound `message_sent.sessionKey` is optional and depends on a resolvable outbound session context;
- `reply_dispatch.runId` is optional;
- CogentNexus currently settles the `message_sent` fallback only when it can resolve a run from `event.runId` or exact `event.sessionKey`.

Classify exactly one primary result when evidence permits:

### `EVIDENCE_NATIVE_SEND_FAILED`
Native Discord send was attempted and failed before a successful receipt.

### `EVIDENCE_NATIVE_SEND_SUCCEEDED_RECEIPT_UNCORRELATED`
Native Discord send succeeded, but CogentNexus lacked usable run/session correlation to settle the Ticket.

### `EVIDENCE_REPLY_DISPATCH_SETTLEMENT_FAILED`
`reply_dispatch` took ownership of the run but its dispatcher-settlement path failed/hung/returned an evidenced failure.

### `EVIDENCE_MESSAGE_SENT_NOT_EMITTED`
Native send evidence exists but no corresponding `message_sent` hook emission is retained and the absence can be established from authoritative instrumentation.

### `EVIDENCE_OTHER_PRECISE`
Another exact, evidenced mechanism explains the boundary.

### `INSUFFICIENT_RETAINED_EVIDENCE`
Evidence cannot distinguish the mechanisms above.

Do not infer a hook payload field merely from type contracts; retain actual live evidence where available.

## Phase E — repository handoff recommendation

If a mechanism is proven, identify the **smallest deterministic repository RED** that should be written next. Do not write the test or production fix in this task.

The recommendation must specify:

- hook/event shape to simulate;
- required missing/present fields (`runId`, `sessionKey`, dispatcher, target, etc.);
- expected pre-fix Ticket state;
- desired safe invariant;
- concurrency/ambiguity fence so no receipt can settle the wrong run.

If evidence is insufficient, recommend the smallest instrumentation-only change needed for a future single-send diagnostic, but do not implement it here.

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260901-206-task205-discord-native-delivery-hook-forensics.md`

Include:

- exact authority SHA;
- evidence file inventory + hashes;
- exact time window;
- transcript/session findings;
- native Discord outbound findings;
- hook diagnostic findings;
- classification;
- smallest next RED recommendation;
- mutation ledger proving zero Send and zero runtime/source mutation.

Then stop for ChatGPT review.
