# CogentNexus-OpenClaw Flexible Roadmap

**Updated:** 2026-09-22

This roadmap is directional and evidence-driven. A phase advances because its gate passes, not because code exists.

## Current position — v0.9.7 exact Gateway-interruption recovery

v0.9.6 is the latest published accepted release. CNX-444 opens the v0.9.7 line after a genuine Discord turn exposed a recovery gap across an OpenClaw Gateway process replacement.

The defect is narrow but fundamental:

- a Direct Ticket and model call were durably recorded;
- the external Host confirmed the Gateway was unresponsive;
- the Gateway was replaced while the model call was still active;
- the old process could no longer emit `model_call_ended` / `agent_end`;
- provider-neutral safety correctly prevented timer-only destructive recovery;
- the model-call row remained `active` and the Ticket stranded until OpenClaw's configured 2700-second whole-run timeout.

v0.9.7 repairs that exact process-boundary gap without making elapsed time destructive authority.

## Short term — CNX-444 / v0.9.7 qualification

Required gates:

1. RED reproduces the missing exact Gateway-interruption path.
2. Confirmed hard-hang recovery orders `prepare -> stop/quiesce -> classify -> start`.
3. Eligible active Direct calls are converted to pending Direct Recovery while inference is impossible.
4. Gateway-interruption event/outcome evidence is distinct from deadline/timeout evidence.
5. Response-ready, delivery, terminal, cancellation, workflow and owner-generation fences remain authoritative.
6. Healthy slow local-model inference is never regenerated merely because the observational 15-minute deadline elapsed.
7. Provider/model/auth/routing ownership remains OpenClaw-owned; CNX does not restart or reroute a provider as part of this repair.
8. Focused and full Python suites pass.
9. Full plugin/Vitest, evaluation, package validation and production audit pass.
10. VERSION/package/manifest/lock/CI release contract agree on 0.9.7.
11. Windows install-over/lifecycle acceptance passes on OpenClaw 2026.9.5.
12. Live exact interruption/recovery proof demonstrates one authorized recovery and no duplicate inference/delivery.
13. Exact candidate SHA is pushed and GitHub validation passes.
14. Only then may v0.9.7 be published and independently checksum-verified.

## Accepted predecessor

CNX-443 / v0.9.6 remains final release GREEN:

- public tag/release `v0.9.6`;
- accepted release SHA `db8433676c2412706ef3b3966c97e3509f2255c8`;
- OpenClaw 2026.9.5 physical lifecycle acceptance;
- authoritative Stop/session FIFO acceptance;
- MIT License and documentation convergence.

The v0.9.6 tag/release must not be rewritten.

## Medium term — compatibility and resilience evidence

After v0.9.7:

- formalize a newer OpenClaw regression dependency baseline rather than relying only on the older 2026.7.1-2 dev pin;
- expand explicit compatibility testing around OpenClaw 2026.9.x+;
- abrupt machine power-loss/cold-boot continuation;
- high-concurrency/long-soak behavior;
- disk-full/database-corruption handling;
- stronger external-side-effect adapters with idempotency/receipt/read-after-write evidence.

## Long term — durable intent across replaceable intelligence/runtime

```text
human intent
-> durable accepted work
-> replaceable runtime/intelligence workers
-> interruption/failure
-> durable reconciliation
-> resume only incomplete work
-> deliver without duplicating completed effects
```

Preserve recursively:

- durable intent outranks transient model memory;
- responsibility-local data and policy;
- terminal evidence fences duplicate work;
- provider/model replacement must not silently redirect intent;
- irreversible effects require explicit reconciliation evidence;
- scaling coordination must not weaken artifact identity or proof.

## Roadmap movement rule

Move forward only when the relevant evidence gate passes. If evidence exposes a narrower defect, creating a repair/requalification phase is correct behavior rather than schedule failure.
