# Coordination Channel Status

**State:** `READY_HERMES`  
**Execution mode:** `WINDOWS_FRESH_REINSTALL_POST_UNINSTALL_REACCEPTANCE_HERMES`  
**Updated:** 2026-08-31 ICT  
**Transport:** GitHub repository history  
**Active task:** `CNX-20260831-185`

## Active work

[`tasks/CNX-20260831-185-hermes-fresh-reinstall-post-uninstall-reacceptance.md`](tasks/CNX-20260831-185-hermes-fresh-reinstall-post-uninstall-reacceptance.md)

Executor: Hermes/Codex. Coordinator / final reviewer: ChatGPT.

Standing model: executor-heavy / reviewer-light.

## Accepted repository/live state

Task 179:

`ACCEPTED_PASS — INTERACTIVE_LIFECYCLE_DELEGATION_REPAIR_ACCEPTED`

Exact repository candidate:

`f6392da3e4112ce441526d5ef19925c90a872b0b`

Required installed facade SHA-256:

`aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

Task 183:

`ACCEPTED_PASS — QUALIFIED_HARNESS_RESET_FRESH_STATE_REACCEPTED`

Task 184:

`ACCEPTED_PASS — QUALIFIED_HARNESS_UNINSTALL_EXTERNAL_PRESERVATION_ACCEPTED`

Current live state is post-uninstall native OpenClaw. CNX launcher/skill/plugin/state/runtime/scheduled-task/config registration are absent. OpenClaw `2026.7.1-2`, native Gateway health, Ollama/model inventory, unrelated plugins, and Gateway command surface were preserved.

## Task 185 gate

Task 185 must independently re-prove the clean post-uninstall boundary and exact candidate identity before mutation, then may invoke the supported installer exactly once.

Post-install acceptance requires:

- active `cnxclaw.py` SHA-256 `aa747f8f...`;
- release `0.9.3`, plugin loaded/enabled with accepted fingerprint;
- ownership present and legacy namespace empty;
- controller MANAGED with selected provider Ollama and no transition;
- healthy Gateway and Ollama;
- SQLite integrity `ok` and no manufactured Ticket/session/delivery/model/recovery history;
- delivery/recovery READY with outbox `0`;
- external OpenClaw/Ollama/model/unrelated-plugin/Gateway-command preservation.

No retry is authorized if the one installer invocation becomes ambiguous; inspect the same process/evidence instead.

## UI policy

Task 185 uses no Dashboard/UI semantic action.

For final Dashboard acceptance after Task 185 review:

- user controls New Session/navigation and clicks;
- user focuses/selects the text field;
- Hermes may type the nonce/test text after focus;
- Hermes must not press Send;
- user presses Send exactly once;
- Hermes/Codex then collect Ticket/model/durable-delivery evidence.

## Hard fence

Supported fresh-install root invocation maximum: `1`.
Semantic/model/recovery action budget: `0`.

No reset, uninstall, second install/retry, executor lifecycle helper outside installer, manual Gateway/Ollama action, Dashboard Send/chat.inject, model/recovery action, manual repair, source/product/test/workflow edit, release/tag/merge, or force push.

After Task-185 report publication, stop for ChatGPT review. Final Dashboard semantic acceptance remains unauthorized.
