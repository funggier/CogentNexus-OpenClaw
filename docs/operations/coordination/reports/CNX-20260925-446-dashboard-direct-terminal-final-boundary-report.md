# CNX-20260925-446 — Dashboard Direct Terminal-Final Boundary Repair Report

Status: `LIVE_GREEN_INSTALLER_TIMEOUT_REPAIR_LOCAL_GREEN_COMMIT_PENDING`

Task: `CNX-20260925-446-dashboard-direct-terminal-final-boundary.md`

Target release line: `v0.9.8`

Working branch: `cnx-446-dashboard-direct-terminal-final-boundary`

## Production trigger

A real OpenClaw 2026.9.5 Dashboard run proved that CogentNexus-OpenClaw could close a Direct Ticket from a visible assistant progress/commentary message while the exact run was still active.

Exact production identity:

- Dashboard session key: `agent:main:dashboard:6090e8c3-88fc-420d-8ee8-1f498b9146f6`
- OpenClaw session id: `3dfbe4db-db86-4b07-9f89-6dc3757c07d9`
- run id: `63bb6787-a016-426b-9ba0-d84ac15ff555`
- Ticket: `CNXT-f191f552-305a-4950-a77c-1dfd3444d253`
- provider/model: `openai/gpt-5.6-luna`

The Ticket-first boundary itself was healthy:

- `accepted`: approximately `2026-09-25T08:11:06.317Z`
- `ingress_persisted`: same admission boundary
- exact ingress run binding: `2026-09-25T08:11:06.332Z`
- Direct route: `workflow_eligible=0`
- OpenClaw run start: approximately `2026-09-25T08:11:11.106Z`

The defect occurred downstream at final-result selection.

## Early-completion evidence

The first visible assistant message was a progress/commentary message stating that the agent would inspect the installed workspace before producing the architecture explanation.

That message was persisted at approximately:

`2026-09-25T08:11:16.592Z`

CNX nevertheless recorded:

- `response_ready`: `2026-09-25T08:11:16.587Z`
- `direct_response_durable`: `2026-09-25T08:11:16.587Z`
- `delivery_confirmed`: `2026-09-25T08:11:16.595Z`
- `completed`: `2026-09-25T08:11:16.595Z`

The stored durable payload SHA-256 was:

`c35a26869150ac903c207a1cb9eb87a3d95a52aa6e06ac138cb3c1d8ff3f3ff6`

Direct hashing proved that this digest matched the first progress/commentary text after removing the CNX delivery marker. It did not match the true final response.

After the Ticket was already `completed`, OpenClaw continued tool execution until:

- true final assistant message: approximately `2026-09-25T08:13:07.217Z`
- `model.completed`: `2026-09-25T08:13:07.244Z`
- `session.ended=success`: `2026-09-25T08:13:07.249Z`

Therefore the durable Ticket terminal state preceded actual run termination by approximately 110.65 seconds.

## Internal terminal-authority finding

The operator observed that the Dashboard exposes a Stop control while a run is still active. Rather than bind CNX to UI state, the investigation traced the underlying message/run metadata.

Both the false progress message and the real final message had:

`stopReason="stop"`

Therefore `stopReason` is not sufficient terminal authority.

The false progress message had:

- `__openclaw.runId=63bb6787-a016-426b-9ba0-d84ac15ff555`
- `__openclaw.mirrorOrigin="codex-app-server"`
- no `__openclaw.runTerminal`

The true final message had:

- the same exact run id
- the same mirror origin
- `__openclaw.runTerminal=true`

Inspection of recent OpenClaw transcript evidence also showed that native Ollama terminal messages on the same OpenClaw 2026.9.5 runtime do not carry `__openclaw.runTerminal`.

Therefore the repair cannot globally require `runTerminal`. The signal is used only for the Codex/App-Server mirrored fallback that exposed the defect.

## Root cause

The fallback in:

`plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`

allowed `before_message_write` to stage the current assistant text whenever exactly one accepted Dashboard Direct Ticket existed for the session and no prior `before_agent_finalize` candidate had been established.

The fallback proved session ownership but did not prove terminality or exact run ownership.

A non-terminal mirrored progress write could therefore become:

`assistant progress -> durable result -> delivery marker -> transcript settlement -> Ticket completed`

while the exact OpenClaw run continued.

## RED evidence

A production-topology regression was added:

`plugins/cogentnexus-openclaw/src/cnx446-dashboard-terminal-final-boundary.test.ts`

Before the repair:

- test files: 1
- tests: 4
- result: 2 failed / 2 passed

The two RED failures proved:

1. a Codex/App-Server mirrored progress message with exact run id, `stopReason="stop"`, and no `runTerminal` was incorrectly given a CNX delivery marker;
2. a mirrored terminal message carrying a different run id could incorrectly capture the session's accepted Ticket.

The already-correct controls passed:

- exact mirrored terminal fallback could settle a result;
- native fallback without mirror terminal metadata remained operational.

## Repair

Production source change:

`plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`

The repair adds a narrow Codex mirror authority classifier:

- recognizes only `mirrorOrigin="codex-app-server"`;
- extracts exact `__openclaw.runId`;
- accepts `__openclaw.runTerminal === true` as strong terminal evidence for that mirrored fallback.

The `before_message_write` fallback now behaves as follows:

1. if `before_agent_finalize` already established the exact final candidate, preserve the existing proven path;
2. otherwise, Discord still does not use the Dashboard fallback;
3. if the message is a Codex/App-Server mirror:
   - require `runTerminal=true`;
   - require an exact run id;
   - resolve the accepted Direct Ticket by exact run id;
   - require exact owner-session match;
4. if the message is not a Codex/App-Server mirror, preserve the existing native/legacy fallback, including Ollama;
5. if mirrored run identity is present but conflicts with the established candidate run, refuse staging.

No provider/model/auth routing behavior changed.

## GREEN evidence

Focused CNX-446 regression after repair:

- 1 file PASS
- 4/4 tests PASS

Related Dashboard/direct-delivery regression:

- 5 files PASS
- 10/10 tests PASS

Covered historical topology includes:

- `v162-dashboard-transcript-authority.test.ts`
- `v167-native-delivery-staging-order.test.ts`
- `task235-exact-topology.test.ts`
- `task234-dashboard-discord-ingress.test.ts`
- CNX-446 production-topology regression

A full plugin Vitest run after the semantic repair completed:

- 93/93 test files PASS
- 436/436 tests PASS

The final exact-source full-suite rerun after the TypeScript-only narrowing cleanup also completed GREEN:

- 93/93 test files PASS
- 436/436 tests PASS
- duration: approximately 95.15 seconds

## Build / package validation

`npm run plugin:validate`:

- TypeScript build: PASS
- canonicalized dist text files: 44
- plugin schema/artifact verification: PASS
- config properties: 46
- tools: 5
- Ticket DB bootstrap: PASS
- required Ticket tables: 9 + v095 registration fence
- package contents verification: PASS
- packed file count: 294

One initial validation attempt found only a TypeScript control-flow narrowing error on a possibly-undefined Ticket value. The code was changed to an explicit fail-closed null/owner check without changing behavior. Focused CNX-446 tests remained 4/4 PASS afterward.

Production dependency audit:

`npm audit --omit=dev`

Result:

`0 vulnerabilities`

Plugin evaluation:

- PASS
- interruption recovery: PASS
- bounded retry: PASS
- duplicate suppression: PASS
- retrieval precision/recall/provenance/latency gates: PASS
- evidence SHA-256: `ebcfa4d1353922834aa926810b724f3aacfff8a85fc12442d0cb17d8b7e85207`

Repository validation gates executed locally:

- namespace isolation: PASS
- v0.9.7 baseline consistency: PASS
- workspace validation: PASS
- Cogent self-test: PASS
- runtime self-test: PASS
- workflow self-test: PASS
- benchmark validator positive + intentional negative/tamper self-test: PASS

Full Python pytest:

- 737 passed
- 5 skipped
- 38 subtests passed
- exit code: 0
- duration: approximately 221.90 seconds

`git diff --check`:

PASS.

## Safety properties preserved

The repair does not:

- use the Dashboard Stop button as a runtime API or contract;
- treat `stopReason="stop"` as terminal proof;
- globally require `runTerminal`;
- alter native Ollama routing or delivery semantics;
- change Ticket-first admission;
- change Direct/workflow routing;
- change provider/model/auth authority;
- weaken session ownership;
- regenerate an already terminal result;
- rewrite the immutable v0.9.7 release.

## Exact implementation commit

Implementation commit:

`70a41c5d5465a898cc10cd23e5b415ffdf5695f2`

Commit subject:

`fix(v0.9.8): fence dashboard direct terminal result`

Exact-SHA CI for `70a41c5d5465a898cc10cd23e5b415ffdf5695f2`:

- PS5.1 Acceptance Smoke run `36115741706`: SUCCESS
- Windows Installer Pack Smoke run `36115741675`: SUCCESS
- Validate run `36115741683`: SUCCESS across Ubuntu / Windows / macOS and Python 3.11 / 3.14

That SHA established the terminal-boundary implementation authority. A later real install-over exposed an additional OpenClaw 2026.9.5 plugin CLI lifecycle hang, so a new exact SHA is now required before release.

## Fresh live Codex/App-Server acceptance

The repaired candidate was exercised on the original authenticated Dashboard owner session using a fresh production `chat.send` run:

- session: `agent:main:dashboard:6090e8c3-88fc-420d-8ee8-1f498b9146f6`
- run: `cnx446-live-codex-b-send-v1`
- Ticket: `CNXT-c4e850f7-a7bd-48ec-9839-3264350d7a6c`
- provider/model: `openai/gpt-5.6-luna`
- runtime: `codex`
- route: Direct

Timestamped transcript evidence:

- commentary seq 39: `2026-09-25T09:51:53.454Z`, `stopReason="stop"`, no `runTerminal`;
- tool call seq 40: `2026-09-25T09:51:55.781Z`, `stopReason="toolUse"`, no `runTerminal`;
- tool result seq 41: `2026-09-25T09:51:55.829Z`;
- true final seq 42: `2026-09-25T09:51:57.932Z`, `stopReason="stop"`, `runTerminal=true`.

All mirrored rows carried the exact run id and `mirrorOrigin="codex-app-server"`.

Ticket terminal events occurred only after the true final:

- `response_ready`: `2026-09-25T09:51:57.950Z`;
- `direct_response_durable`: same timestamp;
- `delivery_confirmed`: `2026-09-25T09:51:57.957Z`;
- `completed`: `2026-09-25T09:51:57.957Z`.

Final text:

`CNX446_TERMINAL_FINAL_B — # AGENTS.md - Your Workspace`

Marker-stripped final SHA-256:

`64c8c4897e62f937e87121309b6cbc056838c1d359999573a7251bedbe7a0f2a`

This exactly matched the Ticket payload SHA-256. Exactly one `direct_result` delivery row was created and delivered.

## Native Ollama compatibility acceptance

The native control completed on the unchanged fallback path:

- session: `agent:main:dashboard:cnx446-live-native-ollama-a`
- run: `cnx446-ollama-live-a`
- Ticket: `CNXT-ca68602c-ef77-49a2-aa83-31dff08b137d`
- provider/model: `ollama/qwen3.8:27b`
- runtime: native `openclaw`
- final timestamp: `2026-09-25T09:56:38.515Z`
- final: `CNX446_OLLAMA_NATIVE_OK`

As expected, the native assistant row exposed neither `mirrorOrigin` nor `runTerminal`. The fallback still settled exactly once.

Marker-stripped final SHA-256:

`e6805dd942c32903d50b030863c01aadeb04d6784d029c90ac7e1788042167a3`

This exactly matched the Ticket payload SHA-256. `response_ready` occurred at `09:56:38.555Z`, delivery and completion at `09:56:38.567Z`, with exactly one `direct_result` delivery.

## Real install-over finding and timeout hardening

A real candidate install-over reached package validation and supervisor quiescence, then exposed OpenClaw 2026.9.5 behavior in which:

`openclaw plugins disable cogentnexus-openclaw`

persisted the requested mutation but did not exit before the existing 180-second timeout. Rollback then encountered transient SQLite lock contention while Gateway/supervisor state was converging.

Recovery was bounded:

- no OpenClaw SQLite row was edited directly;
- the official plugin registry was regenerated through `openclaw plugins registry --refresh`;
- canonical config returned `enabled=true`;
- `plugins inspect --json` returned `enabled=true`, `status=loaded`, diagnostics empty;
- Gateway and CNX runtime registration were restored before further qualification.

The Host plugin mutation helper is now hardened narrowly:

1. keep the normal 180-second checked mutation path unchanged;
2. catch only `subprocess.TimeoutExpired`;
3. require canonical `config get` to match the requested boolean;
4. regenerate the official plugin registry;
5. require `plugins inspect --json` to match the requested enabled/status state with no diagnostics;
6. accept only when all OpenClaw-owned authorities converge;
7. otherwise re-raise the original timeout and remain fail-closed.

No arbitrary nonzero exit is converted to success.

RED-to-GREEN / regression evidence for this additional repair:

- pre-repair focused result after adding timeout-reconciliation cases: 1 passed / 3 failed;
- final focused timeout suite: 6/6 PASS;
- related Host / installer regression suite: 90/90 PASS;
- live non-mutating production parser probe: canonical config match PASS; inspector match PASS;
- full Python after the repair: 742 passed, 5 skipped, 38 subtests passed;
- `git diff --check`: PASS.

## Second real install-over finding: dependency lifecycle side effect

The timeout-reconciliation repair was committed and pushed as:

`6f8c9ab25b52da8673fa9099cc2660063581d570`

Exact-SHA GitHub status for that commit was fully GREEN:

- Validate run `36122764663`: SUCCESS;
- PS5.1 Acceptance Smoke run `36122764650`: SUCCESS;
- Windows Installer Pack Smoke run `36122764661`: SUCCESS.

A real install-over from that exact SHA then stopped earlier than the prior failure: candidate preparation invoked plain `npm ci` before classification. npm resolved `openclaw@2026.7.1-2` from the plugin peer/dev dependency graph and entered:

`scripts/postinstall-bundled-plugins.mjs`

The npm/node child tree stopped making progress. This was not a CNX runtime mutation and not the OpenClaw 2026.9.5 runtime itself; it was a lifecycle side effect of the dependency installed for build/type validation.

The installer attempt was terminated while still before classification/first install mutation. The parent PowerShell installer was stopped and the orphaned npm/node child tree was explicitly terminated. Gateway/Ticket state was therefore not intentionally mutated by this attempt.

The installer repair is deliberately narrow:

- both candidate dependency-preparation paths now use `npm ci --ignore-scripts`;
- dependency installation remains deterministic from the lockfile;
- TypeScript/plugin validation still runs explicitly through `npm run plugin:validate`;
- package construction still runs explicitly through `npm pack`;
- no CNX plugin install lifecycle script is being skipped because the plugin package does not define a required install/preinstall/postinstall lifecycle;
- unrelated peer/dev dependency lifecycle side effects are no longer executed during candidate preparation.

RED-to-GREEN evidence:

- added lifecycle-suppression contract before repair: 1 passed / 1 failed;
- after repair: 2/2 PASS;
- related installer transaction/runtime/package regression: 60/60 PASS;
- PowerShell parser for `scripts/install.ps1`: PASS;
- `git diff --check`: PASS;
- full Python after this second installer repair: 743 passed, 5 skipped, 38 subtests passed in approximately 390 seconds.

## Final exact-candidate qualification

Final production-code candidate:

`b908efe9f82550bc3cc071ad24c0f2d1d41cc4ec`

Exact-SHA CI:

- Validate run `36125311413`: SUCCESS;
- Windows Installer Pack Smoke run `36125311412`: SUCCESS;
- PS5.1 Acceptance Smoke run `36125311419`: SUCCESS.

The final real install-over began at approximately `2026-09-25T12:07:26Z` and completed successfully at `12:14:16Z` with exit code 0.

The live install proved both installer compatibility repairs:

1. candidate preparation completed with `npm ci --ignore-scripts` and no OpenClaw peer/dev postinstall hang;
2. the OpenClaw 2026.9.5 plugin disable lifecycle crossed the known post-mutation timeout boundary, reconciled through canonical config + registry refresh + plugin inspection, and the Host transaction proceeded to a durable managed authority commit rather than rolling back.

Install outcome:

- Host mode: `active`;
- generation: 30;
- provider ownership: `openclaw`;
- Gateway restart requested and completed;
- Gateway verified healthy after bounded readiness polling;
- Ollama verified healthy;
- v092 supervisor installed as hidden background task, Ready/Enabled, `LastTaskResult=0`;
- no recovered Tickets were required;
- no post-commit recovery error occurred.

Independent post-install verification:

- repository HEAD remained exact `b908efe9f82550bc3cc071ad24c0f2d1d41cc4ec`, clean and upstream-equal;
- source/installed `host_legacy_v094.py` SHA-256:
  `217c9f6b5e68e79ccc06e7895700ade1c6bcad37bd80de4fb8dfd0cad4d3a876`;
- source/installed `v091-dashboard-verified-delivery.js` SHA-256:
  `cfadb60ae8110671bca579acea3d9234f5905b716cdfbffb1eff46f918cad5a8`;
- plugin inspector: enabled=true, activated=true, status=loaded, diagnostics=[];
- Gateway Dashboard HTTP: 200 in 7 ms;
- runtime attestation: `runnerReady=true`, `globalHookCount=7`;
- `classification=AMBIGUOUS` remains the known OpenClaw 2026.9.5 public-SDK limitation because per-plugin hook count is not exposed;
- Ticket DB: zero non-terminal Tickets, zero outbox rows.

OpenClaw inspector reports `trust.reason="provenance-invalid"` for the local archive install. Inspection of OpenClaw 2026.9.5 source shows that non-official archive records fall through to this trust classification; it is not a load diagnostic. The plugin remains explicitly enabled, activated, loaded, with empty diagnostics.

## Fresh installed-candidate Codex/App-Server acceptance

A fresh run was executed after the successful exact-candidate install:

- session: `agent:main:dashboard:6090e8c3-88fc-420d-8ee8-1f498b9146f6`;
- run: `cnx446-live-codex-c-send-v1`;
- Ticket: `CNXT-95707ba8-a977-451e-b526-8ff83eb06c8c`;
- provider/model: `openai/gpt-5.6-luna`;
- runtime: `codex`;
- route: Direct.

Timestamped terminal-boundary evidence:

- commentary seq 44: `2026-09-25T12:17:56.979Z`, `stopReason="stop"`, no `runTerminal`;
- tool call seq 45: `2026-09-25T12:17:59.305Z`, no `runTerminal`;
- tool result seq 46: `2026-09-25T12:17:59.346Z`;
- true final seq 47: `2026-09-25T12:18:00.772Z`, `runTerminal=true`.

Ticket terminal events occurred only after the true final:

- `response_ready`: `2026-09-25T12:18:00.786Z`;
- `direct_response_durable`: same timestamp;
- `delivery_confirmed`: `2026-09-25T12:18:00.793Z`;
- `completed`: `2026-09-25T12:18:00.793Z`.

Final text:

`CNX446_TERMINAL_FINAL_C — # AGENTS.md - Your Workspace`

Marker-stripped SHA-256:

`b876888d047dd37bd76f65f39ca6307a7b7a96523f0543cf3e59047da582f1d6`

The SHA exactly matches the Ticket payload. Event cardinality is exactly one each for `response_ready`, `direct_response_durable`, `delivery_confirmed`, and `completed`; exactly one `direct_result` delivery row exists.

Native Ollama control from `cnx446-ollama-live-a` remains GREEN and proves that the Codex-specific terminal fence did not globally require `runTerminal`.

## Final classification

`CNX446_DASHBOARD_DIRECT_TERMINAL_BOUNDARY_GREEN`

Task 446 is complete. v0.9.8 release preparation may proceed from production-code candidate `b908efe9f82550bc3cc071ad24c0f2d1d41cc4ec`.
