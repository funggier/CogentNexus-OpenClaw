# Active Coordination Task

Status: `IN_PROGRESS`
State: `V095_PROVIDER_RUNTIME_COMMAND_REPAIR`
Execution mode: `SINGLE_EXECUTOR__ROOT_CAUSE_TDD`
Task ID: `CNX-20260909-315`
Parent: `CNX-20260907-314`
Base release: `v0.9.4`
Base commit: `40352b3c8b6b9c98c1dfdead5d197f976976bc9f`
Working branch: `agent/v0.9.5-architecture-repair`

## Objective

Implement the approved CogentNexus-OpenClaw v0.9.5 provider-independent capability and local-provider command contract without changing the user's OpenClaw provider/model/auth route.

## Current phase

Plan 1 closeout: provider/runtime/command repair.

## Completed in current phase

- Canonical v0.9.5 Host authority state and v0.9.4 migration are implemented.
- Provider-neutral runtime, terminal-error claim/classification, recovery lifecycle hardening, and provider-independent capability registration are implemented.
- Normal CNX lifecycle commands no longer invoke provider routing.
- `cnxclaw cloud` is removed from the public CLI.
- Legacy lifecycle `--provider` input is rejected without transition.
- Canonical local Ollama adapter facade is present at `local_adapters_v095.py`; `local_adapter.py` remains a compatibility shim.
- Public `reset` now routes through `reset_v095.py`, which does not select, probe, start, stop, or commit a provider.
- Provider-switch invariant matrix tests are present.

## Current verification position

The last fully successful exact-head validation before the latest reset/adapter/doc commits was successful across Validate, Windows Python, macOS Python, PS5.1 Live Runner Smoke, PS5.1 Acceptance Smoke, and Windows Installer Pack Smoke.

A new Actions run for the resulting HEAD is required before Plan 1 can be declared green. Package dry-run must remain on public v0.9.4 metadata until release preparation.

## Remaining Plan 1 gate

1. Fresh exact-HEAD Actions must pass.
2. Provider-switch matrix must remain green.
3. No CNX lifecycle or local-adapter command may mutate OpenClaw routing.
4. Coordination checkpoint must record the final exact SHA and evidence.

## Hard fences

- No force push.
- No release, tag, or public-version mutation during Task315.
- No live provider/model/auth route mutation during source repair.
- Do not reduce Ticket, Durable, context, recovery, or delivery capability merely because OpenClaw selects a Cloud or unknown provider.
- Preserve v0.9.4 exact-delivery, owner-generation, terminal-fence, config-race, stale-wake, and recovery-safety fixes unless an equal-or-stronger v0.9.5 contract replaces them.
- Provider/model switching is OpenClaw-owned and must not cause CNX mode changes, Host-generation increments, mandatory Gateway restarts, policy mutations, or plugin enable/disable transitions.

## Next authority

Do not start Plan 2 until the final Plan 1 checklist is green on the exact resulting HEAD.
