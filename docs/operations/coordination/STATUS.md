# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `SOURCE_ONLY_TDD`  
**Updated:** 2026-08-28 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator authorized continued stabilization; Task 111 authorizes source/test/CI repair only  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260828-111-interrupted-rollover-reentry-repair.md`](tasks/CNX-20260828-111-interrupted-rollover-reentry-repair.md)

Task ID:

`CNX-20260828-111`

## Task 110 closure

Task-110 report:

`docs/operations/coordination/reports/CNX-20260828-110-rollover-retired-state-exactness-repair.md`

Task-110 independent review:

`docs/operations/coordination/reviews/CNX-20260828-110-rollover-retired-state-exactness-repair-review.md`

Review commit:

`ad9532fa88dcbc9b23db7abf0e47229794386b17`

Review verdict:

`ACCEPTED PASS — TASK-110 DEFECT REPAIRED; LIVE GATE BLOCKED BY PRE-EXISTING INTERRUPTED-ROLLOVER RE-ENTRY GAP`

Task 110 satisfied its strict TDD contract:

- test-only RED `edec90ac455cf3cf6b3b9842e5ca3fe5c0014338`;
- production fix `25d229cd496a11af37ea2ff556a0126dfc194377`;
- exact Validate `33164787392` success;
- exact Windows Installer Pack Smoke `33164787432` success;
- exact PS5.1 Acceptance Smoke `33164787396` success;
- exact artifact `9683127656` with outer SHA256 `90a9e329c040312ded336de4c7dd6f81b1c546aceb7869d6d284a119d7a87b25`.

The Task-110 package is valid historical source/package evidence but is not live-authorized because the preserved Task-107 live state exposes a separate installer re-entry gap.

## Confirmed Task-111 gap

The preserved Task-107 failure happened after the external local `.tgz` OpenClaw plugin installation succeeded. That external operation removed the old manifest-owned npm generation before the then-current ownership rollover failed.

No later task performed live mutation, so Task 107 remains the last authoritative live boundary.

At Task-110 source:

- `recovery-preflight` automatically recovers incomplete **fresh** transactions only;
- an existing ownership manifest returns `OWNERSHIP_PRESENT`;
- attested `classify-install` then calls `verify_manifest(... verify_plugin=False)` while `require_artifacts=True` remains active;
- the manifest's old `pluginPath` is therefore required to exist;
- Task 107 already removed that exact path.

A new live install-over would consequently stop at pre-mutation classification. This is safe fail-closed behavior, but it cannot complete the required acceptance sequence.

## Authorized Task-111 sequence

Only source/test/CI work is authorized:

`reconcile -> separate TEST-ONLY RED commit -> reproduce Task-107-shaped interrupted rollover -> minimal narrow re-entry repair -> GREEN targeted -> full validation -> exact Actions/package proof -> report`

The valid recovery path must prove exact manifest metadata/non-plugin artifacts, PASSTHROUGH controller, a specifically missing retired path, exactly one canonical active replacement, exact candidate fingerprint/version/package/id, OpenClaw containment, and absence of conflicting/mixed state.

If the exact active replacement is already present, re-entry must not perform an unnecessary second external plugin installation. Final normal ownership creation and exact verification must bind the replacement before MANAGED authority.

All ambiguous, altered, foreign, multiple, mismatched, or incomplete states remain fail-closed.

## Source boundary

Accepted Task-110 candidate:

`25d229cd496a11af37ea2ff556a0126dfc194377`

Task-110 report descendant:

`efbb8f19d19dfcb9ad8b8525a6393996db688324`

Task-110 review/task coordination commits after that are documentation-only at Task-111 authorization time. Executor must fetch current GitHub state before editing and stop `BLOCKED` on unexplained production drift.

## Preserved live boundary

Task 111 must not touch the machine. The last recorded Task-107 post-failure state remains evidence only: CNX passthrough generation `25`, OpenClaw `2026.7.1-2`, Gateway healthy, Ollama healthy/ready, SQLite integrity `ok`, Supervisor absent, and installer residue retained.

A future live task must verify the machine read-only rather than assume this state still exists.

## Hard fence

Task 111 does **not** authorize:

- any real Windows install-over/reset/uninstall/reinstall/lifecycle/recovery action;
- replaying Task 107;
- manual live cleanup/normalization;
- Dashboard semantic Send;
- OpenClaw/Ollama update, reinstall, uninstall, stop, or rebaseline;
- provider/model/timeout changes;
- live SQLite/config/session mutation;
- credential/token/password access or re-entry;
- LM Studio management;
- process-tree kills;
- reboot;
- merge/tag/GitHub Release/force push;
- generic adoption of partial or unowned plugin state.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-111-interrupted-rollover-reentry-repair.md`

The report must include separate RED/fix commits, exact RED failure, positive/negative re-entry semantics, GREEN/full validation, exact candidate source, exact three workflow run IDs/results, and a new exact package-proof artifact identity/hashes/fingerprint.

After report publication, stop for independent ChatGPT review. No real-Windows lifecycle acceptance task is authorized until that review accepts a new exact candidate.
