# Phase 6 durability and retrieval evaluation

This deterministic benchmark exercises CogentNexus against an isolated temporary SQLite database. It never reads or mutates the live runtime database.

It verifies:

- expired-lease interruption recovery with fencing-generation advancement;
- bounded validation retry followed by verified completion;
- duplicate intake and single side-effect suppression;
- verified-lesson top-1 precision, recall at 3, provenance coverage, and p95 retrieval latency;
- SQLite integrity, schema migrations, ticket volume, and p95 write latency.

Run from the plugin directory:

```bash
npm run evaluation
```

To retain the machine-readable report:

```bash
npm run build
node scripts/evaluate.mjs phase6-report.json
```

The command exits non-zero if any durability or retrieval gate fails. The report includes a canonical SHA-256 evidence digest and explicit decisions for optional semantic retrieval and a PostgreSQL adapter.

## Decision policy

Semantic retrieval is justified only when FTS5 falls below 0.90 top-1 precision or 0.90 recall at 3, or exceeds 50 ms p95 retrieval latency on the fixed fixture. PostgreSQL is justified only when observed ticket count exceeds 100,000 or SQLite write latency exceeds 100 ms p95 in the isolated evaluation.

These thresholds are evaluation gates, not permission to weaken durability. Optional retrieval or database adapters must remain replaceable and cannot become dependencies of Ticket intake, recovery, validation, assembly, or owner delivery.
