# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_TDD_SEMANTIC_P1_REPAIR_AND_BOUNDED_PROVIDER_DIAGNOSTICS`
Current authorization: `SEMANTIC_P1_REPAIR_AND_PROVIDER_READINESS_AUTHORIZED`
Task ID: `CNX-20260826-078`
Updated: 2026-08-26 22:11 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260826-078-close-semantic-p1s-and-provider-readiness.md`](tasks/CNX-20260826-078-close-semantic-p1s-and-provider-readiness.md)

## Task 077 review

Task 077 final amended report HEAD:

`b252879bdbc8cba8f187f883f943d9a913199204`

Partial test implementation HEAD:

`6867af2cad75cb4ee8e70206d70b0ba5bd5abeea`

Independent review decision:

`REWORK`

Disposition:

`REWORK_UNRESOLVED_SEMANTIC_P1S_AND_PROVIDER_READINESS`

Review path:

[`reviews/CNX-20260826-077-diagnose-owner-entry-semantic-admission-contract.md`](reviews/CNX-20260826-077-diagnose-owner-entry-semantic-admission-contract.md)

## Accepted Task-077 findings to preserve

- `openclaw agent --session-key agent:main:main` is not owner-authenticated merely by choosing that session key; do not broaden arbitrary CLI admission.
- Dashboard/WebChat is the supported owner-surface candidate for eventual live semantic acceptance.
- canonical installed v0.9.3 plugin generation/source identity and dynamic hook registration were materially verified.
- registered-hook owner positive and CLI/subagent negative tests from `6867af2...` are useful and remain part of the candidate source lineage.
- no new semantic message was sent in Task 077.

## Why Task 078 exists

The comprehensive Task-077 report carried unresolved P1s and independent review confirmed additional direct-path idempotency evidence was missing. Task 078 must close/prove these before any new semantic message:

1. delivery-marker owner/session binding and fail-closed behavior;
2. repeated `before_agent_run` route/event idempotency;
3. single timeout/recovery authority for Ticketed direct runs;
4. direct model-call lease/Host ordering, repairing only if deterministic RED proves a defect;
5. workflow completion stale/concurrent scheduling idempotency;
6. coherent direct owner -> Ticket -> response-ready -> owner-bound delivery terminal integration;
7. exact OpenClaw `2026.7.1-2` / Ollama provider readiness and timeout hierarchy.

The operator explicitly authorized a heavy comprehensive pass.

## Provider diagnostic authorization

Task 078 may perform at most two inert **direct local Ollama** probes to the already configured `qwen3.5:9b` solely to measure first-token/total timing. These probes bypass OpenClaw/CogentNexus and must not mutate product durable state or configuration.

No OpenClaw owner/user semantic message is authorized.

## Hard live fences

No Dashboard/WebChat semantic turn, no `openclaw agent` semantic/provider probe, no reuse of the Task-076 nonce, no live Ticket/session/SQLite mutation, no install/install-over/uninstall/reset/cleanup, no provider/model/config/plugin/AGENTS change, no diagnostic restart/reboot, no merge/tag/release. Source work must use a fresh isolated worktree.

Accepted live production source remains:

`79b51ed06363f6e8862c491ee0a313ddb412c806`

Any accepted Task-078 production source must later pass supported install-over/source-live parity before a new final semantic message is authorized.
