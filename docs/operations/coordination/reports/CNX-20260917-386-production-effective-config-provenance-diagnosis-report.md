# CNX-20260917-386 — Production Effective Configuration Provenance Diagnosis

## Authoritative Starting / Final HEAD

- **Starting remote HEAD**: `254e4b86d0a46822e4596e3f05328d5305c41a3f` (origin/cnx-357-openai-dashboard-ticket-first-requalification-v2)
- **Final executor HEAD**: `254e4b86d0a46822e4596e3f05328d5305c41a3f` (same; no further commits after CNX-385 publication)
- **Classification**: `PRODUCTION_EFFECTIVE_CONFIG_PROVENANCE_UNRESOLVED`

## Live PID / Version

- **Gateway PID**: `27372`
- **Process**: `node.exe`, command line `"C:\Program Files\nodejs\node.exe" C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\dist\index.js gateway --port 18789`
- **Service**: Scheduled Task `\\OpenClaw Gateway` (registered), launched via `C:\Users\CDQ-P\.openclaw\gateway.cmd`
- **OpenClaw version**: `2026.7.1-2` (resolved from `C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\package.json`)
- **Runtime**: `v24.18.0`, Node.js
- **Gateway state**: Running, Ready, last run `9/17/2026 5:13:48 AM`
- **Gateway bind**: `127.0.0.1:18789` (loopback)

## Effective CogentNexus Artifact SHA

- **Artifact path**: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
- **SHA-256**: `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- This artifact was the effective source input to the production loader at registration time.

## Command-Line / Environment Evidence

- **Config path** (production runtime): `~/.openclaw/openclaw.json`, resolved via `resolveConfigPathCandidate()` / `OPENCLAW_CONFIG_PATH` environment variable (not explicitly set; defaulted to state dir `~/.openclaw`)
- **Config file contents** (read-only, from disk):
  ```json
  {
    "enabled": true,
    "config": {
      "ticketFirst": true,
      "preInferenceAdmission": true,
      "autoWorkflowCompletion": true,
      "enforcedMode": true,
      "autoResume": true,
      "workspaceDir": "C:\\Users\\CDQ-P\\.openclaw\\workspace",
      "ticketDispatchLimit": 1,
      "ticketMaximumRunning": 1,
      "ticketMaximumAttempts": 5,
      "ticketRecoveryPollMs": 60000,
      "ticketDispatchPollMs": 60000,
      "ticketOutboxPollMs": 60000,
      "completionPollMs": 60000,
      "contextMaintenancePollMs": 30000,
      "providerMode": "passthrough"
    },
    "hooks": {
      "allowConversationAccess": true
    }
  }
  ```
- **`plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess`**: `true` (raw config, verified via `openclaw config get plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess` returning `true`)

## Config Path Selected by OpenClaw

- **Selection mechanism**: OpenClaw resolves the config path via `resolveConfigPathCandidate()` which prefers:
  1. Explicit `OPENCLAW_CONFIG_PATH` environment variable
  2. Existing config file in state dir (`~/.openclaw/openclaw.json`)
  3. Canonical path `$STATE_DIR/openclaw.json`
- **No override**: `OPENCLAW_CONFIG_PATH` was not set in the production environment; the default `~/.openclaw/openclaw.json` was used.
- **State dir**: `~/.openclaw` (default, verified `resolveStateDir()`)
- **Result**: Production loader read config from `~/.openclaw/openclaw.json`.

## Raw Config Value

- **Key**: `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess`
- **Value**: `true` (present in `~/.openclaw/openclaw.json` under `"hooks": {"allowConversationAccess": true}`)
- **Schema**: `PluginEntrySchema` in `zod-schema-O9ml_nmo.js:788-806` explicitly accepts this field; `strict()` allows it.
- **Normalization** (proven by CNX-385): `normalizePluginEntries()` preserves `allowConversationAccess` when present and boolean (config-normalization-shared-w2iz0aeC.js:265-277). The normalized entry `hooks.allowConversationAccess` is `{allowConversationAccess: true}`.

## Validation / Normalization Result

- **Schema validation**: PASS — `allowConversationAccess: true` is a known boolean field in `PluginEntrySchema`.
- **Normalization**: PRESERVED — `normalizePluginEntries` extracts and retains `allowConversationAccess: true` into `normalized.entries['cogentnexus-openclaw'].hooks`.
- **Normalized entry** (isolated reproduction via `config-normalization-shared-w2iz0aeC.js`):
  ```json
  {
    "cogentnexus-openclaw": {
      "enabled": true,
      "hooks": {
        "allowConversationAccess": true
      },
      "config": { ... }
    }
  }
  ```
- **Loader `entry`**: At `loader-D8d2EvVh.js:1730`, `const entry = normalized.entries[pluginId]`; at lines 1997/2240, `hookPolicy: entry?.hooks` is passed to `createApi`.
- **`createApi(hookPolicy)`**: The gate at `registry-B8eQDFB4.js:4226` reads `policy?.allowConversationAccess`. When `policy = {allowConversationAccess: true}`, the gate **allows** the conversation hook for non-bundled plugins.

## Production Effective-Config Evidence

- **Raw config contains** `hooks.allowConversationAccess: true` ✅
- **Normalization preserves** the field ✅ (CNX-385)
- **Loader passes** `entry?.hooks` → `createApi(hookPolicy)` ✅ (source-proven path)
- **Gate receives** `policy = {allowConversationAccess: true}` ✅ (proven source trace)
- **Yet production shows**: `hookCount = 0`, `hookNames = []` ❌

**Critical dissonance**: The production effective config path and normalization logic both support `allowConversationAccess: true`, but the production runtime does not register the hook. The normalization-strip hypothesis (CNX-385) is **closed** — normalization does not strip the field. The remaining question is whether the production loader actually consumes the expected effective config object at plugin-registration time.

## Isolated Reproduction Evidence

- **Disposable probe** (PID `24428`, Node `v22.23.2`) imported exact OpenClaw `2026.7.1-2` modules from `C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\dist\` and exercised `normalizePluginsConfigWithResolver` / `OpenClawSchema.safeParse` against three fixtures.
- **Fixture A** (`allowConversationAccess: true`): normalization preserves `{allowConversationAccess: true}`; gate allows.
- **Fixture B** (`allowConversationAccess: false`): normalization preserves `{allowConversationAccess: false}`; gate blocks.
- **Fixture C** (hooks omitted): normalization yields `undefined`; gate blocks (`policy?.allowConversationAccess !== true`).
- **Conclusion**: The normalization path is proven to preserve the field; the production probe uses identical module bytes (SHA-256 verified). The remaining production uncertainty is **not** whether normalization strips the field, but whether the production runtime actually presents the effective config object at loader start.

## Explicit Conclusion

**Whether production receives `allowConversationAccess=true` cannot be proven from the current non-invasive runtime inspection alone.**

- The raw config file `~/.openclaw/openclaw.json` contains `hooks.allowConversationAccess: true`.
- Normalization preserves the field (CNX-385).
- The loader's source-proven path `entry?.hooks` → `createApi(hookPolicy)` → gate reads `policy?.allowConversationAccess` would allow the hook **if** the normalized entry is present.
- However, production `hookCount=0` and `hookNames=[]` indicate that either:
  1. The normalized entry `plugins.entries.cogentnexus-openclaw.hooks` was absent or `undefined` at loader runtime (config drift, different config path, or reload race), **or**
  2. A separate registry-composition boundary (explored in CNX-377/CNX-378) blocks hook visibility after gate passage, **or**
  3. The production loader used a different effective config source than `~/.openclaw/openclaw.json` at registration time.

**No production config mutation, restart, or debugger attach was performed** (all forbidden by hard fences). The evidence boundary is therefore **unresolved** at the production level.

## Relationship to CNX-385

- CNX-385 **proved** that the raw-config → normalization → `normalized.entries[pluginId]` → `entry.hooks` → `createApi(hookPolicy)` → `registerTypedHook` gate path **preserves** `plugins.entries.<id>.hooks.allowConversationAccess=true` end-to-end.
- CNX-385 **closed** the normalization-strip hypothesis.
- CNX-386 **extends** the inquiry from normalization to **production effective-config provenance**: while normalization preserves the field, the production runtime's actual config source at loader registration time cannot be confirmed without invasive inspection.
- CNX-386 does **not** reopen or contradict CNX-385; it reports a higher-level provenance uncertainty that persists after CNX-385's classification of `NORMALIZED_HOOK_POLICY_PRESERVED_HOST_CONTRACT_FOUND`.

## Remaining Registry-Composition Uncertainty

Even if the gate passes and `record.hookCount` increments, CNX-377/CNX-378 identified a separate registry-composition boundary where hooks may not reach the composed registry view visible to `openclaw plugins list --json` or `hasHooks("before_agent_run")`. This task does not re-investigate that boundary but notes it as a persistent uncertainty layer.

## Hard-Fence Compliance

| Item | Count |
|---|---|
| Production Gateway restart/reload | 0 |
| Production config mutation | 0 |
| OpenClaw dependency patch | 0 |
| CogentNexus source/artifact repair | 0 |
| Artifact rebuild/deploy | 0 |
| Semantic/model/provider requests | 0 |
| TicketStore/admission/routing/auth changes | 0 |
| Permanent/committed instrumentation | 0 |
| Broad refactor | 0 |
| Release/tag/main changes | 0 |
| Force-push/history rewrite | 0 |
| Historical CNX-360 through CNX-384 edits | 0 |
| CNX-386 started | 0 |
| Semantic requests (this task) | 0 |
| Production mutation count | 0 |

## Report Publication Transition

- `ACTIVE.md` and `STATUS.md` are set to `WAITING_FOR_CHATGPT_REVIEW` per CNX-385 closeout procedure.
- No CNX-387 is created.
- Historical CNX-360 through CNX-385 are unchanged.
- `main`, tags, and releases are unchanged.