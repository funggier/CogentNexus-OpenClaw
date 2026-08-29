# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `OFFLINE_INSTALLER_OWNERSHIP_BOUNDARY_TDD_REPAIR_ONLY`
Current authorization: `CNX-20260829-140_INSTALLER_OWNERSHIP_BOUNDARY_ROLLOVER_REPAIR`
Task ID: `CNX-20260829-140`
Updated: 2026-08-29 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260829-140-installer-ownership-boundary-rollover-repair.md`](tasks/CNX-20260829-140-installer-ownership-boundary-rollover-repair.md)

Task 140 is an offline RED-first TDD diagnosis/repair of the ownership-safe plugin generation-rollover failure observed by Task 139. It does **not** authorize a live install-over retry and does **not** authorize any Dashboard semantic Send.

## Task-139 disposition

Task-139 report:

`docs/operations/coordination/reports/CNX-20260829-139-repaired-candidate-install-over-and-health-proof.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-139-repaired-candidate-install-over-and-health-proof-review.md`

Review disposition: **ACCEPT** of the execution evidence and controlled `FAIL_INSTALL_OVER` classification.

This is not acceptance of a successful install.

The exact repaired Dashboard candidate remains:

`16f5c396e9be0af8d1bd34824fe2993613501a6f`

It remains **not deployed** to the effective installed runtime.

Task 139 built/validated/packaged that exact candidate and performed the one authorized supported install-over. The installer entered native handoff, then failed closed before plugin replacement because ownership-safe generation rollover could not prove the installed plugin path under the expected managed npm projects boundary.

Observed error:

```text
RuntimeError: plugin is not inside the managed npm projects boundary:
C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw
ownership-safe plugin generation rollover pre-install proof failed
```

The old installed plugin fingerprint remained:

`3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`

Post-failure live state recorded by Task 139 is intentionally left untouched: controller `passthrough`, one plugin identity disabled, Gateway/Ollama healthy, recovery/delivery read-only checks READY, SQLite integrity `ok`, pending outbox `0`, and historical Task-136/137 evidence preserved.

## Task-140 execution contract

Task 140 must:

1. reconstruct the exact Task-139 installer ownership/caller/path contract offline;
2. distinguish path/layout/normalization/link/generation causes rather than infer one from the error string;
3. add a deterministic genuine RED reproducing the factual Task-139 failure before any production edit;
4. prove the exact source-level root cause;
5. make the smallest safe repair at the owning boundary;
6. preserve rejection of unmanaged paths, boundary escapes, and unsafe symlink/junction ownership claims;
7. run the complete relevant ownership/rollover/installer/package/build validation surface and exact-repair-SHA CI where required;
8. publish the matching report and stop for independent review.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260829-140-installer-ownership-boundary-rollover-repair.md`

Then stop for independent ChatGPT review.

A Task-140 PASS does not automatically authorize a new install-over attempt. A separate deployment-proof task is required after review.

## Hard fence

No live Windows install/install-over/update/uninstall/reset; no runtime cleanup/normalization; no manual plugin enable/disable/delete/replace; no controller-mode mutation; no Dashboard semantic Send/resend; no Task-136/137 semantic reuse; no alternate semantic injection; no manual Ticket/workflow/outbox/ack/delivery/recovery/database mutation; no recovery/crash injection; no provider/model/OpenClaw config mutation; no unrelated process/task/service mutation; no reboot; no credentials/secrets; no merge/tag/release; no force push.
