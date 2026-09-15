# CNX-20260915-361 — Rollover canonical-mode repair

Status: `READY_FOR_HERMES`
Parent: `CNX-20260915-360`
Executor: `Hermes`
Reviewer: `ChatGPT`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Objective

Repair the plugin generation rollover ownership boundary so it accepts the repository's canonical disabled/PASSTHROUGH state without weakening fail-closed ownership checks.

## Exact CNX-360 failure

Fresh exact candidate activation failed at `plugin-rollover-prepare` with:

```text
RuntimeError: plugin generation rollover requires PASSTHROUGH mode; observed None
```

CNX-360 proved candidate source checkout, package build/validation, supported installer invocation, and that activation did not reach the installed candidate. Runtime ended with `cnxMode=disabled`, `mode=passthrough`, generation `102`, plugin disabled/status disabled. No Dashboard request occurred.

## Root-cause hypothesis

`CANONICAL_MODE_SCHEMA_MISMATCH_AT_ROLLOVER_BOUNDARY`: `scripts/install.ps1` translates canonical `cnxMode=disabled` to legacy `mode=passthrough`, but `skills/cogentnexus-openclaw/scripts/namespace_ownership.py::_require_passthrough()` reads only `controller.get("mode")` and can reject a valid canonical disabled controller.

## Affected boundary

`namespace_ownership.py::_require_passthrough()` and its plugin generation rollover callers, especially `plugin-rollover-prepare`.

## Hard fences

- Do not modify `main`, tag `v0.9.5`, release, force-push, or rewrite history.
- Do not manually repair runtime state.
- Do not retry the failed CNX-360 installer before offline source repair validation.
- Do not run Dashboard or send `CNX359-DONE`/`CNX360-DONE`.
- Do not weaken/remove `_require_passthrough()` or accept unknown/missing modes.
- Do not bundle unrelated canonical-mode consumer repairs.
- After successful repaired activation, stop before Dashboard and hand the one-shot UI action to Operator.
- If activation fails, stop without retry and preserve exact failure evidence.

## TDD plan

1. Identify existing mode/ownership/rollover tests and canonical mode helper semantics.
2. Add the smallest focused RED test: controller with `cnxMode=disabled` and no legacy `mode`, calling `_require_passthrough()`, must currently fail at the existing implementation boundary.
3. Run and retain exact RED output; confirm it is a product assertion failure, not a harness/dependency error.
4. Implement the smallest source repair, reusing the existing canonical interpretation helper where applicable. Accept only `cnxMode=disabled` or legacy `mode=passthrough`; reject active/managed, maintenance, unknown, missing, and malformed states.
5. Run focused GREEN and regression tests, relevant installer tests, plugin suite, TypeScript build if affected, Python suite, and `npm run plugin:validate`.
6. Perform a repository-wide static comparison of direct `controller["mode"]`/`controller.get("mode")` consumers against `cnxMode` consumers. Document additional mismatches separately; do not repair unrelated consumers.
7. Only after offline validation, build a fresh exact candidate and record source SHA, package SHA, contents/fingerprint. Perform the supported activation lifecycle exactly once and prove source → package → installed artifact → active runtime identity.

## Acceptance criteria

- RED proves the canonical-mode mismatch at `_require_passthrough()`.
- GREEN accepts canonical `cnxMode=disabled` as PASSTHROUGH.
- Legacy `mode=passthrough` remains accepted.
- `cnxMode=active`, `cnxMode=maintenance`, managed/maintenance legacy modes, missing, unknown, and malformed controller state remain rejected fail-closed.
- Focused, ownership, installer, plugin, build, validation, and relevant Python tests pass, with exact results recorded.
- Static consumer consistency check is recorded without unrelated changes.
- Fresh repaired candidate identity is recorded and exact activation either proves source/package/installed/runtime identity or stops on the first failure without retry.
- No Dashboard semantic PASS is claimed in CNX-361.

## Required final report fields

Branch; exact commit SHA; RED/GREEN/regression evidence; root-cause statement; changed paths; source/package/installed artifact identity; activation evidence; static consistency findings; remaining proof gap.
