# Independent Review — CNX-20260904-245

## Verdict

`ACCEPT_FAIL_INSTALLER_TERMINAL__MANIFEST_BINDING_AND_ONE_SHOT_EXECUTION_PROVEN__ROLLOVER_PREPARE_EXACT_EXCEPTION_UNPROVEN__READ_ONLY_FORENSIC_REQUIRED_BEFORE_ANY_RETRY`

## Reviewed authority

- Report HEAD: `5984e3dfe3503bee37c218cb1f34eff16a071bef`
- Exact executable candidate: `18a51b15768fb3d2196e65f1ef470c34aeef7f36`
- Candidate plugin fingerprint: `1ff69c459517b6ea0bd35bf6e21fed0bb2f21f716168653fecad4160b1babb5f`
- Parent Task 244: `CNX-20260904-244`
- Parent umbrella: `CNX-20260831-188`

## Accepted findings

Task 245 closes the prior scheduler/action-binding uncertainty. The frozen manifest and runner were qualified and rehashed before start. The decoded child vector contained exactly one `-File` and bound it to the detached exact-candidate `scripts/install.ps1`.

The live installer execution cardinality is accepted as:

```text
installer Scheduled Task registrations = 1
installer Scheduled Task starts = 1
installer child invocations = 1
installer retries after start = 0
manual installer invocations = 0
```

The hardened runner and Task Scheduler agreed on terminal exit `1`. Captured installer stages prove `ticket-db-bootstrap` and `plugin-npm-pack` completed with exit `0`, followed by entry into `plugin-rollover-prepare`, then terminal failure.

No semantic operation, recovery replay, direct Discord/API send, manual plugin repair, manual rollover action, manual lifecycle normalization, or manual durable-state mutation occurred.

## Source-level narrowing

At exact candidate `18a51b15768fb3d2196e65f1ef470c34aeef7f36`, `scripts/install.ps1` invokes:

```text
namespace_ownership.py rollover-prepare
```

and writes the rollover transaction only after the Python command returns success.

The Python CLI likewise calls `prepare_plugin_rollover_transaction(...)` first and only then atomically writes the requested transaction JSON. Therefore Task 245's combination of:

```text
plugin-rollover-prepare entered
child exit = 1
no new rollover transaction JSON
```

proves the failure occurred before successful return from `prepare_plugin_rollover_transaction()` or during an exception raised inside it.

The exact function's pre-transaction path includes, in order:

1. passthrough proof;
2. ownership manifest verification;
3. retired plugin payload proof;
4. expected replacement fingerprint validation;
5. external application-data boundary validation;
6. backup-token validation;
7. retired storage-root resolution;
8. backup destination validation;
9. backup directory creation / `copytree`;
10. retired project-tree hash;
11. backup project-tree hash;
12. project-tree equality assertion.

The report's bounded traceback is insufficient to select one of these exact invariants. No more specific production root cause is accepted yet.

## Important backup distinction

Task 245 observed a new workspace backup:

`C:/Users/CDQ-P/.openclaw/workspace/.cogentnexus-openclaw/install-backups/cogentnexus-openclaw-20260904-195413`

That path belongs to the normal installer/skill backup boundary. It is not the rollover prepare boundary, which is external application-data under `plugin-generation-rollover-backups`. The workspace backup therefore does not prove that rollover `copytree` completed and must not be used as a substitute for rollover backup evidence.

## Preserved live boundary

Accepted post-failure state:

```text
controller = passthrough
generation = 39
provider = ollama
installed plugin fingerprint = e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386
plugin status = disabled
candidate installed = false
```

Gateway/provider/model/storage/recovery/delivery remained healthy. Candidate installation, rollover finalization, and managed convergence were not achieved.

## CI / repository provenance

The Task-245 report commit is coordination-only relative to the Task-245 authority head. Report-head Actions are all SUCCESS:

- Validate `33876070613`
- Windows Installer Pack Smoke `33876070664`
- PS5.1 Acceptance Smoke `33876070529`

No report-head product/source/test/workflow drift is accepted.

## Required successor

Before any installer retry, execute a separate read-only forensic task that:

1. immediately preserves Task-245 raw runner artifacts from `%LOCALAPPDATA%/Temp` byte-identically to a non-temp forensic evidence root, recording before/after SHA-256;
2. captures the complete raw `child-stderr.txt`, relevant `child-stdout.txt`, transcript, runner result, launch manifest, and frozen runner identity;
3. inventories external `plugin-generation-rollover-backups` with creation/write times around the Task-245 execution and distinguishes all historical Task-223/237 artifacts;
4. inventories `install-staging` for any Task-245 transaction or temporary transaction residue;
5. if a new rollover backup exists, hashes the exact backup tree and current retired storage tree without modifying either and records their path-level differences if any;
6. determines whether the exact traceback/error string identifies a specific invariant in `prepare_plugin_rollover_transaction()`;
7. distinguishes the workspace `install-backups/...195413` skill backup from rollover-generation backup evidence;
8. leaves plugin, controller, Gateway, DB, Ticket/outbox/recovery, and historical evidence unchanged.

No installer, rollover prepare/finalize, semantic send, or recovery replay is authorized by this review.
