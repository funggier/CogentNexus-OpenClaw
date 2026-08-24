# Task Resumption

Resume from the last durable committed state, not from remembered reasoning.

## Direct work

If no durable response exists and Host proves a pre-response interruption, Direct Recovery may re-enter inference once under the same session/generation/model provenance. If a durable result already exists, resume delivery only.

## Staged work

Resume from committed workflow/task checkpoints, verified artifacts and lease/generation state. Do not replay already-verified external effects without reconciliation.

## Terminal fences

Cancellation, completion and explicit failure are terminal authorities. Stale startup/recovery residue must not reopen them.
