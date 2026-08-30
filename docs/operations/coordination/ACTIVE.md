# Active Coordination Task

Status: `READY_HERMES`
Execution mode: `REPOSITORY_DASHBOARD_NATIVE_TRANSCRIPT_AUTHORITY_REPAIR_HERMES`
Current authorization: `CNX-20260830-164_HERMES_REPOSITORY_DASHBOARD_NATIVE_TRANSCRIPT_AUTHORITY_REPAIR`
Task ID: `CNX-20260830-164`
Updated: 2026-08-30 ICT
Executor: Hermes
Coordinator / final reviewer: ChatGPT
Review type at completion: ChatGPT review required before successor authorization

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative.

## Active task

[`tasks/CNX-20260830-164-hermes-native-transcript-authority-red-to-green.md`](tasks/CNX-20260830-164-hermes-native-transcript-authority-red-to-green.md)

Task 164 is the delegated Hermes continuation of the Task-162 Dashboard final-delivery authority repair.

## Handoff state

The production-faithful RED is already committed and CI-proven at:

`61218ca6cc13a5c0312829abd72bcdb524944d12`

Regression:

`plugins/cogentnexus-openclaw/src/v162-dashboard-transcript-authority.test.ts`

RED Actions evidence:

- Validate run `33318911825`: expected `FAILURE`
- PS5.1 Acceptance Smoke `33318911867`: `SUCCESS`
- Windows Installer Pack Smoke `33318911864`: `SUCCESS`

First observed RED assertion:

`v162-dashboard-transcript-authority.test.ts:61`

`expect(beforeAgentFinalize).toBeTypeOf("function")`

Actual: `expected undefined to be type of 'function'`.

## Proven authority candidate

ChatGPT review rejected Hermes Task-163 `BLOCKED` because exact OpenClaw `v2026.7.1-2` commit `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c` exposes the missing public trusted-plugin post-persistence primitive:

`api.runtime.events.onSessionTranscriptUpdate(...)`

Required composite ordering:

`terminal assistant candidate -> before_message_write(marker + native claim) -> native SessionManager originalAppend -> onSessionTranscriptUpdate(post-persistence receipt) -> CogentNexus delivery settlement`

`before_message_write` is pre-persistence and must not itself confirm delivery. Recovery must be fenced while native-write ownership is active and must have no claimable pending row after native persistence is settled.

Review:

`reviews/CNX-20260830-163-hermes-dashboard-final-delivery-authority-repair-review.md`

## Current TDD gate

Hermes must first re-read GitHub current state and verify the inherited RED against exact pinned upstream source. If valid, the RED checkpoint is already satisfied and Hermes is authorized to proceed directly to the **minimal CogentNexus production repair**, then GREEN validation.

Do not weaken or replace the RED merely to obtain GREEN. If exact source disproves an assumption, stop and report the discrepancy.

## Hard fence

Repository-only. No Dashboard semantic Send or semantic UI interaction; no real Windows install/uninstall/reinstall/reset; no live Gateway/Ollama/Supervisor mutation; no manual Ticket/workflow/result/outbox/delivery/database mutation; no OpenClaw source patch; no dependency upgrade; no unrelated product change; no release/promotion; no merge to default/release branch; no force push.

Even Task-164 PASS does not authorize another Dashboard Send. ChatGPT review is required, followed by a separate repaired-candidate Windows install-over + provenance/health acceptance checkpoint before any new exactly-one-Send Dashboard reacceptance.
