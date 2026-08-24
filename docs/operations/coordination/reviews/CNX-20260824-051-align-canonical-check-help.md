# Review — CNX-20260824-051 Align Canonical Check Help and Usage

Decision: **ACCEPT**

Disposition: `ACCEPT_CANONICAL_CHECK_HELP_ALIGNED`

Reviewed task: `CNX-20260824-051`

Reviewed start HEAD: `1a71acacdfb048c823922ff869e66f2802f23e9f`

Implementation commit: `6d90025f832bb36c477176809a0af2e6c1858c19`

Report commit: `47888a2d72f624396cd09b296492637f518ab722`

Reviewed report:

[`../reports/CNX-20260824-051-align-canonical-check-help.md`](../reports/CNX-20260824-051-align-canonical-check-help.md)

## Publication and scope fences

The Task 051 compare contains exactly two commits:

1. one implementation commit changing exactly five authorized source/test paths;
2. one report-only commit changing exactly the Task 051 report path.

The implementation commit changes:

- `skills/cogentnexus-openclaw/scripts/cnxclaw.py`
- `skills/cogentnexus-openclaw/scripts/cnxclaw_v093.py`
- `scripts/check_namespace_isolation.py`
- `tests/test_canonical_check_help.py`
- `tests/test_namespace_lint.py`

No plugin, installer, provider, lifecycle, controller, manifest, release, or live-machine path changed.

## Root-cause repair

The implementation correctly aligns operator-facing help/usage with the pre-existing canonical check-engine key `cogentnexus-openclaw`.

Independent commit inspection confirms:

- base missing-component usage now advertises `cogentnexus-openclaw`;
- base help now advertises `cogentnexus-openclaw`;
- v0.9.3 help now advertises `cogentnexus-openclaw`;
- no compatibility alias was added;
- generic `cogentnexus` remains rejected by the existing check mapping;
- namespace lint now rejects a complete-token generic check command before migration-literal exceptions;
- historical coordination exclusions remain intact.

## TDD and validation

Accepted TDD evidence:

- canonical-help RED: 2 expected failures and 1 mapping pass before production edits;
- canonical-help GREEN: 3 passed after the minimal correction;
- namespace-lint RED reproduced the migration-exception gap;
- namespace-lint GREEN passed after the command-specific guard;
- final focused suite: 6 passed;
- final full suite: 252 passed, 1 platform skip, 4 subtests passed;
- namespace isolation, baseline consistency, compileall, diff check, and final invalid-command inventory passed.

The initial nine unrelated failures were traced to an in-process test isolation mistake that rebound provider modules. Correcting the test to execute v0.9.3 help in a subprocess is an appropriate test-only fix; no production behavior was changed for it.

## Live boundary and next gate

Task 051 did not touch the installed copy. The live Task 050 installation remains on the prior reviewed source and still contains stale help text, while its canonical check/runtime remains healthy.

The operator has approved using the installed-copy update as a real install-over acceptance test. A successor may invoke the reviewed default installer exactly once from the Task 051 source, provided it first proves coherent `mode=upgrade`, preserves durable state, captures the exact installer exit code, and performs full post-upgrade ownership/help/runtime/preservation checks.

Do not use clean reinstall or edit installed files manually.
