# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `CNX360_RUNTIME_ACTIVATION_VERIFICATION`
Execution mode: `SUPPORTED_RUNTIME_ACTIVATION_OBSERVATION_ONLY`
Task ID: `CNX-20260915-360`
Parent: `CNX-20260915-359`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Candidate source commit: `1aa7b37c23e2bb2abdd150a893f1f37102731089`

## Objective

Prove `SOURCE COMMIT -> PACKAGE -> INSTALLED ARTIFACT -> ACTIVE RUNTIME` for the CNX-359 diagnostic candidate before any new Dashboard request.

## Hard fences

No Dashboard control or request; no reuse of `CNX359-DONE`; no provider/auth/routing or admission-semantic changes; no `main`, `v0.9.5` tag/release, force-push, or history rewrite. Use only the supported installer and lifecycle. Observational checks must not perform model inference.

## Authority

`docs/operations/coordination/tasks/CNX-20260915-360-runtime-activation-verification.md`
