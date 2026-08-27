# CNX-20260827-103 — Diagnose Live Dashboard Durable-Staging Boundary

## Result

`BLOCKED_ROOT_CAUSE_NOT_YET_ISOLATED`

Task 103 completed the authorized read-only diagnosis. It eliminated installed/source/dist parity failure and verified that the active release boundary registers the verified-delivery hook in a disposable production-shaped harness. Existing live evidence proves the final durable staging row was absent before the direct-delivery deadline, but does not record whether the live `reply_dispatch` handler ran, whether its `appendBeforeDeliver` callback ran, which filter predicate rejected the payload, or whether staging threw before commit. Therefore no single H3/H4/H5/H6 root-cause token is asserted.

No product fix, semantic resend, provider probe, live SQLite/config/runtime mutation, install/reset, restart, credential access, or maintained-source/test edit was performed.

## Phase A — execution and baseline fence

- Task-103 execution started from synchronized remote HEAD: `7c1a1aa722a22a726cd67f7dafc3a4c5b55b7c61`.
- Task-102 report commit `4d23875f4c402cf47109439ebd6b6b5eb72e131b` is an ancestor.
- Task-102 independent review is present in the synchronized branch and is an ancestor.
- Task-103 report was absent before this report-only publication.
- The accepted live plugin source fingerprint remains `df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`.
- OpenClaw CLI/runtime identity is `2026.7.1-2 (0790d9f)`, matching the required exact build.
- The live SQLite baseline remained integrity `ok`; after the already-completed Task-102 lifecycle the read-only counts were: tickets `2`, ticket events `14`, ticket outbox `0`, direct model calls `2`, assistant deliveries `0`, direct recovery rows `0`.
- The Task-102 Ticket remained the only new semantic artifact and was terminally failed by the existing no-regeneration safety policy; no Task-103 semantic/provider effect was observed.

## Phase B — source → dist → installed runtime parity

### Repository source

The repository source contains:

- `plugins/cogentnexus-openclaw/src/v091-release-entry.ts`: calls `installV091DashboardVerifiedDelivery(api, config)` after legacy registration.
- `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`: contains `REGISTERED_APIS`, `api.on("reply_dispatch", ...)`, run-id fallback, `appendBeforeDeliver`, final-kind/cardinality/media filters, and `stageDashboardDirectResult`.

Relevant source hashes:

- `src/v091-release-entry.ts`: `2460df988386be4f40d387d4b8c441a61b332bd30a473d38cea4e1f0ea172169`
- `src/v091-dashboard-verified-delivery.ts`: `2020a6a9db5e6875b058c03f72dc734e7096238632e429a86409e47dd182aced`
- `package.json`: `fb18fc75cae471f359ca5d51cc59c65e65999276cbaf93dabfc8e65d2114eb26`

### Repository dist vs installed live dist

The following repository and active installed files were byte-identical:

| Artifact | Repository SHA-256 | Installed live SHA-256 | Result |
| --- | --- | --- | --- |
| `dist/v091-release-entry.js` | `fa959512c8a7a1bf07c07f367ac1759521edf50155bfc2e3ac5cdac7e14da276` | same | PASS |
| `dist/v091-dashboard-verified-delivery.js` | `6f1bfb6a4532618ec0fa01cad3d0bc522908f235a47a9cfbefcf0dc529d7faa8` | same | PASS |
| `dist/index.js` | `96d3341cb6025034eff6aa59efc62cb6a18bdecbfe072422fa41a45031a4da19` | same | PASS |
| `package.json` | `fb18fc75cae471f359ca5d51cc59c65e65999276cbaf93dabfc8e65d2114eb26` | same | PASS |

Installed live plugin path resolved by `openclaw plugins list`:

`~/.openclaw/npm/projects/openclaw-plugin-cogentnexus-openclaw__openclaw-generation__g-8e5adec878a7c4e3/node_modules/openclaw-plugin-cogentnexus-openclaw/dist/v091-release-entry.js`

The active plugin was listed as enabled, version `0.9.3`, with that installed release-entry path. H1 is eliminated. No installed shadow-copy mismatch was found.

## Phase C — exact OpenClaw hook contract

The installed OpenClaw package is version `2026.7.1-2`; `openclaw --version` returned `OpenClaw 2026.7.1-2 (0790d9f)`.

The installed declarations define:

- `PluginHookReplyDispatchEvent.runId?: string` and `sessionKey?: string`;
- `PluginHookReplyDispatchContext.cfg`, `dispatcher`, `recordProcessed`, and `markIdle`;
- `ReplyDispatcher.appendBeforeDeliver?: (payload, info) => Promise<ReplyPayload | null> | ReplyPayload | null`;
- `getQueuedCounts()`, `getFailedCounts()`, and optional `getCancelledCounts()`;
- `ReplyDispatchRuntimeInfo.kind` with the final-kind path used by the plugin.

The installed runtime `dispatch` implementation invokes `hookRunner.runReplyDispatch(createReplyDispatchEvent(...))` and passes `dispatcher: dispatchHookDispatcher`, `runId: params.replyOptions?.runId`, and the lifecycle callbacks. The hook runner uses sequential first-claim semantics, but a handler only short-circuits when it returns `{ handled: true }`; the legacy observer handler returns `undefined` and does not claim the dispatch.

The exact contract therefore supports the verified-delivery implementation. H2 is eliminated at the release-registration level, and a static contract mismatch is not proven for H4.

## Phase D — Task-102 live correlation

Preserved Task-102 trajectory:

- OpenClaw runtime: `2026.7.1-2`, provider `ollama`, model `qwen3.5:9b`;
- exact Dashboard session: `agent:main:dashboard:89992501-1b33-46cf-85f7-eb0c1ef4d311`;
- exact Task-102 Ticket: `CNXT-415b82d9-5553-4bd2-996a-54f57163f7e4`;
- exact run ID is preserved in SQLite and event payloads but is not repeated here beyond the already-authorized diagnostic correlation;
- model completed successfully and the exact nonce was visibly rendered once;
- Ticket event sequence: `accepted`, `routed`, `direct_model_call_started`, `direct_model_call_ended`, `response_ready`, then timeout safety failure and `failure_delivery_suppressed`;
- no `direct_response_durable`, `delivery_confirmed`, or `completed` event;
- `cnx_assistant_delivery = 0` and `ticket_outbox = 0`.

The failure payload says: `direct response delivery became unverifiable before the final payload was durably captured; refusing regeneration to avoid duplicate output`.

The trajectory records session/model lifecycle but no `reply_dispatch`, `appendBeforeDeliver`, staging-result, filter-reason, or staging-exception event. Existing runtime logs available for this diagnosis likewise contain no guaranteed hook invocation marker. Per the task contract, absence of a non-guaranteed log line is not treated as proof that the handler did not run.

## Boundary table

| Boundary | Expected | Observed | Proven/Unproven |
| --- | --- | --- | --- |
| release entry active | installed `v091-release-entry.js` active | plugin enabled and active path resolves to installed dist | Proven |
| hook registered | verified-delivery adds one runtime `reply_dispatch` handler | disposable real release registration captured three compatibility-layer registrations, including verified handler | Proven for registration; live invocation unproven |
| `reply_dispatch` emitted | final Dashboard response reaches dispatch hook | exact runtime contains and invokes the hook in the normal dispatch implementation; Task-102 trace has no hook marker | Emission for Task-102 unproven |
| run correlation | event or context carries Task run ID | installed type/event builder supports event `runId`; plugin also supports `ctx.runId` fallback | Static contract proven; live value unproven |
| dispatcher available | `appendBeforeDeliver` callable | exact type/runtime provides it; disposable callback reproduction received it | Static and disposable proof; live availability unproven |
| final payload filter | one text final, no media, `kind=final`, final count one | source requires these predicates; Task-102 payload shape was not captured at this boundary | Unproven |
| stage function entered | exact run/text calls `stageDashboardDirectResult` | no `direct_response_durable` row/event and no guaranteed stage log in Task-102 | Unproven whether skipped before entry or failed inside |
| durable write | one pending assistant-delivery row | zero rows; later timeout safety failure | Proven absent |
| terminal settlement | delivery confirmation and completed | neither occurred | Proven absent |

## Phase E — production-shaped source-only reproduction

A disposable harness was created outside maintained product source and removed after execution. It loaded the real repository `dist/v091-release-entry.js`, used a temporary managed controller and temporary SQLite databases, captured the actual release registration boundary, and invoked all captured `reply_dispatch` handlers using the installed OpenClaw callback shape.

Results:

- release registration completed under Host `managed`;
- `reply_dispatch` handler count captured: `3` across compatibility layers;
- `appendBeforeDeliver` callbacks captured: `2` (legacy observer plus verified-delivery handler);
- with `runId`, active Dashboard session, `kind=final`, `finalCount=1`, text-only payload and no media, the verified handler inserted exactly one `cnx_assistant_delivery` row;
- the returned native payload contained the expected delivery marker;
- the verified handler logged durable staging before native delivery.

This reproduction proves the source/dist/release registration path can stage successfully under the modeled OpenClaw callback. It does not prove which live boundary diverged during Task 102, because the live hook payload and invocation trace were not captured.

## H1–H6 disposition

- **H1 — installed/runtime payload mismatch:** eliminated. Source, repository dist, package manifest, installed dist, active plugin entry, and fingerprint were consistent.
- **H2 — verified-delivery installer not registered:** eliminated for the active release registration boundary. The active plugin is enabled and the real release-entry harness registered the verified handler.
- **H3 — Dashboard bypasses `reply_dispatch`:** open. The exact OpenClaw build supports `reply_dispatch`, but Task-102 evidence does not prove the Dashboard path emitted it.
- **H4 — callback context contract mismatch:** open but not proven. Static exact types provide the required fields; Task-102 did not capture the runtime callback object or dispatcher shape.
- **H5 — final payload filter/correlation rejected:** open. No live payload/filter telemetry exists to distinguish missing run ID, non-final kind, count/media rejection, session correlation failure, or a successful callback that never reached staging.
- **H6 — staging attempted and failed before commit:** open. No staging exception or transaction error was recorded; zero row alone cannot distinguish non-entry from pre-commit failure.

## Root-cause decision

`BLOCKED_ROOT_CAUSE_NOT_YET_ISOLATED`

The first failing boundary cannot be selected safely from the preserved live evidence. The missing evidence is specifically a bounded, non-secret hook trace around the final Dashboard response containing: handler entry, event/context key presence (values redacted or hashed where appropriate), dispatcher method availability, `info.kind`, queued final count, media presence, stage return reason, and any pre-commit exception class. Adding such observability is a successor implementation/diagnostic task; it was not performed here.

## Minimal successor repair/diagnostic design

Before any new semantic retest or source fix, create a separately approved task that:

1. adds narrowly scoped, redacted diagnostics around the verified `reply_dispatch` handler and `stageDashboardDirectResult` boundary;
2. records only booleans/enumerated reasons, hashed correlation identifiers, and non-secret counts—never prompt text, credentials, tokens, or provider payloads;
3. covers handler entry, callback registration, final filter result, stage result reason, transaction begin/commit outcome, and exception class;
4. adds a RED source-only reproduction for the exact observed failing branch, then a GREEN regression through the real release registration boundary;
5. verifies package/dist/installed fingerprint impact before any install-over;
6. only after the boundary is isolated, designs the minimal fix and a separately gated operator-assisted live retest. Any live retest must use the proven procedure where the operator clicks the exact composer once and confirms readiness before a single authorized Send.

No implementation is authorized by Task 103.

## Final verification and publication fence

- Task-103 disposable harness file was outside the repository and removed by its `finally` cleanup; no ephemeral diagnostic material is tracked.
- Maintained product source and tests remained unchanged.
- Live state was inspected read-only; no Task-103 semantic/provider/product mutation occurred.
- No credentials were accessed.
- `git diff --check` was run before publication.
- This file is the single Task-103 report-only artifact.
- Report HEAD and remote HEAD, plus the remote report blob, are verified in the final publication command below.
