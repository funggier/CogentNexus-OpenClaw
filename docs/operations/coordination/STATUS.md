# Coordination Channel Status

**State:** `READY_FOR_CODEX`  
**Updated:** 2026-08-24 19:01 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator authorized Task 050 with response `1`  
**Execution trigger:** manual only; scheduled execution remains disabled by operator

## Task 049 disposition

Task `CNX-20260824-049` is reviewed `ACCEPT_FRESH_WITH_EXPECTED_PREHOST_AGENTS_RESTORE`.

Legacy CogentNexus was externally backed up and removed. The accepted machine boundary is exact `mode=fresh`; the 7,196-byte pre-host `AGENTS.md` baseline is correct and no current product is installed.

## Active Task 050

Task `CNX-20260824-050` is ready for the operator's manual Codex signal:

[`tasks/CNX-20260824-050-fresh-install-current-v093.md`](tasks/CNX-20260824-050-fresh-install-current-v093.md)

Goal: install reviewed CogentNexus-OpenClaw v0.9.3 exactly once from a new isolated clone, then prove exact ownership, canonical namespace, MANAGED/Ollama integration, and preservation.

## Important pre-install review findings

- Required implementation commit: `4c825f8ec1ed6b43a419ad52e0bb85cee28007c1`.
- There is no non-coordination code drift after that implementation commit.
- Fresh classifier and native plugin/task residue checks occur before installer mutation.
- Plugin packaging/installation is non-linked and exact-ID.
- Ownership manifest creation and exact verification occur before MANAGED authority.
- Transactional enable rolls back policy/plugin/scheduler/host state toward PASSTHROUGH/native on activation failure.
- Failure before transactional enable may leave a partial current installation; therefore Task 050 forbids a retry, manual completion, or automatic legacy restore and requires exact partial-state reporting.

## Exact authorized invocation

`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "C:\Users\CDQ-P\.openclaw\workspace"`

No `-SkipPlugin`, `-SkipGatewayRestart`, `-SkipAgentsPolicy`, `-LinkPlugin`, custom provider, clean reinstall, migration, or Release installer.

## Expected success state

- classifier: `mode=upgrade`;
- launcher: `cnxclaw.cmd`;
- skill: `skills\cogentnexus-openclaw`;
- state: `.cogentnexus-openclaw`;
- ownership manifest exact-verified for v0.9.3;
- plugin: exactly one `cogentnexus-openclaw` v0.9.3 payload;
- scheduler: `CogentNexus-OpenClaw-Supervisor`;
- controller: MANAGED;
- provider: Ollama only;
- Gateway/Ollama healthy;
- no legacy aliases/artifacts;
- unrelated data and Task 049 backup preserved.

## Stop gates

Stop and report on source/duplicate/concurrency drift, fresh-baseline drift, native inventory failure, nonzero/unresolved installer outcome, partial namespace, managed-enable rollback, ownership/runtime verification failure, unexplained unrelated drift, or unsafe publication.

Do not retry the installer. An outer-wrapper timeout does not authorize a duplicate invocation; observe the original child/durable state.

## Exclusions

No Task 049 repeat, legacy restore, clean reinstall, second installer, manual partial completion, reset/uninstall, destructive recovery tests, force-kill, broad cleanup, OpenClaw upgrade/reinstall, manual SQLite/config edit, Ollama/model mutation, primary-repository Git mutation, HermesAgent, Ecosystem, staged-capability-loop, Procmon/Task 027/038, merge, tag, GitHub Release, or archive publication.

Report meaningful progress approximately every 3 minutes and at every source/fresh/install/plugin/ownership/enable/runtime/publication transition.
