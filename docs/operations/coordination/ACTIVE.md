# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `OFFLINE_DIRECT_RETIRED_STORAGE_INDIRECTION_TDD_REPAIR_ONLY`
Current authorization: `CNX-20260829-141_DIRECT_RETIRED_STORAGE_INDIRECTION_SAFETY_REPAIR`
Task ID: `CNX-20260829-141`
Updated: 2026-08-29 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260829-141-direct-retired-storage-indirection-safety-repair.md`](tasks/CNX-20260829-141-direct-retired-storage-indirection-safety-repair.md)

Task 141 is an offline RED-first safety rework of the Task-140 direct retired-storage repair. It does **not** authorize a live install-over retry and does **not** authorize any Dashboard semantic Send.

## Task-140 disposition

Task-140 report:

`docs/operations/coordination/reports/CNX-20260829-140-installer-ownership-boundary-rollover-repair.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-140-installer-ownership-boundary-rollover-repair-review.md`

Review disposition: **REWORK**.

Task 140 correctly proved the Task-139 functional root cause: the retired payload may legitimately be a real direct OpenClaw extension directory, while the old prepare phase required an isolated managed npm-project path.

Production commit under rework:

`4d47629edeb8b4e0ab23f1fabee98c05f702d141`

The blocking review finding is narrower. The new direct-root authorization occurs after `Path.resolve()`, so root-level symlink/junction/reparse identity can be lost before ownership authorization. Boundary escape outside `.openclaw` is still rejected; the unproven case is an indirection from the canonical direct path to another in-state directory.

## Live-state boundary

No live retry is authorized.

The exact Dashboard durable-capture repair lineage remains not proven live-installed. Task 139 left the controller in `passthrough` with the existing plugin disabled after its one failed install-over attempt. That state remains evidence and must not be normalized during Task 141.

## Task-141 execution contract

Task 141 must:

1. produce a deterministic RED against the current Task-140 repair for a root-level direct-path indirection;
2. prove portable symlink rejection and Windows junction/reparse rejection or an equally direct Windows root-attestation proof;
3. make the smallest repair at the lexical direct retired-root attestation boundary;
4. preserve the accepted ordinary real direct-directory topology;
5. preserve valid managed npm-project rollover;
6. preserve rejection of outside-state, arbitrary, shared-wrapper, malformed, and ambiguous ownership states;
7. run the full relevant installer/ownership/plugin/build validation and exact-SHA CI;
8. publish the matching report and stop for independent review.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-141-direct-retired-storage-indirection-safety-repair.md`

Then stop for independent ChatGPT review.

## Hard fence

No live Windows install/install-over/update/uninstall/reset; no runtime cleanup/normalization; no manual plugin enable/disable/delete/replace; no controller-mode mutation; no Dashboard semantic Send/resend; no Task-136/137 semantic reuse; no alternate semantic injection; no manual Ticket/workflow/outbox/ack/delivery/recovery/database mutation; no recovery/crash injection; no provider/model/OpenClaw config mutation; no unrelated process/task/service mutation; no reboot; no credentials/secrets; no merge/tag/release; no force push.
