# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_ACCEPTANCE`
Current authorization: `CNX-20260828-116_V093_REAL_WINDOWS_LIFECYCLE_ACCEPTANCE_FINAL_CANDIDATE`
Task ID: `CNX-20260828-116`
Updated: 2026-08-28 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260828-116-v093-real-windows-lifecycle-acceptance-final-candidate.md`](tasks/CNX-20260828-116-v093-real-windows-lifecycle-acceptance-final-candidate.md)

Task 116 is the **read-only-first real-Windows lifecycle acceptance** for the exact independently reviewed v0.9.3 candidate.

## Frozen candidate

- Source: `47b069daed90f54feae2c9eb26f38c438493f3c8`
- Artifact: `9687249771`
- Outer SHA256: `c009450560176ce89c8a5a6ef65aec5ce9f821e75053617d56de212cf6093fdf`
- Inner ZIP SHA256: `8771869962babe591c6ba4431b8f4737b716f2258cfcfc6fd45eec4f582b2fc5`
- tar.gz SHA256: `057cc016becd91ba4baf49a3c59152ce9ff467ff0a30b758e8e460e43f6ee2c5`
- Payload count: `178`
- Payload fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- Recovery harness blob: `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`

## Task 115 closure

Report:

`docs/operations/coordination/reports/CNX-20260828-115-interrupted-reentry-semantic-matrix-hardening.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-115-interrupted-reentry-semantic-matrix-hardening-review.md`

Review verdict:

`ACCEPTED PASS — SEMANTIC MATRIX COMPLETE; EXACT CANDIDATE MAY ADVANCE TO A SEPARATE READ-ONLY-FIRST REAL-WINDOWS LIFECYCLE TASK`

## Required Task-116 sequence

`fresh provenance -> fresh read-only machine reconciliation/classification -> preserve external evidence -> install-over once -> reset y once -> uninstall y once -> fresh reinstall same artifact once -> stop/start/restart once each -> recovery reality harness once -> final read-only snapshot -> report -> independent review`

Mutation is forbidden until Phase 0 proves current live state coherent. Stop on first non-zero/ambiguity; do not replay or manually normalize.

## Preserved external dependencies

- OpenClaw must remain exactly `2026.7.1-2`.
- Ollama remains the selected provider and must not be updated/reinstalled/reconfigured.
- No provider/model changes.
- No credentials/secrets access or re-entry.

## Dashboard fence

No Dashboard semantic nonce/message/Send is authorized in Task 116. That remains a separate final acceptance task after lifecycle success.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-116-v093-real-windows-lifecycle-acceptance-final-candidate.md`

Then stop for independent ChatGPT review. Do not create or execute the final Dashboard semantic-delivery task.
