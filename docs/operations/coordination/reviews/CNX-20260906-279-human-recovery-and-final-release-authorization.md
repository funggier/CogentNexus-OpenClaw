# CNX-20260906-279 — Human Recovery and Conditional Final Release Authorization

## Human direction

On 2026-09-06 ICT, the human owner explicitly stated:

- `ถ้าต้องติดตั้งใหม่ก้ทำไดเลยนะครับ`
- `ถ้าทุกอย่างเรียบร้อยแล้วผมอยากให้ทำ release เป็นอันจบงานครับ`

## Task279 recovery authority

The preferred recovery remains the smallest supported action: prove the current exact candidate/ownership/PASSTHROUGH predicates, then invoke the canonical `cnxclaw.cmd enable` path once.

If read-only evidence proves that canonical enable alone is not a valid/sufficient recovery from the Task278 partial-install state, or if one supported enable attempt fails and leaves a coherent state for supported replacement, the human authorizes one supported reinstall/install-over of the same accepted candidate:

`36cd4c800ded28bdb7165fcad6e0bfb48b4e933b`

This fallback must be root-cause driven and may not be used merely because reinstall is available.

The reinstall authority does not imply a clean uninstall, reset, broad cleanup, manual plugin mutation, manual SQLite mutation, semantic send, session Delete/reset, Ticket/recovery disposition, release promotion, or force push.

## Conditional final release authority

The human owner also directs that once the stabilization work is fully accepted, release should be the final step of the work without asking again whether a release is desired.

This is conditional authority only. No release may occur until ChatGPT independently verifies all applicable final gates, including at minimum:

1. accepted source/test/CI candidate and repository state;
2. live CogentNexus-OpenClaw MANAGED activation and runtime health;
3. required Task272 session Delete/recreation / first-turn durable-delivery acceptance;
4. no unresolved blocker that invalidates release readiness;
5. exact release version/tag/artifact provenance resolved from the repository's existing release plan and current authoritative state;
6. release artifacts/checks are bound to the exact accepted release candidate.

When all final gates pass, ChatGPT may open/authorize the bounded final release task and Hermes may execute the repository's supported release path as the closing action. Do not infer permission to invent a version/tag, bypass release checks, force-push, or promote an unreviewed candidate.

## Standing protected state

The protected old Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` remains excluded from generic mutation unless separately and explicitly authorized. Task272 semantic test messages remain human-origin where the acceptance contract requires that evidence.
