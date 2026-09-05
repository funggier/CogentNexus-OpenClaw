# CNX-20260905-261 — Deployment-Transition Process-Boundary Repair

**Final disposition:** `REPAIRED_DEPLOYMENT_TRANSITION_BOUNDARY__NEW_CANDIDATE_REVIEW_REQUIRED`

**Repository:** `funggier/CogentNexus-OpenClaw`
**Branch:** `agent/v0.9.3-full-stabilization`
**Final exact HEAD:** `a87c3930651eecf4563d5d8bafe897e058bbdfe0`
**Executor:** Luna
**Independent reviewer / next actor:** Musethree
**Parent:** CNX-20260905-260

## Authority and lineage

Fresh opening authority was Task261 at `4472c199a65c4f5282bc518cd4930e72db4a3452`, linearly after Task260 coordination commit `bbfd43408282a94a76c7d3aa69953f6dcc0d09e8`. Task261 authorized repository/source/test repair only and explicitly prohibited live installer execution, Gateway/provider lifecycle mutation, live DB/recovery mutation, recovery disposition/redelivery, semantic acceptance, release/tag mutation, and force-push.

The repair lineage is linear and published:

1. `5a40a21783eabe4a3e546f03c5d71c699a5e11ff` — TDD regression RED for install-over process boundary and installed fingerprint binding.
2. `0a0368628c6dec613a5cbbd0b49cfdc498f98dd6` — minimal production repair.
3. `a87c3930651eecf4563d5d8bafe897e058bbdfe0` — corrective test-fixture mock required by the first authoritative Validate failure.

No force-push or rewrite occurred; local and remote final HEAD are exact.

## Root cause confirmation

Task260's finding was reproduced from exact source: `lifecycle start` can skip an already-healthy Gateway, while install-over had no mandatory process boundary after replacement. The existing proven `openclaw_runtime_boundary_v092.activate_current_config()` restarts and verifies the current Gateway configuration.

## TDD evidence

### RED

Added `test_install_over_forces_fresh_boundary_and_binds_installed_fingerprint` to `tests/test_v091_install_wiring.py`. Native unittest execution on the unmodified implementation failed exactly because `host_v091.py` lacked `activate_current_config` and `install.ps1` lacked the explicit installed-vs-expected fingerprint guard. Existing tests in that file passed (5/5).

A first local pytest invocation failed only because pytest was absent from the Hermes venv; the supported unittest entrypoint then produced the genuine product-shaped RED. This harness event is recorded separately from product outcome.

### Minimal repair

1. `skills/cogentnexus-openclaw/scripts/host_v091.py`
   - imports `openclaw_runtime_boundary_v092`;
   - after `legacy.runtime(..., "lifecycle", "start", "--provider")`, calls `runtime_boundary.activate_current_config()`;
   - fails closed if the mandatory fresh process boundary is not verified;
   - returns boundary evidence in the enable result.

2. `scripts/install.ps1`
   - retains the source candidate fingerprint as `$expectedPluginFingerprint`;
   - parses the post-install `resolve-plugin` result;
   - compares `$installedPluginFingerprint` to the expected candidate fingerprint case-insensitively and fails closed on invalid/mismatched identity before managed activation.

3. `tests/test_host_v091.py`
   - corrective fixture mock for the new boundary dependency, committed separately as `a87c393` after authoritative CI exposed the missing mock.

### GREEN and corrective CI

Local verification on final checkout:

- `python tests/test_v091_install_wiring.py -v`: 6/6 passed.
- `python tests/test_host_control_v092.py -v`: 9/9 passed.
- `python tests/test_openclaw_runtime_boundary_v092.py -v`: 4/4 passed.
- `python -m pytest -q`: 517 passed, 5 skipped, 4 subtests passed.
- `git diff --check`: passed.
- Plugin `npm test`: 58/58 files, 286/286 tests passed.
- `npm run plugin:validate`: passed.
- `npm run plugin:build`: passed.

First authoritative failure:

- HEAD `0a0368628c6dec613a5cbbd0b49cfdc498f98dd6` Validate run `33958878098`: failed with 2 existing `host_v091` tests not stubbing the new boundary; the exact error was `OpenClaw CLI unavailable` from the unmocked boundary. PS5.1 and Installer passed on that SHA.

Corrective rerun was not a blind workflow rerun: the test fixture was repaired and published as the next exact commit `a87c3930651eecf4563d5d8bafe897e058bbdfe0`. Its exact CI is terminal success:

- PS5.1 Acceptance Smoke — `33959290275` — completed success.
- Windows Installer Pack Smoke — `33959290257` — completed success.
- Validate — `33959290259` — completed success.

## Contract result

The successful install-over path now requires both:

- an explicit installed payload fingerprint equal to the candidate source fingerprint before managed activation; and
- a fresh Gateway process boundary after candidate replacement/lifecycle start, with post-boundary health verification before enable success.

The existing transactional rollback path remains in force; the repair did not add recovery replay, semantic output, or unrelated refactoring. `-SkipGatewayRestart` remains staging-only and does not claim verified managed transition.

Because production source changed, Task259's `d1531404...` is reference-only and the final `a87c393...` tree is a new candidate requiring independent review, exact-SHA CI binding, and fresh Windows proof before any live install-over successor.

## Hard-fence ledger

All counts remained zero throughout Task261:

- installer Scheduled Task registration/start: `0`
- `scripts/install.ps1` live starts: `0`
- Gateway/controller/provider lifecycle mutation: `0`
- live DB/recovery row mutation: `0`
- recovery dispose/claim/replay/redeliver/resend: `0`
- Dashboard/Discord/API semantic sends: `0`
- release/tag mutation: `0`
- force push/history rewrite: `0`

## Next step

Stop Task261 for independent review by Musethree. No live install-over, Gateway restart, recovery disposition/redelivery, or semantic acceptance is authorized by this repair task.
