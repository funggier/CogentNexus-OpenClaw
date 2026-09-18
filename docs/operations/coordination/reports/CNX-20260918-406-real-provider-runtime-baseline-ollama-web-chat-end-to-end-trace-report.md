# CNX-20260918-406 — Real Provider Runtime Baseline: Ollama Web Chat End-to-End Trace

## Classification

`OLLAMA_VERTICAL_SLICE_MAPPED_READY_FOR_RED_TEST`

This is a read-only source/runtime archaeology report. The OpenClaw-owned Web Chat/session/provider path is mapped to the installed OpenClaw 2026.7.1-2 artifact and the repository's CNX boundary tests. A fresh semantic request was intentionally not sent under the task hard fence; claims requiring live UI/session/provider correlation are marked `REQUIRES_LIVE_AUTHORIZATION`.

## Authority and hard-fence compliance

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Authoritative starting remote HEAD: `5ca145e192427beb2547d365b87068db6384b9b4`
- Starting checkout: clean dedicated read-only clone at `C:\Users\CDQ-P\.hermes\workspace\CNX406-readonly`
- Starting gate: `READY_FOR_HERMES`
- Runtime artifact inspected read-only: `C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw`
- OpenClaw package: `2026.7.1-2`
- No Gateway restart/reload, provider/config/credential/environment mutation, provider selection, semantic request, dependency patch, CNX repair, deploy, release, force-push, or successor task: all `0`.

## Executive finding

OpenClaw already owns the route. Web Chat is a client of the Gateway chat/session APIs; the selected model is carried through the normal session boundary (`sessions.patch` for a model change), and the provider is represented by the provider/model route rather than by CogentNexus session identity. OpenClaw resolves the effective provider/model at execution time, runs the common Agent Core, emits normalized lifecycle/assistant/tool stream events, and persists/reloads session history through its session store.

CogentNexus does not need a provider router for this goal. Its intended intersection is provider-independent continuity and observation: Ticket/session/generation/policy, durable delivery/recovery, and model-call lease evidence. The current practical blocker is the separate CNX admission boundary: the repository records that OpenAI execution can succeed while `before_agent_run` is absent from the live composed hook registry, so Ticket-first continuity is skipped. This is not evidence that OpenClaw routing or Ollama invocation is missing.

## Ollama vertical sequence

```text
Web Chat control-ui chat page
  -> Gateway WebSocket/RPC (chat.send; session key; optional model metadata)
  -> session key resolution / session store
  -> selected session model state (sessions.patch is the model-selection boundary)
  -> OpenClaw model-ref normalization and provider/model resolution
  -> Agent Core / embedded agent runner
  -> provider adapter selected by resolved provider/model
  -> Ollama extension (provider discovery/config + Ollama stream adapter)
  -> Ollama HTTP transport (local base URL; streamed response)
  -> OpenClaw normalized lifecycle/assistant/tool events
  -> Web Chat stream delivery
  -> OpenClaw assistant/session transcript persistence
  -> next turn reads the same session key/history and resolves the current target
```

The exact outbound UI bundle is the installed artifact `dist/control-ui/assets/chat-page-DrPkxqJK.js`; the Gateway chat/session surfaces are `dist/gateway-chat-BW6uyvQL.js`, `dist/server-chat-wgxNCdC3.js`, and `dist/sessions-UcKjjh_n.js`. These are generated/minified runtime artifacts, so source symbol names are less legible than repository TypeScript. The strings and imports bind the UI to `sessions.patch`, `chat.send`, session keys, provider/model display, and Gateway chat RPC; exact live payload values require an authorized UI trace.

## Selection path

### What is direct source/runtime evidence

1. The installed Web Chat bundle contains the `sessions.patch` method and provider/model display/selection code (`control-ui/assets/chat-page-DrPkxqJK.js`).
2. The repository boundary test `plugins/cogentnexus-openclaw/src/v090-model-selection-boundary.test.ts:12-21,24-36` sends `{key, model}` to `sessions.patch`; the mocked Gateway returns `{resolved:{model, modelProvider:"ollama"}}`.
3. The same test at `:38-52` proves an existing CNX SQLite database remains byte-identical after a model change; `:55-72` proves repeated model changes create no Ticket/event state.
4. `tests/test_v095_provider_switch_matrix.py:14-33,35-49` models provider/model changes as OpenClaw-owned metadata and asserts CNX mode/generation/ownership remain unchanged and no `selectedProvider`/`desiredProvider` is introduced into CNX state.
5. `docs/PROVIDERS.md:5,32,46` states that Cloud routing/auth/model selection/runtime remain OpenClaw-owned; CNX manages Ollama lifecycle only and does not silently fall back.
6. `V095_PROVIDER_SWITCH_ACCEPTANCE.md:35-57,73-90` defines normal Web Chat switching and the negative CNX invariants.

### Selection lifetime

The repository proves the model-change RPC is pass-through and session-keyed, but does not prove the complete lifetime semantics of the live installed UI without a live trace. The strongest source-supported model is: session identity is the session key; selection is OpenClaw session/route metadata applied to the next execution; the provider is derived from the resolved provider/model route, not CNX state. Whether a selected route is persisted across Gateway restart, and whether a UI selection is sticky versus a one-turn override, is `UNKNOWN_NEEDS_LIVE_QUALIFICATION`.

Changing model does not mutate CNX identity in the tested boundary. Provider changes are covered as metadata-only in the historical acceptance/test design, but a real provider-switch UI sequence remains live qualification, not a passing fact.

## Session and persistence path

- Session identity owner: OpenClaw session/Gateway layer, keyed by the Web Chat session key. The CNX test uses `agent:main:dashboard:A` as the stable key and observes it unchanged across `sessions.patch` calls (`v090-model-selection-boundary.test.ts:31-34,47-51,62-69`).
- History/context owner: OpenClaw session store and Agent Core context assembly. The installed runtime contains `session-accessor-D7yi6P1i.js` imports in `agent-runner.runtime-DtdxZiBX.js`, including session load/update/reset functions.
- Assistant persistence owner: OpenClaw chat/agent/session runtime, not CNX TicketStore. The runtime exposes assistant stream events and session persistence; this archaeology did not mutate or inspect a live transcript.
- Next turn: same session key is looked up, stored history is assembled, and the current OpenClaw-resolved execution target is used. The exact persisted record shape and target-precedence order require live or deeper source qualification.
- CNX state: CNX Ticket/session/generation/policy and durable delivery/recovery stores remain separate. The model-change test explicitly proves no CNX SQLite mutation for model selection.

Historical acceptance evidence requires the same Ticket/session/generation/policy and canonical delivery invariants across a provider switch (`V095_PROVIDER_SWITCH_ACCEPTANCE.md:17-33,45-88`), but no live run was authorized here.

## Provider/model resolution and Ollama invocation

### Provider/model resolution

The installed OpenClaw runtime contains `model-selection-shared-iHJcI8fT.js`, `model-selection-normalize-Y5vjde6P.js`, `model-fallback-BPQMpbqN.js`, and provider/model resolution calls in `agent-runner.runtime-DtdxZiBX.js`. The Gateway runtime also projects resolved provider/model fields for sessions in `server-methods-NpEcZnvp.js`. This is direct artifact evidence of an OpenClaw-owned resolution path; the exact internal precedence among turn override, session selection, agent default, and system default is not fully recoverable from the generated bundle without a dedicated source-map/source qualification.

Model reference format is provider-scoped (`provider/model`), demonstrated by `ollama/qwen3.8:27b` in `v090-model-selection-boundary.test.ts:31` and `openai/gpt-5.6-luna` in CNX tests/config. Provider is therefore explicit in the resolved route when the model reference contains it; CNX does not infer or own it.

### Ollama adapter/invocation

Installed artifact `dist/extensions/ollama/index.js` imports the Ollama provider/discovery/base URL and stream modules (`provider-base-url-e9GVAsqB.js`, `stream-DwcvMYU5.js`, `discovery-shared-XxlmIfaG.js`). The artifact defines the Ollama provider ID, model discovery, and configured Ollama stream construction. Its source-visible runtime boundaries include:

- configured/local base URL resolution through `resolveOllamaApiBase`/`resolveOllamaRuntimeBaseUrl`;
- provider/model discovery through `resolveOllamaDiscoveryResult` and `fetchOllamaModels`;
- stream construction through `createConfiguredOllamaStreamFn` and `createConfiguredOllamaCompatStreamWrapper`;
- provider-native HTTP request/response handling and error normalization behind the imported provider HTTP helpers.

The installed extension also contains a separate node-inference command whose non-streaming request body visibly includes `model`, `messages`, `stream:false`, `think:false`, and `options.num_predict` (`extensions/ollama/index.js:72-77,156-165,200-223`). That node-inference command is not claimed to be the normal Web Chat Agent Core path. The normal chat stream adapter is identified by the imported `stream-DwcvMYU5.js` surface; exact request body/callback names for that path require a bounded installed-artifact source probe or authorized runtime trace.

### Streaming/result handling

OpenClaw's runtime emits separate normalized `lifecycle`, `assistant`, `thinking`, and `tool` streams in `agent-runner.runtime-DtdxZiBX.js` (visible stream readers around the installed artifact's assistant/tool event handling). The Web Chat bundle consumes Gateway chat events and renders assistant/tool history. CNX observes model-call lifecycle separately: `v091-direct-model-call-lease.ts:330-390` registers `model_call_started`, `model_call_ended`, and `agent_end`, recording non-secret provider/model/run/call metadata and using the Host as recovery authority.

This proves the intended event intersection, not a fresh live stream trace. Live stream ordering, cancellation propagation, and final assistant persistence are `REQUIRES_LIVE_AUTHORIZATION` for this task.

## CogentNexus intersection map

| Boundary | Owner before/after | CNX behavior | Provider/model effect |
|---|---|---|---|
| Web Chat selector / `sessions.patch` | OpenClaw before CNX | Safety proxy passes the Gateway request through | None; no Ticket mutation (`v090-model-selection-boundary.test.ts`) |
| Session key/history | OpenClaw session layer | CNX uses owner session key for Ticket correlation | Must remain provider-neutral |
| Agent admission | CNX before Agent Core/provider execution | `before_agent_run` is intended Ticket-first admission/policy boundary | Current live composed registry may omit it; this is the continuity blocker carried from CNX-375/376/405 evidence |
| Model-call lifecycle | OpenClaw emits; CNX observes | `model_call_started`/`ended` lease persistence (`v091-direct-model-call-lease.ts:343-375`) | Records provider/model but does not route |
| Agent completion/delivery | OpenClaw Agent Core then CNX delivery/recovery fences | `agent_end`, durable assistant delivery, recovery fencing | Provider failure must not create replacement CNX identity |
| Provider lifecycle/auth/routing | OpenClaw | CNX must not read/copy Cloud credentials or select Cloud routes (`docs/PROVIDERS.md`) | No CNX provider router |

The v0.9.5 entry explicitly installs the legacy chain and the inference bridge only after Host authority is accepted (`v091-release-entry.ts:142-205`). It also exports `hooks.allowConversationAccess: true` (`:154-160,207-210`) because the OpenClaw 2026.7.1-2 host gates conversation hooks on the definition's hook policy; the CNX-374 test documents the gate and expects `before_agent_run` registration (`cnx374-registry-wiring.test.ts:8-32,34-55`). This is the smallest known CNX-side intersection relevant to continuity, but production acceptance of the composed live hook remains separate evidence.

## State ownership table

| State | Owner | Lifetime / switching expectation | Evidence |
|---|---|---|---|
| Web Chat visible selection | OpenClaw control UI | UI/session route state; live lifetime unresolved | installed `chat-page` bundle |
| Session key / conversation identity | OpenClaw Gateway/session layer | Stable across model/provider changes | CNX model boundary test |
| Conversation history/transcript | OpenClaw session store | Read by next turn; provider-neutral in design; live persistence not requalified here | installed session runtime + goal docs |
| Resolved provider/model | OpenClaw model selection/router | Per execution from current route/selection | model-selection artifacts + `sessions.patch` test |
| Ollama endpoint/config | OpenClaw Ollama extension/config | Provider-owned; CNX managed lifecycle is separate | installed Ollama extension; `PROVIDERS.md` |
| CNX Ticket/generation/policy | CogentNexus | Must survive switching unchanged | provider-switch matrix + acceptance doc |
| CNX model-call lease | CogentNexus observation/recovery store | Per actual call; provider/model recorded as metadata | `v091-direct-model-call-lease.ts` |
| Assistant delivery/recovery fence | CogentNexus | Durable, session/generation fenced | CNX delivery/recovery modules and acceptance docs |

## Provider/model ownership table

| Concern | OpenClaw | CogentNexus |
|---|---|---|
| Provider listing/discovery | Yes | No; diagnostic/read-only at most |
| Model listing/resolution | Yes | No |
| Authentication/credentials | Yes | Must not inspect Cloud secrets |
| Route selection and adapter dispatch | Yes | No competing router |
| Ollama lifecycle | CNX managed path may control local Ollama lifecycle | Yes for managed Ollama only |
| Session continuity/Ticket/policy | No | Yes |
| Durable execution/delivery/recovery | Shared execution events, CNX fences | Yes for CNX safeguards |
| Provider-independent capability policy | Agent/OpenClaw capability plus CNX safeguards | Yes only for CNX continuity/safety; providerMode is not a kill-switch |

## Gap matrix against Product Goal

| Goal behavior | Classification | Evidence / remaining gap |
|---|---|---|
| Provider listing | `ALREADY_NATIVE` for OpenClaw route machinery; UI live qualification pending | OpenClaw catalog/installed UI artifacts; no live UI assertion |
| Model listing | `ALREADY_NATIVE` for Ollama discovery/configured models; UI qualification pending | Ollama extension discovery artifacts |
| Model selection | `ALREADY_NATIVE_BUT_CNX_INTERFERES` only at continuity boundary | `sessions.patch` pass-through test; live `before_agent_run` gap |
| Provider selection | `PARTIALLY_PRESENT` | Acceptance design and OpenClaw ownership are present; real Web Chat switch not run here |
| Session-sticky selection | `UNKNOWN_NEEDS_LIVE_QUALIFICATION` | Session-keyed patch is proven; restart/stickiness lifetime is not |
| Per-turn override | `UNKNOWN_NEEDS_LIVE_QUALIFICATION` | Runtime has model selection/fallback machinery; exact UI/API semantics not proven |
| Same-session model switch | `ALREADY_NATIVE_BUT_CNX_INTERFERES` | CNX boundary proves no session/Ticket mutation; end-to-end assistant next turn not live-qualified |
| Same-session provider switch | `PARTIALLY_PRESENT` | Historical design/matrix; live route plus continuity pending |
| Ollama real chat | `ALREADY_NATIVE` historically / `UNKNOWN_NEEDS_LIVE_QUALIFICATION` fresh | Existing known-good baseline and adapter; no new request allowed |
| OpenAI real chat | `ALREADY_NATIVE_BUT_CNX_INTERFERES` | CNX-357/367 historical real response; CNX-375/376 continuity bypass |
| Cross-provider context continuity | `MISSING` as an accepted live proof | Product acceptance still requires Ollama -> OpenAI -> Ollama same session |
| Tools across provider switch | `UNKNOWN_NEEDS_LIVE_QUALIFICATION` | Capability differences are recognized; no live cross-provider run |
| Streaming | `ALREADY_NATIVE` in OpenClaw path; CNX continuity qualification pending | runtime stream surfaces and Ollama adapter imports |
| Cancellation | `UNKNOWN_NEEDS_LIVE_QUALIFICATION` | no task-authorized live trigger |
| Failure recovery | `PARTIALLY_PRESENT` | CNX lease/recovery fences exist; cross-provider failure sequence not accepted |
| Restart persistence | `UNKNOWN_NEEDS_LIVE_QUALIFICATION` | no restart allowed and selection lifetime unresolved |

## What is already native vs what CNX interferes with

### Already native / should be reused

- OpenClaw Web Chat, Gateway chat RPC, session keys, session history, Agent Core, provider/model resolution, provider authentication/configuration, adapter dispatch, stream normalization, and assistant/tool event delivery.
- Ollama provider discovery and configured stream adapter.
- Model change via `sessions.patch` without session recreation or CNX lifecycle mutation.
- OpenClaw-owned Cloud pass-through design; CNX must not become a second route owner.

### Current CNX interference / missing continuity

- The live composed hook registry may not contain `before_agent_run`; source/test wiring exists, but CNX-375/376 evidence says the Dashboard/OpenAI execution can bypass Ticket-first admission when this hook is absent.
- Therefore a successful provider response is not yet proof of CNX continuity. The first broken edge is CNX admission/observation registration, not Ollama routing.
- The repository's provider-switch tests are mostly boundary/metadata simulations, not a real Web Chat vertical run. They are valid ownership/negative-invariant evidence, not live acceptance.

## Direct evidence vs inference

**Direct source/artifact evidence:** paths and symbols listed above; installed OpenClaw package/version; Ollama extension imports and discovery/stream surfaces; repository `sessions.patch` pass-through and byte-identity tests; provider ownership docs; CNX hook-policy declaration and model-call observation registrations.

**Historical acceptance evidence:** `V095_PROVIDER_SWITCH_ACCEPTANCE.md`, provider-switch matrix, and prior CNX-357/367/375/376 evidence carried by CNX-406 task/review. These establish intended behavior and historical observations, not a new run.

**Inference:** the sequence diagram's exact internal call order from chat UI through Agent Core is the normal OpenClaw architecture implied by the installed module graph and event surfaces; provider selection is likely applied to the next turn because `sessions.patch` is session-keyed, but sticky/restart semantics are not claimed as proven.

**Unknown:** live selected provider/model payload, exact current Web Chat control interaction, actual Ollama endpoint/model for a fresh run, live hook registry membership, exact assistant transcript persistence record, next-turn context proof, cancellation, cross-provider tool behavior, and restart persistence.

## Smallest next RED test

Add one repository-level integration RED test at the existing `sessions.patch`/Agent Core boundary, without a real provider request:

1. Create one synthetic Web Chat session key `S` with a minimal session/history fixture and a CNX controller/Ticket fixture.
2. Execute turn 1 with resolved target `ollama/model-a`.
3. Apply the same OpenClaw-owned session model-selection operation to `ollama/model-b` (or a distinct provider target in a second assertion).
4. Execute turn 2 through the normal Agent Core invocation seam with a fake provider adapter/transport.
5. Assert: both turns use the same session key and history; the resolved target changes only for turn 2; CNX Ticket ID, generation, policy fingerprint, and admission count remain stable; no CNX provider-selection action occurs.
6. Add the cross-provider variant only after the same-provider model-switch assertion is RED/GREEN.

The test must fail today specifically when `before_agent_run` is absent from the composed registry: the provider call may be reached, but CNX admission/Ticket continuity evidence is missing. It should not assert or implement a new provider router. The smallest repair task after RED should restore/qualify the existing CNX conversation-hook registration boundary, then run the normal OpenClaw route with an explicitly authorized live qualification.

## Recommended next bounded task

A narrowly scoped implementation/qualification task should: (a) prove the exact live composed hook registry contains `before_agent_run` for the ordinary Web Chat path; (b) add the RED test above at the same boundary; (c) make the minimal CNX registration/projection repair only if the fresh evidence confirms that boundary; and (d) defer the canonical `Ollama -> OpenAI -> Ollama` semantic acceptance to a separate explicitly authorized live task. Do not add a CNX provider router.

## Live qualification required

`REQUIRES_LIVE_AUTHORIZATION` for: fresh Ollama semantic traffic; fresh OpenAI traffic; changing production/UI provider/model state; proving actual stream/persistence/next-turn behavior; proving cross-provider context/tool continuity; restart persistence; and accepting the complete V095 provider-switch sequence.

## Closeout intent

This report reaches the preferred CNX-406 classification: `OLLAMA_VERTICAL_SLICE_MAPPED_READY_FOR_RED_TEST`. ACTIVE/STATUS are set to `WAITING_FOR_CHATGPT_REVIEW`; no CNX-407 was created or started.
