# Independent Review — CNX-20260829-133 Recovery Sequencing Behavioral Matrix and Package-Proof Closeout

## Verdict

**ACCEPTED PASS — Task 133 closes the remaining Task-132 proof gaps. The provider→operator sequencing exception is now exercised through the real harness-owned PowerShell self-test with the required fail-closed structural negatives, all four required workflows passed on the exact candidate SHA, and the fresh package artifact metadata/identity are coherent. Candidate `1424d6fbee2c458c8c30440616783d2fa1bc1201` may advance to a new separately authorized one-shot real-Windows recovery acceptance.**

## Reviewed authority

- Task-133 start HEAD: `f3e32879ae7700f79bc817fb085f5d0306223d00`
- Task-133 report HEAD: `983706b8cf286c42c64f6e3ec50b052b6b9dd253`
- Exact candidate: `1424d6fbee2c458c8c30440616783d2fa1bc1201`
- Exact repaired harness blob: `a4138e00e2056db89b0a9eceed1b54e001c4e319`

Candidate→report comparison is report-only; no source/runtime drift was introduced after the exact-SHA proof.

## Findings

### 1. TDD/proof order is valid

Tests-only commit `758a6c2228e3fc4e3decd6872c90fd9ee45edfb3` first required the missing real `powershell.exe ... -ContractSelfTest` case markers and produced the expected RED before the harness self-test was expanded.

Harness-only commit `1424d6fbee2c458c8c30440616783d2fa1bc1201` then expanded synthetic observations/self-test cases. It did not weaken provider recovery runtime policy.

### 2. Behavioral matrix is executable, not grep-only

The final harness self-test calls the same `Test-DurableConvergenceObservation` / `Test-OperatorBoundaryObservation` predicates used by the recovery harness. Each case compares the actual predicate result to the expected result and throws before emitting PASS on mismatch.

The closeout now explicitly exercises rejection of:

- adapter `expected=true`;
- host provider mismatch;
- provider-status mismatch;
- missing Gateway listener;
- missing Ollama listener;
- ordinary/post-operator-start `READY_WITH_WARNINGS` leakage.

Existing carried-incident positive/negative cases remain present, including standalone rejection, different/missing incident, extra WARN, wrong verdict, circuit-open/closed/duplicate/missing incident and adapter cases.

### 3. Exception remains sequence-local and fail-closed

The exceptional operator boundary still requires an immediately preceding `provider-crash`, exact carried incident identity, `READY_WITH_WARNINGS`, the reviewed single provider-incident warning shape, managed/Ollama structural health, correct adapter, and healthy listeners.

Ordinary/post-start convergence invokes `Test-DurableConvergenceObservation` with provider-incident allowance disabled and therefore remains strict.

### 4. Exact-SHA CI is complete

For exact candidate `1424d6fbee2c458c8c30440616783d2fa1bc1201`, GitHub records success for:

- Validate — `33235544556`
- PS5.1 v0.9.3 Ollama Recovery V3 Smoke — `33235544569`
- PS5.1 Acceptance Smoke — `33235544559`
- Windows Installer Pack Smoke — `33235544603`

The dedicated recovery smoke runs the real non-disruptive PowerShell contract self-test.

### 5. Fresh package proof is coherent

Fresh Validate artifact:

- artifact ID `9709798190`
- name `cogentnexus-openclaw-v0.9.3-package-proof-1424d6fbee2c458c8c30440616783d2fa1bc1201`
- GitHub outer digest `sha256:e8dbb2f742bfeffc93a80a7cda62a8c273ced9e2b1e9b47a3962dead52ccfeef`
- source commit `1424d6fbee2c458c8c30440616783d2fa1bc1201`
- payload count `178`
- payload/plugin fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- inner tar.gz SHA256 `33be3ccea56bae7926c371d37e46f30dbec39364380b9bb5601e5d9a6e073a9a`
- inner ZIP SHA256 `cfe1c6cfccd298849b0d9c5f0a4603848f27c50c3b579629538616fd72ec81c1`

The outer digest now matches GitHub Actions artifact metadata, closing the stale-digest defect from Task 132.

### 6. Safety boundary was respected

Task 133 performed no live recovery/lifecycle/provider/model/config/process/task/service/Dashboard operation. Historical live ledgers remain unchanged.

## Advancement decision

Task 132/133 repository repair and proof closeout are accepted closed.

Open a **new** one-shot real-Windows recovery acceptance against exact candidate `1424d6fbee2c458c8c30440616783d2fa1bc1201` and harness blob `a4138e00e2056db89b0a9eceed1b54e001c4e319`.

The new live task must preserve the already-established authoritative-root discipline from Tasks 129/130/131, use a true interactive PowerShell PTY, run the exact harness once with fail-stop/no-rerun semantics, and keep Dashboard durable-delivery acceptance closed until the live recovery suite passes and is independently reviewed.
