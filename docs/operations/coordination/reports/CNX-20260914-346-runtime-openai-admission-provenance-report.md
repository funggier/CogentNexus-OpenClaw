# CNX-346 — Runtime OpenAI Dashboard Admission Provenance Report

## Verdict

`PASS — FIRST DIVERGENCE NARROWED TO ACTIVE-HOOK EXECUTION/REGISTRATION; NOT DURABLE-ADMISSION PREDICATE`

The current runtime contains the Dashboard-aware Ticket-first admission implementation and is configured to enable it. The retained CNX-344 runtime trace records `senderIsOwner=true`, a canonical Dashboard session key, `sessionId`, `runId`, prompt metadata, and a successful OpenAI `gpt-5.6-luna` completion. Under the inspected source and configuration, those facts would not produce the pre-admission `pass` path. They would reach Ticket intake and create a Ticket before native provider inference. The narrowest evidence-backed divergence is therefore that the CogentNexus `before_agent_run` handler was not executed for CNX-344 (not registered/active in the effective runtime), or that the effective runtime used a different handler/module than the inspected admission implementation. A historical boolean result from inside the hook is not present, so this report does not claim a direct runtime registration read-back as proven.

CNX-344 was not rerun and its request was not resent.

## Authority and fingerprints

- Repository: `funggier/CogentNexus-OpenClaw`
- Task branch: `cnx-346-runtime-openai-admission-provenance`
- Exact source HEAD inspected: `00a94163784505da8efe540c49ed052504812515`
- Active task state at that HEAD: `READY_FOR_HERMES`
- Runtime host: `C:\Users\CDQ-P`
- OpenClaw gateway process observed read-only: `node.exe ...\\openclaw\\dist\\index.js gateway --port 18789`, PID `17080`
- Installed plugin root: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw`
- Installed manifest version: `0.9.5`
- Installed package entry: `./dist/v091-release-entry.js`
- Installed `dist/index.js` size: `69,231` bytes
- Installed `dist/index.js` SHA-256: `d284291bef3d92cabd93b3fb9a4481436a00350e8fc04e7876e8da21f46e436d`
- Installed `dist/v091-release-entry.js` SHA-256: `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8`
- Installed package archive `openclaw-plugin-cogentnexus-openclaw-0.9.5.tgz` SHA-256: `74c9aebd4a4539ccc47f547537a29e293a1ddfa373ae864113687509a97d2bd9`
- Installed `package.json` SHA-256: `3c3738f51eb82fc3c90ce658c5cd8bde295a6593f44f619d59f3c93f808fedd9`
- Source `plugins/cogentnexus-openclaw/src/index.ts` SHA-256: `13dc321d6892e93e96c4133329a5e4e199896f3124e674199c4504c57a144736`
- Source `plugins/cogentnexus-openclaw/src/ticket-store.ts` SHA-256: `738489856f8bcede713655ee4c7e489795ea52971d9e7c1fba28486dcf9778a9`

The installed archive is a runtime artifact fingerprint, not a claim that it was produced from the CNX-346 source HEAD. No build or package mutation was performed.

## Runtime registration and handler evidence

### Configuration

Read-only `/c/Users/CDQ-P/.openclaw/openclaw.json` contains:

- `plugins.entries.cogentnexus-openclaw.enabled=true`
- `ticketFirst=true`
- `preInferenceAdmission=true`
- `enforcedMode=true`
- `providerMode="passthrough"`
- workspace `C:\\Users\\CDQ-P\\.openclaw\\workspace`

The installed `openclaw.plugin.json` has `activation.onStartup=true` and the package extension points to `dist/v091-release-entry.js`.

### Static registration

The installed artifact contains the admission symbols and registration:

- `dist/index.js` contains `before_agent_run`, `durableAdmissionEligible`, `ticketIntakeEligible`, Dashboard handling, and `ticketFirst`.
- `dist/index.js` registers `before_agent_run` only when `config.preInferenceAdmission !== false`.
- The handler registration is `{ priority: 2000, timeoutMs: 30_000 }`.
- `v091-release-entry.js` calls the legacy entry's `register(runtimeApi)` and explicitly documents that the legacy `before_agent_run` Ticket-first gate is installed through that path.
- The handler identity is the admission closure created in the `register(api)` function in `dist/index.js`; no separate higher-priority handler identity for this admission decision was found in the installed artifact.

The gateway process and enabled startup manifest prove that the candidate runtime is present and eligible to load. They do not, by themselves, prove that OpenClaw completed the registration call or invoked this handler for CNX-344. No mutation, restart, or diagnostic registration probe was attempted.

## Admission predicate and source semantics

Source and installed artifact agree on the relevant logic:

1. `durableAdmissionEligible({sessionKey, senderIsOwner})` returns false only when the session key is absent/contains `:subagent:`, or when `senderIsOwner=false` and the key is not canonical Dashboard form `^agent:[^:]+:dashboard:[^:]+$`.
2. The CNX-344 session key `agent:main:dashboard:0874c9ea-7020-428f-ad66-cb5edbc18a53` is canonical Dashboard form.
3. The retained CNX-344 trace records `senderIsOwner=true`, which is directly sufficient for `durableAdmissionEligible` to return true regardless of namespace fallback.
4. `ticketIntakeEligible` rejects internal delivery/continuation/workflow markers and interrupted-run text. The literal CNX-344 prompt is not one of those exclusions.
5. With `ticketFirst=true`, an eligible prompt calls `TicketStore.accept(...)` before inference, using `ctx.runId` and `ctx.sessionKey`.
6. A non-durable classifier lane still creates a Ticket before returning `pass`; therefore classifier lane alone cannot explain zero Ticket rows.
7. With `providerMode=passthrough`, a durable classifier lane returns `block` before native provider dispatch. It does not pass through to OpenAI.
8. Only the early `durableAdmissionEligible=false` return produces `pass` without Ticket acceptance among the relevant normal-user branches.

## CNX-344 historical event/context evidence

The retained files for session ID `819c2940-1983-42b5-97c7-b94bae2ea7df` were read without sending traffic:

- Session key: `agent:main:dashboard:0874c9ea-7020-428f-ad66-cb5edbc18a53`
- Session ID: `819c2940-1983-42b5-97c7-b94bae2ea7df`
- Run ID: `a95d243d-4e42-412a-8169-75dbad69d87f`
- Prompt: `CNX-344-OPENAI-TICKET-ROUTING: Reply exactly with DONE.`
- Source channel: `webchat`
- `senderIsOwner=true`
- Provider: `openai`
- Model ID: `gpt-5.6-luna`
- Model API: `openai-chatgpt-responses`
- Thread ID: `01a0a052-f686-70a2-847a-1209e0b56f7f`
- Turn ID: `01a0a053-0a67-7c90-a573-80dfb827fbcd`
- `imagesCount=0`
- Model completed successfully, `timedOut=false`, `aborted=false`, assistant text `DONE`
- Session ended with status `success`

The earlier CNX-344 report records no CNX-344 Ticket, Run, Call, inference-attempt, Result, or Delivery row, with global counts unchanged. That durable read-back remains the historical lifecycle evidence; it was not recreated or altered here.

## Hook-absent vs hook-active-plus-pass distinction

### Hook active plus `durableAdmissionEligible=false`

This is **not consistent with the retained CNX-344 trace**: the trace has a present canonical Dashboard session key and `senderIsOwner=true`, so the inspected predicate evaluates true. It would require the effective runtime to have received materially different context than the retained event, or to have loaded a different implementation.

### Hook not active/not registered, or different effective handler

This is the narrowest explanation consistent with all retained facts: OpenClaw natively completed the OpenAI turn, while the CogentNexus pre-admission handler did not own the boundary. Static artifacts prove that the intended handler exists and is configured, but no authoritative historical hook invocation/registration record was retained. Thus the exact subcase—registration call failure, hook list omission, stale/different loaded module, or an effective runtime path bypassing the plugin—remains unresolved.

## Native OpenClaw passthrough

The source's passthrough comments and branch semantics state that provider/auth/lifecycle/recovery ownership remains with OpenClaw. A CogentNexus `pass` returns control to the host agent-run pipeline; it does not dispatch OpenAI itself. Native OpenClaw can then use the session's provider/model selection and complete `openai / gpt-5.6-luna`. The CNX-344 trajectory is direct historical evidence of that native completion boundary.

## CNX-343 Ollama comparison

CNX-343's successful Ollama Dashboard path contains the expected `accepted` Ticket event followed by routed/direct-model-call/inference/result/delivery/completed records. CNX-344 diverges before `accepted`: no Ticket row or admission event exists, while native OpenAI trajectory records show provider completion. Because the CNX-344 prompt is intake-eligible and its event is owner-eligible, the first divergence is the effective `before_agent_run` execution/registration boundary, not `ticketIntakeEligible`, Ticket routing, provider selection, or delivery settlement.

## Proven / strongly supported / remaining uncertainty

### Proven

- Exact source HEAD and installed runtime artifact fingerprints above.
- Installed artifact contains Dashboard-aware `durableAdmissionEligible`, `ticketFirst`, `ticketIntakeEligible`, and `before_agent_run` logic.
- Configuration enables the plugin, `preInferenceAdmission`, and `ticketFirst` in passthrough mode.
- Static handler priority is `2000`; the installed entry delegates to the legacy registration path.
- CNX-344 retained context contains the exact sessionKey, sessionId, runId, prompt, `senderIsOwner=true`, OpenAI provider/model, and successful native completion.
- The retained CNX-344 report contains no durable CogentNexus Ticket lifecycle.
- Source semantics show that a hook `pass` returns to native OpenClaw provider dispatch.

### Strongly supported

- CNX-344 first diverged before Ticket acceptance at the effective hook execution/registration boundary.
- The cause was not `durableAdmissionEligible=false` under the retained event values.
- The OpenAI completion was native OpenClaw passthrough after CogentNexus did not own admission.

### Remaining uncertainty

- No retained runtime registry snapshot or per-invocation hook diagnostic proves whether OpenClaw registered the handler, whether registration threw/was skipped, or which exact module instance was loaded at CNX-344 time.
- The installed runtime artifact is version 0.9.5 and is not byte-proven identical to the source HEAD; the artifact fingerprint is recorded, but no rebuild or provenance mutation is allowed.
- No durable OpenAI provider-call row was present in CNX-344's CogentNexus database, so provider identity is proven by the OpenClaw trajectory, not by CogentNexus call ownership.
- Distinguishing “handler absent” from “different handler/module active” requires a read-only runtime registration snapshot or correlated admission diagnostic; it does not authorize replay.

## Minimal remediation target — NOT IMPLEMENTED

Add a read-only startup and admission-boundary diagnostic for the exact handler identity, registration priority, plugin artifact fingerprint, event fields, predicate result, `ticketFirst`, `ticketIntakeEligible`, classifier lane, and final outcome, all keyed by `sessionKey/sessionId/runId`. The smallest deterministic follow-up should first prove effective registration/invocation on a fresh non-semantic diagnostic path or existing runtime introspection surface; then repair only the registration/provenance mismatch if confirmed. Do not rerun CNX-344 and do not resend its request. No remediation was implemented by CNX-346.

## Explicit fence accounting

- Read-only source, configuration, installed-artifact, process, and historical-file inspection only.
- CNX-344 was not rerun.
- CNX-344 semantic request was not resent.
- No semantic request, replay, resend, retry, recovery, fallback, or manual dispatch occurred.
- No UI interaction occurred.
- No provider, model, config, controller, or database mutation occurred.
- No production code or test change occurred.
- No install, reinstall, rebuild, or restart occurred.
- No v0.9.5 mutation occurred.
- No force-push or history rewrite occurred.
- Only this coordination report is being published.

**Stop condition:** publish the report and stop for independent ChatGPT review. CNX-346 is not self-accepted.
