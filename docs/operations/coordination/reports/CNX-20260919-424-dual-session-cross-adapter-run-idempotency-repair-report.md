# CNX-20260919-424 — Dual-Session Cross-Adapter Run Idempotency Repair Report

## Result

Final classification:

`READY_FOR_CONTROLLED_OPENCLAW_2026_9_4_UPGRADE_REVIEW`

CNX-424 repaired the residual cross-adapter idempotency defect found during independent CNX-423 review.

The repaired invariant is:

`ONE HOST RUN -> ONE TICKET -> ONE ROUTE EVENT`

including the bound ACP case where:

- `reply_dispatch` uses the source owner session;
- a later `before_agent_run` observes the effective ACP target session;
- both adapters carry the same real OpenClaw runId.

No live OpenClaw upgrade or semantic provider request occurred.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Task: `CNX-20260919-424`
- Parent: `CNX-20260919-423`
- Starting authoritative HEAD: `de951acb479763741eb913f56a02069952b69b4d`
- RED commit: `01bad9e5f00e0fafae9aa52edfd8dceddf5d04f6`
- Qualified implementation HEAD: `f56a62e41533710ec72a7bbab20d305109437289`
- Final publication HEAD: verified after publication and reported in executor closeout.

## Root cause

TicketStore persistent idempotency is keyed by:

`hash(ownerSessionKey + "\0" + runId)`

CNX-423 correctly separated:

- source owner session;
- effective ACP dispatch session.

For a bound ACP host run, `reply_dispatch` therefore persisted the Ticket under the source owner session.

If the same host run later emitted `before_agent_run`, that adapter could observe the effective ACP target session. Because the persistence request key includes owner session, the same runId under a different session produced a second Ticket.

The plugin already maintained an in-process:

`ticketedRuns: Set<runId>`

and `reply_dispatch` populated it immediately after successful admission, but `before_agent_run` did not consult that run-level fence before invoking the shared Ticket admission kernel.

## TDD RED

New regression:

`plugins/cogentnexus-openclaw/src/cnx424-dual-session-idempotency.test.ts`

Pre-repair result:

- test files: `1 failed`
- tests: `1 failed / 2 passed`
- total: `3`

Exact failing sequence:

1. bound ACP `reply_dispatch`
   - source owner: `agent:main:discord:C123`
   - effective target: `agent:opencode:acp:bound-session`
   - runId: `dual-session-run`

2. `before_agent_run`
   - session: effective target
   - same runId
   - same prompt

Expected one Ticket owned by the source session.

Observed two Tickets:

- source-owner Ticket;
- effective-target Ticket;
- both with runId `dual-session-run`.

The two controls already passed:

- same-session reply_dispatch + before_agent_run remained one Ticket;
- before_agent_run alone still admitted a Ticket when no earlier reply_dispatch admission existed.

RED was committed before production repair:

`01bad9e5f00e0fafae9aa52edfd8dceddf5d04f6`

## Minimal repair

Production change is four lines in:

`plugins/cogentnexus-openclaw/src/index.ts`

Immediately before `before_agent_run` invokes the shared Ticket admission kernel:

- if the exact real `currentRunId` is already present in `ticketedRuns`;
- the hook records a pass trace;
- it returns `outcome:"pass"`;
- no second Ticket persistence occurs.

This preserves earlier handling of:

- delivery markers;
- post-compaction recovery;
- eligibility checks.

It does not disable `before_agent_run` fallback. If no earlier adapter admitted the run, `before_agent_run` continues through the existing shared admission kernel.

No Ticket DB schema or request-key semantics were changed.

## GREEN

### CNX-424 / CNX-423 / CNX-422

After repair:

- test files: `3 passed`
- tests: `27/27 PASS`

CNX-424:

- `3/3 PASS`

The repaired bound ACP case now proves:

- exactly one Ticket;
- owner session remains source owner;
- exactly one routed event.

Controls prove:

- same-session adapter idempotency remains one Ticket;
- before_agent_run-only admission still works.

### Focused baseline regression

Included:

- CNX-424;
- CNX-423;
- CNX-422;
- core index;
- Dashboard verified delivery;
- direct model-call lease;
- direct recovery;
- session ownership;
- Discord direct delivery;
- Discord receipt lifecycle;
- Ticket contention.

Result:

- test files: `11 passed`
- tests: `102/102 PASS`

### Package validation

`npm run plugin:validate`:

- TypeScript build: PASS
- canonicalized dist files: `50`
- mixed-plugin artifact verification: PASS
- Ticket DB bootstrap: PASS
- required tables: `9`
- v095 registration fence: PASS
- package contents verification: PASS
- packed file count: `264`

## Broad regression

Final full plugin suite:

- test files: `82 passed / 1 failed` (`83` total)
- tests: `370 passed / 1 failed` (`371` total)

The only failure remains the historical predecessor:

`src/cnx383-hook-policy-projection.test.ts`

with the unchanged assertion:

`expected undefined to be true`

No CNX-424 regression was introduced.

## OpenClaw v2026.9.4 target qualification

Candidate source was copied into the exact isolated OpenClaw 2026.9.4 qualification package.

Confirmed target:

`TARGET_OPENCLAW=2026.9.4`

Result:

- TypeScript build: PASS
- target test files: `9 passed`
- target tests: `100/100 PASS`

Target tests included:

- CNX-424;
- CNX-423;
- CNX-422;
- core index;
- Dashboard delivery;
- direct model-call lease;
- direct recovery;
- session ownership;
- runtime-hook attestation.

## Isolated v2026.9.4 runtime

Fresh isolated Gateway:

`127.0.0.1:19794`

Live Gateway remained:

`127.0.0.1:18789`

Observed:

- candidate CNX loaded from isolated `dist/v091-release-entry.js`;
- reply_dispatch registration observed;
- plugin errors: `0`;
- Gateway reached `ready`;
- health: `ok=true`;
- runtime attestation:
  - `runnerReady=true`
  - `globalHookCount=7`
  - plugin registry-specific count unavailable through public target SDK
  - classification `AMBIGUOUS`;
- semantic provider sends: `0`.

Windows-native `CTRL_C_EVENT` shutdown:

- SIGINT received;
- admission closed;
- active-work drain settled;
- shutdown completed cleanly in `17ms`;
- process exit code: `0`.

After shutdown:

- isolated port `19794`: closed;
- live port `18789`: remained listening.

## Migration/rollback evidence

CNX-424 changes only in-process pre-admission run-id deduplication inside `before_agent_run`.

It does not change:

- Ticket DB schema;
- OpenClaw migration behavior;
- session persistence;
- startup recovery schema;
- installer/bootstrap;
- rollback restore procedure.

Therefore accepted CNX-422 migration/rollback evidence remains applicable:

- shared DB `v1 -> v17`;
- agent DB `v1 -> v19`;
- sessions `19 -> 19`;
- binary-only downgrade to 2026.7.1-2 is unsafe after migration;
- complete pre-upgrade state/config/session/workspace/CNX snapshot is required for rollback.

## Changed files

RED commit:

`01bad9e5f00e0fafae9aa52edfd8dceddf5d04f6`

- `plugins/cogentnexus-openclaw/src/cnx424-dual-session-idempotency.test.ts`

Production fix commit / qualified implementation HEAD:

`f56a62e41533710ec72a7bbab20d305109437289`

- `plugins/cogentnexus-openclaw/src/index.ts`

Production repair size:

- `4 insertions`
- `0 deletions`

## Hard-fence accounting

- Semantic sends: `0`
- External provider probes: `0`
- Browser mutation: `0`
- Live OpenClaw upgrade: `0`
- Live session/state migration: `0`
- Live provider/model mutation: `0`
- Live plugin lifecycle mutation for upgrade: `0`
- Manual live Ticket/outbox/recovery/SQLite mutation: `0`
- Release/tag/main: `0`
- Force push/history rewrite: `0`

## Final decision

`READY_FOR_CONTROLLED_OPENCLAW_2026_9_4_UPGRADE_REVIEW`

The residual dual-session adapter idempotency defect is repaired and the candidate is requalified against exact OpenClaw v2026.9.4 in isolated state.

Stop for independent review before live upgrade.
