# CNX-20260824-045 — Live Windows Clean-Reinstall Acceptance

Status: **BLOCKED**  
Result: `BLOCKED_LEGACY_MIGRATION_NOT_AUTHORIZED`  
Fetched start HEAD: `0e3083332663d3e39d664d9e80ee81b5241f8177`  
Repository: `C:\Users\CDQ-P\AppData\Local\Temp\cnx045-clone-20260824T062333Z`  
Branch: `agent/v0.9.3-recovery-reality-tests`  
Preflight UTC: `2026-08-24T06:24:08.7010267Z`

## Duplicate, source, and collision fence

- No matching Task 045 report existed at fetched HEAD.
- A new isolated full clone was created under `%LOCALAPPDATA%\Temp`; no Git worktree was created.
- `git merge-base --is-ancestor 4c825f8ec1ed6b43a419ad52e0bb85cee28007c1 HEAD` returned exit `0`.
- `git diff --name-only 4c825f8ec1ed6b43a419ad52e0bb85cee28007c1..HEAD -- . ':(exclude)docs/operations/coordination/**'` returned no paths. Executable/install/test source has not drifted from the reviewed implementation.
- A read-only Win32 process command-line collision scan found `0` active install/reset/uninstall/migration/clean-reinstall commands.
- The primary repository remained on `master`; its pre-existing untracked status was recorded and was identical after preflight. No checkout/reset/clean/prune/worktree action was run there.
- The existing scheduled identity `CogentNexus Supervisor` was `Ready`; it was inspected only and not changed.

## Read-only environment and boundary evidence

- Windows: `Microsoft Windows NT 10.0.19045.0`
- Windows PowerShell: `5.1.19041.6456`
- Python: `3.14.6`
- Node: `v24.18.0`
- npm: `11.16.0`
- OpenClaw: `2026.7.1-2 (0790d9f)`
- Ollama: `0.32.13`
- C: free space: `109272649728` bytes of `499435945984` bytes.
- Default backup boundary validation exited `0`: active app data `C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw`; backup root `C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw-Clean-Reinstall-Backups`; boundary `external`.
- Neither active application-data root nor default backup root existed before or after preflight.

Gateway status exited `0`: runtime running, PID `27560`, Gateway/CLI version `2026.7.1-2`, loopback port `18789`, connectivity probe `ok`, capability `connected-no-operator-scope`.

Ollama `ps` and `list` exited `0`. `qwen3.5:9b` was active; installed models listed were `qwen3.5:9b`, `muse-glimmer:30b`, `qwen3.6:27b`, and `qwen3.8:27b`. No model/provider action occurred.

## Mandatory ownership gate

Executed from the isolated reviewed source:

`python skills/cogentnexus-openclaw/scripts/namespace_ownership.py classify-install --workspace C:\Users\CDQ-P\.openclaw\workspace --app-data C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw`

Exit: `0`. Exact result:

- `mode`: `legacy`
- `legacyMode`: `managed`
- evidence: `legacy-skill-metadata`, `legacy-controller-structure`, `legacy-launcher-content`
- legacy artifacts: `cnx.cmd`, `skills\cogentnexus`, `.cogent`
- current/new artifacts: none

The controller summary was `mode=managed`, `desiredProvider=running`, `generation=32`. Exact v0.9.3 paths `cnxclaw.cmd`, `skills\cogentnexus-openclaw`, `.cogentnexus-openclaw`, and the direct `cogentnexus-openclaw` extension were absent.

OpenClaw npm projects included `openclaw-plugin-cogentnexus-rotation` and its generation wrapper, independently corroborating the legacy installation. `openclaw plugins list --json` was attempted read-only twice and timed out after 24 and 49 seconds respectively (tool exit `124`), so native plugin-list JSON remains unproved. No retry with mutation or alternate config access was attempted.

### Immutable pre-mutation hashes

- `cnx.cmd`: length `172`; SHA-256 `0B2EB63FD725236BC6B8F9616307F2B454C4FEBE0BF46CE4DE68F32A9C61B637`
- legacy `SKILL.md`: length `5111`; SHA-256 `5F5136F0F280D4B00C8EF8CF75198BB8844C642CDF249E8A8C8ED63F90AF8C41`
- legacy controller: length `433`; SHA-256 `F173EFE6EEE6D4E826B5CAF127614BD9AFE292AAE8CC8261EA3A3E0EE2129E5F`
- OpenClaw config: length `5300`; SHA-256 `F2A541DBDFDB8CDD08C1F4693734BF65763F0136804EEB19CA98C06A2BC1656A`
- workspace `AGENTS.md`: length `8878`; SHA-256 `C9BFD0288A379D62BD4C43B5B782AAFE0CFCAE43651B48EB5794780609B7DBBE`

## Stop, actions not executed, and side effects

The Task 045 mandatory gate states that a `legacy` classification must stop as `BLOCKED_LEGACY_MIGRATION_NOT_AUTHORIZED`. Therefore:

- destructive invocation count: **0**;
- `scripts/clean-reinstall.ps1` was not invoked;
- no PASSTHROUGH handoff was attempted;
- no backup directory or recovery record was created;
- no plugin/config/task/service mutation occurred;
- no install, uninstall, migration, clean reinstall, reset, cleanup, deletion, restore, or retry occurred;
- no launcher/skill/state/application-data path was created, removed, or changed;
- Gateway and Ollama were read only and remained running;
- CogentNexus-HermesAgent, unrelated OpenClaw projects/user data, Ollama data, CogentNexus-Ecosystem, staged-capability-loop, Procmon and retained Task 027/038 evidence were not touched;
- the primary repository was read only and retained the same branch/status.

Because mutation never began, Phase 2 and Phase 3 backup/post-install acceptance are not applicable and remain unproved.

## Problem classification and next action

Blocker type: authorization/state mismatch, not a Task 044 repository defect. The live machine contains a managed legacy CogentNexus installation, while Task 045 authorizes only an exact coherent v0.9.3 `upgrade` classification and explicitly prohibits legacy migration.

Narrow safe option: ChatGPT should review this evidence and publish a separately authorized legacy MANAGED-to-PASSTHROUGH migration task with exact backup, legacy plugin/config/load-path removal, rollback, duplicate, and unrelated-data gates. Do not reuse Task 045 clean-reinstall authority for that migration.

Recommended option: authorize the narrowly scoped legacy migration and subsequent exact v0.9.3 verification as a new task; retain the hashes and managed generation above as its precondition evidence.

Human decision required: **YES** — authorize or decline a new bounded live legacy-migration task. No destructive action should occur until that decision is recorded in coordination.

## Commands and exit codes

- fresh clone/fetch/source ancestry and non-coordination drift checks — exit `0`.
- process collision scan — exit `0`, count `0`.
- version, disk, path, primary-repository, hash, controller, npm-project, scheduler, Gateway, and Ollama read-only inspections — exit `0`.
- default backup boundary validation — exit `0`.
- live ownership classifier — exit `0`, `legacy/managed`.
- `openclaw plugins list --json` — timed out twice; execution-tool exit `124`; no output accepted as proof.
- authorized clean-reinstall command — **not executed**, count `0`.

Duplicate/external-side-effect accounting: no completed Task 045 report existed; no external side effect was executed or repeated. This report records the mandatory pre-mutation stop only.
