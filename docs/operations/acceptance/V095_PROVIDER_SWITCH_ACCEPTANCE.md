# v0.9.5 Provider Switch Acceptance

## Purpose

Verify that changing the OpenClaw-selected provider does not transfer provider/model/auth lifecycle ownership to CogentNexus-OpenClaw and does not rotate the Cogent session generation merely because the provider changes.

This document defines the acceptance protocol. It is not evidence that the live test has passed.

## Preconditions

- Candidate is built from one exact v0.9.5 SHA.
- CogentNexus-OpenClaw is enabled in managed mode with a valid owner session.
- The OpenClaw provider/auth/model configuration is captured before the test.
- The same owner `sessionKey`, `sessionId`, and generation are recorded before and after the switch.
- A controlled Direct and a controlled Durable Ticket are available for the test.
- No unrelated Gateway lifecycle or configuration operation is scheduled during the observation.

## Baseline capture

Record before the switch:

- candidate commit SHA;
- OpenClaw provider identity and model selection;
- OpenClaw auth/profile/routing configuration identifiers, without copying secrets;
- CNX mode and desired Gateway state;
- CNX session identity and generation;
- policy/ownership state;
- pending Ticket/recovery/delivery counts;
- managed local-provider adapter state.

## Switch sequence

1. Start with provider A and submit one controlled Direct request.
2. Confirm the request is bound to the current owner session/generation.
3. Start one controlled Durable Ticket.
4. Change only the OpenClaw-selected provider from A to provider B using the native OpenClaw provider path.
5. Do not invoke a CNX reset, delete, rotate, mode change, Gateway lifecycle command, or local-provider recovery operation as part of the switch.
6. Capture the exact state immediately after the provider switch.
7. Allow the Durable Ticket to continue under the same owner lifecycle.
8. Verify that a subsequent Direct request can still bind to the same active CNX lifecycle.

## Acceptance invariants

The test passes only when all applicable observations hold:

- provider/model/auth ownership remains OpenClaw-owned;
- CNX mode is unchanged;
- session generation is unchanged solely because of provider switch;
- CNX policy state is unchanged;
- Gateway lifecycle state is unchanged;
- managed local-provider adapter state is unchanged unless an explicitly authorized local-provider operation was separately requested;
- the Durable Ticket remains bound to its original owner lifecycle and continues or recovers without being recreated solely because the provider changed;
- no stale-generation delivery is accepted;
- no provider switch creates a second CNX lifecycle for the same physical session;
- provider selection is retained only as provenance/route metadata where the surrounding OpenClaw interface requires it, never as CNX lifecycle authority.

## Failure classification

Classify observed failures precisely:

- **Ownership violation:** CNX mutates provider/auth/model/Gateway ownership state.
- **Generation violation:** provider switch rotates generation without a physical lifecycle boundary.
- **Continuity violation:** the existing Durable Ticket is lost, duplicated, or rebound to a different lifecycle without authorization.
- **Delivery violation:** a stale or mismatched delivery is accepted after the switch.
- **Evidence failure:** required before/after state or process evidence is missing or ambiguous.

## Evidence retention

Retain the exact candidate SHA, before/after state snapshots, Ticket IDs, session identity/generation, provider transition evidence, and structured runtime records. Redact secrets and tokens; retain identifiers sufficient to prove ownership and continuity.

A missing observation is not PASS. The final record must distinguish `PASS`, `FAIL`, and `INDETERMINATE`.

## Release gate

Live provider-switch acceptance must be completed against the exact release candidate after Tasks 1–5 are frozen and before any public `v0.9.5` release/tag is published.
