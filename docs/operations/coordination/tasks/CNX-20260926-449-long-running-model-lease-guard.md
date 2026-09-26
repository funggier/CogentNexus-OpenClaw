# CNX-20260926-449 — Long-Running Model Lease Guard

Status: `ACTIVE`
Owner: ChatGPT
Executor: ChatGPT
Parent: `CNX-20260926-448-native-ollama-terminal-boundary-and-long-running-semantics.md`
Baseline release: `v0.9.8` (immutable)
Working branch: `cnx-449-long-running-model-lease-guard`
GitHub issue: `#41`

## Objective

Prevent slow local Ollama inference from being mistaken for a hard-hung Gateway on low-throughput machines.

## Production evidence

Fresh CNX-448 qualification showed `ollama/qwen3.8:27b` still computing when the external Host saw two failed Gateway fast probes and authorized `host_direct_model_gateway_interruption_authorized` before the model-call deadline.

Current behavior in `host_v091.supervisor_tick()`:

1. lightweight Gateway probe fails;
2. sleep only `HARD_HANG_CONFIRM_DELAY_SECONDS = 1.0`;
3. second probe fails;
4. if startup grace is inactive, restart Gateway immediately.

That behavior does not distinguish a genuinely dead Gateway from one temporarily unable to answer while a large local model consumes CPU/RAM.

## Required semantics

1. Slow is not equivalent to hung.
2. Default Direct model-call lease for `provider=ollama` becomes 45 minutes.
3. Default Direct model-call lease for non-Ollama providers remains 15 minutes.
4. Existing explicit `timeoutMs` override remains authoritative within current 1–60 minute bounds.
5. If Gateway probes fail but there is an accepted/waiting Direct model call with an unexpired lease, the external Host must not restart Gateway.
6. The Host should return explicit `long-running-protected` evidence including call/provider/model/deadline.
7. After the active lease expires, existing stall/hard-hang recovery remains reachable.
8. Existing exact Gateway boot-interruption recovery, generation fences, delivery fences, and exactly-once behavior remain unchanged.
9. Provider/model/auth selection remains OpenClaw-owned.
10. `v0.9.8` remains immutable.

## TDD

RED/GREEN coverage must prove:

- Ollama default lease = 45 minutes;
- non-Ollama default lease = 15 minutes;
- explicit timeout override still wins;
- double failed Gateway probe + active unexpired Direct lease does not call `_restart_unresponsive_gateway`;
- expired/no lease preserves existing restart behavior;
- CNX-448 terminal-boundary tests remain GREEN;
- existing Host/recovery tests remain GREEN.

## Primary repair surfaces

- `plugins/cogentnexus-openclaw/src/v091-direct-model-call-lease.ts`
- `skills/cogentnexus-openclaw/scripts/host_stall_v091.py`
- `skills/cogentnexus-openclaw/scripts/host_v091.py`

## Local qualification checkpoint

Implemented and locally GREEN:

- Ollama default Direct lease: 45 minutes;
- non-Ollama default: 15 minutes;
- explicit timeout override preserved;
- unexpired active Direct lease fences probe-only Gateway restart;
- guard expires exactly at deadline;
- existing post-deadline recovery path remains unchanged.

Validation:

- focused Host/recovery Python: `40 passed`;
- focused lease + CNX-446 + CNX-448: `16/16 PASS`;
- full Python: `747 passed, 5 skipped, 38 subtests passed`;
- full Vitest: `94 files / 442 tests PASS`;
- build/evaluation/plugin validation/audit/diff-check: PASS;
- evaluation evidence SHA-256: `71bff654a2f3005f1528bb6377bdb4145dcee30fa216ae1012299b2e38debd28`.

## Current classification

`CNX449_LOCAL_GREEN_CI_PENDING`
