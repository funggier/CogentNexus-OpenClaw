# CNX-20260828-108 — Independent Review

Status: `COMPLETE`

Review verdict: `REJECTED — RESIDUAL FAILURE-PATH SOURCE DEFECT`

Date: 2026-08-28 ICT
Reviewer: ChatGPT
Repository: `funggier/CogentNexus-OpenClaw`
Branch: `agent/v0.9.3-full-stabilization`

## Reviewed boundary

Task:

`docs/operations/coordination/tasks/CNX-20260828-108-windows-plugin-rollover-transaction-repair.md`

Executor report:

`docs/operations/coordination/reports/CNX-20260828-108-windows-plugin-rollover-transaction-repair.md`

Report commit / current reviewed branch candidate:

`dc5e7a87867d03501b80b662e11aeaab833e0280`

Task-108 RED commit:

`686598e68a0be7b38bf983a43e72fa163796b614`

Task-108 production fix commit:

`f034cebe5cbe94116c10a81b89c2ef30de6646a8`

Comparison `f034cebe... -> dc5e7a87...` is exactly one coordination report file; there is no production/test drift between the fix and the later CI candidate.

## CI/package evidence recovered after the executor report

The executor correctly reported `BLOCKED` because two exact-source workflows were still running during its bounded wait. That temporal CI block later cleared on the report-only descendant `dc5e7a87867d03501b80b662e11aeaab833e0280`, whose production/test tree is unchanged from `f034cebe...`.

All three required workflows for `dc5e7a87...` completed successfully:

- Validate — run `33158715078` — `success`
- PS5.1 Acceptance Smoke — run `33158715084` — `success`
- Windows Installer Pack Smoke — run `33158715087` — `success`

New package proof:

- artifact ID: `9680707129`
- artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-dc5e7a87867d03501b80b662e11aeaab833e0280`
- outer artifact SHA256: `1d6a84d64bcd86e6489203d5fddfc5a0528529ce155ad4401c0a8e8174a1c0bc`
- inner ZIP SHA256: `cdb7f4a63fe64bba21f5ebc8b82f75cfe07071e0472d41b5cd9abf372bbddb2b`
- tar.gz SHA256: `a7c36b01b7e2ee6fbbcb454fc9ab612adda04450ebf8cceb4a98b33edc38f61e`
- package version: `0.9.3`
- package identity source commit: `dc5e7a87867d03501b80b662e11aeaab833e0280`
- payload file count: `178`
- payload-v2 fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- recovery harness Git blob SHA: `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`

The packaged installer contains the local archive command, `rollover-prepare`, and `rollover-finalize`, and does not contain the superseded `npm-pack:` invocation.

Therefore Task 108 is no longer blocked by CI/package availability.

## Source review finding

The main Task-107 defect is substantially repaired: Task 108 added a real pre-install ownership proof/backup boundary and a post-install replacement proof before durable ownership is switched.

However, one production failure path violates an explicit Task-108 invariant.

Task 108 required:

> A failure after the external command has mutated OpenClaw must remain fail-closed; do not falsely reassert a manifest for a generation that no longer exists.

In `finalize_plugin_rollover_transaction`, after writing the replacement manifest, a final verification exception executes an exception handler that writes `transaction["manifestBefore"]` back to the durable manifest path.

That old manifest is bound to `retiredPluginPath`. Task 107 proved that the external `openclaw plugins install ... --force` boundary can remove exactly that old generation before finalization begins. The transaction backup is stored under an external backup boundary and does not make `retiredPluginPath` live again.

Consequently, if replacement-manifest verification fails after the external mutation, the current implementation can actively restore a durable ownership manifest that points to a generation known to be allowed to no longer exist. That is the exact state Task 108 prohibited.

## Missing regression

The two new production-shaped Task-108 regressions prove:

1. successful prepare -> external old-generation removal -> replacement finalize;
2. unexpected replacement fingerprint -> reject without committing new ownership.

They do not inject a failure after the replacement manifest has been written and before/while final ownership verification completes. Therefore they do not catch the stale-manifest restoration branch described above.

Existing older rollback tests apply to the pre-Task-108 rollover model where the old project can be physically rolled back. They do not prove the new prepare/external-mutation/finalize failure semantics.

## Decision

Task 108 is **not accepted as a live-Windows candidate** despite GREEN local tests and successful CI/package proof.

The rejection is narrow: the prepare/finalize architecture is directionally correct, the npm-12/local-archive repair remains intact, and the new package is reproducibly proven. The remaining defect is the post-mutation finalization failure policy.

No real-Windows lifecycle acceptance is authorized from `dc5e7a87867d03501b80b662e11aeaab833e0280`.

## Required next work

Authorize a new source-only TDD task that must first reproduce this exact failure path:

`valid old ownership -> prepare -> external replacement/removal -> replacement manifest write -> injected final verification failure`

The required invariant is:

- the failure must remain non-zero/fail-closed;
- no manifest may be newly/re-written to assert ownership of a missing retired generation;
- no unrelated OpenClaw or user-owned state may be mutated in compensation;
- the exact replacement must not be declared successfully owned unless its final ownership proof succeeds;
- recovery evidence/transaction state must remain sufficient for a later authorized repair/retry path;
- successful prepare/finalize behavior and all previous npm12/namespace/fresh-install protections must remain GREEN.

Do not solve this merely by suppressing verification or by treating a failed verification as success.

## Safety decision

- Task 107 must not be replayed.
- Task 108 candidate/artifact is evidence only, not a live acceptance candidate.
- No install/reset/uninstall/reinstall/lifecycle/recovery is authorized yet.
- No Dashboard semantic Send is authorized.
- OpenClaw/Ollama external state remains protected.
