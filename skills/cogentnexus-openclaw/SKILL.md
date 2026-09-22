---
name: "CogentNexus-OpenClaw"
description: "Durable Host-managed continuity, lifecycle control, session serialization, recovery, and verified execution for OpenClaw work."
---

# CogentNexus-OpenClaw

**Current source/release line:** `v0.9.7`
**Latest physical OpenClaw acceptance:** `2026.9.5 (ec9c1a1)`
**Regression/dev OpenClaw pin:** `2026.7.1-2`
**Managed local provider:** Ollama
**Cloud/model/auth routing:** OpenClaw-owned pass-through

CogentNexus-OpenClaw separates **continuity** from **execution depth**. Eligible owner input may be durably admitted before inference without forcing ordinary DIRECT work into a heavyweight workflow.

Keep private reasoning private. Expose useful status, evidence, decisions, and results.

## Authority order

1. Preserve higher-priority safety, authorization, and platform constraints.
2. Preserve the user's intended outcome.
3. Respect durable Ticket/session/generation state.
4. Choose the lightest reliable execution lane.
5. Claim consequential completion only from evidence.

## Request lanes

- **DIRECT** — ordinary conversation, explanation, drafting, simple questions.
- **LOOKUP** — focused read-only retrieval.
- **ACTION** — bounded reversible execution with proportionate verification.
- **STAGED** — multi-step, interruption-prone, dependency-heavy, or independently verified work using durable workflow state.

Ticket creation does not imply STAGED execution.

## Same-session serialization

Later eligible owner input in the same generation is held at `before_dispatch` while an older Ticket is non-terminal. This keeps queued input outside the native Host queue.

A valid user Stop advances owner generation once and cancels active + held Tickets. Held cancelled ingress is consumed before Host queue admission, preventing a cancelled successor inference.

## Host-managed recovery

For a committed Direct turn interrupted before durable response, bounded recovery may be authorized only from durable evidence. Recovery preserves Ticket owner generation and original provider/model provenance.

A confirmed Gateway process replacement is exact interruption evidence for active Direct calls owned by the old Gateway generation, but recovery authority is persisted only after Gateway inference is quiesced. An elapsed model-call deadline alone remains observational and does not authorize replacement inference.

Restart recovery for a held pre-dispatch message is limited to accepted ingress that never bound to a Host run (`bound_run_id IS NULL`) and remains FIFO-fenced.

## Provider boundary

Managed local-provider ownership is Ollama-only. OpenClaw owns Cloud credentials, provider/model selection, routing, runtime probing, and Cloud recovery.

Do not silently fall back to another provider.

## Operating modes

- **MANAGED** — Ticket-first continuity and managed lifecycle ownership.
- **PASSTHROUGH** — provider/model/auth remain OpenClaw-owned; managed provider ownership inactive.
- **MAINTENANCE** — deliberate stop; durable state preserved and recovery must not fight operator intent.

## Runtime invariants

- Recover committed state before replacement action.
- Never repeat external side effects blindly after interruption.
- `response_ready` is durable and immutable.
- Delivery retry must not silently regenerate inference.
- Fence duplicate workers with leases/generations.
- Respect terminal/cancelled state.
- Periodic supervision performs no model inference.
- Accepted work must become completed/delivered, cancelled, or explicitly failed.

## Module routing

Do not load heavy CogentNexus-OpenClaw modules merely to answer an obvious DIRECT request.

Load references lazily:

- [constitution.md](references/constitution.md) — ambiguity/consequence/safety.
- [task-loop.md](references/task-loop.md) — multi-step loop.
- [execution-success.md](references/execution-success.md) — tool-heavy/failing work.
- [resource-survival.md](references/resource-survival.md) — interruption/resource survival.
- [minimal-memory.md](references/minimal-memory.md) — minimal durable memory.
- [lesson-learning.md](references/lesson-learning.md) — reusable lessons.
- [task-resumption.md](references/task-resumption.md) — resume from committed state.
- [output-verification.md](references/output-verification.md) — final verification.
- [architecture.md](references/architecture.md) — architecture baseline.
- [runtime-toolkit.md](references/runtime-toolkit.md) — runtime tooling.
- [recovery-controller.md](references/recovery-controller.md) — recovery.
- [capability-registry.md](references/capability-registry.md) — capabilities.
- [artifact-integrity.md](references/artifact-integrity.md) — artifact identity.
- [runtime-supervisor.md](references/runtime-supervisor.md) — supervision.
- [concurrency-manager.md](references/concurrency-manager.md) — admission/concurrency.
- [context-continuity.md](references/context-continuity.md) — context.
- [scheduler-adapters.md](references/scheduler-adapters.md) — scheduling.
- [startup-policy.md](references/startup-policy.md) — startup policy.

## Validation

```sh
python scripts/check_namespace_isolation.py
python scripts/check_baseline_consistency.py
python skills/cogentnexus-openclaw/scripts/validate.py --workspace-singleton
python skills/cogentnexus-openclaw/scripts/workflow.py self-test
python skills/cogentnexus-openclaw/scripts/cogent.py self-test
python skills/cogentnexus-openclaw/scripts/runtime.py self-test
python -m pytest -q
```

Historical versioned coordination/release artifacts remain evidence for the state they describe and are not rewritten to match later releases.
