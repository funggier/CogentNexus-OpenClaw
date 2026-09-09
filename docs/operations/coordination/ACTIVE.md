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

The current phase is Plan 1: provider/runtime/command repair. Production changes must follow RED -> minimal fix -> GREEN.

## Authoritative design

- `docs/superpowers/specs/2026-09-09-v0.9.5-architecture-repair-design.md`
- `docs/superpowers/specs/2026-09-09-v0.9.5-local-provider-command-contract.md`
- `docs/superpowers/specs/2026-09-09-v0.9.5-idle-quiescence-and-single-wake-contract.md`
- `docs/superpowers/plans/2026-09-09-v0.9.5-execution-index.md`

## Hard fences

- No force push.
- No release, tag, or public-version mutation during Task315.
- No live provider/model/auth route mutation during source repair.
- Do not reduce Ticket, Durable, context, recovery, or delivery capability merely because OpenClaw selects a Cloud or unknown provider.
- Preserve v0.9.4 exact-delivery, owner-generation, terminal-fence, config-race, stale-wake, and recovery-safety fixes unless an equal-or-stronger v0.9.5 contract replaces them.
- Provider/model switching is OpenClaw-owned and must not cause CNX mode changes, Host-generation increments, mandatory Gateway restarts, policy mutations, or plugin enable/disable transitions.

## Immediate next action

Task315 Step 2: write and verify failing Host-state/provider-independence migration tests before modifying production runtime code.
