# Coordination Status

Status: `ACTIVE`
State: `CNX453_PHYSICAL_GREEN_CLOSEOUT_CI_PENDING`
Task: `CNX-20260926-453-scheduled-supervisor-direct-lease-fence.md`
Branch: `cnx-453-supervisor-direct-lease-fence`
Candidate: `f90a67b739ed60355c9194407f6b7e20309a5918`
GitHub issue: `#45`
Baseline release: `v0.9.8` (immutable)

## Accepted physical result

CNX-453 follow-up passed exact-SHA CI 3/3 and physical long-running requalification. The scheduled Supervisor no longer performs probe-only destructive recovery during an unexpired Direct lease, startup boundary settlement closes stale execution evidence, and the Windows recovery budget is `PT15M` with `IgnoreNew`.

Live run `CNXT-41b9af1b-a2e9-48ff-81b4-b1d468fbc6da` completed after two model calls: ~23m04s tool-use continuation plus ~3m53s terminal call, with one delivery and no outbox residue.

`OLLAMA_KEEP_ALIVE=6h` is persistent and confirmed active in the running Ollama server.

CNX-451 remains the next active objective after this closeout CI. CNX-452 remains backlog for hard-pressure compact/resume semantics.

## Current classification

`CNX453_PHYSICAL_GREEN_CLOSEOUT_CI_PENDING`
