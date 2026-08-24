# Review — CNX-20260824-045

Decision: `ACCEPT`  
Disposition: `ACCEPT_SAFE_PREMUTATION_STOP`  
Reviewer: ChatGPT  
Reviewed report: [`reports/CNX-20260824-045-live-windows-clean-reinstall-acceptance.md`](../reports/CNX-20260824-045-live-windows-clean-reinstall-acceptance.md)  
Result accepted: `BLOCKED_LEGACY_MIGRATION_NOT_AUTHORIZED`

## Accepted evidence

Task 045 correctly stopped at its mandatory pre-mutation gate.

The live classifier ran from the isolated reviewed source and returned:

- mode: `legacy`;
- legacy mode: `managed`;
- evidence: legacy skill metadata, controller structure, and launcher content;
- exact legacy artifacts: `cnx.cmd`, `skills\cogentnexus`, and `.cogent`;
- exact v0.9.3 CogentNexus-OpenClaw artifacts: absent.

The controller remained `managed`, desired provider `running`, generation `32`.

The report also retained exact precondition hashes for the legacy launcher, skill metadata, controller, OpenClaw config, and AGENTS policy. These hashes should be used as the starting evidence for any separately authorized migration.

## Independent publication and safety check

Compared with fetched Task 045 start HEAD `0e3083332663d3e39d664d9e80ee81b5241f8177`, the branch was ahead by exactly one commit and the only changed path was:

`docs/operations/coordination/reports/CNX-20260824-045-live-windows-clean-reinstall-acceptance.md`

No executable source drift or unrelated publication was found.

The following safety outcomes are accepted:

- destructive invocation count: `0`;
- clean reinstall, install, uninstall, migration, reset, cleanup, restore, and retry were not run;
- no backup was created because mutation never began;
- primary repository remained on `master` with unchanged pre-existing status;
- Gateway and Ollama were inspected read-only and remained running;
- HermesAgent, unrelated OpenClaw data/projects/plugins, Ollama models/data, Ecosystem, staged-capability-loop, Procmon, and Task 027/038 evidence were not touched.

## Non-blocking uncertainty retained

`openclaw plugins list --json` timed out twice, so native plugin-list JSON is not accepted as proof. This does not weaken the mandatory stop because the filesystem/controller/launcher classifier already proved a managed legacy source. A future migration task must resolve or safely work around that read-only inventory timeout before plugin/config mutation.

## Root cause and next boundary

This is not a Task 044 repository defect. The authorization/state mismatch is exact:

- Task 045 authorized clean reinstall only from a coherent v0.9.3 `upgrade`;
- the live machine still contains managed legacy CogentNexus;
- migration from the legacy namespace was explicitly excluded.

The clean-reinstall authority must not be reused for legacy migration.

## Recommended next task

Recommended sequence:

1. separately authorize one bounded live legacy MANAGED-to-PASSTHROUGH migration/install-over to CogentNexus-OpenClaw v0.9.3;
2. require external migration backup, legacy hash recheck, native handoff, exact legacy plugin/config/load-path removal, new manifest/plugin verification, and unrelated-data proof;
3. stop after verified v0.9.3 migration and review the report;
4. authorize the clean-reinstall acceptance again as a later task.

Combining migration and clean reinstall in one task would perform two destructive lifecycle transitions before review and is not recommended.

Human decision required: **YES**
