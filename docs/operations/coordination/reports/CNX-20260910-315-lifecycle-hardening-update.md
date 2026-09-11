# CNX-20260910-315 — v0.9.5 Lifecycle Hardening Update

## Repository position

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.5-architecture-repair`
- Base release: `v0.9.4`
- Public version remains unchanged at `0.9.4` during Task315.
- No v0.9.5 release/tag has been created.

## Work completed in this update

### 1. Terminal-error Supervisor consumption

Commit:

`167dca6a2801cc4b1b9db085d3013c28d53a24b3`

Supervisor now consumes an exact eligible terminal Direct model-call claim before falling back to legacy stall recovery, while retaining provider-neutral execution authority.

### 2. Partial-stop restoration hardening

Commit:

`7c8b32dd03f9185cad82936b18a3fda85a944545`

`recover_terminal_error_direct_model_call()` now arms Gateway restoration intent before invoking lifecycle stop. If stop raises after quiescing begins, the `finally` path still attempts lifecycle start.

### 3. Lifecycle failure-path coverage

Commit:

`800ffa2789edf093603c70e97bce19e23492d6c2`

Added `tests/test_v095_lifecycle_recovery.py` covering:

- prepare failure: no stop/start attempt;
- classification failure after stop: Gateway restoration is attempted;
- Gateway start failure: one restoration retry is attempted by the existing `finally` path;
- unhealthy Gateway after start: recovery reports failure without issuing a duplicate start;
- partial-stop failure is covered by the existing provider-neutral Supervisor test suite.

The tests preserve the recovery contract: lifecycle failures are surfaced rather than converted into fake success.

## Evidence and verification

The updated test source and production source were fetched back from the exact commit/branch and inspected.

The local execution environment cannot reach GitHub from the container, so a local `pytest` run could not be performed here. GitHub Actions should remain the authoritative execution proof.

At the time of this update there was no fresh Actions run visible for the new commits through the available commit-run query, so the branch is **not declared CI-green**.

The previous known validation run remains:

- Run `34383579174`: overall failure due to Windows 3.14 plugin Phase 6 timeout;
- Python suite on that run passed before the plugin timeout;
- PS5.1 acceptance smoke passed.

That prior failure must not be reused as proof that the new lifecycle tests fail; it predates the current commits.

## Current lifecycle invariant

The recovery transition is now modeled as:

```text
exact terminal claim
 -> prepare
 -> stop (restoration armed before call)
 -> exact quiesced classification
 -> start
 -> Gateway health verification
```

Failure semantics:

```text
prepare failure
    -> fail immediately; no stop was attempted

stop failure / partial stop
    -> surface original failure; attempt start restoration

classification failure after successful stop
    -> surface failure; attempt start restoration

start failure
    -> surface failure; existing finally path attempts one restore start

start succeeds but Gateway unhealthy
    -> return explicit recovery-failed result; no duplicate start
```

If classification has already durably authorized recovery and a later lifecycle step fails, the system must not claim inference success or erase the durable recovery state.

## Next approved work

1. Inspect provider-mode capability gating in the plugin entry path and Direct model-call path.
2. Prove Cloud/unknown providers retain Ticket, workflow, context, recovery, and delivery capability.
3. Add RED tests where any provider-mode branch suppresses capability.
4. Make the smallest provider-neutral repair.
5. Re-run focused tests and GitHub Actions before any release preparation.

## Release gate

Do not mutate `VERSION`, release metadata, or create/tag v0.9.5 until:

- lifecycle failure matrix is proven by CI;
- terminal-error Supervisor integration is proven by CI;
- provider-mode capability gating is removed/proven neutral;
- full validation is green on the required matrix;
- the known Windows 3.14 plugin timeout is separately resolved or formally accepted with new evidence.
