# CNX-20260916-374 — Plugin Hook Registration / Registry Wiring Diagnosis

## Task identity

- **Task ID:** CNX-20260916-374
- **Parent:** CNX-20260916-373
- **State:** `CNX374_PLUGIN_HOOK_REGISTRY_WIRING_DIAGNOSIS`
- **Executor:** Hermes
- **Reviewer:** ChatGPT
- **Human final authority:** Operator
- **Branch:** `cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Objective

Determine why the live non-bundled `cogentnexus-openclaw` plugin is reported as `loaded/enabled` and the effective configuration has `allowConversationAccess=true`, while the live Dashboard execution still produces no `before_agent_run` evidence.

CNX-371 established the installed Dashboard → Gateway agent → embedded selection runner path and the runner's `hookRunner` dispatch site. CNX-372 could not observe the process-local registry. CNX-373 proved the conversation-hook access permission is explicitly granted. The remaining focus is therefore the **plugin hook registration → host hook registry wiring boundary**.

## Diagnosis scope

Use exact current branch source plus the installed OpenClaw `2026.7.1-2 (0790d9f)` runtime to distinguish:

1. CogentNexus calls `api.on("before_agent_run", ...)` but the host does not retain/register the handler.
2. The handler is registered, but `plugins list`/inventory does not expose dynamically registered hooks and therefore is not diagnostic of registry membership.
3. The plugin entry/register layering causes the handler to be registered on a proxy or API object that does not feed the runner's global conversation-hook registry.
4. The plugin's registration timing/Promise behavior causes hooks to be installed too late for the Gateway runner.
5. OpenClaw requires an explicit manifest/permission/metadata declaration in addition to `api.on` for this hook to enter the registry, despite `allowConversationAccess=true`.
6. A different concrete host wiring condition explains the absence.

Do not assume any of these before evidence.

## Required source inspection

Inspect both plugin and host-side behavior around:

- `plugins/cogentnexus-openclaw/src/v091-release-entry.ts`
- `plugins/cogentnexus-openclaw/src/v091-final-entry.ts`
- `plugins/cogentnexus-openclaw/src/index.ts`
- the `definePluginEntry(...)` contract
- `api.on("before_agent_run", ...)` registration
- `withWebchatLegacyDeliveryFence()` / wrapper APIs
- `legacyEntry.register(runtimeApi)` invocation and return type
- whether `register(runtimeApi)` is synchronous or asynchronous
- ordering of `register()` versus `installManagedRuntimeGuards()`
- OpenClaw plugin loader/registry implementation in the installed `2026.7.1-2` package
- hook inventory implementation (`hookNames`, `hookCount`)
- hook registry construction/attachment to `selection-JInn13lc.js`
- `hasHooks("before_agent_run")`
- `runBeforeAgentRun(...)`

The goal is to trace the object/reference lineage:

`OpenClaw plugin API → plugin api.on → host registry → selected runner hookRunner`

### Special attention: API proxying

`v091-release-entry.ts` creates proxy-like APIs around the original `api` and passes a wrapped API into `legacyEntry.register(runtimeApi)`.

Prove whether calls such as:

`runtimeApi.on(...)`

ultimately register against the same host registry consumed by the Dashboard selection runner.

Do not assume object spreading/proxy wrapping preserves every host-side API capability or identity-sensitive registration behavior.

### Special attention: registration timing

Prove whether the relevant `api.on("before_agent_run")` registration occurs:

- before the plugin is considered fully loaded,
- before the Dashboard runner is created/selected,
- before the first Dashboard request,
- and before `runEmbeddedAttempt` tests `hookRunner.hasHooks(...)`.

A source-level `api.on(...)` call is insufficient evidence if registration happens too late or against the wrong registry.

## Runtime diagnosis

Use supported read-only diagnostics where possible.

Permitted observations include:

- installed plugin source inspection and hashing;
- OpenClaw plugin metadata/inventory;
- installed runtime source inspection;
- process/module inspection;
- static module dependency/load inspection;
- any already-enabled supported diagnostic interfaces.

Do not enable a debugger/inspector if doing so mutates runtime state unless the task authorization is expanded explicitly.

Do not send a Dashboard semantic request unless a supported observation mechanism genuinely requires one. It is not authorized by default.

## Desired concrete finding

Produce one of the following only when evidence supports it:

`REGISTRY_WIRING_BROKEN`
= `api.on` registration does not reach the registry consumed by the Dashboard runner.

`REGISTRATION_TIMING_BROKEN`
= registration occurs after the runner's registry snapshot/use point.

`REGISTRATION_METADATA_REQUIRED`
= host requires a concrete declaration/metadata beyond `api.on`, proven from host implementation.

`INVENTORY_FALSE_NEGATIVE`
= `hookCount: 0` is not representative, and another source/runtime path proves the hook is registered; continue diagnosis to explain CNX-370 separately.

`PROVEN_OTHER`
= a different concrete mechanism is established.

`INCONCLUSIVE`
= evidence still cannot distinguish the cases.

## Repair authorization

This task is **diagnosis-first**. No production source repair is authorized until the concrete registration/registry cause is proven.

Once and only once a cause is proven, the task may implement the smallest justified repair at that exact boundary, with focused regression tests.

Do not redesign admission.
Do not duplicate Ticket admission.
Do not move admission into Dashboard UI or provider layer.
Do not alter `durableAdmissionEligible()` or TicketStore without separate evidence proving those are causal.

## Testing

If a concrete source repair is made:

1. create/extend a focused regression reproducing the exact registry/timing failure;
2. prove RED before repair;
3. implement minimal fix;
4. prove GREEN;
5. run relevant plugin tests and applicable full validation/build.

Do not add a test for a merely hypothesized mechanism.

## Runtime activation

Only after validated source repair, use supported activation/reload if needed. Record exact before/after process identity and installed/effective artifact hashes.

Do not perform semantic requalification in this task unless a separate authorization is explicitly created later.

## Hard fences

- No provider/auth/routing/model changes.
- No semantic-contract changes.
- No Dashboard UI/provider-layer changes.
- No speculative source patch.
- No TicketStore/admission redesign.
- No manual controller normalization.
- No repeated Dashboard traffic.
- No semantic requalification by default.
- No historical edits to CNX-360 through CNX-373.
- No release/tag/main.
- No force-push/history rewrite.
- If diagnosis remains inconclusive, stop and report the uncertainty.
- Do not start CNX-375 yourself.

## Reporting

Publish:

`docs/operations/coordination/reports/CNX-20260916-374-plugin-hook-registration-registry-wiring-report.md`

Include:

- starting/final remote HEAD;
- exact source/installed paths examined;
- API object/reference lineage;
- registration timing evidence;
- host hook registry/inventory implementation evidence;
- `before_agent_run` registry membership conclusion;
- classification;
- source changes and hashes, if any;
- test/build/validation results, if repair occurred;
- runtime activation evidence, if any;
- semantic request count;
- hard-fence compliance;
- remaining uncertainty;
- recommended next state.

After report publication, set coordination to `WAITING_FOR_CHATGPT_REVIEW` and stop.
