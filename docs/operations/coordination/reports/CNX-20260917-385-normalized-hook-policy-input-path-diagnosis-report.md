# CNX-20260917-385 — Normalized Hook Policy Input Path Diagnosis Report

## Classification

**`NORMALIZED_HOOK_POLICY_PRESERVED_HOST_CONTRACT_FOUND`**

The raw-config → normalization → `normalized.entries[pluginId]` → `entry.hooks` → `createApi(hookPolicy)` → `registerTypedHook` gate path **preserves** `plugins.entries.<id>.hooks.allowConversationAccess=true` end-to-end. The field is not stripped, transformed, renamed, schema-rejected, defaulted, or overwritten by the host normalization pipeline. It is an intended, supported host configuration contract, and the smallest existing extension point that carries the policy to the gate is the OpenClaw runtime config key itself.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Task ID: `CNX-20260917-385`
- Required starting status: `READY_FOR_HERMES` (confirmed)
- Authoritative starting HEAD: `d7ad9b4e62becf26a456df60685e352a3753fcb2`
- Starting remote HEAD: `d7ad9b4e62becf26a456df60685e352a3753fcb2`

`ACTIVE.md`, `STATUS.md`, this task, and the CNX-384, CNX-383, CNX-382, CNX-381, CNX-374, and CNX-373 reports were read from the authoritative branch before action. The required identity was confirmed: `Task ID = CNX-20260917-385`; `Status = READY_FOR_HERMES`.

## Proven baseline (predecessor evidence, not re-executed)

| Task | Proven claim |
|---|---|
| CNX-373 | Live runtime config contains `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess=true` |
| CNX-374 | Executable definition `releaseEntry.hooks.allowConversationAccess=true` was added after `definePluginEntry` |
| CNX-381 | `api.on("before_agent_run")` reaches real `registerTypedHook`; rejected by non-bundled conversation gate |
| CNX-382 | Loader binds `entry = normalized.entries[pluginId]`; passes `hookPolicy: entry?.hooks` to `createApi` |
| CNX-383 | Executable definition projection loss proven; focused RED regression `cnx383-hook-policy-projection.test.ts` |
| CNX-384 | Plugin repository does not own normalization; no tracked clean-install host-dependency patch mechanism |

## Exact OpenClaw version and module hashes

- OpenClaw version: `2026.7.1-2` (resolved from `C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\package.json`)
- Node runtime: `v22.23.2`

| Module | SHA-256 | Role |
|---|---|---|
| `dist/config-normalization-shared-w2iz0aeC.js` | `c3b7bccc26f72ac0ab79ef0635daaa5931d23f86d9bc7e21f4ae8b60ce80f7c2` | `normalizePluginsConfigWithResolver`, `normalizePluginEntries` |
| `dist/config-state-CtMlHVRM.js` | `af2e3bc003048755d820284d3e01a777fae907aff3be8bc4e281dee663f409c5` | `normalizePluginsConfig` wrapper |
| `dist/loader-D8d2EvVh.js` | `3a10479bdcbb713692c3ded7dbd5baad27c1b17ae3566172c117d45916dabce7` | `const entry = normalized.entries[pluginId]`; `createApi(..., hookPolicy: entry?.hooks)` |
| `dist/registry-B8eQDFB4.js` | `25f3ef82756d85281ad5c25375a5cd2f405989a1145ed438de05992e8c995376` | `registerTypedHook` gate at lines 4225-4244 |
| `dist/zod-schema-O9ml_nmo.js` | `daca03ca77175870afbb2e32508693ad4641669e417d2a05112669c95d403813` | Config schema; `PluginEntrySchema` with `hooks.allowConversationAccess` |

## Source trace

### 1. Raw config → schema validation

`zod-schema-O9ml_nmo.js:788-806` defines `PluginEntrySchema`:

```js
const PluginEntrySchema = object({
  enabled: boolean().optional(),
  hooks: object({
    allowPromptInjection: boolean().optional(),
    allowConversationAccess: boolean().optional(),
    timeoutMs: number().int().positive().max(6e5).optional(),
    timeouts: record(string(), number().int().positive().max(6e5)).optional()
  }).strict().optional(),
  subagent: ...,
  llm: ...,
  config: record(string(), unknown()).optional()
}).strict();
```

`zod-schema-O9ml_nmo.js:1528`: `entries: record(string(), PluginEntrySchema).optional()` — the schema explicitly accepts `hooks.allowConversationAccess` as a boolean. The schema is `strict()`, so unknown keys are rejected, but `hooks.allowConversationAccess` is a known, accepted field.

**Field help text** (`schema-DRyO1XBt.js:819`):

> "Controls whether this plugin may read raw conversation content from typed hooks such as `before_agent_run`, `before_model_resolve`, `before_agent_reply`, `llm_input`, `llm_output`, `before_agent_finalize`, and `agent_end`. Non-bundled plugins must opt in explicitly."

This documents the field as an intended host contract.

### 2. Schema validation → normalization

`config-state-CtMlHVRM.js:35-37`:

```js
const normalizePluginsConfig = (config) => {
  return normalizePluginsConfigWithResolver(config, createScopedPluginIdNormalizer());
};
```

`config-normalization-shared-w2iz0aeC.js:254-312` — `normalizePluginEntries`:

```js
function normalizePluginEntries(entries, normalizePluginId) {
  if (!entries || typeof entries !== "object" || Array.isArray(entries)) return {};
  const normalized = {};
  for (const [key, value] of Object.entries(entries)) {
    const normalizedKey = normalizePluginId(key);
    if (!normalizedKey) continue;
    if (!value || typeof value !== "object" || Array.isArray(value)) {
      normalized[normalizedKey] = {};
      continue;
    }
    const entry = value;
    const hooksRaw = entry.hooks;
    const hooks = hooksRaw && typeof hooksRaw === "object" && !Array.isArray(hooksRaw) ? {
      allowPromptInjection: hooksRaw.allowPromptInjection,
      allowConversationAccess: hooksRaw.allowConversationAccess,
      timeoutMs: normalizeHookTimeoutMs(hooksRaw.timeoutMs),
      timeouts: normalizeHookTimeouts(hooksRaw.timeouts)
    } : void 0;
    const normalizedHooks = hooks && (typeof hooks.allowPromptInjection === "boolean" || typeof hooks.allowConversationAccess === "boolean" || hooks.timeoutMs !== void 0 || hooks.timeouts !== void 0) ? {
      ...typeof hooks.allowPromptInjection === "boolean" ? { allowPromptInjection: hooks.allowPromptInjection } : {},
      ...typeof hooks.allowConversationAccess === "boolean" ? { allowConversationAccess: hooks.allowConversationAccess } : {},
      ...hooks.timeoutMs !== void 0 ? { timeoutMs: hooks.timeoutMs } : {},
      ...hooks.timeouts !== void 0 ? { timeouts: hooks.timeouts } : {}
    } : void 0;
    normalized[normalizedKey] = {
      ...normalized[normalizedKey],
      enabled: typeof entry.enabled === "boolean" ? entry.enabled : normalized[normalizedKey]?.enabled,
      hooks: normalizedHooks ?? normalized[normalizedKey]?.hooks,
      subagent: normalizedSubagent ?? normalized[normalizedKey]?.subagent,
      llm: normalizedLlm ?? normalized[normalizedKey]?.llm,
      config: "config" in entry ? entry.config : normalized[normalizedKey]?.config
    };
  }
  return normalized;
}
```

**Critical lines 265-277**: the normalizer reads `entry.hooks`, extracts `allowConversationAccess` (only if `typeof === "boolean"`), and reconstructs `normalizedHooks` preserving the boolean value. Line 305 assigns `hooks: normalizedHooks ?? normalized[normalizedKey]?.hooks`. The field is **preserved** when present and boolean; it is **omitted** only when absent from the raw config or non-boolean.

### 3. Normalized config → loader `entry`

`loader-D8d2EvVh.js:1730`:

```js
const entry = normalized.entries[pluginId];
```

This is the decisive identity: `entry` is the normalized runtime configuration entry, NOT the executable definition and NOT the manifest record.

### 4. `entry.hooks` → `createApi(hookPolicy)`

`loader-D8d2EvVh.js:2237-2242` (normal path):

```js
const api = createApi(record, {
  config: cfg,
  pluginConfig: validatedConfig.value,
  hookPolicy: entry?.hooks,
  registrationMode
});
```

`loader-D8d2EvVh.js:1994-1999` (setup-entry variant, same projection):

```js
const api = createApi(record, {
  config: cfg,
  pluginConfig: {},
  hookPolicy: entry?.hooks,
  registrationMode
});
```

Both paths project `entry?.hooks` (the normalized config hooks) into `hookPolicy`.

### 5. `createApi(hookPolicy)` → `registerTypedHook` gate

`registry-B8eQDFB4.js:4180-4260` — `registerTypedHook`:

```js
const registerTypedHook = (record, hookName, handler, opts, policy) => {
  // ...
  if (isConversationHookName(effectiveHookName)) {
    const explicitConversationAccess = policy?.allowConversationAccess;
    if (record.origin !== "bundled" && explicitConversationAccess !== true) {
      pushDiagnostic({
        level: "warn",
        pluginId: record.id,
        source: record.source,
        message: `typed hook "${effectiveHookName}" blocked because non-bundled plugins must set plugins.entries.${record.id}.hooks.allowConversationAccess=true`
      });
      return;  // BLOCKED
    }
    if (record.origin === "bundled" && explicitConversationAccess === false) {
      // ... blocked for bundled with explicit false
      return;
    }
  }
  // ... accepted: record.hookCount += 1; registry.typedHooks.push(...)
};
```

The gate reads `policy?.allowConversationAccess` directly. When `policy` is `{allowConversationAccess: true}`, the gate passes for non-bundled plugins.

## Required runtime probe (disposable, isolated)

A disposable probe (`cnx385-probe.mjs`) imported the exact installed OpenClaw `2026.7.1-2` modules and exercised the exported `normalizePluginsConfigWithResolver` and `OpenClawSchema.safeParse` functions against three fixtures. PID `24428`, Node `v22.23.2`. This probe directly captures raw, validated, normalized, `entry.hooks`, and the policy values that the source-proven loader/API/gate assignments consume; it does not itself instrument private `loadOpenClawPlugins` internals or intercept the actual `createApi` call. The loader/API/gate behavior is established by the exact source trace and predecessor CNX-381 runtime lifecycle evidence.

### Fixture A — `hooks.allowConversationAccess: true`

| Stage | Value |
|---|---|
| Raw config | `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess = true` |
| Schema validation | PASS |
| `normalized.entries[id]` | `{hooks: {allowConversationAccess: true}}` |
| `entry?.hooks` | `{allowConversationAccess: true}` |
| `createApi` hookPolicy | `{allowConversationAccess: true}` |
| `registerTypedHook` policy | `{allowConversationAccess: true}` |
| Gate result | **ALLOW** |

### Fixture B — `hooks.allowConversationAccess: false`

| Stage | Value |
|---|---|
| Raw config | `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess = false` |
| Schema validation | PASS |
| `normalized.entries[id]` | `{hooks: {allowConversationAccess: false}}` |
| `entry?.hooks` | `{allowConversationAccess: false}` |
| `createApi` hookPolicy | `{allowConversationAccess: false}` |
| `registerTypedHook` policy | `{allowConversationAccess: false}` |
| Gate result | **BLOCK** (gate requires `=== true`) |

### Fixture C — hooks omitted

| Stage | Value |
|---|---|
| Raw config | `plugins.entries.cogentnexus-openclaw = {}` (no hooks key) |
| Schema validation | PASS |
| `normalized.entries[id]` | `{}` |
| `entry?.hooks` | `undefined` |
| `createApi` hookPolicy | `undefined` |
| `registerTypedHook` policy | `undefined` |
| Gate result | **BLOCK** (`policy?.allowConversationAccess` is `undefined`, which is `!== true`) |

### A/B/C comparison matrix

| Fixture | Raw hooks | Validation | Normalized entry hooks | createApi hookPolicy | Gate result |
| --- | --- | --- | --- | --- | --- |
| A | `true` | PASS | `{allowConversationAccess: true}` | `{allowConversationAccess: true}` | **ALLOW** |
| B | `false` | PASS | `{allowConversationAccess: false}` | `{allowConversationAccess: false}` | BLOCK |
| C | absent | PASS | `undefined` | `undefined` | BLOCK |

**Conclusion**: normalization **preserves** the field. It does not strip, reject, default, or transform. The gate result is determined solely by whether the normalized `entry.hooks.allowConversationAccess` is exactly `true`.

## Bundled vs non-bundled

The gate at `registry-B8eQDFB4.js:4227` branches on `record.origin`:

- **Non-bundled** (`record.origin !== "bundled"`): blocked when `explicitConversationAccess !== true`. Requires explicit opt-in.
- **Bundled** (`record.origin === "bundled"`): blocked only when `explicitConversationAccess === false`. Bundled plugins are allowed by default.

The normalization path (`normalizePluginEntries`) does NOT branch on bundled/non-bundled — it processes `entry.hooks` identically for all plugin origins. The bundled/non-bundled distinction is applied only at the gate, not during normalization.

`cogentnexus-openclaw` is a non-bundled (global) plugin, so it must set `hooks.allowConversationAccess=true` explicitly. The normalization path correctly preserves this when configured.

## Manifest comparison

`openclaw.plugin.json` (in the plugin repository) declares plugin metadata for discovery, including `extensions`, `channels`, `providers`, etc. The manifest `hooks` field (when present in `openclaw.plugin.json`) is a **capability/list field** for manifest capability listings — it is NOT the same schema as `plugins.entries.<id>.hooks.allowConversationAccess`.

The manifest-discovery path (`manifest-registry--UiRn6nq.js:273-326`) normalizes manifest metadata and records `hooks: []` as a capability list. This is a separate concept from the runtime policy object. No source path copies manifest `hooks` into the runtime `normalized.entries[pluginId].hooks` policy object.

**Confirmed**: manifest `hooks` and `plugins.entries.<id>.hooks` are different schemas. The runtime policy is sourced exclusively from the OpenClaw runtime config (`openclaw.json` / `plugins.entries.<id>.hooks`), not from the plugin manifest.

## Existing supported extension point analysis

The diagnosis proves that the **existing, supported, intended host contract** for this policy is:

```
plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess = true
```

This is:
- **Schema-validated**: accepted by `PluginEntrySchema` in `zod-schema-O9ml_nmo.js:788-806`
- **Normalized faithfully**: preserved by `normalizePluginEntries` in `config-normalization-shared-w2iz0aeC.js:265-277`
- **Projected to the gate**: passed as `hookPolicy` to `createApi` in `loader-D8d2EvVh.js:2240`
- **Read by the gate**: consumed at `registry-B8eQDFB4.js:4226`
- **Documented**: field help text in `schema-DRyO1XBt.js:819` explicitly describes it

No patch to OpenClaw, no new dependency architecture, no executable definition change, and no bypass registration mechanism is required. The config key is the smallest and only extension point needed.

### Why CNX-382/383/384 observed loss

CNX-382 proved that the executable definition's `releaseEntry.hooks.allowConversationAccess=true` is NOT projected into the loader's `entry?.hooks`. This is correct — the loader sources `hookPolicy` from `normalized.entries[pluginId].hooks` (runtime config), not from the executable definition. CNX-374's fix added the field to the executable definition, which does not affect the loader path. CNX-383/384 correctly identified that the plugin repository does not own the loader/normalization code.

**The resolution**: the loss is not in the normalization path — it is in the assumption that the executable definition feeds the loader's `hookPolicy`. The runtime config path works correctly. If the effective runtime config contains `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess=true`, the gate receives `hookPolicy = {allowConversationAccess: true}` and allows the hook.

## Production vs isolated evidence separation

### Production facts (previously established, not changed by this task)

- PID `27372`
- OpenClaw `2026.7.1-2`
- Effective artifact SHA-256 `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- Production plugin loaded
- Production inventory `hookCount=0`
- CNX-373 observed raw config with `hooks.allowConversationAccess=true`

### Isolated evidence (this task)

- PID `24428` disposable probe
- Exact OpenClaw `2026.7.1-2` modules imported from `C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\dist\`
- Real `normalizePluginsConfigWithResolver` and `OpenClawSchema.safeParse` exercised
- Three-fixture A/B/C comparison proves preservation

### Correspondence

The isolated probe uses the exact same module bytes (verified by SHA-256) as the production OpenClaw `2026.7.1-2`. The normalization logic is identical. Therefore, if the production effective runtime config contains `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess=true`, the production gate MUST receive `hookPolicy = {allowConversationAccess: true}` and ALLOW the hook.

The remaining production uncertainty is NOT whether the normalization path preserves the field (proven that it does), but whether the production effective runtime config actually contains the field at the moment the loader runs. CNX-373 observed it in the raw config file, but `hookCount=0` in production suggests either:

1. The production effective config at loader runtime does not contain the field (config drift, reload race, or different config path), OR
2. The hook registration is being blocked at a different boundary (registry composition, as explored in CNX-377/CNX-378), OR
3. The hook is registered but the inventory projection (`hookCount`) is stale or cached

This task does not resolve production causal equivalence — it resolves the normalization input path, which is the specific question CNX-385 was authorized to answer.

## Remaining uncertainty

1. **Production effective config at loader runtime**: CNX-373 observed `hooks.allowConversationAccess=true` in the raw config file, but this task does not re-validate the production effective config at loader runtime. The normalization path is proven to preserve the field; whether production actually feeds it to the loader is a separate question.

2. **Registry composition boundary**: Even if the gate passes and `record.hookCount` increments, CNX-377/CNX-378 identified a separate registry-composition boundary where hooks may not reach the composed registry view. This task does not re-investigate that boundary.

3. **Executable definition path**: CNX-374 added `hooks.allowConversationAccess=true` to the executable definition. This task confirms that path does not affect the loader's `hookPolicy` (loader uses normalized config, not definition). The CNX-374 fix's effect on production is not re-validated here.

## Hard-fence compliance

- Production Gateway restart/reload: `0`
- Production configuration mutation: `0`
- OpenClaw dependency patch: `0`
- CogentNexus source/artifact repair: `0`
- Artifact rebuild: `0`
- Semantic/model/provider requests: `0`
- TicketStore/admission/routing/auth/Dashboard changes: `0`
- Permanent or committed instrumentation: `0` (probe file `cnx385-probe.mjs` and `cnx385-probe.json` are disposable, uncommitted, in workspace only)
- Broad refactor: `0`
- Release/tag/main changes: `0`
- Force-push/history rewrite: `0`
- Historical CNX-360 through CNX-384 edits: `0`
- CNX-386 started: `0`

## Closeout

Classification: **`NORMALIZED_HOOK_POLICY_PRESERVED_HOST_CONTRACT_FOUND`**.

The raw-config → normalization → `normalized.entries[pluginId]` → `entry.hooks` → `createApi(hookPolicy)` → `registerTypedHook` gate path preserves `plugins.entries.<id>.hooks.allowConversationAccess=true` end-to-end. The field is an intended, documented, supported host configuration contract. No repair is needed in the normalization path; the existing extension point is the config key itself.

After publication, `ACTIVE.md` and `STATUS.md` are set to `WAITING_FOR_CHATGPT_REVIEW`. No runtime activation, semantic probe, or CNX-386 task is started.
