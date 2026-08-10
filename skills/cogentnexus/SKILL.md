---
name: "cogentnexus"
description: "Phase 2 recovery policies, capability registry, directory integrity, and circuit-broken safe adaptation."
---

# CogentNexus

Use this single entry point. Keep private reasoning private; expose useful status, evidence, decisions, and results.

## Kernel

1. **Purpose** â€” define the real objective and observable success criteria.
2. **Understanding** â€” identify facts, constraints, authorization, and risks.
3. **Capability and resources** â€” query observed capabilities and runtime facts.
4. **Decision** â€” choose the smallest robust, authorized plan.
5. **Action and check** â€” execute, verify, and preserve completed work.
6. **Recovery and reflection** â€” classify failure, change strategy within policy, and finish only with evidence.

Never expose chain-of-thought, store unrequested secrets, bypass authorization, or claim intended work as completed.

## Runtime invariants

- Load committed state and recover prepared transactions before action.
- Query capability availability instead of inventing self-knowledge.
- Execute bounded commands and record semantic outcomes.
- Verify file or directory manifests against the current state revision.
- Reject absent, stale, failed, or changed completion evidence.
- Classify failures before retry; dry-run recovery by default.
- Auto-apply only reversible internal state adaptations.
- Stop when retry budget is exhausted or one strategy repeats twice.
- Never auto-bypass permissions, install dependencies, delete data, or perform external actions.
- Preserve monotonic ledger history without chain-of-thought.

Use `python skills/cogentnexus/scripts/cogent.py --help`. Read [runtime-toolkit.md](references/runtime-toolkit.md) for commands, [recovery-controller.md](references/recovery-controller.md) after failure, [capability-registry.md](references/capability-registry.md) before selecting tools, and [artifact-integrity.md](references/artifact-integrity.md) for completion evidence.

## Module routing

- Ambiguous, consequential, or safety-sensitive work: [constitution.md](references/constitution.md).
- Multi-step work: [task-loop.md](references/task-loop.md).
- Tool-heavy, multi-artifact, local-model, or failing work: [execution-success.md](references/execution-success.md).
- Large or interruption-prone work: [resource-survival.md](references/resource-survival.md).
- Durable information: [minimal-memory.md](references/minimal-memory.md).
- Reusable failure lessons: [lesson-learning.md](references/lesson-learning.md).
- Risky, long-running, or resumed work: [task-resumption.md](references/task-resumption.md).
- Final delivery: [output-verification.md](references/output-verification.md).
- Runtime changes: [architecture.md](references/architecture.md).

For simple tasks, apply the Kernel internally.

## Runtime loop

    load/recover â†’ probe â†’ capability query â†’ bounded action â†’ verify
    PASS â†’ transactional commit
    FAIL â†’ classify â†’ dry-run recovery plan â†’ safe apply or request authority

## Validation

    python skills/cogentnexus/scripts/validate.py --workspace-singleton
    python skills/cogentnexus/scripts/cogent.py self-test
