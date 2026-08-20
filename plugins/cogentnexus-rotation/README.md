# CogentNexus OpenClaw Bridge — v0.9.1

This plugin is the OpenClaw-side bridge for CogentNexus Ticket-first admission, Direct Recovery, delivery continuity, session/generation fencing, and compatibility ownership rules.

## Current accepted recovery wiring

The release entry installs the current recovery boundary before legacy Ticket-first intake where ordering matters.

### v094 Direct Recovery

- pins recovery to the original provider/model;
- records runtime provenance;
- preserves first `response_ready_at`;
- aborts/refuses output when durable authority becomes terminal;
- applies a read-only SQLite busy timeout;
- treats transient SQLite BUSY/WAL contention as an inconclusive authority read rather than revocation;
- emits file-only runtime error diagnostics that must not alter recovery semantics.

### v095/v096/v097/v098

- Direct lane ownership fencing;
- recursive self-intake prevention;
- post-restart liveness;
- startup/recovery-session residue hygiene.

### v099 Native Restart Ownership

OpenClaw 2026.7.1-2 may enqueue its own restart continuation after Gateway recovery. The v099 `before_agent_run` fence consumes only the exact native restart shape when durable state proves:

- same owner session;
- same generation;
- Host-authorized original timeout;
- pending/running CNX Direct Recovery;
- queued original prompt exactly matches the durable Ticket prompt.

Unreadable/missing DB fails open to native behavior. Ordinary prompts are never globally suppressed.

## Acceptance

Recovery Core checkpoint: `eadb89099637d24f96e265a500d66c577aa939a3`.

The accepted Test A v16 completed with a single recovery attempt, no duplicate Ticket, no recursive intake, no escaped database-lock retry, original model provenance, one durable result, and confirmed delivery.

## Development validation

```sh
npm ci
npx vitest run src/v094-direct-recovery.test.ts --config ./vitest.config.ts
npx vitest run src/v099-native-restart-ownership.test.ts --config ./vitest.config.ts
npm test
npm run evaluation
npm run plugin:validate
```

The repository ignores `dist/`; release validation regenerates distribution output and checks it through the build/package pipeline rather than treating generated files as source-of-truth.

See the root `README.md` and `docs/CURRENT_STATE.md` for supported operational scope.
