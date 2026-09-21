# CNX-443 — Documentation Convergence, MIT License, and v0.9.6 Release

Status: `IN_PROGRESS`
Classification: `DOCUMENTATION / RELEASE PREPARATION / PUBLICATION`
Executor: `ChatGPT`
Reviewer: `ChatGPT independent final verification`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Parent: `CNX-442 final live Stop acceptance`

## Objective

Converge all current-facing repository documentation on the actually qualified runtime/source state, add an MIT License, prepare exact v0.9.6 release metadata and release notes, run the complete release gates, publish the GitHub Release from an exact validated candidate SHA, and verify the public tag/assets/checksums.

Historical task/report/review/release documents remain historical evidence and must not be rewritten merely to look current.

## Current facts to preserve

- CNX-442 final live Stop acceptance is GREEN.
- Production repair candidate: `8dee9cd635ca3dfcbf96f2f4161b5026355dbcf9`.
- Latest accepted live runtime: OpenClaw `2026.9.5 (ec9c1a1)`.
- Regression/dev dependency pin remains OpenClaw `2026.7.1-2` unless separately changed and requalified.
- Managed provider ownership remains Ollama; Cloud/model/auth routing remains OpenClaw-owned pass-through.
- The retired `CogentNexus coordination watch` Codex automation is not part of the current coordination workflow.
- No force push.

## Required documentation audit

Audit all tracked Markdown files. Classify them as:

1. current-facing/operator/installation/architecture guidance;
2. current coordination authority;
3. historical evidence.

Update current-facing documents that contain stale version, branch, OpenClaw compatibility, release-state, coordination/watch-mode, or provider statements. Preserve historical evidence as historical evidence and add a current-state pointer where needed rather than rewriting historical facts.

At minimum verify and converge:

- root `README.md`, `AGENTS.md`;
- `docs/CURRENT_STATE.md`, `BASELINE.md`, `INSTALL*.md`, `PROVIDERS.md`, `CHECK_SYSTEM.md`, clean-reinstall/commands/continuity guidance;
- `docs/operations/STATUS.md`, `ROADMAP.md`, `README.md`;
- current coordination documents including `ACTIVE.md`, `STATUS.md`, `README.md`, `CODEX_BOOTSTRAP.md`, `SIGNALS.md`, `WATCH_MODE.md`;
- plugin README;
- skill `SKILL.md` and current lifecycle reference/template guidance.

## MIT License

Add the standard MIT License at repository root with:

`Copyright (c) 2026 funggier`

Update README/license references where appropriate.

## v0.9.6 release metadata

The release candidate must consistently report `0.9.6` in:

- `VERSION`;
- plugin `package.json`;
- plugin `openclaw.plugin.json`;
- package lock root/package version metadata;
- release-validation CI contract;
- current operator/version surfaces and corresponding release-version tests.

Create `docs/releases/v0.9.6.md`.

Do not rewrite v095/v094 component names or historical compatibility comments merely because the public package version advances.

## Qualification gates

Before publication require:

- repository worktree clean at candidate freeze;
- `git diff --check` PASS;
- baseline/namespace/skill validation PASS;
- Python tests PASS;
- plugin build/test/evaluation/`plugin:validate` PASS;
- package/release metadata exactness PASS;
- GitHub CI/checks for the exact candidate terminal and acceptable;
- no unexpected dependency/source mutation introduced solely to force release success.

## Publication

Publish through `.github/workflows/release.yml` with:

- version: `0.9.6`;
- candidate_sha: exact frozen candidate SHA.

Verify:

- workflow success;
- tag `v0.9.6` points to exact candidate SHA;
- GitHub Release is public, non-draft, non-prerelease;
- tar.gz, zip, `SHA256SUMS.txt`, and release notes exist;
- independent checksum verification passes.

## Success classification

`CNX443_V096_DOCUMENTATION_LICENSE_RELEASE_GREEN`

only after documentation convergence, MIT licensing, exact-candidate validation, publication, and public release verification all pass.

## Local release-preparation checkpoint — 2026-09-21

Status: `LOCAL_GATES_GREEN / PRE_CANDIDATE_FREEZE`

The existing uncommitted v0.9.6 worktree was preserved throughout qualification. No `git reset`, `git checkout`, or `git restore` was used to reconstruct the release work.

Local evidence now GREEN:

- full Python suite: `708 passed, 5 skipped, 38 subtests passed`;
- namespace isolation: PASS;
- v0.9.6 baseline consistency: PASS;
- skill validation: PASS;
- Cogent/runtime/workflow self-tests: PASS;
- Python compile and repository benchmark-validator self-test: PASS;
- Windows PowerShell syntax, PowerShell 5.1 serializer, and exact root-process exit-code self-tests: PASS;
- clean plugin dependency install: PASS;
- plugin Vitest suite: `91/91` files, `428/428` tests PASS, including CNX-383;
- `npm run evaluation`: PASS with all evaluation gates true;
- `npm audit --omit=dev`: `0 vulnerabilities`;
- `npm run plugin:validate`: PASS, including mixed-plugin/schema verification, Ticket DB bootstrap, and `npm pack --dry-run` package-content verification;
- current-facing Markdown local-link audit: `28` files checked, `0` broken local links;
- `git diff --check`: PASS;
- VERSION/package/manifest/package-lock metadata all report `0.9.6`;
- OpenClaw regression/dev dependency remains `2026.7.1-2`.

The large formatting-only manifest churn in `openclaw.plugin.json` was reduced to the intended one-line semantic version change after proving that the original worktree diff had exactly one semantic JSON difference: `0.9.5 -> 0.9.6`.

One local `npm ci` attempt encountered a Windows `EBUSY` lock under generated `node_modules/openclaw`. Only the LConnect-owned npm process tree and generated plugin `node_modules` directory were cleaned. Git status entry count remained `59` before and after that cleanup. A clean managed `npm ci` then completed successfully.

### Release-topology decision

Historical v0.9.5 publication used a merged `main` SHA. The current v0.9.6 authority differs: CNX-443, the current roadmap, current status, and `.github/workflows/release.yml` require an exact validated candidate SHA but do not require a PR/main merge before publication. The release workflow checks out the supplied `candidate_sha` directly and creates the tag against that exact SHA.

Therefore no unrequired PR/merge will be introduced merely to imitate v0.9.5 history. The next authority boundary is the exact committed/pushed candidate plus its GitHub validation.

### Remaining sequence

1. publish this local qualification evidence in the CNX-443 preparation report;
2. rerun candidate-sensitive checks after the final documentation evidence changes;
3. commit the release candidate and freeze its exact SHA;
4. push without force and verify local/remote SHA equality;
5. require exact-candidate GitHub validation to finish GREEN;
6. dispatch `release.yml` for `0.9.6` with that SHA;
7. verify public tag/release/assets/checksums independently;
8. only then mark CNX-443 and coordination COMPLETE.
