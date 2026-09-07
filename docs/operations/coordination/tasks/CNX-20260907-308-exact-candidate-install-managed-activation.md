# CNX-20260907-308 — Exact candidate install and managed activation requalification

Status: `READY_FOR_HERMES`
Parent: `CNX-20260907-307`
Executor: `Hermes`
Source candidate: `853650ce7f59687fbce172bd96543a38f288e47a`

## Authority

Under the operator's full-authority release objective and Task307 exact-SHA success, Hermes may perform one bounded supported installation of the exact source candidate, one bounded canonical managed activation, and read-only post-activation requalification. Hermes may choose evidence capture and supported implementation details without micro-confirmation, but may not broaden semantic or durable-state authority.

## Required procedure

1. Fresh-fetch GitHub authority and require `ACTIVE.md`, `STATUS.md`, and this immutable task to agree. Require candidate `853650ce7f59687fbce172bd96543a38f288e47a` to exist and retain successful runs Validate `34137033103`, PS5.1 `34137033075`, and Windows pack `34137033014`.
2. Materialize and preserve a disposable detached checkout at the exact candidate. Require detached HEAD, clean tree, version `0.9.3`, successful declared plugin build/validation, and source fingerprint `9af4712dd3265afc577a233b4716279901b9eab1128ad6640c63e0ba846f0f33` before any live operation.
3. Capture a fresh read-only baseline: installed skill/plugin fingerprints, plugin inventory, Host mode/generation, quiescence lease, Gateway/Ollama/Supervisor/process identity, SQLite integrity, exact target/protected Ticket/session/recovery/delivery/outbox rows, and candidate promotion/delivery predicates. Prove no competing installer/enable writer.
4. Stop `BLOCKED_PREFLIGHT` if the repaired generic predicates would select the protected Ticket/session or arm delivery for a stale/ambiguous lifecycle. Do not repair durable state manually.
5. If installed plugin/skills are not exact, invoke the repository's supported `scripts/install.ps1` from the detached candidate at most once through a file-based PowerShell shim, with exact workspace `C:\Users\CDQ-P\.openclaw\workspace`, `-SkipGatewayRestart`, and `-SkipAgentsPolicy`. Do not use `-SkipPlugin`. Record inner installer exit, transcript, backup/transaction provenance, and post-install byte identity. No retry after process start.
6. Only after installed/source identity and health are exact, invoke canonical `C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd enable` at most once through a file-based PowerShell shim. Record invocation count, exact exit, lease acquire/release evidence, transaction generation/config, plugin state, and worker identity. No alternate activation command or retry.
7. Perform read-only postflight. Require Host managed state, plugin enabled/exact, lease absent, healthy Gateway/Ollama/Supervisor, SQLite integrity `ok`, no competing writer, and exact installed module hashes/fingerprint bound to candidate.
8. Compare the complete protected baseline before/after. Protected Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` and owner session `agent:main:discord:channel:1531199905673252946` must be byte/row-semantically unchanged; no recovery/delivery/outbox/model-call/event lineage may be added for it by this task.
9. Requalify the existing target and pending delivery read-only. Activation must not inject, replay, settle, disposition, or increment attempts for a stale/ambiguous owner. If autonomous state changes occur, capture exact evidence and stop without retry or compensation.
10. Publish `docs/operations/coordination/reports/CNX-20260907-308-exact-candidate-install-managed-activation.md` with exact invocation ledger, hashes, runtime/durable deltas, health, and disposition. Create only the smallest necessary successor after evidence is terminal.

## Acceptance

- exact candidate source/build/CI provenance is retained;
- supported installer invocation count is `0` if already exact, otherwise exactly `1`, with terminal evidence;
- canonical enable invocation count is exactly `1` only after all preconditions pass;
- installed plugin and owning Host modules match candidate payload/fingerprint;
- quiescence is acquired/released and no pre-guard supervisor work occurs;
- managed runtime, worker identity, health, and SQLite integrity are GREEN;
- protected Ticket/session and stale pending delivery remain unchanged and unemitted;
- no unauthorized semantic or manual durable-state action occurs.

## Stop conditions

Stop only the affected operation on candidate drift, failed exact-SHA provenance, ambiguous installed identity, competing writer, unsafe promotion/delivery predicate, protected-state drift, installer/enable nonzero exit, missing one-shot evidence, health/integrity failure, or autonomous semantic/durable anomaly. Preserve state and create the smallest evidence-bound successor; never retry a consumed installer/enable operation blindly.

## Hard fences

No semantic send, session Delete/cancel, replay/redelivery/disposition, manual SQLite/Ticket/session/transcript/config mutation, payload inspection for eligibility, protected-state mutation, second installer invocation, second enable invocation, ad-hoc file copy, unsupported command, Gateway restart outside the supported owned path, release/tag/default-branch mutation, force push, or use of `cnxclaw session cancel` as Delete substitute.
