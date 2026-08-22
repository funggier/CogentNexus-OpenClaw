# Evidence-aware, event-driven local model-call recovery

CogentNexus v0.9.2 does not treat elapsed time as proof that a model or provider is dead. Recovery authority comes from durable events and explicit failure evidence. Periodic reconciliation and long watchdogs remain safety mechanisms only.

## What live LM Studio testing proved

Native Windows testing with OpenClaw `2026.7.1-2`, LM Studio, Qwen3.5:9B and real OpenClaw tool schemas established this sequence:

1. OpenClaw opened the OpenAI-compatible `/v1/chat/completions` request successfully.
2. LM Studio returned HTTP 200/SSE and kept its backend alive.
3. llama.cpp runtime logs showed prompt processing progressing through roughly 17%, 35%, 52%, 70% and 87%.
4. No generated token was available yet, so the OpenAI-compatible stream exposed no prompt-progress event to OpenClaw.
5. OpenClaw's default stuck-session boundary aborted the client connection at about 360 seconds.
6. LM Studio observed the client disconnect and only then cancelled the still-running inference.
7. Repeating the same cold test with a wider watchdog allowed the request to finish successfully at roughly 469 seconds wall time.

Therefore:

> `active_model_call_without_progress` is not sufficient evidence that the provider is hung.

Silence can mean valid cold prompt processing whose progress is hidden by the OpenAI-compatible stream.

## Tool-surface evidence

After applying the LM Studio llama.cpp schema compatibility profile:

```json
{
  "unsupportedToolSchemaKeywords": ["pattern", "maxLength"]
}
```

all of these model-facing schema surfaces completed successfully with a sufficient request envelope:

- minimal;
- `cron`;
- `image_generate`;
- `cron + image_generate`;
- full OpenClaw `coding` profile (26 tools in the observed run).

The full coding surface also exposed the independent `agents.defaults.timeoutSeconds` boundary: a valid request can outlive the default agent timeout even after provider/stuck-watchdog tuning.

## Event hierarchy

Recovery decisions are ordered by evidence strength:

```text
model/provider success event
    -> close current incident

provider prompt progress
    -> proof of life
    -> destructive recovery forbidden

provider process/endpoint failure event
    -> open provider incident
    -> bounded recovery authority

HTTP 4xx / schema / grammar rejection
    -> provider_protocol_error
    -> non-retryable, no provider restart

elapsed model-call deadline with healthy provider + healthy Gateway
    -> observation checkpoint only
    -> wait for event evidence
    -> no restart, no re-inference
```

## Provider event adapter

LM Studio exposes prompt-prefill progress through a blocking runtime stream:

```text
lms log stream --source runtime
```

v0.9.2 runs a provider event adapter while LM Studio is the selected MANAGED provider. It persists observations such as:

```text
prompt_progress
provider_dead
provider_ready
stable_success
```

`prompt_progress` is deliberately **suppression-only evidence**. A parser mistake can delay destructive recovery but can never authorize a restart or repeated inference.

If the runtime stream ends, the adapter probes LM Studio. Only when the provider is actually unreachable does it publish `provider_dead` and wake the Host immediately. Periodic supervisor reconciliation remains a fallback for events that the external provider cannot expose.

## Failure classes

### `provider_protocol_error`

Examples:

- deterministic HTTP 4xx before inference starts;
- JSON-schema conversion failure;
- llama.cpp grammar initialization failure.

Policy:

```text
inference_started = false
retryable = false
provider_restart = false
```

Restarting a healthy provider does not repair a deterministic request-shape incompatibility.

### `active_model_processing`

Evidence:

- provider endpoint is healthy;
- Gateway is healthy;
- Direct model call is still active;
- provider runtime emitted prompt-progress evidence after that call started.

Policy:

```text
recoveryEligible = false
providerRestart = false
```

There is no duration threshold. Continued progress remains proof of life regardless of how long prompt processing takes.

### `active_model_processing_unknown`

Evidence:

- provider endpoint is healthy;
- Gateway is healthy;
- Direct model call remains active;
- no explicit provider/model failure event exists;
- the old durable lease checkpoint has passed, but no observable prompt progress is available.

Policy:

```text
recoveryEligible = false
providerRestart = false
wait_for_event_evidence = true
```

The deadline is **not extended** and does not become permission to recover. It is only the point at which CogentNexus records that the call is silent/unknown and waits for stronger evidence.

### `provider_dead` / `provider_unreachable`

The selected provider process/endpoint is unavailable while MANAGED expects it to be running. This explicit failure evidence opens a durable provider incident and may authorize bounded recovery immediately.

When such an event intersects an active Direct model call, v0.9.2 marks the existing call lease claimable at the failure-event timestamp. This reuses the accepted v0.9.1 claim/quiesce/result-fence/recovery primitives without waiting for a timer to expire.

## Incident-based circuit breaker

Automatic recovery is bounded per **failure incident**, not per minute/hour.

Current policy:

| Provider | Maximum automatic recoveries per incident |
| --- | ---: |
| Ollama | 3 |
| LM Studio | 2 |

An incident opens only from failure evidence. Attempts remain part of that incident no matter how much wall-clock time passes. The circuit cannot reopen merely because a cooldown or rolling window expired; those concepts are not part of v0.9.2 recovery authority.

The incident closes only when stronger evidence arrives, such as:

- a durable successful `model_call_ended` event (`outcome=ok` or equivalent stable-success outcome); or
- a verified explicit/manual provider transition (`start`, `restart`, provider switch) that re-establishes provider + Gateway + route successfully.

A later failure opens a new incident generation with a fresh bounded attempt budget.

## OpenClaw timeout boundary

v0.9.2 does **not** own OpenClaw's native stuck-session watchdog. The accepted v0.9.1 Host control already moves `diagnostics.stuckSessionAbortMs` to a ~24-hour MANAGED compatibility fence and restores the operator's original value on PASSTHROUGH.

For LM Studio, v0.9.2 manages only the request envelope proven necessary by live testing:

```text
models.providers.lmstudio_local.timeoutSeconds = 1100 s
agents.defaults.timeoutSeconds                 = 1200 s
```

These values prevent premature request/agent cancellation; they are **not recovery policy timers**. The v0.9.1 ~24-hour native watchdog remains a final external safety fuse, well outside normal CogentNexus event-driven recovery.

`disable`, `reset`, and `uninstall` restore the v0.9.2-owned provider/agent fields, while v0.9.1 independently restores its watchdog snapshot.

## Durable-result boundary

The accepted v0.9.1 Direct recovery ordering remains authoritative once explicit failure evidence has made a call recovery-eligible:

1. Host claims the model-call lease;
2. Gateway/provider runtime is quiesced;
3. delivery/result fences are reconciled while inference is impossible;
4. exactly one durable Direct-recovery authorization is written;
5. runtime restarts;
6. the hidden recovery worker consumes that authorization.

v0.9.2 changes only **when authority to enter that sequence exists**. It does not weaken the sequence itself.

## Durable result exists

If exact response text already exists durably, inference must **not** run again. Transport/delivery owns retry.

## Response may have reached the user but exact durable payload is missing

The accepted v0.9.1 fence fails closed rather than regenerating text. Ambiguous UI visibility is not permission to infer again.

## External side effect may already have happened

A retry is permitted only when the external action has an idempotency/receipt/read-after-write contract proving repetition is safe. Provider recovery alone is never sufficient evidence.

## Process exit is not success proof

Live diagnostics produced cases where the OpenClaw CLI process returned exit code 0 while the inner agent result was an error/timeout. CogentNexus therefore inspects durable/inner completion evidence instead of treating process exit or a top-level wrapper status as success proof.
