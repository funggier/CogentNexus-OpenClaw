# Coordination Channel Status

**State:** `READY_HERMES`  
**Execution mode:** `WINDOWS_REPAIRED_CANDIDATE_INSTALL_OVER_PROVENANCE_HEALTH_HERMES`  
**Updated:** 2026-08-30 ICT  
**Transport:** GitHub repository history  
**Active task:** `CNX-20260830-165`

## Active work

[`tasks/CNX-20260830-165-hermes-windows-install-over-provenance-health.md`](tasks/CNX-20260830-165-hermes-windows-install-over-provenance-health.md)

Executor: Hermes. Coordinator / final reviewer: ChatGPT. ChatGPT review is required before any Dashboard semantic reacceptance.

## Accepted parent checkpoint

Task 164 repository repair is accepted.

Task:

`docs/operations/coordination/tasks/CNX-20260830-164-hermes-native-transcript-authority-red-to-green.md`

Report:

`docs/operations/coordination/reports/CNX-20260830-164-hermes-native-transcript-authority-red-to-green.md`

ChatGPT review:

`docs/operations/coordination/reviews/CNX-20260830-164-hermes-native-transcript-authority-red-to-green-review.md`

Accepted disposition:

`PASS — REPOSITORY_NATIVE_TRANSCRIPT_AUTHORITY_REPAIR_ACCEPTED`

Accepted production repair SHA:

`80b87dfbe0d9176e421f3748b4cee0827db12d0c`

Task-164 exact-SHA workflow evidence:

- Validate `33322815641`: `SUCCESS`
- Windows Installer Pack Smoke `33322815634`: `SUCCESS`
- PS5.1 Acceptance Smoke `33322815695`: `SUCCESS`

Pinned intended OpenClaw target remains:

`0790d9f593ad30c940ed93b5872a8cf6d6f3cf8c` (`v2026.7.1-2`)

## Current objective

Prove that the real Windows installation is actually running the repaired candidate before any new semantic Dashboard test.

Task 165 must:

1. capture pre-install installed provenance and health;
2. prove the install-over artifact derives from the accepted repaired candidate;
3. perform the supported install-over path;
4. prove installed post-state provenance using deterministic package/file evidence;
5. confirm intended OpenClaw version/provenance;
6. confirm CogentNexus plugin/schema/bootstrap/status/health coherence;
7. avoid every semantic Dashboard Send or equivalent semantic live input.

## Current gate

No exactly-one-Send Dashboard reacceptance is authorized yet.

Task 165 must first complete and publish:

`docs/operations/coordination/reports/CNX-20260830-165-hermes-windows-install-over-provenance-health.md`

ChatGPT must independently review that report and evidence.

Only an accepted Task-165 PASS may authorize creation of the later exactly-one-Send Dashboard durable-delivery reacceptance task.

## Hard fence

Supported repaired-candidate install-over and its inherently required runtime transitions are authorized.

No Dashboard semantic Send; no semantic input through another live OpenClaw surface; no uninstall/reinstall/reset without separate authorization; no manual Ticket/workflow/result/outbox/delivery/database mutation; no arbitrary live-state deletion; no OpenClaw patch/upgrade; no unrelated product repair; no release/promotion; no merge to default/release branch; no force push.
