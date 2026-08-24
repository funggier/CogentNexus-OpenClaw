# Review — CNX-20260824-044

Decision: `ACCEPT`  
Reviewer: ChatGPT  
Reviewed report: [`reports/CNX-20260824-044-repair-install-classifier-and-clean-reinstall-handoff.md`](../reports/CNX-20260824-044-repair-install-classifier-and-clean-reinstall-handoff.md)  
Implementation commit: `4c825f8ec1ed6b43a419ad52e0bb85cee28007c1`

## Accepted implementation

Task 044 repairs the four bounded Task 043 findings:

- product inventory no longer treats every unrelated OpenClaw npm project as CogentNexus-OpenClaw state;
- exact direct/plugin-child/wrapper metadata remains product evidence, including partial, corrupt, old, and conflicting exact product payloads;
- the default clean-reinstall backup is external to the active `%LOCALAPPDATA%\CogentNexus-OpenClaw` application-data root;
- the active application-data root is backed up and removed before the fresh installer classifier runs;
- reinstall failure preserves the default external backup and records `clean-reinstall-recovery.json`;
- skip-plugin is rejected before mutation for fresh and legacy states and is allowed only for a classifier/manifest/plugin-verified coherent upgrade;
- both installers exact-verify the created ownership manifest and installed artifacts/plugin before `enable`.

The implementation commit is a direct child of Task 044 start HEAD `02f22464ed214ca57074519e93ecca211482286c` and changes exactly the eight reported implementation/test paths.

## Independent review evidence

The review inspected the implementation rather than relying only on the report:

- `product_plugin_inventory()` admits only the exact direct extension, exact package child, or exact wrapper/package dependency metadata;
- `classify_install()` still fails closed on mixed/partial product evidence and exact-verifies coherent upgrades;
- `require_skip_plugin_safe()` accepts only `upgrade`, and both installers invoke it before native handoff/copy/init;
- `clean-reinstall.ps1` validates the default external backup boundary, verifies ownership before backup/deletion, removes the active application-data root, and writes recovery accounting when fresh reinstall fails;
- both installers order manifest creation, exact verification, then `enable`;
- behavior tests cover unrelated npm fixtures, exact partial/conflicting payloads, external backup composition, recovery accounting, unknown application-data residue, and skip-plugin classification.

Reported validation is accepted: 248 Python tests passed with one existing platform skip and four subtests; 237 plugin tests passed; lint, baseline, compile/self-tests, PowerShell parser, production audit, and diff checks passed.

## Acceptance boundary and remaining proof

This review accepts repository implementation only.

- No live installation, migration, reset, uninstall, clean reinstall, Gateway, OpenClaw, Ollama, scheduler/service, Procmon, Ecosystem, tag, Release, archive, or merge was performed.
- GitHub returned no pull-request workflow run for implementation commit `4c825f8ec1ed6b43a419ad52e0bb85cee28007c1`; real POSIX-shell validation therefore remains unproved in this review.
- Clean-reinstall acceptance is limited to the reviewed default backup root. A future live task must use the default path and must not substitute an arbitrary custom `-BackupRoot`.
- Live destructive acceptance requires a separate, explicit operator authorization after the exact rollback/backup boundary is presented.

## Disposition

Retain implementation commit `4c825f8ec1ed6b43a419ad52e0bb85cee28007c1`.

Next gate: human authorization for a bounded Windows live clean-reinstall acceptance task using the default external backup path. Until authorized, remain read-only and do not start Codex execution.

Human decision required: **YES**
