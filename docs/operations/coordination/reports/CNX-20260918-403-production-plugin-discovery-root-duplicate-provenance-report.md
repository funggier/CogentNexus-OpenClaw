# CNX-20260918-403 — Production Plugin Discovery Root and Duplicate Candidate Provenance Report

## Classification

`PRODUCTION_PLUGIN_DISCOVERY_INCONCLUSIVE`

Read-only evidence identifies one manifest-selected CogentNexus root in the supported persisted inventory and one corresponding global extension root on disk. It does not prove that the persisted `plugins list --json` projection is the complete historical live discovery candidate set for PID 27372, nor does it expose the loader's invocation-local candidate array. No second same-ID production candidate was directly observed, but `UNIQUE_ROOT_PROVEN` is not claimed because installed-index provenance and live discovery candidates are distinct boundaries.

## Authority and exact starting identity

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Task: `CNX-20260918-403`
- Expected baseline supplied by task: `f1cbe0e0258a2dc508187335f8c790f3a03d1b76`
- Exact authoritative starting local HEAD after fetch: `f1cbe0e0258a2dc508187335f8c790f3a03d1b76`
- Exact authoritative starting GitHub HEAD: `f1cbe0e0258a2dc508187335f8c790f3a03d1b76`
- Starting gate: `READY_FOR_HERMES`

GitHub was fetched with an explicit branch refspec and `git ls-remote` matched the checked-out starting HEAD. ACTIVE, STATUS, CNX-403, CNX-402, corrected CNX-401, CNX-400, CNX-399, and CNX-398 through CNX-391 were read. The checkout was clean. No historical report was modified.

## Exact runtime and hashes

OpenClaw: `2026.7.1-2 (0790d9f)`.

Installed OpenClaw module root:
`C:\Users\CDQ-P\.openclaw\workspace\test\CogentNexus-OpenClaw\plugins\cogentnexus-openclaw\node_modules\openclaw\dist`

| Module | SHA-256 |
|---|---|
| `discovery-7zi_zNvu.js` | `5489a4b1086fed443cedf54efccc76a730960e8419bba4d97010c3420a342ddd` |
| `loader-D8d2EvVh.js` | `3a10479bdcbb713692c3ded7dbd5baad27c1b17ae3566172c117d45916dabce7` |
| `manifest-registry--UiRn6nq.js` | `819c76c314e6ed1fd39c5ed6b169d63997905b3ae8a98b9373783d626431ace4` |
| `roots-BmJakFIf.js` | `03924457839e9a99c585d9490d961157f615da1402182f16778d63cd02e1da3d` |

Corrected production artifact identity from CNX-402:

- Declared entry: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
- SHA-256: `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- Size: `8,596` bytes

Observed alternate on-disk artifact, not treated as selected:

- `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-dashboard-verified-delivery.js`
- SHA-256: `1276bd624b62f96692eaa19f493f69e422771b6994b39ded94b2bcb3399e1f98`
- Size: `39,760` bytes

The two files are byte-different. The installed package manifest declares only `./dist/v091-release-entry.js` under `openclaw.extensions`.

## Exact discovery source mapping

### Root derivation

`roots-BmJakFIf.js:6-15`, `resolvePluginSourceRoots(params)`, returns:

- `stock`: `resolveBundledPluginsDir(env)`
- `global`: `path.join(resolveConfigDir(env), "extensions")`
- `workspace`: `path.join(workspaceRoot, ".openclaw", "extensions")` when `workspaceDir` is supplied

`resolvePluginCacheInputs` in the same module also resolves configured `loadPaths` from the loader context.

### Discovery domains and origins

`discovery-7zi_zNvu.js:1267-1400`, `discoverOpenClawPlugins(params)`, creates separate scoped and shared discovery results:

- configured `extraPaths` / `plugins.load.paths` are sent to `discoverConfiguredPluginLoadPathsInto` with origin `config` (`:1280-1290` and `:1193-1230`);
- workspace root is scanned only when it exists and does not resolve to the bundled root (`:1291-1303`), with origin `workspace`;
- bundled source overlays and the stock bundled root are scanned with origin `bundled` (`:1309-1350`);
- installed/index-derived paths are collected by `collectInstalledPluginRecordPaths` and scanned with origin `global`, with `scanFiles: true` (`:1365-1382`);
- the canonical global root is scanned with origin `global`, while installed plugin directory keys are passed as `skipRootDirKeys` (`:1383-1395`).

The source therefore makes installed/index paths a discovery input/provenance source, not automatically the live registry. It also explicitly avoids rescanning installed managed directories through the ordinary global-root scan when their canonical keys are in `skipRootDirKeys`.

`discoverFromPath` / `discoverInDirectory` (same discovery module, preceding the exported function) canonicalize the path through the realpath cache and associate package manifests before candidate creation. The candidate carries `rootDir`, `source`, `origin`, workspace context, and manifest association. A directory name alone is not a candidate identity.

### Root → manifest association and pre-API candidate selection

`loader-D8d2EvVh.js:1640-1666` constructs:

```text
manifestByRoot = new Map(manifestRegistry.plugins.map(record => [record.rootDir, record]))
orderedCandidates = discovery.candidates.toSorted(compareDuplicateCandidateOrder)
for candidate:
  manifestRecord = manifestByRoot.get(candidate.rootDir)
  if (!manifestRecord) continue
  pluginId = manifestRecord.id
  scope filter / activation state / enablement follow
```

Thus missing or non-canonical `rootDir` association skips the candidate before normalized entry lookup. The plugin ID is taken from the manifest record, not inferred from the path or filename.

`compareDuplicateCandidateOrder` is `loader-D8d2EvVh.js:201-235`. `resolveCandidateDuplicateRank` ranks candidates as:

1. `config`: rank 0
2. bundled inside development source root: rank 1
3. explicit installed global candidate: rank 2
4. other bundled: rank 3
5. workspace: rank 4
6. other: rank 5

The comparator only orders candidates whose `manifestByRoot` IDs are equal (`:220-223`). Ordering inputs include candidate origin, manifest-associated ID, provenance install rules, source path, environment, and bundled-source-root status.

### `seenIds` and override semantics

`loader-D8d2EvVh.js:1650-1663` creates invocation-local `seenIds` and iterates the sorted candidates. The duplicate branch begins at `:1691`. An overridden duplicate is materialized as a disabled plugin record with `status = "disabled"`, `error = "overridden by <existingOrigin> plugin"`, and `enabled: false` (`:1692-1720` and following record construction). It is retained as a disabled record; it is not registered.

The candidate that wins precedence owns the record slot and is the one eligible for subsequent normalized entry lookup, enablement, module load, `createApi`, and `register(api)`. Therefore, if two actual same-ID candidates enter the live discovery array with different origins/ranks, source mechanism can change which code reaches registration. That is mechanism evidence only; it is not evidence that two such production candidates existed for PID 27372.

The same loader module has a separate CLI/metadata registry path around `:2397-2673`; it repeats manifest association and duplicate processing but is not proof of the Gateway's historical live loader candidate array.

## Production root inventory

The production configuration read-only projection showed:

- `workspace`: absent/null
- `plugins.load.paths`: absent; `openclaw config get plugins.load.paths --json` reported the path was not found
- `plugins.entries.cogentnexus-openclaw.enabled`: `true`
- `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess`: `true`
- configured plugin `workspaceDir`: `C:\Users\CDQ-P\.openclaw\workspace` inside plugin config, but top-level resolver workspace was not supplied by the supported config projection used here

Exact resolver roots evaluated from the installed environment:

| Resolver domain | Absolute path | Exists | CogentNexus candidate | Origin | Result |
|---|---|---:|---|---|---|
| canonical global root | `C:\Users\CDQ-P\.openclaw\extensions` | yes | `...\extensions\cogentnexus-openclaw` | `global` | one relevant installed root observed |
| workspace root derived from top-level workspace | `C:\Users\CDQ-P\.openclaw\workspace\.openclaw\extensions` | no | none | `workspace` | no candidate observed |
| configured load paths | none returned | N/A | none observed | `config` | no configured path observed |
| stock bundled root | `C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\dist\extensions` | yes | no `cogentnexus-openclaw` directory observed | `bundled` | no same-ID candidate observed |
| installed/index-derived paths | loader supports them | not exposed as a live list | not directly enumerable from supported projection | `global` | provenance boundary unresolved |

The global extension directory also contained `.openclaw-install-backups` and the CogentNexus directory. The backup directory was not treated as a candidate root: the exact resolver's global discovery path operates on child plugin directories and the installed/managed skip rules; no manifest-bearing CogentNexus candidate was observed there. No unrelated user-data recursive scan was performed.

### Candidate/manifest/ID table

| Candidate/root | source entry | origin | manifest ID | version | declared extension entry | SHA-256 | status/evidence |
|---|---|---|---|---|---|---|---|
| `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw` | `...\dist\v091-release-entry.js` | `global` | `cogentnexus-openclaw` | `0.9.5` | `./dist/v091-release-entry.js` | `2841b704...c2d95` | supported persisted inventory: `loaded`, enabled |
| same root, alternate file | `...\dist\v091-dashboard-verified-delivery.js` | not separately reported as a candidate | no separate manifest association | N/A | not declared in package manifest | `1276bd...` | on-disk alternate only; discovery participation unproven |

The supported `openclaw plugins list --json` response contained exactly one record with `id = cogentnexus-openclaw`, source `...\dist\v091-release-entry.js`, rootDir `...\extensions\cogentnexus-openclaw`, origin `global`, version `0.9.5`, enabled `true`, status `loaded`. Its registry header was `source: persisted`, `diagnostics: []`. This is a persisted/derived projection, not a live candidate-array trace.

## Duplicate analysis

Directly observed same-ID candidates: `0`.

Directly observed production CogentNexus candidate roots: `1` in the supported inventory, corresponding to the canonical global extension root. The installed/index-derived path, if it resolves to this same root, is intentionally de-duplicated by the loader's managed-directory and `skipRootDirKeys` logic; no second root was exposed by the supported projection.

No root/manifest/ID mismatch was directly observed for the selected root:

- rootDir resolves to the global extension directory;
- package manifest ID is `cogentnexus-openclaw`;
- package version is `0.9.5`;
- package extension entry is `./dist/v091-release-entry.js`;
- the selected entry hash matches CNX-402's corrected production baseline;
- `plugins.entries.cogentnexus-openclaw` is enabled and has the required hook policy.

The dashboard artifact is not a second manifest-selected candidate. Its existence inside the same root does not create a second candidate because the package manifest declares only the release entry and the supported inventory names only that entry.

Source proves duplicate precedence could alter registration if a second same-ID candidate were actually in the discovery array. Ordering can differ across lifecycle contexts when `extraPaths`, installed provenance rules, origin, workspace, environment, or bundled source-root conditions differ. No production telemetry binds those per-invocation inputs or exposes `orderedCandidates`.

## Installed-index distinction

CNX-394/395 established that the supported inventory is a persisted/derived installed-index projection. CNX-395 recorded the relevant row refresh as `policy-changed` at `2026-09-16T13:07:14.051Z`/`.052Z`, before PID 27372 creation (`2026-09-17T10:13:08.606Z`). The exact source uses installed records to build provenance/install rules and to supply installed paths into discovery (`discovery:1365-1382`, loader provenance construction around `:1635-1640`). That is a candidate-input relationship, not proof that an index row equals a live typed-hook registry or that its path was selected in the historical Gateway invocation.

The `plugins list --json` result's `registry.source = persisted` reinforces this boundary. It cannot prove the live Gateway's candidate array, duplicate ordering, `seenIds`, or registration winner.

## Production process and chronology

Read-only PID evidence:

- PID: `27372`
- executable: `C:\Program Files\nodejs\node.exe`
- command line: `"C:\Program Files\nodejs\node.exe" C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\dist\index.js gateway --port 18789`
- OpenClaw version: `2026.7.1-2 (0790d9f)`

The inherited chronology is process creation → config load → first discovery → `hook-registered` at `05:13:58.242` → server listening → Gateway ready → later discovery/prewarm-labelled activity → `hook-registered` at `05:14:10.542`. The timestamps do not expose candidate roots, origin, ordering inputs, duplicate selection, or the selected source path for either registration event.

The corrected production artifact is the manifest-selected release entry. The dashboard file has no direct discovery participation evidence. This does not prove that the live process never loaded another candidate; it shows only that no supported read-only evidence currently binds one.

## Isolated probe

No isolated loader/discovery probe was run. The installed public surface exposes discovery invocation but does not expose the private production candidate array and registry identity without instrumenting or patching OpenClaw. A synthetic relocated fixture could demonstrate comparator ranks but would not establish production roots and was not used as production evidence. The exact source mapping above is sufficient to prove the duplicate-selection mechanism without fabricating a production result.

## Required conclusions

1. **Relevant production roots:** one directly observed manifest-bearing CogentNexus root in the supported inventory: the canonical global extension root. Completeness of the historical live candidate set is not proven because the inventory is persisted and installed-path records are not exposed as a live candidate list.
2. **Same-ID candidates:** zero directly observed; one persisted/derived inventory record.
3. **Selected winner:** the supported selected projection is the global root with `v091-release-entry.js` / `2841b704...c2d95`. Historical live-loader winner is not independently proven.
4. **Duplicate precedence:** yes, source proves precedence can change which candidate reaches registration when same-ID candidates enter the candidate array; no production duplicate was observed.
5. **Root/manifest/ID mismatch:** none directly observed for the selected root. The alternate dashboard file is an artifact mismatch/unselected file, not a second manifest candidate.
6. **Dashboard discovery participation:** not proven; direct evidence instead shows it is not the manifest-selected extension entry.
7. **Hypothesis impact:** materially reduces the duplicate-root hypothesis for the currently supported production projection, but cannot eliminate it for the historical live invocation because candidate arrays and installed-path provenance were not captured per PID/invocation.
8. **Remaining production evidence:** PID-correlated live discovery candidate list, root/origin/manifest mapping, installed-path records used by that invocation, duplicate comparator inputs and winner, loader invocation ID, and registration source identity.

The missing `before_agent_run` explanation is therefore narrowed from an unbounded duplicate-file theory to a conditional mechanism: a duplicate can matter only if a second same-ID candidate entered the live discovery array and won precedence. Current production evidence does not prove that condition. Registry replacement/cache restoration from CNX-401 remains source-proven and separately unresolved in production.

## Direct evidence versus inference

**Direct:** exact source lines and hashes; resolver root derivation; config projection; filesystem existence; package manifest and declared entry; both artifact hashes; one supported persisted inventory record; PID/version/command line; and prior chronology.

**Inference/limitation:** absence of a second candidate in a persisted inventory and absence of a configured path do not prove absence from the historical live candidate array. The dashboard file's presence does not establish discovery participation. No production duplicate-selection event is claimed.

## Counts and hard-fence compliance

- Production mutations: `0`
- Semantic/model/provider/Dashboard requests: `0`
- Gateway restart/reload: `0`
- Production config/environment/Scheduled Task mutation: `0`
- Production global extension installation/mutation: `0`
- Artifact replacement/deploy/rename/copy-over: `0`
- OpenClaw dependency patch: `0`
- CogentNexus source repair: `0`
- Debugger/inspector attachment: `0`
- Permanent instrumentation: `0`
- TicketStore/admission/routing/auth changes: `0`
- Historical CNX-360 through CNX-402 edits: `0`
- Release/tag/main changes: `0`
- Force-push/history rewrite: `0`
- CNX-404 created/started: `0`
- Retained temporary probe files: `0`

## Closeout

This report is the only new report artifact. ACTIVE.md and STATUS.md are set to `WAITING_FOR_CHATGPT_REVIEW` after publication. No CNX-404 was created or started.
