# CNX-20260905-260 — Task259 Candidate Deployment Transition Safety Requalification

Status: `READY_FOR_LUNA`
Assigned executor: `Luna`
Handoff from: `Musethree`
Next actor after report: `Musethree`
Parent task: `CNX-20260905-259`
Parent umbrella: `CNX-20260831-188`

## Accepted authority

Task259 independent review accepted the repaired candidate:

`d1531404d3eb8e7349a2058484c2fbc7ec9f1bf6`

with exact-SHA GitHub Actions **9/9 success** and accepted source contracts for:

- 15-minute owner-session freshness in direct-recovery due/wake selection;
- exact-ticket, owner-bound, idempotent, auditable `disposeDirectRecoveryTicket()`.

The old executable candidate `6822af464fe7a5cb3f93305d0263dfc86b56ac68` remains retired/parked.

## Objective

Prove whether `d1531404...` can be deployed to the current Windows installation through the supported install-over path **without any transition window that can start the old emittable direct-recovery implementation or emit the stale Discord recovery response**.

This is an evidence/requalification task. It does **not** authorize the installer, Gateway restart, recovery disposition, redelivery, or semantic send.

## Required work

1. Fetch fresh remote authority and require this Task260 to remain assigned to Luna.
2. Reconfirm Task259 review and exact candidate/CI lineage.
3. Recompute canonical candidate identity needed for deployment gating, including `scripts/install.ps1`, the Windows runner/launcher used by the supported path, and relevant candidate plugin/package fingerprint(s). Do not reuse a working-tree CRLF digest as canonical Git identity.
4. Trace the supported install-over lifecycle from source/scripts with exact file/function/line evidence:
   - preflight;
   - old Gateway/service/task stop behavior;
   - file/package replacement point;
   - any intermediate start/restart paths;
   - final Gateway start;
   - rollback/failure branches;
   - whether any branch can start the predecessor runtime after stop but before candidate code is active.
5. Establish the exact transition-safety proposition needed for live authorization: the first post-stop Gateway execution must load the repaired candidate direct-recovery code, not the predecessor emittable code.
6. Perform fresh **read-only** Windows/runtime/SQLite inspection as needed. Reconfirm the subject Ticket/recovery posture, current installed fingerprint, session timestamp/generation, model-call fence, outbox/delivery posture, health/storage/integrity, and whether any relevant state changed since Task259. Open SQLite read-only only.
7. Determine whether the candidate's 15-minute freshness contract would make the subject stale row non-due/non-waking immediately after candidate startup, using source predicates plus current read-only timestamps. Do not start candidate code to prove this in Task260.
8. Determine exact one-shot live successor preconditions/cardinality if transition safety is proven. Include abort conditions for any identity, runtime, recovery, or installer-order drift.
9. Preserve exact commands/evidence and publish the required report.

## Acceptance criteria

PASS only if all are proven:

- exact candidate identity and CI remain valid;
- installer lifecycle/order has no path that can restart old emittable runtime during the planned transition;
- current read-only live state has not introduced a new blocker;
- candidate freshness predicate makes the known stale row non-due/non-waking at candidate startup based on current timestamps/generation;
- no recovery disposition or semantic send is needed merely to make deployment transition safe;
- a future one-shot live install-over task can be specified with deterministic preflight/action/postflight gates and bounded cardinality.

If installer ordering can expose the predecessor runtime, or transition safety cannot be proven, use `BLOCKED_DEPLOYMENT_TRANSITION_RISK` and identify the smallest repository/source/test repair needed. Do not perform live mutation.

## Hard fences

```text
installer Scheduled Task registration/start = 0
scripts/install.ps1 live starts = 0
Gateway/controller/provider lifecycle mutation = 0
live DB/recovery mutation = 0
recovery claim/dispose/replay/redeliver/resend = 0
Dashboard/Discord/API semantic sends = 0
release/tag mutation = 0
force push/history rewrite = 0
```

Repository/read-only source inspection, tests, hash/provenance computation, GitHub Actions inspection, and read-only Windows/SQLite observations are allowed.

## Required report

Publish:

`docs/operations/coordination/reports/CNX-20260905-260-task259-candidate-deployment-transition-safety-requalification.md`

Final disposition must be one of:

- `PASS_DEPLOYMENT_TRANSITION_SAFE__LIVE_INSTALL_OVER_SUCCESSOR_ELIGIBLE`
- `BLOCKED_DEPLOYMENT_TRANSITION_RISK`
- `BLOCKED_<exact-cause>`

Then follow `HERMES_DUAL_AGENT_BATON_PROTOCOL.md`: hand the baton to **Musethree** and invoke/call Musethree when available. Luna must not self-review Task260.
