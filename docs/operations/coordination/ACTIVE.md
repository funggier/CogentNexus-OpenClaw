# Active Coordination Task

Status: `READY_FOR_HERMES`
State: `V096_REGISTRATION_BOUNDARY_REPAIR`
Execution mode: `V096_REGISTRATION_BOUNDARY_REPAIR`
Task ID: `CNX-347`
Parent: `CNX-346`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`
Active branch: `cnx-347-source-investigation`
Task commit: `037ebf976e0558dc0baf9689b240c320043a626c`

## Objective

Repair the effective CogentNexus `before_agent_run` registration/execution boundary so an eligible Dashboard OpenAI turn cannot bypass Ticket-first admission and fall directly into native OpenClaw provider dispatch.

The repair target is registration/execution wiring. Do not modify `durableAdmissionEligible` unless new evidence proves that predicate is the failing boundary.

## Hard fences

- Do not modify `v0.9.5` tag or published history.
- No force-push/history rewrite.
- Do not rerun or resend CNX-344.
- No live semantic request during diagnosis or repair.
- No UI interaction unless a later explicitly authorized requalification task requires it.
- No provider/model/config/controller/database mutation for this task.
- No install/reinstall/restart until code-level tests and reviewer approval explicitly authorize a later qualification stage.
- No fallback/manual provider dispatch.

## TDD contract

1. Inspect the exact release-entry registration chain from `v091-release-entry.ts` through `v091-final-entry.ts`, `v090-final-entry.ts`, and the canonical admission registration in `index.ts`.
2. Inspect existing wiring/registration tests, especially `v091-wiring.test.ts`, `index.test.ts`, and any tests asserting `before_agent_run` registration.
3. Add a RED regression test that exercises the canonical release-entry registration path and proves the admission handler is effectively registered exactly once with priority `2000` when `preInferenceAdmission=true`.
4. The RED test must also prove that the effective registration preserves `ticketFirst` behavior and cannot silently omit the admission handler because of wrapper/proxy/release-entry composition.
5. Run only the focused regression test and record the intended failure.
6. Implement the smallest production change that makes the RED test pass. Do not introduce a second independent admission path.
7. Run the focused regression suite and verify exactly one canonical admission owner/registration remains.
8. Run the complete test suite.
9. Run plugin build and schema/validation checks.
10. Confirm no unrelated files, provider semantics, timeout semantics, or v0.9.5 history changed.
11. Publish a CNX-347 report documenting root cause, exact changed files, RED evidence, GREEN evidence, full-suite/build results, and remaining live qualification requirement.
12. Stop for independent ChatGPT review. Do not self-accept.

## Required invariants

- Canonical admission hook: `before_agent_run`.
- Priority: `2000`.
- Exactly one effective CogentNexus admission owner for this hook.
- `preInferenceAdmission=true` must activate the handler.
- `ticketFirst=true` must remain effective through the registration wrappers.
- Dashboard/OpenAI eligible requests must enter the same admission path used by the successful CNX-343 Ollama path.
- `durableAdmissionEligible` semantics remain unchanged unless explicitly justified by new evidence.

## Required report

Publish:
`docs/operations/coordination/reports/CNX-20260915-347-before-agent-run-registration-boundary-repair-report.md`

Stop for independent ChatGPT review after publishing the report.
