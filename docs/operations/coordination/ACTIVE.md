# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `TEST_SEMANTIC_GATE`
Current authorization: `CNX-20260828-115_INTERRUPTED_REENTRY_SEMANTIC_MATRIX_HARDENING`
Task ID: `CNX-20260828-115`
Updated: 2026-08-28 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260828-115-interrupted-reentry-semantic-matrix-hardening.md`](tasks/CNX-20260828-115-interrupted-reentry-semantic-matrix-hardening.md)

Task 115 is a **tests-first semantic matrix fidelity gate**. The accepted Task-113 production behavior is preserved unless corrected boundary-specific tests expose a genuine source defect.

## Task 114 closure

Task-114 report:

`docs/operations/coordination/reports/CNX-20260828-114-interrupted-reentry-direct-matrix-validation.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260828-114-interrupted-reentry-direct-matrix-validation-review.md`

Review verdict:

`SOURCE BEHAVIOR ACCEPTED; LIVE GATE BLOCKED — MATRIX FIDELITY / SEMANTIC ASSERTION DEFECTS`

Accepted Task-114 reproducibility facts include exact candidate `83e8452de116bf6204be884e4cddf9f3b92b90da`, all three exact-SHA workflows successful, and artifact `9686448746` independently hash-verified. No Task-114 production edit occurred.

Independent reviewer execution against the exact packaged candidate also confirmed that real legacy residues (`cnx.cmd`, `.cogent`, and `extensions/cogentnexus-rotation`) are rejected by the current production source with `mixed legacy state`, and valid direct/managed re-entry returns all expected result/path bindings. The remaining defect is durable regression-test fidelity, not a demonstrated production defect.

## Required Task-115 method

`fresh reconcile -> TESTS-ONLY semantic fixture/assertion correction -> run corrected matrix -> (all GREEN: no production edit; genuine RED: minimal separate repair) -> targeted/full validation -> exact same-source CI/package proof -> report -> independent review`

Task 115 must use real exact payloads for outside/noncanonical storage cases, real legacy filesystem/extension residue for mixed namespace, boundary-specific error assertions, and classification non-mutation checks.

## Preserved live boundary

Task 107 remains the last authoritative live-machine evidence. No later task has authorized real Windows lifecycle mutation. Any future live acceptance must begin with a fresh read-only machine preflight.

## Hard fence

Task 115 does **not** authorize:

- real Windows install-over/reset/uninstall/reinstall/lifecycle/recovery;
- Task-107 replay or manual normalization;
- Dashboard semantic nonce/message/Send;
- OpenClaw/Ollama update/reinstall/uninstall/stop/rebaseline;
- provider/model/timeout changes;
- live SQLite/config/session mutation;
- credential/token/password access or re-entry;
- LM Studio management;
- process-tree kills or reboot;
- merge/tag/GitHub Release/force push;
- weakening namespace/wrapper/manifest/payload/product-evidence/ownership/final verification.

## Completion signal

Hermes/Codex must publish exactly:

`docs/operations/coordination/reports/CNX-20260828-115-interrupted-reentry-semantic-matrix-hardening.md`

After publishing the report, stop for independent ChatGPT review. Do not create or execute a live-Windows acceptance task.
