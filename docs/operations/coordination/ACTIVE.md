# Active Coordination Task

Status: `READY_HERMES`
Execution mode: `FINAL_DOCUMENTATION_CONVERGENCE_AND_V093_RELEASE_PUBLICATION`
Current authorization: `CNX-20260831-187_FINAL_DOCUMENTATION_AND_RELEASE_AUTHORIZED_BY_USER`
Task ID: `CNX-20260831-187`
Updated: 2026-08-31 ICT
Executor: Hermes/Codex
Coordinator / final reviewer: ChatGPT
Human release authority: User — explicit publication authorization granted

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative.

## Active task

[`tasks/CNX-20260831-187-final-documentation-convergence-and-v093-release-publication.md`](tasks/CNX-20260831-187-final-documentation-convergence-and-v093-release-publication.md)

## Accepted product/live baseline

Frozen product candidate:

`f6392da3e4112ce441526d5ef19925c90a872b0b`

Required active facade SHA-256:

`aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

Accepted plugin fingerprint:

`e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`

Accepted sequence:

- Task 179: interactive lifecycle repair accepted;
- Task 183: reset accepted;
- Task 184: uninstall/external preservation accepted;
- Task 185: fresh reinstall accepted;
- Task 186: final Dashboard semantic/durable-delivery accepted.

Task 186 proved the final designed path after reset → uninstall → fresh reinstall:

`1 human Send → 1 Ticket → 1 session/run → 1 Ollama model call → 1 durable assistant delivery → 1 logical Dashboard assistant result`

with no duplicate semantic work, retry, recovery, outbox residue, or runtime-health regression.

## Product identity after acceptance

At Task-187 opening, remote branch HEAD before activation was:

`b920bb7b741f6b4f3b851c81c107b42dbff021df`

Fresh comparison from `f6392da3...` to that HEAD showed 31 commits and **all changed paths were under `docs/operations/coordination/**`**. No source/plugin/test/workflow path changed after the accepted product candidate.

Re-prove this from fresh remote state during Task 187 and preserve product identity across documentation convergence.

## Task-187 authorization

The user explicitly instructed that the next/new session should:

1. inspect and update all current documentation;
2. converge release notes/install/current operational guidance;
3. continue through the v0.9.3 release without another routine confirmation if all gates pass.

Task 187 therefore authorizes documentation-only convergence, current release PR/merge handling, and exact-SHA GitHub Release publication according to the task contract.

The repository-supported `.github/workflows/release.yml` is the preferred publication gate. It accepts `version=0.9.3` and an exact `candidate_sha`, reruns release validation, builds archives/SHA256, and publishes only after successful gates.

## Release topology caution

At Task opening:

- default branch: `main`;
- latest published release: `v0.9.2`;
- `VERSION`: `0.9.3`;
- open PR #24 is an older Draft from `agent/v0.9.3-recovery-reality-tests` to `release/v0.9.2` and must not be merged blindly.

Use fresh GitHub state to choose/create the correct current v0.9.3 merge path, preferably a current full-stabilization → main PR if history supports it.

## Documentation / artifact boundary

Audit all current/living docs, but do not silently invalidate accepted artifact identity.

If a documentation file participates in the plugin/package/payload fingerprint, prove that before editing it. A material fingerprint-sensitive change blocks release until required candidate/reacceptance work is explicitly handled.

Production/runtime/plugin executable source, tests, dependency behavior, and workflow behavior are not authorized to change under this Task merely to facilitate release.

## Publication gate

If documentation convergence, exact product-identity proof, CI, PR/merge, and exact-SHA release validation all pass, the user has already authorized:

- merge to the intended release/default branch;
- Release workflow dispatch with `version=0.9.3` and the exact merged publication SHA;
- creation of tag/release `v0.9.3` and its validated assets by the repository workflow.

Do not ask for a second routine publication confirmation.

If any material ambiguity changes what product/artifact would be released, fail closed and report rather than guessing.

## Hard fence

Authorized:

- documentation-only updates subject to payload/fingerprint classification;
- validation/CI;
- current release PR creation and stale-PR supersession as supported by evidence;
- merge when gates are green;
- exact-SHA `v0.9.3` Release-workflow publication;
- Task-187 report and coordination updates.

Forbidden without a new repair/reacceptance task:

- production/runtime/plugin executable source changes;
- test/dependency/workflow behavior changes;
- live reset/uninstall/reinstall/install-over for release convenience;
- new Dashboard semantic acceptance turns;
- manual DB/config/runtime repair;
- force push;
- release publication after an unaccepted material product/payload identity change.

After Task-187 report publication, stop for ChatGPT review.
