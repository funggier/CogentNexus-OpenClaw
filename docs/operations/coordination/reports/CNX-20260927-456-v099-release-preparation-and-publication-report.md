# CNX-20260927-456 — v0.9.9 Release Preparation and Publication Report

Status: `PUBLISHED_MAIN_CONVERGENCE_PENDING`
Branch: `cnx-456-v0.9.9-release`
GitHub Issue: `#48`
Release: `v0.9.9`
Exact release/tag SHA: `ea3b454815378dc1d45b2db621662744ddcd9936`

## Release objective

Prepare, physically qualify, publish, and independently verify CogentNexus-OpenClaw v0.9.9 from the OpenClaw 2026.9.6-qualified CNX-455 baseline while preserving durable user state and provider/model ownership boundaries.

v0.9.9 consolidates post-v0.9.8 fixes for native Ollama terminal delivery, healthy long-running model calls, soft/hard context pressure, stale Direct settlement, supervisor lease fencing, provider/model catalog refresh, and OpenClaw 2026.9.6 restart convergence.

## Exact candidate

- exact candidate/tag SHA: `ea3b454815378dc1d45b2db621662744ddcd9936`;
- release branch: `cnx-456-v0.9.9-release`;
- candidate working tree: clean;
- branch and remote candidate were byte-identical before publication;
- no force push and no prior release/tag mutation were used.

## Local qualification

Focused release/baseline/docs/package contracts:

- `44 passed in 31.94s`;
- baseline consistency: `CogentNexus-OpenClaw v0.9.9 baseline consistency: PASS (Bridge v0.9.9)`;
- isolated gateway-readiness portability proof with an empty PATH: `6 passed in 2.01s`.

Full Python:

- `764 passed, 5 skipped, 38 subtests passed`.

Plugin/package:

- Vitest: `96 files / 448 tests PASS`;
- evaluation: PASS;
- evaluation evidence SHA-256: `c8e46942cfb280f1f3540e7dfd391fffb6074b7e31e017f50bcd3bfc8c51ab49`;
- production `npm audit --omit=dev`: `0 vulnerabilities`;
- plugin validation: PASS;
- plugin schema: 46 config properties / 5 tools;
- Ticket DB bootstrap: 9 required tables;
- packed plugin file count: 300.

## Exact-SHA GitHub qualification

All required push workflows passed on exact candidate `ea3b4548...`:

- Validate `36333858334`: SUCCESS;
- PS5.1 Acceptance Smoke `36333858304`: SUCCESS;
- Windows Installer Pack Smoke `36333858298`: SUCCESS.

The preceding candidate `dd69889d...` exposed one CI-only portability defect: the new gateway-readiness tests resolved the real OpenClaw executable before reaching the monkeypatched command runner. The production repair was retained unchanged; the test fixture was corrected to isolate executable resolution. The repaired test passes even with PATH empty.

## Physical Windows install-over and runtime qualification

Physical host baseline:

- OpenClaw `2026.9.6 (eb377ac)`;
- prior CogentNexus-OpenClaw state: PASSTHROUGH / generation 55;
- default model: `ollama/qwen3.8:27b`;
- context: `24576` / `num_ctx=24576`;
- `OLLAMA_KEEP_ALIVE=6h`;
- Gateway healthy;
- Ollama healthy;
- durable Tickets: cancelled 9 / completed 34 / failed 15 / pending outbox 0.

Before install-over, source versus installed skill contained exactly two changed files: `host_v091_legacy_v094.py` and `runtime.py`, proving the replacement was materially required.

Supported install-over from exact candidate completed with exit code 0:

- installer start: `2026-09-27T16:43:37.836Z`;
- installer completion: `2026-09-27T16:53:37.262Z`;
- existing durable Ticket DB preserved;
- skill backup created before replacement;
- exact candidate skill installed and validated;
- owned runtime/launcher restored;
- MANAGED authority committed before plugin reload;
- controller generation advanced `55 -> 56`;
- startup supervisor installed/enabled;
- no recovered Tickets;
- `postCommitRecoveryError=null`;
- transaction remained transactional.

OpenClaw 2026.9.6 restart convergence was physically requalified:

- native Gateway restart exit code: 0;
- restart duration: `134873 ms`;
- bounded restart budget: `180 s`;
- verification attempts: 1;
- Gateway `2026.9.6`, listening on `127.0.0.1:18789`, connectivity probe OK;
- Ollama healthy/already healthy.

Post-install parity/state:

- installedVersion: `0.9.9`;
- controller: active / MANAGED / generation 56;
- source skill versus installed skill: 97/97 equal, zero changed, digest `51dfc0798e2aaf90b1d1e5dc11ecfec92434c13b073b8a237b3ad853da1c6d03`;
- installed plugin package: all 300 packaged files byte-identical to source counterparts; source-only dev/test/build files are intentionally not packaged;
- default model remained `ollama/qwen3.8:27b`;
- context remained `24576`;
- `OLLAMA_KEEP_ALIVE` remained `6h`;
- durable Ticket counts remained intact with pending outbox 0.

## Release workflow

Accepted Release workflow:

- run: `36335012227`;
- event: `workflow_dispatch`;
- workflow ref: `cnx-456-v0.9.9-release`;
- run head SHA: `ea3b454815378dc1d45b2db621662744ddcd9936`;
- package job: SUCCESS;
- publish job: SUCCESS;
- overall conclusion: SUCCESS.

The release workflow reran baseline/skill/runtime/workflow/full Python/plugin/evaluation/audit/package validation, verified exact metadata, built all archives, staged validated assets, and only then created the public tag/release.

## Published release

- tag: `v0.9.9`;
- exact target: `ea3b454815378dc1d45b2db621662744ddcd9936`;
- draft: false;
- prerelease: false;
- published: `2026-09-27T16:57:50Z`.

Remote tag proof:

`ea3b454815378dc1d45b2db621662744ddcd9936  refs/tags/v0.9.9`

## Public assets and independent SHA-256 verification

All public assets were independently downloaded to:

`T:\CogentNexus\CogentNexus-OpenClaw\temp\v0.9.9-public-verify`

Recomputed SHA-256 values:

- `cogentnexus-openclaw-v0.9.9.tar.gz`: `e93d27a1c180a409a1ecd678482919582336699d0095c624835b69cd1f59966a`;
- `cogentnexus-openclaw-v0.9.9.zip`: `1a26d2305cd0ccb65d6688ebfc63535b0419caffa784d67da0f2784d52e40d1d`;
- `cogentnexus-openclaw-v0.9.9-document.zip`: `c0f7ae4a4570026b21dec8c9993e7006d8e2aa54bc2254151d6fa7f26b483c1e`;
- `SHA256SUMS.txt`: `72abd0a17e4d68458f266e3d84fddf6f40e53df5d861a7241121736c332a9637`.

The three archive hashes exactly match both the downloaded `SHA256SUMS.txt` and GitHub asset digest metadata.

## Documentation archive verification

The public documentation ZIP contains 59 entries under the single root `cogentnexus-openclaw-v0.9.9-document/`.

Independent verification:

- required current user/operator files: all present;
- `missing=[]`;
- coordination internals: `[]`;
- all entries are under the expected archive root;
- runtime state, credentials, dependency trees, and development coordination history are excluded.

## Reset / clean-reinstall disposition

No additional destructive reset or clean-reinstall cycle was required for v0.9.9.

Reason:

- v0.9.9 does not introduce a reset/clean-reinstall ownership repair;
- reset/ownership boundaries remain covered by existing regression and Windows installer CI;
- the task required physical reset/restore only as applicable;
- the changed production paths were physically exercised through same-version install-over, PASSTHROUGH -> MANAGED restoration, plugin replacement, Gateway restart convergence, and source/installed parity without losing durable state.

## Publication classification

`CNX456_V099_PUBLISHED_PUBLIC_VERIFICATION_GREEN`

The immutable v0.9.9 tag/release is complete. Post-release current-document convergence to `main` is the only remaining closeout step; the published tag/release must not be rewritten.
