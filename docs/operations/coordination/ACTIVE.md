# Active Coordination Task

Status: `READY_HERMES`
Execution mode: `WINDOWS_FRESH_REINSTALL_POST_UNINSTALL_REACCEPTANCE_HERMES`
Current authorization: `CNX-20260831-185_HERMES_FRESH_REINSTALL_POST_UNINSTALL_REACCEPTANCE`
Task ID: `CNX-20260831-185`
Updated: 2026-08-31 ICT
Executor: Hermes/Codex
Coordinator / final reviewer: ChatGPT
Review model: executor-heavy / reviewer-light

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative.

## Active task

[`tasks/CNX-20260831-185-hermes-fresh-reinstall-post-uninstall-reacceptance.md`](tasks/CNX-20260831-185-hermes-fresh-reinstall-post-uninstall-reacceptance.md)

## Accepted state

Task 179 repository repair:

`ACCEPTED_PASS — INTERACTIVE_LIFECYCLE_DELEGATION_REPAIR_ACCEPTED`

Exact frozen candidate:

`f6392da3e4112ce441526d5ef19925c90a872b0b`

Candidate/required active facade SHA-256:

`aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

Task 183 reset acceptance:

`ACCEPTED_PASS — QUALIFIED_HARNESS_RESET_FRESH_STATE_REACCEPTED`

Task 184 uninstall/external preservation:

`ACCEPTED_PASS — QUALIFIED_HARNESS_UNINSTALL_EXTERNAL_PRESERVATION_ACCEPTED`

The live machine is intentionally at a native-OpenClaw post-uninstall boundary: CNX-owned surfaces are absent; OpenClaw/Gateway, Ollama, model inventory, unrelated plugin inventory, and Gateway command surface were preserved.

## Task-185 authorization

After a fresh read-only post-uninstall/candidate/process preflight, Hermes/Codex may invoke exactly one repository-supported fresh install from exact candidate `f6392da...`.

PASS requires active installed facade byte identity with SHA-256 `aa747f8f...`, release/plugin/ownership/controller/Ollama/Gateway health, fresh zero semantic durable state, and preservation of external OpenClaw/Ollama/unrelated surfaces.

## UI policy

No UI semantic action is authorized in Task 185.

For the later final Dashboard test, the user controls New Session/navigation/focus and presses Send. Hermes may type only after the user focuses the intended text field and must not press Send.

## Hard fence

Task 185 supported installer root invocation budget: `1`.
Semantic/model/recovery action budget: `0`.

No reset, uninstall, second install/retry, executor lifecycle helper outside the installer, manual Gateway/Ollama lifecycle action, Dashboard Send/chat.inject, model/recovery action, manual state repair, source/product/test/workflow edit, release/tag/merge, or force push.

After Task-185 report publication, stop for ChatGPT review. Final Dashboard semantic acceptance remains unauthorized.
