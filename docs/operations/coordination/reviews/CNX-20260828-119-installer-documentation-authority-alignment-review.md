# Independent Review — CNX-20260828-119 Installer Documentation Authority Alignment

## Verdict

`ACCEPTED PASS — CANONICAL INSTALL CONTRACT ALIGNED; EXACT CANDIDATE MAY ADVANCE TO A NEW READ-ONLY-FIRST REAL-WINDOWS LIFECYCLE ACCEPTANCE TASK`

Task 119 closes the documentation/test-authority blocker left by Task 118. The exact candidate `01d08cd7c82f542c821e3a60f7fffa036efb1d75` is accepted for a separately authorized real-Windows lifecycle retry.

## Review findings

The Task-119 sequence is materially valid:

- tests-only RED commit: `9e4250545ad4d30aca700ee7492ab23eb024fb6c`;
- docs/test repair candidate: `01d08cd7c82f542c821e3a60f7fffa036efb1d75`;
- the RED targeted canonical consumer docs rather than coordination files;
- `docs/INSTALL.md` and `docs/INSTALL.th.md` now remove provider executables from installer prerequisites;
- both canonical provider-free source-install commands are documented;
- installer-owned work is separated from runtime/provider readiness;
- current runtime provider support remains documented only in runtime/post-install context;
- the POSIX command authority test now reads `docs/INSTALL.md` rather than a coordination task;
- no installer source/runtime/provider implementation change was made in Task 119;
- the accepted Task-117/118 provider-neutral installer implementation remains intact.

The initial RED was intentionally broader than the final section-scoped contract in places. The candidate tightens those assertions so permitted runtime/provider documentation is not incorrectly forbidden while installation sections remain protected. This is a valid test-harness correction and does not conceal an implementation regression.

## Exact candidate proof

Accepted candidate:

`01d08cd7c82f542c821e3a60f7fffa036efb1d75`

Exact-SHA workflows independently verified:

- Validate `33185349482`: `completed / success`;
- Windows Installer Pack Smoke `33185349413`: `completed / success`;
- PS5.1 Acceptance Smoke `33185349400`: `completed / success`.

Package proof:

- artifact ID `9691451156`;
- artifact name `cogentnexus-openclaw-v0.9.3-package-proof-01d08cd7c82f542c821e3a60f7fffa036efb1d75`;
- GitHub artifact digest `sha256:9db9290e14646575586a42160b79cfea691e35f3a0ca7d294f7f941dcae0c87a`;
- package ZIP SHA256 `8e06b186e425170a22bfce06fa3505a7cdac3b097d4bfdc4ccc4d810d502cac1`;
- package tar.gz SHA256 `6a14cb665ca6148ce2912970df62027533aef34fb0c871a2e542d1b149e94f31`;
- payload file count `178`;
- payload V2 fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`.

GitHub artifact metadata binds the artifact to the exact candidate SHA.

## Candidate/report fence

The candidate-to-report comparison from `01d08cd7c82f542c821e3a60f7fffa036efb1d75` to Task-119 report commit `46b7beabbf71867eba3ff0f1b92c2f2fecca64c3` contains exactly one added file:

`docs/operations/coordination/reports/CNX-20260828-119-installer-documentation-authority-alignment.md`

No source/test/package drift occurred after candidate freeze.

## Advancement authorization boundary

This review authorizes opening a **new** lifecycle acceptance task only. It does not itself authorize replaying Task 116.

The new live task must:

1. pin the exact candidate/artifact above;
2. begin from fresh read-only machine reconciliation;
3. independently classify the current interrupted-reentry/ownership state before mutation;
4. use the provider-neutral installer command with no `-Provider` argument;
5. stop on the first non-zero exit or ambiguous state;
6. never replay a completed disruptive phase;
7. preserve external OpenClaw/provider runtime/data and unrelated namespaces;
8. keep Dashboard semantic delivery out of scope until lifecycle acceptance passes independent review.

Task 116 remains historical failure evidence, not an instruction to resume from its mutation step.
