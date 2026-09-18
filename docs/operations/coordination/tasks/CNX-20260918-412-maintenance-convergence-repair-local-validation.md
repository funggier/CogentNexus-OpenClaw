# CNX-20260918-412 — Maintenance Convergence Repair Local Validation

Status: `READY_FOR_HERMES`

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Parent: `CNX-20260918-411`
- Executor: `Hermes`
- Reviewer: `ChatGPT`
- Human final authority: `Operator`
- Parent report: `docs/operations/coordination/reports/CNX-20260918-411-healthy-runtime-maintenance-marker-convergence-repair-report.md`

GitHub remote is authoritative.

## Objective

Validate the CNX-411 healthy-runtime maintenance-marker convergence repair on a clean local checkout.

This task is source/test validation only.

Do not deploy or mutate the production runtime.

## Candidate lineage

RED regression:

`c30b3788dafba55ebef456c119c66815359c3e05`

Minimal repair:

`368073d67e75cc89b9b04b21b0ee002e76f7e82f`

Expected source surfaces:

- `skills/cogentnexus-openclaw/scripts/host_v091.py`
- `tests/test_v091_idle_recovery_hint.py`

## Required focused validation

At minimum run:

```text
python -m unittest tests.test_v091_idle_recovery_hint -v
python -m unittest tests.test_v095_idle_quiescence tests.test_v095_provider_neutral_supervisor tests.test_host_v091_actionability tests.test_wake_authority_v095 -v
```

Then run the repository's broader relevant Python test suite. If practical and already supported by the repository, run:

```text
python -m unittest discover -s tests -p "test_*.py" -v
```

If the full suite is excessively broad because of known platform-only integration tests, use the repository's established bounded validation set and document exactly what was excluded and why.

## Required assertions

Prove:

1. healthy Gateway + no actionable work + no marker remains lightweight idle;
2. healthy Gateway + `healthy-runtime` marker + `execute_safe=false`:
   - marker is not mutated;
   - no lifecycle call;
   - no legacy heavy Supervisor;
   - result reports recovery pending;
3. healthy Gateway + `healthy-runtime` marker + `execute_safe=true`:
   - exactly one provider-neutral `lifecycle start`;
   - no `--provider`;
   - no legacy provider-heavy Supervisor;
   - marker retirement is required before convergence is claimed;
   - after retirement and no durable work, result returns idle with reconciliation evidence;
4. provider-neutral supervisor tests remain GREEN;
5. wake-authority/single-wake tests remain GREEN.

## Repair authority

If validation exposes a defect caused by CNX-411, minimal source/test repair is authorized using:

`RED -> minimal fix -> GREEN`

Do not expand into unrelated architecture changes.

## Hard fences

- No production install/install-over.
- No Gateway restart/reload.
- No live lifecycle command against the operator runtime.
- No production maintenance-marker mutation.
- No provider/model/auth/routing changes.
- No semantic/model/provider request.
- No Ticket/outbox/recovery/SQLite production mutation.
- No OpenClaw dependency patch/version change.
- No release/tag/main.
- No force push/history rewrite.
- Do not create/start CNX-413 yourself.

## Exit classification

Use one:

- `MAINTENANCE_CONVERGENCE_LOCAL_VALIDATION_GREEN`
- `MAINTENANCE_CONVERGENCE_LOCAL_REPAIR_GREEN`
- `MAINTENANCE_CONVERGENCE_LOCAL_VALIDATION_FAILED`
- `BLOCKED_BY_LOCAL_TEST_ENVIRONMENT`

## Closeout

Publish:

`docs/operations/coordination/reports/CNX-20260918-412-maintenance-convergence-repair-local-validation-report.md`

Then set ACTIVE/STATUS to `WAITING_FOR_CHATGPT_REVIEW`, verify local HEAD equals remote HEAD, verify clean worktree, and stop.

Do not deploy.
