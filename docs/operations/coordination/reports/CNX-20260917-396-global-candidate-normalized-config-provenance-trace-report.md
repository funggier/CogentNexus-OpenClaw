# CNX-20260917-396 — Global Candidate Normalized-Config Provenance Trace Report

## Classification

`GLOBAL_CONFIG_NORMALIZATION_DIAGNOSTICALLY_BLOCKED`

The exact installed source proves one common normalized configuration producer and one common lookup/policy path for `origin=config` and `origin=global`; it does not provide a safe exact global-origin A/B replay under the hard fences. Therefore equivalence is strong mechanism evidence, not historical proof of the already-running production Gateway.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Authoritative starting HEAD: `d35421bf26189c8ccc8e43df66cdeaa12706c752`
- Authoritative final HEAD: recorded after publication and remote verification
- Starting gate: `READY_FOR_HERMES`
- Task: `CNX-20260917-396`
- Parent: `CNX-20260917-395`

GitHub was fetched first. The local checkout was reset to the fetched remote tip, and both local and `git ls-remote` matched the starting SHA. ACTIVE, STATUS, CNX-396, and CNX-391 through CNX-395 were re-read before investigation.

## Runtime identity and hashes

- OpenClaw: `2026.7.1-2 (0790d9f)`
- Effective artifact: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
- Effective artifact SHA-256: `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- Production config SHA-256: `19d7e6acf53ce370ddc20e5e2a2547c9674c33b178208b79920cb0e9dce9b46b`

| Module | SHA-256 |
|---|---|
| `dist/loader-D8d2EvVh.js` | `3a10479bdcbb713692c3ded7dbd5baad27c1b17ae3566172c117d45916dabce7` |
| `dist/config-normalization-shared-w2iz0aeC.js` | `c3b7bccc26f72ac0ab79ef0635daaa5931d23f86d9bc7e21f4ae8b60ce80f7c2` |
| `dist/discovery-7zi_zNvu.js` | `5489a4b1086fed443cedf54efccc76a730960e8419bba4d97010c3420a342ddd` |
| `dist/registry-B8eQDFB4.js` | `25f3ef82756d85281ad5c25375a5cd2f405989a1145ed438de05992e8c995376` |

## Exact normalized producer and lifetime

The loader function in `loader-D8d2EvVh.js` calls `resolvePluginLoadCacheContext` for a load invocation. At `1189-1201`, it selects `options.config` (or `{}`), resolves the activation-source config, applies environment resolution/defaults when requested, and then executes `const normalized = normalizePluginsConfig(cfg.plugins)` at `1201`. The resulting object is local to that loader invocation and is shared by the subsequent candidate loop; it is not rebuilt per candidate.

The producer is `normalizePluginsConfigWithResolver` (exported as `i`) in `config-normalization-shared-w2iz0aeC.js:314-325`. It constructs one object containing normalized `enabled`, `allow`, `deny`, `loadPaths`, `slots`, and `entries`. `normalizePluginEntries` at `253-310` creates a fresh `normalized` map, normalizes each key through `normalizePluginId`, and assigns `normalized[normalizedKey]` from the config entry.

For hooks, `normalizePluginEntries:263-279` reads `entry.hooks`, retains boolean `allowConversationAccess` at `268`, and includes it in `normalizedHooks` at `272-279` only when it is boolean. The final entry assignment at `302-309` stores `hooks: normalizedHooks` and preserves `config` only from the input entry. Thus the production value enters the normalized structure from `cfg.plugins.entries[<key>].hooks.allowConversationAccess`; it is not read from the executable plugin definition or from candidate origin.

## Exact backward trace from `normalized.entries[pluginId]`

At `loader-D8d2EvVh.js:1730`:

```text
entry = normalized.entries[pluginId]
```

The preceding path is:

```text
cfg.plugins
  -> normalizePluginsConfig(cfg.plugins)                    (loader:1201)
  -> normalizePluginsConfigWithResolver                    (shared:314-325)
  -> normalizePluginEntries(cfg.plugins.entries, resolver) (shared:325, 253-310)
  -> normalized.entries[pluginId]
```

The candidate identity path is:

```text
candidate.rootDir
  -> manifestByRoot.get(candidate.rootDir)                  (loader:1640, 1664)
  -> manifestRecord.id                                     (loader:1666)
  -> pluginId
  -> normalized.entries[pluginId]                          (loader:1730)
```

`manifestByRoot` is keyed by `rootDir`, not by discovery `idHint`, filename, or config key. Missing manifest records are skipped at `1665`. Duplicate effective IDs are handled by `seenIds` at `1650` and `1689-1720`; a later duplicate is disabled as overridden before the ordinary lookup. The scoped filter `matchesScopedPluginOrDreamingSidecar` is evaluated at `1667-1672` before activation and lookup.

After lookup, enablement is resolved at `1679-1687` and again used to build the record at `1729-1753`. Registration planning is at `1794-1808`; null plans return before registration at `1809-1815`. `registrationMode` is assigned from `registrationPlan.mode` at `1817`, not directly from origin. The ordinary API construction at `2237-2242` passes `pluginConfig: validatedConfig.value`, `hookPolicy: entry?.hooks`, and `registrationMode` to `createApi`. The setup branch passes the same `entry?.hooks` at `1994-1999`.

## Global versus config candidate paths

Discovery assigns `origin: "config"` to configured load paths at `discovery-7zi_zNvu.js:1231-1242`. Installed paths and the global directory scan assign `origin: "global"` at `1368-1395`. Both produce candidate records through the same discovery machinery and carry `rootDir`, source, manifest metadata, and origin.

The loader then uses the same `manifestByRoot` association, same `manifestRecord.id` assignment, same normalized object, same effective enablement resolver, same duplicate-ID map, same scoped filtering, same registration-plan resolver, and same `entry?.hooks` API input for both origins. Origin is passed as metadata and affects explicit origin predicates in some unrelated setup/trust decisions; the inspected conversation-policy path has no `global`-specific normalized configuration source.

The source also proves that `registrationMode` comes from the registration plan. The plan may inspect candidate origin for specific setup-only conditions, but no inspected line makes `origin=global` select a different `normalized` object or a different `hooks` entry. The direct conversation gate in `registry-B8eQDFB4.js:4180-4250`, especially `4226-4235`, treats both `config` and `global` as non-bundled and checks `policy?.allowConversationAccess === true`; it does not branch between those two origins.

## Plugin-ID correlation and policy provenance

For the target plugin, the exact source correlation is:

```text
configured load path or installed/global path
  -> candidate.rootDir
  -> manifestByRoot.get(candidate.rootDir)
  -> manifestRecord.id = "cogentnexus-openclaw" (if manifest says so)
  -> pluginId = "cogentnexus-openclaw"
  -> normalized.entries["cogentnexus-openclaw"]
  -> entry.hooks.allowConversationAccess
  -> createApi({ hookPolicy: entry?.hooks })
```

For both origins, the value source is the same normalized config map created from `cfg.plugins.entries`. The config key is normalized by the supplied plugin-ID resolver before map insertion. A manifest ID mismatch, missing normalized entry, duplicate-ID override, disabled activation, or absent `registrationPlan` can still prevent the value from reaching API registration. Matching displayed IDs in inventory are not used as proof that the live lookup succeeded.

## Isolated A/B probe

No exact global-origin A/B probe was executed. Reproducing the real `origin=global` discovery path would require using the production global installation/extension-tree or mutating its installation metadata. A relocated temporary copy would not be the same global discovery mechanism and would fabricate the decisive condition. No OpenClaw or CogentNexus source was patched, no permanent instrumentation was added, and no production installation was changed.

The available exact isolated mechanism evidence is CNX-391: the production-shaped config-origin replay supplied `allowConversationAccess=true` through the real loader/API path and accepted conversation hooks; its false control omitted them. That proves the common downstream policy contract, not historical production global consumption.

## Production read-only observation

The supported production inventory remains the previously recorded projection: `id=cogentnexus-openclaw`, `origin=global`, `status=loaded`, `hookCount=0`, `hookNames=[]`. The installed index is persisted state, predates the current Gateway, and is not live typed-hook state per CNX-394/CNX-395. No Gateway PID was safely correlated to a loader-internal normalized object in this read-only pass. No restart, reload, retry, semantic request, or debugger attachment occurred.

## Predecessor comparison

- **CNX-391:** exact config-origin replay accepted `allowConversationAccess=true` through the real loader/API lifecycle.
- **CNX-392:** global/config origin does not directly choose a different downstream conversation-hook policy branch; `registrationMode` comes from registration planning rather than directly from origin.
- **CNX-393:** source chain reaches `candidate.rootDir → manifestRecord.id → normalized.entries[pluginId]`, but production live values were not observable.
- **CNX-394:** inventory is an installed-index projection; hook fields are not live typed-hook state.
- **CNX-395:** the installed index is persisted SQLite state predating the current Gateway and can refresh without a live loader record.
- **CNX-396:** the common normalized producer and lookup path are proven statically; exact global-origin runtime equivalence remains diagnostically blocked.

## Direct evidence versus inference

**Direct evidence:** exact module hashes and version; normalization function and line ranges; field preservation/defaulting behavior; loader-local normalized object construction; root-to-manifest association; manifest-ID assignment; filtering, deduplication, enablement, and registration-plan ordering; `entry?.hooks` passed to `createApi`; and the common non-bundled host policy branch.

**Inference:** global and config candidates should consume the same normalized entry when they resolve to the same manifest ID in the same loader invocation. This is mechanism evidence only. It is not proof that the already-running production global candidate had that ID, found that entry, remained enabled, or reached `createApi`.

## Effect on the remaining production gap

The origin-only divergence hypothesis is weakened: source shows no separate global normalized-config producer and no global-specific conversation policy branch. The remaining gap is earlier runtime provenance/activation: whether production's global candidate was associated with `manifestRecord.id = cogentnexus-openclaw`, whether the normalized entry existed in that process, and whether filtering, enablement, duplicate precedence, or registration planning stopped it before `createApi`. This report does not claim production hook acceptance or rejection, registry-composition loss, or Dashboard Ticket-first semantic success.

## Counts and hard-fence compliance

- Semantic/model/provider/Dashboard requests: `0`
- Production mutation count: `0`
- Production Gateway restart/reload: `0`
- Production config/environment/Scheduled Task mutation: `0`
- Production global extension installation/mutation: `0`
- Artifact replacement/deploy/rebuild: `0`
- OpenClaw dependency patch: `0`
- CogentNexus source repair: `0`
- Debugger/inspector attachment: `0`
- Permanent instrumentation: `0`
- Historical CNX-360 through CNX-395 modifications: `0`
- Release/tag/main changes: `0`
- Force-push/history rewrite: `0`
- CNX-397 created/started: `0`

## Closeout

After this report is published, ACTIVE.md and STATUS.md will be set to `WAITING_FOR_CHATGPT_REVIEW`. No successor task will be created or started. Execution stops after final remote verification.
