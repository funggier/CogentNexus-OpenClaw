# Single-AI Hybrid E2E Benchmark

This benchmark tests whether one tool-using model can complete a staged,
evidence-backed workflow without CogentNexus orchestration. It is intentionally
small in data volume but demanding in workflow discipline.

For a complete Thai-language test procedure, fairness rules, and result-report
template, see [`TESTING-GUIDE.th.md`](TESTING-GUIDE.th.md).

## Run

1. Give [`PROMPT.md`](PROMPT.md) to the model under test.
2. Set `SUBMISSION_DIR` to an empty directory that the model may write to.
3. After the model stops, validate its output:

```powershell
python validator.py C:\path\to\submission
```

The validator exits with code `0` only when the root gate can be independently
reconstructed from the submitted artifacts. A model-authored claim that the
workflow passed is not sufficient.

Run the validator from the benchmark checkout, not from the submission. It is
benchmark-owned: the model, compiler, and workflow may not replace it with a
generated validator.

Validate the validator itself with a generated known-good fixture and a
deliberately tampered fixture:

```powershell
python test_validator.py
```

## Interpreting the result

Keep these three outcomes separate:

1. **Workflow complete**: the controller reached terminal `completed` after
   running every step in its compiled manifest.
2. **Submission valid**: the independent validator accepted the artifacts in
   the exact `SUBMISSION_DIR` and exited with code `0`.
3. **Root pass**: the submission is valid, the run was unassisted, and the
   model respected the allowed write scope.

A run may be workflow-complete but submission-invalid. That is
`FAIL/INCOMPLETE`, not a partial pass. Controller completion proves the
compiled manifest finished; it does not prove that the compiler captured the
entire benchmark contract.

## Lessons covered by the Qwen 27B run

The Qwen 27B orchestration run exposed a useful false-positive pattern:

- the durable workflow reached `completed` and its internal validator passed;
- fourteen compiler-selected artifacts were created;
- the required `SUBMISSION_DIR` remained empty because files were written at
  the workspace root;
- deterministic evidence, reviewer verdicts, leaf checkpoints, and
  `events.jsonl` were missing;
- several recorded hashes looked plausible but did not match the real files;
- the internal validator checked existence and parseability, not the complete
  semantic contract.

The benchmark must reject this result. Do not weaken the prompt to make the
run pass; fix artifact extraction, write-scope enforcement, or validation and
rerun the same task.

## Isolation and scope rules

- Start every run with a new empty `SUBMISSION_DIR`.
- Record a filesystem snapshot or equivalent audit evidence before dispatch.
- Treat every created or modified artifact outside `SUBMISSION_DIR` as a scope
  violation.
- Never move misplaced files into the submission after the model stops.
- Validate the directory assigned before the run, even when similarly named
  artifacts exist elsewhere.

## What the independent gate verifies

The gate checks meaning, not JSON syntax alone:

- exact candidate and integration values;
- the complete contract, evidence, review, checkpoint, repair, and event set;
- SHA-256 values recomputed from the accepted files;
- unchanged EAST and ISLANDS hashes across the WEST-only repair;
- safe evidence references that resolve inside the submission;
- strictly increasing event sequences and required lifecycle ordering.

Plausible-looking evidence fails when its hash or reference does not match the
real artifact.

## Result labels

- `PASS`: independent root gate exits `0`, no human changed artifacts, and no
  out-of-scope writes occurred.
- `ASSISTED PASS`: the gate exits `0` only after disclosed human help.
- `FAIL/INCOMPLETE`: the gate exits non-zero, the submission is misplaced or
  incomplete, the run times out, or scope rules are violated.

Report the controller status, exact submission path, validator command and
exit code, elapsed time, model/harness settings, assistance, out-of-scope
writes, and missing or invalid artifacts.

## What it measures

- completeness across a multi-file dependency graph;
- deterministic validation before semantic review;
- bounded repair of an intentionally invalid candidate;
- preservation of accepted sibling artifacts during repair;
- evidence, checkpoint, and append-only lifecycle discipline;
- final integration based only on accepted leaf outputs.

The benchmark is model-neutral. Record the model identity, harness, context
limit, timeout, number of turns, and tool permissions alongside each result.
