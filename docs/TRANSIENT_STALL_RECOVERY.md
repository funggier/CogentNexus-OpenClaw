# Transient model-call stall recovery

CogentNexus treats a stalled model call as a recoverable failure candidate only when durable evidence proves that retrying inference cannot duplicate an already committed result or external side effect.

## Observed failure mode

Native OpenClaw/local-provider testing demonstrated a non-deterministic failure pattern in which the same model, provider, tool policy and prompt can stall in one run and complete in a later retry without a configuration change.

This is not evidence that a specific provider or tool is permanently broken. Tool-schema behavior may also be non-monotonic: a smaller tool set can fail while a larger set succeeds on another run. Single PASS/FAIL observations are therefore insufficient to assign a permanent culprit.

The operational fact that matters to CogentNexus is simpler:

> A model call can stop making progress even while Gateway/provider health endpoints remain reachable, and a later equivalent attempt can succeed.

## Why durable intent matters

Without an external durable owner, the user may have to notice the stall and send the request again manually. That loses the exact relationship between the original accepted intent, any partial execution, and later delivery.

CogentNexus commits eligible intent as a Ticket before inference and keeps recovery authority outside the lifetime of the stalled model call. The Host can then classify the interruption against durable Ticket/result/delivery state rather than guessing from UI behavior.

## Recovery boundary

### 1. No durable result exists

If the Host confirms that the model call exceeded its durable deadline, the Ticket is still inference-eligible, and no response-ready/durable-result/delivery fence exists, bounded inference recovery may be authorized.

The v0.9.1 Direct-stall path uses this order:

1. Host claims the expired model-call lease;
2. Gateway/provider runtime is quiesced;
3. delivery/result fences are reconciled while inference is impossible;
4. exactly one durable Direct-recovery authorization is written;
5. runtime restarts;
6. the hidden recovery worker consumes that authorization.

v0.9.2 preserves this classifier/order and replaces only the concrete local provider lifecycle adapter.

### 2. Durable result exists

If exact response text already exists durably, inference must **not** run again. Transport/delivery owns retry.

This protects against duplicated assistant output when the model completed but UI/channel delivery became uncertain.

### 3. Response may have reached the user but exact durable payload is missing

The accepted v0.9.1 fence fails closed rather than regenerating text. Ambiguous UI visibility is not treated as permission to infer again.

### 4. External side effect may already have happened

A retry is permitted only when the external action has an idempotency/receipt/read-after-write contract that proves repeating the action is safe. Model-call recovery alone is never sufficient evidence.

## Classification terminology

A stalled call should be classified as a transient model-call/recovery condition, not automatically as a permanently offline provider.

For example:

```text
model_call_stalled
  -> durable result absent?
  -> side-effect fence clear?
  -> bounded recovery candidate
```

This distinction matters because the exact same provider may answer normally on the next attempt.

## Provider independence

The Recovery Core owns the decision to retry inference. Provider adapters own only discovery, readiness, start and stop.

That separation allows the same durable recovery policy to operate above Ollama, LM Studio, or future local provider adapters without rewriting Ticket/result/delivery authority.
