# CNX-20260917-393 — Global Discovery / Config-Entry Association Trace Report

## Classification

`GLOBAL_CONFIG_ENTRY_ASSOCIATION_DIAGNOSTICALLY_BLOCKED`

The exact installed source proves the loader's association algorithm: the candidate is first associated to a manifest record by `rootDir`, the effective `pluginId` is then `manifestRecord.id`, and the configuration object is selected by the exact statement `entry = normalized.entries[pluginId]`. `createApi` receives `hookPolicy: entry?.hooks`. There is no origin-specific lookup branch in this path. A production/global-origin candidate can nevertheless receive no policy if its manifest ID does not equal the normalized configuration key, or if the normalized entry is absent; source alone cannot establish whether that occurred in the already-running production process. The required exact global-origin disposable replay is blocked by the hard fence against mutating/installing in the production global extension tree. No global substitute was fabricated.

This report does not claim production hook acceptance/rejection, registry-composition loss, or Dashboard Ticket-first semantic success.

## Authority and closeout

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Authoritative starting HEAD: `5d0fed22d90dc1a7b099219457f54dcd85a1adff`
- Authoritative final HEAD: recorded after publication and remote read-back
- Starting gate: `READY_FOR_HERMES`
- Task: `CNX-20260917-393`
- Parent: `CNX-20260917-392`

Remote was fetched with an explicit branch refspec and the working branch was checked out at the requested remote tip before reading the authority files. Historical CNX-360 through CNX-392 files were not edited.

## Exact runtime, artifact, and module identity

Installed OpenClaw `2026.7.1-2 (0790d9f)` was inspected read-only from the installed module graph used by the predecessor probes. Node runtime in predecessor exact-loader evidence: `v22.23.2`.

| Item | SHA-256 / identity |
|---|---|
| Effective plugin artifact `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js` | `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95` |
| `dist/discovery-7zi_zNvu.js` | `5489a4b1086fed443cedf54efccc76a730960e8419bba4d97010c3420a342ddd` |
| `dist/loader-D8d2EvVh.js` | `3a10479bdcbb713692c3ded7dbd5baad27c1b17ae3566172c117d45916dabce7` |
| `dist/registry-B8eQDFB4.js` | `25f3ef82756d85281ad5c25375a5cd2f405989a1145ed438de05992e8c995376` |
| `dist/runtime-D0xGMZdc.js` | `a050a101e3c352345179b77f8c304da99596238fcde95cf03319ebc11dea8791` |
| `dist/hook-runner-global-BmIrGlLG.js` | `c066170e97a2355603f0bdd3079a687bf835632856a741fa9a92683d7d4b2750` |
| Production config SHA-256 | `19d7e6acf53ce370ddc20e5e2a2547c9674c33b178208b79920cb0e9dce9b46b` |

The module hashes match CNX-392/CNX-391 evidence; no installed-source divergence was found.

## Production read-only baseline

Fresh supported observation (`openclaw plugins list --json`) returned the target record:

```json
{"id":"cogentnexus-openclaw","source":"C:\\Users\\CDQ-P\\.openclaw\\extensions\\cogentnexus-openclaw\\dist\\v091-release-entry.js","rootDir":"C:\\Users\\CDQ-P\\.openclaw\\extensions\\cogentnexus-openclaw","origin":"global","status":"loaded","hookCount":0,"hookNames":[]}
```

This is inventory evidence only. It does not expose the candidate-to-entry lookup, `createApi` arguments, `registerTypedHook`, or the live registry decision.

Production config read-only extraction established:

- `plugins.entries.cogentnexus-openclaw` exists;
- entry/plugin key: `cogentnexus-openclaw`;
- `enabled: true`;
- `hooks.allowConversationAccess: true`;
- no other non-secret entry fields were present in the inspected target entry (secret-bearing values were not printed).

## Exact source trace

### Candidate construction and identity

In `discovery-7zi_zNvu.js`:

- `addCandidate` at `:707-752` resolves `source` with `path.resolve`, canonicalizes `rootDir` using `safeRealpathSync`/`path.resolve`, deduplicates candidates by the resolved source (`:708-710`), and stores `idHint`, `source`, `rootDir`, `origin`, manifest/package metadata, and dependency metadata (`:730-751`).
- Package-extension candidates derive their hint with `deriveIdHint({ filePath, manifestId, packageName, hasMultipleExtensions })` at `:942-951`; the manifest ID comes from `resolveCandidateManifest` at `:914-915`.
- The global roots are passed through `discoverInDirectory` with `origin: "global"` at `:1368-1392`; configured load paths use `origin: "config"` at `:1231-1242`.
- Directory discovery derives file hints from the filename at `:861-872`, package candidates from manifest/package extension resolution at `:907-963`, and fallback index candidates from `manifestId ?? entry.name` at `:978-989`.
- Directory traversal uses canonical real paths and visited/skip-root keys at `:838-880`. Global and config origins therefore differ at candidate metadata and discovery policy inputs, not by a separate configuration-entry map.
- Discovery-result merging deduplicates sources, not configuration IDs: `mergeDiscoveryResult` at `:516-545` uses candidate `source` as its key and preserves candidate records; the per-scan `seen` set in `:1261-1263` and `:1279-1300` likewise prevents duplicate resolved sources.

### Manifest/root association and plugin ID

In `loader-D8d2EvVh.js`:

- `manifestByRoot = new Map(manifestRegistry.plugins.map(record => [record.rootDir, record]))` at `:1640` is the candidate-to-manifest association index. The key is `rootDir`, not source path, `idHint`, or configuration key.
- For each ordered candidate, `manifestRecord = manifestByRoot.get(candidate.rootDir)` at `:1663-1665`; a missing root record causes `continue` before loading.
- `pluginId = manifestRecord.id` at `:1666`. Thus the effective lookup identity is the normalized manifest registry ID, not the discovery `idHint` and not the source filename.
- Duplicate/dedup precedence is ordered by `compareDuplicateCandidateOrder` at `:1641-1648`; `seenIds` is a map keyed by effective `pluginId` at `:1650`. If an ID was already seen, the later candidate becomes a disabled record with `error = overridden by ${existingOrigin} plugin` at `:1691-1720`. This is an ID-level precedence outcome after root/manifest association.

### Normalized entry and hook policy

- The exact assignment is `const entry = normalized.entries[pluginId]` at `loader-D8d2EvVh.js:1730`.
- The normal plugin record is then built from the manifest/candidate at `:1731-1753`; the record does not copy `entry.hooks` into the executable definition.
- Registration-plan resolution starts at `:1794-1808`; if no plan exists, loading is disabled and returns before registration at `:1809-1815`. `registrationMode` is assigned from `registrationPlan.mode` at `:1817`, not from `candidate.origin`.
- The normal runtime API construction passes `pluginConfig: validatedConfig.value`, `hookPolicy: entry?.hooks`, and `registrationMode` at `:2237-2242`; the setup branch passes `hookPolicy: entry?.hooks` at `:1994-1999`.
- In `registry-B8eQDFB4.js:4776`, `api.on` calls `registerTypedHook(record, hookName, handler, opts, params.hookPolicy)`.
- `registerTypedHook` at `:4180-4250` reads `policy?.allowConversationAccess` at `:4226`; non-bundled records (`record.origin !== "bundled"`) are blocked unless the value is exactly `true` at `:4227-4235`. There is no separate `global` branch. `config` and `global` both enter this non-bundled predicate.

### Association conclusion from source

The proven mapping is:

```text
discovery candidate
  -> candidate.rootDir
  -> manifestByRoot.get(candidate.rootDir)
  -> manifestRecord.id  (= pluginId)
  -> normalized.entries[pluginId]
  -> entry?.hooks
  -> createApi(... hookPolicy: entry?.hooks)
  -> api.on(...)
  -> registerTypedHook(... params.hookPolicy)
```

A different source path or origin does not itself select a different entry. However, a candidate whose manifest registry record has an ID different from `cogentnexus-openclaw`, or for which `normalized.entries[pluginId]` is absent, will not receive the production entry's `hooks` object; optional chaining makes the resulting policy undefined. The installed source provides no direct production proof that either condition occurred.

## Candidate/entry matrix

| Discovery origin | Candidate ID | Normalized lookup key | Entry exists? | `entry.hooks` | `hookPolicy` |
|---|---|---|---|---|---|
| config | manifest-derived `manifestRecord.id`; CNX-391 exact replay used `cogentnexus-openclaw` | `cogentnexus-openclaw` | observed in CNX-391 production-shaped fixture | `allowConversationAccess=true` observed | true policy accepted in CNX-391 real registry | 
| global | production inventory reports `cogentnexus-openclaw`; exact loader candidate-to-entry runtime value not exposed | source-traced key is `manifestRecord.id`; runtime lookup value `UNRESOLVED` | `UNRESOLVED` | `UNRESOLVED` | `UNRESOLVED` |

The global row deliberately does not infer entry existence from the same displayed ID or from the on-disk config.

## Isolated association evidence

No true global-origin replay was performed. Reproducing it would require the real global installation/discovery record or extension-tree state, which is forbidden. A relocated temporary copy would change only path and would not prove the global discovery mechanism, so it was correctly not used as a global-origin substitute.

The direct isolated evidence available from CNX-391 remains valid mechanism evidence: exact loader/API execution with the production-shaped entry observed `register(api)`, repeated `api.on("before_agent_run")`, and six accepted `before_agent_run` registrations when `entry.hooks.allowConversationAccess=true`; its false control omitted the targeted hook. That evidence proves the downstream policy path when the normalized entry is supplied, not that production global discovery supplied it.

## Direct evidence versus inference

**Direct:** remote/local starting HEAD equality; current production config key, enabled flag, hook value, and config hash; current supported inventory record; exact installed module hashes; discovery source origin assignment; source dedup keys; root-to-manifest map; manifest-ID assignment; exact `normalized.entries[pluginId]` assignment; `entry?.hooks` passed to `createApi`; `api.on` routing to `registerTypedHook`; and the non-bundled policy predicate.

**Inference:** the same candidate ID is likely intended to map to the same entry, but this is not accepted as proof for the live process. The source permits an association gap at manifest ID mismatch or missing normalized entry. The production `hookCount=0` symptom cannot identify that gap or prove hook rejection.

## Relation to CNX-391 and CNX-392

CNX-391 proves config-origin acceptance only after the exact loader/API path received the production-shaped normalized entry with `allowConversationAccess=true`. It does not imply that production's global candidate received the same `entry.hooks`, because candidate-to-manifest association and normalized-entry lookup are separate host-owned steps.

CNX-392 correctly established that origin metadata alone does not select a different conversation policy branch and that `hookPolicy` comes from `entry?.hooks`. CNX-393 narrows the remaining gap to the unobserved runtime association value: `manifestRecord.id` and the existence/content of `normalized.entries[pluginId]` for the already-running global candidate. No contradiction with CNX-385/388/389 was found; those reports were not reopened.

## Production gap and remaining uncertainty

The production gap is narrowed from “global origin might use a different policy branch” to “the live global candidate's manifest-root-to-ID-to-normalized-entry association is not observable through supported read-only inventory.” The exact missing fact is whether the running loader used `pluginId = cogentnexus-openclaw` and found the normalized entry containing the true hook policy. Closing it would require forbidden lifecycle/instrumentation or exact global discovery replay.

No production acceptance or rejection is claimed. No registry-composition loss is claimed.

## Counts and hard-fence compliance

- Semantic/model/provider/Dashboard requests: `0`
- Production mutation count: `0`
- Production Gateway restart/reload: `0`
- Production config mutation: `0`
- Environment mutation: `0`
- Scheduled Task mutation: `0`
- Production global extension installation/mutation: `0`
- Artifact replacement/deploy/rebuild: `0`
- OpenClaw dependency patch: `0`
- CogentNexus source repair: `0`
- Debugger/inspector attachment: `0`
- Permanent instrumentation: `0`
- Historical CNX-360 through CNX-392 modifications: `0`
- Release/tag/main changes: `0`
- Force-push/history rewrite: `0`
- CNX-394 created/started: `0`

## Closeout

`ACTIVE.md` and `STATUS.md` were changed only after the report was written, to `WAITING_FOR_CHATGPT_REVIEW`. No successor task was created or started. Execution stops for review.
