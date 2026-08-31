# Coordination Channel Status

**State:** `READY_HERMES`  
**Execution mode:** `WINDOWS_QUALIFIED_HARNESS_RESET_FRESH_STATE_REACCEPTANCE_HERMES`  
**Updated:** 2026-08-31 ICT  
**Transport:** GitHub repository history  
**Active task:** `CNX-20260831-183`

## Active work

[`tasks/CNX-20260831-183-hermes-qualified-harness-reset-fresh-state-reacceptance.md`](tasks/CNX-20260831-183-hermes-qualified-harness-reset-fresh-state-reacceptance.md)

Executor: Hermes/Codex. Coordinator / final reviewer: ChatGPT.

Standing model: executor-heavy / reviewer-light.

## Accepted repository/live state

Task 179:

`ACCEPTED_PASS — INTERACTIVE_LIFECYCLE_DELEGATION_REPAIR_ACCEPTED`

Exact repository candidate:

`f6392da3e4112ce441526d5ef19925c90a872b0b`

Task 181:

`ACCEPTED_PASS — HISTORICAL_TASK178_OUTER_OBSERVER_RETIRED_CLEAN_BOUNDARY_PROVEN`

Task 182:

`ACCEPTED_PASS — REPAIRED_CANDIDATE_INSTALL_OVER_ACCEPTED`

The accepted repair is now active on Windows. Active facade SHA-256:

`aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

Current pre-reset durable history remains the expected four-ticket state, including Task-171 historical delivery evidence. Reset is intended to remove this CNX-owned durable state while preserving program files, OpenClaw, Ollama, models, and unrelated namespaces.

## Fresh implementation correlation

At the accepted candidate:

- v0.9.3 injects Ollama for reset when provider is omitted;
- repaired legacy facade uses direct interactive delegation for reset/uninstall;
- host-control routes reset into provider-aware `lifecycle_v092`;
- ownership/provider/route/plugin bootstrap preflight occurs before confirmation;
- only exact `y` at `Continue? [y/N]: ` crosses the destructive boundary;
- the reset transaction itself owns native-route restoration, state recreation, DB bootstrap, policy, managed Ollama route activation, enable, Gateway boundary, verification, and final commit.

## Task 183 gate

Exactly one reset may be launched after fresh clean-process/runtime/durable preflight.

Use the qualified character-prompt/concurrent-drain/incremental-ledger harness. Persist prompt and input-intent events before sending one literal `y`. Do not retry if an outer shell/session times out or loses contact; inspect and continue observing the same process through durable ledger/process evidence.

PASS requires the reset child to exit `0`, emit `COGENTNEXUS-OPENCLAW RESET: PASS` and `State     : fresh-install MANAGED`, retain the accepted facade/release, restore healthy MANAGED Ollama routing, and remove reset-owned Ticket/event/delivery/model-call/session rows to zero while external OpenClaw/Ollama assets remain intact.

## Hard fence

Reset root invocation maximum: `1`.
Confirmation send maximum: `1`.
Semantic/model/recovery action budget: `0`.

No install/reinstall/install-over, uninstall, second reset, second `y`, executor lifecycle helper, Dashboard semantic action, manual repair, source/product/test/workflow edit, release/tag/merge, or force push.

After Task-183 report publication, stop for ChatGPT review. Uninstall remains unauthorized.
