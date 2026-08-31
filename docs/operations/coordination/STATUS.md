# Coordination Channel Status

**State:** `READY_HERMES`  
**Execution mode:** `WINDOWS_QUALIFIED_HARNESS_UNINSTALL_EXTERNAL_PRESERVATION_HERMES`  
**Updated:** 2026-08-31 ICT  
**Transport:** GitHub repository history  
**Active task:** `CNX-20260831-184`

## Active work

[`tasks/CNX-20260831-184-hermes-qualified-harness-uninstall-external-preservation-acceptance.md`](tasks/CNX-20260831-184-hermes-qualified-harness-uninstall-external-preservation-acceptance.md)

Executor: Hermes/Codex. Coordinator / final reviewer: ChatGPT.

Standing model: executor-heavy / reviewer-light.

## Accepted repository/live state

Task 179:

`ACCEPTED_PASS — INTERACTIVE_LIFECYCLE_DELEGATION_REPAIR_ACCEPTED`

Exact repository candidate:

`f6392da3e4112ce441526d5ef19925c90a872b0b`

Task 182:

`ACCEPTED_PASS — REPAIRED_CANDIDATE_INSTALL_OVER_ACCEPTED`

Task 183:

`ACCEPTED_PASS — QUALIFIED_HARNESS_RESET_FRESH_STATE_REACCEPTED`

The repaired candidate is currently installed on Windows with active facade SHA-256:

`aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

Reset established fresh-install MANAGED state with zero reset-owned durable rows while preserving OpenClaw `2026.7.1-2`, Ollama, and the model inventory.

## Task 184 gate

Task 184 independently re-proves the clean fresh-state boundary, freezes external-preservation evidence, then may invoke exactly one installed uninstall through the qualified character-prompt harness.

The real `Continue? [y/N]: ` prompt must be observed before exactly one literal `y` is sent. No retry is allowed if the outer shell or observer loses contact.

After exit, the task must allow the implementation-owned Windows delayed cleanup to converge and then prove:

- CNX-owned launcher/skill/plugin/state/startup/config surfaces are removed;
- CogentNexus plugin is no longer registered/loaded;
- native OpenClaw remains installed and healthy;
- Ollama remains healthy and model inventory is unchanged;
- unrelated data/namespaces frozen in preflight remain intact.

Reinstall is deliberately excluded from this task and remains a later successor.

## UI policy

No UI action is required in Task 184. For the later final Dashboard acceptance, New Session/navigation/field selection/Send are user-controlled UI actions. Hermes may enter text only after the user has focused the intended text field and must not press Send.

## Hard fence

Uninstall root invocation maximum: `1`.
Confirmation send maximum: `1`.
Semantic/model/recovery action budget: `0`.

No reinstall/install/install-over, reset, second uninstall, second `y`, executor lifecycle helper, manual Gateway/Ollama lifecycle action, manual deletion/repair, Dashboard semantic action, model/recovery action, source/product/test/workflow edit, release/tag/merge, or force push.

After Task-184 report publication, stop for ChatGPT review. Reinstall remains unauthorized.
