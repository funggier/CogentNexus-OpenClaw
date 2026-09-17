# CNX-20260917-383 — Hook Policy Projection Repair Report

## Classification

**`HOOK_POLICY_PROJECTION_REPAIR_BLOCKED`**

The authorized repair could not be completed without changing the OpenClaw host loader/dependency or bypassing its policy gate. Both are outside the hard fence. No Dashboard Ticket-first semantic success is claimed.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Task ID: `CNX-20260917-383`
- Starting status: `READY_FOR_HERMES`
- Authoritative starting HEAD: `f3e93ee8f228f6b8bfadacfdf4cf742cc4a1efd9`
- Starting remote HEAD: `f3e93ee8f228f6b8bfadacfdf4cf742cc4a1efd9`
- Starting worktree: contained pre-existing unrelated untracked files; they were not modified

The required `ACTIVE.md`, `STATUS.md`, CNX-383 task, CNX-382 report, CNX-381 report, and CNX-374 report were read. The required tokens were confirmed: `Task ID = CNX-20260917-383`, `Status = READY_FOR_HERMES`.

## CNX-382 root cause and source boundary

CNX-382 proved that the executable export contains `releaseEntry.hooks.allowConversationAccess = true`, while the OpenClaw loader binds `const entry = normalized.entries[pluginId]` and passes `hookPolicy: entry?.hooks` to `createApi`. The API closes `api.on` over that policy and `registerTypedHook` rejects non-bundled `before_agent_run` before registry storage when `allowConversationAccess` is not true.

The installed OpenClaw `2026.7.1-2` source confirms:

- `loader-D8d2EvVh.js:1730`: `const entry = normalized.entries[pluginId]`
- `loader-D8d2EvVh.js:2237-2242`: `createApi(..., { pluginConfig: validatedConfig.value, hookPolicy: entry?.hooks, ... })`
- `registry-B8eQDFB4.js:4776`: `registerTypedHook(..., params.hookPolicy)`
- `registry-B8eQDFB4.js:4226`: conversation policy check

The plugin repository has no source function that owns or mutates `normalized.entries[pluginId]`. The OpenClaw loader is a dependency under `plugins/cogentnexus-openclaw/node_modules/openclaw`; patching it is explicitly prohibited. Adding or retaining `hooks` on the executable export does not alter the normalized runtime configuration object consumed at the proven boundary.

## RED evidence

Added focused regression:

- `plugins/cogentnexus-openclaw/src/cnx383-hook-policy-projection.test.ts:1-28`

The test asserts the exact loss boundary: executable `entry.hooks.allowConversationAccess` is `true`, while the host input modeled as `normalized.entries[entry.id]?.hooks` is empty. It failed as required:

```text
FAIL src/cnx383-hook-policy-projection.test.ts
expected undefined to be true
Test Files 1 failed; Tests 1 failed
```

This reproduces the CNX-382 mechanism at the policy projection boundary. It does not accept a test that merely checks the exported `releaseEntry` field.

## Repair assessment

The two authorized directions were evaluated against the actual source:

1. Preserving the field through `definePluginEntry` cannot repair this boundary because the loader does not source `hookPolicy` from the executable definition or the `definePluginEntry` result.
2. An explicit narrow projection would have to execute in the OpenClaw loader between `normalized.entries[pluginId]` and `createApi`. No such plugin-owned boundary exists in this repository. Implementing it requires an OpenClaw dependency patch or a second/bypass registration mechanism, both prohibited.

No speculative source patch was made. No gate bypass, hardcoded gate acceptance, duplicate registration path, TicketStore change, admission change, or broad refactor was made.

## Validation

- Focused CNX-383 regression: **RED / failed**, proving the un repaired projection.
- Existing CNX-374 regression: **PASS** (`1 passed`, `1 test passed`).
- Plugin build: **PASS** (`tsc -p tsconfig.json` and `canonicalize-dist.mjs`; 50 dist text files canonicalized).
- Type/lint: TypeScript compilation passed as part of build; no separate lint script is defined in `package.json`.
- Full plugin suite: not reported as GREEN because the required focused regression remains RED.

## Artifact and runtime evidence

No runtime activation occurred because source/build/test acceptance was not GREEN. Therefore:

- pre-activation PID: not applicable
- post-activation PID: not applicable
- installed effective artifact: not activated or replaced
- known effective artifact SHA-256, read directly from the built file: `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- known previous repaired artifact SHA-256: `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- production facts remain separate and unchanged: PID `27372`, OpenClaw `2026.7.1-2`, plugin loaded, production `hookCount=0`
- plugin hook visibility after this task: not changed; `before_agent_run` remains unproven/blocked in the effective production runtime
- Dashboard semantic requests: `0`

The matching SHA is reported as identity evidence only; no claim is made that a newly activated artifact exists.

## Mutation counts

- Plugin source repair: `0`
- Focused regression added: `1`
- Coordination report added: `1`
- Runtime activation/restart: `0`
- Production configuration mutation: `0`
- Semantic requests: `0`
- Provider/auth/routing/model changes: `0`
- TicketStore/admission changes: `0`
- Dashboard UI changes: `0`
- OpenClaw dependency changes: `0`
- Force-push/history rewrite/release/tag/main changes: `0`
- Historical CNX-360 through CNX-382 edits: `0`
- Successor CNX-384 started: `0`

## Hard-fence compliance

All requested hard fences were respected. The only code change is the focused CNX-383 RED regression. Existing unrelated untracked files were left untouched.

## Remaining uncertainty

The next repair authority would need to authorize a host-side OpenClaw projection change, or provide an existing supported host extension point that maps executable definition policy into `normalized.entries[pluginId].hooks`. This task did not invent either. Until that boundary is changed under an appropriate authorization, the chain cannot be demonstrated beyond the proven failure:

`releaseEntry.hooks.allowConversationAccess=true`
→ **loss at host normalized-entry projection**
→ `createApi(hookPolicy=undefined)`
→ `registerTypedHook` policy rejection
→ `before_agent_run` absent from typed registry.

## Closeout

Classification: **`HOOK_POLICY_PROJECTION_REPAIR_BLOCKED`**.

After publication, coordination status is set to `WAITING_FOR_CHATGPT_REVIEW`. No runtime activation, semantic probe, or CNX-384 task was started.
