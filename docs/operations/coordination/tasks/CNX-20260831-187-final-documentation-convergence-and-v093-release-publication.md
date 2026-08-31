# CNX-20260831-187 — Final Documentation Convergence and v0.9.3 Release Publication

Status: `READY_HERMES`

Execution mode: `FINAL_DOCUMENTATION_CONVERGENCE_AND_V093_RELEASE_PUBLICATION`

Authorization: `CNX-20260831-187_FINAL_DOCUMENTATION_AND_RELEASE_AUTHORIZED_BY_USER`

Executor: Hermes/Codex

Coordinator / final reviewer: ChatGPT

Human release authority: User — explicit authorization granted in chat on 2026-08-31 to start a new session, review/update all documentation, and continue through release publication without a second routine confirmation if all gates pass.

## Objective

Complete the final release phase for CogentNexus-OpenClaw v0.9.3:

1. fresh-audit all current/living documentation against the accepted implementation and real-Windows evidence;
2. update stale documentation where doing so does not silently change the accepted product/runtime artifact identity;
3. converge release notes, install guidance, status/roadmap/decisions, examples, naming, and compatibility claims;
4. independently prove the final publication tree still represents the accepted v0.9.3 product candidate;
5. run the required validation/release gates on the exact publication SHA;
6. choose the correct current PR/merge path based on fresh GitHub state, superseding rather than blindly reusing stale Draft PR paths;
7. merge to the intended release branch/default branch when gates are green;
8. dispatch the repository-supported Release workflow for version `0.9.3` against the exact merged publication SHA;
9. verify the resulting `v0.9.3` tag, GitHub Release, release notes, archives, and SHA256 assets;
10. publish one complete Task-187 report and stop for ChatGPT review.

## Accepted product/live baseline

Frozen product candidate:

`f6392da3e4112ce441526d5ef19925c90a872b0b`

Accepted active facade SHA-256:

`aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

Accepted plugin fingerprint:

`e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`

Accepted lifecycle/semantic sequence:

- Task 179: interactive lifecycle delegation repair accepted;
- Task 183: reset/fresh-state acceptance accepted;
- Task 184: uninstall/external-preservation acceptance accepted;
- Task 185: fresh reinstall/post-install acceptance accepted;
- Task 186: final post-lifecycle Dashboard semantic/durable-delivery acceptance accepted.

Task 186 proved:

`1 human Send → 1 Ticket → 1 session/run → 1 Ollama model call → 1 durable assistant delivery → 1 logical Dashboard assistant result`

with no duplicate semantic work, retry, direct recovery, outbox residue, or runtime-health regression.

## Starting repository authority

At Task creation, branch `agent/v0.9.3-full-stabilization` was:

`b920bb7b741f6b4f3b851c81c107b42dbff021df`

Fresh-check this value before every write or publication decision; GitHub remote state is authoritative.

Important ancestry fact already independently verified at Task creation:

`f6392da3... → b920bb7b...` is 31 commits ahead and every changed path is under `docs/operations/coordination/**`. No source/plugin/test/workflow path changed after the accepted product candidate.

Re-prove this fact from fresh remote state before publication.

## Current release state at Task creation

- repository default branch: `main`;
- latest published release: `v0.9.2`;
- `VERSION`: `0.9.3`;
- repository has `.github/workflows/release.yml` using `workflow_dispatch` inputs:
  - `version`;
  - exact `candidate_sha`;
- the Release workflow checks out the exact SHA, runs namespace/baseline/self-test/pytest/npm/evaluation/audit/plugin validation, verifies release metadata, builds `.tar.gz` and `.zip`, generates `SHA256SUMS.txt`, and publishes the GitHub Release only after those gates pass;
- open PR #24 is an older Draft path from `agent/v0.9.3-recovery-reality-tests` to `release/v0.9.2`; it must be treated as stale context and must not be merged blindly.

## Phase A — Fresh authority / release topology inspection

Before mutation:

1. fetch exact remote HEAD of `agent/v0.9.3-full-stabilization`;
2. read `ACTIVE.md`, `STATUS.md`, this Task, Task-186 report/review, `ROADMAP.md`, release workflow, current releases/tags, default branch, open PRs, and relevant branch heads;
3. verify no `v0.9.3` release/tag already exists;
4. inspect `main` and determine the correct merge/release topology;
5. inspect PR #24 and classify whether to close/supersede/leave historical;
6. freeze exact pre-documentation product-tree identity against `f6392da3...`;
7. record all current release metadata versions and expected asset names.

If a concurrent release/tag/merge already occurred, do not duplicate it; inspect and reconcile current state first.

## Phase B — Full current-documentation audit

Audit **all current/living documentation**, not only files that happen to mention v0.9.3.

At minimum include:

- root `README*` and current consumer-facing project overview;
- `docs/BASELINE.md`;
- `docs/INSTALL.md`;
- `docs/INSTALL.th.md`;
- `docs/operations/STATUS.md`;
- `docs/operations/ROADMAP.md`;
- `docs/operations/DECISIONS.md`;
- current quickstart/operations/recovery/uninstall/reset guidance;
- current architecture/ownership/namespace/provider guidance;
- `docs/releases/v0.9.3.md`;
- release workflow documentation and examples;
- current command examples (`cnxclaw.cmd`, provider behavior, reset/uninstall confirmations);
- any README/current guidance under plugin/skill directories **after classifying whether that file participates in the accepted payload/fingerprint**;
- current links, names, branch/release references, supported OpenClaw claim, and artifact names.

Historical reports, old release notes, completed coordination evidence, and explicitly historical documentation must remain historical; do not rewrite history merely to make old evidence look current.

### Required semantic alignment

Current docs must consistently describe the accepted v0.9.3 reality, including:

- project/repository name `CogentNexus-OpenClaw` and `cnxclaw` user-facing command surface;
- runtime support boundary actually proven for v0.9.3;
- OpenClaw guarantee no broader than the accepted `2026.7.1-2 (0790d9f)` evidence unless stronger evidence exists;
- v0.9.3 managed local provider behavior (Ollama selected in accepted live state; no stale LM Studio v0.9.2 instructions presented as current v0.9.3 behavior);
- provider-neutral installer responsibility where implemented/documented;
- install-over, reset, uninstall, external-preservation, and fresh reinstall behavior proven by Tasks 182–185;
- Ticket-first/durable-delivery semantics proven by Task 186;
- recovery claims must not exceed evidence;
- exact confirmation behavior for destructive commands;
- current release artifact names generated by `release.yml`.

## Phase C — Documentation mutation boundary

Documentation updates are authorized, but accepted product identity must not be changed silently.

### Safe default

Prefer changes to documentation outside runtime/plugin payload identity.

### Payload/fingerprint-sensitive documentation

Before modifying any documentation/readme inside a directory included in plugin/package/payload fingerprinting or installer provenance:

1. prove whether the file contributes to the accepted plugin/package identity;
2. if it does **not**, update normally;
3. if it **does**, do not modify it casually after live acceptance.

If a materially incorrect current document is fingerprint-sensitive and must change, classify this as a candidate/artifact-identity change. Stop release publication and report the required reacceptance scope rather than pretending the old Windows evidence applies to a different artifact.

Minor non-payload documentation fixes may advance the publication SHA while preserving product/runtime identity. Prove that with path/tree/hash comparisons.

### Product/source fence

This Task does not authorize production source, runtime code, plugin executable payload, tests, dependency, or workflow behavior changes merely to make documentation/release easier.

If the audit discovers a real product/source defect, release is BLOCKED and a new repair candidate is required.

## Phase D — Documentation validation and final publication SHA

After documentation convergence:

1. run all repository-provided documentation/link/example consistency checks that apply;
2. run baseline/namespace/version consistency checks;
3. run the repository's required validation suite appropriate for a release candidate;
4. prove every non-coordination change from `f6392da3...` to the final publication tree is documentation/release metadata only and does not change accepted runtime/plugin identity;
5. prove active facade source still hashes to the accepted value when materialized/installed source content is compared;
6. verify version alignment across `VERSION`, plugin package/manifest/lock metadata, and `docs/releases/v0.9.3.md`;
7. freeze the exact final documentation/publication commit SHA.

Do not use a moving branch name as release identity after this point.

## Phase E — PR / merge path

Use fresh GitHub evidence to select the clean current path.

Preferred shape, if repository history supports it:

`agent/v0.9.3-full-stabilization` → new current PR → `main`

Do not repurpose PR #24 if its head/base/history no longer represent the accepted full-stabilization tree.

Authorized actions when evidence supports them:

- create a replacement v0.9.3 release PR;
- update its description with accepted validation/live evidence;
- mark/close/supersede stale PR #24 as appropriate;
- wait for and inspect required CI/checks;
- merge the new release PR to `main` once all required gates are green and the merge tree preserves the accepted product identity.

No force push.

After merge, record exact `main` HEAD. This exact merged SHA becomes the preferred Release-workflow `candidate_sha` if all checks prove it is the intended publication tree.

## Phase F — Exact-SHA release workflow

Publication is explicitly authorized by the user **only if all prior gates pass**.

Dispatch `.github/workflows/release.yml` with:

```text
version = 0.9.3
candidate_sha = <exact accepted merged publication SHA>
```

The workflow itself is an authoritative release gate and must complete successfully.

Required package job evidence includes:

- exact SHA checkout;
- namespace isolation;
- baseline consistency;
- self-tests;
- pytest;
- npm tests/evaluation/audit/plugin validation;
- exact release metadata check;
- archive construction and archive-content verification;
- SHA256 generation/check.

Required publish evidence:

- `v0.9.3` did not pre-exist;
- workflow publish job succeeds;
- GitHub Release `v0.9.3` exists;
- release targets the exact intended SHA;
- title is correct;
- release notes correspond to `docs/releases/v0.9.3.md`;
- assets exist and are non-empty:
  - `cogentnexus-openclaw-v0.9.3.tar.gz`;
  - `cogentnexus-openclaw-v0.9.3.zip`;
  - `SHA256SUMS.txt`;
- published asset digests/checksums agree with workflow output;
- release is neither accidental duplicate nor wrong-target publication.

If the workflow fails, inspect the same failed run. Documentation/release-metadata-only defects may be corrected within this Task followed by fresh validation and a new exact SHA. Source/runtime/plugin/test/workflow/dependency defects block release and require a new candidate/repair task.

## Phase G — Post-release verification

After publication:

1. re-fetch `main`, tag `v0.9.3`, and release metadata;
2. verify tag/release target exact intended SHA;
3. verify all release assets and checksums;
4. verify consumer-facing install guidance points to the newly published v0.9.3 artifacts correctly;
5. verify no unintended source/product drift occurred during release preparation;
6. record final branch/main/tag/release identities and workflow run IDs;
7. update current coordination state to release-published/complete only after proof exists.

No additional Windows semantic/lifecycle acceptance is authorized unless a product/payload identity change occurred and a new task explicitly authorizes reacceptance.

## Release decision already granted

The user's current instruction constitutes the required explicit human publication authorization:

> start a new session, inspect/update all documentation, then continue and make the release.

Do not ask for a second routine confirmation before PR merge/tag/GitHub Release publication if all gates above pass.

If a material ambiguity changes what would be released, fail closed and report it instead of guessing.

## Report contract

Publish exactly one report:

`docs/operations/coordination/reports/CNX-20260831-187-final-documentation-convergence-and-v093-release-publication.md`

The report must include:

1. disposition (`PASS`, `FAIL`, `BLOCKED`, or `UNPROVEN`);
2. fresh starting authority and all relevant branch/release/PR topology;
3. complete documentation audit inventory/classification;
4. every documentation file changed and reason;
5. payload/fingerprint sensitivity analysis;
6. product-identity preservation proof from `f6392da3...` through final publication SHA;
7. validation/test/workflow evidence;
8. PR creation/supersession/merge evidence;
9. exact merged `main` SHA;
10. Release workflow dispatch inputs and run IDs;
11. package/publish job results;
12. `v0.9.3` tag/release target;
13. release asset names/sizes/SHA256 values;
14. release-note/install-guidance verification;
15. anomalies and corrections;
16. hard-fence audit;
17. final repository/main/tag/release state;
18. Reviewer Verification Packet.

After report publication, stop for ChatGPT review.

## Hard fence

Authorized:

- read-only repository/GitHub/live-evidence inspection;
- documentation-only updates subject to payload/fingerprint boundary above;
- release notes/install/status/roadmap/decisions convergence;
- repository validation/CI required to prove the exact publication SHA;
- creation of the correct current release PR;
- superseding/closing stale PR paths when evidence supports it;
- merge to `main` when all release gates pass;
- exact-SHA Release workflow dispatch for `0.9.3`;
- resulting tag/GitHub Release publication by the repository-supported workflow;
- Task-187 report publication and coordination-state updates.

Forbidden without a new repair/reacceptance task:

- production/runtime/plugin executable source changes;
- test/dependency/workflow behavior changes;
- changing accepted provider/runtime semantics;
- resetting/uninstalling/reinstalling the live machine merely for release publication;
- new Dashboard semantic acceptance turns;
- manual DB/config/runtime repair;
- force push;
- publishing a release after a material product/payload identity change without required reacceptance evidence.
