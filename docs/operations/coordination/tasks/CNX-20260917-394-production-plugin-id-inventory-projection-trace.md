# CNX-20260917-394 — Production Plugin-ID / Inventory Projection Trace

## Purpose

Resolve the next remaining observability gap after CNX-393 by tracing how the production plugin inventory record exposed by `openclaw plugins list --json` obtains its `id`, `rootDir`, `origin`, `status`, and hook-count fields from the loader/registry state.

CNX-393 proved from the exact installed OpenClaw `2026.7.1-2` source that the loader's hook-policy association path is:

`candidate.rootDir → manifestByRoot.get(candidate.rootDir) → manifestRecord.id → normalized.entries[pluginId] → entry?.hooks → createApi(hookPolicy) → registerTypedHook`

CNX-393 also established that the current production inventory reports:

- `id = cogentnexus-openclaw`
- `rootDir = C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw`
- `origin = global`
- `status = loaded`
- `hookCount = 0`
- `hookNames = []`

The remaining uncertainty is whether that inventory `id` is a direct projection of the same `pluginId = manifestRecord.id` used for `normalized.entries[pluginId]`, or whether another registry/serialization layer can rewrite, normalize, or otherwise decouple the displayed inventory ID from the loader lookup identity.

This task is diagnosis only. No production mutation is authorized.

## Parent

`CNX-20260917-393`

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
- CNX-393 report
- CNX-392 report
- CNX-391 report
- CNX-390 report
- CNX-389 report
- CNX-388 report

Record authoritative starting HEAD in the report.

Known baseline:

- OpenClaw `2026.7.1-2 (0790d9f)`
- exact effective CogentNexus artifact SHA:
  `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- production config SHA:
  `19d7e6acf53ce370ddc20e5e2a2547c9674c33b178208b79920cb0e9dce9b46b`
- production inventory symptom:
  `origin=global`, `status=loaded`, `hookCount=0`, `hookNames=[]`
- authoritative starting HEAD for CNX-394:
  `dac8539b9bf1d43fb71754872a97c7ec8026e6b3`

## Objective

Determine whether the production inventory record's displayed plugin ID is provably the same identity used by the loader for:

`pluginId = manifestRecord.id`

and therefore for:

`entry = normalized.entries[pluginId]`

The decisive question is:

> Does `openclaw plugins list --json` expose the exact loader/registry `pluginId` used for normalized config-entry lookup, or can an intermediate inventory projection alter/detach that identity?

A positive result does not prove hook acceptance. It only removes or narrows the candidate-ID association uncertainty.

## Required investigation

### 1. Trace loader record construction

Inspect the exact installed OpenClaw `2026.7.1-2` source read-only.

Trace from:

- `manifestRecord.id` / `pluginId`;
- loader record construction after `normalized.entries[pluginId]`;
- registry insertion/registration;
- any later record normalization or projection;
- fields used to populate plugin inventory output: `id`, `rootDir`, `origin`, `status`, `hookCount`, `hookNames`.

Record exact file/function/line evidence.

### 2. Trace the `plugins list --json` projection

Identify the command implementation and trace:

`plugins list --json → registry/loader state → inventory record → serialized JSON`

Determine exactly where the output `id` comes from.

Specifically establish whether it is:

- the original `manifestRecord.id` / `pluginId`;
- a registry key;
- a derived/normalized name;
- a separate inventory identifier.

Also determine whether `hookCount` and `hookNames` are calculated from the same registry object that receives `registerTypedHook`, if that can be proven read-only.

### 3. Production read-only correlation

Using supported diagnostics only, collect the current production inventory for the target plugin and correlate:

- inventory `id`;
- `rootDir`;
- `origin`;
- status;
- hook count/names;
- production configuration key `plugins.entries.cogentnexus-openclaw`.

Do not print secrets.

Do not infer internal object identity merely because values are equal; the source projection path must establish it.

### 4. Isolated exact projection probe

Only if technically safe and without touching production, use a disposable isolated OpenClaw fixture or exact module graph to verify that a known `manifestRecord.id` / `pluginId` appears unchanged in plugin inventory output.

Good evidence includes:

- a controlled manifest ID with a matching normalized entry;
- observed loader `pluginId`;
- observed registry record ID;
- observed `plugins list --json` ID;
- equality established through source path and runtime observation.

A synthetic object may be used only for deterministic projection functions and must be clearly labeled mechanism evidence.

Do not install or mutate any disposable plugin in the production global extension tree.

### 5. Compare against CNX-393 and CNX-391

Explain precisely what the projection result changes:

- If inventory `id` is proven to be the same loader `pluginId`, state that CNX-393's remaining uncertainty is narrowed to whether `normalized.entries[pluginId]` actually existed/populated in the live loader at registration time.
- If inventory `id` can differ, identify the exact transformation and whether it could explain a missing `entry.hooks` policy.
- Do not relabel projection evidence as direct proof of historical in-memory `hookPolicy` unless the source path and runtime observation establish it.

## Interpretation rules

- Do not treat equal strings alone as object identity proof.
- Do not assume inventory output is a raw loader record; prove its projection source.
- Do not infer hook acceptance/rejection from `hookCount=0` alone.
- Do not claim registry-composition loss unless direct evidence establishes it.
- Do not claim Dashboard Ticket-first semantic success.
- Do not reopen CNX-385 normalization, CNX-388 launch provenance, CNX-389 environment, or CNX-393 association unless contradictory evidence appears.
- Keep production historical in-memory state separate from current read-only inventory.

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

`PRODUCTION_PLUGIN_ID_PROJECTION_PROVEN`

`PRODUCTION_PLUGIN_ID_PROJECTION_NOT_CAUSAL`

`PRODUCTION_PLUGIN_ID_PROJECTION_INCONCLUSIVE`

`PRODUCTION_PLUGIN_ID_PROJECTION_DIAGNOSTICALLY_BLOCKED`

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260917-394-production-plugin-id-inventory-projection-trace-report.md`

Include:

- authoritative starting/final HEAD;
- exact OpenClaw/artifact/module hashes;
- production inventory snapshot;
- exact loader plugin-ID source;
- registry record construction;
- `plugins list --json` projection path;
- `hookCount` / `hookNames` projection path if provable;
- production config linkage;
- isolated probe evidence, if any;
- direct evidence versus inference;
- what uncertainty from CNX-393 is removed or remains;
- semantic/model/provider/Dashboard request count = `0`;
- production mutation count = `0`;
- hard-fence compliance;
- remaining uncertainty.

## Closeout

After publication:

- set `ACTIVE.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- set `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- stop;
- do not create/start CNX-395;
- do not modify historical CNX-360 through CNX-393;
- do not modify `main`, tags, or releases.
