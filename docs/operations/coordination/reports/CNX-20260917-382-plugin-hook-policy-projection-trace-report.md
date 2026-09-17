# CNX-20260917-382 — Plugin Hook Policy Projection Trace Report

## Classification

**`HOOK_POLICY_PROJECTION_LOSS_PROVEN`**

The exact host path was traced to a concrete projection mismatch. The exported CogentNexus definition contains `hooks.allowConversationAccess=true`, but OpenClaw does not derive `createApi(..., hookPolicy)` from that definition. In the non-bundled loader, `hookPolicy` is passed as `entry?.hooks`, where `entry` is `normalized.entries[pluginId]` from runtime plugin configuration. The manifest/discovery record and loader plugin record do not carry the executable definition's `hooks` field. Thus CNX-374 changed the executable export, but did not populate the separate configuration object consumed by the gate.

No repair was attempted or authorized.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Authoritative starting HEAD: `d9545be104e93e29dde219f5872fd5de0bbf870b`
- Starting status: `READY_FOR_HERMES`
- Task ID: `CNX-20260917-382`
- Parent: `CNX-20260917-381`

## Runtime and hashes

- OpenClaw: `2026.7.1-2`
- Node used for disposable probe: `v22.23.2`
- Disposable process PID: `26324`
- Effective artifact: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
- Effective artifact SHA-256: `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`

Relevant exact installed module hashes:

| Module | SHA-256 |
|---|---|
| `dist/loader-D8d2EvVh.js` | `3a10479bdcbb713692c3ded7dbd5baad27c1b17ae3566172c117d45916dabce7` |
| `dist/manifest-registry--UiRn6nq.js` | `819c76c314e6ed1fd39c5ed6b169d63997905b3ae8a98b9373783d626431ace4` |
| `dist/plugin-entry-CM_XK0Yw.js` | `1727ed4701071c7a8d395db824ca5324c25e08353a5a2451420db59232fce4a5` |
| `dist/registry-B8eQDFB4.js` | `25f3ef82756d85281ad5c25375a5cd2f405989a1145ed438de05992e8c995376` |
| `dist/hook-runner-global-BmIrGlLG.js` | `c066170e97a2355603f0bdd3079a687bf835632856a741fa9a92683d7d4b2750` |
| `dist/runtime-D0xGMZdc.js` | `a050a101e3c352345179b77f8c304da99596238fcde95cf03319ebc11dea8791` |

The disposable probe imported the real effective artifact and logged:

```json
{"pid":26324,"exportedHooks":{"allowConversationAccess":true},"exportedKeys":["id","name","description","configSchema","register","hooks"]}
```

CNX-381 separately exercised the real loader lifecycle against this artifact and recorded the native `registerTypedHook` policy diagnostic and rejected `before_agent_run` registrations.

## Exact projection evidence

### 1. Exported definition and `definePluginEntry`

`v091-release-entry.js:133-174` constructs `releaseEntry` as:

```js
const releaseEntry = {
  ...definePluginEntry({ ... }),
  hooks: { allowConversationAccess: true }
};
```

The installed SDK helper `plugin-entry-CM_XK0Yw.js:23-38` defines `definePluginEntry({ id, name, description, kind, configSchema, reload, nodeHostCommands, securityAuditCollectors, register })` and returns only the supported fields. It does not accept or return a `hooks` parameter. The outer spread then adds `hooks` to the final exported object. The runtime probe proves the final default export has `hooks.allowConversationAccess === true`.

Therefore:

- `definePluginEntry(...)` result alone: no `hooks` property.
- final exported `releaseEntry`: `hooks.allowConversationAccess === true`.
- these are different object stages; the `hooks` property is added by the outer object reconstruction after the helper returns.

### 2. Discovery/manifest and loader record

The manifest registry normalizes discovered plugin metadata in `manifest-registry--UiRn6nq.js:273-326` and records manifest capabilities such as channels/providers/config schema. Its normalized manifest record has a `hooks` collection for manifest capability listings, not the executable definition policy object. No path copies `releaseEntry.hooks` into the manifest record.

The real loader creates the plugin record in `loader-D8d2EvVh.js:1730-1755`. The record is populated from `manifestRecord` and candidate metadata (`name`, `description`, `version`, `format`, `bundleCapabilities`, `source`, `rootDir`, origin, config schema, and related fields). The executable definition is imported later and only selected fields are copied back at `loader-D8d2EvVh.js:2182-2200` (`name`, `description`, `version`, `kind`). There is no `record.hooks = definition.hooks` projection.

The loader's `entry` variable is explicitly assigned at `loader-D8d2EvVh.js:1730`:

```js
const entry = normalized.entries[pluginId];
```

This is the decisive identity distinction: `entry` is a normalized runtime configuration entry, not `resolved.definition` and not `record`.

### 3. `createApi` and policy argument

For the normal non-bundled path, `loader-D8d2EvVh.js:2238-2242` calls:

```js
createApi(record, {
  config: cfg,
  pluginConfig: validatedConfig.value,
  hookPolicy: entry?.hooks,
  registrationMode
});
```

The setup-entry variant uses the same projection at `loader-D8d2EvVh.js:1995-2000`.

`validatedConfig.value` is derived from `entry?.config` at `loader-D8d2EvVh.js:1898-1907`; this confirms that `pluginConfig` and `hookPolicy` are two projections of the configuration entry. They are not the executable definition's `hooks` field.

`registry-B8eQDFB4.js:4384-4415` receives `record` and `params`, and `registry-B8eQDFB4.js:4776` closes `api.on` over `params.hookPolicy`:

```js
on: (hookName, handler, opts) =>
  registerTypedHook(record, hookName, handler, opts, params.hookPolicy)
```

`registerTypedHook` is defined at `registry-B8eQDFB4.js:4180-4244`; its conversation gate reads `policy?.allowConversationAccess` at `4226` and emits the non-bundled diagnostic at `4232-4234` when it is not true.

### 4. Runtime gate evidence

CNX-381's exact isolated OpenClaw lifecycle used the real loader, API, `api.on`, and `registerTypedHook`. It recorded repeated `before_agent_run` calls returning `undefined`, no throw, the native diagnostic:

```text
typed hook "before_agent_run" blocked because non-bundled plugins must set plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess=true
```

and final absence of `before_agent_run`. Combined with the current disposable export probe and the source-bound identity trace above, the gate's `policy` is the configuration-derived `entry?.hooks`, not `releaseEntry.hooks`.

## Identity/projection matrix

| Boundary | Property exists? | Value | Object identity/token | Evidence |
|---|---:|---|---|---|
| exported `releaseEntry` | yes | `true` | P1 | PID 26324 import; artifact lines 133-174 |
| `definePluginEntry(...)` result | no | `undefined`/omitted | P2 | SDK lines 23-38 accepts no hooks field |
| discovered metadata / manifest record | no policy field | omitted | P3 | manifest normalization lines 273-326; loader metadata construction |
| loader plugin record | no policy field | omitted | P4 | loader lines 1730-1755 and 2182-2200 |
| `entry` at `createApi` | configuration object | `entry?.hooks` (absent in the CNX-381 effective isolated configuration) | P5 | loader line 1730; createApi calls lines 1997/2240 |
| `pluginConfig` | separate config projection | `validatedConfig.value` from `entry?.config` | P6 | loader lines 1898-1907, 2239 |
| `hookPolicy` inside API | absent/false for the observed non-bundled run | `params.hookPolicy` | P7 | registry createApi and closure lines 4384-4415, 4776 |
| `registerTypedHook` policy | absent/false for target | same `params.hookPolicy` | P8 | registry lines 4180-4244 |
| conversation gate | policy test fails | `policy?.allowConversationAccess !== true` | P9 | registry line 4226; diagnostic lines 4232-4234 |

P1 is not the same object as P2: the helper result is spread into a new outer object. P1 is not P3/P4/P5: no source path assigns definition hooks to manifest metadata, loader record, or API policy. P5/P6 are projections from the normalized configuration entry and are distinct from P1. The exact CNX-381 runtime observation supplies the policy-failure side effect at P8/P9.

## First boundary

**First proven loss is the executable-definition-to-loader-policy boundary.** More precisely, `hooks` is not accepted by `definePluginEntry` (P2), is added only to the outer exported object (P1), and is then not copied into either discovered metadata or the loader record. At `loader-D8d2EvVh.js:1730`, the variable named `entry` is instead `normalized.entries[pluginId]`; at lines 1997/2240 its `hooks` is passed to `createApi`. This is a separate configuration path.

This is not a later registry-composition loss. The policy gate rejects the conversation hook before registry storage, consistent with CNX-381.

## Direct answers to required questions

1. `definePluginEntry(...)` result does **not** preserve `hooks`; the final outer `releaseEntry` does.
2. The real loader does not retain executable-definition `hooks` in its discovered/plugin entry record.
3. `createApi` receives `entry?.hooks` from normalized plugin configuration, not the loaded definition.
4. In the CNX-381 effective isolated run, `entry?.hooks` at `createApi` was not true; the native gate diagnostic proves the resulting policy was not true. The current source shows why.
5. `pluginConfig.hooks` and definition `hooks` are distinct concepts. `pluginConfig` comes from `validatedConfig.value` (`entry.config`); `hookPolicy` comes from `entry.hooks`; neither is sourced from the executable definition.
6. The non-bundled path uses the same `entry?.hooks` projection and applies the explicit non-bundled gate. Bundled paths may differ in registration planning, but no bundled path is needed to explain this result.
7. The manifest/discovery schema does not carry the executable policy object; its `hooks` metadata is a capability/list field, not `allowConversationAccess` policy propagation.
8. The compatibility adapter does not cause the policy loss. It forwards the host API; the policy is already supplied by loader configuration when `createApi` is built.
9. Yes. CNX-374 added `hooks` to the executable exported object after `definePluginEntry`, but that property is not on the normalized metadata/config object used by the loader's `entry?.hooks` expression.
10. The decisive mismatch is therefore proven: CNX-374's executable definition contains the property, while the host policy path reads a separate normalized config entry.

## Comparison with CNX-374 and CNX-381

CNX-374's installed artifact hash and source shape are confirmed: the property is present on the exported `releaseEntry`. CNX-381 proved the exact lifecycle reaches the host gate and receives the non-bundled rejection. CNX-382 connects those observations by identifying the separate `normalized.entries[pluginId]` policy source and the missing definition-to-policy projection.

## Production evidence

Previously established production facts, not changed here:

- PID `27372`
- OpenClaw `2026.7.1-2`
- effective artifact SHA-256 `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- plugin loaded
- production `hookCount=0`

No production restart/reload, debugger attach, config mutation, or semantic/model request occurred. The isolated diagnosis is strongly mechanistically corresponding because it uses the same exact OpenClaw version/module hashes and effective artifact family, and CNX-381 observed the same native gate. It is not a claim that production memory objects were inspected; production root-cause equivalence remains limited to the shared loader/gate mechanism and artifact identity.

## Exact isolated evidence

- PID `26324` imported the effective artifact and proved exported P1.
- Exact installed module source and hashes above identify the loader, manifest, SDK helper, API registry, runner, and runtime.
- CNX-381 PID `16216` is the exact isolated lifecycle evidence for the real loader/API/gate call and native diagnostic; it is cited as predecessor evidence, not relabeled as the CNX-382 probe.
- No synthetic registry model was used for the cited lifecycle evidence.

## Remaining uncertainty

The disposable PID 26324 probe did not mutate or inspect production memory and did not expose private JavaScript object identities across the loader's internal calls. The exact isolated policy value is established by CNX-381's native diagnostic and source-bound argument path, while the current probe establishes P1. A future repair task would need to decide how to populate the host-supported configuration/policy path; CNX-382 has no repair authority and makes no recommendation beyond identifying the boundary.

## Hard-fence compliance

- Production Gateway restart/reload: `0`
- Production configuration mutation: `0`
- OpenClaw dependency patch: `0`
- CogentNexus source/artifact patch: `0`
- Artifact rebuild: `0`
- Semantic/model/provider requests: `0`
- TicketStore/admission/routing/auth/Dashboard changes: `0`
- Permanent or committed instrumentation: `0`
- Broad refactor: `0`
- Release/tag/main changes: `0`
- Force-push/history rewrite: `0`
- Historical CNX-360 through CNX-381 edits: `0`
- CNX-383 started: `0`

## Closeout

Classification: **`HOOK_POLICY_PROJECTION_LOSS_PROVEN`**

Diagnosis only. No repair success is claimed.
