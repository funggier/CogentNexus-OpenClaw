# Ticket-first Admission — Current Baseline

Ticket-first means an eligible owner message in MANAGED mode can be durably admitted **before inference**. It does not mean every message becomes a workflow.

## DIRECT example

For a greeting or ordinary question:

```text
user message
  -> durable Ticket
  -> DIRECT inference
  -> response_ready/direct_result
  -> delivery confirmed
  -> completed
```

`workflow_eligible=0` is valid and expected for lightweight Direct work.

## Why admission comes first

If Gateway/provider/runtime fails after durable admission, the Host can decide whether the request is genuinely pre-response and eligible for Direct Recovery without requiring the user to repeat the intent.

## Duplicate rule

The exact recovery/native restart continuation of an already-owned Direct Ticket is not admitted as a second user Ticket. The v0.9.9 ownership fence runs before legacy Ticket-first intake for that exact compatibility envelope.

Ordinary messages, different sessions, generation drift, terminal recovery state, missing Host authority, or unreadable durable state must not be falsely claimed by the fence.

## Terminal rule

A Ticket is not complete merely because an LLM returned text. The durable result and delivery confirmation boundary determines completion.

See `docs/BASELINE.md` and `docs/CURRENT_STATE.md` for the full v0.9.1 invariants.
