# Transient Model-Call Stall Recovery

CogentNexus-OpenClaw treats a transient model-call stall as a continuity problem, not as automatic proof that a provider, model, or tool is permanently defective.

A run can start normally, stop making user-visible/model-stream progress, and later fail at a watchdog or interruption boundary while an equivalent later run succeeds without changing the provider configuration. Ticket-first durability matters because the accepted user intent can survive that failed inference attempt. Recovery is then bounded by durable evidence:

- if inference is confirmed interrupted and no durable result or protected external side-effect receipt exists, recovery may resume/retry the same committed Ticket within policy;
- if response content is already durable, recovery retries delivery only and must not regenerate completed work;
- if an external side effect may already have happened, retry requires idempotency, receipt, checkpoint, or read-after-write evidence;
- elapsed silence alone is never sufficient authority to restart a healthy provider or launch duplicate inference.

This file also preserves the historical v0.9.2 live LM Studio evidence that motivated the event-driven recovery model. v0.9.3 currently manages Ollama only; the LM Studio observations below remain technical history rather than a current provider-management promise.

## Historical live LM Studio evidence

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

After applying the historical LM Studio llama.cpp schema compatibility profile:

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

## Historical provider event adapter

LM Studio exposed prompt-prefill progress through a blocking runtime stream:

```text
lms log stream --source runtime
```

The v0.9.2 provider event adapter persisted observations such as:

```text
prompt_progress
provider_dead
provider_ready
stable_success
```

`prompt_progress` was deliberately suppression-only evidence. A parser mistake could delay destructive recovery but could never authorize a restart or repeated inference.

If the runtime stream ended, the adapter probed LM Studio. Only when the provider was actually unreachable did it publish `provider_dead` and wake the Host immediately. Periodic supervisor reconciliation remained a fallback for events that the external provider could not expose.

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

The deadline is not extended and does not become permission to recover. It is only the point at which CogentNexus-OpenClaw records that the call is silent/unknown and waits for stronger evidence.

### `provider_dead` / `provider_unreachable`

The selected provider process/endpoint is unavailable while MANAGED expects it to be running. Explicit failure evidence opens a durable provider incident and may authorize bounded recovery immediately.

When such an event intersects an active Direct model call, the durable model-call lease can be made claimable at the failure-event timestamp so the accepted claim/quiesce/result-fence/recovery primitives can proceed without waiting for elapsed time alone.

## Incident-based circuit breaker

Automatic recovery is bounded per failure incident, not merely by a rolling time window. An incident opens from failure evidence and closes only when stronger success or explicit/manual transition evidence establishes a new stable generation.

Historical v0.9.2 limits were provider-specific; v0.9.3 current operator/provider policy is Ollama-only and its accepted behavior is defined by the current runtime code and tests rather than the historical LM Studio table.

## OpenClaw timeout boundary

Timeout/watchdog values are request/runtime safety envelopes, not recovery authority. CogentNexus recovery decisions remain evidence-driven. A long timeout may prevent premature interruption, but it does not prove that a silent call is healthy; conversely, crossing a timer does not prove that a healthy provider is dead.

Historical LM Studio testing used widened provider/agent request envelopes to prove this distinction. Those exact LM Studio values are retained only in historical reports and should not be interpreted as current v0.9.3 operator configuration.

## Durable-result boundary

Once explicit failure evidence has made a call recovery-eligible, the accepted ordering remains:

1. Host claims the model-call lease;
2. Gateway/provider runtime is quiesced where required;
3. delivery/result fences are reconciled while inference cannot race them;
4. exactly one durable Direct-recovery authorization is written;
5. runtime restarts/converges as required;
6. the recovery worker consumes that authorization.

The decisive rule is unchanged: **authority to enter recovery comes from durable/observable evidence, not elapsed time alone.**

## Durable result exists

If exact response text already exists durably, inference must not run again. Transport/delivery owns retry.

## Response may have reached the user but exact durable payload is missing

The system fails closed rather than regenerating text. Ambiguous UI visibility is not permission to infer again.

## External side effect may already have happened

A retry is permitted only when the external action has an idempotency/receipt/read-after-write contract proving repetition is safe. Provider recovery alone is never sufficient evidence.

## Process exit is not success proof

Live diagnostics produced cases where an OpenClaw CLI process returned exit code 0 while the inner agent result was an error/timeout. CogentNexus-OpenClaw therefore inspects durable/inner completion evidence instead of treating process exit or a top-level wrapper status as success proof.
