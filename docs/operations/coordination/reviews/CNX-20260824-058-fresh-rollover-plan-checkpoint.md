# Review — CNX-20260824-058 Fresh Plugin Generation Rollover Plan Checkpoint

Decision: `REWORK`

Disposition: `REWORK_INVENTORY_CAPTURE_BINDING_AMBIGUOUS`

Reviewed report commit: `1650436aabb5d9c384e44a0e10013047090b7729`

Fetched execution HEAD recorded by report: `6a1b371641fcaeeed1659314df7c26f3071cfb42`

Reviewed report path:

`docs/operations/coordination/reports/CNX-20260824-058-fresh-rollover-plan-checkpoint.md`

Reported plan SHA-256:

`360393b0ac8a9ffee0ad603e67efb23b48fe06a7f5e9719d0bc18d03ace76c2c`

## Publication-fence review

The report publication fence itself passes.

Independent GitHub compare from the fetched execution HEAD `6a1b371641fcaeeed1659314df7c26f3071cfb42` to the report-bearing branch state showed exactly one commit and exactly one changed path:

`docs/operations/coordination/reports/CNX-20260824-058-fresh-rollover-plan-checkpoint.md`

No implementation, task, ACTIVE, STATUS, installer, lifecycle, or unrelated repository file was included in the Hermes execution commit.

## Safety review

The durable report records zero live mutations and no `rollover-apply`. It reports controller PASSTHROUGH, startup disabled, no CogentNexus supervisor, healthy Gateway/Ollama, read-only SQLite integrity `ok`, and no installer/plugin/lifecycle/process mutation.

Nothing in this review authorizes apply. The reported Task 058 plan SHA-256 is **not accepted for Phase B authorization**.

## Blocking evidence defect

Task 058 A2 required exactly one invocation of:

`openclaw plugins list --json`

and required the fresh raw inventory captured by that invocation to be the inventory supplied to the planner and SHA-bound in the checkpoint.

The report is internally contradictory:

1. A2 states the command was invoked exactly once.
2. The retained evidence listing includes both `openclaw-plugins-list.json` and `openclaw-plugins-list-before-recapture.json`.
3. The report explicitly states that an `identical-state recapture during this task` was performed.

Therefore Task 058 did not satisfy the exact-once inventory-capture fence.

More importantly, after a recapture the durable report no longer proves without ambiguity that the published raw inventory SHA-256 `B660AB4FEB4CCE610E61E0AF353F9B3046F6AA3DC857AB2607AF885679AF2BCD` belongs to the exact byte file consumed by the one A3 planner invocation. Semantic equality after parsing or equality of the planner-normalized `inventorySha256` is insufficient for the Task 058 raw-input binding requirement.

The report also does not publish the fresh Task 049 manifest SHA-256 required by A1. Local retained evidence may contain additional facts, but a missing required durable proof cannot be inferred during review.

## Findings that remain useful but are not acceptance

The following reported facts are consistent with the intended recovery shape and may be treated only as non-authorizing context for the successor:

- reported plan generation exited `0`;
- reported plan SHA-256 was `360393b0ac8a9ffee0ad603e67efb23b48fe06a7f5e9719d0bc18d03ace76c2c`;
- reported A4 verification was `46 / 46` checks passed;
- normalized registration used package `openclaw-plugin-cogentnexus-openclaw` with `packageNameEvidence: payload-package-json`;
- retired and replacement payload fingerprints matched the expected v0.9.3 payload fingerprint;
- retired and replacement project roots were distinct;
- reported backup destination was under the external product rollover-backup boundary on the same `C:` volume;
- reported live mutation count was `0`.

These facts do not cure the raw inventory binding defect and do not authorize reuse of the Task 058 plan.

## Required successor

Create a fresh Phase A-only successor checkpoint that:

1. uses a new isolated clone and a new unique retained evidence directory;
2. does not use Task 058 inventory or Task 058 plan as planning input;
3. invokes `openclaw plugins list --json` exactly once total for the task;
4. writes that output directly to a uniquely named raw inventory file and never overwrites, renames, replaces, or recaptures it;
5. computes and records the raw SHA-256 immediately after capture;
6. feeds that exact same path to `rollover-plan`;
7. performs all normalized/semantic verification by parsing that same retained file, never by invoking OpenClaw inventory again;
8. explicitly publishes the fresh Task 049 manifest SHA-256;
9. explicitly proves the expected two exact canonical v0.9.3 payload roots and no unexpected third product-owned root;
10. regenerates a fresh machine-produced plan and independently verifies its SHA-256 and all prior safety bindings;
11. stops without `rollover-apply` or any live mutation.

The successor must not reuse or approve Task 058 plan SHA-256 `360393b0ac8a9ffee0ad603e67efb23b48fe06a7f5e9719d0bc18d03ace76c2c`.

## Authorization state

Task 058 is reviewed `REWORK`.

Phase B remains unauthorized.

A future apply task still requires all of the following:

1. an accepted successor fresh-plan checkpoint;
2. explicit operator approval of the exact accepted successor plan SHA-256;
3. a new task recording `PHASE_B_APPLY_AUTHORIZED`, the approved SHA-256, and the accepted review commit.
