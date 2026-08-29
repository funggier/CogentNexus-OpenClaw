# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `OFFLINE_DIRECT_REGISTRATION_CANONICALITY_TDD_REPAIR_ONLY`  
**Updated:** 2026-08-29 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator requested continuation; Task 143 report was independently reviewed and requires one narrow canonical-registration rework before any live completion retry  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260829-144-direct-same-path-registration-canonicality-repair.md`](tasks/CNX-20260829-144-direct-same-path-registration-canonicality-repair.md)

Task ID:

`CNX-20260829-144`

## Task-143 review

Task-143 report:

`docs/operations/coordination/reports/CNX-20260829-143-direct-in-place-rollover-finalization-repair.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-143-direct-in-place-rollover-finalization-repair-review.md`

Disposition: **REWORK**.

Accepted facts:

- Task 143 reproduced the Task-142 direct same-path failure with genuine RED before production edit;
- the functional repair correctly distinguishes direct in-place generation change from managed distinct-generation storage for covered cases;
- canonical direct A -> B success, managed same-path rejection, fingerprint transition, backup proof, manifest drift, direct-root reparse rejection, conflicting storage rejection, and partial-state re-entry were tested;
- exact repair SHA `59952167f51657ae2ff900a28aae528f835f9b6e` completed Validate, Windows Installer Pack Smoke, and PS5.1 Acceptance Smoke successfully.

Blocking gap:

- raw OpenClaw `plugins[].rootDir` is resolved by `_active_registered_plugin()`;
- the finalizer does not require the raw lexical registration path itself to equal the canonical direct root before same-path authority;
- an alias/symlink/junction registration path resolving to the real canonical direct root can therefore lose its lexical noncanonical identity;
- current tests do not cover that case even though Task 143 required singular **canonical** active registration.

## Task-144 authorization

Task 144 is offline-only.

Required sequence:

1. prepare the accepted canonical direct A -> B transition offline;
2. keep the canonical direct root real and non-reparse;
3. point singular inventory `rootDir` at a distinct alias path resolving to the direct root;
4. prove current Task-143 repair incorrectly authorizes or fails to reject that registration;
5. add Windows junction/reparse alias proof;
6. minimally require canonical lexical registration for direct same-path authority;
7. preserve all Task-143 positive/negative ownership invariants and Task-142 partial-state classification;
8. run full relevant test/build/plugin/package validation and exact-SHA CI;
9. publish the matching report and stop.

## Live-state caution

The user's live machine remains in Task-142's observed partial state with the candidate payload already present but plugin disabled and controller `passthrough`. Do not replay the installer or normalize that state during Task 144.

## Semantic fence

Task 144 authorizes **zero Dashboard semantic Sends** and zero live runtime/database/ownership mutation.

## Prohibited

No live Windows install/install-over/update/uninstall/reset/clean-reinstall; no live cleanup/normalization; no manual plugin enable/disable/delete/replace; no controller-mode mutation; no ownership-manifest mutation; no Dashboard semantic Send/resend; no Task-136/137 semantic reuse; no alternate semantic injection; no manual Ticket/workflow/outbox/ack/delivery/recovery/database mutation; no crash/recovery injection; no provider/model/OpenClaw config mutation; no unrelated process/task/service mutation; no reboot; no credentials/secrets; no merge/tag/GitHub Release; no force push.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-144-direct-same-path-registration-canonicality-repair.md`

Then stop for independent ChatGPT review. No live recovery/install completion or Dashboard semantic acceptance is automatic.
