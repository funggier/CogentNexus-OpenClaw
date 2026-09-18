# Coordination Channel Status

Status: `READY_FOR_HERMES`
State: `CNX423_READY_FOR_HERMES`
Execution mode: `REPLY_DISPATCH_PROVENANCE_AND_ACP_IDENTITY_SEMANTICS_REPAIR`
Task ID: `CNX-20260919-423`
Parent: `CNX-20260918-422`
Executor: `Hermes / authorized repository executor`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Review: `docs/operations/coordination/reviews/CNX-20260918-422-chatgpt-review.md`
Task: `docs/operations/coordination/tasks/CNX-20260919-423-reply-dispatch-provenance-and-acp-identity-semantics-repair.md`

## Review result

CNX-422 executor classification:

`READY_FOR_CONTROLLED_OPENCLAW_2026_9_4_UPGRADE`

is **not accepted**.

Reviewer classification:

`REJECT_READY__ADMISSION_SEMANTICS_REPAIR_REQUIRED`

Blocking findings:

- privileged internal/control provenance can reach the owner-admission adapter without being excluded;
- valid OpenClaw ACP retargeting can intentionally use different source-owner and effective-dispatch session keys, but CNX-422 treats that relation as identity conflict.

## Preserved evidence

Accepted from CNX-422:

- v2026.9.4 build/plugin compatibility;
- fresh isolated startup/shutdown;
- copied-state migration characterization;
- full-state rollback proof;
- binary-only downgrade incompatibility;
- no provider/model/harness rewrite.

These do not authorize live upgrade until CNX-423 passes review.

## Safety boundary

Live OpenClaw upgrade, live migration, semantic acceptance send, release/tag/main and force-push remain prohibited.
