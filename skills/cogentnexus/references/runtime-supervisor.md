# Runtime Supervisor

CogentNexus supervision is deterministic and performs **no model inference** inside the periodic scheduler process.

In v0.8, distinguish two layers:

1. **Host supervisor entry point** — reads Host operating/desired state and decides whether runtime reconciliation is allowed.
2. **Runtime supervisor** — probes health/resources, applies cooldown/retry/circuit-breaker policy, discovers resumable workflows, and launches separately fenced controllers when authorized.

Normal automatic scheduling should enter through the Host Controller so PASSTHROUGH and MAINTENANCE intent cannot be bypassed accidentally.

## Low-level runtime commands

```text
python skills/cogentnexus/scripts/runtime.py supervisor doctor
python skills/cogentnexus/scripts/runtime.py supervisor tick
python skills/cogentnexus/scripts/runtime.py supervisor tick --execute-safe
python skills/cogentnexus/scripts/runtime.py supervisor status
python skills/cogentnexus/scripts/runtime.py supervisor history
```

The Host Controller may invoke these after confirming MANAGED/running intent.

## Tick behavior

A tick may observe:

- Gateway/provider health;
- memory/disk pressure;
- cooldown/retry/circuit-breaker state;
- Ticket/workflow leases and generations;
- bound session/context pressure;
- resumable non-terminal workflows;
- pending delivery state.

Without `--execute-safe`, workflow discovery is observation-only. With it, the runtime supervisor may launch a bounded number of detached workflow controllers. It still does not execute LLM inference inside the scheduler process.

## Ownership rules

- PASSTHROUGH -> Host supervisor does no CogentNexus recovery action.
- MAINTENANCE/stopped -> Host supervisor does not restart managed runtime.
- MANAGED/running -> Host supervisor may reconcile confirmed unplanned failures and invoke safe runtime supervision.
- Cancelled/terminal work -> never relaunch.
- Stale generation/lease -> cannot regain authority.
- Existing durable response -> retry delivery rather than inference.

Runtime evidence is stored under `.cogent/runtime`; workflow evidence remains under `.cogent/workflows`.
