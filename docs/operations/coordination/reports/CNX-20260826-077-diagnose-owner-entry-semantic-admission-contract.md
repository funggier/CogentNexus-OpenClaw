# CNX-20260826-077 — Comprehensive Semantic-Path Audit

Result: `PASS_OWNER_ENTRY_COVERAGE_REPAIRED`

## Scope and authorization

This report executes both Task 077 documents as one contract:

- `CNX-20260826-077-diagnose-owner-entry-semantic-admission-contract.md`
- `CNX-20260826-077-comprehensive-semantic-path-audit-addendum.md`

Execution mode: `SOURCE_COMPREHENSIVE_SEMANTIC_PATH_DIAGNOSTIC_TDD`
Authorization: `COMPREHENSIVE_SEMANTIC_PATH_DIAGNOSIS_AND_PROVEN_BLOCKER_REPAIR_AUTHORIZED`

All work was performed in a fresh isolated worktree. No new semantic message, no direct Ollama semantic call, no live install/config/provider/plugin/AGENTS change, no live Ticket/session/SQLite mutation, no restart, merge, tag, or release was performed.

## Identity and evidence

- Repository: `funggier/CogentNexus-OpenClaw`
- Coordination branch: `agent/v0.9.3-recovery-reality-tests`
- Accepted source baseline: `79b51ed06363f6e8862c491ee0a313ddb412c806`
- Execution HEAD before test-only change: `e7348334e0a8536ecb73f6929e8ed9dc6763e73a`
- Isolated worktree: `C:\Users\CDQ-P\AppData\Local\Temp\cnx077-preflight-20260826T144315Z\worktree`
- Evidence directory: `C:\Users\CDQ-P\AppData\Local\Temp\cnx077-preflight-20260826T144315Z`
- Installed OpenClaw: `2026.7.1-2`
- Installed CogentNexus plugin: `0.9.3`
- Task 076 accepted blocker: `BLOCKED_SEMANTIC_ENTRY_PATH`
- Task 076 run (not repeated): `97b7e136-3258-415b-a595-02792d393ff9`

## Executive finding

Task 076 selected `openclaw agent --session-key agent:main:main`. In installed OpenClaw `2026.7.1-2`, selecting an owner-looking session key does not itself confer owner trust. The Gateway agent path derives `senderIsOwner` from the connecting client's `ADMIN_SCOPE`; the CLI path is not an authenticated Dashboard/WebChat control-UI client. The CogentNexus admission gate therefore correctly rejects that surface for durable Ticket creation, while normal inference can proceed on the non-owner path. This explains the accepted Task-076 zero-Ticket/provider-timeout result without weakening security.

The plugin source/live artifact identity is sound. The primary gap was executable coverage at the registered production hook boundary for direct trusted owner metadata and explicit negative CLI/subagent metadata. Two focused tests were added; no production implementation was changed.

The adjacent provider risk remains: Task 076 spent approximately 245.7 seconds in two provider-stage idle-watchdog attempts before timing out. This is not repaired here because the hard fence forbids timeout/model/provider mutation. It is carried forward as an explicit successor gate: the next semantic acceptance must use a proven effective timeout/model combination or a separately authorized timeout design change.

## Comprehensive boundary finding matrix

| Boundary | Exact production path | Evidence | Status | Severity | Next action |
| --- | --- | --- | --- | --- | --- |
| A. owner surface: CLI | OpenClaw Gateway agent handling in `dist/agent-D6kiZtPt.js`; `clientHasAdminScope(client)` checks only `connect.scopes` for `ADMIN_SCOPE`, and the agent request passes `senderIsOwner: clientHasAdminScope(client)` around line 2352 | Installed source read; Task-076 run targeted `openclaw agent --session-key agent:main:main` and reached Ollama with zero Tickets | Correctly non-owner for this surface; inference bypass is expected policy behavior | P1 | Successor must use a proven authenticated owner surface, not CLI session-key targeting |
| A. owner surface: Dashboard/WebChat | `dist/chat-pg-BxhF6.js`; `hasGatewayAdminScope(client)` uses the same authenticated admin-scope invariant; `chat.send` routes into the normal agent lifecycle | Installed source read around `hasGatewayAdminScope`; plugin test fixture uses `agent:main:dashboard:acceptance` | Supported owner candidate; no channel-trigger-name dependency | INFO | Independent review should approve the exact control-UI surface before live use |
| A. channel/direct-message surface | Channel ingress and sender authorization are handled by OpenClaw channel adapters before the shared agent lifecycle; session-key shape alone is not sufficient | No live channel mutation allowed; plugin policy rejects non-owner metadata unless exact Dashboard fallback invariant applies | Not proven for a configured Discord owner path in this build | P1 | Do not use as next surface until source/runtime auth metadata is captured |
| A. scheduled/internal continuation | OpenClaw continuation/recovery messages carry internal markers/session context; CogentNexus `ticketIntakeEligible()` excludes continuation and workflow-result markers | `src/ticket-store.ts` `ticketIntakeEligible`; existing `v090-*`, recovery and compaction tests | Correctly excluded from fresh owner admission | INFO | Retain negative coverage |
| B. plugin generation/loading | Installed `openclaw plugins info cogentnexus-openclaw` reports loaded v0.9.3 from canonical `~/.openclaw/npm/projects/...g-5593.../node_modules/.../dist/v091-release-entry.js`; enabled global npm pack | Plugin info/list output saved in `b05-plugin-runtime-selection.txt`; source/live hashes match in `b06-plugin-identity.txt` | Canonical artifact loaded; no stale-copy drift found | INFO | No live repair |
| B. hook registration | Installed `v091-release-entry.js` calls `legacyEntry.register(api)` only after Host authority; `v091-final-entry.js` contains `api.on("before_agent_run")`, `session_end`, `reply_dispatch`, `message_sent`, `after_compaction`, `agent_end` | Installed entry source read; clone `src/index.ts` hook registrations at lines 727, 800, 810, 830, 844, 853; byte-for-byte dist identity verified | Runtime registration is conditional on Host `mode=managed`; `plugins list` static `hookCount: 0` is metadata introspection, not evidence that dynamic registration failed | INFO | No source/live change |
| C. admission gate | `src/index.ts` `before_agent_run` handler calls `durableAdmissionEligible`, `classifyDurableRequest`, then `TicketStore.accept` for eligible owner requests | Existing admission tests plus new registered-hook tests | Eligible trusted owner request commits before normal continuation; untrusted CLI/subagent gets pass without Ticket | PASS | Keep exact metadata fixtures |
| C. bypass: missing/unsupported session | `durableAdmissionEligible` rejects unsupported owner identity; no session-key pattern grants trust | `src/index.test.ts` owner eligibility matrix; negative registered-hook test | Fail-closed for CLI/subagent | INFO | No change |
| C. bypass: sender signal | `senderIsOwner` false is allowed only through exact Dashboard fallback logic; CLI and subagent namespaces remain rejected | Existing lines 38–44 tests plus new hook-level negative test | Security-preserving behavior proven | PASS | Next live run must carry authenticated Dashboard metadata |
| C. bypass: config gate | `ticketFirst` and `preInferenceAdmission` gate hook installation/behavior | `src/index.ts`; plugin config and wiring tests | Configuration behavior covered; no live config changed | INFO | No change |
| C. bypass: store/open failure | Ticket acceptance uses durable SQLite operations; tests cover bootstrap and store behavior | TicketStore tests; `plugin:validate` DB bootstrap PASS | No fail-open repair proven necessary in this pass | P2 | Review any future store-error finding separately |
| C. deduplication | Ticket acceptance/request identity and active-request fingerprint prevent duplicate durable work | `src/index.test.ts` deduplication test; TicketStore tests | Existing dedup behavior green | INFO | No change |
| D. trusted owner integration | Registered `before_agent_run` fixture with exact owner session metadata, `senderIsOwner:true`, and isolated SQLite | New test: `admits a direct owner turn at the registered hook before provider continuation` | Exactly one accepted direct Ticket, `workflow_eligible=0`, events `accepted -> routed`; provider continuation is represented only after durable hook return | PASS | Included in implementation/test commit |
| D. untrusted integration | Registered hook with `agent:main:cli:*` and `agent:main:subagent:*`, `senderIsOwner:false` | New test: `rejects untrusted CLI and subagent metadata at the registered hook` | Zero Tickets; no owner impersonation | PASS | Included in implementation/test commit |
| E. direct lifecycle | `reply_dispatch`/`message_sent` handlers in `src/index.ts`; direct response boundary in `v093-response-ready-boundary.test.ts`; delivery tests in `v090-dashboard-delivery.test.ts` and `v091-dashboard-verified-delivery.test.ts` | Full plugin suite includes response-ready, direct delivery, outbox and duplicate-delivery tests | Accepted/routed/direct-result/delivery and idempotency behavior covered by deterministic fixtures; no live semantic delivery claimed | PASS | Independent review should confirm coverage sufficiency |
| F. provider timeout hierarchy | OpenClaw `dist/selection-JInn13lc.js` defines `DEFAULT_LLM_IDLE_TIMEOUT_MS = 12e4`; `dist/embedded-agent-DGUuxGR2.js` emits idle-watchdog retry; `dist/agent-via-gateway-_KoeINns.js` derives Gateway timeout from run timeout; user-facing error names `models.providers.<id>.timeoutSeconds` and `agents.defaults.timeoutSeconds` ceilings | Source scan saved as `b04-timeout-source.txt`; Task-076 correlated evidence recorded two ~120 s idle attempts, total ~245.7 s; read-only `ollama ps` showed qwen3.5:9b loaded | Provider-stage no-token idle timeout is a credible next-run blocker independent of owner-entry correction; exact effective configured provider timeout was not exposed by queried config paths | P1 carried forward | Successor must resolve/read-only prove effective timeout/model readiness, then obtain explicit config/provider authorization if change is required |
| G. provider failure/recovery | Ticket remains durable; recovery and direct model-call lease boundaries prevent direct-result regeneration and distinguish pending delivery from completed | `v094-direct-recovery.test.ts`, `v095-direct-recovery.test.ts`, `v096-direct-recovery.test.ts`, `v097-direct-recovery-liveness.test.ts`, `v098-owner-reconcile-residue.test.ts`, `v099-native-restart-ownership.test.ts` | No duplicate Ticket/recovery regression found; full tests green | INFO | No change |
| G. delivery failure/idempotency | Ticket outbox and direct delivery mark attempts/errors and converge on receipt | `ticket-store.test.ts`, `ticket-runtime.test.ts`, `delivery-continuity.test.ts`, dashboard verified-delivery tests | Pending/failed delivery remains distinguishable from completed; duplicate callbacks guarded | INFO | No change |
| H. security invariants | Admission policy combines session namespace, sender signal, authenticated Dashboard fallback, continuation exclusion and dedup identity | Existing eligibility tests plus new registered-hook negative test; source review of OpenClaw scope derivation | Arbitrary owner-looking CLI key, subagent, and false sender metadata cannot obtain owner Ticket admission | PASS | Preserve least privilege |
| I. adjacent blockers | Provider timeout is outside safe source-only repair and live fence; no independently proven production semantic defect required a production-code change | `b03-timeout-health.txt`, `b04-timeout-source.txt`, full validation | One P1 operational semantic-acceptance risk explicitly carried; no unresolved P0 | P1 carried forward | Create successor gate for effective timeout/model or use a proven fast provider path |

## Source-only TDD change

Only one test file changed in the isolated worktree:

`plugins/cogentnexus-openclaw/src/index.test.ts`

Added focused registered-hook coverage for:

1. trusted Dashboard/WebChat-shaped owner metadata creating exactly one direct Ticket before provider continuation;
2. untrusted CLI and subagent metadata creating zero Tickets.

RED/GREEN record:

- Initial test implementation exposed a test-fixture issue (`tickets` table is intentionally absent when a rejected request never opens TicketStore); no product defect was inferred.
- Fixture corrected to initialize/read the store through `TicketStore.snapshot()`.
- Final focused tests pass.
- No production `.ts` implementation file changed.

Implementation/test commit: `6867af2` (`test: cover registered owner admission boundary`)

## Verification

### Plugin / Node compatibility paths

- npm 12.0.2 / Node 22.23.2: `npm ci`, plugin test and validation passed before the final test-only change; the final test suite was rerun on the npm 12 path and passed.
- npm 11.16.0 / Node 24.18.0: `npm ci` passed; final `npm test` passed: **49 test files, 239 tests**; `npm run plugin:validate` passed.
- Plugin validation: mixed-plugin artifact verification PASS (45 config properties, 5 tools).
- Ticket DB bootstrap: PASS (9 required tables plus v0.9.5 registration fence).
- Package contents: PASS; `openclaw-plugin-cogentnexus-openclaw-0.9.3.tgz`, 176 packed files, required entry/artifact files present.

### Repository verification

- Full Python suite via `uv run --with 'pytest>=8,<10' --with 'PyYAML>=6,<7' python -m pytest tests/ -q`: **356 passed, 2 skipped, 4 subtests passed**.
- `python scripts/check_baseline_consistency.py`: **PASS (Bridge v0.9.3)**.
- `git diff --check`: PASS.
- Final source diff reviewed: test-only, no unrelated changes.
- Worktree was clean after the implementation/test commit before report creation; report publication is the only remaining tracked change.

## Live hard-fence accounting

Counts in Task 077:

- semantic messages: 0
- direct Ollama semantic calls: 0
- live Ticket/session/SQLite mutations: 0
- install/install-over/uninstall/reset/cleanup: 0
- provider/model/config/plugin/AGENTS changes: 0
- restart/reboot/process termination for diagnosis: 0
- merge/tag/release: 0

The Task-076 semantic send and nonce were not reused.

## P0/P1 disposition and successor gate

- **P0:** none found.
- **P1 owner-entry coverage:** repaired at the registered production hook boundary with focused tests; no production policy broadening was made.
- **P1 provider timeout:** explicitly carried forward. The Task-076 Ollama no-token idle watchdog remains capable of making a future semantic attempt fail after entry is corrected. No safe source-only change or live timeout/provider mutation was authorized in Task 077. The successor must first prove the effective timeout/model path and obtain a separately authorized configuration/provider remedy or choose a proven bounded provider path.

This report does not authorize a new live semantic message. Independent review remains required before successor authorization.
