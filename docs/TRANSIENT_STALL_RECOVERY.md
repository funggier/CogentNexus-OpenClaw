# Transient Model-Call Stall Recovery

CogentNexus is designed to preserve accepted user intent across transient failures that may disappear on a retry.

One practical failure mode is a **model call that starts but stops making observable progress**. Native OpenClaw testing on 2026-08-21 demonstrated that this behavior can be nondeterministic: with the same configuration, provider, model, and tool policy, one run can stall until OpenClaw interrupts it while a later run succeeds without changing configuration or restarting the provider.

This observation does **not** establish that a specific provider, model, or OpenClaw tool is universally defective. It establishes a continuity problem: a transient inference stall can otherwise force the user to notice the failure and manually repeat the original request.

## Observed failure shape

A representative native failure looked like this conceptually:

```text
user request
   -> model_call started
   -> no model-call progress
   -> long-running diagnostic
   -> stalled_agent_run
   -> watchdog / interrupt
```

In the controlled tests, stalled runs reached the OpenClaw watchdog boundary at roughly six minutes, while an identical later retry could complete successfully.

The same test campaign also showed that tool-schema composition can change latency or success behavior in non-monotonic ways. A smaller tool set is therefore not guaranteed to fail or succeed solely because it is smaller, and a single PASS/FAIL is not sufficient evidence to blame one tool.

## Why Ticket-first continuity matters

In MANAGED mode, CogentNexus can durably accept an eligible user message as a Ticket before inference. The original intent therefore survives the lifetime of a single OpenClaw/model call.

Conceptually:

```text
receive message
   -> commit Ticket
   -> begin inference
   -> inference stalls
   -> classify interruption from durable/observable evidence
   -> recover the same eligible Ticket within bounded retry policy
   -> commit durable result
   -> deliver
```

The important property is not simply "retry on timeout". Recovery is constrained by durable state.

## Recovery boundaries

CogentNexus must distinguish three materially different cases.

### 1. Inference stalled and no durable result exists

If the run is confirmed stalled, the Ticket is still eligible, no durable response/result has been committed, and no protected external side effect has already been performed, bounded recovery may retry inference for the **same committed Ticket**.

A transient provider/model stall is therefore a recovery candidate, not proof that the provider is permanently offline.

### 2. Durable result already exists, but delivery is incomplete or unconfirmed

Once completed response content is durable, recovery must **not rerun inference merely because delivery failed**.

Instead:

```text
durable result exists
   -> retry delivery / redelivery
   -> do not regenerate completed work
```

This is the purpose of the Delivery Commit Gate and Direct Recovery Guard.

### 3. External side effects may already have happened

Consequential actions cannot be repeated blindly. Recovery must use idempotency, receipts, checkpoints, or read-after-write evidence before deciding whether any external action may be retried.

A timeout or missing UI reply is never sufficient evidence that an external side effect did not occur.

## What CogentNexus does not claim

CogentNexus does not claim to:

- make every model/provider/tool combination reliable;
- diagnose every stall as a provider defect;
- retry forever;
- treat every interruption as permission to rerun inference;
- repeat external side effects without evidence;
- override intentional operator stop/maintenance state.

Its role is to preserve durable intent and apply bounded recovery at the correct boundary so that a transient failure does not silently discard accepted work or cause completed work to be repeated.

## Operational lesson

A useful mental model is:

```text
transient inference failure
        +
durable accepted intent
        +
evidence-aware bounded recovery
        =
continuity without blind duplication
```

This is one of the practical reasons CogentNexus places deterministic Host/Ticket state outside the lifetime of OpenClaw and any individual LLM call.
