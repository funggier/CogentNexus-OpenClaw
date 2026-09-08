# CNX-20260903-235 Independent Review — Task234 Exact-Topology TDD Evidence Closure

Date: 2026-09-03 ICT  
Reviewer: ChatGPT  
Repository: `funggier/CogentNexus-OpenClaw`  
Branch: `agent/v0.9.3-full-stabilization`

## Verdict

`ACCEPT_PASS_REPOSITORY_TDD_EVIDENCE_CLOSED__CANDIDATE_READY_FOR_LIVE_REQUALIFICATION`

Task 235 is accepted. The repository/TDD evidence gaps identified by the Task-234 review are closed sufficiently to authorize a separate, controlled Windows install-over requalification of the exact candidate. This review does **not** authorize a Dashboard semantic turn, Discord-origin semantic turn, replay, manual settlement, stale-evidence cleanup, reset/uninstall/fresh-reinstall, or public Release/tag mutation.

## Reviewed authority

Task-235 report:

`docs/operations/coordination/reports/CNX-20260903-235-task234-exact-topology-tdd-evidence-closure.md`

Report-head coordination commit observed at review start:

`3ed3e3408ae28e6a1dd02a44f070a2646e31cf0c`

Exact final candidate:

`ffb0dd4ed47affe2e496c17b74ca74d358905bd7`

Exact final candidate plugin payload fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

Public `v0.9.3` remains immutable at:

`26ce64a624255278a3a0266ad38746e0e6ed2e31`

Parent umbrella:

`CNX-20260831-188`

The umbrella sequencing remains authoritative: install the exact candidate first, establish managed/runtime identity and health, and only after that gate passes perform the single human semantic/durable-delivery requalification. Splitting those effects into separate coordination tasks is accepted as the safer fail-closed decomposition.

## Independent findings

### 1. Corrected RED provenance is accepted

The exact-topology RED commit is:

`517d555cdc3287fe76f74490490cf0431448ee1a`

Its parent is:

`27e34e9f2a45fa3bb5d265cb9908b9cdcd5dcfc7`

Independent commit inspection shows the RED commit changes only:

`tests/test_plugin_static.py`

with no production/source mutation. The regression creates the exact Dashboard-origin + Discord-associated-owner topology and asserts terminal settlement rather than accepting the broken `discord_pending` result. The contradictory recognized-ingress expectation is also encoded fail-closed.

The Task-235 report records the intended RED shape before the final fix, including the exact-topology settlement failure and contradictory-ingress failure. This closes the Task-234 review objection that the corrected production-shaped RED had not been independently established before repair.

### 2. Exact topology now crosses the real settlement boundary

The strengthened regression no longer stops at marker/enqueue/pending staging. It exercises the same Discord-associated owner under Dashboard-origin ingress through durable settlement and requires the terminal behavior expected by the acceptance topology, including completion rather than remaining `discord_pending`.

The same-owner true Discord-origin negative control remains outside Dashboard-native staging. Owner/session identity therefore remains distinct from ingress provenance instead of being globally reclassified.

This closes the Task-234 exact-topology gap.

### 3. Contradictory recognized ingress is fail-closed

Final production candidate commit:

`ffb0dd4ed47affe2e496c17b74ca74d358905bd7`

Its parent is the test-only RED commit above. Independent diff inspection shows the production repair is narrowly scoped to:

`skills/cogentnexus-openclaw/scripts/v091-dashboard-verified-delivery.ts`

with the candidate refusing contradictory recognized ingress candidates instead of silently choosing a precedence winner. The related test expectation is hardened in `tests/test_plugin_static.py`.

No broader session-classification rewrite or unrelated product change was introduced by this final repair.

### 4. Final candidate validation is GREEN

For exact candidate `ffb0dd4ed47affe2e496c17b74ca74d358905bd7`, GitHub Actions were independently rechecked and are terminal GREEN:

- Validate `33688878141` — SUCCESS
- Windows Installer Pack Smoke `33688878183` — SUCCESS
- PS5.1 Acceptance Smoke `33688878240` — SUCCESS

Task-235 report additionally records:

- Python: `478 passed, 33 skipped, 4 subtests passed`
- plugin tests: `58 files / 287 tests passed`
- Dashboard tests: PASS
- lifecycle preview: PASS
- production npm audit: 0 vulnerabilities

### 5. Candidate-to-report drift is coordination-only

Independent compare from exact candidate `ffb0dd4...` to Task-235 report head `3ed3e340...` shows only the Task-235 coordination/report publication commit after the candidate. No product/source/test/workflow drift was introduced after the validated candidate.

### 6. Task-235 live-effect fence remained intact

Task 235 did not perform live candidate installation, Dashboard semantic submission, Discord-origin semantic submission, direct Discord/API Send, manual Ticket/outbox/recovery/SQLite mutation, reset/uninstall/reinstall, or public Release/tag mutation.

The currently installed live payload therefore must not be mistaken for the new candidate merely because repository validation passed. Live identity remains to be established by the successor installer requalification.

## Authorization boundary

This review authorizes exactly one successor class of work:

`exact candidate Windows install-over requalification`

The successor must use exact source candidate:

`ffb0dd4ed47affe2e496c17b74ca74d358905bd7`

and require installed payload fingerprint:

`1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`

The installer task must preserve the repaired Task-226 rollover/attestation safety contract, close its execution retry gate once installer execution begins, permit only bounded evidence-driven tooling/observer retries before or around read-only observation, and preserve Task-223 forensic evidence.

Because the live installed plugin is expected to differ from this new candidate, installer-owned plugin replacement/rollover is permitted if classification requires it. It must not be replaced by manual plugin operations, and any rollover/finalizer failure is terminal for that installer invocation.

## Explicitly not authorized here

Until the installer successor independently passes and is reviewed:

- no Dashboard semantic acceptance message;
- no Discord-origin semantic test;
- no semantic retry/replay;
- no manual durable settlement;
- no Task-233 replay/repair by manufacturing delivery;
- no Task-223 forensic-evidence cleanup;
- no reset, uninstall, or fresh reinstall merely for reassurance;
- no provider/model substitution;
- no Release/tag/asset mutation;
- no force push/history rewrite.

## Final disposition

`ACCEPT_PASS_REPOSITORY_TDD_EVIDENCE_CLOSED__CANDIDATE_READY_FOR_LIVE_REQUALIFICATION`

Next action: open a dedicated installer-only successor, perform the exact-candidate Windows install-over once under explicit fail-closed retry/effect budgets, publish its evidence report, and stop for another independent review before any one-human semantic/durable-delivery acceptance turn.