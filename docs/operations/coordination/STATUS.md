# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `LIVE_WINDOWS_SUPPORTED_INSTALLER_REENTRY_AND_HEALTH_PROOF`  
**Updated:** 2026-08-30 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator requested continuation; Task 144 is independently ACCEPTed and the next irreducibly local proof is one controlled supported-installer re-entry from the preserved Task-142 partial state  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260830-145-accepted-candidate-partial-install-reentry-and-health-proof.md`](tasks/CNX-20260830-145-accepted-candidate-partial-install-reentry-and-health-proof.md)

Task ID:

`CNX-20260830-145`

## Task-144 accepted result

Report:

`docs/operations/coordination/reports/CNX-20260829-144-direct-same-path-registration-canonicality-repair.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-144-direct-same-path-registration-canonicality-repair-review.md`

Disposition: **ACCEPT**.

Accepted production implementation SHA:

`fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

Task 144 established a genuine alias-registration RED, added the minimal direct same-path lexical canonicality guard, exercised Windows junction semantics, preserved direct/managed/reparse/backup/manifest/storage/partial-state invariants, and passed exact production-SHA CI.

The outside-state alias preservation case was added afterward as a test-only descendant. No production source changed after `fb5781c1...`.

Fresh verification head `1a8834e7f5a9083ec427bab2357d1ea0a83a3020` passed:

- Validate `33265799943` — all matrix/package jobs success;
- Windows Installer Pack Smoke `33265800014` — success;
- PS5.1 Acceptance Smoke `33265799941` — success.

## Task-145 authority

Task 145 is the first live Windows action after Task-143/144 offline repair acceptance.

GitHub remote working branch is authority. Hermes/Codex must not use a stale local checkout as coordination truth. Preserve uncertain local work and use a fresh detached clone/worktree from exact accepted implementation SHA `fb5781c1...`.

Before any mutation:

- recompute candidate package/fingerprint/hash provenance;
- re-read the real Task-142-derived state without changing it;
- prove one singular canonical direct plugin registration and no root indirection/conflicting product storage;
- record plugin/controller/manifest state;
- prove Gateway/OpenClaw/Ollama/recovery/delivery/SQLite/data-history health;
- run candidate-aware production install classification and lifecycle action resolution.

Only a coherent accepted classification may proceed.

If the preflight passes, exactly **one** normal supported `scripts/install.ps1` invocation is authorized. The production classifier/action resolver decides whether the plugin is already exact or whether one bounded rollover is needed.

Installer failure means immediate stop, no retry/cleanup/manual normalization, and read-only post-failure evidence.

Success must prove exact accepted-candidate installation, refreshed/finalized ownership, normal managed operating state, healthy runtime/provider/recovery/delivery, pending `0`, SQLite `ok`, preserved durable history, singular storage, and Dashboard Send count `0`.

## Current live-state caution

The Task-142 state is historical evidence, not an assumption. Do not replay or normalize anything merely to make it match that snapshot.

## Semantic fence

Task 145 authorizes **zero Dashboard semantic Sends** and no manual semantic database/Ticket/workflow/outbox/delivery/recovery mutation.

## Prohibited

No Dashboard Send/resend; no crash/recovery injection; no reset/uninstall/clean reinstall; no manual plugin/controller/ownership-manifest normalization; no installer retry; no alternate installer; no unrelated process/service/task mutation; no reboot; no credentials/secrets; no merge/tag/GitHub Release; no force push.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260830-145-accepted-candidate-partial-install-reentry-and-health-proof.md`

Then stop for independent ChatGPT review. No lifecycle clean-uninstall/reinstall or final Dashboard acceptance is automatic.
