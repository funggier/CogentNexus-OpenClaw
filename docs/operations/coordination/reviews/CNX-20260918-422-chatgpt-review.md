# CNX-20260918-422 — ChatGPT Review

## Decision

`REJECT_READY__ADMISSION_SEMANTICS_REPAIR_REQUIRED`

Rejected executor classification:

`READY_FOR_CONTROLLED_OPENCLAW_2026_9_4_UPGRADE`

CNX-422 contains substantial valid work: the shared admission kernel, the early `reply_dispatch` seam, target-version build compatibility, isolated v2026.9.4 startup/shutdown, copied-state migration characterization, and full-snapshot rollback proof are accepted as useful evidence.

However, independent source review found two material admission-semantics defects. Either defect is sufficient to reject controlled live-upgrade readiness because the task explicitly required control/recovery exclusion and correct harness-agnostic identity handling.

No live upgrade is authorized from implementation HEAD:

`5ae72d9ecc3f91da496b72d7b909f50bde07149a`

Reviewed publication HEAD:

`8ffac9cb6fbbd24a005fe0534f83141a607179c2`

## Accepted evidence

The following CNX-422 findings are accepted unless superseded by the narrow repair:

- `reply_dispatch` is a valid pre-model host seam and exposes the real dispatch event plus `FinalizedMsgContext`;
- OpenClaw v2026.9.4 target build compatibility was proven;
- explicit `InboundAccessAuthorized=false` correctly overrides Gateway scope fallback in the current helper;
- provider/model/harness fields are not rewritten by the CNX repair;
- focused CNX-422 tests and package validation passed as reported;
- the single full-suite CNX-383 RED is historical/pre-existing rather than a new CNX-422 regression;
- fresh isolated v2026.9.4 startup/plugin load and clean SIGINT shutdown are accepted;
- copied-state migration `shared v1 -> v17`, `agent v1 -> v19`, and session-count preservation are accepted;
- binary-only downgrade to 2026.7.1-2 is unsafe after migration;
- full pre-upgrade snapshot restoration is the required rollback model;
- semantic provider sends remained zero and no live OpenClaw upgrade was performed.

The copied-state workspace-path incident was disclosed and the later isolated-v2 evidence is sufficient to keep the migration findings usable. It is not the reason for this rejection.

## Blocking finding 1 — internal/control provenance is not excluded before trust fallback

Task 422 Stage 2 required the shared admission policy to exclude:

- subagent/synthetic paths;
- control paths;
- delivery paths;
- continuation/recovery paths.

The implemented `reply_dispatch` adapter does not classify OpenClaw provenance before invoking the shared kernel.

Current trust helper:

`replyDispatchTrusted(event)`

accepts either:

- `InboundAccessAuthorized === true`; or
- Gateway scope `operator.write` / `operator.admin` when the explicit field is absent.

The shared kernel then excludes only:

- prompt patterns recognized by `ticketIntakeEligible(prompt)`; and
- session keys containing `:subagent:`.

That is insufficient for OpenClaw v2026.9.4, whose `FinalizedMsgContext` exposes explicit control provenance:

- `InputProvenance.kind = external_user | inter_session | internal_system`;
- `InternalTurnSource`;
- provenance `sourceTool`.

### Exact upstream control-path counterexample

OpenClaw v2026.9.4:

`src/gateway/server-restart-sentinel.ts`

constructs restart/recovery turns with:

- owner/canonical `SessionKey`;
- `InputProvenance.kind = "internal_system"`;
- `InputProvenance.sourceTool = "restart-sentinel"`;
- `GatewayClientScopes = ["operator.admin"]`;
- ordinary model-facing text.

It then dispatches through the normal assembled channel-turn path.

OpenClaw's reply-dispatch gate only suppresses inbound handlers for heartbeat-owned operations:

`src/auto-reply/reply/dispatch-from-config.gather.ts`

`allowInboundHandlers: replyOperationRunState.heartbeat === undefined`

The restart-sentinel continuation is not a heartbeat operation, so it can reach `reply_dispatch`.

CNX-422 therefore does not reliably exclude this internal recovery/control turn before its trust decision. Depending on run-id availability, the current adapter can either:

- admit a new Ticket for internal recovery; or
- fail closed with `handled=true` because a required owner-style field is missing.

Both outcomes are incorrect. The control/recovery turn should be classified as non-owner-intent and skipped, not re-admitted or taken over.

### Reviewer RED reproduction

A disposable reviewer-only regression was executed against the published implementation using the exact relevant context shape:

- owner session key;
- ordinary prompt;
- `InputProvenance.kind="internal_system"`;
- `sourceTool="restart-sentinel"`;
- `GatewayClientScopes=["operator.admin"]`.

Expected:

`tickets = 0`

Observed:

`tickets = 1`

Vitest result:

- `1 failed / 1 total`
- assertion: `expected 1 to be 0`

The temporary reviewer test was removed afterward; the Git worktree returned clean. This evidence is not a repository mutation.

## Blocking finding 2 — valid ACP retargeting is misclassified as contradictory session identity

CNX-422 currently defines identity conflict as:

`event.sessionKey !== event.ctx.SessionKey`

when both are present.

That is not universally a contradiction in OpenClaw v2026.9.4.

### Exact upstream ACP contract

OpenClaw v2026.9.4:

`src/auto-reply/reply/dispatch-from-config.gather.ts`

computes:

- `sourceSessionKey = ctx.SessionKey`;
- `boundAcpDispatchSessionKey = resolveBoundAcpDispatchSessionKey(...)`;
- `acpDispatchSessionKey = boundAcpDispatchSessionKey ?? ...`.

Then:

`src/auto-reply/reply/dispatch-from-config.reply-dispatch-hook.ts`

constructs the hook event with:

`sessionKey: state.acpDispatchSessionKey`

while passing:

`ctx: state.ctx`

unchanged.

Therefore a legitimate bound ACP/Codex dispatch can intentionally have:

- `event.sessionKey = effective bound ACP session`;
- `event.ctx.SessionKey = source owner conversation session`.

OpenClaw itself has a regression explicitly named:

`retargets reply_dispatch to a bound generic ACP session before model fallback`

in:

`src/auto-reply/reply/dispatch-from-config.abort-and-dedupe.test-utils.ts`.

The current CNX-422 adapter marks this legitimate source/effective-session distinction as `identityConflict=true` and fails closed.

That can block the exact Codex/ACP path CNX-422 was intended to repair.

## Architectural correction required

The early adapter must distinguish at least two identities instead of collapsing them:

1. **source owner session**
   - the external-owner conversation/session from `FinalizedMsgContext`;
   - used for Ticket ownership / user-intent correlation;

2. **effective dispatch session**
   - `reply_dispatch.event.sessionKey`;
   - may be a bound ACP/harness target and may legitimately differ from the source owner session.

A mismatch is only contradictory when the host contract says the two fields claim the same semantic role. Bound ACP retargeting is not such a contradiction.

Similarly, trust must be decided only after provenance classification. Privileged Gateway scopes on an internal/control/recovery turn are authority for that internal host action, not proof that the turn is new external owner intent.

## Required repair scope

Authorize a narrow successor source-only task.

Required RED cases before production change:

1. restart-sentinel `internal_system` turn with privileged scopes creates no Ticket and is not claimed as owner admission;
2. generic `InputProvenance.kind="internal_system"` control turn is excluded;
3. `InputProvenance.kind="inter_session"` subagent completion into an owner session is excluded from ordinary owner admission;
4. valid bound ACP retargeting with different source/effective session keys is not treated as identity conflict;
5. Ticket ownership remains bound to the source external-owner session, not the ACP target session;
6. genuinely contradictory same-role identity still fails closed;
7. external Dashboard/Codex and Dashboard/embedded paths remain Ticket-first;
8. same external turn across `reply_dispatch` and `before_agent_run` remains one Ticket / one route event;
9. provider/model/harness fields remain untouched;
10. missing/untrusted external-owner ingress remains fail closed.

Preferred repair shape:

`reply_dispatch host adapter -> provenance/control-path classifier -> normalized source-owner + effective-dispatch identities -> existing shared Ticket admission kernel`

Do not encode OpenClaw provider/model/harness routing inside CogentNexus.

## Review impact on upgrade qualification

The migration and rollback evidence does not need to be discarded.

However, controlled upgrade readiness must remain blocked until the repaired candidate proves:

- the new RED matrix GREEN;
- focused existing regressions GREEN;
- build/typecheck/package validation GREEN;
- OpenClaw v2026.9.4 target build GREEN;
- isolated v2026.9.4 plugin startup/register/shutdown GREEN with the repaired candidate.

A full copied-state migration rerun is optional unless the repair changes startup/migration/storage behavior. If no such behavior changes, CNX-422 migration/rollback evidence may be reused with explicit provenance.

## Safety decision

Until the successor repair is reviewed:

- live OpenClaw upgrade: prohibited;
- live session/state migration: prohibited;
- semantic provider send for this repair: prohibited;
- live provider/model mutation: prohibited;
- live plugin install-over/uninstall for upgrade: prohibited;
- release/tag/main: prohibited;
- force push/history rewrite: prohibited.

## Reviewer

ChatGPT

Human final authority: Operator
