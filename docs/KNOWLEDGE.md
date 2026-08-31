# Knowledge, Evidence, and Durable Lessons

CogentNexus-OpenClaw separates **durable execution truth** from model memory. Tickets, workflow state, receipts, validators, artifact hashes, and terminal evidence live in durable state; model context is not the authority for whether work happened.

## Sources of truth

For operational decisions, prefer in this order:

1. durable Ticket/session/recovery state;
2. committed outbox/delivery receipts;
3. workflow checkpoints and validators;
4. artifact manifests/hashes;
5. verified reusable lessons;
6. reconstructed conversational context.

A model recollection must never override a terminal Ticket, cancellation fence, generation fence, or committed delivery receipt.

## Recovery knowledge

The accepted v0.9.1 baseline adds two important durable lessons:

- a transient SQLite BUSY read during authority polling is not proof that Host authority was revoked;
- OpenClaw native restart continuation is not a new user request when the exact session/generation/prompt envelope is already owned by durable CNXCLAW Direct Recovery.

These are architecture invariants, not heuristics to be guessed by the model.

## Lesson storage

Reusable lessons should contain provenance/evidence and be promoted only when they are stable enough to influence future work. Temporary reasoning and speculative diagnostics should not be stored merely because they were produced during one run.

## Context continuity

Context rotation/compaction may reduce conversational history, but durable work identity must survive independently. Recovery should reconstruct the minimum context required from durable records and verified artifacts rather than preserving unlimited model memory.

See `skills/cogentnexus-openclaw/references/lesson-learning.md`, `context-continuity.md`, and `minimal-memory.md` for internal routing details.
