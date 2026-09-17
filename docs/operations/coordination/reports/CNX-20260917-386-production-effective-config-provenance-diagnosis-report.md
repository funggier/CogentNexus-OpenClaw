# CNX-20260917-386 — Production Effective Configuration Provenance Diagnosis

## Authoritative Starting / Final HEAD

- **Starting remote HEAD**: `254e4b86d0a46822e4596e3f05328d5305c41a3f` (origin/cnx-357-openai-dashboard-ticket-first-requalification-v2)
- **Final executor / handoff HEAD**: `2bfe33d4eedc66030dc083999267ce1fb616d4d0`
- **Classification**: `PRODUCTION_EFFECTIVE_CONFIG_PROVENANCE_UNRESOLVED`

The starting HEAD was the reviewed CNX-385 state. The final handoff HEAD above is the commit at which the CNX-386 report and `ACTIVE.md`/`STATUS.md` transition to `WAITING_FOR_CHATGPT_REVIEW` were published. This reviewer amendment preserves the executor evidence and corrects documentation boundaries only.

## Task-record note

The CNX-386 report was published before a committed task specification file existed. To restore the coordination record without rewriting historical evidence, the corresponding task specification is being added as a documentation correction after execution. The task file is therefore a reconstructed contract from the authorized CNX-386 investigation scope; it was not part of the executor's starting tree.

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
- This is the effective CogentNexus artifact currently correlated with the live loaded plugin record. The evidence does **not** independently prove that this exact artifact path was the source observed at the historical instant of plugin registration beyond the existing production correlation evidence.

## Command-Line / Environment Evidence

- **Default configuration candidate**: `~/.openclaw/openclaw.json`.
- OpenClaw's config-path resolution logic prefers an explicit `OPENCLAW_CONFIG_PATH`, then the existing state-directory config, then the canonical `$STATE_DIR/openclaw.json` path.
- `OPENCLAW_CONFIG_PATH` was not set in the inspected environment, and `~/.openclaw` was the resolved state directory.
- This establishes the supported config-path resolution result for the inspected environment, but it does **not** prove the in-memory configuration object already held by PID `27372` at the historical plugin-registration instant.

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

## Config Path Resolution Result

- **Selection mechanism**: `resolveConfigPathCandidate()` resolves the supported config source according to the precedence above.
- **Observed result**: the inspected environment resolves to `~/.openclaw/openclaw.json`.
- **Important limitation**: the read-only evidence shows what the current CLI/config resolver selects and what is currently on disk. It does not expose the already-running gateway process's historical in-memory config object at plugin-registration time.
- Therefore the precise statement supported by this task is: **the current supported config resolution points to `~/.openclaw/openclaw.json`, which currently contains the required field**. The stronger statement that the live loader definitely used this exact object at registration time remains unproven.

## Raw Config Value

- **Key**: `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess`
- **Value**: `true` (present in `~/.openclaw/openclaw.json` under `"hooks": {"allowConversationAccess": true}`)
- **Schema**: `PluginEntrySchema` in `zod-schema-O9ml_nmo.js:788-806` explicitly accepts this field; `strict()` allows it.
- **Normalization** (proven by CNX-385): `normalizePluginEntries()` preserves `allowConversationAccess` when present and boolean (config-normalization-shared-w2iz0aeC.js:265-277). The isolated normalized entry contains `hooks.allowConversationAccess=true`.

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
- **Gate behavior from exact source trace**: `registry-B8eQDFB4.js:4226` reads `policy?.allowConversationAccess`; a policy object with `allowConversationAccess=true` would satisfy the non-bundled gate.

## Production Effective-Config Evidence

- **Raw config contains** `hooks.allowConversationAccess: true` ✅
- **Normalization preserves** the field ✅ (CNX-385)
- **Loader passes** `entry?.hooks` → `createApi(hookPolicy)` ✅ (source-proven path)
- **Production gate input value**: **not directly observed** ⚠️
- **Source-traced gate behavior**: `policy={allowConversationAccess:true}` would be accepted ✅
- **Yet production shows**: `hookCount = 0`, `hookNames = []` ❌

**Critical dissonance**: The current disk config and the exact OpenClaw normalization/loader/gate source path are all compatible with `allowConversationAccess=true`, but the running production inventory still reports no registered typed hooks. The normalization-strip hypothesis (CNX-385) is **closed** — normalization does not strip the field. The remaining production question is where the observable registration outcome diverges from the expected path.

## Isolated Reproduction Evidence

- **Disposable probe** (PID `24428`, Node `v22.23.2`) imported exact OpenClaw `2026.7.1-2` modules from `C:\Users\CDQ-P\AppData\Roaming\npm\node_modules\openclaw\dist\` and exercised `normalizePluginsConfigWithResolver` / `OpenClawSchema.safeParse` against three fixtures.
- **Fixture A** (`allowConversationAccess: true`): normalization preserves `{allowConversationAccess: true}`; the traced gate condition accepts it.
- **Fixture B** (`allowConversationAccess: false`): normalization preserves `{allowConversationAccess: false}`; the traced gate condition blocks it.
- **Fixture C** (hooks omitted): normalization yields `undefined`; the traced gate condition blocks it.
- **Conclusion**: the normalization path is proven to preserve the field. The isolated probe validates the host transformation semantics, but it is not direct instrumentation of the production loader instance.

## Explicit Conclusion

**Whether production received `allowConversationAccess=true` in its in-memory loader configuration at plugin-registration time cannot be proven from the current non-invasive inspection.**

What is proven:

- The current configuration file contains `allowConversationAccess=true`.
- The supported config resolver inspected in this environment points to that file.
- The OpenClaw schema accepts the field.
- Normalization preserves the field.
- The loader source passes `entry?.hooks` as `hookPolicy`.
- The gate reads `policy?.allowConversationAccess` and would allow a `true` policy for a non-bundled plugin.

What is **not** proven:

- The historical in-memory config object held by PID `27372` at plugin-registration time.
- The exact production `hookPolicy` argument observed inside `registerTypedHook` for the failing registration.
- That `hookCount=0` reflects gate rejection rather than a downstream registry visibility/composition issue.

The non-invasive evidence therefore supports the classification:

`PRODUCTION_EFFECTIVE_CONFIG_PROVENANCE_UNRESOLVED`

## Relationship to CNX-385

- CNX-385 **proved** the raw-config → normalization → `normalized.entries[pluginId]` → `entry.hooks` → `createApi(hookPolicy)` → `registerTypedHook` path preserves `allowConversationAccess=true`.
- CNX-385 **closed** the normalization-strip hypothesis.
- CNX-386 extends the inquiry to **production effective-config provenance** and finds that the live process's historical in-memory value cannot be observed safely under the hard fences.
- CNX-386 therefore does **not** reopen or contradict CNX-385.

## Remaining Registry-Composition Uncertainty

CNX-377/CNX-378 identified a separate registry-composition boundary where hooks may not reach the composed registry view consumed by later queries. This remains a distinct downstream hypothesis. CNX-386 does not prove that registry composition is the cause, only that production inventory remains inconsistent with the expected registration path.

## Hard-Fence Compliance

| Item | Count |
|---|---|
| Production Gateway restart/reload | 0 |
| Production config mutation | 0 |
| OpenClaw dependency patch | 0 |
| CogentNexus source/artifact repair | 0 |
| Artifact rebuild/deploy | 0 |
| Semantic/model/provider requests | 0 |
| TicketStore/admission/routing/auth/Dashboard changes | 0 |
| Permanent/committed instrumentation | 0 |
| Broad refactor | 0 |
| Release/tag/main changes | 0 |
| Force-push/history rewrite | 0 |
| Historical CNX-360 through CNX-385 edits | 0 |
| CNX-387 started | 0 |
| Semantic requests (this task) | 0 |
| Production mutation count | 0 |

## Report Publication Transition

- `ACTIVE.md` and `STATUS.md` were set to `WAITING_FOR_CHATGPT_REVIEW` for CNX-386.
- The original executor handoff HEAD was `2bfe33d4eedc66030dc083999267ce1fb616d4d0`.
- This report correction does not alter production state or historical task evidence.
- CNX-387 task specification was added afterward as a documentation correction; its execution is not claimed here.
- `main`, tags, and releases are unchanged.
