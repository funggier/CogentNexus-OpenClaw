# CNX-20260917-397 — Global Candidate Pre-API Eligibility and Manifest Provenance Trace Report

## Classification

`GLOBAL_CANDIDATE_PRODUCTION_CORRELATION_INCONCLUSIVE`

The exact installed OpenClaw source proves the complete pre-API mechanism and identifies every skip gate. Fresh production read-only evidence shows the intended global root, manifest ID, artifact, configured ID, and enabled/policy values are mutually consistent. It does not prove that the already-running Gateway's historical loader candidate passed every gate or reached `createApi`; the supported inventory is a persisted/derived projection and no restart, debugger, or permanent instrumentation was permitted.

## Authority and scope

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Task: `CNX-20260917-397`
- Parent: `CNX-20260917-396`
- Authoritative starting local HEAD: `36c4ce51373b890a52c524af35b2abd5174c5022`
- Authoritative starting remote HEAD: `36c4ce51373b890a52c524af35b2abd5174c5022`
- Starting gate: `READY_FOR_HERMES`

GitHub was fetched first with an explicit branch refspec. Local HEAD and `git ls-remote` matched before investigation. `ACTIVE.md`, `STATUS.md`, this task, CNX-396, and CNX-391 through CNX-395 were read from that authoritative checkout.

## Exact runtime, artifact, and module identity

- OpenClaw: `2026.7.1-2 (0790d9f)`
- Effective production artifact: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
- Artifact SHA-256: `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- Production config: `C:\Users\CDQ-P\.openclaw\openclaw.json`
- Production config SHA-256: `19d7e6acf53ce370ddc20e5e2a2547c9674c33b178208b79920cb0e9dce9b46b`

Exact installed OpenClaw module hashes, read from the exact `2026.7.1-2` module graph used by the predecessor probes:

| Module | SHA-256 |
|---|---|
| `dist/loader-D8d2EvVh.js` | `3a10479bdcbb713692c3ded7dbd5baad27c1b17ae3566172c117d45916dabce7` |
| `dist/discovery-7zi_zNvu.js` | `5489a4b1086fed443cedf54efccc76a730960e8419bba4d97010c3420a342ddd` |
| `dist/registry-B8eQDFB4.js` | `25f3ef82756d85281ad5c25375a5cd2f405989a1145ed438de05992e8c995376` |
| `dist/config-normalization-shared-w2iz0aeC.js` | `c3b7bccc26f72ac0ab79ef0635daaa5931d23f86d9bc7e21f4ae8b60ce80f7c2` |

## Exact pre-API source trace

All line numbers below are from the hashed modules above.

1. **Origin and discovery path.** Configured load paths call `discoverFromPath` with `origin: "config"` at `discovery-7zi_zNvu.js:1231-1242`. Installed paths call it with `origin: "global"` at `:1368-1382`; the global directory scan also uses `origin: "global"` at `:1383-1395`. Origin is candidate metadata. The global path can differ in root/source and discovery ordering, but it does not select a separate normalized config object at this boundary.
2. **Manifest index and root association.** `loader-D8d2EvVh.js:1640-1648` constructs `manifestByRoot` keyed by `record.rootDir` and sorts candidates with `compareDuplicateCandidateOrder`. At `:1663-1666`, `manifestByRoot.get(candidate.rootDir)` is performed; missing manifest is an immediate `continue` at `:1665`; otherwise `pluginId = manifestRecord.id` at `:1666`.
3. **Scoped candidate filtering.** `:1667-1671` calls `matchesScopedPluginOrDreamingSidecar`; a non-match skips before activation, deduplication, normalized entry lookup, and API creation. Dreaming-sidecar selection is established at `:1654-1660` and its special enablement is at `:1672-1682`.
4. **Enablement.** Ordinary activation state is resolved at `:1682-1690` using `resolveEffectivePluginActivationState`, with candidate `origin`, normalized config, root config, and manifest default. The effective enable state is resolved at `:1722-1729` using the same origin/config inputs. Thus origin is an input to enablement resolution and can matter if that resolver has an origin-sensitive rule; no production-specific divergent value was observed here.
5. **Duplicate-ID precedence.** `:1691-1720` checks `seenIds`. A later effective duplicate is materialized disabled, marked `overridden by <existingOrigin>`, inserted into the registry, and skipped at `:1720`. The first ordered candidate therefore wins; ordering is computed before the loop at `:1641-1648` and can depend on candidate provenance.
6. **Selected configuration entry.** After enablement, `:1730` reads exactly `const entry = normalized.entries[pluginId]`. The key is the manifest-derived ID, not the candidate's source or configured spelling directly. A missing entry is not itself an immediate skip at this line, but it supplies no `entry?.hooks` and may affect validation/registration behavior downstream.
7. **Registration plan and null skip.** `:1794-1808` calls `resolvePluginRegistrationPlan` with enablement, validation/load/activation flags, manifest, config, environment, setup-channel conditions, and tool discovery. A null plan is an explicit pre-API skip at `:1809-1815`; the record is disabled and the loop continues. `registrationMode = registrationPlan.mode` at `:1817`, so mode derives from the plan rather than directly from `origin`. Setup-only conditions include an origin predicate at `:1795` (`candidate.origin !== "workspace"`), not a global-versus-config predicate.
8. **Additional pre-API checks.** The loader validates module/export identity and plugin ID before API construction. The setup branch's ID mismatch diagnostic/skip is at `:1988-1993`, followed by setup `createApi` at `:1994-1999`. In the ordinary path, missing register/activate export handling is at `:2232-2235`, followed by ordinary `createApi` at `:2237-2242`.
9. **Hook-policy projection.** Both API paths pass `hookPolicy: entry?.hooks`: setup at `:1994-1999`, ordinary at `:2237-2242`. `pluginConfig` is separately sourced from `validatedConfig.value` in the ordinary path at `:2238-2241`. The host conversation gate in `registry-B8eQDFB4.js:4225-4235` checks `record.origin !== "bundled"` and `policy?.allowConversationAccess === true`; it does not distinguish `global` from `config`. Accepted hooks increment/store live registry state at `:4251-4255`.

**Direct answer:** a global candidate *can* diverge before `createApi` through root/path discovery, missing or mismatched root-keyed manifest, manifest ID, scope filtering, candidate ordering/duplicate precedence, enablement, null registration plan, or other module/ID validation. The exact source does not show a dedicated `origin=global` branch that changes `normalized.entries[pluginId]`, `entry?.hooks`, or the non-bundled conversation policy predicate. Whether any such divergence occurred in the historical production loader remains unproven.

## Production read-only correlation

Fresh read-only inspection found:

- Global extension root: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw`
- Manifest: `...\openclaw.plugin.json`
- Manifest `id`: `cogentnexus-openclaw`
- Manifest version: `0.9.5`
- Artifact path: `...\dist\v091-release-entry.js`
- Artifact SHA-256: `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- Configured entry: `plugins.entries.cogentnexus-openclaw.enabled=true`
- Configured policy: `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess=true`

The supported inventory context remains `id=cogentnexus-openclaw`, `origin=global`, `status=loaded`, `hookCount=0`, `hookNames=[]`. CNX-394/395 established that this is a separate installed-index projection; zero/empty hook fields are initialized summary fields, not live-loader proof. The target persisted index row has `refresh_reason=policy-changed`, generated/updated at `2026-09-16T13:07:14.051Z`/`.052Z`, before the current Gateway PID `27372` creation time `2026-09-17T10:13:08.606Z` (CNX-395 evidence). It therefore cannot close historical in-memory candidate provenance.

No fresh startup/discovery log line was found that directly binds the current Gateway PID to `candidate.rootDir`, `manifestRecord.id`, or `createApi`. Existing config-audit records are configuration-write history and were not treated as loader proof. No production file was changed.

## Global/config comparison and isolated replay

| Field | Config origin | Global origin | Exact conclusion |
|---|---|---|---|
| `rootDir` / load path | configured load path | installed/global path | Can differ; source assigns origins at discovery lines above |
| manifest lookup | same `manifestByRoot.get(rootDir)` | same | Same mechanism; missing root entry skips |
| manifest ID / `pluginId` | `manifestRecord.id` | `manifestRecord.id` | Same assignment; values can differ if manifests differ |
| scoped filtering | same matcher | same matcher | Same function; candidate can be skipped |
| duplicate precedence | ordered candidate loop / `seenIds` | same | Order/provenance can affect winner |
| enablement | same resolvers with origin input | same | Can differ only if resolver inputs/rules differ; no direct global-only branch proven |
| registration plan/mode | same resolver; `mode` from plan | same | Null plan skips; mode is not directly origin-derived |
| selected entry/hooks | `normalized.entries[pluginId]`, `entry?.hooks` | same | Same normalized object/path in one loader invocation |
| conversation gate | non-bundled policy check | non-bundled policy check | `global` and `config` are treated alike |

No new exact global-origin isolated replay was run. The task's exact global path cannot be reproduced without using or mutating the production global installation metadata/tree; a relocated copy would be synthetic mechanism evidence and would not prove historical production values. CNX-391 remains the exact-loader config-origin true/false replay: true policy reached real typed-hook storage, while false omitted conversation hooks. It does not prove production global activation.

## Predecessor comparison

- CNX-391 proved exact config-origin true-policy acceptance through loader/API.
- CNX-392 proved origin is not itself the direct conversation-policy selector.
- CNX-393 traced root → manifest → plugin ID but could not observe historical production values.
- CNX-394 established inventory as an installed-index projection.
- CNX-395 established the index predates the current Gateway and refreshes independently of live activation.
- CNX-396 established one common normalized producer/path while exact global replay remained blocked.
- CNX-397 narrows the remaining gap to unobserved historical global candidate identity/eligibility and confirms possible pre-API divergence mechanisms without claiming which occurred.

## Direct evidence, inference, and remaining gap

**Direct:** exact remote starting SHA; exact module/artifact/config hashes; discovery origin assignments; root-keyed manifest map; missing-manifest skip; manifest-ID derivation; scoped filter; activation/enablement calls; duplicate handling; normalized entry read; registration-plan/null path; mode derivation; both `createApi` calls; origin-insensitive non-bundled hook predicate; production root/manifest/artifact/config values; and persisted-index provenance.

**Inference:** the production root, manifest, ID, artifact, and config are mutually consistent and are the expected inputs for the global path. This consistency does not establish that the running Gateway used them together, passed candidate ordering/scope/duplicate/enablement/plan gates, or passed the resulting `entry?.hooks` to `createApi`.

Remaining production gap: contemporaneous loader-local evidence for `candidate.rootDir`, `manifestRecord.id`, selected candidate after deduplication, enablement, registration plan, `normalized.entries[pluginId]`, and `createApi` arguments. Under the hard fences, classification remains `GLOBAL_CANDIDATE_PRODUCTION_CORRELATION_INCONCLUSIVE`; no hook acceptance/rejection is claimed.

## Required counts and hard-fence compliance

- Semantic/model/provider/Dashboard requests: `0`
- Production mutation count: `0`
- Gateway restart/reload: `0`
- Production config/environment/Scheduled Task mutation: `0`
- Production global extension mutation/artifact replacement/deploy: `0`
- OpenClaw dependency patch: `0`
- CogentNexus source repair/rebuild: `0`
- Debugger/inspector attachment: `0`
- Permanent instrumentation: `0`
- TicketStore/admission/routing/auth changes: `0`
- Historical CNX-360 through CNX-396 edits: `0`
- Release/tag/main changes: `0`
- Force-push/history rewrite: `0`
- CNX-398 created/started: `0`

## Closeout

ACTIVE.md and STATUS.md were updated to `WAITING_FOR_CHATGPT_REVIEW` after this report was written. Final local/remote verification and clean-worktree state are recorded in the executor closeout. Execution stops here; no CNX-398 is created or started.
