# CNX-345 — OpenAI Dashboard Admission Provenance Report

## Verdict

`PASS — SOURCE-BOUNDARY IDENTIFIED; CNX-344 NOT REPLAYED`

This report identifies the deterministic admission boundary and the evidence-supported first divergence without claiming that CNX-344 was repaired. CNX-345 is not self-accepted; it stops for independent ChatGPT review.

## Authority and exact source

- Task: `CNX-345`
- Branch: `cnx-345-openai-admission-provenance`
- Exact source commit investigated: `70ed0578fa7d4d5cac2c5f32b9380e4aa2923e61`
- Parent source/report commit: `eff0806e9493437ce74cd9123989396a6aefb609`
- Source paths:
  - `plugins/cogentnexus-openclaw/src/index.ts`
  - `plugins/cogentnexus-openclaw/src/ticket-store.ts`
  - `plugins/cogentnexus-openclaw/src/cloud-passthrough.ts`
- Historical runtime anchor: session `agent:main:dashboard:0874c9ea-7020-428f-ad66-cb5edbc18a53`
- Historical semantic request (not replayed): `CNX-344-OPENAI-TICKET-ROUTING: Reply exactly with DONE.`

## Dashboard/WebChat to provider boundary

The Dashboard submits a normal OpenClaw agent turn for the resolved session. The CogentNexus plugin observes that turn at `before_agent_run` (`index.ts:730`). The hook records the run/session context, then applies the following gates in order:

1. Internal delivery marker and post-compaction continuation handling (`index.ts:734-755`).
2. `durableAdmissionEligible({sessionKey: ctx.sessionKey, senderIsOwner: event.senderIsOwner})` (`index.ts:761`).
3. `classifyDurableRequest(...)`, producing `decision.lane` (`index.ts:762`).
4. If `providerMode === "passthrough"` and `decision.lane === "durable"`, return `block` before Ticket acceptance (`index.ts:763-770`).
5. If `ticketFirst === true` and `ticketIntakeEligible(event.prompt)`, call `TicketStore.accept(...)` (`index.ts:774-786`).
6. Route the accepted Ticket using `decision.lane === "durable"` (`index.ts:787`).
7. For a non-durable lane, return `pass` (`index.ts:788`). For a durable lane, block after committing/admitting or start the workflow (`index.ts:789-805`).

A `pass` from this hook does not dispatch the provider itself. It returns control to the host OpenClaw agent-run pipeline. The host then continues its native model/provider selection and dispatch. In passthrough mode the plugin explicitly documents that provider/auth/lifecycle/recovery ownership remains with OpenClaw (`index.ts:539`; `cloud-passthrough.ts:25-39`). Therefore native OpenClaw can select the configured `openai/gpt-5.6-luna` route and obtain a response after the CogentNexus hook has passed, without a CogentNexus Ticket being the owner of that request.

## Predicate evidence

### `durableAdmissionEligible`

`index.ts:310-318` returns false when the session key is absent or contains `:subagent:`. Otherwise it returns true when `senderIsOwner !== false`. When the event reports `senderIsOwner=false`, it returns true only for the canonical Dashboard shape:

`/^agent:[^:]+:dashboard:[^:]+$/u`

The CNX-344 historical session key matches this canonical Dashboard shape. Thus, on the investigated source, a correctly delivered event with that session key should not be rejected solely because WebChat reports `senderIsOwner=false`.

### `ticketIntakeEligible`

`ticket-store.ts:608-610` rejects only internal Context/Delivery/Continuation markers, workflow-result/resume markers, or the interrupted-run text. The CNX-344 semantic request contains none of these exclusions. Therefore, if the hook ran with `ticketFirst=true` and reached this predicate, the prompt was intake-eligible.

### `ticketFirst`, `decision.lane`, and the first divergence

The historical runtime configuration in the CNX-344 report recorded `ticketFirst=true`, `preInferenceAdmission=true`, `enforcedMode=true`, and `providerMode=passthrough`.

The source ordering makes the decisive boundary explicit:

- If the hook is reached and `durableAdmissionEligible` is false: immediate `pass` at `index.ts:761`; no classifier, no Ticket acceptance, and native OpenClaw continues.
- If eligible but `providerMode=passthrough` and `decision.lane=durable`: `block` at `index.ts:763-770`; native provider dispatch should not continue for that turn.
- If eligible, not stopped by passthrough, and `ticketFirst=true`: normal CNX Ticket acceptance occurs at `index.ts:774-786`.
- If the lane is conversational: the accepted Ticket, if any, is routed non-durable and the hook returns `pass` at `index.ts:788`; this still leaves a durable Ticket row, unlike CNX-344's observed zero-row result.

Consequently, the first source boundary consistent with CNX-344's observed **absence of every Ticket/Run/Call/inference/delivery row while a provider response was reported** is the pre-admission `pass` path at `index.ts:761` (or an equivalent runtime condition where this hook was not the active hook). The source cannot prove from the historical read-back which of those two runtime possibilities occurred.

## CNX-344 historical runtime evidence

From the parent report at `eff0806e9493437ce74cd9123989396a6aefb609`:

- Dashboard session: `agent:main:dashboard:0874c9ea-7020-428f-ad66-cb5edbc18a53`.
- Visible selector: `GPT-5.6 Luna · Medium`.
- Internal configuration contained `openai/gpt-5.6-luna`.
- `ticketFirst=true` and `preInferenceAdmission=true` were observed.
- After the single UI send and a 60-second read-only observation window: no Ticket owned by the session, zero rows with prompt prefix `CNX-344-`, and no Ticket ID, Run ID, Call ID, inference-attempt ID, Result, or Delivery ID.
- Counts remained `tickets=23`, `ticket_events=864`, `cnx_inference_attempt=3`, `cnx_assistant_delivery=14`, `ticket_outbox=0`, and `cnx_direct_model_call=20`.

This is strong evidence that the historical request was not admitted by the observed CogentNexus Ticket path. It does not independently prove the OpenAI provider call because the CNX-344 report explicitly recorded that no OpenAI call row was observed; the reported Dashboard response and native dispatch are the historical premise under investigation, not a newly generated runtime fact.

## CNX-343 comparison and first divergence

CNX-343 used the Dashboard session `agent:main:dashboard:945504d3-42f1-497a-b635-9975561e4bd5` and the Ollama route `ollama / qwen3.8:27b`. Its report records one correlated lifecycle:

`accepted → routed → direct_model_call_started → inference_attempt_started → direct_model_call_ended → inference_attempt_ended → response_ready → direct_response_durable → delivery_confirmed → completed`

It also records a Ticket, Run, Call, inference-attempt ID, final `completed` status, native-dashboard delivery confirmation, and outbox `0`.

The first observable divergence is before `accepted`: CNX-343 has the Ticket admission event and all downstream ownership records; CNX-344 has none. On current source, the corresponding decision point is the `durableAdmissionEligible` early return at `index.ts:761`, or failure to execute this plugin hook in the active runtime. `ticketIntakeEligible` is not the differentiator for the literal CNX-344 prompt, and a mere conversational `decision.lane` would still have produced a Ticket row.

## Proven cause vs remaining uncertainty

### Proven

1. Current source has a pre-Ticket early-return boundary: `before_agent_run` returns `pass` when `durableAdmissionEligible` is false (`index.ts:761`).
2. Current source permits native OpenClaw continuation after that `pass`; passthrough leaves provider/auth/lifecycle/recovery ownership with OpenClaw (`index.ts:539`, `cloud-passthrough.ts:25-39`).
3. The CNX-344 historical database read-back proves no CogentNexus Ticket lifecycle was created for that request.
4. The literal request is intake-eligible under `ticketIntakeEligible` (`ticket-store.ts:608-610`).
5. The historical result is not explained by `decision.lane` alone: if the hook reached Ticket intake with `ticketFirst=true`, `accept()` would create a Ticket even for a non-durable lane.

### Remaining uncertainty

1. No live replay is permitted, so the exact historical values of `ctx.sessionKey`, `event.senderIsOwner`, `config` as loaded by the running process, and the actual hook registration/priority cannot be reconstructed from the CNX-344 report alone.
2. The historical report did not observe an OpenAI `cnx_direct_model_call` row; therefore provider call identity and provider response are not independently durable-proven by CNX-344 evidence.
3. The exact active installed artifact/runtime may differ from the source commit inspected here. This report therefore classifies the first divergence as `pre-admission pass / hook-runtime applicability`, not as a proven single boolean value from the old event.

## Minimal remediation hypothesis — not implemented

Add read-only, correlated admission diagnostics at the `before_agent_run` boundary (session key shape, `senderIsOwner`, `durableAdmissionEligible`, `ticketFirst`, `ticketIntakeEligible`, `decision.lane`, `providerMode`, hook registration/priority, and final outcome) and bind the native provider dispatch observation to the same run/session identity. Then define an explicit policy for Dashboard passthrough turns: either fail closed before native dispatch when Ticket admission is required, or record a durable non-Ticket admission decision. Do not infer admission from the provider response alone.

No code, configuration, provider, controller, database, or runtime policy was changed by CNX-345.

## Fence and publication accounting

- CNX-344 was not rerun.
- The CNX-344 semantic request was not resent.
- No semantic request, UI interaction, retry, resend, recovery, fallback, or manual dispatch occurred.
- No install, reinstall, rebuild, restart, or v0.9.5 mutation occurred.
- No production code or test change occurred.
- No protected-state mutation occurred.
- No force-push or history rewrite occurred.
- Only this investigation report was added for CNX-345.

**Stop condition:** report published for independent ChatGPT review. CNX-345 is not self-accepted.
