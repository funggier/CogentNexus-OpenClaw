# CNX-20260926-450 — Headless Agent Durable Settlement

Status: `BACKLOG`
GitHub issue: `#42`
Discovered by: `CNX-20260926-449-long-running-model-lease-guard.md`
Baseline release: `v0.9.8` (immutable)

## Trigger

CNX-449 used `openclaw agent` without `--deliver` as an isolated Gateway-routed acceptance surface. The model call completed and the invoking CLI received the final response, but CogentNexus retained the Ticket at `accepted` with `response_ready_at` present and no delivery-confirmation row.

## Objective

Define the durable settlement/receipt contract for the headless OpenClaw agent return-to-caller surface without weakening Dashboard/Discord exactly-once delivery semantics.

## Evidence

- session: `agent:main:cnx449-live-ollama`;
- Ticket: `CNXT-ce33b7ae-2e88-4150-bba9-8d34ee68f1ab`;
- run: `57245acc-0448-4d4b-b3ac-81212e28e45d`;
- final model call: completed;
- final response returned by CLI;
- Ticket remained `accepted + response_ready` after a supervisor reconciliation cycle;
- no delivery row and no outbox row;
- the isolated Ticket was explicitly cancelled after evidence capture, leaving no runtime residue.

## Constraints

- distinguish CLI return-to-caller from channel `--deliver` semantics;
- do not synthesize receipt without observable transport acceptance;
- preserve Ticket-first durability and existing Dashboard/Discord fences;
- no change to immutable `v0.9.8`.

## Current classification

`CNX450_BACKLOG_HEADLESS_SETTLEMENT_CONTRACT`
