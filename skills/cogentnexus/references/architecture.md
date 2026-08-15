# Architecture and Extension Contract

CogentNexus v0.8 uses a layered architecture. The canonical public baseline is [../../../docs/BASELINE.md](../../../docs/BASELINE.md).

## Layers

1. **Host Controller** — external deterministic continuity/lifecycle authority.
2. **OpenClaw Bridge** — plugin boundary for Ticket intake, owner/session binding, dispatch, recovery, context handoff, and delivery.
3. **Request lane policy** — DIRECT / LOOKUP / ACTION / STAGED, selected before heavy modules are loaded.
4. **Durable workflow runtime** — checkpointed controller, deterministic validators, bounded repair/review, artifact evidence.

The skill remains a modular monolith for discoverability, but CogentNexus as a system is no longer described as merely one OpenClaw skill. The Host Controller must remain useful when OpenClaw inference is unavailable.

## Repository contract

- `SKILL.md`: compact managed-execution entry point; must not force every request into heavy runtime behavior.
- `references/`: lazily loaded cognitive and operational contracts.
- `scripts/host.py`: external Host Controller CLI and deterministic mode/lifecycle ownership.
- `scripts/runtime.py`: deterministic runtime/supervisor/lifecycle primitives.
- `scripts/workflow.py`: durable workflow controller.
- `plugins/cogentnexus-rotation/`: OpenClaw bridge; the historical plugin ID is retained for compatibility.
- `templates/`: workspace/scheduler/deployment adapters.
- `.cogent/`: durable runtime state outside version control.

## Extension rules

Every new module or feature must:

- have one clear responsibility and authority boundary;
- preserve the continuity invariant;
- preserve PASSTHROUGH/native OpenClaw operation;
- avoid making DIRECT requests pay STAGED overhead;
- retain deterministic supervision without inference;
- define interruption/recovery and cancellation semantics;
- add validation/tests for observable behavior;
- avoid silently repeating external side effects after interruption.

Portable logic should remain in Python/TypeScript modules with platform-specific behavior behind adapters. Windows Task Scheduler, systemd, launchd, cron, Docker, and Kubernetes must preserve the same persisted-state and supervisor contracts.

Do not add nested `SKILL.md` files as a substitute for deterministic controller logic. Load references lazily rather than expanding the default model context.
