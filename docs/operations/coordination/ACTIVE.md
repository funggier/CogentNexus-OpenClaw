# Active Coordination Task

Status: `IN_PROGRESS_CHATGPT`
Execution mode: `REPOSITORY_DASHBOARD_FINAL_DELIVERY_AUTHORITY_REPAIR_CONTINUATION`
Current authorization: `CNX-20260830-162_REPOSITORY_DASHBOARD_FINAL_DELIVERY_AUTHORITY_REPAIR_CONTINUATION`
Task ID: `CNX-20260830-162`
Updated: 2026-08-30 ICT
Owner / coordinator / executor / reviewer: ChatGPT
Review type at completion: self-review / non-independent

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative.

## Active task

[`tasks/CNX-20260830-162-dashboard-final-delivery-authority-repair-continuation.md`](tasks/CNX-20260830-162-dashboard-final-delivery-authority-repair-continuation.md)

## Delegated investigation review

Task 163 delegated the unresolved authority-boundary trace to Hermes.

Hermes reported `BLOCKED`, but ChatGPT final review did not accept that conclusion because exact OpenClaw `v2026.7.1-2` exposes a missing plugin-accessible post-persistence primitive:

`api.runtime.events.onSessionTranscriptUpdate(...)`

Review:

`reviews/CNX-20260830-163-hermes-dashboard-final-delivery-authority-repair-review.md`

The exact upstream source establishes:

`before_message_write -> native SessionManager originalAppend -> emitSessionTranscriptUpdate`

and `PluginRuntime.events` publicly exposes `onSessionTranscriptUpdate` to trusted native plugins.

Task 162 therefore resumes under ChatGPT authority.

## Current TDD gate

No production source change is authorized yet.

ChatGPT must first commit a production-faithful test-only RED regression proving the composite authority candidate:

1. pre-model `reply_dispatch` has no append-capable dispatcher;
2. no second `reply_payload_sending` callback is assumed;
3. exact assistant result/run/session correlation is available on the real post-model path;
4. `before_message_write` binds the stable CogentNexus durable-delivery marker to the assistant message that OpenClaw will natively persist;
5. `runtime.events.onSessionTranscriptUpdate` is observed only after the native append and carries the marker-bearing assistant plus native message identity;
6. delivery success remains withheld until that post-persistence observation;
7. native persistence suppresses recovery injection;
8. native-write ownership and recovery ownership cannot race into duplicate semantic assistant output;
9. no second inference occurs after an assistant result already exists;
10. Task-155 duplicate/no-regeneration safeguards remain intact.

Only after the RED commit and expected failure are recorded may the smallest CogentNexus-OpenClaw production repair be made.

## Hard fence

Repository-only. No Dashboard semantic Send or semantic UI interaction; no real Windows install/uninstall/reinstall/reset; no Gateway/Ollama/Supervisor live restart; no manual durable-state mutation; no OpenClaw source patch; no dependency upgrade; no unrelated product change; no release/promotion; no merge to default/release branch; no force push.

Even Task-162 ACCEPT does not authorize another Dashboard Send. A separate repaired-candidate Windows install-over + provenance/health acceptance checkpoint is still required first.
