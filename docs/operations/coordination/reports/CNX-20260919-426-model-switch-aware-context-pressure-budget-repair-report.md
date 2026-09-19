# CNX-20260919-426 — Model-Switch-Aware Context Pressure Budget Repair Report

## Final classification

`MODEL_SWITCH_CONTEXT_BUDGET_REPAIR_GREEN`

CNX-426 repaired the context-pressure authority boundary exposed by same-session OpenClaw provider/model switching.

The repair is installed on the accepted live OpenClaw `2026.9.4` host.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Parent: `CNX-20260919-425`
- Task-open commit: `9577a4e02fa423ef7d5a46074297f34fc7b3eb58`
- Core implementation commit: `e8418b8e7010c205b4e0496d6f41e8730c1f535e`
- Terminal-residue safety commit: `0a8759e190ef42f952f92bd5d095b4bfe25f9191`

## Live trigger evidence

Observed Dashboard session:

`agent:main:dashboard:7ce3cf7e-0ad6-4ed9-a17d-cf3b712954bb`

Physical session id:

`5dbf3919-2f66-4f99-8f02-7da1f08ff422`

The operator successfully switched providers/models inside this single session:

1. OpenAI / `gpt-5.6-luna` / Codex;
2. Ollama / `qwen3:1.7b` / OpenClaw runtime;
3. Ollama / `qwen3.8:27b` / OpenClaw runtime;
4. OpenAI / `gpt-5.6-sol` / Codex.

Provider/model ownership remained OpenClaw-owned throughout.

### False context-pressure block

Run:

`fd47fa35-8ff5-49cf-854c-fe0d076af784`

Ticket:

`CNXT-0fb9379f-815c-4ef3-b669-120067d56f0f`

The OpenClaw transcript stored a turn-local model snapshot:

- provider: `ollama`;
- model: `qwen3.8:27b`.

But CNX emitted `context_pressure_deferred` using:

- contextWindow: `32768`;
- projectedTokens: `28425`;
- softLimit: `22282`;
- hardLimit: `29491`;
- ratio: `0.867462158203125`;
- level: `soft`;
- source: `fresh-session-counter`.

The configured/discovered effective context window for `qwen3.8:27b` is `262144`.

Therefore the block was a stale-window false positive after a model switch.

## OpenClaw 2026.9.4 host contract

OpenClaw's typed `before_agent_run` context provides:

- `modelProviderId`;
- `modelId`;
- `contextTokenBudget`;
- `contextWindowSource`;
- `contextWindowReferenceTokens`.

The host contract defines `contextTokenBudget` as the resolved effective context-token budget after model/config/agent caps.

This is the correct turn-local authority during a same-session model switch.

`sessions.describe` remains useful for the fresh token counter and physical session identity, but its persisted model/window metadata may lag the current turn.

## TDD evidence

### Initial RED

Focused CNX-426 suite before the production repair:

- total: 3
- failed: 2
- passed: 1

Failures:

1. stale session window `32768` + current turn budget `262144` false-blocked;
2. stale session window `262144` + current turn budget `40960` false-passed.

Control:

- absent/invalid turn budget preserved legacy session-window behavior.

This proved the defect was authority ordering, not merely one incorrect constant.

### Continuation RED

After repairing admission, two additional tests exposed downstream stale-window use:

1. passive compaction observer accepted stale session `262144` instead of stored turn `40960` and released a hold incorrectly;
2. context maintenance worker accepted compaction at `38000` tokens against stale `262144` instead of continuing protection against stored `40960`.

Both failed before their production repairs.

### Terminal-residue RED

Live inspection found the false-block Ticket was already terminal, while its context-maintenance row remained pending.

A dedicated test proved the pre-repair worker still made two Gateway calls for this terminal Ticket.

RED:

- expected Gateway maintenance calls: `0`;
- observed: `2`.

## Production repair

Changed:

- `plugins/cogentnexus-openclaw/src/v091-context-guard.ts`
- `plugins/cogentnexus-openclaw/src/v090-compaction-boundary.ts`

Added/expanded:

- `plugins/cogentnexus-openclaw/src/cnx426-context-budget-model-switch.test.ts`

### 1. Turn-local budget authority

At `before_agent_run`:

- valid finite positive `ctx.contextTokenBudget` becomes the exact context window for pressure evaluation;
- the fresh session counter can still provide `totalTokens`, `totalTokensFresh`, and session identity;
- no `max(old,new)` operation is used.

This is important in both directions:

- small → large model: prevents false blocking;
- large → small model: prevents false safety.

If the host does not provide a valid budget, the legacy session/default fallback remains intact.

### 2. Durable turn-window continuity

When context maintenance is authorized, the effective turn window is stored in:

`cnx_context_maintenance.context_window`

That stored window remains authoritative through:

- passive native compaction observation;
- background context maintenance;
- hard-trim target calculation;
- context capsule generation.

A later stale `sessions.describe.contextTokens` value cannot silently change the safety boundary for that hold.

### 3. Terminal Ticket fence

Context maintenance now cancels residue if the associated Ticket is no longer `accepted`.

The fence exists at three race boundaries:

- due-row reconciliation;
- maintenance claim;
- current authority re-check.

Terminal residue is completed as:

- state: `cancelled`;
- last_error: `ticket no longer accepted`;
- no Gateway compaction call.

## GREEN validation

### Focused CNX-426

Final:

`6/6 PASS`

Coverage:

1. 32K stale → 262K current turn does not false-block;
2. 262K stale → 40K current turn blocks correctly;
3. passive compaction preserves stored turn budget;
4. maintenance worker preserves stored turn budget;
5. terminal Ticket residue cancels without Gateway compaction;
6. invalid/absent turn budget preserves legacy fallback.

### Targeted regression

Final:

`67/67 PASS`

Included:

- CNX-426;
- v0.9 context guard;
- compaction boundary;
- passive compaction observer;
- v0.9.1 wiring;
- v0.9.1 direct recovery;
- direct recovery model-call fence;
- session ownership;
- CNX-422 reply_dispatch admission;
- CNX-423 provenance/ACP identity.

### Plugin validation

`npm run plugin:validate` — PASS

Evidence:

- TypeScript build PASS;
- 50 dist text files canonicalized;
- mixed-plugin artifact verification PASS;
- 46 config properties;
- 5 tools;
- Ticket DB bootstrap PASS;
- 9 required tables + v095 registration fence;
- package content verification PASS;
- packed file count: `266`.

### Full suite

Final:

- test files: `83 passed / 1 failed` out of `84`;
- tests: `376 passed / 1 failed` out of `377`.

The only failure is the historical predecessor RED:

`src/cnx383-hook-policy-projection.test.ts`

Assertion:

`expected undefined to be true`

No CNX-426 regression was introduced.

## Qualified candidate

Exact source HEAD:

`0a8759e190ef42f952f92bd5d095b4bfe25f9191`

Candidate package:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\candidates\CNX-20260919-426-0a8759e1\openclaw-plugin-cogentnexus-openclaw-0.9.5.tgz`

SHA256:

`3672D995B1D8A9C3ED22037D27259EBAE9F71A2294283BD8D642FD42E4D04360`

Candidate implementation hashes:

- `dist/v091-context-guard.js`
  `0B47511C9290B341D300F56505F341103FA7778D9C3D6DF463D354C6A709D6B9`
- `dist/v090-compaction-boundary.js`
  `18344C79E82C8E8C2D3709CCD4FFC9D5A294EEB14FC7F45732008836A8975C55`

`dist/v091-release-entry.js` itself did not change because it is an import boundary rather than a bundle of the modified modules.

## Live install-over

Before install:

- live Gateway healthy;
- Gateway PID `27576`;
- sessions `23`;
- Discord connected;
- Supervisor last result `0`;
- the false-block maintenance row was still `pending`;
- target physical session id `5dbf3919-2f66-4f99-8f02-7da1f08ff422`;
- target transcript maxSeq `47`, event count `48`.

A pre-install live-plugin copy was retained at:

`C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\candidates\CNX-20260919-426-0a8759e1\pre-install-live-plugin`

The CNX supervisor was disabled and the Gateway was explicitly stopped with:

`openclaw gateway stop --force`

Port `18789` was confirmed closed before install.

The exact candidate archive was installed with explicit capability/policy acknowledgement.

Install result:

- exit `0`;
- source change scheduled for next Gateway start.

Before starting the Gateway, live installed implementation hashes matched the candidate exactly.

## Live terminal-residue qualification

Immediately before Gateway start, the historical false-block row was still:

- Ticket: `CNXT-0fb9379f-815c-4ef3-b669-120067d56f0f`;
- state: `pending`;
- context_window: `32768`;
- projected_tokens: `28425`;
- attempt_count: `0`;
- completed_at: null.

The associated Ticket was already `failed`.

After the new plugin started:

- state: `cancelled`;
- last_error: `ticket no longer accepted`;
- attempt_count: `0`;
- completed_at: `2026-09-19T06:01:46.098Z`.

No compaction occurred:

- physical session id remained exactly `5dbf3919-2f66-4f99-8f02-7da1f08ff422`;
- transcript remained exactly maxSeq `47`, event count `48`;
- no post-start compaction log matched this session/Ticket.

This proves the installed terminal fence cleaned the stale row without touching the conversation.

## Non-semantic installed-artifact context-budget qualification

No provider semantic message was generated for CNX-426 qualification.

The installed live plugin modules were imported directly into an isolated temporary SQLite harness.

Results:

### Upswitch

Input:

- stale described window: `32768`;
- total tokens: `28425`;
- current turn budget: `262144`;
- model: `qwen3.8:27b`.

Installed artifact result:

`outcome=pass`

Observed context authority:

`262144`

### Downswitch

Input:

- stale described window: `262144`;
- total tokens: `38000`;
- current turn budget: `40960`;
- model: `qwen3:1.7b`.

Installed artifact result:

`outcome=block`

Observed pressure:

- contextWindow: `40960`;
- projectedTokens: `38002`;
- softLimit: `30310`;
- hardLimit: `36864`;
- ratio: `0.927783203125`;
- level: `hard`.

The temporary maintenance row stored:

`context_window=40960`

Probe result:

`pass=true`

## Final live state

After Supervisor restoration:

- OpenClaw: `2026.9.4`;
- Gateway health: `ok=true`;
- Gateway PID: `27760`;
- sessions: `23`;
- plugin errors: `0`;
- Discord connected: true;
- CNX Supervisor: enabled/Ready;
- Supervisor last task result: `0`.

Runtime attestation:

- `runnerReady=true`;
- `globalHookCount=7`;
- `latestRegistryPluginHookCount=null`;
- classification: `AMBIGUOUS`.

The attestation classification remains the previously accepted conservative OpenClaw 2026.9.4 public-SDK limitation.

SQLite integrity:

- shared state DB: user_version `17`, quick_check `ok`;
- agent DB: user_version `19`, quick_check `ok`;
- CNX DB: quick_check `ok`.

Final live implementation hashes match the candidate exactly.

No new semantic Ticket was created by CNX-426 install/qualification. The latest live Ticket remains the operator's prior completed Dashboard turn:

`CNXT-485c4ef3-bb0d-4383-a3f7-f1103016bb64`

## Residual external dependency

Tailscale remains a separate known degraded dependency from CNX-425:

- external daemon backend remains `NoState`;
- OpenClaw managed Tailscale exposure remains `off`;
- local loopback Gateway remains healthy.

CNX-426 did not alter this state.

## Final decision

`MODEL_SWITCH_CONTEXT_BUDGET_REPAIR_GREEN`

The false model-switch context-pressure block is repaired.

CogentNexus now uses the OpenClaw-resolved effective turn budget at admission, preserves that exact budget through context-maintenance lifecycle, and refuses to maintain context for terminal Tickets.

Provider/model selection remains owned by OpenClaw.
