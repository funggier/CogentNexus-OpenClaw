# Coordination Channel Status

Status: `BLOCKED`
State: `CNX364_PATH_BOUND_RUNTIME_PROVENANCE`
Task ID: `CNX-20260915-364`
Parent: `CNX-20260915-363`
Executor: `Hermes`
Reviewer: `ChatGPT`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Base report: `docs/operations/coordination/reports/CNX-20260915-364-path-bound-runtime-provenance-report.md`

## Current position

CNX-360 is stale and no longer the current task. CNX-361 through CNX-364 are historical/preceding task records; CNX-364 remains `BLOCKED` because historical controller-path identity was not proven. The current canonical root is identified, but runtime state must not be normalized by guessing.

## Authorization boundary

Next authorized task: `CNX-365_PATH_BOUND_CONTROLLED_REQUALIFICATION`.

This authority permits creation of the successor task and, only after that task is separately accepted as current authority, its read-only path-bound preflight. No runtime semantic test, Dashboard request, model request, or runtime mutation is authorized yet.

## Hard fences

No Dashboard or model request; no semantic requalification; no enable/start/restart/disable/stop/reinstall; no controller edit; no provider/auth/routing, hook, main, v0.9.5 tag/release, force-push, or history rewrite.
