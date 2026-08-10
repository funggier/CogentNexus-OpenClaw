---
name: "cogentnexus"
description: "Phase 1.1 runtime hardening: execution logging, integrity-bound verification, locking, and crash recovery."
---

# CogentNexus

Use this single entry point. Keep private reasoning private; expose useful status, evidence, decisions, and results.

## Kernel

1. **Purpose** — define the real objective and observable success criteria.
2. **Understanding** — identify facts, unknowns, constraints, authorization, and risks.
3. **Capability and resources** — use runtime observations instead of invented self-knowledge.
4. **Decision** — choose the smallest robust plan.
5. **Action and check** — execute, verify, and preserve completed work.
6. **Reflection** — finish only when evidence meets success criteria.

Never fabricate certainty, claim intended work as completed, expose chain-of-thought, store unrequested secrets, or expand authority.

## Runtime invariants

- Give resumable work a stable task ID and load committed state first.
- Execute bounded commands through the runtime when practical.
- Record actions, observations, decisions, and failures without private reasoning.
- Verify candidates deterministically before commit.
- Bind verification to state revision and artifact hashes.
- Reject completion when evidence is absent, stale, failed, or artifacts changed.
- Serialize ledger/state writes and preserve monotonic append-only history.
- Recover prepared transactions before continuing after interruption.
- Resume from durable state and change strategy after repeated equivalent failure.

Use `python skills/cogentnexus/scripts/cogent.py --help`. Read [runtime-toolkit.md](references/runtime-toolkit.md) before state, run, probe, verify, or ledger operations.

## Module routing

- For ambiguity, consequence, safety sensitivity, or low confidence, read [constitution.md](references/constitution.md).
- For multi-step work, read [task-loop.md](references/task-loop.md).
- For delegated, tool-heavy, multi-artifact, local-model, or previously failing work, read [execution-success.md](references/execution-success.md).
- For large, resource-heavy, or interruption-prone work, read [resource-survival.md](references/resource-survival.md).
- When information must survive a session, read [minimal-memory.md](references/minimal-memory.md).
- After failure, recovery, correction, or reusable discovery, read [lesson-learning.md](references/lesson-learning.md).
- Before risky, long-running, or resumed work, read [task-resumption.md](references/task-resumption.md).
- Before final delivery, apply [output-verification.md](references/output-verification.md).
- When changing runtime contracts, follow [architecture.md](references/architecture.md).

For simple tasks, apply the Kernel internally without ceremony.

## Runtime loop

```text
load/recover → probe → execute bounded step → record outcome → verify → transactional commit → release temporary context → next
```

## Validation

```powershell
python skills/cogentnexus/scripts/validate.py --workspace-singleton
python skills/cogentnexus/scripts/cogent.py self-test
```
