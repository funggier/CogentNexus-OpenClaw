# CNX-20260824-038 — Validate Operator-Created Task027 Procmon Configuration

Status: READY
Owner: ChatGPT
Executor: Codex
Execution mode: AUTO
Predecessor: CNX-20260823-037 (reviewed ACCEPT as PASS_ALREADY_CLEAN_NO_TERMINATE)

## Human authorization

The human operator explicitly authorized creation of this proof-only task:

> ได้เลยครับ สร้าง task ให้ codex ได้เลย

This authorizes read-only validation of the operator-created Procmon configuration artifact and publication of the matching Task 038 report.

It does not authorize launching Procmon, loading/importing the configuration, starting capture, touching the target worktree, stimulating filesystem activity, restoring files, changing runtime state, or performing any cleanup or lifecycle action.

## Role split

ChatGPT established the approved configuration fingerprint from:

* operator-provided Procmon screenshots;
* the uploaded PMC artifact;
* the local metadata and SHA256 results supplied by the operator;
* the clean Procmon process and driver poststate supplied by the operator.

Codex performs independent local-machine identity, structure, and clean-poststate proof only.

Codex must not redesign the Procmon configuration or attempt to prove it by launching Procmon.

## Objective

Independently prove that the retained operator-created PMC file is byte-identical to the configuration artifact already reviewed by ChatGPT, confirm its narrow structural indicators, confirm that Procmon remains stopped, and publish a durable evidence report.

This task is validation-only. It must not capture any events.

## Exact identities

Repository:

`funggier/CogentNexus-OpenClaw`

Branch:

`agent/v0.9.3-recovery-reality-tests`

Target worktree identity, reference only:

`C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-027`

Do not access, enumerate, stat, refresh, or touch the target worktree during this task.

Retained Task 035 directory:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx035-procmon\20260823T140738Z`

Exact PMC artifact:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx035-procmon\20260823T140738Z\task027-exact-filesystem-dropfiltered.pmc`

Required size:

`2051 bytes`

Required SHA256:

`61F3BBB57B65F8DC708E66BC15B5B808AB44E9DC770799E8C32ED40724AE6CBC`

Operator-reported timestamps:

* CreationTimeUtc: `2026-08-23T17:06:31Z`
* LastWriteTimeUtc: `2026-08-23T17:06:31Z`

Exact retained Procmon executable, identity reference only:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx035-procmon\20260823T140738Z\extracted\Procmon64.exe`

Do not execute it.

Matching report:

`docs/operations/coordination/reports/CNX-20260824-038-validate-operator-created-task027-procmon-pmc.md`

## Approved configuration fingerprint

ChatGPT reviewed a byte-identical uploaded copy with the required SHA256 and established the following approved configuration:

* exactly one intended include rule;
* Column: `Path`;
* Relation: `begins with`;
* Value:
  `C:\Users\CDQ-P\.openclaw\worktrees\cogentnexus-CNX-20260823-027`
* Action: `Include`;
* `Drop Filtered Events` enabled;
* File System activity enabled;
* Registry activity disabled;
* Network activity disabled;
* Process/Thread activity disabled;
* Profiling activity disabled;
* capture remained disabled before and after export.

Raw artifact inspection also exposed:

* the exact target-path string;
* `FilterRules`;
* `DestructiveFilter` with enabled value;
* disabled Registry, Network, Process, and Profiling indicators.

Local equality with the required size and SHA256 proves byte-for-byte equality with the approved artifact. Codex must distinguish this identity proof from any unsupported claim that Procmon itself loaded the file.

## Duplicate-execution fence

Freshly fetch the branch before any local validation.

If the matching Task 038 report already exists at fetched HEAD:

* do not repeat local inventory;
* do not read the PMC again;
* do not create another report;
* stop awaiting ChatGPT review.

Do not repeat Tasks 035, 036, or 037.

## Authorized read-only validation

Codex may perform only the following:

1. Record the freshly fetched start HEAD.
2. Confirm the exact PMC path exists as a regular file.
3. Read file metadata without changing timestamps or attributes.
4. Compute SHA256.
5. Read raw bytes for bounded structural inspection.
6. Confirm the exact target-path string and expected configuration field names are present.
7. Inventory only Procmon-related processes.
8. Inventory only Procmon/Process Monitor driver and service state.
9. Inventory only the retained Task 035 directory for:

   * the exact expected PMC;
   * `.PML`;
   * `.CSV`;
   * backing/log/capture artifacts;
   * unexpected additional `.PMC` files.
10. Publish exactly the matching Task 038 report.

Permitted examples include `Get-Item`, `Get-FileHash`, bounded `ReadAllBytes`, read-only byte/string inspection, `Get-Process`, and read-only CIM process/driver/service queries.

Do not recursively inspect unrelated directories.

## Identity acceptance gate

Return PASS only when all of the following are proven:

* the exact PMC file exists;
* file length is exactly `2051`;
* SHA256 exactly matches the required hash;
* creation and last-write timestamps match the operator-reported UTC values, or any timestamp formatting difference is fully explained without changing the file;
* bounded raw inspection contains the exact target-path string;
* bounded raw inspection contains configuration indicators consistent with `FilterRules` and `DestructiveFilter`;
* zero Procmon, Procmon64, Procmon64a, or Process Monitor processes exist;
* zero matching Procmon driver/service entries exist;
* no `.PML`, `.CSV`, backing file, or other capture artifact exists;
* no unexpected additional `.PMC` exists in the retained Task 035 directory;
* the validation itself caused no file, process, driver, service, runtime, target, or worktree mutation.

The required size and SHA256 are the authoritative semantic-identity gate. Do not launch Procmon to reinterpret or independently load the file.

## Immediate blockers

If the file is absent, return:

`BLOCKED_PMC_MISSING`

If size or SHA256 differs, return:

`BLOCKED_PMC_IDENTITY_MISMATCH`

If a Procmon process, driver, or service is present, return:

`BLOCKED_PROCMON_RUNTIME_RESIDUAL`

Do not terminate or modify it.

If a `.PML`, `.CSV`, backing file, or other unexpected capture artifact exists, return:

`BLOCKED_UNEXPECTED_CAPTURE_ARTIFACT`

Do not open, delete, move, or overwrite it.

If structural inspection cannot be completed without executing Procmon, report the exact proven fields and return:

`BLOCKED_PMC_STRUCTURE_UNPROVEN`

Do not launch Procmon.

## Report publication fence

The only repository mutation permitted to Codex is:

`docs/operations/coordination/reports/CNX-20260824-038-validate-operator-created-task027-procmon-pmc.md`

Stage and commit exactly that path.

Prohibit:

* `git add .`
* `git add -A`
* `git commit -a`
* deletion
* reset
* clean
* checkout
* restore
* force push

Verify that the report commit changes exactly one path.

Commit message must begin:

`report: CNX-20260824-038`

The report must include:

* fetched start HEAD;
* exact commands used;
* exact PMC path;
* existence and regular-file result;
* length;
* CreationTimeUtc and LastWriteTimeUtc;
* SHA256;
* bounded structural indicators found;
* process inventory;
* driver/service inventory;
* retained-directory artifact inventory;
* acceptance-gate evaluation;
* side-effect accounting;
* remaining uncertainty;
* explicit confirmation that Procmon was not launched and capture was not started;
* `Human decision required: YES|NO`.

Do not commit the PMC, binaries, ZIP, screenshots, hashes as separate files, command-output dumps, or any unrelated evidence.

## Results

Return exactly one:

* `PASS_OPERATOR_PMC_ARTIFACT_VALIDATED`
* `BLOCKED_PMC_MISSING`
* `BLOCKED_PMC_IDENTITY_MISMATCH`
* `BLOCKED_PROCMON_RUNTIME_RESIDUAL`
* `BLOCKED_UNEXPECTED_CAPTURE_ARTIFACT`
* `BLOCKED_PMC_STRUCTURE_UNPROVEN`
* `BLOCKED_REPORT_PUBLICATION_UNSAFE`

A PASS does not authorize capture. Any trace execution requires a new task and separate human authorization.

## Progress communication

Report meaningful progress approximately every 3 minutes and immediately after:

* duplicate fence and start-HEAD verification;
* PMC identity verification;
* bounded structural inspection;
* process/driver/service and capture-artifact poststate;
* publication result or any blocker.

Progress updates are not pause points.

## Prohibited

No Procmon launch, `/LoadConfig`, `/OpenLog`, `/BackingFile`, `/Terminate`, GUI interaction, capture, PML, CSV, backing file, target stimulation, target worktree access, restoration/materialization, Git index refresh, Git worktree repair/removal/registration/prune, watcher/Supervisor/task/config change, process termination, driver/service action, retained-evidence deletion or overwrite, Task 025 execution, CogentNexus/OpenClaw/Ollama runtime/provider/recovery/lifecycle action, force push, merge, tag, or release.
