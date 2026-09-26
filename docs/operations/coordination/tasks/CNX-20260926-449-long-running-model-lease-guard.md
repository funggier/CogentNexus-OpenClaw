# CNX-20260926-449 — Long-Running Model Lease Guard

Status: `COMPLETE`
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

## Physical installed-candidate qualification

- Exact candidate SHA: `dfb3706e7c11e61cc7987a7e4928f3c5d7203435`.
- Exact-SHA GitHub CI: Validate `36224230322`, Windows Installer Pack `36224230304`, PS5.1 `36224230318` — all SUCCESS.
- Supported install-over: exit `0`; MANAGED generation `36`; Gateway/OpenClaw `2026.9.5` healthy; supervisor healthy; Ollama healthy.
- Source/installed payload identity: `296` files, fingerprint `561c3903d2bb0476c37912b10941587ea76f0e07ac26e095d02bde08a04009c9` on both sides.
- Fresh live `ollama/qwen3.8:27b` call recorded a durable 45-minute lease (`timeoutMs=2700000`).
- Installed Host deterministic failed-probe proof returned `gateway-long-running-protected` and did not invoke the restart sentinel.
- Natural scheduled supervisor continued successfully during the live call; Gateway child PID stayed `38760`.
- The live model call ran `1,210,862 ms` (~20m10.9s), exceeding the old 15-minute boundary by >5 minutes, then completed successfully with marker `CNX449_OLLAMA_LONG_RUNNING_OK`.
- `response_ready` occurred after model/inference end, preserving the CNX-448 terminal fence.
- Isolated headless test Ticket was explicitly cancelled after evidence capture; final runtime has `pendingOutbox=0`.
- Headless CLI return-to-caller receipt semantics are tracked separately as Task 450 / GitHub issue #42.

## Final classification

`CNX449_LONG_RUNNING_OLLAMA_GUARD_GREEN`
