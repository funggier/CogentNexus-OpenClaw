# CNX-20260917-395 — Installed Plugin-Index Population / Freshness Provenance Trace

## Purpose

Resolve the remaining identity gap after CNX-394 by tracing how the persisted/derived installed-plugin index used by `openclaw plugins list --json` is populated and refreshed.

CNX-394 proved:

- the live loader assigns `pluginId = manifestRecord.id`;
- the live loader selects `entry = normalized.entries[pluginId]`;
- the live loader creates its plugin record with `id: pluginId`;
- the live loader inserts that record into its runtime registry;
- `openclaw plugins list --json` does not directly serialize that live loader record;
- the command loads a persisted/derived installed-plugin index and constructs a new inventory object;
- inventory `id` is read from `plugin.pluginId` in that index;
- inventory `hookCount` and `hookNames` are independently initialized to `0` and `[]`, so those fields do not report live typed-hook registration state.

The remaining question is therefore not whether inventory currently displays the expected string. It is whether the installed-plugin index entry containing `pluginId=cogentnexus-openclaw` was produced from the same loader/plugin identity during the relevant production activation, or whether it can be stale, independently derived, or populated by another path.

This task is diagnosis only. No production mutation is authorized.

## Parent

`CNX-20260917-394`

## Branch

`cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Executor / Reviewer

Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`

## Starting authority

Begin from the authoritative branch HEAD and re-read:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`
- this task
- CNX-394 report
- CNX-393 report
- CNX-392 report
- CNX-391 report

Record the authoritative starting HEAD in the final report.

Known baseline:

- OpenClaw `2026.7.1-2 (0790d9f)`
- effective CogentNexus artifact SHA-256:
  `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- production config SHA-256:
  `19d7e6acf53ce370ddc20e5e2a2547c9674c33b178208b79920cb0e9dce9b46b`
- production inventory currently reports:
  `id=cogentnexus-openclaw`
  `rootDir=C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw`
  `origin=global`
  `status=loaded`
  `hookCount=0`
  `hookNames=[]`

## Objective

Trace the exact lifecycle of the installed-plugin index entry used by `plugins list --json`:

`loader/plugin identity`
→ `installed-index write/update path`
→ `persisted/derived installed-index record`
→ `loadPluginRegistrySnapshotWithMetadata`
→ `buildPluginRecordFromInstalledIndex`
→ `plugins list --json`

Determine whether the index's `pluginId` can be directly and time-correlated to the loader's `manifestRecord.id` for the production activation, using only read-only evidence.

The decisive question is:

> Can the current persisted/derived installed-plugin index entry be established as a contemporaneous projection of the same production loader identity, or is its provenance/freshness independent of the running loader lifecycle?

## Required investigation

### 1. Exact installed-index source trace

Inspect the exact installed OpenClaw `2026.7.1-2` module graph read-only.

Trace:

- installed-index schema and record reader;
- index store/load functions;
- index write/update functions;
- all call sites that populate or refresh `pluginId`, `rootDir`, `origin`, `enabled`, and source/manifest metadata;
- whether any write path receives the live loader record or `manifestRecord.id` directly;
- whether any write path can run from discovery, installation, enable/disable, migration, or other CLI state independently of live activation;
- how persisted versus derived index sources are selected.

Record exact file/function/line evidence.

### 2. Provenance of `pluginId`

For every relevant index population path, determine where `pluginId` comes from.

Build an evidence table:

| Index population path | Input identity | Stored `pluginId` | Root/source fields | Trigger/context | Direct loader linkage? |
|---|---|---|---|---|---|
| Path A | observed | observed | observed | observed | yes/no/unresolved |
| Path B | observed | observed | observed | observed | yes/no/unresolved |

Do not infer direct linkage from matching strings.

### 3. Freshness / timestamp evidence

Read-only inspect the production installed-index storage and any associated metadata that is safely exposed without mutation.

Determine, where possible:

- index file/path;
- record or snapshot generation timestamp;
- last-write timestamp;
- schema/version metadata;
- whether the index was created/updated before or after the current production gateway process started;
- whether the index contains the target `pluginId`, `rootDir`, and `origin` together;
- whether source/manifest fields correspond to the current effective artifact.

Do not print secrets.

A timestamp relationship may narrow provenance but must not be treated as proof of object identity by itself.

### 4. Current production read-only correlation

Use only supported read-only commands/files.

Collect, without restarting or reloading production:

- current gateway PID and start time if already available through supported observation;
- current inventory record;
- installed-index record for the target plugin if safely readable;
- relevant index metadata;
- production config key and non-secret `enabled` / `hooks.allowConversationAccess` state.

Do not mutate any production file.

### 5. Disposable isolated provenance probe

Only when technically safe and outside production:

Use the exact installed OpenClaw module graph in a disposable state to exercise the index population path.

Prefer a fixture where:

- a loader/plugin record has a known `id`;
- the installed-index write/update path is invoked;
- the resulting index record can be read back;
- the `pluginId` source is observable;
- a control record with a different plugin identity demonstrates whether the index stores the input loader ID or derives another identifier.

Do not install a test plugin into the production global extension tree.

Do not patch OpenClaw.

Do not add permanent instrumentation.

A synthetic provenance probe is mechanism evidence only and must not be presented as proof of historical production activation.

### 6. Compare persisted and derived modes

The CNX-394 report established that the inventory snapshot can be persisted or derived.

Trace the exact branch selection and determine:

- what conditions select persisted versus derived data;
- whether the derived path reads current discovery/loader data or another index;
- whether either path bypasses the live activation registry;
- whether both paths preserve `pluginId` without transformation.

This comparison is important because a fresh-looking inventory entry does not necessarily mean it was generated by the current live process.

### 7. Compare with CNX-391 through CNX-394

Explain precisely what this task changes in the evidence chain:

- CNX-391: true-policy acceptance through exact config-origin loader/API lifecycle;
- CNX-392: global/config origin does not select a different conversation-hook branch;
- CNX-393: global candidate association reaches `manifestRecord.id → normalized.entries[pluginId]`, but the live values were unobservable;
- CNX-394: inventory is a separate installed-index projection, and its hook fields are not live registry fields;
- CNX-395: determine whether that installed-index projection has direct population/freshness linkage to the production loader identity.

Do not reopen prior tasks unless genuinely contradictory evidence appears.

## Interpretation rules

- Matching `pluginId` strings are not sufficient proof of runtime identity.
- A current index timestamp after process start is not by itself proof that the current loader wrote it.
- An index timestamp before process start is evidence against contemporaneous creation, but do not overstate what it proves about later updates.
- Do not claim production hook acceptance or rejection.
- Do not treat inventory `hookCount=0` or `hookNames=[]` as live registry evidence.
- Do not claim registry-composition loss.
- Do not claim Dashboard Ticket-first semantic success.
- Keep historical production memory/lifecycle claims separate from read-only persisted-state evidence.

## Runtime restrictions

Production is strictly read-only.

Forbidden:

- Gateway restart/reload;
- production configuration mutation;
- environment mutation;
- Scheduled Task mutation;
- production artifact replacement/deploy;
- dependency patch;
- CogentNexus source repair;
- debugger/inspector attachment;
- semantic/model/provider/Dashboard request;
- production retry;
- permanent instrumentation;
- installation of any disposable test plugin into the production global extension tree.

Disposable isolated files/probes are allowed outside production and should not be committed unless a narrowly scoped regression is required to preserve a proven mechanism.

## Required classification

Use exactly one:

`INSTALLED_INDEX_PROVEN_CONTEMPORANEOUS_LOADER_PROJECTION`

`INSTALLED_INDEX_PROVEN_INDEPENDENT_OF_LIVE_LOADER`

`INSTALLED_INDEX_PROVEN_STALE_OR_PREEXISTING`

`INSTALLED_INDEX_PROVENANCE_INCONCLUSIVE`

`INSTALLED_INDEX_DIAGNOSTICALLY_BLOCKED`

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260917-395-installed-plugin-index-population-freshness-provenance-report.md`

Include:

- authoritative starting/final HEAD;
- exact OpenClaw/artifact/module hashes;
- exact installed-index paths/functions and population chain;
- `pluginId` provenance;
- persisted/derived branch selection;
- production inventory/index correlation;
- timestamp/freshness evidence;
- isolated provenance probe, if any;
- direct evidence versus inference;
- whether CNX-394's identity gap is reduced or closed;
- remaining uncertainty;
- semantic/model/provider/Dashboard request count = `0`;
- production mutation count = `0`;
- hard-fence compliance.

## Closeout

After publication:

- set `ACTIVE.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- set `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- stop;
- do not create/start CNX-396;
- do not modify historical CNX-360 through CNX-394;
- do not modify `main`, tags, or releases.
