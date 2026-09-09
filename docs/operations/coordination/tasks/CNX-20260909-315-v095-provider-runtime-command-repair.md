# CNX-20260909-315 — v0.9.5 Provider / Runtime / Command Repair

Status: `IN_PROGRESS`
Execution mode: `SINGLE_EXECUTOR__ROOT_CAUSE_TDD`
Branch: `agent/v0.9.5-architecture-repair`
Base release: `v0.9.4`
Base SHA: `40352b3c8b6b9c98c1dfdead5d197f976976bc9f`
Parent coordination task: `CNX-20260907-314` (historical release-provenance gate)

## Objective

Implement the first v0.9.5 repair phase so CogentNexus capability is independent of the inference provider selected by OpenClaw.

The target operator contract is:

```text
Provider/model routing      -> OpenClaw
CogentNexus lifecycle       -> cnxclaw top-level lifecycle commands
Local Ollama management     -> cnxclaw local ollama ...
```

## Authoritative specifications

- `docs/superpowers/specs/2026-09-09-v0.9.5-architecture-repair-design.md`
- `docs/superpowers/specs/2026-09-09-v0.9.5-local-provider-command-contract.md`
- `docs/superpowers/specs/2026-09-09-v0.9.5-idle-quiescence-and-single-wake-contract.md`
- `docs/superpowers/plans/2026-09-09-v0.9.5-provider-runtime-command-repair.md`
- `docs/superpowers/plans/2026-09-09-v0.9.5-execution-index.md`

## Required behavior

1. OpenClaw provider/model selection does not change CogentNexus capability.
2. Direct and Durable lanes remain available for every OpenClaw-supported provider, including unknown/future providers for which CogentNexus has no process adapter.
3. `cnxclaw start|stop|restart|enable|disable` do not select or rewrite provider/model routing.
4. Local Ollama lifecycle is exposed under `cnxclaw local ollama ...` and is route-neutral.
5. Legacy `--provider` and `cnxclaw cloud` behavior, if retained for compatibility, is deprecated and cannot reduce capability or mutate provider/model/auth routing.
6. v0.9.4 `passthrough + plugin enabled` migrates to v0.9.5 `active` without changing OpenClaw route/auth/model state.
7. Provider changes do not increment Host generation, force Gateway restart, mutate policy, or enable/disable the plugin.

## Hard fences

- No force push.
- No release/tag mutation.
- No live provider/model/auth route mutation during source repair.
- No production repair before a failing regression/contract test demonstrates the missing behavior.
- Preserve existing exact-delivery, terminal, owner-generation, config-race, stale-wake, and recovery safety boundaries.
- Do not infer the user's provider from credentials or model strings when migration does not require it.
- Do not add a new CogentNexus Cloud-provider routing framework.

## TDD sequence

### Phase A — coordination authority

- Update `ACTIVE.md` and `STATUS.md` to the real v0.9.5 line.
- Record Task315.

### Phase B — Host authority state

RED tests:

```text
managed -> active
maintenance -> maintenance
passthrough + plugin disabled -> disabled
passthrough + plugin enabled -> active
no desiredProvider authority in canonical v0.9.5 state
```

Then implement the minimal canonical Host-state migration.

### Phase C — plugin capability

RED tests prove legacy passthrough/provider-mode cannot block Durable admission, compaction continuation, or recovery while CNX is active.

Then remove provider-route capability gating.

### Phase D — command surface

RED tests prove:

```text
cnxclaw start -> no route mutation
cnxclaw local ollama start -> local Ollama only, no route mutation
legacy --provider -> no route selection
cnxclaw cloud -> no reduced capability / no route selection
```

Then implement the provider-neutral CLI and local Ollama adapter namespace.

### Phase E — local recovery isolation and docs

Prove Cloud/unknown-provider work does not wake or restart Ollama and update current operator docs to the three-way ownership model.

## Acceptance for Task315

Task315 may be marked complete only when:

- all focused Python tests for Host state, CLI/local adapter, Cloud compatibility and provider recovery pass;
- focused plugin provider-independence tests pass;
- plugin validation passes;
- repository remains runnable;
- no OpenClaw route/auth/model mutation is introduced by normal CNX lifecycle;
- exact HEAD and evidence are recorded in a coordination report.
