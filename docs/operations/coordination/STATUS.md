# Coordination Channel Status

**State:** `READY_FOR_HERMES`  
**Execution mode:** `DOCS_TEST_CONTRACT_REPAIR`  
**Updated:** 2026-08-28 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator authorized continued stabilization; Task 119 authorizes documentation/test/CI/package alignment only  
**Execution trigger:** manual Hermes/Codex continuation; scheduled execution remains disabled

## Active work

Task:

[`tasks/CNX-20260828-119-installer-documentation-authority-alignment.md`](tasks/CNX-20260828-119-installer-documentation-authority-alignment.md)

Task ID:

`CNX-20260828-119`

## Task 118 independent review

Task-118 report:

`docs/operations/coordination/reports/CNX-20260828-118-posix-installer-provider-neutrality-alignment.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-118-posix-installer-provider-neutrality-alignment-review.md`

Verdict:

`REJECTED FOR CANDIDATE ADVANCEMENT — CODE REPAIR ACCEPTED; CANONICAL INSTALL DOCUMENTATION/AUTHORITY REMAINS INCONSISTENT`

Task 118 successfully removed provider policy from the POSIX installer. Together with Task 117, both current installer entry points are now provider-neutral and delegate provider policy to runtime/configuration layers.

The review found the remaining blocker in current documentation/test authority rather than installer implementation:

- canonical install docs still list Ollama as a general install requirement;
- installer behavior text still claims provider preflight;
- canonical POSIX source-install command is absent from user-facing install guidance;
- the POSIX install-command regression assertion reads a coordination task document instead of canonical consumer docs.

## Task 119 documentation-authority gate

Task 119 must make user-facing installation guidance describe the same responsibility boundary as implementation.

Required result:

- provider-free canonical PowerShell source-install command;
- provider-free canonical POSIX source-install command;
- no installer-level `-Provider`/`--provider` guidance;
- clear separation of installer prerequisites from runtime/provider readiness requirements;
- no claim that provider selection/provider-specific preflight is installer-owned;
- accurate current runtime provider support retained in runtime/post-install context;
- automated tests protect canonical user-facing docs, not coordination task files;
- no installer source change unless a new implementation defect is demonstrated.

Required order:

`fresh reconcile -> TESTS-ONLY canonical-doc RED -> minimal docs/test alignment -> GREEN -> focused/full validation -> exact candidate CI/package proof -> report`

## Live mutation fence

Task 119 does not authorize any live lifecycle mutation:

- no Task-116 install-over replay;
- no reset/uninstall/reinstall;
- no live POSIX install;
- no live stop/start/restart or recovery harness;
- no manual cleanup/normalization;
- no OpenClaw/provider-runtime changes;
- no provider/model/endpoint/timeout changes;
- no live SQLite/manifest/plugin/session mutation;
- no credential/secret access;
- no Dashboard semantic Send.

The latest authoritative live-machine boundary remains Task 116 post-failure coherent state.

## Required output

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-119-installer-documentation-authority-alignment.md`

After publishing, stop for independent ChatGPT review. A new real-Windows lifecycle retry may be opened only after Task 119 passes independent review on a newly frozen exact candidate.
