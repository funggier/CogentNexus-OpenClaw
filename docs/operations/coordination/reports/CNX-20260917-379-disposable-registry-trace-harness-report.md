# CNX-20260917-379 — Disposable Registry Trace Harness Report

## Classification

**`DIAGNOSTIC_HARNESS_INSUFFICIENT`**

The disposable harness proved identity tracing and controlled failure-mode discrimination, but it did not safely execute the exact production OpenClaw loader/plugin lifecycle. It therefore does not prove a production root cause and no repair was attempted.

## Authority and final state

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Authoritative starting HEAD: `d368a1123c6d4a3d41f892c3d8d57321f0c82236`
- Starting remote HEAD matched local HEAD before work.
- Final HEAD is recorded in the closeout after the report/state commit and remote read-back.
- Task confirmed from fresh GitHub files: `CNX-20260917-379`, status `READY_FOR_HERMES`.

## Production facts (not produced by this harness)

Reused unchanged from CNX-378:

- PID `27372`
- OpenClaw CLI/Gateway `2026.7.1-2`
- Node runtime reported by the gateway: `24.18.0`
- Effective CogentNexus artifact: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
- Artifact SHA-256: `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- Loaded plugin inventory: `status: loaded`, `hookCount: 0`, `hookNames: []`
- Supported diagnostics did not expose JavaScript object identity.

CNX-376 established the Dashboard dispatch boundary at plugin registration to host composed-registry visibility. CNX-378 correlated the live PID/build/artifact/plugin record but left object identity and causal mechanism unobserved. Those are production observations; no harness result below is substituted for them.

## Disposable environment

A fresh repository clone was used at `C:\Users\CDQ-P\cnx379-preflight`, pinned initially to the authoritative branch HEAD above. The temporary harness was a separate Node process and did not import or modify the live Gateway.

- Harness runtime: Node `v22.23.2`
- Harness source: `cnx379-disposable-harness.js`
- Harness source SHA-256: `09d6d991946c555eb36fb77fcd64ab7a97554c978751113d7d171bbc64e1e0f`
- Captured output SHA-256: `04ec9e97fba367991ea9a9f3cbec0a7c98787c3c8cc867a7efe40a406f3a1c26`
- The harness was discarded after evidence capture; no temporary instrumentation was written to the installed OpenClaw tree or production CogentNexus artifact.

This was a production-shaped lifecycle model based on the observed OpenClaw boundaries (`api.on`/typed registration, active registry, live collection, composed facade, global `hasHooks`). It was not an exact execution of the bundled OpenClaw module graph because loading the exact installed entrypoint would require reproducing its full host/configuration/plugin environment; doing so safely was not established within this diagnosis-only fence.

## Instrumentation points

The harness assigned stable `WeakMap`-generated IDs to every registry object and recorded:

1. plugin `api.on("before_agent_run")` registration target before and after mutation;
2. `initializeGlobalHookRunner(registry)` argument;
3. `state.registry`;
4. `collectLivePluginRegistries()` result;
5. composed facade input and hook collection;
6. `hasHooks("before_agent_run")` result.

Hook counts were recorded at each boundary. Registry owner metadata and retirement state were retained in the fixture objects. The harness ran controlled cases for normal flow, instance mismatch, replacement/reset, and collection exclusion.

## Identity matrix — closest production-shaped case

| Boundary | Identity | Same as active registry? | Hook count | Notes |
|---|---:|---:|---:|---|
| plugin registration target | R2 | yes | 1 | count 0 before `api.on`, 1 after |
| `initializeGlobalHookRunner` arg | R2 | yes | 1 | same object |
| `state.registry` | R2 | yes | 1 | same object |
| collected live registry | R2 | yes | 1 | one live member |
| composed facade input | R2 | yes | 1 | deduplicated composition |
| `hasHooks("before_agent_run")` | — | — | 1 / `true` | hook visible |

### Controlled mutation validation

The control case independently proved that the mechanism detects a known mutation: the same token remained `R1` across registration, initialization, state, collection, composition, and query; hook count changed from `0` to `1`; `hasHooks` returned `true`.

### Controlled candidate mechanisms

| Case | Registration | Init/state | Collection | Composed count | `hasHooks` | Interpretation |
|---|---|---|---:|---:|---:|---|
| instance mismatch | R3 | R4 | R3,R4 | 1 | true | mismatch alone does not imply invisibility when composition includes both |
| replacement/reset | R5 (retired) | R6 | R5,R6 | 0 | false | replacement plus retired filtering reproduces the empty view |
| collection exclusion | R7 | R7 | empty | 1 | true | in this model state registry remains composed, so exclusion alone does not reproduce absence |

These cases validate the diagnostic instrument, not the production mechanism.

## Ownership/filter observations

The fixture carried owner `cogentnexus-openclaw`. No production ownership/filter decision was observed. In the synthetic exclusion case, removing the registration target from the live collection while retaining it as `state.registry` did not hide the hook because the composed facade also included `state.registry`. This is evidence about the fixture's modeled composition only.

## Candidate-mechanism evidence

- **Registry instance mismatch:** not proven in production. The harness can distinguish it, but its closest case still returned `hasHooks=true` because both registries were composed.
- **Registry replacement/reset:** not proven in production. The controlled case can reproduce `hookCount=0` and `hasHooks=false` when the original is retired and the replacement is empty.
- **Different registry collection:** not proven in production. The controlled exclusion case did not reproduce invisibility under the modeled facade.
- **Ownership/filter exclusion:** not proven in production. No exact host filtering path was executed.
- **Initialization ordering/recomposition:** not proven in production. The harness had deterministic synchronous ordering and no exact loader timing.
- **Inventory projection differs from runner registry:** not proven or disproven. The harness has no supported inventory projection equivalent bound to the live process.
- **Other mechanism:** none directly observed in production.

## Production versus harness boundary

**Production:** CNX-376/CNX-378 facts above, including the live `hookCount: 0` projection and inability to inspect object identity.

**Harness:** WeakMap identity tokens, counts, mutation timing, modeled collection/composition, and controlled mechanism cases above.

The harness does not connect its synthetic object identities to PID `27372`, the production artifact, or the production global runner. Consequently no synthetic case is promoted to a production root cause.

## Cleanup and validation

- Identity mechanism executed successfully: PASS.
- Known mutation detected and query visibility changed as expected: PASS.
- Closest production-shaped lifecycle traced: PASS as a model, not exact runtime: LIMITATION.
- Identity matrix and boundary hook counts captured: PASS.
- Comparison with CNX-376/CNX-378 recorded: PASS.
- Exact production lifecycle/artifact execution: NOT PROVEN.
- Production gateway restart/reload: 0.
- Production semantic/model requests: 0.
- Production config/dependency/source mutation: 0.
- Disposable environment cleanup: PASS; temporary harness/evidence directory discarded after capture.

## Remaining uncertainty

The decisive missing evidence is a safe, exact, process-isolated execution of the OpenClaw `2026.7.1-2` loader and effective CogentNexus artifact with instrumentation at the real registry references. Until that is available, the contradiction remains unresolved and no candidate mechanism can be called the production cause.

## Hard-fence compliance

No production Gateway restart/reload, configuration change, dependency patch, CogentNexus source patch, Dashboard semantic request, model request, TicketStore/admission/provider/auth/routing change, UI change, speculative repair, broad refactor, release/tag/main change, force-push, historical CNX-360–CNX-378 edit, or CNX-380 activity occurred. Temporary code was disposable and was not committed.

## Handoff

`ACTIVE.md` and `STATUS.md` are set to `WAITING_FOR_CHATGPT_REVIEW`. Stop after this publication; CNX-380 was not started.
