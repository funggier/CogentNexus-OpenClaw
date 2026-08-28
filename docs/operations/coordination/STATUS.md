# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `LIVE_WINDOWS_ACCEPTANCE`  
**Updated:** 2026-08-28 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator authorized continued stabilization; Task 116 authorizes the exact read-only-first live lifecycle sequence defined in its task file  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260828-116-v093-real-windows-lifecycle-acceptance-final-candidate.md`](tasks/CNX-20260828-116-v093-real-windows-lifecycle-acceptance-final-candidate.md)

Task ID:

`CNX-20260828-116`

## Repository/source gate accepted

Task-115 report:

`docs/operations/coordination/reports/CNX-20260828-115-interrupted-reentry-semantic-matrix-hardening.md`

Task-115 independent review:

`docs/operations/coordination/reviews/CNX-20260828-115-interrupted-reentry-semantic-matrix-hardening-review.md`

Verdict:

`ACCEPTED PASS — SEMANTIC MATRIX COMPLETE; EXACT CANDIDATE MAY ADVANCE TO A SEPARATE READ-ONLY-FIRST REAL-WINDOWS LIFECYCLE TASK`

## Frozen Task-116 candidate

- source `47b069daed90f54feae2c9eb26f38c438493f3c8`;
- artifact `9687249771`;
- artifact outer SHA256 `c009450560176ce89c8a5a6ef65aec5ce9f821e75053617d56de212cf6093fdf`;
- inner ZIP SHA256 `8771869962babe591c6ba4431b8f4737b716f2258cfcfc6fd45eec4f582b2fc5`;
- tar.gz SHA256 `057cc016becd91ba4baf49a3c59152ce9ff467ff0a30b758e8e460e43f6ee2c5`;
- version `0.9.3`;
- payload count `178`;
- payload fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- recovery harness Git blob `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`.

Exact same-source CI on the frozen candidate:

- Validate `33175145162` success;
- Windows Installer Pack Smoke `33175145179` success;
- PS5.1 Acceptance Smoke `33175145178` success.

## Authorized live sequence

Task 116 is explicitly read-only first:

1. fresh GitHub/source/artifact provenance;
2. external evidence root;
3. read-only current Windows/OpenClaw/Ollama/CNX/Gateway/provider/recovery/delivery/resources/SQLite/Supervisor capture;
4. read-only ownership/product inventory and exact `classify-install` using real OpenClaw plugin inventory;
5. **only if coherent**, preserve pre-mutation evidence;
6. install-over exact artifact once;
7. `cnxclaw reset` once with normal `y` confirmation;
8. `cnxclaw uninstall` once with normal `y` confirmation;
9. fresh reinstall from the same artifact once;
10. stop/start/restart once each;
11. reviewed v0.9.3 Ollama recovery-reality harness once;
12. final read-only acceptance snapshot;
13. report and stop.

Stop immediately at first non-zero, ownership ambiguity, contradictory evidence, or unexpected external dependency mutation. No destructive command replay and no manual cleanup/normalization.

## External dependency fence

- OpenClaw must remain exactly `2026.7.1-2`; no update/downgrade/reinstall/uninstall.
- Ollama remains selected; no update/reinstall/provider/model change.
- No LM Studio management.
- No credential/token/password access or re-entry.
- No manual SQLite/config/manifest/plugin repair.
- No reboot or generic process-tree kill outside the exact recovery harness.

## Dashboard fence

No Dashboard semantic Send is authorized in Task 116. A final durable-delivery semantic test may be opened only after Task 116 reports PASS and independent review accepts the live lifecycle evidence.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-116-v093-real-windows-lifecycle-acceptance-final-candidate.md`

After publishing, stop for independent ChatGPT review. Do not open the Dashboard semantic-delivery task.
