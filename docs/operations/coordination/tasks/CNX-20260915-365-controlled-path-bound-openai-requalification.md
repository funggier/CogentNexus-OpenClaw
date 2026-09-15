# CNX-20260915-365 — Controlled Path-Bound OpenAI Requalification

Status: `READY_FOR_HERMES`
Parent: `CNX-20260915-364`
Base: `CNX-20260915-364_PATH_BOUND_RUNTIME_PROVENANCE`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`

## Objective

Prepare a controlled, path-bound requalification of the OpenAI Dashboard/Ticket-first path using the current canonical state established by CNX-364. This task does not restore or assume any historical CNX-361/CNX-362 controller identity and does not treat historical `generation=103` as a durable precondition.

## Required path-bound proof before any semantic test

The read-only preflight must resolve and record, at test time, the exact path and SHA-256 (or repository-established equivalent exact hash) for:

- canonical current state root;
- current controller identity;
- current ownership manifest;
- current launcher binding;
- current installed candidate identity.

The preflight must also record the current controller/root relationship and enough runtime-authority/process context to show which path is being tested. Historical generation values may be recorded as evidence, but `generation=103` is not required merely because CNX-361 recorded it.

A missing, conflicting, or unbound path identity is `BLOCKED`; do not guess, normalize, or continue to semantic execution.

## Execution boundary

This task is initially limited to read-only path-bound preflight and preparation of the evidence contract. A fresh Dashboard request and any OpenAI semantic test require a later explicit authorization after the preflight passes. The operator must perform any actual Dashboard UI action. No Dashboard handoff is issued during authority alignment or preparation.

## Hard fences

- Do not enable, disable, start, stop, restart, reinstall, or otherwise mutate runtime state.
- Do not edit controller.json, provider/auth/routing, hooks, main, or the v0.9.5 tag/release.
- Do not require or restore historical controller identity or generation numbers.
- Do not send a Dashboard/model request in the preparation phase.
- Do not claim OpenAI PASS, CURRENT_RED, or semantic requalification before separately authorized execution and evidence.
- Do not rewrite CNX-360/361/362/363/364 historical records.
- Do not force-push or rewrite history.

## Deliverable and stop gate

Publish a report under `docs/operations/coordination/reports/` containing exact branch/head, path-bound identities and hashes, preflight result, explicit mutation/request counts, and the authorization boundary. Stop if the preflight is blocked or if semantic execution is not explicitly authorized.
