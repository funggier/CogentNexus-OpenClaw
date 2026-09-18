# CNX-20260919-424 — ChatGPT Review

## Decision

`ACCEPTED_PASS__CONTROLLED_OPENCLAW_2026_9_4_UPGRADE_AUTHORIZED`

Accepted executor classification:

`READY_FOR_CONTROLLED_OPENCLAW_2026_9_4_UPGRADE_REVIEW`

CNX-424 is accepted.

The residual dual-session cross-adapter idempotency defect is repaired with a narrow in-process real-run fence while preserving persistent TicketStore semantics and before_agent_run fallback.

Reviewed implementation HEAD:

`f56a62e41533710ec72a7bbab20d305109437289`

Reviewed publication HEAD:

`8577cbf24c62c2c14d2803e191ab8e868909eb13`

## Source review

The repair adds a four-line guard in the Ticket-first before_agent_run path:

- delivery-marker handling remains earlier;
- post-compaction handling remains earlier;
- owner eligibility remains earlier;
- only immediately before shared Ticket admission does it check whether currentRunId is already present in ticketedRuns.

reply_dispatch adds the real admitted runId to ticketedRuns after successful Ticket acceptance.

Therefore, when the same OpenClaw run later reaches before_agent_run under an effective ACP target session, the second adapter passes without generating a second persistent request key.

The fallback remains intact: if no earlier reply_dispatch admission exists, ticketedRuns does not contain the runId and before_agent_run continues through the shared kernel.

## Host run-id review

OpenClaw v2026.9.4 reply_dispatch receives:

`params.replyOptions?.runId`

The execution lifecycle preserves/observes the real agent run ID through onAgentRunStart and generates a UUID when a run ID is not supplied.

Using exact runId as the in-process cross-adapter fence is therefore aligned with the host's run identity rather than provider/model/session routing.

## TDD review

Accepted RED provenance:

- RED commit: `01bad9e5f00e0fafae9aa52edfd8dceddf5d04f6`
- pre-fix result: `1 failed / 2 passed`
- observed duplicate: same runId created one source-owner Ticket plus one effective-ACP-target Ticket.

Accepted GREEN:

- CNX-424: `3/3 PASS`
- CNX-424/423/422: `27/27 PASS`
- focused baseline: `102/102 PASS`
- target v2026.9.4: `100/100 PASS`
- package validation: PASS
- broad suite: `370 PASS / 1 known historical CNX-383 RED`
- isolated v2026.9.4 startup/health/plugin load: PASS
- clean SIGINT shutdown: PASS

## Preserved findings

CNX-423 provenance and ACP source/effective identity repairs remain accepted.

CNX-422 migration/rollback evidence remains accepted:

- shared state migration `v1 -> v17`;
- agent state migration `v1 -> v19`;
- sessions `19 -> 19`;
- binary-only downgrade is not safe after migration;
- full pre-upgrade state/config/session/workspace snapshot is mandatory.

## Upgrade authorization

Authorize a new controlled live-upgrade task to move the live OpenClaw host from:

`2026.7.1-2`

to exact target:

`2026.9.4`

The upgrade must be fail-closed and rollback-first.

Before any migration/install mutation, it must:

1. verify current live health/version/session count;
2. quiesce the live Gateway cleanly;
3. capture and verify a complete rollback snapshot;
4. preserve the old OpenClaw executable/package identity;
5. preserve live config, workspace migration files, shared state, agent state, sessions/transcripts and CNX DB;
6. record hashes/versions/provenance.

Only after the snapshot is verified may the host package/state migration begin.

If the target installation or migration fails, restore the old package and complete snapshot rather than attempting binary-only downgrade over migrated state.

Post-upgrade acceptance must include:

- exact version 2026.9.4;
- config validation/doctor result;
- Gateway health;
- CNX plugin load and reply_dispatch registration;
- session count/preservation;
- CNX runtime state integrity;
- no unexpected recovery consumption;
- one controlled semantic Ticket-first acceptance only after non-semantic health gates pass.

## Safety

No release/tag/main mutation is authorized by this review.

Rollback evidence and the pre-upgrade snapshot must be retained through final review.

## Reviewer

ChatGPT

Human final authority: Operator
