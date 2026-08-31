# Startup Policy

Startup reconciles durable intent before waking work.

1. read controller mode and desired Gateway/provider state;
2. apply terminal/cancellation fences;
3. reconcile stale sessions/leases/recovery residue;
4. restore only eligible pending work;
5. keep PASSTHROUGH native and MAINTENANCE stopped;
6. in MANAGED mode, enforce CNXCLAW recovery ownership before native restart continuation can create a competing Ticket/inference.

Startup hygiene is part of recovery correctness: stale running-session residue or queued native continuation must not manufacture new authority.
