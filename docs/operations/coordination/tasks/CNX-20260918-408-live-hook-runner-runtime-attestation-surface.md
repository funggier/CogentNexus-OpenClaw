# CNX-20260918-408 — Live Hook Runner Runtime Attestation Surface

Status: `IN_PROGRESS_CHATGPT`

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Parent: `CNX-20260918-407`
- Executor: `ChatGPT`
- Human final authority: `Operator`
- Architecture report: `docs/operations/coordination/reports/CNX-20260918-407-pre-inference-admission-hook-strategy-review-report.md`

## Objective

Add a read-only, operator-scoped Gateway RPC that reports whether the active OpenClaw runtime can attest the `before_agent_run` hook boundary before any semantic model request is sent.

The surface must use the public OpenClaw plugin SDK exposed by the pinned runtime dependency and must not mutate the hook registry.

## Required method

Gateway RPC:

`cogentnexus.runtimeAttestation`

Scope:

`operator.read`

## Required evidence

Return a non-secret structured snapshot including at least:

- schema version;
- CogentNexus plugin ID;
- target hook name;
- whether the global hook runner exists;
- global hook count for `before_agent_run`;
- CogentNexus `before_agent_run` count in the most recently initialized registry when inspectable;
- a conservative classification:
  - `PRESENT`
  - `ABSENT`
  - `AMBIGUOUS`
  - `RUNNER_UNAVAILABLE`

Classification must not claim CogentNexus presence solely because another plugin owns a `before_agent_run` hook.

## Classification contract

- no global runner -> `RUNNER_UNAVAILABLE`
- global count == 0 -> `ABSENT`
- global count > 0 and latest registry contains at least one CogentNexus `before_agent_run` registration -> `PRESENT`
- global count > 0 but latest registry does not establish CogentNexus ownership -> `AMBIGUOUS`

The latest-registry record is a sufficient positive proof because that registry is one source of the composed runner. Its absence is not sufficient negative proof because the composed runner may include other live registries.

## Implementation constraints

- Use public `openclaw/plugin-sdk/plugin-runtime` exports.
- Do not invoke `runBeforeAgentRun` from the attestation path.
- Do not register/re-register hooks from the attestation path.
- Do not inspect provider credentials.
- Do not touch TicketStore.
- Do not alter provider/model/auth/routing.
- Do not patch OpenClaw.
- Keep the method available only when normal CogentNexus Host authority allows runtime registration.
- Add focused tests for classification and Gateway method registration.
- Correct misleading source comments only where necessary to reflect accepted CNX-385+ evidence.

## TDD

1. Add focused RED contract tests.
2. Implement the smallest attestation module.
3. Wire it into the release entry.
4. Run/inspect repository validation available through GitHub CI or report any unavailable local execution honestly.

## Hard fences

- No production deploy/install-over.
- No Gateway restart/reload.
- No live Gateway RPC call in this task.
- No semantic/model/provider request.
- No config/environment/Scheduled Task mutation.
- No release/tag/main.
- No force push/history rewrite.

## Exit

Use:

- `RUNTIME_ATTESTATION_IMPLEMENTED_PENDING_LIVE_QUALIFICATION`
- `RUNTIME_ATTESTATION_BLOCKED_BY_SDK_BOUNDARY`
- `RUNTIME_ATTESTATION_TEST_FAILURE`

Do not perform the live machine qualification in this task.
