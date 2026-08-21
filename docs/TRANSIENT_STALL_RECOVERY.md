# Evidence-aware local model-call recovery

CogentNexus treats a silent model call as a recoverable failure candidate only when durable evidence proves that retrying inference cannot duplicate an already committed result or external side effect. v0.9.2 also distinguishes a **slow but healthy local inference** from a dead provider.

## What live LM Studio testing proved

Native Windows testing with OpenClaw `2026.7.1-2`, LM Studio, Qwen3.5:9B and real OpenClaw tool schemas established the following sequence.

1. OpenClaw successfully opened the OpenAI-compatible `/v1/chat/completions` request.
2. LM Studio returned HTTP 200/SSE and kept its backend alive.
3. llama.cpp runtime logs showed prompt processing progressing through roughly 17%, 35%, 52%, 70% and 87%.
4. No generated token was available yet, so the OpenAI-compatible stream exposed no visible prompt-progress event to OpenClaw.
5. OpenClaw's default stuck-session boundary aborted the client connection at about 360 seconds.
6. LM Studio observed the client disconnect and only then cancelled the still-running inference.
7. Repeating the same cold test with a wider watchdog allowed the request to finish successfully at roughly 469 seconds wall time.

Therefore:

> `active_model_call_without_progress` is not sufficient evidence that the provider is hung.

For a local backend, it can mean that the provider is alive and performing cold prompt prefill while the transport cannot expose that progress.

## Tool-surface evidence

After applying the LM Studio llama.cpp schema compatibility profile:

```json
{
  "unsupportedToolSchemaKeywords": ["pattern", "maxLength"]
}
```

all of these model-facing schema surfaces completed successfully when given a sufficient timeout envelope:

- minimal;
- `cron`;
- `image_generate`;
- `cron + image_generate`;
- full OpenClaw `coding` profile (26 tools in the observed run).

The full coding surface also demonstrated another timeout layer: widening the provider/stuck watchdog while leaving `agents.defaults.timeoutSeconds` near 600 seconds still caused a valid long request to be aborted. Increasing the agent/provider request envelope allowed the same full coding schema to complete successfully.

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

Repeating or restarting a healthy provider does not repair a deterministic request-shape incompatibility.

### `cold_model_long_running`

Evidence:

- selected provider endpoint is healthy;
- Gateway is healthy;
- a Direct model-call lease reached its normal durable deadline;
- no durable result exists;
- no recovery attempt has yet been consumed;
- the provider is LM Studio, whose OpenAI-compatible stream cannot expose prompt-prefill progress to the Host.

v0.9.2 response:

1. leave the Direct Ticket in the Direct lane (`workflow_eligible=0`);
2. leave the model-call state active;
3. do **not** consume a recovery attempt;
4. do **not** restart LM Studio;
5. extend the model-call deadline once by the configured long-running grace (currently 600 seconds);
6. write durable `host_direct_model_long_running_grace` evidence.

Only a later expiry, after this one-time grace, may enter the accepted Direct recovery path.

### `provider_dead`

Evidence is materially different: the selected provider endpoint/process is unavailable when it is expected to be running.

This is provider-lifecycle recovery territory, but automatic recovery is still bounded by a durable circuit breaker.

## Bounded provider recovery

Automatic provider restart/recovery must never become an infinite loop.

Current v0.9.2 policy:

| Provider | Maximum automatic recoveries / rolling hour | Minimum cooldown between attempts | Long-running grace |
| --- | ---: | ---: | ---: |
| Ollama | 3 | 300 s | 0 |
| LM Studio | 2 | 900 s | 600 s |

Every automatic recovery starts its cooldown immediately. The rolling-hour maximum is an independent gate. For LM Studio this means at least 15 minutes between automatic recovery attempts and never more than two attempts in a rolling hour.

The durable state is stored outside the provider process. When either gate blocks recovery, the Host reports `provider_recovery_circuit_open` and does not claim another Direct call for restart recovery.

A successful explicit/manual provider transition clears that provider's automatic-recovery budget because the operator has intentionally re-established and verified the route/runtime.

## Timeout and recovery authority

v0.9.2 does **not** take ownership of OpenClaw's native stuck-session watchdog. The accepted v0.9.1 Host control already owns that boundary while CogentNexus is MANAGED and moves `diagnostics.stuckSessionAbortMs` to a 24-hour compatibility fence. That keeps the native OpenClaw stuck-session abort outside the normal CogentNexus durable recovery horizon and restores the operator's original value on PASSTHROUGH/disable.

For LM Studio, v0.9.2 transactionally manages only the additional provider/agent request envelope proven necessary by live testing:

```text
models.providers.lmstudio_local.timeoutSeconds = 1100 s
agents.defaults.timeoutSeconds                 = 1200 s
```

The effective authority ordering is therefore:

```text
CogentNexus durable model-call deadline / evidence classifier
    -> one-time LM Studio long-running grace when eligible
    -> bounded CogentNexus recovery if later eligible

LM Studio provider request timeout = 1100 s
OpenClaw agent timeout             = 1200 s
OpenClaw native stuck watchdog     = v0.9.1 MANAGED fence (~24 h)
```

The provider request must expire before the enclosing agent timeout, while the native stuck watchdog remains far outside both. `disable`, `reset`, and `uninstall` restore the v0.9.2-owned provider/agent fields; the accepted v0.9.1 Host control independently restores its watchdog snapshot.

## Durable-result boundary

The accepted v0.9.1 Direct recovery ordering remains authoritative after an inference is truly eligible for recovery:

1. Host claims the expired model-call lease;
2. Gateway/provider runtime is quiesced;
3. delivery/result fences are reconciled while inference is impossible;
4. exactly one durable Direct-recovery authorization is written;
5. runtime restarts;
6. the hidden recovery worker consumes that authorization.

v0.9.2 does not weaken any of those fences. The new long-running classification occurs **before** this destructive recovery sequence and exists specifically to avoid quiescing/restarting a provider that still has credible evidence of valid work.

## Durable result exists

If exact response text already exists durably, inference must **not** run again. Transport/delivery owns retry.

This protects against duplicated assistant output when the model completed but UI/channel delivery became uncertain.

## Response may have reached the user but exact durable payload is missing

The accepted v0.9.1 fence fails closed rather than regenerating text. Ambiguous UI visibility is not treated as permission to infer again.

## External side effect may already have happened

A retry is permitted only when the external action has an idempotency/receipt/read-after-write contract that proves repeating the action is safe. Model-call recovery alone is never sufficient evidence.

## Process exit is not success proof

Live diagnostics also produced cases where the OpenClaw CLI process returned exit code 0 while the inner agent result was an error/timeout. CogentNexus must therefore inspect durable/inner completion evidence rather than treating process exit or a top-level wrapper status as proof of successful inference.

Success requires the appropriate combination of durable result state, inner completion/liveness state, and delivery/result fences for the operation being classified.
