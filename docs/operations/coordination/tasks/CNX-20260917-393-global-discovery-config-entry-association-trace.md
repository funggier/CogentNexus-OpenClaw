# CNX-20260917-393 — Global Discovery / Config-Entry Association Trace

## Purpose

Resolve the remaining production discrepancy after CNX-392 by tracing how a globally discovered plugin candidate (`origin=global`) is associated with the normalized runtime configuration entry used for `hookPolicy`.

CNX-391 proved that the exact production-shaped plugin configuration with `hooks.allowConversationAccess=true` is accepted by the real OpenClaw loader/API lifecycle when replayed through a configuration-origin path.

CNX-392 proved from the exact installed OpenClaw `2026.7.1-2` source that:

- `origin="global"` and `origin="config"` are discovery metadata assigned at candidate construction;
- both origins use the same non-bundled conversation-hook policy branch because the gate distinguishes only `record.origin === "bundled"`;
- `registrationMode` comes from `registrationPlan.mode`, not directly from the origin string;
- the ordinary runtime `createApi` path still receives `hookPolicy: entry?.hooks`.

CNX-392 could not safely reproduce the real `origin=global` discovery path without mutating or installing into the production global extension tree.

The remaining high-value question is therefore:

> For a globally discovered plugin candidate, how does OpenClaw identify and select the normalized `entry = normalized.entries[pluginId]` used for `hookPolicy`, and can candidate/plugin-ID/path matching cause the production global candidate to miss the configuration entry even though the on-disk config contains `hooks.allowConversationAccess=true`?

This task is diagnosis only. No production mutation is authorized.

## Parent

`CNX-20260917-392`

## Branch

`cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Executor / Reviewer

Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`

## Starting authority

Begin from authoritative branch HEAD and re-read:

- `ACTIVE.md`
- `STATUS.md`
- this task
- CNX-392 report
- CNX-391 report
- CNX-390 report
- CNX-389 report
- CNX-388 report
- CNX-385 report
- CNX-382 report
- CNX-381 report

Record authoritative starting HEAD in the report.

Known baseline:

- OpenClaw `2026.7.1-2 (0790d9f)`
- exact effective CogentNexus artifact SHA:
  `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- production config SHA:
  `19d7e6acf53ce370dc20e5e2a2547c9674c33b178208b79920cb0e9dce9b46b`
- production inventory symptom:
  `origin=global`, `status=loaded`, `hookCount=0`, `hookNames=[]`

## Objective

Trace the exact association path among:

`discovery candidate`
→ `candidate.id / pluginId`
→ `normalized.entries[pluginId]`
→ `entry.hooks`
→ `createApi(... hookPolicy: entry?.hooks)`
→ `registerTypedHook`

The decisive question is whether a globally discovered candidate can legitimately have a different or missing `entry` association despite the same plugin ID appearing in `plugins.entries.cogentnexus-openclaw`.

## Required investigation

### 1. Exact source trace

Inspect the installed OpenClaw `2026.7.1-2` source read-only.

Trace:

- discovery candidate construction for `origin=global`;
- plugin ID/name/path derivation;
- normalization of `plugins.entries`;
- the exact statement assigning `entry = normalized.entries[pluginId]`;
- any candidate/plugin matching or deduplication step between discovery and loader record creation;
- any map/index keyed by plugin ID, source path, root directory, or manifest identifier;
- any branch where the normalized config entry can be omitted even though the plugin candidate loads;
- any difference between global-discovered and config-discovered candidate handling before `createApi`.

Record exact file/function/line evidence.

### 2. Production config linkage

Read the production config read-only and establish:

- exact key `plugins.entries.cogentnexus-openclaw` exists;
- normalized-relevant `hooks.allowConversationAccess=true` is present;
- plugin entry ID and candidate ID naming are identical or, if not, explain the mapping;
- enabled/disabled/config fields relevant to loader association.

Do not expose secrets.

### 3. Candidate/entry association matrix

Build a source-backed matrix for both discovery origins:

| Candidate origin | Candidate/plugin ID | Config entry lookup key | `entry` expected | `entry.hooks` source | createApi hookPolicy |
|---|---|---|---|---|---|
| config | observed/source-traced | observed | observed | observed | observed |
| global | observed/source-traced | observed | observed/source-traced | observed/source-traced | observed/source-traced |

Do not fill unknown cells with inference; mark them unresolved.

### 4. Isolated exact association probe

Only if technically safe and without touching production, construct a disposable probe that directly exercises the loader's candidate-to-entry association logic.

The preferred probe should use the exact loader/module graph and exact artifact, but does not need to reproduce the entire global extension installation.

Good evidence includes:
- direct observation of the `pluginId` used for normalized-entry lookup;
- direct observation of whether `normalized.entries[pluginId]` exists for the candidate;
- direct observation of `entry.hooks` at `createApi` for both a config-origin and a global-origin-equivalent candidate;
- a controlled candidate fixture that changes only the candidate identity/path while keeping the same config entry.

If producing a true `origin=global` candidate requires production installation/discovery mutation, do not do it. A synthetic object may be used only to inspect deterministic association functions, but must be clearly labeled as source-level/isolated mechanism evidence and not as a global-origin production reproduction.

### 5. Exact production correlation if read-only supported data permits

Use only existing production diagnostics/logs/files to see whether any logged plugin ID, source path, rootDir, manifest identity, or normalized-entry metadata can be correlated to the global candidate.

Do not restart production and do not add instrumentation.

### 6. Compare with CNX-391

Explain precisely why CNX-391's config-origin acceptance does or does not imply that the production global candidate should receive the same `entry.hooks`.

Do not relabel isolated association evidence as production memory proof.

## Interpretation rules

- Do not assume same plugin ID means same loader record when discovery can deduplicate or normalize candidates.
- Do not assume `origin=global` means `entry` is absent; prove it.
- Do not assume `entry.hooks` comes from candidate metadata; source trace must show its origin.
- Do not claim production hook acceptance or rejection from association analysis alone.
- Do not claim registry composition loss.
- Do not reopen CNX-385 normalization, CNX-388 launch provenance, or CNX-389 environment unless contradictory evidence appears.
- `hookCount=0` remains a symptom unless association evidence ties it to a specific missing policy.

## Runtime restrictions

Production is strictly read-only.

Forbidden:

- Gateway restart/reload;
- production config mutation;
- environment mutation;
- Scheduled Task mutation;
- production artifact replacement/deploy;
- dependency patch;
- CogentNexus source repair;
- debugger/inspector attachment;
- semantic/model/provider/Dashboard request;
- production retry;
- permanent instrumentation;
- installation of a disposable test plugin into the production global extension tree.

Disposable source-level probes and temporary isolated files are allowed outside production and must not be committed unless a narrowly scoped regression is required to preserve a proven mechanism.

## Required classification

Use exactly one:

`GLOBAL_CONFIG_ENTRY_ASSOCIATION_PROVEN`

`GLOBAL_CONFIG_ENTRY_ASSOCIATION_NOT_CAUSAL`

`GLOBAL_CONFIG_ENTRY_ASSOCIATION_INCONCLUSIVE`

`GLOBAL_CONFIG_ENTRY_ASSOCIATION_DIAGNOSTICALLY_BLOCKED`

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260917-393-global-discovery-config-entry-association-trace-report.md`

Include:

- authoritative starting/final HEAD;
- exact OpenClaw/artifact/module hashes;
- production inventory symptom;
- exact discovery-origin source trace;
- candidate/plugin-ID derivation;
- normalized `entry` lookup path;
- `entry.hooks` to `hookPolicy` path;
- production config linkage;
- config-origin versus global-origin association comparison;
- isolated probe evidence, if any;
- direct evidence versus inference;
- whether the association mechanism narrows the production gap;
- semantic/model/provider/Dashboard request count = `0`;
- production mutation count = `0`;
- hard-fence compliance;
- remaining uncertainty.

## Closeout

After publication:

- set `ACTIVE.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- set `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- stop;
- do not create/start CNX-394;
- do not modify historical CNX-360 through CNX-392;
- do not modify `main`, tags, or releases.
