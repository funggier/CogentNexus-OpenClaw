# Review — CNX-20260823-013

Verdict: `REWORK`

## Basis

Task 013 correctly verified the two exact evidence files and produced a plausible partial adjudication. It distinguished executed, failed, and skipped scenarios; identified exact Gateway and Ollama target/replacement PIDs; stated that no process-tree kill was recorded; classified provider convergence as `RUNTIME_RECOVERED_DURABLE_STATE_STUCK`; and did not perform a new runtime action.

However, the report does not satisfy all immutable acceptance criteria:

- the requested exact tested source HEAD, branch, version, harness path, harness Git blob, harness SHA256, and harness byte size are not reported; it states only that provenance is recorded;
- the scenario/step matrix omits the required start/end timestamps for individual steps;
- the exact listener endpoints are omitted from the injection safety table;
- the exact kill action exit status is omitted;
- the provider incident timeline does not give exact timestamps or explicitly account for opened, advanced, and cleared/not-cleared transitions;
- the report therefore marks several gates `PROVEN` without publishing the full evidence fields the task required for independent review.

The report also notes a bounded extraction timeout. It states that focused extraction later completed successfully, so this is not itself a blocker, but the missing required fields still prevent acceptance.

## Evidence boundary

The following remain credible but provisional pending exact-field completion:

- healthy MANAGED/Ollama baseline;
- Gateway exact-PID runtime recovery and durable convergence;
- Ollama exact-PID runtime recovery;
- provider incident opening;
- provider durable-state convergence failure inside the observation fuse;
- operator stop/start skipped;
- final cleanup health.

No safety violation is established, and no disruptive rerun is authorized.

## Required rework

Do not alter or replace the Task 013 report. Proceed only through Task `CNX-20260823-014`, which must read the same two already-hashed evidence files and publish the missing exact provenance, timestamps, endpoints, kill exit statuses, incident transitions, and corrected gate adjudication.

The recovery suite, scenarios, confirmation, live runtime/process inspection, checkout operations, cleanup, and lifecycle actions remain prohibited.
