# CNX-20260917-377 — Composed Hook Registry Wiring Repair

## Classification

**`INCONCLUSIVE`**

## Authority and scope

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Starting authoritative HEAD: `b9bf07c6b10a13deb39df21e119bd507fa2cf370`
- Final candidate HEAD before report closeout: `2a35be9a9cfeda0da8b7ed1141d28614ad01bd73`
- Parent evidence: CNX-376 `DISPATCH_BOUNDARY_PROVEN`
- Semantic requests in CNX-377: **0**

No TicketStore, admission, provider/model/auth/routing, Dashboard UI, release/tag, force-push, or historical CNX-360..376 changes were made.

## Direct effective-artifact verification

The installed artifact was hashed directly from disk, not copied from an earlier report:

`C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`

SHA-256:

`2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`

The artifact contains `hooks: { allowConversationAccess: true }` at generated lines 173–175. This differs from the CNX-376 report hash (`...c948...`) and from the CNX-374/CNX-375 hash lineage; the direct file hash above is the only hash claimed here.

## Source/runtime trace

The installed OpenClaw 2026.7.1-2 dependency was inspected from the repository's declared dependency after `npm ci --ignore-scripts`.

1. `loader-D8d2EvVh.js` creates a registry through `createPluginRegistry(...)`, loads the plugin, then `activatePluginRegistry(registry, ...)` calls `setActivePluginRegistry(registry, ...)` followed by `initializeGlobalHookRunner(registry)`.
2. `registry-B8eQDFB4.js` exposes `api.on` as `registerTypedHook(record, hookName, handler, opts, params.hookPolicy)`. The conversation-hook gate rejects non-bundled hooks unless `allowConversationAccess === true`; the installed plugin definition satisfies that gate.
3. `runtime-D0xGMZdc.js` stores the active registry and synchronizes the HTTP, channel, and session-extension surfaces. It retires only registries no longer live.
4. `hook-runner-global-BmIrGlLG.js` does not snapshot only `state.registry`: `createComposedHookRegistryFacade(state)` calls `composeLiveHookRegistry(state.registry)` on each getter. The composer includes `state.registry` plus `collectLivePluginRegistries()`, de-duplicates by object identity, skips retired registries, and filters hooks by plugin ownership.
5. `getGlobalHookRunner()` returns the stable runner created with that live facade. `hasHooks("before_agent_run")` therefore reads the composed getter at query time.

These source facts prove the intended identity/composition lineage is live and mutation-visible for the current OpenClaw dependency. They do **not** reproduce CNX-376's observed `hookCount: 0` against the current source/effective artifact, nor identify a repository-side defect that can be repaired minimally without patching OpenClaw itself.

## TDD evidence

- Existing focused CNX-374 regression was run and passed: `src/cnx374-registry-wiring.test.ts` — 1 test passed.
- A RED regression for the **actual** CNX-376 composed-registry failure could not be honestly established from this repository: the host registry/composition implementation is an external OpenClaw dependency, and the current inspected implementation composes live registries.
- No speculative RED test or source patch was added.

## Repair decision

No source repair was applied. A minimal plugin-side change would be speculative: the plugin's `api.on` already forwards to the host API, and the host dependency's current loader/registry/global-runner path already shares live registry identity and recomposes dynamically. Patching TicketStore, admission, Dashboard code, or adding a second registration path would violate the task fences.

Runtime activation/restart was not performed because no validated source repair existed to activate. No semantic probe was sent because read-only/source evidence was sufficient to establish that the remaining divergence is outside a proven repository-side mechanism, but insufficient to claim a repair.

## Remaining uncertainty / blocker

The live `hookCount: 0` observation from CNX-376 cannot be reconciled with the current OpenClaw source inspected in this session. To resolve it, a future authorized task would need a supported process-local observation that binds the effective OpenClaw host build, registry object identity, and plugin load event to one exact runtime. That is outside CNX-377's safe minimal-repair boundary; this task therefore stops as `INCONCLUSIVE`.

## Validation

- `npm ci --ignore-scripts` — passed; 352 packages installed.
- `npm test -- --run src/cnx374-registry-wiring.test.ts` — passed; 1 test passed.
- Effective artifact SHA-256 — freshly computed from installed file above.
- Source/build validation of a repair — not applicable; no repair was made.

## Hard-fence compliance

- Semantic request count: 0/1.
- No force-push or history rewrite.
- No main/release/tag mutation.
- No CNX-378 work.
- No historical CNX-360..376 edits.
- No TicketStore/admission/provider/model/auth/routing/Dashboard UI changes.

## Handoff

`ACTIVE.md` and `STATUS.md` are set to `WAITING_FOR_CHATGPT_REVIEW`. Stop after this handoff.
