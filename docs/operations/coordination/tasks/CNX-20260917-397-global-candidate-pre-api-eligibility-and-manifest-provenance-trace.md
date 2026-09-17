# CNX-20260917-397 — Global Candidate Pre-API Eligibility and Manifest Provenance Trace

## Purpose

Resolve the next causal boundary after CNX-396.

CNX-396 established from exact OpenClaw `2026.7.1-2` source that `origin=config` and `origin=global` candidates enter the same normalized configuration producer and downstream lookup path before `createApi({ hookPolicy })`. Exact global-origin A/B replay remained diagnostically blocked because reproducing the real global discovery path would require mutating production global installation state.

The remaining uncertainty is therefore earlier in the global candidate lifecycle:

> Did the production global candidate resolve to the expected manifest/root/plugin identity and pass the pre-API eligibility gates that can prevent `entry = normalized.entries[pluginId]` from reaching `createApi`?

This task is diagnosis only. No production mutation is authorized.

## Parent

`CNX-20260917-396`

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
- CNX-396 report
- CNX-395 report
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
- production inventory:
  `id=cogentnexus-openclaw`, `origin=global`, `status=loaded`, `hookCount=0`, `hookNames=[]`
- production config entry:
  `plugins.entries.cogentnexus-openclaw.enabled=true`
  `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess=true`

## Objective

Trace the exact pre-API candidate lifecycle:

`discovery candidate`
→ `candidate.rootDir`
→ `manifestByRoot.get(candidate.rootDir)`
→ `manifestRecord.id`
→ `pluginId`
→ scoped/candidate filtering
→ duplicate-ID handling
→ enablement resolution
→ registration-plan selection
→ `entry = normalized.entries[pluginId]`
→ `createApi({ hookPolicy })`

Determine whether a global candidate can diverge from an otherwise equivalent config candidate before `createApi` through any difference in:

- discovery root or load path;
- manifest lookup/presence;
- manifest plugin ID;
- scoped candidate filtering;
- duplicate-ID precedence or override state;
- plugin enablement;
- registration-plan existence/mode;
- selected configuration entry;
- any origin-sensitive condition that can suppress API registration.

The task should narrow the remaining production gap without claiming hook acceptance/rejection unless directly evidenced.

## Required investigation

### 1. Exact source trace of all pre-API gates

Start from the known loader point where `candidate.rootDir` is associated with `manifestByRoot` and trace forward/backward through the exact installed OpenClaw source.

Record exact functions and line mappings for:

- candidate collection and global discovery roots;
- manifest index construction and keying;
- root-to-manifest association;
- plugin ID derivation;
- missing-manifest handling;
- scoped candidate filtering;
- duplicate-ID detection and override behavior;
- enablement calculation/defaulting;
- registration-plan selection and null/skip paths;
- the point where `normalized.entries[pluginId]` is actually read;
- the point where `entry?.hooks` becomes `hookPolicy` for `createApi`.

Explicitly identify every branch that can stop registration before `createApi`.

### 2. Production global-root and manifest provenance — read only

Inspect the actual production global extension installation and manifest files without modifying them.

Correlate, where observable:

- effective global extension root;
- manifest path/content relevant to plugin ID;
- installed artifact path and SHA;
- configured plugin ID;
- discovery global-root selection from source;
- startup/discovery log records that identify root, plugin ID, load path, or activation outcome.

Do not treat `plugins list --json` or the persisted installed-plugin index as live-loader proof; use them only as secondary context.

The objective is to establish whether the current production installation has the inputs that the loader's global candidate path requires, not to infer historical in-memory object identity.

### 3. Exact isolated pre-API replay

If the installed OpenClaw internals can be invoked safely without production mutation, build a disposable fixture that exercises the exact loader-side candidate processing with:

- production-shaped normalized config;
- the real target plugin ID;
- a manifest with the target ID;
- one `origin=config` candidate;
- one `origin=global` candidate;
- observable results after manifest association, filtering, deduplication, enablement, and registration-plan selection.

Prefer a true internal function replay over a hand-built imitation. If internal APIs cannot be invoked safely, stop at exact source tracing and explicitly classify the limitation.

A relocated temporary copy is acceptable only as an isolated mechanism probe and must be labeled as synthetic; it is not proof of the already-running production process.

### 4. Candidate-path comparison

For both origins, establish whether the following inputs are identical or can differ:

`rootDir`
`manifestRecord`
`pluginId`
`normalized.entries[pluginId]`
`enabled`
`registrationPlan`
`registrationMode`
`entry?.hooks`

Where they can differ, identify the exact source condition and whether it applies to the production global candidate.

### 5. Compare against CNX-391 through CNX-396

State precisely:

- CNX-391 proved exact config-origin true-policy acceptance through the loader/API lifecycle;
- CNX-392 proved candidate origin is not itself the direct conversation-policy branch selector;
- CNX-393 traced root-to-manifest-to-plugin-ID association but could not observe historical production values;
- CNX-394 established that supported inventory output is a separate installed-index projection;
- CNX-395 established that the installed index predates the current gateway and can refresh independently of live loader activation;
- CNX-396 established one common normalized producer/path but exact global-origin replay remained blocked;
- CNX-397 now determines whether the remaining gap lies in global candidate identity/eligibility before `createApi`.

Do not reopen prior tasks unless contradictory evidence is found.

## Interpretation rules

Do not infer live loader state from persisted inventory/index state.

Do not infer production hook rejection merely because `hookCount=0` or `hookNames=[]` appear in inventory.

Do not infer production hook acceptance merely because the current manifest or artifact is correct.

A source-level or isolated exact-loader replay can establish mechanism behavior, but not historical runtime state of the already-running production process.

If production read-only evidence directly correlates the active global extension root, manifest ID, effective artifact, and startup discovery/activation record strongly enough to establish the candidate inputs, state exactly what is proven and what remains inferred.

## Runtime restrictions

Production is strictly read-only.

Forbidden:

- Gateway restart/reload;
- production configuration mutation;
- environment mutation;
- Scheduled Task mutation;
- production global extension installation/mutation;
- artifact replacement/deploy;
- OpenClaw dependency patch;
- CogentNexus source repair;
- debugger/inspector attachment;
- semantic/model/provider/Dashboard request;
- TicketStore/admission/routing/auth changes;
- production retry;
- permanent instrumentation;
- speculative workaround;
- release/tag/main;
- force-push/history rewrite;
- historical edits to CNX-360 through CNX-396.

Required counts:

- Semantic/model/provider/Dashboard requests: `0`
- Production mutations: `0`

## Required classification

Use exactly one:

`GLOBAL_CANDIDATE_PRE_API_ELIGIBILITY_PROVEN`

`GLOBAL_CANDIDATE_PRE_API_DIVERGENCE_PROVEN`

`GLOBAL_CANDIDATE_PRODUCTION_CORRELATION_INCONCLUSIVE`

`GLOBAL_CANDIDATE_PRE_API_DIAGNOSTICALLY_BLOCKED`

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260917-397-global-candidate-pre-api-eligibility-and-manifest-provenance-trace-report.md`

Include:

- authoritative starting/final HEAD;
- exact OpenClaw/artifact/module hashes;
- exact source line mappings for every pre-API gate;
- production read-only root/manifest/artifact correlation;
- global/config candidate comparison;
- isolated replay, if used;
- direct evidence versus inference;
- effect on the remaining production hook-policy gap;
- semantic/model/provider/Dashboard request count = `0`;
- production mutation count = `0`;
- hard-fence compliance.

## Closeout

After report publication:

- set `ACTIVE.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- set `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- stop;
- do not create/start CNX-398;
- do not modify historical CNX-360 through CNX-396;
- do not modify `main`, tags, or releases.
