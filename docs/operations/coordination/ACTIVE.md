# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_SUPPORTED_INSTALLER_REENTRY_AND_HEALTH_PROOF`
Current authorization: `CNX-20260830-145_ACCEPTED_CANDIDATE_PARTIAL_INSTALL_REENTRY_AND_HEALTH_PROOF`
Task ID: `CNX-20260830-145`
Updated: 2026-08-30 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

GitHub remote branch `agent/v0.9.3-full-stabilization` is authoritative. A stale local checkout must not be used as coordination truth.

## Active task

[`tasks/CNX-20260830-145-accepted-candidate-partial-install-reentry-and-health-proof.md`](tasks/CNX-20260830-145-accepted-candidate-partial-install-reentry-and-health-proof.md)

Task 145 is a narrow real-Windows proof that the supported installer can safely re-enter the intentionally preserved Task-142 partial install state after the accepted Task-143/144 offline repairs.

## Task-144 disposition

Task-144 report:

`docs/operations/coordination/reports/CNX-20260829-144-direct-same-path-registration-canonicality-repair.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-144-direct-same-path-registration-canonicality-repair-review.md`

Review disposition: **ACCEPT**.

Accepted implementation/deployment source:

`fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

The later report/test/task-document descendants do not redefine the production candidate.

## Verification basis

Production SHA `fb5781c1...` passed:

- Validate `33264956365`
- Windows Installer Pack Smoke `33264956369`
- PS5.1 Acceptance Smoke `33264956375`

Review-added outside-state alias coverage was added without production changes and a fresh descendant verification head `1a8834e7f5a9083ec427bab2357d1ea0a83a3020` passed:

- Validate `33265799943`
- Windows Installer Pack Smoke `33265800014`
- PS5.1 Acceptance Smoke `33265799941`

## Preserved live-state boundary

Task 142 last observed a partial but healthy state:

- one canonical direct plugin identity;
- plugin disabled;
- controller `passthrough`;
- candidate payload already present from the failed Task-142 attempt;
- pre-attempt ownership manifest still present;
- Gateway/Ollama healthy;
- recovery/delivery READY, pending `0`;
- SQLite `ok`;
- semantic history preserved;
- Dashboard semantic Send count `0`.

Task 145 must **re-verify all material live state read-only**. Do not assume the old snapshot still holds and do not normalize drift manually.

## Task-145 execution contract

Before mutation, Hermes/Codex must:

1. fetch the remote working branch and verify this exact Task 145 is still active and unsuperseded;
2. preserve any uncertain local checkout and use a fresh detached clone/worktree of exact implementation SHA `fb5781c1abd68280760bd5b3b4a65fabd8a60e58`;
3. recompute package/fingerprint/hash provenance from that exact source;
4. capture the complete live read-only drift/ownership/runtime/data-health boundary;
5. prove raw plugin `rootDir` is lexically canonical and the direct root is real/non-reparse;
6. run the production candidate-aware `classify-install` and lifecycle action resolver before mutation;
7. stop `BLOCKED` before mutation for partial/mixed/ambiguous/noncanonical/conflicting/unexplained state.

If the gate passes, execute **exactly one** normal supported `scripts/install.ps1` invocation. Let the production classifier/action resolver decide whether the plugin is already exact or requires one bounded rollover. Do not hard-code or manually force either path.

If the installer fails, stop immediately with read-only evidence. No retry or cleanup.

If it succeeds, prove exact candidate provenance, ownership finalization, normal managed controller/plugin/runtime health, preserved durable data, no conflicting storage/stale rollover, pending `0`, and Dashboard Sends `0`.

## Required completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260830-145-accepted-candidate-partial-install-reentry-and-health-proof.md`

Then stop for independent ChatGPT review.

## Hard fence

No Dashboard semantic Send/resend; no manual Ticket/workflow/outbox/delivery/recovery/database mutation; no crash/recovery injection; no reset/uninstall/clean reinstall; no manual plugin copy/delete/replace/enable/disable outside the supported installer; no manual controller or ownership-manifest normalization; no retry after installer failure; no alternate installer; no unrelated process/service/task mutation; no reboot; no credentials/secrets; no merge/tag/release; no force push.
