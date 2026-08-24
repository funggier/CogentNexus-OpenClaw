# Coordination Channel Status

**State:** `READY_FOR_CODEX`  
**Updated:** 2026-08-24 19:32 ICT  
**Transport:** GitHub repository history  
**Human authority:** operator authorized install-over as a real acceptance test  
**Execution trigger:** manual only; scheduled execution remains disabled by operator

## Task 051 disposition

Task `CNX-20260824-051` is reviewed:

`ACCEPT_CANONICAL_CHECK_HELP_ALIGNED`

Implementation commit `6d90025f832bb36c477176809a0af2e6c1858c19` changes only the two CLI help/usage surfaces, namespace lint, and focused tests.

Accepted evidence:

- canonical-help RED reproduced;
- minimal GREEN passed;
- lint RED/GREEN passed;
- final focused suite: 6 passed;
- final full suite: 252 passed, 1 skip, 4 subtests;
- namespace/baseline/compile/diff validation passed;
- no live side effect.

## Active Task 052

[`tasks/CNX-20260824-052-live-install-over-v093-acceptance.md`](tasks/CNX-20260824-052-live-install-over-v093-acceptance.md)

Goal: perform one supported install-over update of the coherent live v0.9.3 installation and use it as a full upgrade acceptance test.

## Exact invocation

`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "C:\Users\CDQ-P\.openclaw\workspace"`

The exact child PID and exit code must be retained through a no-timeout process object. PASS requires one observed exit `0`.

## Required preservation

- coherent classifier `mode=upgrade` before and after;
- ownership manifest/plugin exact verification;
- Task 051 help files installed exactly;
- durable Ticket/workflow/session/policy state not reset;
- AGENTS one canonical block and exact 7,196-byte stripped baseline;
- one canonical plugin/scheduler, no legacy;
- MANAGED/Ollama/Gateway healthy;
- same 71 unrelated plugins and four models;
- Task 049 backup and excluded systems unchanged;
- no installer/lifecycle orphan.

## Retry and failure fence

No clean reinstall, migration, fresh install, custom flags, second installer, manual installed-file edit, manual partial completion, automatic restore, force-kill, or broad cleanup.

An alive child must be observed, not duplicated. Nonzero/unobserved exit or any preservation/runtime failure requires a report and stop.

## Exclusions

No destructive recovery test, reset/uninstall, OpenClaw upgrade/reinstall, manual SQLite/config edit, Ollama/model mutation, primary-repository Git mutation, HermesAgent, Ecosystem, staged-capability-loop, Procmon/Task 027/038, merge, tag, GitHub Release, or archive publication.

Report meaningful progress approximately every 3 minutes and after preflight, PASSTHROUGH, skill/plugin/ownership, exit capture, corrected-help, state comparison, runtime, and publication.
