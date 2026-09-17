# CNX-20260917-394 — Production Plugin-ID / Inventory Projection Trace Report

## Classification

`PRODUCTION_PLUGIN_ID_PROJECTION_INCONCLUSIVE`

The installed source proves that the live loader uses `pluginId = manifestRecord.id` and indexes configuration as `normalized.entries[pluginId]`. It also proves that the `plugins list --json` command does **not** serialize that live loader record: it reads a persisted/derived installed-plugin index and constructs a new inventory record whose `id` is `plugin.pluginId`. The installed source shows the persisted index can carry an ID originating from loader record `record.id`, but this supported inventory observation does not establish that the already-running production loader's `pluginId` and the inventory index entry are the same historical object/value. Therefore the CNX-393 candidate-ID association uncertainty is narrowed but not closed.

The inventory's `hookCount` and `hookNames` are not projected from the live typed-hook registry: the status projection initializes both to zero/empty arrays. Separately, `registerTypedHook` increments the live loader record's `hookCount` and stores typed hooks, while `api.on` also updates the live record's `hookNames` and `registry.hooks`. Consequently `hookCount=0`/`hookNames=[]` is not evidence about historical registration acceptance.

## Authority and closeout

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Authoritative starting HEAD: `240265f919f947235fe4a334efd763dc7c0ed25b`
- Authoritative final HEAD: recorded below after publication and remote read-back
- Starting gate: `READY_FOR_HERMES`
- Task: `CNX-20260917-394`
- Parent: `CNX-20260917-393`

GitHub was fetched first. The local branch was fast-forwarded/re-anchored to the fetched remote tip before investigation. Existing unrelated untracked files were preserved and not modified.

## Exact runtime, artifact, config, and module identity

- OpenClaw: `2026.7.1-2 (0790d9f)`
- Node CLI: installed OpenClaw runtime
- Effective artifact: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
- Effective artifact SHA-256: `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- Production config SHA-256: `19d7e6acf53ce370ddc20e5e2a2547c9674c33b178208b79920cb0e9dce9b46b`

| Installed module | SHA-256 |
|---|---|
| `dist/loader-D8d2EvVh.js` | `3a10479bdcbb713692c3ded7dbd5baad27c1b17ae3566172c117d45916dabce7` |
| `dist/registry-B8eQDFB4.js` | `25f3ef82756d85281ad5c25375a5cd2f405989a1145ed438de05992e8c995376` |
| `dist/status-snapshot-lNsJCo4p.js` | `f14f0f8f7b9847b20718e6d53824894fe81c22879166984bc61016e626ab554f` |
| `dist/plugins-list-command-0fMcQYzj.js` | `d9bfcd6aeb9bc13d8af0c9ae17fca7714199839ed00397fef43fa4f640148a6a` |
| `dist/plugin-registry-8E8D2Hou.js` | `570f856a8f4e517d8bf0e0d768bcf691eaf9bf44b9f8e560c8f86ff8a7cef983` |

## Production read-only correlation

Fresh supported `openclaw plugins list --json` observation returned:

```json
{"id":"cogentnexus-openclaw","rootDir":"C:\\Users\\CDQ-P\\.openclaw\\extensions\\cogentnexus-openclaw","origin":"global","status":"loaded","hookCount":0,"hookNames":[]}
```

Read-only production config extraction returned:

```json
{"configKey":"plugins.entries.cogentnexus-openclaw","enabled":true,"allowConversationAccess":true}
```

No secrets were printed. No production lifecycle or mutation action was issued.

## Exact loader identity path

In `dist/loader-D8d2EvVh.js`:

1. `:1640` constructs `manifestByRoot = new Map(manifestRegistry.plugins.map(record => [record.rootDir, record]))`.
2. `:1664-1666` obtains `manifestRecord = manifestByRoot.get(candidate.rootDir)` and assigns `const pluginId = manifestRecord.id`.
3. `:1730` performs the decisive configuration lookup: `const entry = normalized.entries[pluginId]`.
4. `:1731-1753` calls `createPluginRecord` with `id: pluginId`, `rootDir: candidate.rootDir`, `origin: candidate.origin`, and `enabled` state. `createPluginRecord` is at `:288-341`; it assigns `id: params.id`, `rootDir: params.rootDir`, `origin: params.origin`, and `status: params.enabled ? "loaded" : "disabled"` (`:290`, `:299-310`). It initializes `hookNames: []` and `hookCount: 0` (`:312`, `:336`).
5. `:2237-2242` creates the runtime API with `hookPolicy: entry?.hooks`.
6. `:2271-2272` inserts the record into the live loader registry with `registry.plugins.push(record)` and records the seen ID with `seenIds.set(pluginId, candidate.origin)`.

This proves the loader record ID is a direct parameter projection of `manifestRecord.id`, and that the normalized-entry lookup uses that same local `pluginId` variable. It does not prove that the later inventory object is this same record.

## `plugins list --json` projection path

The exact command is `dist/plugins-list-command-0fMcQYzj.js:25-42`:

- `:26-30` imports `buildPluginRegistrySnapshotReport` and calls it with runtime config.
- `:31` filters the returned report only when `--enabled` is used.
- `:33-41` serializes `report.plugins` as JSON.

`dist/status-snapshot-lNsJCo4p.js` provides the projection:

- `:89-110` calls `loadPluginRegistrySnapshotWithMetadata`, loads a metadata snapshot, and maps `result.snapshot.plugins` through `buildPluginRecordFromInstalledIndex`.
- `:36-86` constructs a **new** inventory object. Its fields are:
  - `id`: `plugin.pluginId` (`:40`), from the installed-index snapshot plugin, not directly from a live loader record or registry key at serialization time.
  - `source`: `plugin.source ?? plugin.manifestPath` (`:47`).
  - `rootDir`: `plugin.rootDir` (`:48`).
  - `origin`: `plugin.origin` (`:49`).
  - `status`: derived as `plugin.enabled ? "loaded" : "disabled"` (`:53`).
  - `hookNames`: freshly initialized to `[]` (`:55`).
  - `hookCount`: freshly initialized to `0` (`:78`).
- `dist/plugin-registry-8E8D2Hou.js:401-410` shows the snapshot may be `source: "derived"`; the persisted path is selected earlier in the same loader. Thus the command can report a persisted/derived installed-index snapshot rather than the live activation registry.

The installed-index reader validates and carries IDs as map keys/`pluginId` fields (`dist/installed-plugin-index-record-reader-Dd35fnKn.js:77-79, 113-114, 199-201`). The installed-index store schema requires `pluginId`, `rootDir`, and `origin` (`dist/installed-plugin-index-store-CWgFGnm0.js:40,59-60`). This establishes an intermediate identity-bearing projection. It does not establish, for this running process, that its `pluginId` was freshly produced from the current `manifestRecord.id` rather than persisted or derived earlier.

## Hook-count and hook-name projection

The live registration path is separate:

- `dist/registry-B8eQDFB4.js:4776` routes `api.on` to `registerTypedHook(..., params.hookPolicy)`.
- `:2723-2729` appends `hookName` to the live `record.hookNames` and pushes a hook object to `registry.hooks`; the hook object uses `pluginId: record.id` (`:2725`).
- `:4251-4259` increments the live `record.hookCount` and pushes the accepted hook to `registry.typedHooks`, again using `pluginId: record.id`.
- By contrast, the inventory status projection explicitly resets `hookNames` and `hookCount` to empty/zero at `status-snapshot-lNsJCo4p.js:55,78`.

Therefore the supported inventory fields are not calculated from the same live registry state that receives `registerTypedHook`. The source directly proves they are summary defaults in a separate installed-index projection.

## Isolated probe

No new plugin installation, production-tree copy, dependency patch, or permanent instrumentation was performed. A synthetic exact projection probe was unnecessary: the exact installed source already exposes the decisive status projection and its separation from the live registry. CNX-391 remains the valid disposable exact-loader/API evidence for downstream true-policy acceptance, but it is not inventory-identity evidence and is not reinterpreted here.

## Direct evidence versus inference

**Direct evidence:** exact GitHub starting SHA; exact runtime/artifact/config/module hashes; fresh production inventory; fresh non-secret config linkage; loader assignments `pluginId = manifestRecord.id`, `entry = normalized.entries[pluginId]`, and `createPluginRecord({ id: pluginId, ... })`; live registry insertion; command implementation; inventory construction from `plugin.pluginId`; inventory `rootDir`/`origin`/status assignments; inventory hook zero/empty initialization; and live `registerTypedHook`/`api.on` updates to the loader record and typed-hook registries.

**Inference:** the production inventory ID `cogentnexus-openclaw` is consistent with the intended loader ID and with the production config key. It is not direct proof that the already-running global loader used that exact value for its `normalized.entries[pluginId]` lookup, because the supported command reads a persisted/derived index and creates a separate object. The source shows the intermediate index can preserve an ID, but the current observation does not establish historical freshness or object identity.

## Comparison with CNX-393 and CNX-391

- CNX-393's source-level loader chain remains correct. CNX-394 removes the assumption that `plugins list --json` is a raw live-loader projection and proves that its `hookCount`/`hookNames` fields cannot answer the live typed-hook question.
- The displayed inventory ID narrows candidate-ID ambiguity: it agrees with the manifest/config spelling and is sourced from an identity-bearing `pluginId` field. It does **not** prove the live global `manifestRecord.id` or the existence of `normalized.entries[pluginId]` at historical registration time.
- An intermediate persisted/derived inventory projection remains capable of being stale, detached, or differently sourced; the source does not show a transformation from `cogentnexus-openclaw` to another ID in this observation, but it also does not provide live identity correlation.
- `hookCount=0` and `hookNames=[]` remain symptoms only. They do not prove policy rejection, registry-composition loss, or failure to call `registerTypedHook`.
- CNX-391 is unchanged: it proved that the exact loader/API lifecycle accepts the production-shaped `entry.hooks.allowConversationAccess=true` in isolation. CNX-394 determines only that inventory identity is not a sufficient proof that production selected that entry.

## Remaining uncertainty

The remaining production gap is the unobserved historical association in the already-running global loader: its actual `manifestRecord.id`, the corresponding `normalized.entries[pluginId]` object, and the `hookPolicy` passed at registration time. Current inventory is a separate persisted/derived projection and cannot close that memory/lifecycle gap under the no-restart/no-debugger fences. No production hook acceptance or rejection is claimed.

## Counts and hard-fence compliance

- Semantic/model/provider/Dashboard request count: `0`
- Production mutation count: `0`
- Production Gateway restart/reload: `0`
- Production configuration mutation: `0`
- Environment mutation: `0`
- Scheduled Task mutation: `0`
- Production global extension installation/mutation: `0`
- Artifact replacement/deploy/rebuild: `0`
- OpenClaw dependency patch: `0`
- CogentNexus source repair: `0`
- Debugger/inspector attachment: `0`
- Permanent instrumentation: `0`
- Historical CNX-360 through CNX-393 modifications: `0`
- Release/tag/main changes: `0`
- Force-push/history rewrite: `0`
- CNX-395 created/started: `0`

## Closeout

`ACTIVE.md` and `STATUS.md` were changed only after report publication to `WAITING_FOR_CHATGPT_REVIEW`. No successor task was created or started. Execution stops for review.
