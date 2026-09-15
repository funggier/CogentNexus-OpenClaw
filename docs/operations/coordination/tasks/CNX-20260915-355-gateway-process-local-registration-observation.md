# CNX-355 — Gateway Process-Local Registration Observation

Status: `READY_FOR_HERMES`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Parent: `CNX-354`
Execution mode: `READ_ONLY_RUNTIME_OBSERVATION`

## Objective

Close the remaining CNX-354 observability gap without changing CogentNexus/OpenClaw production behavior.

Use an already-supported authenticated Control UI / Gateway client path that has previously been proven to carry `operator.read` and `operator.admin`. Do not create a new Gateway method, patch OpenClaw, alter permissions, extract credentials, or broaden authority.

The target evidence is process-local Gateway evidence for the currently running Gateway instance sufficient to distinguish:

1. actual loaded CogentNexus release-entry module identity;
2. effective plugin-manager/runtime registration identity;
3. canonical `before_agent_run` registration ownership and priority;
4. whether the effective Gateway registry contains the CogentNexus admission handler;
5. whether the observed state can explain or exclude the historical CNX-344 OpenAI Ticket-first bypass.

## Evidence baseline

CNX-354 established:

- Gateway connectivity is healthy;
- the default CLI connection is `connect-only` and reports missing `operator.read`;
- documented `gateway call health/status` surfaces are too coarse for process-local registration proof;
- CLI `plugins inspect --runtime` is CLI-process-local and cannot prove Gateway process identity;
- no Level-3 Gateway process-local registration evidence was obtained;
- no production defect was proven and no production source was changed.

A prior read-only investigation (CNX-091) established a supported Control UI path with:

- client `openclaw-control-ui`;
- mode `webchat`;
- role `operator`;
- effective scopes including `operator.read` and `operator.admin`;
- successful read-only `sessions.list` RPC;
- no credential value copied or entered by the investigator.

Use that prior evidence only to select the supported client boundary. Re-verify the live connection before relying on it.

## Hard fences

- No production source modification.
- No OpenClaw source modification.
- No new Gateway diagnostic method.
- No permission/scope broadening.
- No token/password extraction, display, persistence, or rotation.
- No Gateway restart/stop/start.
- No plugin reinstall/enable/disable.
- No provider/model/auth/routing mutation.
- No Dashboard semantic message or provider invocation.
- No CNX-344 replay/resend.
- No Ticket/SQLite/session/transcript/delivery mutation.
- No v0.9.5 tag/history mutation.
- No force-push/history rewrite.

## Required execution

1. Verify remote branch and parent ancestry from GitHub.
2. Verify the Gateway is still running and record only non-secret process identity already exposed by supported status.
3. Establish a read-only authenticated Control UI / Gateway connection using the existing paired profile. Do not inspect or copy token/password values.
4. Confirm the live connection is authorized for `operator.read` (and `operator.admin` where exposed) using non-secret metadata.
5. Enumerate the supported read-only Gateway RPC/method surface available to that authenticated connection.
6. Determine whether any existing supported method returns process-local plugin/runtime registration data. Do not invent or probe undocumented mutating methods.
7. If a supported read method exists, capture only the minimum required redacted fields for the CNX-354 objective.
8. If the supported read-only surface still cannot expose Level-3 state, classify the boundary explicitly as `UNRESOLVED / BLOCKED` and stop. Do not create new runtime instrumentation in CNX-355.
9. Preserve raw evidence and publish the CNX-355 report.
10. Verify the final remote branch tip and report path/blob from GitHub after publication.
11. Stop for independent ChatGPT review.

## Decision rules

- **PASS / BOUNDARY_CLOSED:** only when supported authenticated Gateway evidence directly binds the effective Gateway process to a concrete CogentNexus module/registration identity and shows the effective `before_agent_run` owner/priority/registry state.
- **UNRESOLVED / BLOCKED:** when the supported read-only interface remains unable to expose those process-local facts.
- **DEFECT:** only if direct Gateway-process evidence demonstrates an actual registration/module mismatch or equivalent causal divergence. A mere absence of observability is not a defect.

## Required report

`docs/operations/coordination/reports/CNX-20260915-355-gateway-process-local-registration-observation-report.md`

No production fix is authorized by CNX-355. Any production repair must be a separate successor task after a concrete defect is proven and independently reviewed.
