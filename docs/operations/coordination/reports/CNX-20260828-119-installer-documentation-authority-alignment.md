# CNX-20260828-119 — Installer Documentation Authority Alignment

## Verdict

**PASS — canonical installation documentation and test authority aligned.**

Task 119 was documentation/test/CI/package only. No live Windows or POSIX installation, lifecycle mutation, Task-116 replay, runtime/provider change, cleanup, or credential access was performed.

## RED

Tests-only RED commit: `9e4250545ad4d30aca700ee7492ab23eb024fb6c`

The canonical-doc contract suite failed on the Task-118 candidate with exactly:

```text
4 failed in 0.05s
```

Failures proved that `docs/INSTALL.md` and `docs/INSTALL.th.md` still mixed Ollama into general installation requirements, claimed installer-owned provider/Gateway preflight, omitted the canonical POSIX source-install command, and that the existing POSIX command assertion used a coordination task document instead of consumer-facing documentation.

The two later assertion-tightening corrections were test-harness-only: they preserved permitted runtime Ollama statements and narrowed checks to installation sections. The final focused suite passed.

## Documentation/test repair

Docs/test commit: `01d08cd7c82f542c821e3a60f7fffa036efb1d75`

Changed files:

- `docs/INSTALL.md`
- `docs/INSTALL.th.md`
- `tests/test_install_docs_authority.py`
- `tests/test_posix_provider_neutral_installer_boundary.py`

The canonical docs now provide these provider-free source-install commands:

Windows PowerShell:

```powershell
.\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

POSIX:

```sh
./scripts/install.sh --workspace "$HOME/.openclaw/workspace"
```

Installation prerequisites now exclude provider executables. The installer section states that installation owns staging, validation, owned state, bridge/launcher installation, and installation-owned verification; it does not select or preflight a provider. A separate runtime/provider-readiness section retains the accurate current v0.9.3 runtime target (Ollama only) and places executable, endpoint/model, and provider-health concerns in the runtime layer.

The POSIX command test now reads `docs/INSTALL.md`, not coordination task/report/review files. Historical release notes and reports were not rewritten.

## Validation

- Final focused docs/installer suite: `25 passed`
- Full Python suite: `484 passed, 3 skipped, 4 subtests passed`
- `sh -n scripts/install.sh`: passed
- Python compileall: passed
- PowerShell installer AST validation: passed
- `git diff --check`: passed
- Plugin tests: `50` files passed, `268` tests passed
- Evaluation: `passed: true`
- `npm audit --omit=dev`: `found 0 vulnerabilities`
- Plugin validation: passed, `178` packed files

## Exact candidate CI

Exact candidate SHA: `01d08cd7c82f542c821e3a60f7fffa036efb1d75`

Authoritative exact-SHA workflow results:

- Validate `33185349482`: `completed / success`
- Windows Installer Pack Smoke `33185349413`: `completed / success`
- PS5.1 Acceptance Smoke `33185349400`: `completed / success`

## Package proof

- Artifact ID: `9691451156`
- Artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-01d08cd7c82f542c821e3a60f7fffa036efb1d75`
- Source commit: `01d08cd7c82f542c821e3a60f7fffa036efb1d75`
- Package version: `0.9.3`
- Payload file count: `178`
- Payload V2 fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- tar.gz SHA256: `6a14cb665ca6148ce2912970df62027533aef34fb0c871a2e542d1b149e94f31`
- ZIP SHA256: `8e06b186e425170a22bfce06fa3505a7cdac3b097d4bfdc4ccc4d810d502cac1`

`PACKAGE_IDENTITY.json`, `PAYLOAD_IDENTITY.json`, and `SHA256SUMS.txt` agree. The payload fingerprint remains unchanged; this task changes documentation/tests only.

## Candidate-to-report fence

The candidate was frozen and validated before report publication. The report is published as a separate report-only commit. The candidate-to-report diff must contain exactly this report path and no source/test/package drift.

## Remaining live work

Task 116 remains failed at its original pre-body PowerShell parameter-binding boundary. A future real-Windows lifecycle acceptance retry requires independent review of Tasks 117–119 and a new explicit authorization. It must begin with fresh read-only reconciliation and must not replay Task 116 automatically.
