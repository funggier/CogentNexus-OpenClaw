# CNX-20260827-093 — Repair Dashboard Durable Payload Staging Boundary

Status: `READY_FOR_HERMES`

Execution mode: `SOURCE_TDD_DASHBOARD_DURABLE_PAYLOAD_STAGING_REPAIR`

Current authorization: `TASK092_DASHBOARD_DELIVERY_STAGING_DIAGNOSIS_AND_REPAIR_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Diagnose and repair the exact source boundary that allowed Task 092's authenticated fresh Dashboard/WebChat response to become visibly rendered while no durable `cnx_assistant_delivery` Direct-result row was captured, causing the Ticket to fail closed instead of reaching `delivery_confirmed -> completed`.

This task is source/test-only plus read-only inspection of the exact installed OpenClaw `2026.7.1-2` runtime/log contract. It must not send another semantic message or mutate the accepted live installation.

The final semantic retest is a later task.

## Accepted predecessor evidence

Task 092 report:

`docs/operations/coordination/reports/CNX-20260827-092-final-fresh-session-semantic-acceptance.md`

Report HEAD:

`0939c8b0659f0254c754dd7bbf44dc422648c4da`

Independent review:

Decision: `ACCEPT`

Disposition:

`ACCEPT_BLOCKER_DASHBOARD_DURABLE_PAYLOAD_STAGING`

Review path:

`docs/operations/coordination/reviews/CNX-20260827-092-final-fresh-session-semantic-acceptance.md`

Accepted live semantic evidence from Task 092:

- authenticated `openclaw-control-ui`, mode `webchat`, owner/admin scope proven;
- first New chat entered a clean fresh staged state;
- new semantic session: `agent:main:dashboard:76932fbc-9df2-4415-9020-b6c1d7228505`;
- no stale/unknown/missing-parent failure;
- exactly one semantic message;
- Ticket `CNXT-90b73131-5460-4d0d-8669-2bc86a544754`;
- run `a2ea6b32-fd1a-4235-a6c5-820d475ea4cc`;
- `accepted -> routed` before correlated `ollama/qwen3.5:9b` inference;
- direct model call count `1`;
- exact nonce visibly rendered once;
- exactly one `response_ready`;
- `cnx_assistant_delivery` rows `0`;
- `delivery_confirmed_at = null`;
- Ticket failed permanent with fail-closed no-regeneration message.

Task-092 nonce/session/Ticket/run are retired evidence. Do not reuse or manually repair them.

## Source boundary under investigation

Accepted source installed live remains:

`d6daf8f93fcd5578f267b2017c6cc82e5de20095`

Relevant source:

- `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`
- `plugins/cogentnexus-openclaw/src/v091-release-entry.ts`
- `plugins/cogentnexus-openclaw/src/index.ts`
- `plugins/cogentnexus-openclaw/src/ticket-store.ts`
- adjacent v0.9.2/v0.9.5/v0.9.7/v0.9.9 compatibility layers and tests.

The intended invariant is:

> The exact Dashboard Direct final text must be durably captured as one pending `cnx_assistant_delivery(kind='direct_result')` row before the native transport can make the response visible. Only then may native delivery/marker confirmation terminal the Ticket.

Task 092 falsified this invariant in the live Control UI path: visible response existed while the durable Direct-result row never existed.

---

# Absolute live/semantic fence

Task 093 is source/test-only with read-only installed-source/log/DB inspection.

Do NOT:

- send Dashboard/WebChat content;
- call `chat.send`, `chat.inject`, `openclaw agent`, `sessions_send` or any channel send;
- generate a new semantic nonce;
- call Ollama/provider directly;
- mutate the Task-092 failed Ticket/session/transcript;
- install/install-over/uninstall/reset/cleanup;
- mutate plugin generations;
- edit live controller/startup/Supervisor/AGENTS/ownership/runtime/config;
- change model/provider/timeouts;
- restart/reboot merely to diagnose;
- merge/tag/release.

Read-only inspection of Task-092 Gateway logs, plugin inventory, session metadata and SQLite is allowed. Never disclose Gateway bearer secrets.

Use a fresh isolated source worktree from the current coordination execution HEAD.

---

# Phase A — publication and live-evidence re-proof

1. Fetch coordination branch and record execution HEAD.
2. Prove Task-092 report and ACCEPT review are ancestors.
3. Verify Task-092 publication fence remains report-only.
4. Create a clean isolated worktree.
5. Read-only recheck that live product remains MANAGED/healthy; do not repair drift in this task.
6. Preserve exact Task-092 Ticket/run/session/event evidence and confirm no manual mutation has rewritten it.

If the failed evidence cannot be trusted, stop with:

`BLOCKED_TASK092_EVIDENCE_DRIFT`.

---

# Phase B — root-cause investigation before edits

No production edit is allowed until one exact failing boundary is proven.

## B1 — inspect exact OpenClaw 2026.7.1-2 WebChat delivery lifecycle

Inspect the exact installed OpenClaw build, not current online docs, for:

- `chat.send` Control UI path;
- WebChat final response emission;
- `reply_dispatch` hook invocation and dispatcher construction;
- `message_sent` hook behavior for WebChat;
- `agent_end` ordering relative to native visible delivery;
- plugin register/reload/hot-reload hook cleanup behavior;
- whether plugin re-registration can occur in the same Node process/API lifecycle;
- event/context fields (`runId`, `sessionKey`, dispatcher API, final payload shape, queued counts) for the actual WebChat path.

Record source locations and sanitized conclusions.

## B2 — correlate Task-092 runtime evidence

Read existing Gateway/plugin logs around:

- run `a2ea6b32-fd1a-4235-a6c5-820d475ea4cc`;
- provider end `2026-08-27T04:03:39.036Z`;
- response-ready `2026-08-27T04:03:39.125Z`.

Determine which relevant plugin hooks were actually registered/invoked if logs/source permit. Do not generate a new turn merely to improve logging.

## B3 — test root-cause candidate H1 first

Strong candidate:

`installV091DashboardVerifiedDelivery()` uses one prototype `PATCH` symbol to guard both:

1. one-time `TicketStore.prototype` monkey-patching; and
2. `api.on('reply_dispatch', ...)` runtime hook registration.

Because the function returns immediately when the prototype already has `PATCH`, a later plugin registration in the same process can inherit patched TicketStore methods but receive no new `reply_dispatch` staging hook.

This would exactly explain Task 092:

- V091 patched finalizer/recovery semantics active;
- `response_ready` produced;
- V091 fail-closed unverifiable-delivery message produced;
- no `cnx_assistant_delivery` row staged.

Prove or falsify H1 by examining exact OpenClaw registration lifecycle and by an executable unit/integration reproduction using two runtime API registration instances/lifecycles.

Required RED if H1 is correct:

- first install/register obtains the verified-delivery hook;
- second legitimate runtime registration after prototype patching obtains **no** staging hook under current source;
- TicketStore remains patched;
- a Dashboard Direct final on the second runtime reaches finalization without creating `cnx_assistant_delivery`.

## B4 — if H1 is falsified, inspect hook-shape/early-return candidate H2

The verified-delivery handler can return without staging when any of these conditions differ from the test fixture:

- neither event nor context exposes runId;
- dispatcher/`appendBeforeDeliver` absent;
- `info.kind` not `final`;
- payload text is not at `payload.text`;
- media flag is present;
- `getQueuedCounts().final !== 1`;
- Dashboard ticket/session authority lookup cannot correlate the run.

Use the exact installed OpenClaw source and Task-092 evidence to identify the actual shape. Create a faithful RED fixture for the exact WebChat path.

Do not patch several hypotheses at once.

## B5 — if neither H1 nor H2 is sufficient

Continue backward tracing from the visible WebChat payload to the earliest supported plugin hook that executes **before native visibility** and carries enough identity/payload data for exact durable capture.

If exact OpenClaw exposes no supported pre-visible-delivery plugin boundary capable of exact capture, stop with:

`BLOCKED_NO_SUPPORTED_PRE_DELIVERY_CAPTURE_BOUNDARY`

Do not falsely confirm delivery after visibility merely to pass the test.

---

# Gate R — mandatory RED

After Phase B identifies one root cause, create the smallest executable failing test that reproduces it under the accepted source.

The RED must prove the observed Task-092 class:

- Dashboard Direct Ticket exists and is routed direct;
- one final native-visible payload exists or is about to be emitted;
- current staging boundary fails to create the durable Direct-result row;
- patched finalization can reach `response_ready` without `cnx_assistant_delivery`;
- later recovery would fail closed as unverifiable.

The test must use the actual production registration/hook implementation, not a test-only copy of the logic.

Watch the RED fail for the intended reason before production changes.

---

# Gate F — minimal root-cause fix

Only after RED.

Requirements for any accepted fix:

1. Durable exact final text is committed before the corresponding native Dashboard/WebChat final can become visible.
2. Exactly one `cnx_assistant_delivery(kind='direct_result', status='pending')` row owns the payload.
3. The payload is bound to exact Ticket/run/owner session generation.
4. Native transport receives the exact visible result plus the internal idempotency marker where the existing contract requires it.
5. Successful verified native settlement produces exactly one `delivery_confirmed` and one `completed`.
6. Failure remains retry/fail-closed according to the existing durable ownership rules; never regenerate a visible result speculatively.
7. Generic `message_sent` receipts cannot terminal a durable-staged Dashboard result early.
8. CLI/non-Dashboard sessions cannot claim Dashboard delivery ownership.
9. Repeated plugin/runtime registration cannot lose the staging hook or create duplicate staging hooks.
10. Existing Task-078/079/080 owner/run delivery fences remain intact.

### If H1 is proven

Separate prototype-patch idempotence from runtime-hook registration lifetime.

Do not assume a `WeakSet<Api>` is correct until exact OpenClaw API-object/reload lifetime is understood. The solution must register exactly one verified-delivery hook for each legitimate active plugin registration lifecycle while avoiding duplicate handlers within the same active lifecycle.

### If H2 is proven

Adapt only the exact run/payload/dispatcher correlation required by installed OpenClaw 2026.7.1-2. Do not broaden owner trust or accept ambiguous session/run correlation.

No unrelated refactor.

---

# Gate T — required regression matrix

At minimum add/re-run tests proving:

1. exact Task-092 fresh Dashboard/WebChat production-shaped final path stages a durable row before transport;
2. one active registration -> one staging hook;
3. legitimate re-registration/reload -> active runtime still has staging hook;
4. no duplicate staging/handler side effect;
5. staged final + successful dispatcher settlement -> `response_ready -> delivery_confirmed -> completed` exactly once;
6. staged final + failed/cancelled native delivery remains durable/retry-safe without regeneration;
7. unstaged/unverifiable legacy response remains fail-closed;
8. wrong run/session/non-Dashboard path cannot stage or settle another Ticket;
9. duplicate final observation is idempotent; changed text under same delivery identity fails closed;
10. fresh-session owner key `agent:main:dashboard:<uuid>` is accepted by Dashboard staging without relying on old Main session identity;
11. session successor/rebind behavior is not regressed;
12. Task-092 first-New-Session behavior remains source-compatible; do not introduce parent-session assumptions.

---

# Full verification

After GREEN record fresh evidence for:

- focused delivery-staging RED/GREEN suite;
- v0.9.1 Dashboard verified-delivery tests;
- v0.9.2 durable-delivery boundary tests;
- v0.9.5/v0.9.7/v0.9.9 recovery/ownership tests;
- registered owner-admission tests;
- full plugin suite on Node 24/npm 11;
- full plugin suite on Node 22/npm 12;
- `npm run plugin:validate` on both supported paths;
- package-content/bootstrap gates;
- full Python suite;
- baseline consistency;
- `git diff --check`;
- clean final worktree.

Any plugin payload source change changes the plugin fingerprint. Record the exact new source fingerprint for the later supported install-over task; do not mutate live state here.

---

# Publication fence

Commit source/tests first.

Then publish a separate report-only commit:

`docs/operations/coordination/reports/CNX-20260827-093-repair-dashboard-durable-payload-staging-boundary.md`

Required result tokens:

- `PASS_DASHBOARD_DURABLE_PAYLOAD_STAGING_REPAIRED`
- `BLOCKED_TASK092_EVIDENCE_DRIFT`
- `BLOCKED_DELIVERY_STAGING_ROOT_CAUSE_UNPROVEN`
- `BLOCKED_NO_SUPPORTED_PRE_DELIVERY_CAPTURE_BOUNDARY`
- `BLOCKED_DELIVERY_STAGING_SECURITY_REGRESSION`
- `BLOCKED_TEST_OR_VALIDATION_FAILURE`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Successor gate

Only independent acceptance of:

`PASS_DASHBOARD_DURABLE_PAYLOAD_STAGING_REPAIRED`

may authorize a supported live install-over of the new exact source/fingerprint.

A new semantic acceptance message remains forbidden until that updated source is installed and live parity/MANAGED health are independently accepted.

The eventual final semantic retest must use:

- a new authenticated fresh Dashboard/WebChat session;
- a new execution-time nonce;
- exactly one new semantic message;
- Ticket-before-provider ordering;
- durable exact payload staging before native visibility;
- `delivery_confirmed -> completed`;
- post-completion second New Session continuity without another send.
