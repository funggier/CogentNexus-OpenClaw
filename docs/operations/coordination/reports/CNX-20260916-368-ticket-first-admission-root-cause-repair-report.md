# CNX-368 — Ticket-first admission root-cause repair report

## Disposition

**REPAIRED / VERIFIED — live semantic requalification remains unauthorized.**

The first broken boundary was proven at the Host authority gate before plugin registration: the active canonical Host controller uses schema v2 (`cnxMode`), while the installed plugin entrypoint accepted only schema v1 (`mode`). The entrypoint therefore returned `authorized: false`, registered no downstream handlers, and the Dashboard request could proceed through native OpenClaw/OpenAI without CogentNexus `before_agent_run` admission.

## Authority and forensic anchor

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Exact starting HEAD: `0326a9b9f184047ea677c39d157412006fb7f780`
- Task: `docs/operations/coordination/tasks/CNX-20260916-368-ticket-first-admission-root-cause-repair.md`
- CNX-367 session: `agent:main:dashboard:83027933-3a42-4877-a79a-167caaa396a5`
- CNX-367 run: `c3e88413-5199-4d0c-bfec-deb33e86928e`
- CNX-367 traceId/runtime session ID: `7b1a5ad4-0560-4b19-ae4e-609f9492b2c5`
- CNX-367 route: `openai / gpt-5.6-luna / openai-chatgpt-responses`
- CNX-367 observed trajectory: `prompt.submitted → model.completed → session.ended`
- CNX-367 request/model counts: one Dashboard request and one OpenAI/model request; no retry.

## Registration and dispatch evidence

1. The package manifest declares the installed plugin extension as `./dist/v091-release-entry.js` (`plugins/cogentnexus-openclaw/package.json`, `openclaw.extensions`).
2. The release entry imports `legacyEntry` from `v091-final-entry.js`, and its `register(api)` first calls `hostPluginAuthority(api)`. If unauthorized it logs registration suppression and returns before calling the legacy register path or installing runtime guards.
3. Before repair, `hostPluginAuthority` required `state.schemaVersion === 1` and a string `state.mode` of `managed`, `passthrough`, or `maintenance`.
4. The canonical Host implementation (`skills/cogentnexus-openclaw/scripts/host_state_v095.py`) writes schema v2 with `cnxMode: active|disabled|maintenance`; the compatibility façade explicitly derives legacy `mode` only in memory and persists canonical schema v2. Thus the active controller shape is not a v1 `{schemaVersion:1,mode:...}` record.
5. The Ticket-first handler is registered inside `src/index.ts` at `api.on("before_agent_run", ...)`, behind the legacy registration chain. Its admission trace begins only after that callback is registered and invoked.
6. CNX-367's exact runtime evidence has native OpenClaw session/model trajectory but no `before_agent_run`, `admission.trace.*`, Ticket, lifecycle, or Ticket-linked evidence. This rules out a mere reporting omission for the expected admission chain.
7. The source package and extension path identify the plugin entrypoint; the built artifact produced after repair contains the repaired authority gate and the same `before_agent_run` registration chain. No runtime restart, reinstall, controller edit, or live request was performed in this task, so no claim is made that a live process was reloaded with the repaired artifact.

### First broken component boundary

**Host authority decision → plugin registration.**

The failure occurs before event dispatch, Dashboard eligibility filtering, Ticket persistence, or direct-model lease logic. Because registration is suppressed, there is no CogentNexus callback for the Dashboard event to reach. Native OpenClaw then remains able to dispatch the Dashboard prompt directly to its configured OpenAI route, explaining the exact CNX-367 bypass.

This is not classified from log absence alone: the source call graph, canonical persisted-state contract, installed extension path, pre-repair authority predicate, and exact CNX-367 native trajectory jointly establish the boundary.

## Root-cause repair

Changed production file: `plugins/cogentnexus-openclaw/src/v091-release-entry.ts`.

Minimal change:

- accept a bounded numeric schema set `{1,2}`;
- retain strict fail-closed validation for missing, non-integer, unsupported, or malformed schema values;
- for schema v2, translate `cnxMode` in memory only (`active→managed`, `disabled→passthrough`, `maintenance→maintenance`);
- preserve the existing schema v1 `mode` path and downstream registration behavior.

No provider, authentication, routing, controller, runtime, or semantic request behavior was changed. The controller is not written by the plugin authority check.

## TDD evidence

Regression test: `plugins/cogentnexus-openclaw/src/cnx368-ticket-first-admission.test.ts`.

- Genuine RED before repair: Vitest failed because canonical `{schemaVersion:2,cnxMode:"active"}` produced `{authorized:false,reason:"invalid"}` instead of authorization; exit code 1.
- During initial harness completion, the first post-repair test invocation exposed a test-fixture deficiency (`api.registerTool is not a function`), not a product failure. The fixture was completed with the same registration surface used by the existing Host authority tests; no production change was made for that harness correction.
- GREEN after repair: focused Vitest passed, `1 passed`.

## Validation evidence

- `npx vitest run --config ./vitest.config.ts src/cnx368-ticket-first-admission.test.ts`: PASS, 1/1.
- `npm test`: PASS, 77 test files, 339 tests.
- `npm run plugin:build`: PASS; TypeScript build, dist canonicalization, and `verify-v091-schema.mjs` all passed.
- `npm run plugin:validate`: PASS; plugin build, ticket DB bootstrap validation, and package-content validation passed.
- Repaired built entrypoint SHA-256: `04e12be2dc24a8f60c079031737c32bca5990251e8c219066a4413c31eab802`.
- Repaired source SHA-256: `f033b4a588421da097d3db0f8247e741c1de5cf8782cadcbfb2db993840e6a9a`.
- Built artifact contains `SUPPORTED_CONTROLLER_SCHEMA_VERSIONS`, the schema-v2 branch, and the legacy `before_agent_run` chain.
- Historical CNX-360 through CNX-367 task/report paths were not modified; the pre-publication diff contained only the new regression test and production source repair.

## Instrumentation

No diagnostic runtime instrumentation was added. The existing source registration path and retained CNX-367 evidence were sufficient to prove the first broken boundary. No prompts, credentials, tokens, or secret-bearing data were collected.

## Counters and fences

- Dashboard request count during CNX-368: `0`
- OpenAI/model request count during CNX-368: `0`
- Runtime mutation count: `0`
- Reinstall/restart/controller/provider/auth/routing mutation count: `0`
- Retries: `0`
- Live semantic requalification: `0`

Repository mutation was limited to the two task deliverable implementation files and this report; no historical coordination record was edited.

## Exact files changed

- `plugins/cogentnexus-openclaw/src/v091-release-entry.ts`
- `plugins/cogentnexus-openclaw/src/cnx368-ticket-first-admission.test.ts`
- `docs/operations/coordination/reports/CNX-20260916-368-ticket-first-admission-root-cause-repair-report.md`

## Next authorization boundary

A separate successor task must perform a fresh installed-runtime identity check and one explicitly authorized live Dashboard semantic requalification against the repaired exact SHA. CNX-368 does **not** authorize a Dashboard/model request, runtime reload, reinstall, or semantic requalification; stop here after remote report and branch verification.
