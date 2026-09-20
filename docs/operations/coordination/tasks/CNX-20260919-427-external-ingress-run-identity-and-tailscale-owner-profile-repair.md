# CNX-20260919-427 — External Ingress Run Identity and Tailscale Owner Profile Repair

Status: `COMPLETE`

Parent: `CNX-20260919-426`

Executor: `ChatGPT via LConnect`

Reviewer: `ChatGPT`

Human final authority: `Operator`

Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Objective

Repair the two OpenClaw 2026.9.4 compatibility defects exposed by the operator's live Discord and Tailscale tests without weakening Ticket-first semantics, identity provenance, or Gateway authentication.

The target end state is:

1. external Discord ingress can proceed through CogentNexus Ticket-first admission even when the early `reply_dispatch` hook has no authoritative `runId`;
2. exactly one Ticket is created when the authoritative OpenClaw run identity becomes available;
3. Tailscale Serve remains authenticated and the remote Control UI can resolve the Gateway owner profile and use session/activity RPCs;
4. neither repair bypasses authentication, invents provider/model routing, synthesizes an untrusted run identity, or weakens fail-closed behavior at the true execution boundary.

## Live evidence

### A. Discord external-ingress failure

Channel:

`agent:main:discord:channel:1391855033993138217`

Operator-visible Discord channel ID:

`1391855033993138217`

Two live turns on 2026-09-19 were received by OpenClaw but did not reach CNX Ticket admission or model execution.

The exact traces were:

- `28918a57ed3b6262e763500a61ff420b`
- `4ea04d4c89877bc1305113111792190d`

Both traces contain:

`CogentNexus-OpenClaw reply_dispatch admission failed closed: missing-run-id`

immediately followed by:

`visible channel turn dispatched with no queued reply payloads ... cause=unknown`

No new CNX Ticket was created for either current Discord message.

The OpenClaw diagnostic watchdog later reported:

- `queued_work_without_active_run`
- `classification=stale_session_state`
- recovery action `release_lane`

This proves Discord transport/ingress itself was functioning; the turn was suppressed at the CNX early admission hook before an authoritative OpenClaw run identity existed.

### B. Tailscale remote Control UI profile verification failure

Remote UI:

`https://cdq-p.tail145b6c.ts.net/activity/gateway-owner`

Current relevant Gateway configuration:

- `gateway.auth.mode = token`
- `gateway.tailscale.mode = serve`
- `gateway.bind = loopback`
- allowed Control UI origin includes `https://cdq-p.tail145b6c.ts.net`
- named Gateway roles are not enabled

HTTPS and WebSocket transport reach the Gateway, but remote session RPCs repeatedly return:

`UNAVAILABLE: Authenticated profile verification is unavailable. Retry shortly; if this continues, contact a gateway administrator.`

Observed affected RPCs include:

- `sessions.subscribe`
- `sessions.groups.list`
- `sessions.describe`
- `chat.startup`

OpenClaw 2026.9.4 source defines the fail-closed state as:

`authenticatedGitHubIdentitySync && !authenticatedUserProfile`

The connection code installs `authenticatedGitHubIdentitySync` when the GitHub identity resolver exists. The durable profile resolution precedence is:

1. expected Gateway owner profile;
2. authenticated GitHub identity sync;
3. Tailscale identity;
4. email identity.

Therefore the remote browser is reaching a valid authenticated transport but remains in an unresolved durable-profile state. The repair must preserve this security boundary and fix identity/profile convergence instead of bypassing it.

## Root cause hypotheses to prove or reject

### Track A — Discord/CNX

Current CNX `reply_dispatch` admission calls the Ticket admission kernel before OpenClaw has necessarily assigned a run ID on external channel turns. The kernel correctly rejects a missing run ID, but the adapter currently treats that early lack of identity as a terminal admission failure.

Required distinction:

- **early adapter boundary:** missing run ID can mean `not assigned yet` and should defer;
- **execution boundary:** missing authoritative run ID remains a fail-closed error.

No synthetic run ID may be invented merely to make Discord pass.

### Track B — Tailscale/OpenClaw profile

The remote Control UI has an asynchronous GitHub-backed profile resolver attached but does not converge to `authenticatedUserProfile` before protected session methods are called.

The investigation must determine whether this is caused by:

- stale or incomplete migrated durable identity/profile rows;
- a GitHub identity resolver being activated for a token/Tailscale owner connection that should resolve to `gateway-owner`;
- an asynchronous profile-sync path that is never invoked/completed;
- or another 2026.9.4 connection-state defect.

The repair must use the narrowest supported configuration/state/source fix. Disabling profile verification or broadly relaxing remote authorization is not acceptable.

## TDD requirements — Track A

Add focused CNX-427 tests that prove:

1. external-channel `reply_dispatch` with a valid owner session but no run ID does **not** create a Ticket and does **not** fail the turn;
2. the later `before_agent_run` with authoritative run ID creates exactly one Ticket;
3. same-run dual-adapter idempotency remains exactly one Ticket;
4. Dashboard/ACP paths that already possess a run ID retain current Ticket-first behavior;
5. execution-boundary missing run ID remains fail-closed;
6. malformed/untrusted session identity is not converted into a deferred authorization bypass.

RED must fail against the pre-repair source.

## Validation requirements — Track B

Before any live state mutation:

1. inspect current durable `user_profiles`, `user_profile_identities`, `user_profile_emails` and relevant auth state without exposing secrets;
2. trace the 2026.9.4 profile resolver and remote owner admission path;
3. prove the exact mismatch with a bounded local/source-level reproduction where practical;
4. prefer a documented config/state reconciliation if it preserves all security checks;
5. if the defect is in OpenClaw 2026.9.4 source, produce a minimal source-level repair and validation evidence before installing it.

## GREEN acceptance

### Discord

- live Discord message reaches `before_agent_run`;
- one CNX Ticket is accepted;
- provider/model remains OpenClaw-owned;
- one assistant response is delivered to Discord;
- no `missing-run-id` fail-closed event occurs at early `reply_dispatch`;
- no duplicate Ticket is created;
- no stale session lane remains.

### Tailscale remote Control UI

- Tailscale Serve remains enabled;
- remote HTTPS and WebSocket remain authenticated;
- `authenticatedUserProfile` resolves to the intended durable owner profile;
- `sessions.subscribe`, `sessions.groups.list`, `sessions.describe`, and `chat.startup` no longer fail with `AUTHENTICATED_PROFILE_UNAVAILABLE`;
- local Control UI remains functional;
- Gateway/Discord/Supervisor/SQLite health remain GREEN.

## Safety boundaries

- no auth bypass;
- no disabling profile verification;
- no synthetic run identity for external ingress;
- no force push;
- no main/tag/release mutation;
- no provider/model routing moved into CNX;
- no destructive Tailscale logout/reset/re-auth unless separately required by evidence and operator action;
- preserve rollback ability for every live mutation.

## Final classifications

PASS:

`EXTERNAL_INGRESS_AND_TAILSCALE_OWNER_PROFILE_REPAIR_GREEN`

Partial/blockers must use a narrower evidence-backed classification rather than claiming full success.

## Execution checkpoint — 2026-09-19

Track A has been repaired, qualified, and deployed live.

- source commit: `4ed98c8c5cbd03b3cd26acff8082fc1f14c0537b`;
- focused regression: 39/39 PASS;
- plugin validation: PASS;
- full suite: 381/382 PASS, with only the pre-existing CNX-383 baseline failure;
- qualified package SHA256: `1E1D337FEAFC339A3E1523C68C751D04DC72CA00C7BBF84770AEFF1390D89491`;
- live `dist/index.js` SHA256: `6D96AD5FC4F419105E7E6A82EC941926886A05937C143E599C47FE9143A8FBE3`.

Track B root cause is now proven as transient GitHub identity verification failure rather than Tailscale transport failure.

Pre-restart remote connections authenticated as `funggier@github`, then GitHub identity synchronization failed with HTTP 403. After the controlled Gateway restart, Tailscale Serve came back GREEN, the remote browser authenticated again, and previously failing session RPCs completed successfully without any new profile-verification failure. No auth bypass or additional GitHub credential was introduced.

The final operator-originated Discord gate was completed successfully on 2026-09-20.

## Live acceptance discovery — second-stage Ticket-first gap

The first live Discord acceptance after deploying the early `reply_dispatch` deferral produced a visible correct reply but exposed a deeper Ticket-first gap.

Operator message:

`@Ce ตอบคำว่า CNX427_OK เท่านั้น`

Visible assistant reply:

`CNX427_OK`

Live evidence:

- trace ID: `343c6efbf788333b585d1160af9ed4e6`;
- early `reply_dispatch` correctly logged `admission deferred: authoritative run identity is not assigned yet`;
- OpenClaw subsequently created authoritative run ID `a0660423-e586-4e89-a5c9-fca25d842e1d`;
- the model executed and Discord delivered the reply;
- CNX `message_sent` correctly refused ambiguous receipt correlation without a run ID;
- **no CNX Ticket exists for the 15:38 Discord turn**.

Therefore the first repair restored delivery but did not satisfy Ticket-first. The live turn would be a false PASS if judged only by visible output.

### Refined root cause

OpenClaw 2026.9.4 external Discord dispatch invokes CNX `reply_dispatch` before an authoritative run ID exists. After deferral, this execution path does not invoke the CNX `before_agent_run` handler in the effective Discord execution scope, even though `before_agent_run` is supported by the embedded runner and is observed on Dashboard runs.

OpenClaw creates the authoritative run ID before `before_agent_reply` in `embedded-agent-runner/run-orchestrator.ts`. That hook receives the exact run ID, session key, channel and identity context before model execution. CNX-427 will qualify a narrow second-stage adapter at that supported boundary rather than synthesizing a run ID or moving admission after inference.

### Additional acceptance requirements

The final Discord acceptance must now prove all of the following in the same turn:

1. early `reply_dispatch` defers missing run identity;
2. authoritative host run identity is later observed before inference;
3. exactly one Ticket is created before the model executes;
4. no duplicate is created if another admission hook also sees the same run;
5. one assistant response is delivered;
6. the Ticket reaches terminal delivered/completed state;
7. no ambiguous receipt is used as authority for Ticket creation.

## Final Discord acceptance — GREEN

The operator sent exactly one genuine Discord turn on channel `1391855033993138217`:

`@Ce CNX427_FINAL_ACCEPTANCE_20260920_A1 Reply exactly: CNX427_FINAL_OK_20260920_A1`

Observed lineage:

- physical OpenClaw session: `06e736f1-01e5-45b7-8c0b-bbaa9ed6f700`;
- authoritative run: `e683efcf-b00e-4ee9-bb11-cac0da94a840`;
- CNX Ticket: `CNXT-d6ed7093-5440-435d-91f7-77caaac7ffb3`;
- inference attempt: `cnx-attempt-8004886f-cf61-468d-8dd3-e7649a374398`;
- durable delivery: `27`;
- owner generation: `7`.

Ordering and cardinality from the clean pre-send baseline:

- Tickets: `47 -> 48` (+1);
- direct model calls: `35 -> 36` (+1);
- inference attempts: `33 -> 34` (+1);
- assistant deliveries: `26 -> 27` (+1);
- exactly one new target-channel Ticket;
- exactly one Ticket for the authoritative run;
- Ticket accepted at `2026-09-20T07:04:19.655Z`;
- model call started at `2026-09-20T07:04:19.714Z`;
- inference attempt started at `2026-09-20T07:04:19.726Z`;
- Ticket persistence therefore preceded model-call authority by about 59 ms;
- no direct-recovery row exists for the accepted Ticket;
- no duplicate Ticket, duplicate model call, duplicate inference attempt, or stale-generation settlement occurred.

Terminal delivery proof:

- model call ended `completed` at `2026-09-20T07:22:51.387Z`;
- inference attempt ended `completed` at `2026-09-20T07:22:51.396Z`;
- `response_ready` at `2026-09-20T07:22:51.460Z`;
- durable delivery row 27 was created at `2026-09-20T07:22:51.578Z`;
- durable idempotency key:
  `cnx-discord:CNXT-d6ed7093-5440-435d-91f7-77caaac7ffb3:g7:cnx-attempt-8004886f-cf61-468d-8dd3-e7649a374398`;
- delivery settled as `delivered / confirmed`;
- receipt evidence type:
  `discord-message-receipt-marker`;
- `delivery_confirmed` event count = `1`;
- `completed` event count = `1`;
- Ticket terminal status = `completed`;
- exact delivered text:
  `CNX427_FINAL_OK_20260920_A1`.

OpenClaw trajectory independently recorded:

- finalStatus = `success`;
- timedOut = `false`;
- provider/model = `ollama / qwen3.8:27b`;
- input tokens = `12105`;
- output tokens = `19`;
- compaction count = `0`;
- assistant text = `CNX427_FINAL_OK_20260920_A1`;
- target session status = `done`.

The operator supplied visual Discord screenshots confirming exactly one visible assistant response with the exact expected text.

Current local-model policy remains intentionally unchanged:

- primary model `ollama/qwen3.8:27b`;
- `contextWindow=24576`;
- `num_ctx=24576`;
- `OLLAMA_CONTEXT_LENGTH=24576`;
- `OLLAMA_KEEP_ALIVE=2h`.

The live acceptance used 24K context successfully. During execution llama-server private memory reached about 21.4 GB and free physical RAM was observed as low as about 1.3 GB, so 24K remains the operator-approved default unless future workload proves insufficient.

Final classifications:

`CNX427_EXTERNAL_INGRESS_TICKET_FIRST_DURABLE_DISCORD_GREEN`

`OPENCLAW95_DISCORD_DURABLE_MARKER_SETTLEMENT_GREEN`

Final acceptance report:

`docs/operations/coordination/reports/CNX-20260920-427-440-final-discord-acceptance-report.md`
