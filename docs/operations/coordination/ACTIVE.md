# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `OFFLINE_DIRECT_IN_PLACE_ROLLOVER_FINALIZATION_TDD_REPAIR_ONLY`
Current authorization: `CNX-20260829-143_DIRECT_IN_PLACE_ROLLOVER_FINALIZATION_REPAIR`
Task ID: `CNX-20260829-143`
Updated: 2026-08-29 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260829-143-direct-in-place-rollover-finalization-repair.md`](tasks/CNX-20260829-143-direct-in-place-rollover-finalization-repair.md)

Task 143 is an offline RED-first repair of the direct same-path rollover finalization defect proven by Task 142. It does **not** authorize any live install/install-over retry and does **not** authorize a Dashboard semantic Send.

## Task-142 disposition

Task-142 report:

`docs/operations/coordination/reports/CNX-20260829-142-accepted-candidate-install-over-retry-and-health-proof.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-142-accepted-candidate-install-over-retry-and-health-proof-review.md`

Review disposition: **ACCEPT** of the execution evidence and controlled `FAIL_INSTALL_OVER` verdict.

This is not acceptance of a successful deployment.

Task 142 proved that the supported installer replaced the canonical direct extension payload with the exact accepted candidate, then failed during rollover finalization because the replacement remained at the same canonical direct path recorded as the retired path.

Decisive failure:

```text
RuntimeError: replacement still points to the retired generation
ownership-safe plugin generation rollover finalization failed
```

## Current live-state boundary

Task 142 left the observed live state intentionally untouched after the failure:

- plugin identity singular and canonical;
- plugin payload fingerprint now equals candidate `12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0`;
- installed `namespace_ownership.py` hash equals candidate `e51f03553a24ea67037a3131b5ff4edb8aa435fbbc82b19974ae18f0d03df666`;
- plugin disabled;
- controller `passthrough`;
- existing ownership manifest preserved with its pre-attempt `installedAt`;
- Gateway/Ollama healthy in Task-142 post-failure evidence;
- recovery/delivery read-only READY, pending outbox `0`;
- SQLite integrity `ok` and semantic counts unchanged;
- Dashboard semantic Sends `0`.

Task 143 must not normalize, replay, enable, disable, reinstall, clean, reset, or otherwise mutate this live state.

## Task-143 execution contract

Task 143 must:

1. reconstruct the Task-142 direct same-path replacement sequence offline;
2. create a genuine RED through actual prepare/finalize transaction APIs before production edit;
3. prove the exact distinction between managed distinct-generation rollover and direct in-place payload replacement;
4. make the smallest finalization repair without simply deleting the path-inequality safety check;
5. allow same-path finalization only for rigorously attested canonical real direct storage with an exact old->expected fingerprint transition and exact backup/manifest/inventory evidence;
6. preserve strict managed npm generation ownership and all Task-140/141 indirection protections;
7. prove the exact Task-142 partial-state re-entry classification/action plan offline;
8. run full relevant installer/ownership/plugin/build/package validation and exact-SHA CI;
9. publish the matching report and stop for independent review.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-143-direct-in-place-rollover-finalization-repair.md`

Then stop for independent ChatGPT review.

## Hard fence

No live Windows install/install-over/update/uninstall/reset/clean-reinstall; no live runtime cleanup/normalization; no manual plugin enable/disable/delete/replace; no controller-mode mutation; no Dashboard semantic Send/resend; no Task-136/137 semantic reuse; no alternate semantic injection; no manual Ticket/workflow/outbox/ack/delivery/recovery/database mutation; no crash/recovery injection; no provider/model/OpenClaw config mutation; no unrelated process/task/service mutation; no reboot; no credentials/secrets; no merge/tag/release; no force push.
