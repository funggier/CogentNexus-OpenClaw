# CNX-20260830-164 — Hermes Native Transcript Authority RED-to-GREEN Repair

## Disposition

`PASS`

The inherited production-faithful RED was preserved, the smallest CogentNexus production repair was implemented, targeted and full repository validation passed on the exact repair SHA, and all required push-triggered GitHub workflows passed. No prohibited live action occurred. ChatGPT review is required before any successor authorization.

## Coordination authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Exact starting HEAD: `3c286145633532c37fdc753118a783d4899c5814`
- Fresh remote preflight: `git ls-remote` matched the isolated clone HEAD at the starting SHA.
- Active/Status gate: `READY_HERMES`, Task `CNX-20260830-164`
- Evidence root: `C:\Users\CDQ-P\AppData\Local\Temp\cnx164-hermes-20260830T162111Z\`
- Exact pinned upstream OpenClaw: `v2026.7.1-2`, commit `0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c`

## Inherited RED verification

The existing test-only RED checkpoint was an ancestor of the starting HEAD:

- RED commit: `61218ca6cc13a5c0312829abd72bcdb524944d12`
- Regression: `plugins/cogentnexus-openclaw/src/v162-dashboard-transcript-authority.test.ts`
- First expected failure: `beforeAgentFinalize` was undefined at the assertion requiring production wiring.
- Command: `npm test -- --run src/v162-dashboard-transcript-authority.test.ts`
- Observed result: 1 test failed with `expected undefined to be type of 'function'`.
- Earlier setup correction: the first invocation from repository root produced `Missing script: test`; the valid rerun from the plugin directory produced the expected RED. This was retained as harness evidence and not treated as a product result.

## Exact upstream source evidence

A fresh read-only clone of `openclaw/openclaw` was fetched and detached at the exact pinned commit. Captured evidence files and SHA-256:

- `a04-upstream-head.txt`: `462c410609210d71375856740b4e42d74dde6534eb5420ae8d8a6c78415c99cc`
- `a05-upstream-session-tool-result-guard-wrapper.ts`: `fbb62b4258ff1bc60f20d6f9cb314b00bc2cd56fd57a55fd9cb95118b3884b4a`
- `a05-upstream-session-tool-result-guard.ts`: `54f90dd38604addfcc9ccc2d79cb075c35658884a861e510d323722c5e939800`
- `a05-upstream-runtime-events.ts`: `0ef1c251a11a8909653a151d382aa332c58e19f048cc131f0552eb87760531cf`
- `a05-upstream-types-core.ts`: `a1e6e34971fd3bfbbb28556447684499d9e5ad6642f6940a5019153a2f0c231a`
- `a05-upstream-transcript-events.ts`: `a2d6dda6e39b96ff951dc0615b13f888a57a5cec7851782be03009bf472012d9`
- `a05-upstream-chat.ts`: `fc917d37687c9f819731479206a5954f07e5b1fbdf3ecc759c2d920b35e28f04`

Relevant source facts:

1. `session-tool-result-guard-wrapper.ts` wires the global `before_message_write` hook into the SessionManager guard.
2. `session-tool-result-guard.ts` applies that hook before `originalAppend(...)`, then emits `emitSessionTranscriptUpdate(...)` only after the append returns, carrying the persisted message, message identity, sequence, and session fields.
3. `runtime-events.ts` exposes `onSessionTranscriptUpdate`; `types-core.ts` includes it in `PluginRuntimeCore.events`.
4. The embedded runner's `before_agent_finalize` event supplies `runId`, `sessionId`, `sessionKey`, `lastAssistantMessage`, and projected messages on the post-model terminal path.

## Repair

Implementation commit:

- `80b87dfbe0d9176e421f3748b4cee0827db12d0c`
- Message: `fix: bind dashboard delivery to native transcript receipt`

Changed files in the implementation commit (exactly task-authorized scope):

- `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`
  - captures the exact post-model Dashboard assistant candidate;
  - stages the durable `direct_result` and marker from `before_message_write`;
  - establishes a bounded durable native-write claim before native append;
  - subscribes to `api.runtime.events.onSessionTranscriptUpdate`;
  - settles only when the marker-bearing assistant transcript update is observed after native append;
  - clears claim fields on terminal settlement;
  - prevents legacy recovery from claiming an active in-process native owner.
- `plugins/cogentnexus-openclaw/src/v162-dashboard-transcript-authority.test.ts`
  - no assertions or RED contract were weakened;
  - Windows SQLite fixture cleanup is best-effort only because the test process can release a handle after assertions complete.

The repair does not patch OpenClaw, change dependencies, add a second inference path, or treat transport callbacks as persistence authority.

## Crash-window and duplicate-safety argument

- Before `before_message_write`: no marker or durable direct-result claim exists; no native delivery success is reported.
- After durable staging and before native append: the pending row has a non-expired native claim, and the recovery wrapper refuses to delegate to legacy recovery; no `chat.inject` or second inference is permitted.
- After `originalAppend` and before transcript-event handling: the marker-bearing native message is authoritative evidence in the event path, while the durable claim still blocks recovery.
- After transcript event handling: settlement transaction changes the Ticket to `completed`, changes the delivery row to `delivered`, clears the claim, and writes exactly one `delivery_confirmed` event. A duplicate event finds no pending row and cannot create another confirmation.
- If the process loses the in-memory candidate before the event, the implementation fails closed; it does not inject or regenerate. The durable pending row remains available to the existing owned delivery boundary rather than authorizing a speculative duplicate.

## Validation evidence

Local exact-repair validation:

- Targeted Task-164 regression: `1 passed`
- Full CogentNexus-OpenClaw plugin suite: `52 test files, 272 tests passed`
- `npm run build`: PASS
- `npm run plugin:validate`: PASS
  - schema verification PASS
  - ticket DB bootstrap PASS (`9 required tables + v095 registration fence`)
  - package verification PASS (`182` packed files)
- `python scripts/check_baseline_consistency.py`: PASS
- Existing v091 delivery regression: `11 tests passed`

The initial `npm ci --ignore-scripts` reported 4 high-severity advisories in the existing dependency graph. No dependency upgrade or `npm audit fix` was run because the task explicitly forbids dependency upgrades. Repository Validate/package CI passed on the repair SHA.

Required GitHub Actions, all on exact HEAD `80b87dfbe0d9176e421f3748b4cee0827db12d0c`:

- Validate run `33322815641`: `SUCCESS`; 7/7 jobs completed successfully, including Ubuntu/Windows/macOS Python matrix and package dry-run.
- Windows Installer Pack Smoke run `33322815634`: `SUCCESS`; `npm-pack` job successful.
- PS5.1 Acceptance Smoke run `33322815695`: `SUCCESS`; `serializer` job successful.

The workflows were push-triggered. Manual dispatch was attempted only to discover the workflow contract and returned GitHub HTTP 422 because these workflows do not declare `workflow_dispatch`; no duplicate run or product mutation resulted.

## Publication and exact final state

After implementation validation, remote branch HEAD was rechecked and matched the implementation commit before report creation. The matching report was absent at that point.

This report is the only file in the report publication commit. The report commit SHA and remote blob must be verified after push.

## Hard-fence compliance

No Dashboard semantic Send or semantic UI interaction; no real Windows install-over/uninstall/reinstall/reset; no Gateway/Ollama/Supervisor/OpenClaw runtime mutation; no manual live Ticket/workflow/result/outbox/delivery/database mutation; no arbitrary live-state deletion; no OpenClaw source patch; no dependency upgrade; no release/tag/package publication; no merge to default/release branch; and no force push.

## Recommended next action

ChatGPT should review this report, the exact diff, the inherited RED evidence, upstream source evidence, and the three exact-SHA CI runs. Do not authorize a Dashboard Send or live Windows mutation until a separate repaired-candidate install-over plus provenance/health checkpoint is explicitly opened and accepted.
