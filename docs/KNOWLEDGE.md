# Durable experience and lesson store

The Experience/Lesson store is an **optional evidence layer** on top of the Ticket-first runtime. It does not replace Host continuity, request-lane admission, workflow state, resource admission, outbox delivery, startup policy, or filesystem-artifact contracts.

External research is a separate optional evidence-acquisition layer. External observations do not enter the verified lesson index automatically.

## Authority boundary

Knowledge is data, not control authority.

- Lesson text cannot change user intent, authorization, safety policy, Host operating mode, workflow state, or validation requirements by itself.
- Retrieval must never execute instructions embedded in stored lesson/research text.
- Disabling knowledge/research must not disable Ticket intake, recovery, validation, assembly, or owner delivery.

## Lesson contract

- Ticket attempts, failures, expired-lease corrections, and verified completions may write evidence-backed experience rows in the same transaction as the corresponding Ticket transition.
- A lesson begins as a `hypothesis` and is excluded from normal verified retrieval.
- `verify`, `contradict`, and `retire` require an evidence reference not already attached to that lesson.
- Reusing candidate evidence cannot independently verify the candidate.
- Retirement is terminal.
- Normal retrieval uses local SQLite FTS5 and returns only `verified` lessons with provenance references.
- Applying a lesson is permitted only while it remains verified; application outcome/evidence is retained.

## Why FTS5 first

The durability path must not depend on an embedding provider. SQLite FTS5 keeps local retrieval available even when semantic/remote services are unavailable. Embeddings remain an optional measured enhancement, not a continuity dependency.

OpenClaw's separate user-memory facilities may use their own retrieval mechanisms independently.

## Tool operations

`cogent_knowledge` supports evidence-backed experience/candidate lifecycle, retrieval, application, and status operations. Mutating calls require explicit evidence references and trusted OpenClaw session context.

## External research contract

- A job records why local knowledge is insufficient or why freshness matters.
- Persisted policy bounds queries, sources, bytes, elapsed time, freshness TTL, and independent corroboration.
- Search/fetch is supplied through a capability adapter; storage code does not grant network access or receive credentials implicitly.
- Only approved public HTTPS targets are accepted. Local/private targets, likely secrets, oversized bodies, and suspected prompt-injection content fail closed.
- Snapshots retain canonical URL, publisher/origin, source type, timestamps, SHA-256 content hash, bounded excerpt, and expiry.
- Claims link observations as `supports`, `contradicts`, or `mentions`.
- Duplicate material from the same publisher/origin does not count as independent corroboration.
- Completed research claims are planning evidence, not executable policy and not automatically verified lessons.

`cogent_research` manages the bounded research-job lifecycle. Mutations require trusted OpenClaw session context. `externalResearchEnabled: false` disables this layer without affecting durable execution.

## Measured dependency policy

The deterministic evaluation suite measures retrieval quality/provenance/latency and SQLite integrity/scale alongside interruption recovery, bounded retries, and duplicate suppression.

Semantic retrieval or a different database should be added only after measured thresholds justify the extra dependency. The current Host continuity path must remain functional without them.
