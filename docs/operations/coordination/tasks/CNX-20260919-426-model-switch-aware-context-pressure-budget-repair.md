# CNX-20260919-426 — Model-Switch-Aware Context Pressure Budget Repair

Status: `READY_FOR_EXECUTION`

Parent: `CNX-20260919-425`

## Problem

Live OpenClaw 2026.9.4 provider/model switching is functional, but a same-session switch exposed a false CogentNexus context-pressure block.

Observed live session:

`agent:main:dashboard:7ce3cf7e-0ad6-4ed9-a17d-cf3b712954bb`

The operator switched from Ollama `qwen3:1.7b` to Ollama `qwen3.8:27b`.

For run:

`fd47fa35-8ff5-49cf-854c-fe0d076af784`

the OpenClaw transcript persisted a turn-local model snapshot:

- provider: `ollama`
- model: `qwen3.8:27b`

but CNX emitted:

- event: `context_pressure_deferred`
- contextWindow: `32768`
- projectedTokens: `28425`
- ratio: `0.867462158203125`
- level: `soft`

and blocked before inference.

The configured/discovered effective context window for `qwen3.8:27b` is `262144`.

## Root cause boundary

The production v0.9.1 context guard currently obtains the context window only from `sessions.describe` and falls back to `32768`.

OpenClaw 2026.9.4's typed `before_agent_run` hook context already supplies the authoritative turn-local fields:

- `modelProviderId`
- `modelId`
- `contextTokenBudget`
- `contextWindowSource`
- `contextWindowReferenceTokens`

The host contract defines `contextTokenBudget` as the resolved effective context-token budget after model/config/agent caps.

During a same-session model switch, `sessions.describe` may still describe the previous/persisted session model state when `before_agent_run` executes.

## Required semantics

1. When `ctx.contextTokenBudget` is a valid positive finite value, CNX context-pressure evaluation MUST use it as the exact turn context window.
2. The fresh session counter may still supply `totalTokens` / `totalTokensFresh`; only the stale context-window authority changes.
3. Do not use `max(sessionWindow, turnBudget)`. Switching to a smaller model must also become safer, not less safe.
4. If the host does not provide a valid turn context budget, preserve the existing `sessions.describe` / default fallback behavior.
5. Provider/model selection remains OpenClaw-owned. CNX must not become a provider/model router.

## TDD RED requirements

Add a focused CNX-426 test that proves:

- stale session window `32768`, fresh projected tokens around `28425`, turn budget `262144` => no context block;
- stale session window `262144`, turn budget `40960`, high fresh token count => context block;
- absent/invalid turn budget => legacy session-window behavior remains intact.

The RED suite must fail against the pre-repair production source.

## GREEN requirements

After the minimal repair:

- CNX-426 focused tests PASS;
- existing context-guard tests PASS;
- production wiring tests PASS;
- relevant CNX-423/CNX-425 admission/provider-selection regressions remain PASS;
- TypeScript/plugin validation PASS;
- full suite has no new failures beyond any already documented historical baseline.

## Live qualification

After source/package qualification:

1. install-over the qualified CNX plugin on the already-accepted OpenClaw 2026.9.4 live host;
2. restart only if required by the plugin lifecycle;
3. confirm Gateway health, plugin errors, Discord state, supervisor state, DB integrity and Ticket counters;
4. perform a bounded non-destructive model-switch context-budget qualification without changing OpenClaw provider/model ownership;
5. do not create semantic traffic unless needed to prove the repaired boundary.

## Final classifications

PASS:

`MODEL_SWITCH_CONTEXT_BUDGET_REPAIR_GREEN`

BLOCKED:

`BLOCKED_CONTEXT_BUDGET_AUTHORITY`

or a narrower evidence-backed blocker.

No release/tag/main mutation is authorized by this task.
