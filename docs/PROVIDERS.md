# Provider lifecycle — CogentNexus v0.9.2

CogentNexus v0.9.2 separates durable user intent/recovery authority from the concrete local inference runtime. The accepted v0.9.1 Ticket, Direct Recovery, durable-result and delivery fences remain authoritative. The v0.9.2 provider layer owns discovery, selected-provider lifecycle, the narrow OpenClaw route/request compatibility transaction, provider event evidence, and bounded per-incident recovery.

## Supported local providers

| Provider | Default endpoint | OpenClaw route prefix | Control adapter |
| --- | --- | --- | --- |
| Ollama | `http://127.0.0.1:11434` | `ollama/...` | `ollama` CLI |
| LM Studio | `http://127.0.0.1:1234` | `lmstudio_local/...` | `lms` CLI |

Both may be installed and running because their normal ports differ. CogentNexus has exactly one **selected provider** for MANAGED lifecycle/recovery responsibility.

## Selecting a provider

```powershell
.\cnx.cmd start --provider ollama
.\cnx.cmd start --provider lmstudio
```

A successful verified transition stores `selectedProvider` plus selection metadata. Later `start`/`restart` may omit `--provider` and reuse that verified selection. There is no silent provider fallback.

## Provider + OpenClaw route transaction

CogentNexus does **not** rewrite arbitrary OpenClaw configuration. While MANAGED, v0.9.2 owns only:

1. the default local model route for the selected provider;
2. LM Studio provider/agent request-timeout fields proven necessary by live tests;
3. LM Studio llama.cpp tool-schema compatibility keywords.

`diagnostics.stuckSessionAbortMs` is deliberately not owned by v0.9.2. The accepted v0.9.1 Host-control compatibility fence remains authoritative for that field.

Before lifecycle mutation, CogentNexus performs provider and route preflight. It then writes a durable `providerTransition` marker and a short-lived exact OpenClaw rollback copy. `selectedProvider` is committed only after:

1. target provider availability/startability succeeds;
2. route transaction validates;
3. target provider starts/verifies;
4. Gateway receives a process boundary when the active route/config requires it;
5. provider readiness still succeeds;
6. Gateway health passes;
7. active model route resolves to the target provider;
8. route transaction commits.

If Host transition or verification fails, the OpenClaw route rolls back while `providerTransition` remains durable so the next start resumes the intended target rather than guessing.

## Native/PASSTHROUGH boundary

`disable` is a runtime boundary, not just a config edit. It:

1. completes the accepted v0.9.1 PASSTHROUGH transition;
2. stops CogentNexus provider event adapters;
3. restores pre-CNX route/request-timeout/schema-compat fields;
4. forces Gateway restart (falling back to start if needed);
5. verifies the native Gateway is running/reachable.

`reset` and `uninstall` reuse this boundary and block destructive cleanup if native OpenClaw cannot be reloaded and verified.

## Route discovery

CogentNexus does not invent credentials or an unknown model. A route must be resolvable from one of:

- current OpenClaw default route;
- a previously verified CogentNexus route for that provider;
- an existing provider model catalog entry;
- `CNX_OLLAMA_MODEL` or `CNX_LMSTUDIO_MODEL`.

For LM Studio, an existing `models.providers.lmstudio_local` configuration is required.

## LM Studio compatibility profile

### llama.cpp tool schema

The verified profile is:

```json
{
  "unsupportedToolSchemaKeywords": ["pattern", "maxLength"]
}
```

It passed isolated `cron`, isolated `image_generate`, combined `cron + image_generate`, and the full OpenClaw `coding` tool surface.

### Request envelope

Live tests proved valid LM Studio cold prompt processing can remain silent to OpenClaw for several minutes. v0.9.2 therefore applies:

```text
models.providers.lmstudio_local.timeoutSeconds = 1100 s
agents.defaults.timeoutSeconds                 = 1200 s
```

These values prevent premature request/agent cancellation. They are not recovery-policy clocks. Separately, accepted v0.9.1 places OpenClaw's native stuck-session watchdog at a ~24-hour MANAGED compatibility fence and restores the operator's value on PASSTHROUGH.

## Provider events

For LM Studio, v0.9.2 starts a blocking runtime-event adapter using:

```text
lms log stream --source runtime
```

It can persist `prompt_progress` as proof of life. If that blocking stream ends, the adapter probes LM Studio; only a genuinely unreachable provider becomes `provider_dead`, which wakes the Host immediately.

The progress parser is intentionally one-way safe:

```text
prompt progress -> may suppress destructive recovery
prompt progress -> can never authorize restart/re-inference
```

Providers that cannot expose an equivalent progress stream still use the same event-driven decision policy; periodic health reconciliation remains a safety fallback.

## Event-driven recovery authority

Elapsed time alone never authorizes provider recovery in v0.9.2.

```text
provider/Gateway healthy + silent active call
    -> active_model_processing_unknown
    -> wait for stronger event evidence
    -> no restart
    -> no re-inference

LM Studio prompt_progress after call start
    -> active_model_processing
    -> proof of life
    -> no restart

provider_dead / provider_unreachable
    -> open durable provider incident
    -> bounded automatic recovery allowed

model_call_ended success
    -> stable_success
    -> close incident
```

When an explicit provider-failure event intersects an active Direct model call, v0.9.2 makes the existing lease claimable at the failure-event timestamp and then invokes the accepted v0.9.1 claim/quiesce/result-fence/recovery primitives. The event—not elapsed time—is the authority.

## Per-incident circuit breaker

Current policy:

| Provider | Maximum automatic recoveries per incident |
| --- | ---: |
| Ollama | 3 |
| LM Studio | 2 |

There is no cooldown and no rolling-hour reset. Time passage cannot reopen a circuit.

An incident closes only after stronger evidence such as:

- durable successful model completion; or
- explicit verified manual start/restart/provider transition.

A later failure opens a new incident generation and receives a fresh bounded attempt budget.

## No silent fallback

If a persisted provider is removed, unhealthy, uncontrollable, or missing a model route, `cnx start` fails closed. Select another provider explicitly.

## Fresh state and reset

On fresh state:

- exactly one installed supported provider -> it may be selected automatically after successful verification;
- both installed -> explicit provider required;
- neither installed -> MANAGED provider start refused.

`stop` preserves provider selection and MANAGED route. `disable` preserves durable provider preference but restores native OpenClaw configuration and stops CNX provider event handling.

`reset` uses fresh-install semantics. With both providers installed:

```powershell
.\cnx.cmd reset --provider ollama
# or
.\cnx.cmd reset --provider lmstudio
```

The explicit-`y`, PASSTHROUGH-first v0.9.1 safety boundary remains intact.

## LM Studio control

LM Studio MANAGED start/stop and runtime event streaming require its `lms` CLI. A GUI installation without `lms` remains detectable but is not controllable by CogentNexus.

If LM Studio API authentication is enabled, `LM_API_TOKEN` may be provided for readiness probes.

## Recovery Core boundary

The provider layer never decides whether an already committed result or possible side effect may be repeated. Accepted v0.9.1 fences remain authoritative:

- deterministic HTTP/schema/grammar protocol failure -> non-retryable, no restart;
- durable exact result exists -> delivery retry only;
- ambiguous visible response without durable payload -> fail closed;
- possible external side effect -> receipt/idempotency proof required;
- Host-authorized Direct recovery -> Gateway/provider quiescence and durable result fences remain mandatory.
