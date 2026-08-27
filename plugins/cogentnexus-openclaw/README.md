# CogentNexus-OpenClaw Bridge — v0.9.3

This plugin is the OpenClaw-side bridge for CogentNexus-OpenClaw Ticket-first admission, Direct Recovery, durable delivery continuity, session/generation fencing, and compatibility ownership rules.

Current development line: **v0.9.3**.  
Validated OpenClaw baseline: `2026.7.1-2`.  
Current managed provider at the product/CLI boundary: **Ollama only**.

The Bridge preserves recovery and delivery invariants; provider lifecycle selection is owned by the external v0.9.3 Host/CLI facade.

## Recovery wiring

The release entry installs the current recovery boundary before legacy Ticket-first intake where ordering matters.

### Direct Recovery

- pins recovery to the original provider/model;
- records runtime provenance;
- preserves first `response_ready_at`;
- aborts/refuses output when durable authority becomes terminal;
- applies a read-only SQLite busy timeout;
- treats transient SQLite BUSY/WAL contention as an inconclusive authority read rather than revocation;
- emits redacted/file-only runtime diagnostics where required without changing recovery semantics.

### Native restart ownership

OpenClaw `2026.7.1-2` may enqueue its own restart continuation after Gateway recovery. The ownership fence consumes only the exact native restart shape when durable state proves the continuation belongs to the same CNXCLAW-owned recovery.

Unreadable/missing durable authority fails open to native behavior. Ordinary prompts are never globally suppressed.

### Dashboard durable delivery observability

Task 104 instrumentation is required to remain behavior-neutral:

- non-final callbacks must retain predecessor short-circuit behavior;
- already-owned callbacks must retain predecessor short-circuit behavior;
- supported final callbacks retain predecessor property/dispatcher evaluation order;
- diagnostic output is redacted/bounded and must not expose prompt/response/run identifiers or semantic content.

Instrumentation observes the delivery boundary; it does not create new semantic reads, calls, ordering, or durable diagnostic rows.

## Accepted checkpoint vs current candidate

Accepted Recovery Core checkpoint: `eadb89099637d24f96e265a500d66c577aa939a3`.

The accepted live Test A v16 demonstrated a single recovery attempt, no duplicate Ticket, no recursive intake, no escaped database-lock retry, original model provenance, one durable result, and confirmed delivery.

That checkpoint is historical technical evidence. It is not by itself final v0.9.3 acceptance. The current v0.9.3 candidate must pass repository stabilization, package proof, exact candidate freeze, and separate real-Windows acceptance.

## Development validation

```sh
npm ci
npm test
npm run evaluation
npm audit --omit=dev
npm run plugin:validate
```

The repository ignores generated `dist/` output; release/package validation must build the distributable payload and verify required runtime files inside the candidate archive rather than treating generated output as source-of-truth.

See root `README.md` and `docs/CURRENT_STATE.md` for current operational scope.
