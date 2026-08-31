# CNX-20260826-077 — Diagnose Owner-Entry Semantic Admission Contract

Status: `READY_FOR_HERMES`

Execution mode: `SOURCE_DIAGNOSTIC_TDD_OWNER_ENTRY_CONTRACT`

Current authorization: `OWNER_ENTRY_DIAGNOSIS_AND_SOURCE_REPAIR_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes after operator continuation

## Goal

Resolve the Task-076 blocker without sending another live semantic acceptance message.

Determine, from exact OpenClaw `2026.7.1-2` behavior and the installed CogentNexus plugin contract, why:

`openclaw agent --session-key agent:main:main ...`

started a real Ollama-backed run but created no Ticket before inference.

Classify the cause as exactly one of:

1. **surface-selection mismatch** — the chosen CLI surface is intentionally not an owner-trusted semantic entry and the existing CogentNexus admission policy is correct; or
2. **product admission-coverage defect** — a legitimate normal owner semantic surface is rejected or bypassed by the current CogentNexus owner-admission contract.

If and only if a product defect is proven, repair it with TDD using the narrowest safe trusted-owner rule. Do not broaden arbitrary CLI/channel/subagent admission.

## Accepted predecessor

Task 076 result:

`BLOCKED_SEMANTIC_ENTRY_PATH`

Independent review:

Decision: `ACCEPT`

Disposition:

`ACCEPT_BLOCKER_SEMANTIC_ENTRY_PATH_OWNER_SIGNAL_COVERAGE`

Task-076 report HEAD:

`4dc5dbba9b5933f6f2ca274cbea0c1eee0fe446d`

Task-076 review commit:

`67de33878ef35fe32e584d15bfc86ee0b8354b8b`

Accepted live source remains:

`79b51ed06363f6e8862c491ee0a313ddb412c806`

Task-076 failed run identity:

- owner/session key targeted: `agent:main:main`
- OpenClaw run ID: `97b7e136-3258-415b-a595-02792d393ff9`
- nonce: `CNXSEM-20260826T212900Z-7F3A`
- provider/model reached: `ollama / qwen3.5:9b`
- terminal surface result: provider-stage timeout
- Ticket DB before/after: zero Tickets, zero Ticket events, zero outbox rows

The Task-076 message MUST NOT be resent.

## Hard live fence

This task is source/read-only-live diagnosis only.

Do NOT:

- send any new user/semantic test message through OpenClaw;
- resend the Task-076 nonce;
- install or install-over;
- uninstall/reset/cleanup;
- restart Gateway/Ollama/Supervisor merely for diagnosis;
- change provider/model/plugin/config/AGENTS;
- mutate Ticket/SQLite/session state;
- invoke Ollama directly for a semantic test;
- merge/tag/release;
- use the primary workspace for implementation.

Allowed live access is read-only inspection of local OpenClaw 2026.7.1-2 package/runtime/help/logs/config and the existing Task-076 evidence.

## Phase A — execution and worktree fence

1. Fetch current remote coordination branch.
2. Verify current HEAD contains the Task-076 report and accepted blocker review.
3. Read current `ACTIVE.md`, `STATUS.md`, this Task 077, Task-076 task/report/review.
4. Create a fresh isolated worktree/branch from the current coordination HEAD.
5. Record:
   - coordination execution HEAD;
   - isolated worktree path;
   - branch name;
   - `git status --short` clean;
   - accepted source ancestor `79b51ed...`.
6. Do not use the live OpenClaw workspace as the source edit location.

## Phase B — trace exact OpenClaw owner-entry contract

Use the installed/public exact OpenClaw `2026.7.1-2` implementation available locally. Do not infer semantics from names alone.

Trace the real code path for at least these surfaces where present:

- `openclaw agent --session-key ...`;
- dashboard/WebChat user turn;
- supported session-send/message surface used by OpenClaw itself, if distinct.

For each relevant surface determine and record:

1. whether it invokes the plugin `before_agent_run` hook;
2. the `sessionKey` shape provided to the hook;
3. the source and exact semantics of `event.senderIsOwner`;
4. whether owner trust is derived from authenticated dashboard control, channel sender identity, CLI invocation, or another verified runtime signal;
5. whether there is any additional hook context/trigger/channel metadata that is safer than session-key pattern matching;
6. whether the surface naturally executes final reply delivery hooks (`reply_dispatch` / `message_sent`).

Do not treat a CLI command that merely targets an existing session as owner-authenticated unless exact OpenClaw code proves that contract.

### Task-076 correlated evidence

Inspect the preserved Task-076 OpenClaw logs/evidence read-only if available. Determine whether the failed run itself exposes:

- `senderIsOwner`;
- trigger/channel/surface identity;
- session-key transformation;
- evidence that `before_agent_run` was invoked and returned pass rather than being bypassed.

If those fields were not logged, state that explicitly. Do not generate another live run to obtain them in this task.

## Phase C — compare against current CogentNexus policy

Current accepted production behavior includes:

```ts
export function durableAdmissionEligible(input: { sessionKey?: string; senderIsOwner?: boolean }) {
  if (!input.sessionKey || input.sessionKey.includes(":subagent:")) return false;
  if (input.senderIsOwner !== false) return true;
  return /^agent:[^:]+:dashboard:[^:]+$/u.test(input.sessionKey);
}
```

Current tests intentionally accept dashboard sessions with `senderIsOwner=false` and reject arbitrary CLI sessions with `senderIsOwner=false`.

Compare exact OpenClaw runtime semantics against this policy.

### Classification A — surface-selection mismatch

Use this only if exact OpenClaw evidence proves:

- `openclaw agent` is not an authenticated owner semantic surface under the hook contract; and
- a separate supported owner surface exists that current CogentNexus policy already accepts; and
- that surface can carry a real user turn through `before_agent_run` and final delivery without a Ticket/model shortcut.

If Classification A is proven:

- do not change production source merely to make CLI convenient;
- add/strengthen executable compatibility tests only where needed to encode the exact owner-surface contract;
- document the exact supported surface that the next live semantic task must use.

### Classification B — product admission-coverage defect

Use this only if exact OpenClaw evidence proves a legitimate owner user-message surface reaches the hook with metadata current CogentNexus rejects or mishandles.

If Classification B is proven:

- use strict TDD;
- first add a RED test that faithfully models the exact OpenClaw 2026.7.1-2 hook metadata;
- prove the current accepted source fails that test for the correct reason;
- implement the smallest safe production change;
- GREEN the focused test;
- preserve rejection of subagents, internal continuation turns and untrusted/arbitrary CLI/channel senders;
- do not whitelist `agent:main:main` by string alone unless OpenClaw source proves that namespace itself is a stable authenticated-owner invariant;
- prefer an explicit trusted runtime signal/metadata when available.

## Phase D — production-facing Ticket-before-inference test

Regardless of Classification A or B, add or identify an executable production-facing test proving the chosen legitimate owner surface metadata actually reaches the Ticket-first hook behavior.

The test must exercise the registered `before_agent_run` handler or an equivalent production integration boundary, not just `durableAdmissionEligible()` in isolation.

For a simple direct-lane prompt in an isolated temp workspace/database prove:

1. exactly one Ticket is accepted;
2. exact prompt/run/session identity is stored;
3. `accepted` event exists;
4. `routed` event exists with `workflowEligible=false`;
5. hook outcome permits normal inference after Ticket commit;
6. a rejected untrusted CLI/subagent fixture creates no Ticket;
7. Ticket commit exists before any provider stub/inference continuation is allowed by the harness.

No real Ollama call is required or allowed for this source test.

## Phase E — provider-timeout secondary diagnosis

Task 076 also observed an Ollama provider-stage idle timeout after ~245 seconds. This is secondary to the missing Ticket because Ticket admission should already have happened.

Read-only diagnose whether existing evidence indicates:

- a persistent provider health incident;
- resource contention/model loading;
- OpenClaw idle-timeout policy;
- a one-off timing condition;
- or insufficient evidence.

Do not change model/provider/timeouts in Task 077.

Record whether anything here must block the next semantic attempt. If evidence is insufficient, say so rather than guessing.

## Phase F — regression verification

Run focused tests first, then full gates.

Required where applicable:

- owner-entry/admission focused tests;
- TicketStore/direct-delivery tests;
- plugin index/admission tests;
- Task-069 fresh transaction coverage;
- Task-070/071 nonfresh mode isolation tests;
- Task-073/074 recovery preflight/isolation tests;
- full `pytest tests/ -q` with zero failures;
- PowerShell full-file parse for modified `.ps1` files if any;
- plugin `npm ci`, validate and tests under npm 11 / Node 24 compatible path;
- plugin `npm ci`, validate and tests under npm 12 compatible path;
- exact pinned OpenClaw version remains `2026.7.1-2`;
- repository baseline consistency checks;
- final worktree clean after commits.

If production source changes, independently verify no unrelated installer/runtime behavior changed.

## Phase G — publication fence

If there is an implementation/test change:

1. commit implementation/tests first;
2. record implementation HEAD;
3. verify diff from execution HEAD contains only justified Task-077 files;
4. then add the report in a separate report-only commit.

If no source/test change is required, report-only publication is acceptable only when the diagnosis is backed by exact OpenClaw source/runtime evidence already captured.

Report path:

`docs/operations/coordination/reports/CNX-20260826-077-diagnose-owner-entry-semantic-admission-contract.md`

The report must include:

- execution HEAD and implementation HEAD if any;
- exact OpenClaw 2026.7.1-2 source/runtime evidence for each examined message surface;
- actual owner-signal semantics;
- Task-076 failed-surface explanation;
- Classification A or B with evidence;
- RED/GREEN evidence if production was changed;
- production-facing Ticket-before-inference test evidence;
- untrusted/subagent negative tests;
- provider-timeout secondary diagnosis;
- full verification results;
- live hard-fence statement;
- implementation-to-report publication fence.

## Result tokens

Use exactly one:

- `PASS_OWNER_ENTRY_SURFACE_CONTRACT_PROVEN_NO_SOURCE_CHANGE`
- `PASS_OWNER_ENTRY_COVERAGE_REPAIRED`
- `BLOCKED_OPENCLAW_OWNER_SIGNAL_UNPROVEN`
- `BLOCKED_NO_SUPPORTED_OWNER_SURFACE`
- `BLOCKED_OWNER_ENTRY_SECURITY_REGRESSION`
- `BLOCKED_TEST_OR_VALIDATION_FAILURE`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Successor rule

If `PASS_OWNER_ENTRY_SURFACE_CONTRACT_PROVEN_NO_SOURCE_CHANGE` is independently accepted, the next task may perform one new final semantic acceptance message through the exact proven supported owner surface. The failed Task-076 nonce remains retired and MUST NOT be reused.

If `PASS_OWNER_ENTRY_COVERAGE_REPAIRED` is independently accepted, the new source must first be installed through the supported install-over path with source/live parity and health verification before another final semantic acceptance message is authorized.
