# Active Coordination Task

Status: `READY_HERMES`
Execution mode: `WINDOWS_QUALIFIED_HARNESS_UNINSTALL_EXTERNAL_PRESERVATION_HERMES`
Current authorization: `CNX-20260831-184_HERMES_QUALIFIED_HARNESS_UNINSTALL_EXTERNAL_PRESERVATION`
Task ID: `CNX-20260831-184`
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

[`tasks/CNX-20260831-184-hermes-qualified-harness-uninstall-external-preservation-acceptance.md`](tasks/CNX-20260831-184-hermes-qualified-harness-uninstall-external-preservation-acceptance.md)

## Accepted state

Task 179 repository repair:

`ACCEPTED_PASS — INTERACTIVE_LIFECYCLE_DELEGATION_REPAIR_ACCEPTED`

Accepted candidate:

`f6392da3e4112ce441526d5ef19925c90a872b0b`

Task 182 installed-candidate acceptance:

`ACCEPTED_PASS — REPAIRED_CANDIDATE_INSTALL_OVER_ACCEPTED`

Task 183 reset acceptance:

`ACCEPTED_PASS — QUALIFIED_HARNESS_RESET_FRESH_STATE_REACCEPTED`

Current installed facade before uninstall:

`aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

The live CNX state is a fresh-install MANAGED baseline with reset-owned durable tables at zero. OpenClaw `2026.7.1-2`, Ollama, and the model inventory were preserved through reset.

## Task-184 authorization

After fresh authority/process/runtime/durable/external-preservation preflight, Hermes/Codex may launch exactly one installed `cnxclaw.cmd uninstall` through the qualified incremental character-prompt harness.

Exactly one literal `y` may be sent only after the real `Continue? [y/N]: ` prompt is observed and durably recorded.

PASS requires uninstall exit `0`, uninstall PASS/native OpenClaw health evidence, convergence of implementation-owned Windows delayed cleanup, removal of CNX-owned launcher/skill/plugin/state/startup/config surfaces, and preservation of native OpenClaw, Ollama, model inventory, and unrelated data.

## UI policy

No UI action is required in Task 184. For later Dashboard acceptance, UI navigation/click actions and Send are human-controlled by the user. Hermes may type only after the user focuses the intended text field and must not press Send.

## Hard fence

Uninstall root invocation maximum: `1`.
Confirmation send maximum: `1` literal `y` line.
Semantic/model/recovery action budget: `0`.

No reinstall/install/install-over, reset, second uninstall, second confirmation, executor lifecycle helper, manual Gateway/Ollama action, manual file/config/state repair, Dashboard semantic action, model/recovery action, source/product/test/workflow edit, release/tag/merge, or force push.

After Task-184 report publication, stop for ChatGPT review. Reinstall remains unauthorized.
