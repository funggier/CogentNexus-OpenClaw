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

Validate the validator itself with a generated known-good fixture and a
deliberately tampered fixture:

```powershell
python test_validator.py
```

## What it measures

- completeness across a multi-file dependency graph;
- deterministic validation before semantic review;
- bounded repair of an intentionally invalid candidate;
- preservation of accepted sibling artifacts during repair;
- evidence, checkpoint, and append-only lifecycle discipline;
- final integration based only on accepted leaf outputs.

The benchmark is model-neutral. Record the model identity, harness, context
limit, timeout, number of turns, and tool permissions alongside each result.
