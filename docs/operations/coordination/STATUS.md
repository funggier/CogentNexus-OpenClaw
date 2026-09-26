# Coordination Status

Status: `ACTIVE`
State: `CNX453_FOLLOWUP_LOCAL_GREEN_CI_PENDING`
Task: `CNX-20260926-453-scheduled-supervisor-direct-lease-fence.md`
Branch: `cnx-453-supervisor-direct-lease-fence`
Executor: `ChatGPT`
Baseline release: `v0.9.8` (immutable)
Baseline SHA: `09eec4113b371d39334d90a332fa9a6455530db0`
First CNX-453 candidate: `21176b07ad98ada944612d444fe5e2d9a8ee0d2b`
GitHub issue: `#45`

## Physical qualification status

`21176b07...` passed exact-SHA CI 3/3 and physical install-over. Installed Host files match source, Supervisor is `PT15M` + `IgnoreNew`, Gateway is healthy, and controller is MANAGED generation 40.

Physical DB inspection found one remaining stale-session boundary gap: an old session that is intentionally ineligible for resume can still retain an active pre-boundary model-call / canonical inference-attempt. The follow-up repair settles that execution evidence without authorizing stale-session resume.

## Validation

- focused follow-up: `2/2 PASS`;
- CNX-453 Host regressions: `33/33 PASS`;
- Python: `754 passed, 5 skipped, 38 subtests passed`;
- Vitest: `95 files / 444 tests PASS`;
- build/evaluation/plugin validation/audit/diff-check/skill validation: PASS;
- evaluation evidence SHA-256: `48e3dc446018c96cc4dcff6d888d06eb281a5e525b0526b2c8cce90c5a1f8d6f`.

Persistent User `OLLAMA_KEEP_ALIVE=6h`; controlled Ollama restart is deferred until durable Direct state is clean.

## Current classification

`CNX453_FOLLOWUP_LOCAL_GREEN_CI_PENDING`
