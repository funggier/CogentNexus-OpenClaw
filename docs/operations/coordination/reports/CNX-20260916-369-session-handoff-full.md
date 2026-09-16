# CNX-20260916-369 — Full Session Handoff

## Purpose

This document is the durable handoff for the current ChatGPT session. The next session must treat GitHub remote state as authoritative and continue from the exact branch tip recorded below. It must not rely on conversational memory, pasted historical SHA values, or local-only state when those can be verified from GitHub.

## Repository and current authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Working branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Current remote branch HEAD verified through GitHub: `71ff37a8536cd339548b0e4b3f9c2810858f54ff`
- Current branch tip commit message: `coordination: restore CNX-369 task on authoritative tip`
- Current active task: `CNX-20260916-369`
- Current state: `CNX369_RUNTIME_ACTIVATION_VERIFICATION`
- Current status: `READY_FOR_HERMES`
- Executor: Hermes
- Reviewer: ChatGPT
- Human final authority: Operator

The current authority files on the remote branch identify CNX-369 as the active successor and define the task as supported runtime activation plus read-only effective registration verification. They explicitly forbid any Dashboard/model semantic request during CNX-369. fileciteturn170file0 fileciteturn171file0

## Current task

Task file:
`docs/operations/coordination/tasks/CNX-20260916-369-runtime-activation-verification.md`

Current task blob:
`107f41aeef5b51da66698f97f47e81fb58027d5c`

The task objective is to activate the already-verified repaired CogentNexus artifact in the exact path-bound OpenClaw runtime, prove that the active Gateway process is using the repaired entrypoint, and prove that the downstream `before_agent_run` registration path is effective. It permits only the supported bounded runtime lifecycle required for activation. It explicitly does not permit a semantic Dashboard/model request. fileciteturn174file0

## Current next step

Execute CNX-369 only.

The correct sequence is:

1. Read current GitHub `ACTIVE.md`, `STATUS.md`, and CNX-369 task at the exact remote tip.
2. Verify the current canonical state root, controller, ownership manifest, launcher, installed plugin manifest, and installed entrypoint.
3. Verify whether the installed entrypoint equals repaired SHA-256:
   `04e12be2dc24a8f60c079031737c32bca5990251e8c219066a4413c31eab802`
4. If it is not active, use only the supported bounded activation/reload/install mechanism needed to activate that already-verified artifact. Do not manually edit controller state and do not bypass the supported lifecycle.
5. Record any lifecycle mutation with exact action, timestamp, pre/post process identity, and resulting installed artifact identity.
6. Verify the resulting Gateway process identity.
7. Prove that the live Gateway process has actually loaded the repaired entrypoint, not merely that the repaired file exists on disk.
8. Verify the authority gate accepts the live canonical schema-v2 controller and that the downstream `before_agent_run` registration path is effective.
9. Publish the CNX-369 activation report.
10. Read the report back from GitHub and verify the final branch HEAD.
11. STOP.

No Dashboard/model request belongs in CNX-369. Live semantic requalification is a separate successor authorization. fileciteturn174file0

## Proven defect before repair — CNX-367

The original OpenAI Dashboard Ticket-first bypass is proven.

Exact forensic anchor:

- Dashboard session key:
  `agent:main:dashboard:83027933-3a42-4877-a79a-167caaa396a5`
- Dashboard session UUID:
  `83027933-3a42-4877-a79a-167caaa396a5`
- Runtime session ID / traceId:
  `7b1a5ad4-0560-4b19-ae4e-609f9492b2c5`
- Run ID:
  `c3e88413-5199-4d0c-bfec-deb33e86928e`
- Provider:
  `openai`
- Model:
  `gpt-5.6-luna`
- API:
  `openai-chatgpt-responses`
- Thread ID:
  `01a0a9a3-21b4-76f3-9613-aee47672410f`
- Turn ID:
  `01a0a9a3-3583-79a2-87a3-ba59109b47c4`
- Exact semantic message:
  `Reply exactly with CNX365-DONE.`

Verified trajectory:

`session.started → context.compiled → prompt.submitted → model.completed → session.ended`

The exact Dashboard request produced `CNX365-DONE`, but there was no `before_agent_run`, no `admission.trace.*`, no durable Ticket, no Ticket event sequence, no Ticket-linked Run/Call/Inference/Result/Delivery lineage, and no outbox evidence.

The proven first divergence was immediately after `prompt.submitted`: the active runtime went directly to model completion instead of entering the CogentNexus Ticket-first admission chain. CNX-367 was therefore classified `CURRENT_RED`. The test used exactly one Dashboard request and one OpenAI/model request, with zero runtime mutations and zero retries. fileciteturn151file0

## Root cause proven in CNX-368

CNX-368 traced the defect backward and proved the first broken component boundary:

**Host authority decision → plugin registration**

The active canonical Host controller uses schema v2 with:

- `schemaVersion: 2`
- `cnxMode: active|disabled|maintenance`

The pre-repair installed plugin authority gate accepted only schema v1 with a legacy `mode` field. For the canonical v2 controller it returned:

`authorized: false, reason: invalid`

and suppressed registration before the legacy registration chain reached the Ticket-first `before_agent_run` handler.

Because the plugin did not register the expected handler, native OpenClaw could continue directly to the configured OpenAI route. This explains the observed CNX-367 trajectory and is not merely an inference from missing logs: source call graph, canonical state contract, installed extension path, pre-repair authority predicate, and exact runtime trajectory jointly established the broken boundary. fileciteturn158file0

## CNX-368 repair

Production repair file:
`plugins/cogentnexus-openclaw/src/v091-release-entry.ts`

Regression test:
`plugins/cogentnexus-openclaw/src/cnx368-ticket-first-admission.test.ts`

Repair behavior:

- support a bounded controller schema set `{1,2}`;
- preserve strict fail-closed validation for unsupported or malformed schemas;
- for schema v2, translate canonical `cnxMode` to the legacy in-memory mode expected by the existing authority/registration chain;
- mappings:
  - `active → managed`
  - `disabled → passthrough`
  - `maintenance → maintenance`
- preserve the established schema v1 path;
- do not persist legacy mode back to controller state.

This repair changes the authority compatibility boundary only. It does not change provider ownership, authentication, routing, controller persistence, Ticket semantics, or the semantic test path itself. fileciteturn158file0

## CNX-368 TDD and validation evidence

Genuine RED:

- canonical v2 controller produced `authorized:false, reason:"invalid"` before repair;
- focused regression test exited with failure.

GREEN:

- `npx vitest run --config ./vitest.config.ts src/cnx368-ticket-first-admission.test.ts`
- `1 passed`
- exit code `0`

Full validation:

- `npm test`: `77` test files, `339` tests passed.
- `npm run plugin:build`: passed.
- TypeScript build and dist canonicalization passed.
- `npm run plugin:validate`: passed.
- Ticket DB bootstrap validation passed: 9 required tables + v0.9.5 registration fence.
- Package content verification passed.
- Repaired built entrypoint SHA-256:
  `04e12be2dc24a8f60c079031737c32bca5990251e8c219066a4413c31eab802`
- Repaired source SHA-256:
  `f033b4a588421da097d3db0f8247e741c1de5cf8782cadcbfb2db993840e6a9a`

There was an intermediate test-harness deficiency (`api.registerTool is not a function`) during test harness completion. It was fixed only in the test fixture using the existing Host authority registration surface; it was not a production failure and did not require production behavior changes. The final focused test passed. fileciteturn158file0

## Important distinction: source-repaired vs live-runtime-activated

CNX-368 explicitly stopped before runtime activation. The repaired artifact exists and is validated, but the task report states that no runtime restart, reinstall, controller edit, or live semantic request was performed and makes no claim that the live Gateway process had reloaded the repaired artifact. fileciteturn158file0

This distinction is the central reason CNX-369 exists.

Do not claim any of the following until CNX-369 proves them in the live process:

- repaired artifact is active in Gateway;
- `before_agent_run` is effectively registered in the live Gateway process;
- OpenAI Dashboard now follows Ticket-first admission;
- OpenAI runtime behavior is fixed.

## Previously established path-bound runtime identity

The CNX-365 path-bound preflight established the canonical live installation:

State root:
`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw`

Controller:
`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\host\controller.json`

Controller SHA-256 at that preflight:
`8d8b8bd2629325fdff33acbfa47277ab9cfde8ed32417525513d5fb151a05187`

Ownership manifest:
`C:\Users\CDQ-P\.openclaw\workspace\.openclaw\workspace\.cogentnexus-openclaw\ownership.json`

Ownership manifest SHA-256:
`25b83fc79dc48e10ad2451b43377f50282c4d0e8d777f9981f759d15cdc8cd88`

Launcher:
`C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd`

Launcher SHA-256:
`6f7962b2a431d346a22cb90397ed93cf289f732f4ba623234089149b12dcac16`

Installed plugin manifest:
`C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\package.json`

Installed plugin manifest SHA-256:
`3c3738f51eb82fc3c90ce658c5cd8bde295a6593f44f619d59f3c93f808fedd9`

Installed entrypoint:
`C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`

Previously recorded installed entrypoint SHA before CNX-369 activation:
`da8e810e88547ef866e2279fde86195f02557a9ca0a35a8771a0e646a1f6a7ef`

Expected repaired entrypoint SHA for CNX-369:
`04e12be2dc24a8f60c079031737c32bca5990251e8c219066a4413c31eab802`

The path-bound preflight also established the ownership manifest and launcher binding to the same state root and plugin path, plus an OpenClaw Gateway process context. fileciteturn157file0

## CNX-366 fresh Dashboard session proof

Before CNX-367, CNX-366 established a genuinely fresh blank Dashboard session manually through the Operator:

- session key:
  `agent:main:dashboard:83027933-3a42-4877-a79a-167caaa396a5`
- session UUID:
  `83027933-3a42-4877-a79a-167caaa396a5`
- Firefox/OpenClaw Control
- state:
  `Ready to chat`
- transcript: empty
- composer:
  `Message Assistant`
- composer was empty and Operator established focus manually;
- provider/model:
  `GPT-5.6 Luna · Medium`
- preparation Dashboard requests: `0`
- preparation OpenAI/model requests: `0`
- preparation runtime mutations: `0`

CNX-366 therefore removed the previous ambiguity about stale Dashboard conversations and unobservable composer focus. fileciteturn157file0

## Historical chronology

### CNX-356
Effective Admission Boundary Feasibility.

Classification: `UNRESOLVED/BLOCKED`.

Conclusion: supported runtime registry visibility was insufficient; no production change.

### CNX-357
OpenAI Dashboard Ticket-first requalification v2.

Fresh OpenAI Dashboard response was observed, but Ticket-first durable lineage was not observable. Classification remained `UNRESOLVED/BLOCKED` because the first divergence could not be proven.

### CNX-358
Exact OpenAI Dashboard admission trace.

Classification: `UNRESOLVED/BLOCKED`; earliest unobserved boundary was still `before_agent_run` dispatch/result.

### CNX-359
Admission trace instrumentation.

TDD RED exposed missing exported helper wiring; after repair, focused trace test, full plugin suite, build, and validation passed. Fresh Dashboard request still had no effective admission trace because candidate activation was not proven.

### CNX-360
Runtime activation verification.

Candidate package preparation succeeded, but supported installer stopped with:
`plugin generation rollover requires PASSTHROUGH mode; observed None`

Root cause of this installer failure was later established as a canonical mode-schema mismatch.

### CNX-361
Canonical rollover mode repair.

Root cause:
`CANONICAL_MODE_SCHEMA_MISMATCH_AT_ROLLOVER_BOUNDARY`

Bounded repair allowed canonical `cnxMode=disabled` to be interpreted as passthrough at the rollover checker without changing canonical persistence semantics.

### CNX-362
OpenAI semantic requalification attempt.

Blocked before Dashboard because live runtime controller identity did not match the expected canonical state from CNX-361: observed legacy schema v1 / passthrough state. No request or mutation was made.

### CNX-363
Runtime identity reconciliation.

Blocked. Historical controller-path identity was still not proven; no runtime change.

### CNX-364
Path-bound runtime provenance.

Blocked historically because CNX-361/CNX-362 physical controller-path continuity was not proven. Current canonical root was later identified without normalization.

### CNX-365
Path-bound controlled requalification.

First preparation subtask passed and proved exact current path-bound identities.
A semantic attempt then stopped as `UNRESOLVED/BLOCKED` because a fresh blank session could not initially be proven.
CNX-366 resolved that preparation blocker.

### CNX-366
Dashboard Fresh Session Establishment.

Status: `PREPARED`.
Established exact fresh Dashboard session, blank transcript, empty composer, independently observable composer target, Operator-established focus, and provider/model identity with zero requests and zero runtime mutation. Semantic execution required separate authorization.

### CNX-367
OpenAI Dashboard Ticket-first semantic requalification.

Classification: `CURRENT_RED`.
One exact request from the verified fresh session reproduced the bypass:
`prompt.submitted → model.completed → session.ended`
with no `before_agent_run`, no admission trace, no durable Ticket, no Ticket-first lifecycle, and no Ticket-linked delivery evidence.
No repair or runtime mutation was performed in CNX-367.

### CNX-368
Ticket-first admission root-cause repair.

Classification:
`REPAIRED / VERIFIED — live semantic requalification remains unauthorized.`
Proven root cause:
Host authority gate recognized only schema v1 while canonical runtime state is schema v2.
Minimal schema-v2 compatibility repair implemented and verified with TDD + full tests/build/validation.
No runtime activation or live request was performed.

### CNX-369
Current task.

Purpose: activate the repaired artifact in the exact live Gateway process and prove effective registration before any semantic requalification.

## Current coordination state and hard fences

The current authority files identify CNX-369 as the current task and prohibit semantic requests during it. fileciteturn170file0 fileciteturn171file0

CNX-369 may:

- read current authority and runtime identity;
- verify installed artifact hashes;
- use the supported bounded activation/reload/install path if needed;
- inspect the resulting Gateway process and effective registration;
- publish a report.

CNX-369 must not:

- send Dashboard semantic requests;
- send OpenAI/model requests;
- retry CNX-367;
- create another reproduction test;
- manually normalize controller state;
- alter provider/auth/routing;
- change hooks/main source;
- change release/tag state;
- modify historical CNX-360 through CNX-368 records;
- force-push or rewrite history.

Any runtime lifecycle mutation needed solely for activation must be explicitly recorded. fileciteturn174file0

## Expected CNX-369 outcome

Success condition:
`RUNTIME_ACTIVATION_PROVEN`

This requires BOTH:

1. the active Gateway process is demonstrably using repaired entrypoint SHA
   `04e12be2dc24a8f60c079031737c32bca5990251e8c219066a4413c31eab802`;
2. the effective plugin registration path is proven, including the downstream `before_agent_run` registration.

A file existing on disk is insufficient.

Failure condition:
`UNRESOLVED/BLOCKED`

Use this if the active runtime cannot be proven to use the repaired entrypoint or activation cannot safely be completed.

## What must happen after CNX-369

If CNX-369 proves runtime activation, do NOT immediately send a semantic request in the same task.

First publish and verify the CNX-369 report remotely.

Then create/activate a separate successor semantic-requalification task.

That successor will perform exactly one fresh OpenAI Dashboard semantic request using the verified fresh-session pattern, with Operator manually performing the UI send and Hermes tracing:

`Dashboard input`
→ `before_agent_run`
→ `admission.trace.started`
→ `admission.trace.input`
→ `admission.trace.eligible`
→ `admission.trace.ticket-decision`
→ `admission.trace.ticket-persisted`
→ `Ticket`
→ `Run`
→ `Call/Inference`
→ `Result`
→ `Assistant Delivery`
→ `Outbox/Delivery completion`

PASS requires durable, correlated Ticket-first evidence through delivery. A visible `CNX365-DONE` response alone is insufficient.

## Operator workflow for the eventual semantic test

When the separate semantic test task is authorized:

- Operator performs Dashboard UI action manually.
- Use a genuinely blank fresh Dashboard session.
- Provider: `OpenAI`
- Model: `GPT-5.6 Luna`
- Send exactly once:
  `Reply exactly with CNX365-DONE.`
- Do not retry.
- Do not send a second message.
- Do not change provider/model.
- Do not create another session once the exact fresh session has been established.

Hermes is responsible for tracing the resulting session/run/trace/Ticket lifecycle. The Operator is responsible for the actual Dashboard UI action.

## Important caution about identifiers

CNX-366 and CNX-367 deliberately share the Dashboard session key/UUID because CNX-366 established the fresh session and CNX-367 used that already-proven fresh session for the semantic execution. This is not a contradiction.

The runtime OpenClaw session ID/traceId is different:
`7b1a5ad4-0560-4b19-ae4e-609f9492b2c5`

The run ID is:
`c3e88413-5199-4d0c-bfec-deb33e86928e`

Do not conflate the Dashboard UUID, runtime session ID/traceId, and Run ID.

## Historical stability requirements

The following are immutable historical evidence records and must not be rewritten:

- CNX-360
- CNX-361
- CNX-362
- CNX-363
- CNX-364
- CNX-365
- CNX-366
- CNX-367
- CNX-368

Any new state transition must be represented through the live authority files plus a new task/report, not by rewriting historical reports.

The published v0.9.5 tag/release remains untouched and must not be force-pushed or rewritten.

## Current known source files of interest

Primary repaired production source:
`plugins/cogentnexus-openclaw/src/v091-release-entry.ts`

Regression test:
`plugins/cogentnexus-openclaw/src/cnx368-ticket-first-admission.test.ts`

Ticket-first handler:
`plugins/cogentnexus-openclaw/src/index.ts`

Canonical Host state writer:
`skills/cogentnexus-openclaw/scripts/host_state_v095.py`

Installer:
`scripts/install.ps1`

Namespace ownership / rollover boundary:
`skills/cogentnexus-openclaw/scripts/namespace_ownership.py`

## Current repaired logic summary

Before repair, the authority gate effectively required:

`schemaVersion === 1` + legacy `mode`

After repair it accepts schema versions 1 and 2, derives a legacy in-memory mode for v2, and preserves fail-closed semantics for unsupported/malformed state.

For canonical v2:

`cnxMode=active → managed`
`cnxMode=disabled → passthrough`
`cnxMode=maintenance → maintenance`

The semantic goal is not to make schema v2 look like schema v1 on disk. The translation exists only at the compatibility boundary required by the existing registration logic.

## Required reading order for the next ChatGPT session

1. This handoff document.
2. Current remote `docs/operations/coordination/ACTIVE.md`.
3. Current remote `docs/operations/coordination/STATUS.md`.
4. Current CNX-369 task.
5. CNX-368 repair report.
6. CNX-367 semantic requalification report.
7. Only then inspect source/runtime details required by CNX-369.

Do not begin by rereading the entire historical chain unless a specific evidence question requires it.

## Verification note for this handoff

The current branch tip was queried directly from GitHub and verified as:
`71ff37a8536cd339548b0e4b3f9c2810858f54ff`

The current ACTIVE/STATUS/task files were read from the remote branch tip and all agree that CNX-369 is the current task. fileciteturn170file0 fileciteturn171file0 fileciteturn174file0

This handoff itself is a new documentation artifact and does not replace or rewrite any historical task/report evidence.
