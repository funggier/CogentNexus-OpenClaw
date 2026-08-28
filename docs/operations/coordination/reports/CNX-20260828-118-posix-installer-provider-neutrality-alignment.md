# CNX-20260828-118 — POSIX Installer Provider-Neutrality Alignment

## Verdict

**PASS — source/test/CI/package repair complete.**

Task 118 was source/test/CI/package only. No live Windows or POSIX installation, lifecycle mutation, Task-116 replay, runtime/provider change, cleanup, or credential access was performed.

## RED

Tests-only RED commit: `94ae5edfe2f39feae8b16d57beca3585dd7d76dd`

On the unchanged POSIX installer, the provider-neutral boundary suite failed exactly as expected:

```text
4 failed in 0.05s
```

The failures proved real `scripts/install.sh` coupling: `PROVIDER="ollama"`, `--provider` usage/parser/validation, direct Ollama prerequisite, provider-specific messages, provider-specific lifecycle handoff, and missing provider-free canonical invocation contract.

## Production repair

Production repair commit: `9dfa979e745dbbfeb3e5ea1a584f5285d4fb1852`

Changed files:

- `scripts/install.sh`
- `docs/V093_RECOVERY_REALITY_TESTS.md`
- `tests/test_posix_provider_neutral_installer_boundary.py`
- `tests/test_v091_install_wiring.py`
- `tests/test_namespace_install_contract.py`

The POSIX installer now:

- has no provider variable/default or `--provider` installation API;
- does not validate/select a provider;
- does not require `ollama`, `lmstudio`, or another provider executable merely to install;
- emits provider-neutral installation/success messages;
- uses generic `enable` without a provider argument;
- documents the provider-free canonical command:
  `./scripts/install.sh --workspace "$HOME/.openclaw/workspace"`.

The accepted Task-117 PowerShell repair remains intact. Provider selection remains runtime/configuration responsibility; no provider support was broadened.

## Boundary proof

Both current installers now share the same responsibility boundary:

- `scripts/install.ps1` has no installer-level provider API, prerequisite, provider-specific output, or provider-bearing enable handoff;
- `scripts/install.sh` has no installer-level provider API, prerequisite, provider-specific output, or provider-bearing enable handoff.

Runtime provider policy remains in the provider-aware runtime modules and was not changed.

## Validation

- Focused provider-neutral and related suite: `26 passed`
- Full Python suite: `480 passed, 3 skipped, 4 subtests passed`
- POSIX syntax: `sh -n scripts/install.sh` passed
- Python compileall: passed
- `git diff --check`: passed
- Plugin tests: `50` files passed, `268` tests passed
- Evaluation: `passed: true`
- `npm audit --omit=dev`: `found 0 vulnerabilities`
- Plugin validation: passed, `178` packed files

## Exact candidate CI

Exact candidate SHA: `9dfa979e745dbbfeb3e5ea1a584f5285d4fb1852`

Authoritative exact-SHA workflow results:

- Validate `33183765987`: `completed / success`
- Windows Installer Pack Smoke `33183765981`: `completed / success`
- PS5.1 Acceptance Smoke `33183765948`: `completed / success`

## Package proof

- Artifact ID: `9690806882`
- Artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-9dfa979e745dbbfeb3e5ea1a584f5285d4fb1852`
- Source commit: `9dfa979e745dbbfeb3e5ea1a584f5285d4fb1852`
- Package version: `0.9.3`
- Payload file count: `178`
- Payload V2 fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- tar.gz SHA256: `36aa72044deca5c43154877e318373f9c8640b10c4a18f45bd8412de067c2052`
- ZIP SHA256: `3f8079dea63bd1d66051d50652f133ab098f3cbe45b1e52187659da367a1b34f`

`PACKAGE_IDENTITY.json`, `PAYLOAD_IDENTITY.json`, and `SHA256SUMS.txt` agree. The payload fingerprint remains unchanged because this repair is outside the plugin payload.

## Candidate-to-report fence

The candidate was frozen and validated before report publication. The report is published as a separate report-only commit; its candidate-to-report diff contains exactly this report path and no source/test/package drift.

## Remaining live work

The Task-116 real-Windows lifecycle remains failed at its original pre-body PowerShell parameter-binding boundary. A future lifecycle acceptance retry requires independent review of Task 118 and a new explicit authorization. It must begin with fresh read-only reconciliation and must not replay Task 116 automatically.
