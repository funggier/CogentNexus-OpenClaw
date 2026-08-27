# CNX-20260827-086 — Fix Production Pending-Rollover Gate Nesting

Status: `READY_FOR_HERMES`

Execution mode: `SOURCE_TDD_PRODUCTION_ROLLOVER_GATE_REPAIR`

Current authorization: `TASK085_NESTING_REWORK_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Make the smallest source-only correction so `scripts/install.ps1` actually consumes the already-correct Task-085 lifecycle truth table as two independent production gates:

`installPlugin` controls package creation only,

and

`rolloverPlugin` controls rollover-plan/apply independently.

The exact pending recovery tuple:

```text
mode=upgrade
pendingRollover=true
pluginAlreadyExact=false
installPlugin=false
rolloverPlugin=true
```

must execute the existing attested rollover without running npm-pack/OpenClaw plugin install and without creating a third generation.

This task must not mutate the current live Task-083 two-generation PASSTHROUGH installation.

## Rework base

Preserve Task-085 implementation as the source base:

`6b5c9d56a48d4affe67c2bb718898378edee6e8a`

Task-085 report:

`d8951eb1b724fc60236e458a78da0cef2926868d`

Independent review:

Decision: `REWORK`

Disposition:

`REWORK_PENDING_ROLLOVER_STILL_NESTED_UNDER_INSTALL_GATE`

Review path:

`docs/operations/coordination/reviews/CNX-20260827-085-correct-attested-classification-and-pending-rollover-control-flow.md`

## Preserve these accepted Task-084/085 components

Do not redesign or rewrite these without a focused failing test:

- `plugin-fingerprint` source-attestation primitive;
- explicit expected replacement fingerprint in rollover plan/apply;
- apply-time source-attestation re-proof;
- generic two-generation ambiguity/fail-closed resolution;
- single-generation classification truth table;
- explicit expected-source equality for every attested pending replacement;
- `scripts/resolve-plugin-lifecycle-actions.ps1` truth table;
- Ticket DB bootstrap outside package-install gate;
- Task-082 npm-pack resolver;
- ownership manifest/inventory/wrapper/tree/plan-hash fences;
- atomic retirement and rollback;
- Task-078/079/080 semantic/delivery/security lineage.

## Critical payload-preservation fence

Do not modify any file under:

`plugins/cogentnexus-openclaw/**`

The live newer generation `g-7257c4555ca8ad21` must remain fingerprint-equivalent to the candidate plugin payload already installed by Task 083.

Expected production edits should be limited to:

- `scripts/install.ps1`;
- focused tests;
- only if necessary, a small test-support/production AST helper under `scripts/` that does not duplicate installer business logic.

Do not bump v0.9.3.

## Absolute live fence

Task 086 is source/test only.

Do NOT:

- run live install/install-over;
- uninstall/reset/clean reinstall;
- delete/rename either live plugin generation;
- enable/disable the live plugin/controller/startup;
- create/delete/replace Supervisor;
- edit live AGENTS, ownership, config, runtime or launcher;
- mutate live SQLite/Ticket/session state;
- send Dashboard/WebChat, `chat.send`, `openclaw agent`, `sessions_send`, channel or semantic/user messages;
- call Ollama directly;
- change provider/model/timeouts;
- restart Gateway/Ollama/Supervisor;
- reboot;
- merge/tag/release.

Read-only state/fingerprint verification is allowed but need not be repeated if no drift is observed.

Use a fresh isolated worktree.

---

# Phase A — execution fence

Before editing:

1. fetch the coordination branch;
2. record exact execution HEAD;
3. prove Task-085 report and REWORK review are ancestors;
4. create a clean isolated worktree/branch;
5. confirm production base contains implementation `6b5c9d56...`;
6. confirm zero diff under `plugins/cogentnexus-openclaw/**` relative to `6b5c9d56...`;
7. read the full plugin lifecycle portion of `scripts/install.ps1` and the existing Task-085 tests.

Do not edit production before RED evidence.

---

# Gate R — mandatory RED against Task-085 implementation

## R1 — production AST nesting regression

Add a Windows PowerShell 5.1-compatible test against the **real** `scripts/install.ps1` using `System.Management.Automation.Language.Parser` or an equivalently exact PowerShell AST surface.

The test must locate the production rollover-plan/apply invocation and prove its ancestor control-flow.

Required final invariant:

- rollover command is controlled by a condition containing `$actions.rolloverPlugin`;
- rollover command is **not** a descendant of any `if` condition that depends on `$actions.installPlugin`.

Run this test against Task-085 implementation `6b5c9d56...` before fixing source.

Required RED reason:

`rollover is nested under installPlugin gate`

Do not accept a RED caused by parser/setup failure.

## R2 — package install remains install-gated

The same production-AST test should prove npm-pack/OpenClaw package-install operations remain descendants of `$actions.installPlugin`.

This requirement should already pass on the predecessor and protects the separation from being fixed by simply removing all action gates.

## R3 — source order

Prove in the actual production script that:

1. package install block, when selected, precedes rollover;
2. rollover block precedes the later strict `resolve-plugin` call and ownership creation.

The pending path relies on rollover finishing before unique resolution.

---

# Gate F — minimal production fix

Refactor only braces/gates necessary to create two sibling actions.

Required structure is conceptually:

```powershell
if ($actions.installPlugin) {
    # candidate npm-pack / OpenClaw plugins install / disable
}

if ($classification.mode -eq "upgrade" -and $actions.rolloverPlugin) {
    # rollover-plan / rollover-apply
}
```

Equivalent structure is allowed if the production AST proves the same semantics.

Do not duplicate rollover implementation.

Do not call rollover for fresh or legacy states.

Do not create a new plugin generation during pending recovery.

Do not change attestation or ownership primitives unless a separate RED proves a defect.

---

# Gate T — action matrix + production-consumption proof

Preserve and rerun the Task-085 executable action resolver truth table:

| mode | pending | exact | install | rollover |
|---|---:|---:|---:|---:|
| fresh | false | false | true | false |
| legacy | false | false | true | false |
| upgrade | false | false | true | true |
| upgrade | true | false | false | true |
| upgrade | false | true | false | false |

Also retain `SkipPlugin -> false/false` and impossible `pending+exact -> fail`.

Add production-consumption assertions proving:

- pending row reaches rollover code despite install=false;
- ordinary upgrade reaches install then rollover;
- already-exact reaches neither operation;
- fresh/legacy install but do not enter upgrade rollover;
- rollover precedes strict unique `resolve-plugin`.

The test must inspect/execute the real production script structure rather than maintaining a second copy of installer branching.

---

# Gate C — namespace and pending residue fixture

Rerun existing deterministic fixtures proving:

1. Task-083 two-generation topology classifies as pending only with exact source attestation;
2. wrong expected fingerprint fails;
3. generic resolver remains ambiguous before rollover;
4. attested plan/apply retires old generation;
5. resolver becomes unique afterward;
6. manifest binds newer source-exact generation;
7. no third generation is created by the fixture.

Also rerun ordinary changed-source single-generation classification and already-exact classification.

---

# Security/atomicity preservation

Re-run all Task-084/085 negatives, including:

- changed replacement without attestation rejected;
- wrong expected source rejected;
- explicit source mismatch rejected even for equivalent old/new payloads;
- active old-root registration rejected for pending;
- outside-state registration rejected;
- three candidates rejected;
- foreign/shared wrapper rejected;
- wrong id/package/version rejected;
- non-PASSTHROUGH rollover rejected;
- inventory drift rejected;
- manifest drift rejected;
- replacement payload/tree drift rejected;
- unrelated project preserved;
- atomic rename failure preserves old/new/manifest;
- final-verification failure restores old project + manifest;
- exact plan hash required.

---

# Full verification

After GREEN, record fresh outputs for:

1. new PowerShell 5.1 production-AST nesting/order regression;
2. Task-085 action truth-table tests;
3. full `tests/test_plugin_generation_rollover.py`;
4. namespace ownership/classification tests;
5. installer mode/wiring/recovery tests;
6. Task-082 npm-pack boundary tests;
7. Task-069–074 transaction/recovery tests;
8. Task-078/079/080 semantic/delivery/security tests;
9. full Python suite with zero failures;
10. Python compilation for relevant Python files;
11. Windows PowerShell 5.1 syntax for modified PowerShell;
12. Node 24/npm 11 clean `npm ci`, full plugin tests, validation/package checks;
13. Node 22/npm 12 clean `npm ci`, full plugin tests, validation/package checks;
14. baseline consistency;
15. `git diff --check`;
16. clean final worktree;
17. zero diff under `plugins/cogentnexus-openclaw/**` relative to Task-085 base.

If a regression fails, do not publish PASS.

---

# Live preservation proof

Before report publication, read-only verify there was no live mutation by Task 086.

Expected live state remains:

- controller PASSTHROUGH generation 13;
- manifest -> prior `g-5593cbcfff5b35d5`;
- active disabled replacement -> `g-7257c4555ca8ad21`;
- startup disabled;
- Supervisor absent;
- AGENTS managed markers absent;
- Gateway/Ollama remain healthy if inspected;
- SQLite integrity remains accepted with zero Tickets/outbox;
- zero semantic/provider activity.

Do not normalize state.

---

# Publication fence

If source/tests changed:

1. publish one bounded implementation commit;
2. implementation commit must not include coordination report;
3. publish one report-only commit afterward containing only:

`docs/operations/coordination/reports/CNX-20260827-086-fix-production-pending-rollover-gate-nesting.md`

Report must record:

- execution HEAD;
- implementation HEAD;
- exact production diff;
- RED evidence against Task-085 implementation;
- GREEN AST/control-flow evidence;
- action truth table;
- namespace/security/atomicity regressions;
- full verification;
- plugin-payload zero diff;
- live mutation accounting;
- publication fence.

## Result tokens

Use exactly one:

- `PASS_PENDING_ROLLOVER_PRODUCTION_GATE_REPAIRED`
- `BLOCKED_PRODUCTION_AST_ORCHESTRATION_UNPROVEN`
- `BLOCKED_CLASSIFICATION_OR_ROLLOVER_REGRESSION`
- `BLOCKED_PLUGIN_PAYLOAD_PRESERVATION`
- `BLOCKED_TEST_OR_VALIDATION_FAILURE`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Successor gate

Only an independently accepted:

`PASS_PENDING_ROLLOVER_PRODUCTION_GATE_REPAIRED`

may authorize the next live recovery task.

That successor must use the exact accepted implementation source and one supported installer invocation against the preserved Task-083 two-generation topology to:

- complete pending attested rollover without npm-pack/plugin install and without a third generation;
- restore MANAGED/startup/Supervisor/AGENTS;
- prove source/live skill and plugin parity;
- prove ownership/runtime/Gateway/Ollama/SQLite health;
- observe at least five natural PT1M no-flash ticks;
- prove Dashboard/WebChat authenticated owner-surface readiness without sending a semantic message.

Final semantic acceptance remains a separate later task with exactly one fresh authenticated Dashboard/WebChat owner message.
