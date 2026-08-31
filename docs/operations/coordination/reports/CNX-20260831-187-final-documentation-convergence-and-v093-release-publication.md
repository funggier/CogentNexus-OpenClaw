# CNX-20260831-187 — Final Documentation Convergence and v0.9.3 Release Publication

- **Task:** `CNX-20260831-187`
- **Disposition:** `BLOCKED — DOCUMENTATION_BEARING_PRODUCT_PAYLOAD_REQUALIFICATION_REQUIRED`
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Branch:** `agent/v0.9.3-full-stabilization`
- **Fresh Task-187 starting HEAD:** `3fe677b8b047eee2b893cebfc634c5073402446f`
- **Validated safe-documentation HEAD before report publication:** `5ee5089d5b666c84dae4de8db32fd3ab4051788d`
- **Frozen accepted product candidate:** `f6392da3e4112ce441526d5ef19925c90a872b0b`
- **Accepted active facade SHA-256:** `aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`
- **Accepted live installed-plugin inventory fingerprint:** `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`
- **Repository package payload-v2 fingerprint:** `df6e395a47b632c779d12dd95f9ce762c7f28ca2740442b8b299ff622df94959` (`184` files)
- **Coordinator/final reviewer:** ChatGPT
- **Human release authority:** authorization was granted, but the Task-187 artifact-identity gate failed before PR/merge/release publication.

## 1. Disposition

Task 187 is **BLOCKED** and v0.9.3 was **not merged, tagged, or published**.

The full documentation audit found stale current-facing guidance inside files that are themselves part of the installable/product artifact. Correcting those files is necessary for complete documentation convergence, but doing so would create a product/payload identity different from the exact artifact accepted on Windows in Tasks 182–186. Task 187 explicitly forbids silently transferring the old Windows acceptance to such a changed artifact.

The block is therefore intentional evidence preservation, not a CI failure. Safe repository documentation outside the installed/product payload was converged and validated successfully; the remaining correction must occur in a new narrowly scoped documentation-payload candidate/requalification cycle.

## 2. Fresh starting authority and release topology

Fresh GitHub inspection before mutation established:

```text
agent/v0.9.3-full-stabilization = 3fe677b8b047eee2b893cebfc634c5073402446f
main                           = 874dd8f8ce9c1ca5595b29207281430a86c074de
default branch                 = main
latest published release       = v0.9.2
VERSION                         = 0.9.3
v0.9.3 GitHub Release           = absent
v0.9.3 git tag/ref              = absent
```

`ACTIVE.md`, `STATUS.md`, Task 187, the Task-186 report/review, release workflow, current release state, PR topology, and current living documentation were read before release decisions.

Fresh compare from the frozen accepted candidate to Task-187 opening HEAD:

```text
f6392da3e4112ce441526d5ef19925c90a872b0b
...
3fe677b8b047eee2b893cebfc634c5073402446f

status: ahead
ahead_by: 34
behind_by: 0
merge_base: exactly f6392da3...
```

Every changed path was under `docs/operations/coordination/**`. No source/plugin/test/workflow path changed after the accepted product candidate before Task-187 documentation work.

## 3. Documentation audit inventory and classification

### Safe current/living repository documentation reviewed

- `README.md`
- `docs/BASELINE.md`
- `docs/INSTALL.md`
- `docs/INSTALL.th.md`
- `docs/CURRENT_STATE.md`
- `docs/PROVIDERS.md`
- `docs/CHECK_SYSTEM.md`
- `docs/CLEAN_REINSTALL.md`
- `docs/CLEAN_REINSTALL.th.md`
- `docs/CONTINUITY_TESTS.th.md`
- `docs/KNOWLEDGE.md`
- `docs/V093_OLLAMA_ONLY.md`
- `docs/V093_RECOVERY_REALITY_TESTS.md`
- `docs/operations/README.md`
- `docs/operations/STATUS.md`
- `docs/operations/ROADMAP.md`
- `docs/operations/DECISIONS.md`
- `docs/releases/v0.9.3.md`
- `AGENTS.md`

### Historical/current-context documentation reviewed but intentionally not rewritten as current history

- `docs/TRANSIENT_STALL_RECOVERY.md` — historical v0.9.2/LM Studio technical evidence;
- historical release notes/reports/reviews/tasks under coordination/release history;
- completed acceptance evidence for Tasks 179 and 182–186.

### Installed/payload-sensitive current guidance reviewed

- `plugins/cogentnexus-openclaw/README.md`
- `plugins/cogentnexus-openclaw/package.json`
- `plugins/cogentnexus-openclaw/openclaw.plugin.json`
- `plugins/cogentnexus-openclaw/package-lock.json`
- `skills/cogentnexus-openclaw/SKILL.md`
- sampled current skill references including:
  - `references/architecture.md`
  - `references/runtime-toolkit.md`
  - `references/recovery-controller.md`
  - `references/startup-policy.md`
  - `references/artifact-integrity.md`
  - `references/context-continuity.md`

## 4. Safe documentation files changed and reason

Task 187 changed only safe repository documentation outside the accepted installed/plugin payload:

| File | Reason |
|---|---|
| `README.md` | replace pre-acceptance/development-candidate status with accepted-candidate + publication-blocked reality |
| `docs/BASELINE.md` | preserve historical Recovery Core while adding exact current v0.9.3 acceptance/publication boundary |
| `docs/INSTALL.md` | reflect completed lifecycle acceptance, explicit-y reset/uninstall, exact candidate identity, future release assets, and provider-neutral installer responsibility |
| `docs/INSTALL.th.md` | Thai equivalent of current install/acceptance/provider-neutral installer guidance |
| `docs/CURRENT_STATE.md` | record Tasks 182–186 acceptance and the Task-187 artifact-identity blocker |
| `docs/operations/STATUS.md` | replace stale pre-freeze status with current accepted-candidate / blocked-publication state |
| `docs/operations/ROADMAP.md` | define next narrow documentation-payload requalification before final v0.9.3 publication |
| `docs/releases/v0.9.3.md` | converge release-note source with accepted Windows evidence, exact support boundary, assets, and deferred claims |

Durable recovery checkpoint:

`docs/operations/coordination/notes/CNX-20260831-187-checkpoint-01.md`

was published at commit:

`e9f26c0ca7a872834c0fba1d39da798b205baf93`

Safe convergence commit:

`05e587eea953f2d0d18b43d08a7c05b766530ad6`

Documentation-contract correction commit:

`5ee5089d5b666c84dae4de8db32fd3ab4051788d`

No production/runtime/plugin executable source, tests, dependencies, or workflows were edited.

## 5. Payload/fingerprint sensitivity analysis

### npm plugin README is fingerprint-sensitive

`plugin_payload_identity.py` delegates to `_plugin_payload()` in `namespace_ownership.py`. The payload identity hashes `package.json` plus files declared through `package.json.files`.

`plugins/cogentnexus-openclaw/package.json` explicitly declares `README.md` in `files`. Therefore:

`plugins/cogentnexus-openclaw/README.md`

is a package payload-v2 identity input and is also explicitly required inside the release archive by `.github/workflows/release.yml`.

The current README still states that the v0.9.3 candidate must pass repository stabilization/exact freeze/separate real-Windows acceptance before release promotion. Tasks 182–186 already completed and were accepted. Correcting this current-facing statement would change package bytes and therefore the payload-v2 fingerprint.

### Installed skill documentation is product-sensitive

`scripts/install.ps1` defines the source and target skill trees as:

```text
skills/cogentnexus-openclaw
-> <workspace>/skills/cogentnexus-openclaw
```

and stages/copies the installed skill surface. `SKILL.md` therefore participates in the installed runtime instruction surface even though it is not part of the npm plugin fingerprint.

Current stale examples include:

- `skills/cogentnexus-openclaw/SKILL.md`: still says the current v0.9.3 line requires exact-candidate real-machine acceptance before release promotion;
- `skills/cogentnexus-openclaw/references/architecture.md`: starts with `The current v0.9.1 architecture...` despite the current accepted line being v0.9.3.

Correcting these files changes the installed product/instruction identity. That change cannot be treated as the same accepted Windows artifact under Task 187.

## 6. Product-identity preservation proof through safe-doc HEAD

Fresh compare:

```text
f6392da3e4112ce441526d5ef19925c90a872b0b
...
5ee5089d5b666c84dae4de8db32fd3ab4051788d

status: ahead
ahead_by: 37
behind_by: 0
merge_base: exactly f6392da3...
```

All post-acceptance changes through `5ee5089...` are root/docs/coordination/release-note documentation only. No `plugins/**`, `skills/**`, production scripts, tests, dependencies, or workflow path changed after the accepted candidate.

### Active facade exact-byte proof

Task 185 resolved the accepted facade as:

```text
path: skills/cogentnexus-openclaw/scripts/cnxclaw.py
Git blob: 879083d6186589d4b2774b8fd87fa93692dd2dfc
bytes: 17425
SHA-256: aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f
```

At `5ee5089...`, the same path still resolves to the exact same Git blob `879083d6186589d4b2774b8fd87fa93692dd2dfc`. The accepted facade byte identity is therefore unchanged.

### Fingerprint-domain clarification

Two distinct plugin identity values are present in accepted evidence:

1. **Repository/package payload-v2 identity** after deterministic plugin build:
   - fingerprint: `df6e395a47b632c779d12dd95f9ce762c7f28ca2740442b8b299ff622df94959`
   - file count: `184`
2. **Live installed OpenClaw plugin inventory fingerprint** observed on Windows:
   - `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`

The `df6e395a...` value is not a Task-187 drift: exact candidate CI run `33361090584` at `f6392da3...` reported the same payload-v2 fingerprint/file count, and Task-187 safe-doc CI at `5ee5089...` reported the same values. No plugin path changed between those SHAs.

The live `e7d7d6c...` value is the installed-plugin inventory identity recorded independently during Windows acceptance. Both domains must be named explicitly rather than conflated.

## 7. Validation / test / workflow evidence

### Initial safe-doc commit anomaly

Commit `05e587ee...` triggered a documentation-contract pytest failure. The failure was not a product/runtime defect. `tests/test_install_docs_authority.py` requires the install docs to preserve the installer-vs-runtime responsibility boundary:

- exact source-install / installer-description section markers;
- Ollama must not appear in installer prerequisite `Requirements`;
- provider readiness belongs to post-install runtime checks.

Task 187 corrected only `docs/INSTALL.md` and `docs/INSTALL.th.md` at `5ee5089...`. Tests were not changed.

### Exact safe-doc HEAD CI

All push-triggered primary gates on `5ee5089d5b666c84dae4de8db32fd3ab4051788d` completed successfully:

| Workflow | Run ID | Result |
|---|---:|---|
| Validate | `33380292013` | `success` |
| Windows Installer Pack Smoke | `33380292072` | `success` |
| PS5.1 Acceptance Smoke | `33380292047` | `success` |

Validate included successful package dry-run plus the full Ubuntu/macOS/Windows Python matrix, namespace/baseline checks, self-tests, pytest, benchmark validator, installer syntax/smokes as applicable, npm test/evaluation/audit, and plugin validation.

Package dry-run proof for `5ee5089...`:

```text
package version: 0.9.3
payload-v2 fingerprint: df6e395a47b632c779d12dd95f9ce762c7f28ca2740442b8b299ff622df94959
payload file count: 184
cogentnexus-openclaw-v0.9.3.tar.gz SHA-256: 57659678c64f95b3375fa1b63a65503b62b410c79652e82a92cef44a70284032
cogentnexus-openclaw-v0.9.3.zip SHA-256: dffa80f4f760a5d939cab6f7c44324ba8d264287e7082c51fadaaa789df55e33
```

Package-proof artifact:

```text
artifact id: 9753484915
name: cogentnexus-openclaw-v0.9.3-package-proof-5ee5089d5b666c84dae4de8db32fd3ab4051788d
artifact ZIP size: 5,235,308 bytes
artifact digest: sha256:61333738283b6851edee2cc3afa4ba181b36d16623a7cfe6856a2d5da8d06a9a
```

These are **dry-run validation artifacts**, not published GitHub Release assets.

## 8. PR creation / supersession / merge evidence

PR #24 was freshly classified as stale:

```text
PR: #24
state before Task-187 action: open Draft
head: agent/v0.9.3-recovery-reality-tests
head SHA: 1fa60009e71433a028657835b5953084df4e4753
base: release/v0.9.2
base SHA: 986f3c7be8389866f3ffe4f9b372ff1264ddbe8e
commits: 677
changed files: 625
```

Task 187 added an explicit supersession comment and closed PR #24 without merging it. Final PR #24 state:

```text
state: closed
merged: false
closed_at: 2026-08-31T09:55:42Z
```

No replacement v0.9.3 release PR to `main` was created because the artifact-identity blocker occurred before the PR/merge gate. Creating a release PR for a knowingly incomplete documentation-bearing artifact would have been misleading.

## 9. Exact merged main SHA

Not applicable: Task 187 did not merge.

`main` remained:

`874dd8f8ce9c1ca5595b29207281430a86c074de`

through the final pre-report verification.

## 10. Release workflow dispatch

**NOT DISPATCHED.**

The authorized intended inputs would have been:

```text
version = 0.9.3
candidate_sha = <exact accepted merged main SHA>
```

but no accepted merged publication SHA exists because the artifact-identity gate failed before PR/merge.

## 11. Package / publish job result

- repository `Validate` package dry-run: `PASS` on `5ee5089...`;
- `.github/workflows/release.yml` package job: **NOT RUN**;
- `.github/workflows/release.yml` publish job: **NOT RUN**.

The dry-run proves the current safe-doc tree is mechanically packageable. It does not override the product-identity block.

## 12. v0.9.3 tag / GitHub Release target

No `v0.9.3` tag/ref exists. No `v0.9.3` GitHub Release exists. No target SHA exists because publication was not attempted.

## 13. Release asset names / sizes / SHA256

No published release assets exist under v0.9.3.

Expected eventual names remain:

- `cogentnexus-openclaw-v0.9.3.tar.gz`
- `cogentnexus-openclaw-v0.9.3.zip`
- `SHA256SUMS.txt`

The dry-run archive SHA-256 values listed in section 7 belong to `5ee5089...` only and must not be represented as published assets. A corrected payload-sensitive candidate will produce different package/archive identity and requires its own exact proof.

## 14. Release-note / install-guidance verification

Safe current documentation now states the truthful boundary:

- exact `f6392da3...` candidate passed Tasks 182–186;
- validated OpenClaw guarantee is no broader than `2026.7.1-2 (0790d9f)`;
- v0.9.3 managed provider is Ollama only;
- installer prerequisites remain provider-neutral;
- reset/uninstall require explicit `y` and preserve external OpenClaw/Ollama/user data according to accepted evidence;
- final Dashboard semantic/durable-delivery path has been accepted for the frozen artifact;
- no public v0.9.3 release currently exists;
- release workflow eventual asset names are correct.

Full convergence is incomplete only because stale plugin/skill guidance cannot be corrected without changing accepted product/payload identity.

## 15. Anomalies and corrections

### A. Safe install-doc rewrite initially violated documentation authority contract

- **Observed:** pytest failed after `05e587ee...` because section boundaries and provider-neutral prerequisites no longer matched the documented/tested installer responsibility contract.
- **Classification:** Task-187 documentation defect, not product defect.
- **Correction:** commit `5ee5089...` changed only INSTALL EN/TH; tests were left unchanged.
- **Final evidence:** all three primary CI workflows passed.

### B. Apparent `df6e...` vs `e7d...` fingerprint mismatch

- **Observed:** package dry-run reported `df6e395a...`; live acceptance records `e7d7d6c...`.
- **Investigation:** exact candidate CI at `f6392da3...` also reported `df6e395a...` / 184 files, while Windows install reports independently recorded `e7d7d6c...` as the installed plugin inventory fingerprint.
- **Classification:** distinct identity domains, not post-acceptance plugin drift.
- **Consequence:** report names both domains explicitly.

### C. Stale product documentation discovered only after sensitivity classification

- **Observed:** plugin README and installed skill docs contain pre-acceptance/current-version wording.
- **Classification:** material release blocker because the files are product/payload surfaces.
- **Correction in Task 187:** deliberately **not performed**; changing them would invalidate exact-artifact acceptance without requalification.

## 16. Hard-fence audit

```text
production/runtime/plugin executable source edits: 0
test edits: 0
dependency edits: 0
workflow behavior edits: 0
live reset/uninstall/install/reinstall/install-over: 0
new Dashboard semantic turns: 0
manual DB/config/runtime repair: 0
force push: 0
stale PR #24 merge: 0
replacement release PR: 0 (blocked before gate)
main merge: 0
Release workflow dispatch: 0
tag creation: 0
GitHub Release publication: 0
```

Only safe documentation/coordination changes and stale-PR supersession were performed.

## 17. Final repository / main / tag / release state before report publication

```text
working branch safe-doc HEAD: 5ee5089d5b666c84dae4de8db32fd3ab4051788d
main:                         874dd8f8ce9c1ca5595b29207281430a86c074de
PR #24:                       closed, not merged
v0.9.3 tag:                   absent
v0.9.3 GitHub Release:        absent
release workflow dispatch:    none
Task-187 result:              BLOCKED
```

The final report/coordination publication commit will add only coordination/report state on top of this validated safe-doc HEAD; it must not change product/payload/runtime/test/workflow identity.

## 18. Required successor boundary

A new explicit documentation-payload repair/requalification task is required before v0.9.3 publication. Its minimum safe shape is:

1. correct stale current-facing text in `plugins/cogentnexus-openclaw/README.md`, `skills/cogentnexus-openclaw/SKILL.md`, stale installed references such as `references/architecture.md`, and any additional installed/payload current-doc findings;
2. do not change production/runtime/plugin executable source, tests, dependencies, or workflow behavior unless a separately authorized product defect is discovered;
3. freeze the new exact commit and compute the new package payload-v2 fingerprint/file count plus installed skill-tree identity;
4. prove executable/runtime source bytes, including facade `cnxclaw.py`, remain unchanged from `f6392da3...` where intended;
5. rerun repository/package validation on the exact new candidate;
6. perform Windows requalification proportional to the changed product surface: exact install-over/provenance of the corrected artifact, health/fingerprint/skill-byte checks, and one bounded Dashboard semantic/durable-delivery turn because the installed instruction surface changed; repeat reset/uninstall/fresh-reinstall only if evidence from the changed candidate requires those lifecycle boundaries to be re-proven;
7. after acceptance, return to a current PR -> `main` path, exact merged-SHA freeze, `.github/workflows/release.yml` dispatch, tag/release/assets/checksum verification.

## Reviewer Verification Packet

1. Re-fetch `agent/v0.9.3-full-stabilization` and verify Task-187 report publication is documentation/coordination-only on top of `5ee5089...`.
2. Compare `f6392da3...` to the final Task-187 publication HEAD and confirm no post-acceptance `plugins/**`, `skills/**`, product source, test, dependency, or workflow changes were introduced by Task 187.
3. Verify `skills/cogentnexus-openclaw/scripts/cnxclaw.py` still has Git blob `879083d6186589d4b2774b8fd87fa93692dd2dfc`, corresponding to accepted SHA-256 `aa747f8f...`.
4. Verify exact candidate package dry-run `33361090584` and safe-doc dry-run `33380292013` both report payload-v2 `df6e395a...` / 184 files.
5. Verify Tasks 182–186 retain live installed plugin fingerprint `e7d7d6c...`, OpenClaw `2026.7.1-2`, and accepted lifecycle/semantic evidence.
6. Verify `plugins/cogentnexus-openclaw/package.json.files` includes `README.md`, and current plugin README still contains pre-acceptance wording.
7. Verify installer skill source/target boundary and stale `SKILL.md` / `references/architecture.md` wording.
8. Verify exact safe-doc CI run IDs `33380292013`, `33380292072`, `33380292047` all concluded `success`.
9. Verify PR #24 is closed and not merged, with old head/base unchanged.
10. Verify `main` remains `874dd8f8...`, `v0.9.3` tag/release remain absent, and no Release workflow was dispatched.

## Final conclusion

Task 187 successfully completed the safe portion of documentation convergence, preserved exact accepted product/runtime identity, validated the safe documentation tree, and retired the stale PR path. It correctly **did not publish v0.9.3** because completing the remaining current documentation would alter documentation-bearing product/payload bytes that were part of the accepted artifact.

Disposition: `BLOCKED — DOCUMENTATION_BEARING_PRODUCT_PAYLOAD_REQUALIFICATION_REQUIRED`.

Stop here for ChatGPT review.
