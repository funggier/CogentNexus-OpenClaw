# CNX-20260829-126 — Provider-Crash Recovery Convergence Root-Cause Repair

## Verdict

**PASS — repository-side harness contract repaired; no live Windows lifecycle or recovery replay performed.**

Task-125 retained evidence proves that the provider process recovered coherently but the recovery incident intentionally remained open pending stable model-success evidence. The recovery check therefore remained `READY_WITH_WARNINGS`, while the v3 acceptance harness required exact `READY`. This made the provider-crash convergence predicate unsatisfiable during the observed state, independent of the 420-second fuse.

The smallest repair is in the acceptance harness only: `READY_WITH_WARNINGS` is accepted for the provider-crash convergence path when the incident is present and its circuit is closed. Gateway-crash convergence remains strict `READY`. Provider recovery policy was not weakened and no listener/process-health state is treated as stable model success.

## Authoritative retained evidence

- Task-125 log: `C:\Users\CDQ-P\Downloads\CNXCLAW_V093_OLLAMA_RECOVERY_V3_20260829-062300.txt`
- Task-125 JSON: `C:\Users\CDQ-P\Downloads\CNXCLAW_V093_OLLAMA_RECOVERY_V3_20260829-062300.json`
- Task-125 exact candidate: `01d08cd7c82f542c821e3a60f7fffa036efb1d75`
- Task-125 harness blob: `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`

## Evidence-derived predicate analysis

The retained `converge-provider-after` series contains **90 observations** across **420.652 seconds**:

- First observation: `2026-08-29T06:25:08.3260911+07:00`
- Last observation: `2026-08-29T06:32:04.4353846+07:00`
- `mode`: `managed` throughout
- host selected provider: `ollama` throughout
- provider selected provider: `ollama` throughout
- recovery verdict: `READY_WITH_WARNINGS` throughout
- Gateway: listener `true`, PID `16228` throughout the convergence series
- Ollama: listener `true`, PID `14476` throughout the convergence series
- Provider event adapter: one row, `status=PASS`, `details.expected=false` throughout
- Provider recovery incident: one row, `status=WARN`, `incidentOpen=true`, `circuitOpen=false`, incident `ollama:1`, `recoveryAttempts=1` throughout

There was no change-point from `READY_WITH_WARNINGS` to `READY`. The only unsatisfied harness requirement was the exact `recoveryVerdict == READY` check. All process/listener, selection, adapter, and circuit predicates were coherent.

The incident's recorded automatic recovery attempt had `success=true` and reason `provider-failure-event-recovery`. It remained open because the product policy closes it on stable model success or verified operator transition, not merely on process/listener recovery. No stable model completion occurred before the harness entered convergence polling.

Answers to the required diagnosis questions:

- Ollama listener recovered before/during convergence and was present for all 90 observations.
- Gateway remained healthy and listening for all 90 observations.
- Provider selection remained `ollama`.
- The incident was singular, open, and circuit-closed; it was not duplicated, circuit-open, or malformed.
- The provider event adapter was coherent with `expected=false`.
- The recovery verdict was blocked by the WARN incident check, represented by the harness as `providerRecoveryIncident`.
- The system did not become `READY` during the 420-second window; harness cleanup later restored healthy managed state, but that cleanup state is not used as evidence for the failed window.

## Source authority trace

- `skills/cogentnexus-openclaw/scripts/provider_recovery_v092.py`: an automatic provider restart records an attempt but does not close the incident; stable model success or verified operator transition closes it.
- `skills/cogentnexus-openclaw/scripts/checks_v092.py`: an open circuit-closed provider incident is `WARN`; the aggregate verdict becomes `READY_WITH_WARNINGS`.
- `scripts/test-v093-ollama-recovery-windows-v3.ps1::Wait-DurableConvergence`: previously required exact `READY` while `Scenario-Provider` also required a present circuit-closed incident.

The owning defect was therefore the acceptance-harness contract, not provider recovery state management.

## TDD evidence

### RED

Against parent candidate `5643e3daacdf89380ab1879a6a345fe1bab367a0`, the focused regression test was added first and run:

```text
pytest -q tests/test_recovery_harness_contract.py
1 failed, 1 passed
```

The failure was the expected missing provider-crash warning-state acceptance contract.

### GREEN

After the minimal harness change and scope refinement:

```text
pytest -q tests/test_recovery_harness_contract.py
2 passed

PYTHONPATH=. pytest -q
486 passed, 3 skipped, 4 subtests passed
```

The final implementation scopes warning acceptance only to `$RequireProviderIncident`; the gateway-crash path remains exact-`READY`.

## Changed source and test

- `scripts/test-v093-ollama-recovery-windows-v3.ps1`
  - provider-crash convergence accepts `READY` or `READY_WITH_WARNINGS` only when the required incident is present and circuit-closed;
  - gateway-crash convergence remains exact `READY`.
- `tests/test_recovery_harness_contract.py`
  - regression coverage for the evidence-derived open-incident warning state.

Repair commits:

- Initial candidate repair: `14d5d1e006303c98006bbb1401fdff9324c1c793`
- Final scoped refinement: `69a3efa1feb7711f22c83055a8571035240ec81c`

Final candidate: `69a3efa1feb7711f22c83055a8571035240ec81c`

## Validation

Local validation:

- focused regression: `2 passed`
- full Python suite: `486 passed, 3 skipped, 4 subtests passed`
- plugin tests: `50 files, 268 tests passed`
- plugin validation: PASS; 45 config properties, 5 tools
- package payload validation: PASS; 178 files
- evaluation: `passed: true`
- PowerShell harness syntax/load: PASS
- Python compileall: PASS
- POSIX installer syntax: PASS
- `git diff --check`: PASS

Root-level `npm audit --omit=dev` reported two existing high-severity advisories with no available fix. The authoritative CI audit step passed under the repository's established contract; no unrelated dependency change was made.

## Exact-SHA CI

All required workflows passed for final SHA `69a3efa1feb7711f22c83055a8571035240ec81c`:

- Validate: run `33223319908`, conclusion `success`
- Windows Installer Pack Smoke: run `33223319175`, conclusion `success`
- PS5.1 Acceptance Smoke: run `33223319261`, conclusion `success`

Validate completed all seven jobs, including Windows 3.11 and Windows 3.14.

## Package proof

- Artifact ID: `9705965930`
- Artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-69a3efa1feb7711f22c83055a8571035240ec81c`
- Artifact uploaded ZIP digest: `25a877a828e06e78542d790ff2b76314119406d0f06ecc46672767f66f718c41`
- Package version: `0.9.3`
- Payload count: `178`
- Payload/plugin fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- tar.gz SHA256: `516d248dab1143537cc1531d11e92fddaef15112e856f7261605f1e36c91485d`
- ZIP SHA256: `43371d03b4f38fd0c9a9358cdbac629a292ef56e47eda4e5e2fefc63ecfd716d`

## Safety boundary

- No live Windows lifecycle command was run by Task 126.
- No provider crash or recovery suite was replayed.
- No install, reset, uninstall, reinstall, stop, start, or restart was run.
- No live provider/OpenClaw configuration or model state was changed.
- No process was killed, no reboot occurred, and no manual cleanup/normalization occurred.
- No credentials, secrets, or Dashboard semantic Send were accessed/performed.
- No merge, tag, release publication, or force push occurred.

The next live recovery acceptance, if authorized, must use this exact final candidate and a new coordination task. This task does not authorize opening or executing it.
