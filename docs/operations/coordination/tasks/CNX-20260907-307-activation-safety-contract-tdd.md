# CNX-20260907-307 — Activation safety contract TDD repair

Status: `READY_FOR_HERMES`
Parent: `CNX-20260907-306`
Executor: `Hermes`

## Authority

Under the operator's full-authority release objective and Task306 `REWORK_SOURCE_CONTRACT`, Hermes may perform repository/source/test/CI repair only. This deterministic successor is not a claim of independent acceptance and authorizes no live mutation.

## Required strict TDD slices

1. **Outermost production Supervisor quiescence.** Add a test through the composed production entry (`host_provider_v092`/`host_stall_v091`, not bare `host.py`) proving an active lease returns `result=quiesced` before state/provider adapter/event/recovery/probe/start/claim/restart work. Observe genuine RED, then add the smallest owning-entry guard. Preserve passthrough and normal managed behavior.
2. **Enable lease unconditional cleanup.** Test the real authority enable boundary with a reconciler/classifier exception immediately after acquisition. RED must prove the lease remains; minimal repair must release only its own owner/token in unconditional cleanup while preserving the original exception and transactional rollback semantics.
3. **Interrupted-Direct session authority.** Build a production-shaped temporary SQLite fixture with: (a) stale/ambiguous active session, null lifecycle identity, or generation ambiguity; (b) a genuinely active current lifecycle; and (c) sibling/protected-like rows. RED must prove the global promotion currently mutates stale/ambiguous owner work. Repair eligibility generically from lifecycle authority/freshness—never hardcode Ticket/session IDs—and preserve legitimate current-lifecycle recovery. No replay, send, payload inspection, or live mutation.
4. **Pending delivery activation fence.** Prove with a focused source/runtime test that enable cannot launch global assistant delivery for a pre-existing pending row without exact activation-time eligibility. Choose the smallest fail-closed generic contract: activation itself must not convert old unresolved delivery into `chat.inject`. Preserve normal delivery for a fresh explicitly owned runtime path. Do not hardcode the target.
5. Commit genuine RED separately when practical, then minimal fixes. Run focused tests, relevant Host/recovery/delivery suites, full Python suite, plugin test/build/package/schema validation, `git diff --check`, and exact-SHA Actions. Preserve first failures and corrective runs.
6. Publish the matching report only after required CI is terminal. If CI is pending, retain task ownership and recheck; do not create heartbeat commits.

## Acceptance

- composed production Supervisor has zero pre-guard writer/probe/recovery work under an active lease;
- every post-acquire enable exit releases its own lease and original error remains observable;
- stale/ambiguous/owner-intent-unproven Direct Tickets are unchanged; an exact fresh lifecycle positive remains recoverable;
- activation cannot automatically inject a pre-existing pending delivery;
- existing ownership, delivery, lifecycle, provider, installer and package regressions remain GREEN;
- exact candidate SHA and all required workflows are terminal success.

## Hard fences

No install/enable/lifecycle/scheduler/Gateway/provider mutation. No semantic send, session Delete/cancel, replay/redelivery/disposition. No manual SQLite/Ticket/session/transcript/config mutation outside disposable test fixtures. Never touch protected Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` or owner `agent:main:discord:channel:1531199905673252946`. No release/tag/default-branch mutation and no force push.

Report: `docs/operations/coordination/reports/CNX-20260907-307-activation-safety-contract-tdd.md`
