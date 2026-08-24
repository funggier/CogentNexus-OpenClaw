# Active Coordination Task

Status: `AWAITING_HUMAN_AUTHORIZATION`  
Execution mode: `HUMAN_GATE`  
Task ID: `PENDING-CNX-20260824-046`  
Updated: 2026-08-24 14:57 ICT  
Owner: ChatGPT  
Executor: Codex only after explicit operator authorization

## Completed predecessor

[`reports/CNX-20260824-045-live-windows-clean-reinstall-acceptance.md`](reports/CNX-20260824-045-live-windows-clean-reinstall-acceptance.md)

[`reviews/CNX-20260824-045-live-windows-clean-reinstall-acceptance.md`](reviews/CNX-20260824-045-live-windows-clean-reinstall-acceptance.md)

Task 045 is reviewed `ACCEPT_SAFE_PREMUTATION_STOP` with result `BLOCKED_LEGACY_MIGRATION_NOT_AUTHORIZED`.

## Proven live state

The live machine contains a managed legacy CogentNexus installation:

- `cnx.cmd`;
- `skills\cogentnexus`;
- `.cogent`;
- controller mode `managed`;
- desired provider `running`;
- generation `32`.

Exact CogentNexus-OpenClaw v0.9.3 launcher, skill, state root, and direct plugin paths are absent.

Task 045 performed zero destructive invocations and changed no live state.

## Pending human gate

The recommended proposed Task 046 is one bounded live migration/install-over only:

1. revalidate Task 045 legacy hashes and current managed state;
2. resolve the read-only `openclaw plugins list --json` timeout without mutation or stop;
3. create and verify the reviewed external migration backup;
4. use the exact legacy launcher to enter PASSTHROUGH/native OpenClaw;
5. run one v0.9.3 install-over migration from isolated reviewed source;
6. remove only proven legacy plugin/config/load-path identities;
7. exact-verify the new `cnxclaw.cmd`, skill, state root, ownership manifest, plugin, Gateway/Ollama integration, scheduler/service, and unrelated-data sentinels;
8. stop for review after migration; do not run clean reinstall in Task 046.

This migration is destructive and is **not authorized yet**.

## Safety

Until explicit approval:

- no legacy disable/migration/install/uninstall/config/plugin/task/service mutation;
- no clean reinstall, reset, deletion, retry, or automatic restore;
- no primary-repository checkout/reset/clean/worktree action;
- no Procmon or Task 027/038 evidence access;
- no CogentNexus-HermesAgent, Ecosystem, staged-capability-loop, merge, tag, Release, or archive action;
- scheduled ChatGPT/Codex execution remains operator-controlled.
