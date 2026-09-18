# CNX-20260919-423 — Reply-Dispatch Provenance and ACP Identity Semantics Repair Report

## Result

Final classification:

`READY_FOR_CONTROLLED_OPENCLAW_2026_9_4_UPGRADE_REVIEW`

CNX-423 repaired the two admission-semantics defects found by the independent CNX-422 review without changing provider/model/harness ownership.

The repaired candidate now:

- excludes explicit OpenClaw internal/inter-session/control turns before owner-intent trust evaluation;
- treats `FinalizedMsgContext.SessionKey` as the source owner session;
- treats `reply_dispatch.event.sessionKey` as the effective dispatch session;
- allows the documented OpenClaw v2026.9.4 ACP retarget relation where those two identities legitimately differ;
- preserves fail-closed behavior for same-role non-ACP identity contradictions;
- preserves the CNX-422 Ticket-first direct/durable/idempotency behavior;
- builds and tests against both the current baseline and OpenClaw v2026.9.4;
- starts, loads, attests, and shuts down cleanly in isolated v2026.9.4 state.

This task does **not** authorize or perform the live OpenClaw upgrade.

## Authority and exact HEADs

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Task: `CNX-20260919-423`
- Parent: `CNX-20260918-422`
- Starting local/remote HEAD: `ce74b25681a39c4d88ccf8725bd10f708f9cb61d`
- Qualified implementation HEAD: `59830e4512b89d8924295c886f121d077b3d6c61`
- Final report/coordination publication HEAD: verified after publication and reported in executor closeout because embedding the commit containing this report would be self-referential.
- GitHub remote was fetched immediately before implementation staging and still matched the starting authoritative HEAD.
- No force push, history rewrite, tag, release, or `main` mutation occurred.

## Parent review blockers

CNX-422 review rejected upgrade readiness for two reasons.

### Blocker 1 — provenance/control-path confusion

The previous adapter evaluated trust from:

- `InboundAccessAuthorized`; or
- privileged Gateway scopes.

It did not first classify:

- `InputProvenance.kind="internal_system"`;
- `InputProvenance.kind="inter_session"`;
- `InternalTurnSource`.

That allowed privileged host-internal work such as restart recovery to be mistaken for new external-owner intent.

### Blocker 2 — ACP source/effective identity confusion

The previous adapter treated any difference between:

- `event.ctx.SessionKey`; and
- `event.sessionKey`

as contradictory identity.

OpenClaw v2026.9.4 intentionally uses those fields for different semantic roles during ACP binding/retargeting:

- `ctx.SessionKey` remains the source owner conversation session;
- `event.sessionKey` becomes the effective bound ACP dispatch session.

The previous rule could therefore fail closed on a legitimate Codex/ACP dispatch.

## Exact OpenClaw v2026.9.4 contract used

The target remains exact OpenClaw:

- version: `2026.9.4`
- previously qualified upstream annotated tag: `v2026.9.4`
- peeled source commit: `3a9d69db306cd7f081e06254cb89c4bcc14a7107`

Relevant source facts were re-verified from the isolated upstream source used during CNX-422/CNX-423 qualification:

### Provenance

`FinalizedMsgContext` exposes:

- `InputProvenance`;
- `InternalTurnSource`;
- `InboundAccessAuthorized`;
- `GatewayClientScopes`;
- source `SessionKey`.

`InputProvenance.kind` distinguishes:

- `external_user`;
- `inter_session`;
- `internal_system`.

OpenClaw restart continuation constructs internal provenance with:

- `kind="internal_system"`;
- `sourceTool="restart-sentinel"`;
- privileged `GatewayClientScopes`.

Privileged scope is authority for the host-internal turn; it is not evidence that the turn is new external owner intent.

### ACP retargeting

OpenClaw computes a separate ACP dispatch session and passes it as:

`reply_dispatch.event.sessionKey`

while leaving source conversation identity in:

`reply_dispatch.event.ctx.SessionKey`.

The upstream test:

`retargets reply_dispatch to a bound generic ACP session before model fallback`

confirms this is an intentional contract, not corruption.

## TDD RED evidence

A new production-shaped suite was added before source repair:

`plugins/cogentnexus-openclaw/src/cnx423-provenance-acp-identity.test.ts`

Pre-repair result:

- test files: `1 failed`
- tests: `5 failed / 3 passed`
- total: `8`

The five RED cases were:

1. restart-sentinel internal recovery with `operator.admin` created a Ticket instead of being excluded;
2. generic `internal_system` provenance created a Ticket;
3. explicit `InternalTurnSource="cron"` created a Ticket;
4. `inter_session` subagent completion into an owner session created a Ticket;
5. valid bound ACP retargeting produced no Ticket because source/effective session mismatch was treated as conflict.

The three already-GREEN controls were:

- non-ACP same-role identity contradiction still failed closed;
- ordinary external ACP owner intent remained Ticket-first;
- explicit external owner ingress with `InboundAccessAuthorized=false` still failed closed despite privileged scope.

## Minimal production repair

Only two production files changed.

### `ticket-admission-kernel.ts`

Added:

`replyDispatchProvenanceExcluded(event)`

It excludes owner-intent admission when OpenClaw explicitly marks the turn as:

- `InputProvenance.kind="internal_system"`;
- `InputProvenance.kind="inter_session"`;
- `InternalTurnSource="heartbeat"`;
- `InternalTurnSource="cron"`;
- `InternalTurnSource="exec"`.

This classification happens before trust fallback.

The identity normalizer now returns separate concepts:

- `sourceSessionKey`;
- `effectiveDispatchSessionKey`.

Normalization rule:

- source owner = `event.ctx.SessionKey` when available;
- effective dispatch target = `event.sessionKey`;
- fallback source owner = effective dispatch session only when the finalized source session is unavailable.

Identity mismatch is fail-closed only when:

- both identities exist;
- they differ; and
- dispatch kind is not `acp`.

This preserves legitimate ACP retargeting while keeping same-role agent contradictions fail closed.

### `index.ts`

The Ticket-first `reply_dispatch` adapter now performs:

`provenance exclusion -> prompt normalization -> identity normalization -> trust evaluation -> shared Ticket admission`

No provider/model/harness router was introduced.

## GREEN evidence

### CNX-423 + CNX-422 combined

- test files: `2 passed`
- tests: `24/24 PASS`

CNX-423 specifically:

- `8/8 PASS`

This proves:

1. restart-sentinel internal recovery is excluded;
2. generic internal-system provenance is excluded;
3. explicit internal turn source is excluded;
4. inter-session subagent completion is excluded;
5. bound ACP retargeting is legitimate;
6. Ticket ownership remains the source external-owner session;
7. effective ACP target/provider/model/harness event fields remain unchanged;
8. same-role non-ACP contradiction still fails closed;
9. ordinary external ACP owner turn remains Ticket-first;
10. explicit untrusted external owner ingress still fails closed.

CNX-422 remains `16/16 PASS`, preserving:

- embedded/agent Ticket-first admission;
- ACP/Codex-style Ticket-first admission;
- direct unclaimed host execution;
- durable pre-inference takeover;
- reply_dispatch + before_agent_run idempotency;
- one route event;
- delivery/continuation/direct-recovery exclusions;
- subagent session exclusion;
- explicit trust denial precedence;
- exact run-id fail-closed behavior.

### Focused baseline regression

Command set included:

- CNX-423;
- CNX-422;
- `index.test.ts`;
- Dashboard verified delivery;
- direct model-call lease;
- direct recovery;
- session ownership;
- Discord direct delivery;
- Discord receipt lifecycle;
- Ticket contention.

Result:

- test files: `10 passed`
- tests: `99/99 PASS`

### Package validation

`npm run plugin:validate`:

- TypeScript build: PASS
- canonicalized dist text files: `50`
- mixed-plugin artifact verification: PASS
- config properties: `46`
- tools: `5`
- Ticket DB bootstrap: PASS
- required tables: `9`
- v095 registration fence: PASS
- package contents verification: PASS
- packed file count: `262`

## Broad regression characterization

Full plugin suite after the repair:

- test files: `81 passed / 1 failed` (`82` total)
- tests: `367 passed / 1 failed` (`368` total)

The only failure remains:

`src/cnx383-hook-policy-projection.test.ts`

with the same historical assertion:

`expected undefined to be true`

CNX-423 did not modify that test or the historical host-policy projection boundary. No new broad-suite failure was introduced.

## OpenClaw v2026.9.4 target build and tests

The exact CNX-423 candidate source was copied into the isolated OpenClaw 2026.9.4 qualification package.

Confirmed target dependency:

`TARGET_OPENCLAW=2026.9.4`

Result:

- TypeScript build: PASS
- target test files: `8 passed`
- target tests: `97/97 PASS`

The target matrix included:

- CNX-423 provenance/ACP identity;
- CNX-422 admission;
- core index;
- Dashboard delivery;
- direct model-call lease;
- direct recovery;
- session ownership;
- runtime-hook attestation.

No private OpenClaw SDK import was added.

## Fresh isolated OpenClaw v2026.9.4 runtime

Candidate was loaded in the previously established fresh isolated v2026.9.4 state on:

`127.0.0.1:19794`

The live Gateway remained separately bound to:

`127.0.0.1:18789`

Observed isolated startup:

- CNX loaded from the candidate `dist/v091-release-entry.js`;
- `reply_dispatch` registration observed;
- plugin load errors: `0`;
- Gateway reached `ready`;
- startup recovery mutation counts remained zero;
- no semantic provider request was sent.

Health:

- `ok=true`
- plugins loaded: `cogentnexus-openclaw`, `memory-core`
- plugin errors: `[]`

Runtime attestation:

- `runnerReady=true`
- `globalHookCount=7`
- plugin-specific registry count unavailable through public v2026.9.4 SDK
- classification: `AMBIGUOUS`

This is the same conservative public-SDK attestation behavior accepted in CNX-422.

### Clean shutdown

A Windows-native `CTRL_C_EVENT` was sent to the isolated Gateway console.

Observed:

- `signal SIGINT received`
- `admission closed: restart drain`
- `received SIGINT; shutting down`
- `active-work drain settled; beginning server close`
- `[shutdown] completed cleanly in 17ms`
- process exit code: `0`

After shutdown:

- isolated port `19794`: not listening
- live port `18789`: still listening
- live PID remained `13192`

## Migration/rollback evidence reuse

CNX-423 changes only reply-dispatch admission classification/identity normalization plus its regression test.

It does **not** change:

- OpenClaw state migration code;
- CogentNexus Ticket DB schema;
- startup recovery schema;
- installer/bootstrap behavior;
- session/transcript storage;
- copied-state migration boundary;
- rollback restore procedure.

Therefore the independent CNX-422 review explicitly allowed the copied-state migration/rollback evidence to be reused without rerunning the full copied-state migration.

Accepted inherited findings remain:

- OpenClaw shared DB migration: `v1 -> v17`;
- agent DB migration: `v1 -> v19`;
- sessions preserved: `19 -> 19`;
- binary-only downgrade to 2026.7.1-2: unsafe after migration;
- complete pre-upgrade snapshot restore: proven successful;
- future live upgrade requires full pre-upgrade state/config/session/workspace/CNX snapshot.

## Live-state closeout

At the end of CNX-423:

- live OpenClaw: `2026.7.1-2 (0790d9f)`
- live Gateway health: `ok=true`
- live Gateway listener: `127.0.0.1:18789`
- live PID: `13192`
- live sessions: `19`
- Discord: running and connected
- isolated qualification listeners `19794-19800`: none

No live upgrade or live state migration occurred.

## Changed files

Qualified implementation commit:

`59830e4512b89d8924295c886f121d077b3d6c61`

Files:

- `plugins/cogentnexus-openclaw/src/index.ts`
- `plugins/cogentnexus-openclaw/src/ticket-admission-kernel.ts`
- `plugins/cogentnexus-openclaw/src/cnx423-provenance-acp-identity.test.ts`

Implementation diff:

- `326 insertions`
- `6 deletions`

The majority is the dedicated regression matrix; production repair is intentionally narrow.

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

## Remaining risks

1. Live semantic acceptance has intentionally not been run in CNX-423.
2. Runtime attestation remains conservatively `AMBIGUOUS` for plugin-specific hook ownership because OpenClaw v2026.9.4 does not expose the active registry through the public plugin runtime SDK.
3. The known CNX-383 historical RED remains present.
4. Any future live upgrade must preserve the full-snapshot rollback prerequisite proven in CNX-422.
5. The successor controlled-upgrade task must retain source-owner/effective-dispatch identity semantics and must not regress provenance exclusion when live acceptance is added.

## Final decision

`READY_FOR_CONTROLLED_OPENCLAW_2026_9_4_UPGRADE_REVIEW`

CNX-423 has repaired the two blockers identified by the CNX-422 review and requalified the exact candidate against OpenClaw v2026.9.4 in isolated fresh state.

Stop for ChatGPT review before any live upgrade.
