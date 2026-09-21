# CogentNexus-OpenClaw Flexible Roadmap

**Updated:** 2026-09-21

This roadmap is directional and evidence-driven. A phase advances because its gate passes, not because code exists.

## Current position — v0.9.6 release convergence

CNX-442 closed the authoritative Stop/session-queue defect by moving later owner ingress behind a durable pre-dispatch FIFO barrier. Final physical acceptance on OpenClaw 2026.9.5 proved no successor Host run after Stop and zero inference for the held cancelled Ticket.

CNX-443 is the current release-convergence phase:

- reconcile current documentation with the accepted runtime;
- add MIT licensing;
- align version/release metadata to v0.9.6;
- retain historical evidence without presenting it as current guidance;
- pass complete release validation;
- publish and independently verify v0.9.6.

## Short term — v0.9.6 publication

Required gates:

1. current docs contain no misleading active v0.9.4/v0.9.5 release-state claims;
2. current branch/watch instructions do not recreate retired automation;
3. MIT License is present and linked;
4. VERSION/package/manifest/lock/CI release contract agree on 0.9.6;
5. namespace/baseline/skill/Python/plugin tests pass;
6. package dry-run and release archive verification pass;
7. exact candidate SHA is frozen and pushed;
8. required GitHub checks are terminal and acceptable;
9. release workflow publishes tag/assets/checksums against the exact candidate;
10. public release identity and checksums are independently verified.

## Medium term — compatibility and resilience evidence

After v0.9.6 publication:

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
