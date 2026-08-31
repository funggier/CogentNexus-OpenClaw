# CNX-20260827-085 — Correct Attested Classification and Pending-Rollover Control Flow

Status: `READY_FOR_HERMES`

Execution mode: `SOURCE_TDD_ATTESTED_UPGRADE_TRUTH_TABLE_REPAIR`

Current authorization: `TASK084_CONTROL_FLOW_REWORK_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Preserve the sound Task-084 source-attestation and rollover-plan/apply primitives, while correcting the installer-facing classification truth table and production plugin lifecycle control flow so all supported upgrade states behave exactly as intended:

- single old generation different from candidate source -> install replacement, then rollover;
- exact pending two-generation recovery -> do **not** install a third generation, but **do** complete rollover;
- already exact single generation -> create no redundant generation and perform no rollover;
- attested pending recovery is authorized only when the active replacement equals the exact expected source fingerprint.

This task is source/test only. It must not mutate the live Task-083 two-generation partial installation.

## Rework base and predecessor review

Task-084 implementation to preserve as the base:

`0847a260d6f689f364bb096bd7857bb1dd4d58e1`

Task-084 report:

`658eb55b5163c5d74a44ce75ca2c04f538a46ba3`

Independent review:

Decision: `REWORK`

Disposition:

`REWORK_ATTESTED_CLASSIFICATION_AND_PENDING_ROLLOVER_CONTROL_FLOW`

Review path:

`docs/operations/coordination/reviews/CNX-20260827-084-repair-same-version-rollover-attestation-and-pending-recovery.md`

## Task-084 work to preserve

Do not rewrite these unless a focused failing test proves a defect in the primitive itself:

- `plugin-fingerprint` uses the existing `_plugin_payload()` contract;
- explicit `expectedReplacementFingerprint` in rollover plan;
- `replacementAuthorization` audit field;
- wrong/unattested changed replacement rejection;
- apply-time re-entry through `_exact_rollover_state()`;
- generic two-candidate `resolve_installed_plugin()` ambiguity;
- wrapper proofs;
- inventory and active-registration hashes;
- project-tree hashes;
- manifest-before hash;
- plan hash;
- atomic same-volume retirement and rollback;
- Task-078/079/080 semantic/delivery fixes;
- Task-082 npm-pack resolver repair.

## Accepted live state — READ ONLY

The current live system remains the Task-083 fail-closed partial topology:

- controller `passthrough`, generation 13;
- startup disabled;
- Supervisor absent;
- AGENTS managed block absent;
- ownership manifest points to prior generation `g-5593cbcfff5b35d5`;
- newer active/registered disabled generation `g-7257c4555ca8ad21` remains present;
- old fingerprint `7e9189f8...`;
- newer/source fingerprint `8fd911e3...`;
- Gateway healthy;
- Ollama healthy with accepted four models;
- SQLite integrity `ok`, Tickets/outbox zero;
- no semantic/provider activity.

Task 085 must not normalize or mutate this state.

---

# Critical payload-preservation fence

Do not modify any file under:

`plugins/cogentnexus-openclaw/**`

The live Task-083 replacement must remain fingerprint-equivalent to the candidate plugin payload already installed there.

Production edits should remain in the ownership/installer control plane, primarily:

- `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`;
- `scripts/install.ps1`;
- optionally one small PowerShell control-flow helper under `scripts/` if that is the clearest way to make the lifecycle truth table directly executable/testable;
- focused tests under `tests/`.

Do not bump v0.9.3.

---

# Absolute live fence

Task 085 is source/test only.

Do NOT:

- invoke the live installer/install-over;
- uninstall/reset/clean reinstall;
- delete/rename either live plugin generation;
- edit live ownership/controller/startup/Supervisor/AGENTS/config/runtime/launcher;
- enable/disable the live plugin;
- mutate live SQLite/Ticket/session state;
- send Dashboard/WebChat, `chat.send`, `openclaw agent`, `sessions_send`, channel or any semantic/user message;
- call Ollama directly;
- change provider/model/timeouts;
- restart Gateway/Ollama/Supervisor;
- reboot;
- merge/tag/release.

Read-only verification of live fingerprints/state is allowed, but is not required to repeat if Task-084 evidence remains current and no drift is observed.

Use a fresh isolated worktree.

---

# Phase A — execution and source fence

Before editing:

1. fetch the current coordination branch;
2. record exact execution HEAD;
3. prove Task-084 report and REWORK review are ancestors;
4. create a fresh isolated worktree/branch;
5. verify clean status;
6. record production source parent/HEAD;
7. confirm `git diff 0847a260... -- plugins/cogentnexus-openclaw` is empty;
8. read completely the changed Task-084 sections of:
   - `scripts/install.ps1`;
   - `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`;
   - `tests/test_plugin_generation_rollover.py`;
   - installer classification/mode/recovery tests.

Do not edit production before RED tests are added and observed failing for the exact three review findings.

---

# Gate R — mandatory RED evidence against Task-084 implementation

## R1 — ordinary single-generation changed-source upgrade

Construct one coherent manifest-owned v0.9.3 generation whose fingerprint is `OLD`, with expected candidate-source fingerprint `NEW`, where `OLD != NEW`.

Call the real attested `classify_install()` / CLI path with one canonical product registration and the expected source fingerprint.

Required final result:

```json
{
  "mode": "upgrade",
  "pendingRollover": false,
  "pluginAlreadyExact": false
}
```

Task-084 implementation should RED because it raises `manifest-owned plugin does not match the expected source attestation` instead of allowing normal replacement installation.

Record this RED explicitly.

## R2 — pending installer action truth table

Exercise the production lifecycle decision used by `install.ps1` for:

`mode=upgrade, pendingRollover=true, pluginAlreadyExact=false, SkipPlugin=false`.

Required actions:

- `installPlugin=false`
- `rolloverPlugin=true`

The Task-084 wiring must RED because its outer condition causes both actions to be false.

This must be tested against an executable production decision surface, not only described in prose.

Preferred smallest design:

- introduce a tiny PowerShell 5.1-compatible pure action resolver under `scripts/`, or
- expose an equivalently testable pure production function used directly by `install.ps1`.

Do not maintain a separate test-only copy of the truth-table logic.

## R3 — two equivalent old generations must not impersonate current source

Construct exactly two valid candidate generations where:

- retired fingerprint = `OLD`;
- active replacement fingerprint = `OLD`;
- expected candidate-source fingerprint = `NEW`;
- `OLD != NEW`.

Use explicit attested classification.

Required final behavior:

`FAIL CLOSED`

because the active replacement is not the candidate source, even though it equals the retired generation.

Task-084 implementation should RED because `_exact_rollover_state()` currently checks source attestation only when replacement and retired fingerprints differ.

Record that RED.

---

# Gate C — corrected attested classification truth table

Implement the minimum correction in `namespace_ownership.py`.

## C1 — one manifest-owned candidate

When explicit inventory + expected source fingerprint are supplied and exactly one canonical candidate exists at the manifest path:

### Candidate fingerprint equals expected source

Return:

- `mode=upgrade`
- `pendingRollover=false`
- `pluginAlreadyExact=true`
- manifest and replacement paths equal that one candidate
- expected fingerprint recorded

### Candidate fingerprint differs from expected source

Do **not** reject merely because it is old.

Return:

- `mode=upgrade`
- `pendingRollover=false`
- `pluginAlreadyExact=false`
- `manifestPluginPath` = old canonical candidate
- `replacementPluginPath` may be null/absent until OpenClaw installs the replacement, but output schema must be deterministic and tested
- expected fingerprint recorded

This is the normal changed-source install-over path.

Before returning it, retain coherent ownership checks and reject foreign/wrong registration or manifest boundaries as appropriate.

## C2 — exactly two candidates, explicit pending recovery

Return `pendingRollover=true` only when **all** Task-084 P2 fences pass and:

`active replacement fingerprint == expected source fingerprint`

This equality is mandatory regardless of whether:

- replacement fingerprint differs from retired fingerprint, or
- replacement fingerprint happens to equal retired fingerprint.

If explicit expected fingerprint is supplied and active replacement differs from it, fail closed.

## C3 — legacy equivalent-generation rollover compatibility

Existing old behavior without an explicit source-attestation input may still permit an equivalent-generation rollover when retired and replacement fingerprints are equal and all old rollover fences pass.

Do not accidentally require candidate-source attestation for every historical/internal equivalent-generation unit test if no explicit expected authority was supplied.

The important distinction is:

- explicit expected fingerprint supplied -> active replacement MUST match it;
- no expected supplied + changed replacement -> reject;
- no expected supplied + equivalent replacement -> preserve existing reviewed equivalent-generation behavior.

## C4 — three or more candidates remain rejected

No classification or plan path may normalize a three-generation topology.

---

# Gate A — one production plugin lifecycle action truth table

Use one production source of truth consumed by `scripts/install.ps1`.

A small PowerShell helper is recommended because it can be dot-sourced and executed directly under Windows PowerShell 5.1 without invoking the installer.

Inputs should cover at least:

- mode (`fresh`, `legacy`, `upgrade`);
- `pendingRollover` boolean;
- `pluginAlreadyExact` boolean;
- `SkipPlugin` boolean if useful.

Required action truth table with `SkipPlugin=false`:

| mode | pending | exact | install plugin | rollover |
|---|---:|---:|---:|---:|
| fresh | false | false | true | false |
| legacy | false | false | true | false |
| upgrade | false | false | true | true |
| upgrade | true | false | false | true |
| upgrade | false | true | false | false |

Reject logically impossible combinations such as both `pending=true` and `exact=true` rather than silently guessing.

If `SkipPlugin=true`, preserve existing staging semantics and ensure no install/rollover action occurs; existing installer preflight restrictions remain authoritative.

Test this helper directly under Windows PowerShell 5.1.

---

# Gate I — production installer wiring

Refactor only the plugin lifecycle portion necessary to consume the action truth table.

## I1 — source preparation/classification remains pre-mutation

Preserve Task-084 behavior:

- candidate `npm ci` and plugin validation before fingerprinting;
- expected fingerprint derived from source `$pluginDir`;
- read-only OpenClaw inventory captured before classification;
- explicit attested classification arguments;
- classification result captured before mutation.

Do not derive expected authority from live replacement inventory.

## I2 — separate install action from rollover action

The installer must no longer nest rollover under the condition that excludes pending recovery.

Conceptually:

```text
if installPlugin:
    perform npm-pack / openclaw install / disable replacement

if rolloverPlugin:
    perform rollover-plan / rollover-apply
```

These are two independent action gates.

Do not use one outer `if` that makes `pendingRollover=true` skip the rollover block.

## I3 — pending recovery

For `upgrade + pending=true + exact=false`:

1. enter/confirm PASSTHROUGH through existing lifecycle behavior;
2. skip `npm pack`;
3. skip `openclaw plugins install`;
4. do not create a third generation;
5. capture fresh OpenClaw inventory for rollover planning;
6. call rollover-plan with exact expected candidate-source fingerprint;
7. call rollover-apply with fresh inventory and plan hash;
8. require success;
9. unique `resolve-plugin` after rollover must see exactly one active canonical candidate;
10. continue launcher/runtime/ownership/AGENTS/MANAGED restoration normally.

The current Task-083 residue must be recoverable through this path in the later live task without manual generation deletion.

## I4 — ordinary changed-source upgrade

For `upgrade + pending=false + exact=false`:

1. run normal Task-082 npm-pack resolver path;
2. install candidate replacement once;
3. disable replacement in PASSTHROUGH;
4. run attested rollover;
5. replacement must equal source fingerprint;
6. retire old generation atomically;
7. continue normally.

## I5 — already exact upgrade

For `upgrade + exact=true`:

- no npm pack;
- no `openclaw plugins install`;
- no generation rollover;
- preserve the one canonical generation;
- continue supported install-over restoration.

## I6 — fresh and legacy paths

Preserve historical behavior:

- fresh/legacy needing plugin -> install once;
- no upgrade-generation rollover is invented for a topology that has no manifest-owned prior v0.9.3 generation;
- existing fresh transaction rollback rules remain intact.

## I7 — Ticket DB bootstrap

Review the current placement of `bootstrap-ticket-db.mjs` after separating install and rollover actions.

It must not be accidentally skipped if the installer contract requires bootstrap on pending/already-exact recovery. Prefer one safe idempotent bootstrap for every non-`SkipPlugin` install-over after source validation, unless existing tests prove a narrower placement is intentional.

Do not mutate live DB in Task 085; verify only through isolated tests.

---

# Gate T — production-facing regression coverage

Tests must catch the exact Task-084 wiring bug, not only ownership primitives.

At minimum include:

1. direct PowerShell 5.1 truth-table test of the production action resolver;
2. source/wiring test proving installer consumes the resolver result;
3. proof pending action invokes rollover path while package-install action is false;
4. proof ordinary upgrade invokes both install then rollover;
5. proof already-exact invokes neither;
6. proof rollover occurs before later `resolve-plugin` / ownership publication in pending/ordinary upgrade paths;
7. proof pending path contains no `npm pack` / `openclaw plugins install` call through its selected action;
8. deterministic namespace fixture proving pending apply leaves one canonical generation;
9. deterministic ordinary changed-source fixture proving classification no longer blocks before install;
10. negative equivalent-old-two-generation fixture proving mismatched expected source fails closed.

A purely textual assertion that one token exists somewhere in `install.ps1` is insufficient by itself. Pair any static wiring assertions with the executable action truth table and real namespace primitives.

---

# Security and atomicity regression matrix

Re-run and preserve all Task-084 negatives:

- changed replacement without source attestation rejected;
- wrong expected source rejected;
- active registration at manifest-owned old root rejected for pending;
- active root outside OpenClaw state rejected;
- three candidates rejected;
- foreign/shared wrapper rejected;
- wrong id/package/version rejected;
- non-PASSTHROUGH pending rollover rejected;
- inventory drift between plan/apply rejected;
- manifest drift rejected;
- replacement payload/tree drift rejected;
- unrelated project preserved;
- atomic rename failure leaves old/new/manifest unchanged;
- final verification failure restores old project/manifest;
- exact plan hash required;
- generic two-candidate resolution remains ambiguous.

Also add the new explicit-attestation invariant:

- if an expected source fingerprint is supplied, active replacement must match it even when retired and replacement are equivalent to each other.

---

# Full verification

After GREEN, run and record fresh output for:

1. focused Task-085 classification/action truth-table tests;
2. full `tests/test_plugin_generation_rollover.py`;
3. namespace ownership/classification tests;
4. installer mode/wiring/recovery tests;
5. Task-082 npm-pack boundary tests;
6. Task-069–074 transaction/recovery tests;
7. Task-078/079/080 semantic/delivery/security tests;
8. full Python suite;
9. `python -m py_compile` for modified Python;
10. Windows PowerShell 5.1 syntax for modified/new PowerShell;
11. Windows PowerShell 5.1 action truth-table execution;
12. Node 24/npm 11 clean `npm ci`, plugin tests, validation and package checks;
13. Node 22/npm 12 clean `npm ci`, plugin tests, validation and package checks;
14. baseline consistency;
15. `git diff --check`;
16. final `git status --short`;
17. verify zero diff under `plugins/cogentnexus-openclaw/**` relative to Task-084 implementation/predecessor plugin payload.

Do not claim PASS from focused tests only.

---

# Read-only live preservation check

At the end, optionally re-read enough live state to prove Task 085 did not mutate it:

- controller still passthrough;
- both Task-083 generations still present;
- manifest still points old;
- active registration still newer/disabled;
- fingerprints unchanged;
- Supervisor/AGENTS state unchanged;
- no Tickets/outbox/semantic/provider activity generated.

No corrective action is authorized if a drift is observed; report it.

---

# Publication fence

Implementation may change only the bounded Task-085 source/test files.

Publish implementation commit(s), then exactly one report:

`docs/operations/coordination/reports/CNX-20260827-085-correct-attested-classification-and-pending-rollover-control-flow.md`

The final report commit must be report-only.

Report must include:

- execution HEAD;
- implementation HEAD(s);
- exact files changed;
- RED evidence R1/R2/R3;
- corrected classification truth table;
- production PowerShell action truth table;
- installer wiring evidence;
- pending/ordinary/exact behavior;
- security/atomicity matrix;
- full verification outputs;
- zero plugin payload diff;
- live mutation accounting;
- publication fence.

## Result tokens

Use exactly one:

- `PASS_ATTESTED_CLASSIFICATION_AND_PENDING_ROLLOVER_CONTROL_FLOW_REPAIRED`
- `BLOCKED_CLASSIFICATION_CONTRACT`
- `BLOCKED_INSTALLER_ACTION_CONTROL_FLOW`
- `BLOCKED_SECURITY_OR_ATOMICITY_REGRESSION`
- `BLOCKED_FULL_REGRESSION_GATE`
- `BLOCKED_PLUGIN_PAYLOAD_PRESERVATION`
- `BLOCKED_LIVE_STATE_DRIFT`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

---

# Successor gate

Only an independently accepted:

`PASS_ATTESTED_CLASSIFICATION_AND_PENDING_ROLLOVER_CONTROL_FLOW_REPAIRED`

may authorize the next live recovery attempt.

That later live task will use one supported install-over on the existing Task-083 two-generation topology and must prove:

`source fingerprint -> attested pending classification -> installPlugin=false -> rolloverPlugin=true -> atomic old retirement -> unique source-exact generation -> MANAGED/startup/Supervisor/AGENTS restoration -> source/live parity -> five natural no-flash ticks -> Dashboard owner-surface readiness`

with zero semantic/user messages.

Final semantic acceptance remains a separate task after that live gate passes.
