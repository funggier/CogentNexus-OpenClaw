# CNX-20260829-133 — Recovery Sequencing Behavioral Matrix and Package-Proof Closeout

- Status: `READY_FOR_HERMES`
- Execution mode: `REPOSITORY_SOURCE_TDD_REPAIR`
- Owner / independent reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-29 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Close the two proof defects identified by the independent Task-132 review before any further live recovery acceptance:

1. complete the executable harness-owned behavioral negative-case matrix required by Task 132;
2. produce a fresh exact-SHA package proof whose GitHub **outer artifact digest** is published correctly and separately from inner tar/ZIP hashes.

Task 133 is repository/test/CI/package work only. It does not authorize any live Windows recovery or lifecycle operation.

## Authoritative prior review

Task-132 report:

`docs/operations/coordination/reports/CNX-20260829-132-provider-to-operator-recovery-suite-sequencing-contract-repair.md`

Task-132 independent review:

`docs/operations/coordination/reviews/CNX-20260829-132-provider-to-operator-recovery-suite-sequencing-contract-repair-review.md`

Review verdict:

`REJECTED CANDIDATE ADVANCEMENT — THE SEQUENCING REPAIR DIRECTION AND TDD ORDER ARE ACCEPTED, BUT TASK 132 DOES NOT YET SATISFY ITS OWN REQUIRED BEHAVIORAL NEGATIVE-CASE MATRIX, AND THE PUBLISHED ARTIFACT DIGEST DOES NOT MATCH GITHUB'S EXACT-SHA ARTIFACT METADATA. COMPLETE A REPOSITORY-ONLY PROOF CLOSEOUT BEFORE ANY NEW LIVE RECOVERY ACCEPTANCE.`

Task-132 proposed candidate is therefore **not yet accepted for live advancement**:

`b7074c8cb5b10c77624cfe7b5223e3bae338c80d`

Task-132 repaired harness blob:

`8158e4f227e0eafb5c08e89d5f12564e421d460b`

## Accepted Task-132 facts — do not rediscover or undo

The following are accepted:

- tests-only RED commit `d7a8c02296cd29a924cc298f4fc196f20c51b4c4` predates the harness repair;
- RED invokes the real Windows PowerShell harness with `-ContractSelfTest`;
- sequencing repair is responsibility-local and does not weaken provider recovery policy;
- provider listener/process recovery is not treated as stable model completion;
- provider-crash may carry only the exact accepted open/circuit-closed provider incident into an immediately following operator boundary;
- standalone operator-stop remains strict;
- carried incident identity is matched by exact incident ID and classification when available;
- carried state is cleared before operator lifecycle proceeds;
- post-start convergence uses ordinary `Wait-DurableConvergence` without the provider-warning exception;
- exact-SHA candidate `b7074c8c...` had four successful workflows;
- its package contents were coherent.

Do not broaden provider-warning semantics and do not rewrite the product recovery policy.

## Proof defect A — missing executable behavioral cases

Task 132 Phase D required the harness-owned self-test/regression path to exercise a fail-closed matrix. The current candidate does not explicitly exercise all required cases.

Task 133 must add deterministic, non-disruptive cases through the **actual harness-owned `-ContractSelfTest` path** for at least the following missing conditions:

1. provider event adapter row with `expected=true` => reject;
2. host selected provider not `ollama` => reject;
3. provider-status selected provider not `ollama` => reject;
4. Gateway listener missing/not listening => reject;
5. Ollama listener missing/not listening => reject;
6. after the carried provider→operator boundary has been accepted/consumed, ordinary/post-operator-start convergence with `READY_WITH_WARNINGS` must still reject; only strict ordinary `READY` may pass.

Keep and re-run the existing sequence cases:

- exact carried incident => accept;
- standalone same open incident without carried expectation => reject;
- different incident ID => reject;
- missing incident => reject;
- duplicate incident => reject;
- circuit open => reject;
- extra WARN => reject;
- incident closed/PASS paired with `READY_WITH_WARNINGS` => reject;
- adapter missing => reject;
- adapter duplicate => reject;
- ordinary exact READY => accept.

If adding these executable cases reveals a production predicate defect, fix only the smallest harness-local defect and document it. If the existing predicate already behaves correctly, change only the harness self-test/test surface needed to prove it.

A source grep, `Contains`, regex, duplicated Python predicate, or reasoning from code does not satisfy this gate.

## TDD / proof discipline

Because Task 132 already contains the production sequencing repair, Task 133 is primarily a proof closeout.

1. Fresh-fetch coordination and confirm Task 133 is authoritative.
2. Add the missing behavioral expectations first.
3. Demonstrate failure against the pre-closeout harness if the new expectations are not yet represented/executed by the self-test. A missing expected self-test marker/case may establish proof-surface RED only when the actual PowerShell harness is invoked; do not use source text as the RED.
4. Add the minimal harness-owned self-test support and, only if needed, minimal production predicate correction.
5. GREEN must execute `powershell.exe ... -ContractSelfTest` and `tests/test_recovery_harness_contract.py`.

Do not alter runtime/provider policy merely to create a convenient test surface.

## Package-proof defect B — digest identity

For Task-132 artifact `9709442638`, GitHub Actions metadata and independent download both show outer artifact digest:

`sha256:8cb0370b6ba2c741b31f5c972a8de9ce4cfc488ccbe6042d4d6e1d6535db213c`

The Task-132 report incorrectly published the older value `sha256:c5dcbda0...`.

Task 133 must produce a **new fresh exact-SHA artifact** after its final candidate is pushed. Report these as distinct fields:

- artifact ID;
- artifact name;
- GitHub outer artifact digest from Actions metadata;
- independently downloaded artifact SHA256 when practical, and require it to match the GitHub outer digest;
- `PACKAGE_IDENTITY.json` source commit;
- package version;
- payload count;
- payload fingerprint;
- inner tar.gz SHA256;
- inner ZIP SHA256.

Never reuse an outer artifact digest from an older candidate.

## Required validation

At minimum:

- Windows PowerShell 5.1 parse/load of the harness;
- harness `-ContractSelfTest` GREEN with all required sequence/mismatch/listener/adapter/post-start cases;
- `tests/test_recovery_harness_contract.py` GREEN;
- full Python suite;
- relevant provider/recovery/check focused tests;
- `python -m compileall -q .`;
- `bash -n scripts/install.sh` where applicable;
- `git diff --check`;
- plugin tests;
- plugin validation/package payload validation;
- evaluation suite;
- `npm audit` under the established repository contract, recording pre-existing findings accurately rather than using a forced breaking fix.

No live recovery/lifecycle test is allowed.

## Exact-SHA CI requirement

The final Task-133 candidate must have successful exact-SHA push runs for all four established candidate workflows:

- Validate;
- PS5.1 v0.9.3 Ollama Recovery V3 Smoke;
- PS5.1 Acceptance Smoke;
- Windows Installer Pack Smoke.

The Recovery V3 Smoke must execute the real non-disruptive PowerShell `-ContractSelfTest` path on the exact candidate SHA.

If any required workflow is absent, not exact-SHA, or not successful, verdict is `BLOCKED`.

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260829-133-recovery-sequencing-behavioral-matrix-and-package-proof-closeout.md`

The report must include:

- exact Task-133 start HEAD;
- prior Task-132 candidate and review blockers;
- RED/proof-surface commit and output;
- final changed files/commits;
- complete executable behavioral matrix and observed results;
- statement whether production predicate semantics changed or only self-test proof expanded;
- full validation results;
- exact final candidate SHA;
- exact final harness Git blob;
- all four exact-SHA workflow IDs/conclusions;
- fresh artifact ID/name/**outer digest**;
- independently verified downloaded artifact SHA256 if available;
- PACKAGE_IDENTITY source SHA/version/count/fingerprint;
- inner ZIP/tar hashes;
- explicit statement that no live recovery/lifecycle/provider/config/Dashboard action occurred;
- verdict `PASS`, `FAIL`, or `BLOCKED`.

Then STOP for independent ChatGPT review. Do not open a live recovery task automatically.

## Historical live ledger

Remain consumed/closed:

- Task-121 install-over `1 / 1`;
- Task-124 reset/uninstall/fresh reinstall/standalone stop/start/restart `1 / 1` each;
- Task-125 old-harness recovery suite `1 / 1`;
- Task-128 suite `0 / 1`, closed blocked;
- Task-131 suite `1 / 1` consumed;
- Task-131 gateway-crash PASS;
- Task-131 provider-crash PASS;
- Task-131 operator-stop `0`, not reached.

Task 133 authorizes **zero live operations**.

## Hard fence

Forbidden:

- live recovery suite or crash injection;
- install/install-over/reset/uninstall/reinstall;
- live `cnxclaw` start/stop/restart/enable/disable;
- live provider/model/OpenClaw/config mutation;
- process kill;
- scheduled-task/service run/change;
- manual cleanup/normalization;
- reboot;
- credential/secret access;
- Dashboard semantic Send;
- merge/tag/release;
- force push.

Final Dashboard durable-delivery acceptance remains prohibited until a later repaired exact candidate passes a separately authorized real-Windows recovery acceptance and independent review.
