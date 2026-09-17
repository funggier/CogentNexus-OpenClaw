# CNX-20260917-395 — Installed-Plugin Index Population / Freshness Provenance Report

## Classification

`INSTALLED_INDEX_PROVEN_STALE_OR_PREEXISTING`

The production installed-plugin index is a persisted SQLite projection whose target row was generated and updated on `2026-09-16T13:07:14.051Z`. The observed gateway process started at `2026-09-17T10:13:08.606Z`, approximately 21 hours later. Its `pluginId`, root, origin, and source match the current inventory and effective artifact, but the index timestamp and mechanism do not establish contemporaneous production-loader creation. The source also shows that policy-only refresh can update the persisted row without invoking the loader. Therefore the index is proven preexisting relative to the current gateway start; current-loader provenance remains unproven.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Authoritative starting HEAD: `3b89b10c53a5647dbc3dcf26d74630c4bbf9b84b`
- Authoritative final HEAD: recorded in closeout after publication and remote verification
- Starting gate: `READY_FOR_HERMES`
- Task: `CNX-20260917-395`
- Parent: `CNX-20260917-394`

GitHub was fetched before investigation. The detached checkout matched the supplied SHA, and the fetched remote branch was verified at the same SHA. No historical coordination file was modified before the report closeout changes.

## Exact runtime and hashes

- OpenClaw: `2026.7.1-2 (0790d9f)`
- Effective artifact: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
- Effective artifact SHA-256: `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- Production config SHA-256: `19d7e6acf53ce370ddc20e5e2a2547c9674c33b178208b79920cb0e9dce9b46b`

| Installed module | SHA-256 |
|---|---|
| `dist/installed-plugin-index-N4jxqS0-.js` | `695dc3196348aa176780979d8c3a75428e9029890470670bcb77cf1a7fa03719` |
| `dist/installed-plugin-index-record-reader-Dd35fnKn.js` | `b7a2d61fcc1b80650a3452bdd80354b90fd81889fc0a7aa8d211f6c673b42170` |
| `dist/installed-plugin-index-store-CWgFGnm0.js` | `0d7bfad658ef322012b9b68b9709620bca8c0b202046f6f3d623ed7d31fc7a18` |
| `dist/installed-plugin-index-records-C_n191FN.js` | `61486eb810bb4ad4542bec9ac37f46b1612317f5b7e65a0bf71aa3740b4a409b` |
| `dist/plugin-registry-8E8D2Hou.js` | `570f856a8f4e517d8bf0e0d768bcf691eaf9bf44b9f8e560c8f86ff8a7cef983` |
| `dist/status-snapshot-lNsJCo4p.js` | `f14f0f8f7b9847b20718e6d53824894fe81c22879166984bc61016e626ab554f` |
| `dist/plugins-list-command-0fMcQYzj.js` | `d9bfcd6aeb9bc13d8af0c9ae17fca7714199839ed00397fef43fa4f640148a6a` |
| `dist/installed-plugin-index-types-BU7TbVqB.d.ts` | `a3b4990acd64f6d37372803f627e82e162151f5812674d530f159f24d4816353` |

## Exact lifecycle trace

### Loader identity

CNX-393/394 source evidence remains unchanged: `loader-D8d2EvVh.js:1640,1663-1666` associates a candidate by `rootDir` to `manifestRecord`, then assigns `pluginId = manifestRecord.id`; `:1730` looks up `normalized.entries[pluginId]`; `:1731-1753` creates the live record; and `:2237-2242` passes `entry?.hooks` to `createApi`. This is live-loader identity evidence, not index evidence.

### Index derivation and record fields

In the exact installed index module:

- `installed-plugin-index-N4jxqS0-.js:1407-1439` resolves candidates using discovery and install records, then builds a manifest registry. With supplied candidates, it still loads the manifest registry; without them it discovers from configured load paths and install records.
- `:1494-1526` builds the index, setting `generatedAtMs` from the refresh call and creating records from the manifest registry.
- `:1348-1403` maps each manifest `record`; `:1352-1356` looks up its candidate and install record; `:1370-1376` resolves enablement; and `:1377-1385` stores `pluginId: record.id`, `source: record.source`, `rootDir: record.rootDir`, `origin: record.origin`, and `enabled`.
- Thus the normal index-population input is a manifest-registry record ID, not a passed live loader record. The source does not pass the live loader's runtime `record` object into the index builder.

### Persistence and update paths

- `installed-plugin-index-store-CWgFGnm0.js:188-235` writes the index to the shared SQLite `installed_plugin_index` row. It persists `generated_at_ms`, `refresh_reason`, install records, plugin records, diagnostics, and `updated_at_ms`; `updated_at_ms` is a write-time `Date.now()` value.
- `:237-255` reads/writes the SQLite-backed store and clears metadata/install-record caches after writes.
- `:308-334` refreshes either by a policy-only transformation (`:310-313`, preserving plugin records and changing enablement/policy timestamp) or by `refreshInstalledPluginIndex` (`:315-320`, `:329-334`) followed by persistence.
- `installed-plugin-index-records-C_n191FN.js:65-81` exposes install-record writes. It calls the refresh path with `reason: "source-changed"` and only an install-record map; it does not receive a live loader record or `manifestRecord.id`.
- `plugins-install-record-commit-C0KU6nk2.js:139-167` invokes that install-record path during install-record commit and can roll back the install record. This is an install lifecycle, separate from live activation.
- `plugin-registry-migration-dr1xeVEY.js:180` writes migrated index state; `state-migrations-DhegLvJn.js:2215,2230` writes migration results. These are additional non-loader population/update contexts.
- `update-cli-CnCrJkiC.js:2834` updates install records during update processing; `missing-configured-plugin-install-CfQlXKsN.js:1288-1289` updates records during missing-configured-plugin recovery.

### Persisted versus derived selection

`plugin-registry-8E8D2Hou.js:326-410` implements `loadPluginRegistrySnapshotWithMetadata`:

1. A supplied `params.index` wins (`:327-331`), labelled `provided`.
2. A current memoized snapshot can win (`:332-337`), subject to its fingerprint inputs.
3. Unless caller preference or `OPENCLAW_DISABLE_PERSISTED_PLUGIN_REGISTRY` disables it (`:339-342`), the persisted SQLite index is read (`:343-345`). It is selected as `persisted` only when policy hash, source paths, diagnostics, startup metadata, manifest/package signatures, and recoverable install records pass the checks (`:346-390`).
4. Otherwise, or when disabled, the code calls `loadInstalledPluginIndexWithDiscovery` (`:401-410`), labelled `derived`.

The derived path is not the live activation registry. `installed-plugin-index-N4jxqS0-.js:1407-1439` obtains discovery candidates, install records, and a manifest registry; `:1494-1533` builds records from that data. Both persisted and derived paths preserve `pluginId` as an index field; neither path serializes the live runtime hook registry.

### `plugins list --json`

`status-snapshot-lNsJCo4p.js:89-110` loads the snapshot metadata and maps each snapshot plugin through `buildPluginRecordFromInstalledIndex`; `:36-86` creates a new inventory object. It takes `id` from `plugin.pluginId` (`:40`), source/root/origin from index fields (`:47-49`), derives status from `plugin.enabled` (`:53`), and initializes `hookNames=[]` and `hookCount=0` (`:55,78`). `plugins-list-command-0fMcQYzj.js:25-42` serializes that report. This remains separate from live loader identity and typed-hook state.

## Provenance table

| Index path | Input identity | Stored `pluginId` | Root/source | Trigger/context | Direct loader linkage |
|---|---|---|---|---|---|
| A — full index refresh/derived build | manifest-registry `record.id` from discovery candidates and root-associated manifest records | `record.id` at `installed-plugin-index-N4jxqS0-.js:1377-1379` | `record.rootDir`, `record.source`, `record.origin` at `:1382-1385`; manifest/package hashes also stored | registry refresh, discovery/config processing, or explicit registry refresh | **no direct linkage observed**; same value may be produced by equivalent loader logic, but no live record is passed |
| B — policy-only persisted refresh | existing persisted index plugin object; no loader identity | existing `plugin.pluginId` preserved at `installed-plugin-index-store-CWgFGnm0.js:272-285`; only enablement/policy metadata changes | existing root/source/origin preserved by spread at `:271-277` | policy change | **no** |
| C — install/update/migration record path | install-record map keyed by caller-supplied plugin ID; no loader record | install records are keyed by `pluginId` at `installed-plugin-index-record-reader-Dd35fnKn.js:126-150,163-169`; full index later uses manifest `record.id` | install/source metadata and later manifest-derived fields | install, update, missing-config recovery, migration | **no** |

Equal strings do not establish object identity or contemporaneous lifecycle linkage.

## Production read-only correlation

The supported `openclaw plugins list --json` capture reported registry source `persisted` and target:

- `id/pluginId`: `cogentnexus-openclaw`
- source: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
- rootDir: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw`
- origin: `global`
- status: `loaded`
- enabled: `true`
- hookCount: `0`, hookNames: `[]`

Read-only SQLite inspection used `C:\Users\CDQ-P\.openclaw\state\openclaw.sqlite` with `mode=ro` and found table `installed_plugin_index`. Target row metadata:

- schema/version: `version=1`
- host contract: `2026.7.1-2`
- migration version: `1`
- refresh reason: `policy-changed`
- generatedAtMs: `1789564034051` = `2026-09-16T13:07:14.051Z`
- updatedAtMs: `1789564034052` = `2026-09-16T13:07:14.052Z`
- target manifest file signature: size `8393`, mtime/ctime about `2026-09-16T12:32:24.758Z`
- target package.json signature: size `1051`, mtime/ctime about `2026-09-16T12:32:24.773Z`
- target manifest hash: `96ac29ff7dab03a3203d39c03837d8957a1a7008c20576496451e5fb5a10b2a5`
- target source/root/origin: as listed above
- target install record hash: `b4f71bc022a3b3ce4ad868127d3da7892ab22ccc05481ed0d55fbad22d51c6b5`

Current gateway process read-only observation:

- PID: `27372`
- command: `node ... openclaw ... gateway --port 18789`
- CreationDate: `1789596828606` = `2026-09-17T10:13:08.606Z`

The index was therefore written before the current gateway started. This is direct evidence that the current gateway did not create this row during its current startup. It does not exclude a later policy-only update in another process, but the stored `refresh_reason=policy-changed` and the source path show a path that can update the row without live loader activation.

Production config read-only correlation remains `plugins.entries.cogentnexus-openclaw.enabled=true` and `hooks.allowConversationAccess=true`; config hash is the known baseline above. No secret was printed.

## Isolated provenance probe

No new plugin was installed and no production path was touched. The exact installed source was exercised at mechanism level by tracing the shipped functions and by inspecting the repository's disposable installed-index test coverage (`src/plugins/installed-plugin-index.test.ts` and `src/plugins/installed-plugin-index-store.test.ts`, including the record-builder and persistence cases). The decisive source path is observable without production instrumentation: the full builder receives a manifest-registry record and stores `record.id`; the policy-only and install-record writers have no loader-record parameter. A new runtime fixture was not needed to establish the source mechanism, and no synthetic result is presented as historical production evidence.

## Direct evidence versus inference

**Direct:** exact remote SHA; installed module hashes; source line mappings above; persisted SQLite source; persisted row version/reason/timestamps; target identity/root/source/origin; gateway PID/start time; supported inventory source `persisted`; config key and non-secret values; write/update call sites.

**Inference:** the persisted target is consistent with the intended production loader identity and current artifact because IDs, paths, and hashes align. It is not proof of the same runtime object or of a current-loader write. The pre-start timestamp proves the current gateway did not create it during startup; it does not prove no later unrelated process refreshed it.

## Effect on CNX-394 identity gap

CNX-394's gap is reduced from “the inventory ID may be a separate projection” to a stronger result: the projection has a documented, persisted, identity-bearing record and a separate discovery-derived builder, but its population input is manifest-registry/discovery data or prior index data—not a live loader record. The production row predates the current gateway and carries `refresh_reason=policy-changed`. The gap is therefore **not closed**: no contemporaneous correlation to the current production loader's `manifestRecord.id` is possible from this evidence.

## Comparison with CNX-391 through CNX-394

- **CNX-391:** isolated exact config-origin loader/API replay accepted `allowConversationAccess=true`; this remains isolated mechanism evidence and is not replaced by index data.
- **CNX-392:** `origin=global` versus `origin=config` does not itself select a different conversation-hook policy branch; this report adds that index refresh paths also do not consume a live loader record.
- **CNX-393:** the loader association chain remains `candidate.rootDir → manifestRecord.id → normalized.entries[pluginId] → entry.hooks`; the index builder instead receives manifest-registry records/discovery data and stores `record.id`.
- **CNX-394:** `plugins list --json` remains a separate installed-index projection; zero/empty hook fields are projection defaults, not live typed-hook evidence.
- **CNX-395:** the target row is proven preexisting to the current gateway and independently refreshable from policy/install/migration/discovery lifecycles. Direct contemporaneous loader provenance is not established.

No production hook acceptance/rejection, registry-composition loss, or Dashboard Ticket-first semantic success is claimed.

## Counts and hard-fence compliance

- Semantic/model/provider/Dashboard requests: **0**
- Production mutation count: **0**
- Gateway restart/reload: `0`
- Production config/environment/Scheduled Task mutation: `0`
- Production extension install/mutation or artifact replacement: `0`
- OpenClaw dependency patch: `0`
- CogentNexus source repair/artifact rebuild: `0`
- Debugger/inspector attachment: `0`
- Permanent instrumentation: `0`
- Historical CNX-360 through CNX-394 edits: `0`
- Release/tag/main changes: `0`
- Force-push/history rewrite: `0`
- CNX-396 created/started: `0`

## Closeout

After this report is published, `ACTIVE.md` and `STATUS.md` are set to `WAITING_FOR_CHATGPT_REVIEW`. No successor task is created or started. Execution stops for review.
