# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `OFFLINE_DIRECT_RETIRED_STORAGE_INDIRECTION_TDD_REPAIR_ONLY`  
**Updated:** 2026-08-29 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator requested continuation; Task 140 report was independently reviewed and requires narrow safety rework before any deployment retry  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260829-141-direct-retired-storage-indirection-safety-repair.md`](tasks/CNX-20260829-141-direct-retired-storage-indirection-safety-repair.md)

Task ID:

`CNX-20260829-141`

## Task-140 review

Task-140 report:

`docs/operations/coordination/reports/CNX-20260829-140-installer-ownership-boundary-rollover-repair.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-140-installer-ownership-boundary-rollover-repair-review.md`

Disposition: **REWORK**.

Accepted from Task 140:

- Task-139's functional ownership mismatch was correctly reproduced by RED;
- the legitimate old payload can be a real direct directory at `<openclawState>/extensions/cogentnexus-openclaw`;
- the previous prepare phase incorrectly required that path to be under the managed npm-project boundary;
- the ordinary real-direct-directory repair works in the new positive regression;
- reported targeted/full tests and exact repair-SHA CI were GREEN.

Blocking safety gap:

- Task-140's `_retired_storage_root()` compares the direct root only after resolving both the expected direct path and manifest-owned plugin path;
- `verify_manifest(..., verify_plugin=False)` proves resolved containment but does not attest that the lexical direct root itself is not a symlink/junction/reparse point;
- therefore a canonical direct path redirected to another directory still inside `.openclaw` can satisfy the new direct-root authorization after resolution;
- Task 140 added no RED/GREEN proving root-level indirection is rejected before backup mutation.

This does not invalidate Task-140's functional root-cause diagnosis. It means the repair is not yet safe enough for a live retry.

## Task-141 authorization

Task 141 is the narrow rework only.

Required sequence:

1. recreate the accepted real direct retired layout offline;
2. bind a coherent manifest to that real direct path;
3. replace the direct root with a root-level indirection to another in-state directory and prove the current Task-140 code incorrectly authorizes it;
4. prove Windows junction/reparse semantics explicitly or through a narrow Windows-attestation primitive exercised in Windows CI;
5. make the smallest lexical-root attestation repair;
6. prove the real direct directory still works;
7. prove managed npm rollover still works;
8. prove unsafe/foreign/escape/ambiguous states remain rejected;
9. run relevant Python/plugin/build validation, `git diff --check`, and exact-SHA CI;
10. publish the matching report and stop.

## Live-state caution

The repaired Dashboard source remains not proven live-installed.

Task 139's post-failure state remains intentionally untouched: controller `passthrough`, one existing plugin identity disabled, Gateway/Ollama previously healthy, historical Task-136/137 durable evidence preserved. Task 141 must not normalize or mutate that state.

## Prohibited

No live Windows install/install-over/update/uninstall/reset; no runtime cleanup/normalization; no manual plugin enable/disable/delete/replace; no controller-mode mutation; no Dashboard semantic Send/resend; no Task-136/137 semantic reuse; no alternate semantic injection; no manual Ticket/workflow/outbox/ack/delivery/recovery/database mutation; no recovery/crash injection; no provider/model/OpenClaw config mutation; no unrelated process/task/service mutation; no reboot; no credentials/secrets; no merge/tag/GitHub Release; no force push.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-141-direct-retired-storage-indirection-safety-repair.md`

Then stop for independent ChatGPT review. No deployment retry or semantic acceptance is automatic.
