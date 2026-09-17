# CNX-20260917-398 — Global-Origin-Only Pre-API Eligibility A/B Replay Report

## Classification

`GLOBAL_ORIGIN_ONLY_PRE_API_DIAGNOSTICALLY_BLOCKED`

The exact installed OpenClaw source was traced through candidate discovery, root/manifest association, filtering, duplicate handling, enablement, registration planning, normalized-entry lookup, `createApi`, and typed-hook policy. The source contains no `global`-versus-`config` conversation-policy branch: both are non-bundled origins. However, the required exact runtime A/B replay could not be invoked without injecting candidate records into the loader or constructing the real global-discovery/install state. Injecting or mutating the production global extension state is forbidden, and a relocated copy would not be an exact `origin="global"` replay. No synthetic A/B result is claimed.

## Authority and exact starting baseline

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Task: `CNX-20260917-398`
- Executor: `Hermes`; reviewer: `ChatGPT`
- Exact authoritative starting local HEAD: `9930563eaef289aca17d143a753613e1a2e212ac`
- Exact authoritative starting remote HEAD: `9930563eaef289aca17d143a753613e1a2e212ac`
- Starting gate: `READY_FOR_HERMES`

GitHub was fetched with an explicit branch refspec before execution. `git ls-remote` and the checked-out local HEAD matched the SHA above. ACTIVE, STATUS, the CNX-398 task, CNX-397, and CNX-396 through CNX-391 were read from this authoritative checkout. The task's embedded historical expected SHA differed from the live GitHub authority; the live value was used.

## Exact runtime, artifact, and module identity

- OpenClaw: `2026.7.1-2 (0790d9f)`
- Effective artifact: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
- Effective artifact SHA-256: `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- Installed OpenClaw module root used for source inspection: `C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw`

| Module | SHA-256 |
|---|---|
| `dist/loader-D8d2EvVh.js` | `3a10479bdcbb713692c3ded7dbd5baad27c1b17ae3566172c117d45916dabce7` |
| `dist/discovery-7zi_zNvu.js` | `5489a4b1086fed443cedf54efccc76a730960e8419bba4d97010c3420a342ddd` |
| `dist/registry-B8eQDFB4.js` | `25f3ef82756d85281ad5c25375a5cd2f405989a1145ed438de05992e8c995376` |
| `dist/config-normalization-shared-w2iz0aeC.js` | `c3b7bccc26f72ac0ab79ef0635daaa5931d23f86d9bc7e21f4ae8b60ce80f7c2` |

## Exact source mapping and origin sensitivity

All mappings are from the hashed installed modules above.

1. **Origin assignment.** `discovery-7zi_zNvu.js:1231-1242` assigns `origin: "config"` for configured load paths. `:1368-1382` assigns `origin: "global"` for installed paths and `:1383-1395` for the global directory scan. This is candidate metadata attached by the same discovery machinery.
2. **Candidate ordering and duplicate identity.** `loader-D8d2EvVh.js:1640-1648` builds the root-keyed manifest map and sorts candidates with `compareDuplicateCandidateOrder`. `:1650` creates `seenIds`; `:1663-1666` resolves `manifestByRoot.get(candidate.rootDir)` and assigns `pluginId = manifestRecord.id`. `:1691-1720` handles later duplicate IDs as disabled/overridden and skips them. Origin can be part of ordering/diagnostic data, but this is a generic candidate-precedence path, not a dedicated global/config branch.
3. **Scoped filtering.** `:1654-1672` calls `matchesScopedPluginOrDreamingSidecar` before ordinary activation and entry lookup. Any difference in candidate data that changes the matcher can change eligibility. The predicate is shared; origin alone is not shown selecting a different config entry.
4. **Enablement.** `:1679-1690` and `:1722-1729` call the effective activation resolvers with candidate origin, normalized config, root config, and manifest defaults. Origin is therefore an input and could matter if resolver rules distinguish it. No concrete `global`-only outcome was produced in this run.
5. **Registration plan.** `:1794-1808` resolves the plan; `:1809-1815` skips on a null plan; `:1817` derives `registrationMode = registrationPlan.mode`. The setup-only condition at `:1795` excludes `workspace`, not `global` versus `config`. Mode is not directly derived from either tested origin.
6. **Validation and API construction.** Setup validation/`createApi` is at `:1988-1999`; ordinary missing-register handling is at `:2232-2235`, followed by ordinary `createApi` at `:2237-2242`. Both paths pass `hookPolicy: entry?.hooks`; ordinary also passes `pluginConfig: validatedConfig.value`.
7. **Normalized entry and policy.** `:1730` reads `const entry = normalized.entries[pluginId]`. The normalized object is produced once per loader invocation from `cfg.plugins` at `:1201`; the shared producer is `config-normalization-shared-w2iz0aeC.js:253-310,314-325`, where boolean `allowConversationAccess` is retained at `:263-279`. Origin is not a source for this value.
8. **Typed-hook gate.** `registry-B8eQDFB4.js:4225-4235` rejects conversation hooks when `record.origin !== "bundled"` and `policy?.allowConversationAccess !== true`. Both `config` and `global` satisfy the same non-bundled predicate. `:4251-4255` stores accepted hooks. There is no `global`-specific branch here.

### Branch classification

- **Origin-sensitive or origin-fed decision points:** discovery labels (`discovery:1231-1242,1368-1395`); duplicate ordering/diagnostics (`loader:1640-1648,1691-1720`); effective enablement resolver inputs (`loader:1679-1690,1722-1729`); setup-only exclusion of `workspace` (`loader:1795`). These can matter only if other resolver/candidate inputs or the predicate make them matter; this inspection did not establish a concrete config/global divergence.
- **Origin as metadata/projection:** candidate construction and loader record identity; `seenIds` diagnostic origin; `createApi` input record origin; registration mode, which is taken from the plan rather than origin (`loader:1817`).
- **Predicates not distinguishing config/global:** setup predicate excluding only `workspace` (`loader:1795`); conversation policy predicate excluding/handling `bundled` separately (`registry:4225-4244`). `config` and `global` follow the same non-bundled policy branch.

## Exact isolated A/B replay status

The public installed loader export is `loadOpenClawPlugins` (`loader` export `s`). Its loader-local candidate list is constructed internally from discovery/config/install inputs; the callable testing surface exposes loader helpers but no supported candidate-list injection or origin override. An exact A/B would require either patching/instrumenting the OpenClaw dependency or creating the real global installation/discovery metadata. Both are outside the fence. The production global root was not changed, copied into, or used as a fixture source.

Consequently, no Case A or Case B runtime result is asserted. In particular, the following are **not observed for this task**: accepted/rejected candidate, candidate order, effective enablement, duplicate/override result, registration plan/mode, normalized-entry presence, `entry?.hooks`, `createApi` reachability, or typed-hook storage for either origin. CNX-391 remains prior exact config-origin mechanism evidence: true policy reached real typed-hook storage and its false control did not. It cannot be relabeled as this task's paired A/B.

| Required observation | Case A `config` | Case B `global` | Status |
|---|---|---|---|
| Candidate accepted/rejected | not run | not run | blocked at exact candidate injection boundary |
| Candidate ordering | not run | not run | blocked |
| Effective enablement | not run | not run | blocked |
| Duplicate/override | not run | not run | blocked |
| Registration plan/mode | not run | not run | blocked |
| `normalized.entries[pluginId]` | not run | not run | blocked |
| `entry?.hooks?.allowConversationAccess` | not run | not run | blocked |
| `createApi` reached | not run | not run | blocked |
| `api.on("before_agent_run")` typed storage | not run | not run | blocked |

## Production read-only correlation

Read-only commands returned:

- Global extension root: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw`
- Manifest ID/version: `cogentnexus-openclaw` / `0.9.5`
- Effective artifact SHA-256: `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- Configured plugin: `plugins.entries.cogentnexus-openclaw`, `enabled=true`
- Configured hook policy: `hooks.allowConversationAccess=true`
- Supported inventory: `origin=global`, `status=loaded`, `hookCount=0`, `hookNames=[]`

The inventory is the persisted/derived installed-index projection described by CNX-394/395, not live-loader proof. No production Gateway restart/reload, debugger, semantic request, retry, or mutation occurred. The isolated source result is mechanism evidence only and is not historical proof for Gateway PID 27372.

## Direct evidence versus inference

**Direct evidence:** exact remote starting SHA; exact installed module/artifact hashes; all source mappings above; common normalization producer; root-keyed manifest lookup; manifest-derived plugin ID; shared filtering, duplicate, enablement, and registration-plan calls; both `createApi` call sites; and the non-bundled policy predicate treating config/global alike. Production root, manifest, ID/version, enabled value, hook policy, artifact hash, and inventory origin were read-only observations.

**Inference:** when all non-origin candidate/config inputs truly match, source strongly predicts the same normalized entry and same conversation-policy branch for config/global. This is not an A/B runtime result and does not prove the historical production candidate passed root association, filtering, duplicate precedence, enablement, or registration planning.

## Effect on remaining production hook-policy gap

The origin-only hypothesis is weakened at the source boundary: origin alone is not the conversation-policy selector, and no dedicated global normalized-config path was found. The production gap remains open because the live candidate's loader-local root association, manifest ID, normalized-entry presence, enablement, registration plan, `createApi` arguments, and typed-hook registry state remain unobserved. The supported inventory cannot close that gap. No production hook acceptance/rejection, registry-composition loss, or Dashboard Ticket-first result is claimed.

## Counts and hard-fence compliance

- Semantic/model/provider/Dashboard requests: `0`
- Production mutation count: `0`
- Gateway restart/reload: `0`
- Production config/environment/Scheduled Task mutation: `0`
- Production global extension installation/mutation: `0`
- Artifact replacement/deploy/rebuild: `0`
- OpenClaw dependency patch: `0`
- CogentNexus source repair: `0`
- Debugger/inspector attachment: `0`
- Permanent instrumentation: `0`
- TicketStore/admission/routing/auth changes: `0`
- Historical CNX-360 through CNX-397 edits: `0`
- Release/tag/main changes: `0`
- Force-push/history rewrite: `0`
- CNX-399 created/started: `0`

## Closeout

The report is the only new report path authorized. ACTIVE.md and STATUS.md are set to `WAITING_FOR_CHATGPT_REVIEW` in the publication commit. Final authoritative HEAD, remote equality, changed paths, and clean-worktree verification are recorded after publication. Execution stops; no CNX-399 is created or started.
