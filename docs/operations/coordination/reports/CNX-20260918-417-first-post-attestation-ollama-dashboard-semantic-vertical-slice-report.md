# CNX-20260918-417 — First Post-Attestation Ollama Dashboard Semantic Vertical Slice Report

## Final classification

`BLOCKED_FRESH_DASHBOARD_TARGET`

The live runtime preflight was GREEN and the authenticated Firefox Dashboard successfully created exactly one fresh, empty session. The fresh session, however, materialized with inherited execution selection `openai/gpt-5.6-luna`, not the required unchanged `ollama/qwen3.8:27b` route. CNX-417 forbids provider/model selection changes and OpenAI requests. Execution therefore stopped before nonce generation and before any semantic send.

## Fresh GitHub authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Authoritative execution HEAD: `95cb91458592614ed9de5f1d63a981af7bd14e2f`
- Local HEAD, fetched remote-tracking tip, and live `git ls-remote` tip matched at the pre-action authority gate.
- ACTIVE and STATUS at `2026-09-18T09:22:13Z`: `READY_FOR_HERMES`, task `CNX-20260918-417`.
- Matching report at the authoritative tip: absent.
- The original checkout was 91 commits behind and contained unrelated tracked/untracked work. It was preserved unchanged. Execution/publication used the clean dedicated clone `C:\Users\CDQ-P\CogentNexus-OpenClaw-CNX417-20260918T0914Z`.

## Live preflight

Read-only preflight began at `2026-09-18T09:16:27Z`.

| Gate | Live result |
|---|---|
| OpenClaw version | `2026.7.1-2 (0790d9f)` |
| Controller | `cnxMode=active`, derived `managed`, desired Gateway `running` |
| Controller generation | `107` |
| Canonical CNX plugin count | exactly `1` |
| Plugin identity | `cogentnexus-openclaw`, version `0.9.5`, canonical direct root |
| Plugin state | `enabled=true`, `status=loaded` |
| Installed fingerprint | `fa7243b4b88fea0b3467a42bc917b1241540c9710ebf495dc04ac1d1963bd41c` |
| Gateway | healthy/reachable, PID `13192`, port `18789` |
| Gateway process | Node, installed OpenClaw `dist/index.js gateway --port 18789` |
| Supervisor | task `CogentNexus-OpenClaw-Supervisor`, enabled, `Ready` |
| Supervisor recent result | last run `2026-09-18T09:25:25Z`, result `0` |
| Maintenance marker | absent |
| Recovery | `READY`; supported read-only check reported no active maintenance marker and no provider incident with authority |
| Delivery | `READY`; supported read-only check reported no pending terminal deliveries |
| Pending outbox | `0` |
| SQLite integrity | `ok` |
| Active direct model calls | `0` |
| Default OpenClaw route | `ollama/qwen3.8:27b` |

No runtime-attestation RPC was repeated. CNX-416's accepted `PRESENT` attestation remained the baseline, and the Gateway PID remained `13192`.

## Admission configuration evidence

The Gateway status bound both CLI and service configuration to `C:\Users\CDQ-P\.openclaw\openclaw.json`. The one canonical loaded plugin had the following non-secret configuration:

- `enabled=true`
- `ticketFirst=true`
- `preInferenceAdmission=true`
- `enforcedMode=true`
- `providerMode=passthrough`
- `hooks.allowConversationAccess=true`

This satisfied the Ticket-first/pre-inference configuration gate without configuration mutation.

## Durable baseline

Captured read-only with SQLite URI `mode=ro` and `PRAGMA query_only=ON` before Dashboard activation:

| Durable object | Baseline count |
|---|---:|
| Tickets | 23 |
| Ticket events | 864 |
| Ticket outbox | 0 |
| Assistant deliveries | 14 |
| Direct model calls | 20 |
| Direct recoveries | 5 |
| CNX sessions | 58 |
| Context-maintenance rows | 0 |

Ticket states were accepted `3`, cancelled `4`, completed `16`. These accepted rows were pre-existing historical Discord lineages also present in CNX-416; the supported live Recovery and Delivery checks classified current actionable work as absent/READY. There were no active model calls and no pending outbox rows.

OpenClaw session baseline:

- session count `17`, `hasMore=false`;
- current Dashboard URL/session before New Session: `agent:main:dashboard:aba017ac-6eb6-4286-96c7-568b95ed94ef`;
- the current historical Dashboard session had prior transcript and `openai/gpt-5.6-luna` overrides;
- Gateway log byte cursor: `1128825`.

The pre-action baseline retained per-session file size, mtime, line count, and SHA-256 without copying transcript content into this report.

## Authenticated Firefox owner surface

- Browser: Mozilla Firefox, PID `27552`, HWND/window ID `983994`.
- Window title: `OpenClaw Control — Mozilla Firefox`.
- URL origin: `http://127.0.0.1:18789`.
- Current paired UI device at session creation:
  - client ID `openclaw-control-ui`;
  - client mode `webchat`;
  - role `operator`;
  - scopes `operator.admin`, `operator.read`, `operator.write`, `operator.approvals`, `operator.pairing`;
  - last seen `2026-09-18T09:22:59.229Z` by `device-token-auth`.
- No credential or bearer token was read, copied, typed, or reported.

## Fresh Dashboard target

One actual `New session` activation occurred at approximately `2026-09-18T09:22:58Z` through the authenticated Firefox UI.

Three preceding coordinate-calibration clicks were verified no-ops against non-semantic page areas: they did not change the URL, create a session, create a Ticket, start a provider call, or populate/submit the composer. The successful control activation is the only `sessions.create` line after the durable/log baseline.

Fresh target evidence:

- session key: `agent:main:dashboard:6e96fece-c6ad-47b9-bfb4-680dd8a3a75b`;
- materialized session ID: `18fab7b9-2fb1-409f-9aed-d79168aaffdc`;
- created at `2026-09-18T09:22:58.816Z`;
- CNX session state `active`, generation `0`;
- OpenClaw session count changed `17 -> 18`;
- CNX session count changed `58 -> 59`;
- URL changed from the historical session to the exact fresh key;
- UI displayed `Ready to chat` and an empty `Message Assistant` composer;
- transcript file contained exactly one `session` header row, zero user rows, and zero assistant rows;
- transcript file SHA-256: `5f4e6cf7ddb32d51f0f3cbcb35222ffc25f0e4756c28954e87668a496cef59af`;
- no stale/unknown/missing-parent error was displayed;
- parent metadata pointed to the previous Dashboard session, but no semantic transcript was inherited into the new transcript;
- Gateway log delta contained one `sessions.create`, read-only `sessions.list`/`chat.history`/`chat.metadata`, and zero `chat.send`, `chat.inject`, or `sessions_send` lines.

New Session itself caused no Ticket, ticket-event, outbox, assistant-delivery, direct-model-call, or direct-recovery delta.

## Blocking route mismatch

The required fresh-target route was `ollama/qwen3.8:27b`.

The actual fresh target materialized as:

- UI label: `GPT-5.6 Luna · Medium`;
- durable OpenClaw session metadata: `modelProvider=openai`;
- model: `gpt-5.6-luna`;
- `providerOverride=openai`;
- `modelOverride=gpt-5.6-luna`;
- parent session: `agent:main:dashboard:aba017ac-6eb6-4286-96c7-568b95ed94ef`.

This proves that New Session inherited the previous session's execution selection even though the new semantic transcript was empty. Sending from this target would have violated all of the following CNX-417 gates:

1. target model must remain `ollama/qwen3.8:27b`;
2. provider/model selection changes are forbidden;
3. OpenAI requests must remain zero;
4. no alternate semantic transport is permitted.

No provider/model control was touched. No attempt was made to repair or override the target. The narrow task classification is therefore:

`BLOCKED_FRESH_DASHBOARD_TARGET`

## Nonce and semantic-send accounting

- nonce generated: `0`;
- nonce value: not applicable;
- composer text entered: `0`;
- Dashboard semantic sends: `0`;
- semantic retry/resend: `0`;
- direct Ollama/model probes: `0`;
- OpenAI requests: `0`;
- alternate semantic transports: `0`.

Because the fresh-target gate failed, no Ticket/run/model-call identifiers exist for CNX-417 and the Ticket-first/Ollama/result/delivery phases were not entered.

## Ticket, model-call, delivery, and duplicate ledger

| Evidence | Baseline | Final | Delta |
|---|---:|---:|---:|
| Tickets | 23 | 23 | 0 |
| Ticket events | 864 | 864 | 0 |
| Ticket outbox | 0 | 0 | 0 |
| Assistant deliveries | 14 | 14 | 0 |
| Direct model calls | 20 | 20 | 0 |
| Direct recoveries | 5 | 5 | 0 |
| CNX sessions | 58 | 59 | +1 fresh empty target |
| OpenClaw sessions | 17 | 18 | +1 fresh empty target |
| Active model calls | 0 | 0 | 0 |
| Pending outbox | 0 | 0 | 0 |
| Tickets owned by fresh target | 0 | 0 | 0 |
| User transcript messages in fresh target | 0 | 0 | 0 |
| Assistant transcript messages in fresh target | 0 | 0 | 0 |

Admission trace, accepted/routed ordering, provider start/end, response-ready, visible nonce, durable settlement, and duplicate semantic accounting are all not applicable because no semantic action occurred. There was no duplicate Ticket, route, provider call, result, delivery, recovery effect, or visible response attributable to CNX-417.

## Final health and preservation

Final read-only capture at `2026-09-18T09:25:55Z` proved:

- Gateway still healthy on PID `13192`;
- controller remained active/managed generation `107`;
- one canonical exact plugin remained enabled/loaded;
- default OpenClaw route remained `ollama/qwen3.8:27b`;
- Recovery remained READY;
- Delivery remained READY;
- pending outbox remained `0`;
- SQLite integrity remained `ok`;
- active model calls remained `0`;
- the fresh blocked target remained intact and empty;
- no session reset, delete, or compact occurred.

The screenshot and read-only evidence pack are retained under:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw-Acceptance-Evidence\CNX-20260918-417`

## Hard-fence cardinality

| Action | Count |
|---|---:|
| Actual New Session creations | 1 |
| Verified non-semantic/no-effect calibration clicks | 3 |
| Post-completion New Session | 0 |
| Dashboard semantic sends | 0 |
| Semantic resend/retry | 0 |
| Direct Ollama/model probes | 0 |
| OpenAI requests | 0 |
| Provider/model selection changes | 0 |
| Config mutations | 0 |
| Installer/install-over | 0 |
| Plugin lifecycle mutations | 0 |
| Gateway restart/reload/repair | 0 |
| CNX lifecycle mutations | 0 |
| Manual Ticket/outbox/recovery/SQLite mutations | 0 |
| Manual delivery/replay | 0 |
| Session reset/delete/compact | 0 |
| Release/tag/main operations | 0 |
| Force pushes/history rewrites | 0 |
| CNX-418 creation/start | 0 |

## Final classification

`BLOCKED_FRESH_DASHBOARD_TARGET`

The task stopped at the mandated pre-nonce boundary. A successor review must decide how to obtain a fresh Ollama-selected Dashboard target without violating the provider/model mutation fence. CNX-418 was not created or started.
