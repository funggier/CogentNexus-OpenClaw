# CNX-20260918-402 — Production Artifact Identity and Registry-Lineage Reconciliation

## Purpose

Resolve the production-identity discrepancy exposed during CNX-401 review before attributing registry/cache behavior to the running Gateway.

CNX-401 proved from exact OpenClaw source that active registry replacement is a real mechanism. However, its report records a production artifact identity of:
- `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-dashboard-verified-delivery.js`
- SHA-256 `1276bd624b62f96692eaa19f493f69e422771b6994b39ded94b2bcb3399e1f98`

The established production baseline in prior accepted tasks is:
- `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
- SHA-256 `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`

No production artifact replacement was authorized or reported in CNX-401. Therefore the discrepancy must be resolved as identity/provenance evidence before later causal conclusions rely on CNX-401's production correlation.

This task is read-only diagnosis and document correction only. No production mutation is authorized.

## Parent

`CNX-20260918-401`

## Branch

`cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Executor / Reviewer

Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`

## Starting authority

Begin from the authoritative branch HEAD and re-read:
- `ACTIVE.md`
- `STATUS.md`
- this task
- CNX-401 report
- CNX-400 report
- CNX-399 report
- CNX-398 through CNX-391 reports

Record exact starting HEAD from GitHub.

Known expected starting HEAD:
`fe07c5660f765360ace580eb768362908de71b07`

Verify; do not assume.

## Objective

Determine whether the CNX-401 artifact identity difference is:

1. a report-only transcription/path error;
2. a real alternate production artifact that was active in the relevant Gateway lifecycle;
3. a historical artifact used by an isolated test rather than production;
4. an artifact alias/delivery filename that resolves to identical or different bytes;
5. an unexplained identity conflict that blocks production correlation.

Do not modify production to resolve this.

## Required investigation

### 1. Exact production artifact identity

Using read-only production inspection, establish:
- current effective CogentNexus artifact path;
- SHA-256 of that exact file;
- manifest/loader selected artifact path if observable;
- process/PID relationship;
- modification timestamps;
- whether both `v091-release-entry.js` and `v091-dashboard-verified-delivery.js` exist;
- SHA-256 for both if both exist.

Do not replace, rename, copy over, or edit files.

### 2. Historical artifact provenance

Inspect accepted prior reports CNX-369 through CNX-400 and identify every authoritative production artifact path/SHA assertion.

Determine whether `1276bd…` appears as:
- production artifact;
- isolated fixture artifact;
- historical artifact;
- stale/transcribed value.

Do not rewrite historical reports merely to make them consistent. If CNX-401 contains a report-local identity mistake, record that precisely.

### 3. Runtime process correlation

Read-only only:
- current Gateway PID;
- command line;
- executable/module paths if safely observable;
- loaded plugin entry path if supported diagnostics expose it;
- production log references to artifact path/version;
- gateway startup chronology.

Do not restart, inspect, debug, or inject.

### 4. Byte identity / alias analysis

If both filenames exist, compare:
- exact SHA-256;
- file size;
- relevant manifest references;
- whether one imports/delegates to the other.

If hashes differ, do not assume semantic equivalence.

### 5. Impact on CNX-401

State whether CNX-401's mechanism proof remains valid independently of artifact identity.

Separately state whether its production-application statements remain:
- usable;
- usable only after correcting report metadata;
- or blocked pending identity resolution.

Do not relabel the CNX-401 classification unless the evidence requires it.

### 6. Correction policy

If the discrepancy is a report-only mistake, create a minimal correction commit touching only the CNX-401 report. Do not alter CNX-360 through CNX-400.

The correction must:
- preserve historical facts;
- distinguish current production baseline from isolated/test artifact identities;
- not invent a provenance story.

If it is not safely resolvable, leave the historical report unchanged and classify the task accordingly.

## Required classification

Use exactly one:

`PRODUCTION_ARTIFACT_IDENTITY_RECONCILED`

`PRODUCTION_ARTIFACT_IDENTITY_CONFLICT_UNRESOLVED`

`PRODUCTION_ARTIFACT_IDENTITY_INCONCLUSIVE`

`PRODUCTION_ARTIFACT_IDENTITY_DIAGNOSTICALLY_BLOCKED`

Use RECONCILED only with direct read-only evidence supporting the final identity mapping.

## Hard fences

- No production Gateway restart/reload.
- No production configuration mutation.
- No environment mutation.
- No Scheduled Task mutation.
- No production global extension installation/mutation.
- No production artifact replacement/deploy/rename/copy-over.
- No OpenClaw dependency patch.
- No CogentNexus source repair.
- No debugger/inspector attachment.
- No semantic/model/provider/Dashboard request.
- No TicketStore/admission/routing/auth changes.
- No production retry.
- No speculative workaround.
- No permanent instrumentation.
- No release/tag/main.
- No force-push/history rewrite.
- No historical edits to CNX-360 through CNX-400 except the minimal CNX-401 report correction explicitly authorized by this task if proven necessary.
- Do not create or start CNX-403 yourself.

Required counts:
- Semantic/model/provider/Dashboard requests: `0`
- Production mutations: `0`

## Required report

Create:

`docs/operations/coordination/reports/CNX-20260918-402-production-artifact-identity-registry-lineage-reconciliation-report.md`

Include:
- authoritative starting/final HEAD;
- exact production artifact paths and hashes;
- prior baseline artifact evidence;
- CNX-401 discrepancy analysis;
- process/PID correlation;
- both-file comparison if applicable;
- impact on CNX-401;
- direct evidence versus inference;
- correction applied, if any;
- counts and hard-fence compliance.

## Closeout

After report publication:
- set `ACTIVE.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- set `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW`;
- verify local HEAD equals remote HEAD;
- verify clean worktree;
- stop;
- do not create/start CNX-403;
- do not modify main, tags, or releases.
