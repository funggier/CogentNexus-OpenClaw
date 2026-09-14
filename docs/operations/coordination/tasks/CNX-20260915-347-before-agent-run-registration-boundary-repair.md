# CNX-347 — before_agent_run Registration Boundary Repair

- Parent: `CNX-346`
- Branch: `cnx-347-source-investigation`
- Executor: `Hermes`
- Reviewer: `ChatGPT`
- Human final authority: `Operator`
- Execution mode: `V096_REGISTRATION_BOUNDARY_REPAIR`

## Objective

Repair the effective CogentNexus `before_agent_run` registration/execution boundary so an eligible Dashboard OpenAI turn cannot bypass Ticket-first admission and fall directly into native OpenClaw provider dispatch.

The repair target is registration/execution wiring. Do not modify `durableAdmissionEligible` unless new evidence proves that predicate is the failing boundary.

## Evidence baseline

CNX-346 established that the inspected source and installed runtime contain:

- `before_agent_run` admission registration at priority `2000`;
- `ticketFirst` admission before inference;
- Dashboard-aware `durableAdmissionEligible`;
- `preInferenceAdmission=true` and `ticketFirst=true` in the inspected runtime config;
- CNX-344 historical context with canonical Dashboard `sessionKey` and `senderIsOwner=true`;
- successful native OpenAI `gpt-5.6-luna` completion with no durable CogentNexus Ticket lifecycle.

The remaining uncertainty is the effective registration/execution boundary: registration omission/suppression, different effective handler/module, or equivalent wiring divergence.

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

The report must include the exact baseline commit, exact production commit, changed-file list, test commands/results, registration identity/priority evidence, duplicate-owner check, and explicit fence accounting.
