# CNX-20260917-396 — Global Candidate Normalized-Config Provenance Trace

## Purpose

Resolve the next causal boundary after CNX-395 by tracing how the loader constructs or selects `normalized` configuration when a plugin candidate has `origin=global`.

CNX-395 proved that the production installed-plugin index is a persisted SQLite projection whose target row predates the current gateway startup and can be refreshed independently of the live loader. It therefore cannot establish what the running loader actually supplied as `hookPolicy` during registration.

CNX-391 independently proved that the exact OpenClaw 2026.7.1-2 loader/API lifecycle accepts production-shaped `plugins.entries.cogentnexus-openclaw.hooks.allowConversationAccess=true` through the config-origin path.

CNX-392 proved from exact source that `origin=global` and `origin=config` do not directly select different conversation-hook policy branches; the host registration mode is taken from `registrationPlan.mode`, not directly from candidate origin.

The remaining causal question is narrower:

> Does a `global` discovery candidate enter the same normalized runtime configuration object, under the same plugin ID, as a `config` candidate before `entry = normalized.entries[pluginId]` and `hookPolicy = entry?.hooks` are evaluated?

This task is diagnosis only. No production mutation is authorized.

## Parent

`CNX-20260917-395`

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

Trace the exact normalized-configuration path before host hook registration:

`runtime config source`
→ `plugin entry normalization`
→ `normalized.entries`
→ `candidate/manifest pluginId`
→ `entry = normalized.entries[pluginId]`
→ `entry?.hooks`
→ `createApi({ hookPolicy })`
→ `registerTypedHook`

Determine whether a `global` candidate can cause any divergence in:

- normalized plugin entry presence;
- normalized plugin ID;
- normalized `hooks.allowConversationAccess`;
- selected config entry;
- hook policy passed to the host API;

relative to a `config` candidate for the same plugin.

The decisive result should establish one of:

1. global and config candidates consume the same normalized entry and same hook policy;
2. global candidate normalization can diverge before `createApi`;
3. the exact production-shaped normalized state cannot be observed under the permitted fences.

## Required investigation

### 1. Exact source trace of normalized configuration

Inspect installed OpenClaw `2026.7.1-2` source read-only.

Trace exact functions and lines for:

- production config loading;
- plugin-entry normalization;
- creation of `normalized.entries`;
- validation/defaulting of `hooks.allowConversationAccess`;
- any transformation keyed by plugin ID;
- the scope/lifetime of the `normalized` object used by the loader;
- the code that chooses or reuses normalized configuration when discovery candidates are processed.

Start from the known line:

`entry = normalized.entries[pluginId]`

and trace backward to the exact producer of `normalized`.

### 2. Candidate-origin comparison

Trace how these two hypothetical paths reach normalization:

`origin=config`

and

`origin=global`

Do not assume origin is irrelevant merely because the final host gate checks the same non-bundled policy branch.

Determine whether candidate origin affects any earlier input to normalization, including:

- selected config object;
- plugin ID derivation;
- load path/profile;
- plugin enablement;
- policy object;
- registration plan;
- candidate filtering/deduplication.

Record exact source evidence.

### 3. Plugin-ID and normalized-entry correlation

Establish the chain for `cogentnexus-openclaw`:

`candidate.rootDir`
→ `manifestRecord.id`
→ `pluginId`
→ `normalized.entries[pluginId]`

Then establish whether:

`normalized.entries["cogentnexus-openclaw"]?.hooks?.allowConversationAccess`

is structurally the same value for global and config candidate paths.

Matching strings alone are insufficient; show the source path that supplies each value.

### 4. Safe isolated probe

If exact loader internals can be invoked without production installation or mutation, build a disposable probe using the installed OpenClaw module graph.

Prefer an A/B fixture with:

- identical production-shaped config;
- same plugin ID;
- one candidate marked `origin=config`;
- one candidate marked `origin=global`;
- observable normalized entry and resulting hook policy.

The probe must not install anything into the production global extension tree.

If internal APIs cannot be invoked safely, do not create a fake result. Use source tracing and classify the limitation explicitly.

Any synthetic fixture is mechanism evidence only, not historical production proof.

### 5. Compare against CNX-391 through CNX-395

State precisely:

- CNX-391 proves true-policy acceptance in exact config-origin loader/API replay;
- CNX-392 proves origin is not directly used as the conversation-hook policy branch selector;
- CNX-393 traces candidate/root/plugin-ID association but could not observe production live values;
- CNX-394 proves `plugins list --json` is an installed-index projection, not live typed-hook registry state;
- CNX-395 proves the production index row predates the current gateway and can be refreshed independently of live loader activation;
- CNX-396 determines whether global-vs-config divergence exists earlier, at normalized configuration input/selection.

Do not reopen prior tasks unless genuinely contradictory evidence appears.

## Interpretation rules

Do not infer live runtime state from the installed-plugin index.

Do not infer equality of global/config paths merely from a shared downstream gate.

Do not treat matching plugin IDs as proof that identical normalized objects were used.

Do not claim production hook acceptance or rejection.

Do not claim Dashboard Ticket-first semantic success.

If the normalized producer is common and the same `hooks.allowConversationAccess=true` value is demonstrated for both origins in an exact isolated replay, treat that as strong mechanism evidence that the remaining gap lies after normalization. It is still not historical proof about the already-running production process.

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
- production retry;
- permanent instrumentation;
- speculative workaround;
- release/tag/main;
- force-push/history rewrite;
- historical edits to CNX-360 through CNX-395;
- creation/start of CNX-397.

Required counts:

- Semantic/model/provider/Dashboard requests: `0`
- Production mutations: `0`

## Required classification

Use exactly one:

`GLOBAL_CONFIG_NORMALIZATION_PATH_PROVEN_EQUIVALENT`

`GLOBAL_CONFIG_NORMALIZATION_DIVERGENCE_PROVEN`

`GLOBAL_CONFIG_NORMALIZATION_INCONCLUSIVE`

`GLOBAL_CONFIG_NORMALIZATION_DIAGNOSTICALLY_BLOCKED`

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260917-396-global-candidate-normalized-config-provenance-trace-report.md`

Include:

- authoritative starting/final HEAD;
- exact OpenClaw/artifact/module hashes;
- exact normalized-config producer and line mappings;
- global/config candidate path comparison;
- plugin-ID correlation;
- `hooks.allowConversationAccess` provenance;
- isolated A/B probe, if used;
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
- do not create/start CNX-397;
- do not modify historical CNX-360 through CNX-395;
- do not modify `main`, tags, or releases.
