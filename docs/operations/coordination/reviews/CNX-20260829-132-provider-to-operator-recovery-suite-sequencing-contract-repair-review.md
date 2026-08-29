# Independent Review — CNX-20260829-132 Provider-to-Operator Recovery Suite Sequencing Contract Repair

## Verdict

**REJECTED CANDIDATE ADVANCEMENT — THE SEQUENCING REPAIR DIRECTION AND TDD ORDER ARE ACCEPTED, BUT TASK 132 DOES NOT YET SATISFY ITS OWN REQUIRED BEHAVIORAL NEGATIVE-CASE MATRIX, AND THE PUBLISHED ARTIFACT DIGEST DOES NOT MATCH GITHUB'S EXACT-SHA ARTIFACT METADATA. COMPLETE A REPOSITORY-ONLY PROOF CLOSEOUT BEFORE ANY NEW LIVE RECOVERY ACCEPTANCE.**

## Scope reviewed

Task-132 activation HEAD:

`e408bdee5868063bb54193c34d1da69c0f96e30d`

Task-132 report commit:

`b1dcfac5c416806e27e80dc6d41e0719a4b57cad`

Proposed repaired candidate:

`b7074c8cb5b10c77624cfe7b5223e3bae338c80d`

Proposed repaired harness blob:

`8158e4f227e0eafb5c08e89d5f12564e421d460b`

## Accepted findings

### 1. TDD order is valid

The RED commit is tests-only:

`d7a8c02296cd29a924cc298f4fc196f20c51b4c4`

It adds a regression that launches the real Windows PowerShell harness entrypoint with `-ContractSelfTest`. The reported RED is therefore against harness-owned executable behavior rather than a duplicated Python predicate or source-text grep.

The production repair comes later at:

`b7074c8cb5b10c77624cfe7b5223e3bae338c80d`

### 2. The repair is responsibility-local and preserves provider policy

The candidate changes only the recovery harness plus its regression test. `provider_recovery_v092.py` is unchanged. The repair does not treat listener/process recovery as stable model success and does not artificially close provider incidents.

### 3. Carried incident semantics are appropriately narrow in the production predicate

`Scenario-Provider` captures the accepted provider incident only after provider convergence passes. `Scenario-OperatorStop` receives the carried record only when the last scenario is `provider-crash`. `Test-OperatorBoundaryObservation` requires:

- previous scenario exactly `provider-crash`;
- non-null carried evidence;
- exact `READY_WITH_WARNINGS`;
- the existing fail-closed provider-warning convergence predicate;
- exactly one provider-recovery incident row;
- exact incident-ID match;
- classification match when carried;
- healthy managed/Ollama structural state from the underlying predicate.

The carried expectation is cleared before the operator lifecycle proceeds, and post-operator-start still calls ordinary `Wait-DurableConvergence` without the provider-incident exception.

### 4. Exact-SHA CI exists and is green

GitHub reports exactly four push workflow runs on candidate `b7074c8c...`, all successful:

- Validate `33234315933`;
- PS5.1 v0.9.3 Ollama Recovery V3 Smoke `33234315938`;
- PS5.1 Acceptance Smoke `33234315948`;
- Windows Installer Pack Smoke `33234315959`.

The dedicated recovery workflow therefore did run on the exact candidate SHA.

### 5. Exact package contents are coherent

Validate artifact `9709442638` is named:

`cogentnexus-openclaw-v0.9.3-package-proof-b7074c8cb5b10c77624cfe7b5223e3bae338c80d`

Independent inspection of the downloaded artifact confirms `PACKAGE_IDENTITY.json` contains:

- `sourceCommit = b7074c8cb5b10c77624cfe7b5223e3bae338c80d`;
- package version `0.9.3`;
- payload count `178`;
- payload fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- tar.gz SHA256 `0b510eb4b5380483c58b0207b94551a32d6e1a98407d7c79e995787cc7768c9b`;
- ZIP SHA256 `0f22081734b67e6e724a6067a19cd1ba1016983eab0c4aa21643fb35e6c091be`.

## Blocking finding 1 — required behavioral matrix is incomplete

Task 132 Phase D explicitly requires the harness-owned self-test/regression proof to cover, at minimum, fifteen behavioral cases. The final self-test adds positive carried-incident coverage and several useful negatives, but it does not explicitly exercise all mandatory cases.

The following required cases are not independently exercised as sequence-boundary behavioral cases in the final self-test:

1. Provider event adapter `expected=true` must reject.
2. Host/provider selection mismatch must reject.
3. Gateway listener missing must reject.
4. Ollama listener missing must reject.
5. Post-operator-start must remain strict `READY` and must not inherit the carried provider-warning exception.

The production predicate appears structurally capable of rejecting these conditions, but Task 132 specifically required behavioral proof. Source inspection is not a substitute for the required executable negative-case matrix.

A closeout must add deterministic non-disruptive contract-self-test cases that drive the actual harness-owned predicate/path and demonstrate rejection for each missing case. It should also keep the already-covered cases for different/missing/duplicate incident, circuit open, extra WARN, closed incident, missing/duplicate adapter, and standalone operator boundary.

## Blocking finding 2 — artifact digest in the report is stale/incorrect

Task-132 report publishes:

`package digest: sha256:c5dcbda0858a08362daa3218c2912ddd4a36c259e61a05be28d7b1d4114b104c`

However GitHub Actions metadata for artifact `9709442638` on exact candidate `b7074c8c...` reports outer artifact digest:

`sha256:8cb0370b6ba2c741b31f5c972a8de9ce4cfc488ccbe6042d4d6e1d6535db213c`

Independent SHA256 of the downloaded artifact ZIP matches GitHub:

`8cb0370b6ba2c741b31f5c972a8de9ce4cfc488ccbe6042d4d6e1d6535db213c`

The package contents and inner archive hashes are correct; this is a proof/report identity defect, not package corruption. Nevertheless Task 132 explicitly requires artifact ID/name/digest, so the published exact-package proof is not fully correct as written.

## Safety review

Task 132 reports and repository history show no live recovery/lifecycle execution, provider/model/config mutation, process kill, normalization, Dashboard semantic Send, merge, tag, or release. Preserve that fence.

Task-131 consumed live ledger remains unchanged:

- Task-131 suite `1 / 1` consumed;
- baseline PASS;
- gateway-crash PASS;
- provider-crash PASS;
- operator-stop not reached.

## Required next step

Open a repository-only Task-133 proof closeout. It should:

1. add the missing harness-owned behavioral negative cases without broadening production warning semantics;
2. demonstrate GREEN through the real `-ContractSelfTest` path and focused Python wrapper;
3. run the full established repository validation;
4. obtain a new exact-SHA Recovery V3 Smoke and the other established exact-SHA workflows;
5. obtain a fresh exact-SHA package artifact and publish its **actual GitHub outer artifact digest** separately from inner tar/ZIP hashes;
6. publish a new report and stop for independent review.

Do not open or run another live Windows recovery acceptance until that closeout is independently accepted.
