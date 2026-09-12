# v0.9.5 Provider Switch Acceptance

## Purpose

Prove the central v0.9.5 invariant that OpenClaw owns provider/model routing while CogentNexus-OpenClaw preserves CNX continuity, identity, policy, and lifecycle state across a normal Web Chat provider switch.

This is a live acceptance procedure, not a substitute for automated tests.

## Preconditions

- Use one exact frozen candidate SHA for the entire acceptance run.
- Start from a healthy installed state with CogentNexus-OpenClaw enabled.
- Record provider/model names only; never record API keys, tokens, cookies, or other credentials.
- Establish one controlled CNX session and one Ticket whose identity can be inspected before and after each switch.
- Ensure the Gateway is otherwise stable and no unrelated maintenance operation is running.

## Baseline evidence

Record:

```text
candidate SHA
installed CNX version/fingerprint
logical session key
session generation
CNX mode
Ticket ID and run ID
Ticket status
plugin enabled/active state
Gateway lifecycle state
CNX policy fingerprint or selected non-secret policy fields
current OpenClaw provider/model route
```

## Provider-switch sequence

Use the normal OpenClaw Web Chat UI and exercise the providers actually configured on the acceptance machine:

```text
Ollama -> Cloud A -> Cloud B -> Ollama
```

After each switch, record the resulting provider/model route and re-check the CNX invariants below.

## Required negative invariants

A provider switch MUST NOT, by itself:

- change CNX mode or generation;
- create a new Ticket/session identity;
- invalidate the current Ticket/session owner;
- mutate CNX policy (`AGENTS.md` managed policy or equivalent state);
- disable or replace the CNX plugin;
- restart or stop the Gateway;
- invoke a CNX provider-selection action;
- rewrite OpenClaw-owned authentication, provider, or model configuration through CNX;
- trigger a CNX recovery workflow merely because the provider changed.

## Continuity checks

### Durable workflow

Start or continue one Durable workflow before a provider switch. After at least one switch, verify that the same Ticket remains the workflow identity and that no duplicate workflow was created.

### Direct response

Run one Direct response after a provider switch and verify that the final payload still settles through the canonical Delivery Core with the expected session/generation fence.

### Failure case

Force or observe one provider failure without changing the provider-routing owner. Verify the Ticket remains recoverable and that provider failure does not silently create a replacement CNX identity.

## Pass criteria

PASS only when all of the following remain true across the complete sequence:

```text
CNX mode unchanged
CNX generation unchanged solely because of provider switching
Ticket identity unchanged
session identity unchanged
plugin remains active
Gateway lifecycle unchanged
CNX policy unchanged
OpenClaw provider/model route remains OpenClaw-owned
Durable work continuity preserved
Direct delivery remains canonical and fenced
```

Any unexpected lifecycle/configuration mutation, duplicate identity, or provider-selection behavior is a release blocker.

## Evidence handling

Runtime evidence belongs in a coordination/acceptance report associated with the exact candidate SHA. Do not commit credentials, raw auth configuration, or other machine-sensitive data.
