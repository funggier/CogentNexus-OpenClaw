# CNX-20260917-398 — Global-Origin-Only Pre-API Eligibility A/B Replay

## Purpose

Resolve the next causal question after CNX-397:

> When every candidate input is held constant and only `candidate.origin` changes between `config` and `global`, does the exact OpenClaw 2026.7.1-2 pre-API lifecycle produce any eligibility, filtering, enablement, duplicate-order, registration-plan, or `createApi` divergence?

CNX-396 proved a common normalized configuration producer/path for both origins but could not perform an exact global-origin replay under production hard fences. CNX-397 then traced the pre-API gates and showed that global candidates can theoretically diverge through root/path, manifest association, filtering, duplicate precedence, enablement, and registration-plan inputs, while production read-only evidence did not prove which gate, if any, caused the historical production failure.

CNX-398 therefore isolates **origin itself** as a variable. This is a mechanism diagnosis task, not a production requalification task.

## Parent

`CNX-20260917-397`

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
- CNX-397 report
- CNX-396 report
- CNX-395 report
- CNX-394 report
- CNX-393 report
- CNX-392 report
- CNX-391 report

Record the exact starting HEAD.

Known expected starting HEAD after CNX-397 closeout:

`d87d8886ac311cff582f49b84377150ef1c50451`

Do not assume this remains current; verify it from GitHub before execution.

## Objective

Construct an exact isolated A/B replay using the installed OpenClaw `2026.7.1-2 (0790d9f)` module graph where:

- all normalized plugin configuration inputs are identical;
- the plugin ID is identical;
- the candidate root and manifest identity are identical;
- filtering inputs are identical;
- candidate ordering context is identical except where origin is itself required by the fixture;
- enablement inputs are identical;
- registration-plan inputs are identical;
- the only intentional candidate-level difference is:
  - Case A: `origin="config"`
  - Case B: `origin="global"`

Observe the exact results before API construction and, where safely possible in a disposable process, at `createApi`/hook registration.

The decisive question is whether `origin` alone changes any pre-API decision relevant to `before_agent_run` registration.

## Required investigation

### 1. Exact source trace of origin-sensitive inputs

Starting from CNX-397's proven gates, inspect the exact installed OpenClaw source for all places between candidate creation and `createApi` where `candidate.origin` can affect behavior.

Specifically trace:

- candidate sorting / duplicate ordering;
- manifest-root association;
- scoped filtering;
- plugin enablement resolution;
- effective activation state;
- registration-plan selection;
- setup/trust predicates;
- module/export/ID validation;
- `normalized.entries[pluginId]` lookup;
- `entry?.hooks` and `hookPolicy` construction.

Separate:

1. origin-sensitive branches that actually change a value/decision;
2. origin passed as inert metadata;
3. branches whose origin predicate excludes only `workspace` or `bundled`, not `config` vs `global`.

### 2. Exact isolated A/B fixture

Use the real installed OpenClaw module graph where internal APIs are callable without modifying production.

Fixture requirements:

- disposable temporary state only;
- no production global extension tree writes;
- same plugin manifest object for both cases;
- same `rootDir` value where the API accepts it as fixture data;
- same normalized config object;
- same `manifestRecord.id = "cogentnexus-openclaw"`;
- same module/export shape;
- same enablement/configuration inputs;
- origin is the only intentional variable.

Capture at minimum:

- candidate accepted/rejected;
- candidate ordering position if applicable;
- effective enablement;
- duplicate/override outcome;
- selected registration plan and mode;
- selected `normalized.entries[pluginId]` presence;
- `entry?.hooks?.allowConversationAccess` value;
- whether ordinary `createApi` is reached;
- whether `api.on("before_agent_run")` reaches typed-hook storage.

Run enough repetitions to rule out fixture-order artifacts, but do not create a benchmark or permanent test harness unless a minimal disposable script is necessary.

### 3. Production correlation

Use read-only production evidence only to establish which origin-sensitive inputs are currently known:

- production global extension root;
- manifest ID/version;
- configured plugin ID and enablement;
- configured hook policy;
- effective artifact SHA;
- supported inventory origin.

Do not claim the isolated A/B result proves historical production behavior.

The purpose of production observation here is only to identify whether any A/B-tested input corresponds to a known production datum.

### 4. Interpretation matrix

If only `origin` changes and both cases produce the same eligibility, same registration plan, same normalized entry, same hook policy, and same `createApi`/typed-hook outcome, classify origin-only divergence as disproven at this boundary.

If `origin=global` changes a concrete pre-API decision while all other inputs are held constant, classify origin-only divergence as proven and document the exact branch and consequence.

If exact internal invocation remains impossible without forbidden mutation/debugging, classify diagnostically blocked rather than substituting a synthetic approximation.

Synthetic fixtures are mechanism evidence only.

## Required classification

Use exactly one:

`GLOBAL_ORIGIN_ONLY_PRE_API_EQUIVALENCE_PROVEN`

`GLOBAL_ORIGIN_ONLY_PRE_API_DIVERGENCE_PROVEN`

`GLOBAL_ORIGIN_ONLY_PRE_API_INCONCLUSIVE`

`GLOBAL_ORIGIN_ONLY_PRE_API_DIAGNOSTICALLY_BLOCKED`

## Hard fences

Production is strictly read-only.

Forbidden:

- Gateway restart/reload;
- production configuration mutation;
- environment mutation;
- Scheduled Task mutation;
- production global extension installation/mutation;
- production artifact replacement/deploy;
- OpenClaw dependency patch;
- CogentNexus source repair;
- debugger/inspector attachment;
- semantic/model/provider/Dashboard request;
- TicketStore/admission/routing/auth changes;
- production retry;
- speculative workaround;
- permanent instrumentation;
- release/tag/main;
- force-push/history rewrite;
- historical edits to CNX-360 through CNX-397;
- creation/start of CNX-399.

Temporary disposable isolated files are allowed only if they are outside the production installation/state and are deleted/cleaned after use.

Required counts:

- Semantic/model/provider/Dashboard requests: `0`
- Production mutations: `0`

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260917-398-global-origin-only-pre-api-eligibility-ab-replay-report.md`

Include:

- exact authoritative starting/final HEAD;
- OpenClaw/artifact/module hashes;
- exact origin-sensitive source line mappings;
- fixture construction and exact invariant/variable fields;
- Case A (`config`) results;
- Case B (`global`) results;
- side-by-side comparison;
- production read-only correlation;
- direct evidence versus inference;
- effect on the remaining production hook-policy gap;
- counts and hard-fence compliance.

## Closeout

After report publication:

- set `ACTIVE.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- set `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- verify local HEAD equals remote HEAD;
- verify clean worktree;
- stop;
- do not create/start CNX-399;
- do not modify historical CNX-360 through CNX-397;
- do not modify `main`, tags, or releases.
