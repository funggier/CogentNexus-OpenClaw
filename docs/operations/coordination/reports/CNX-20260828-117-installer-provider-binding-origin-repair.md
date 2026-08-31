# CNX-20260828-117 — Installer Provider-Binding Origin Repair

## Verdict

**PASS — source/test/CI/package boundary repair complete.**

This task was source/test/CI/package only. No live Windows lifecycle mutation was performed and Task 116's failed install-over was not replayed. Real-Windows acceptance remains separate work requiring independent review and a new explicit authorization.

## Task-116 failure boundary and deepest proven origin

The preserved Task-116 installer output proves that PowerShell parameter binding reached the installer `Provider` parameter with the value `3D Objects` and failed its `ValidateSet("ollama")` validation:

```text
Cannot validate argument on parameter 'Provider'. The argument "3D Objects" does not belong to the set "ollama" specified by the ValidateSet attribute.
```

The deepest proven origin is therefore **the installer parameter-binding boundary**. The preserved evidence does not prove whether the value entered through positional arguments, splatting, a wrapper, or another caller-level construction. No stronger caller-origin claim is made.

Preserved evidence used:

- Task-116 report: `docs/operations/coordination/reports/CNX-20260828-116-v093-real-windows-lifecycle-acceptance-final-candidate.md`
- Task-116 evidence root: `C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw-Acceptance-Evidence\CNX-20260828-116\20260828-210020`
- `a01-readonly-probes.txt`
- `c01-post-failure-readonly.txt`
- pinned artifact identity and archive material

## RED

Tests-only RED commit: `21f83753b6a94b31ecf98c60448c201756aebbd9`

The new provider-neutral boundary tests initially reported:

```text
3 failed, 1 passed
```

The failures covered the installer provider parameter/default/validation surface, provider-specific prerequisite/output coupling, and documentation still instructing callers to pass `-Provider ollama`.

## Repair

Production repair commit: `f079e4b2cde3dc9ed71fd873420274d9bd29b3a7`

Changed files:

- `scripts/install.ps1`
- `docs/INSTALL.md`
- `docs/INSTALL.th.md`
- `docs/V093_RECOVERY_REALITY_TESTS.md`
- `docs/V093_OLLAMA_ONLY.md`

The installer no longer exposes an installer-level `Provider` parameter or `ValidateSet("ollama")`, no longer requires Ollama as an installation prerequisite, no longer emits provider-specific installation coupling, and invokes the runtime's generic `enable` path. Documentation now presents the provider-neutral workspace install command. Provider selection remains owned by runtime/configuration policy, where it is actually required.

The test authority assertion was updated in separate commit `2a519904ce6f2ea22caa943529dc4710ccf7214c` to verify the generic owned-runtime enable path rather than the retired provider argument.

## Validation

- Provider-neutral focused/related suite: `28 passed`
- Full Python suite: `476 passed, 3 skipped, 4 subtests passed`
- Installer lifecycle AST analysis: passed
- `git diff --check`: passed
- Plugin tests: `50` files passed, `268` tests passed
- Evaluation: `passed: true`
- `npm audit --omit=dev`: `found 0 vulnerabilities`
- Plugin validation: passed, `178` packed files

## Exact candidate and CI

Exact candidate SHA: `2a519904ce6f2ea22caa943529dc4710ccf7214c`

Authoritative exact-SHA workflow results:

- Validate `33181958320`: `completed / success`
- Windows Installer Pack Smoke `33181958289`: `completed / success`
- PS5.1 Acceptance Smoke `33181958294`: `completed / success`

## Package proof

- Artifact ID: `9690067077`
- Artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-2a519904ce6f2ea22caa943529dc4710ccf7214c`
- Source commit: `2a519904ce6f2ea22caa943529dc4710ccf7214c`
- Package version: `0.9.3`
- Payload file count: `178`
- Payload V2 fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- tar.gz SHA256: `e9e0a6e6eb44168f0f823100a46a607bdbdaed2ef5ab189d43c87379343d5fd6`
- ZIP SHA256: `b0a00dff78e6e6ad6a439a4eb00059e67ce18eae1e92182efd09a72ebeb17b1e`

Package identity, payload identity, and `SHA256SUMS.txt` agree. The payload fingerprint remains unchanged from the independently reviewed Task-115 candidate because this repair is outside the plugin payload.

## Candidate-to-report proof

The report is intentionally published as a separate report-only commit after freezing and validating candidate `2a519904ce6f2ea22caa943529dc4710ccf7214c`. The candidate-to-report comparison must contain exactly this report path and no source/test/package drift.

## Remaining live work

Task 116 remains failed at the original installer parameter-binding boundary. A future real-Windows acceptance task may use the repaired candidate only after independent review and fresh read-only-first authorization. It must not replay the failed Task-116 lifecycle automatically.
