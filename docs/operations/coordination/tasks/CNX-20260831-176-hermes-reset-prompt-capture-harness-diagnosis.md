# CNX-20260831-176 — Hermes Reset Prompt-Capture Harness Diagnosis

Status: `READY_HERMES`

Execution mode: `WINDOWS_RESET_PROMPT_CAPTURE_HARNESS_DIAGNOSIS_HERMES`

Authorization: `CNX-20260831-176_HERMES_RESET_PROMPT_CAPTURE_HARNESS_DIAGNOSIS`

Executor: Hermes/Codex

Coordinator / final reviewer: ChatGPT

## Objective

Diagnose the Task-175 reset completion-capture failure **without running reset or mutating CogentNexus/OpenClaw/runtime state**.

Determine whether the Task-175 wrapper/observer stalled because the real reset confirmation prompt is emitted by Python `input("Continue? [y/N]: ")` without a newline, because of another buffering/handle/process-tree issue, or because of some different executor-harness defect.

Produce and qualify a non-destructive prompt/input/result capture method suitable for a later reset acceptance task. This task does not authorize the later reset itself.

## Accepted baseline

- Product repair SHA: `231761fca24c315e90536955d3e384f55e2e232e`
- Installed fingerprint: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`
- Accepted package SHA-256: `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`
- Installed release: `0.9.3`
- OpenClaw: `2026.7.1-2`
- Task 174: `ACCEPTED_BLOCKED — RESET_CONFIRMATION_STDIN_BOUNDARY_FAILED_BEFORE_DESTRUCTIVE_MUTATION`
- Task 175: `ACCEPTED_UNPROVEN — RESET_COMPLETION_BOUNDARY_UNAVAILABLE_AFTER_QUALIFIED_STDIN`
- Task-171 through Task-173 semantic/durable result remains accepted.

Task 175 already proved a disposable redirected Python `input()` round trip can work. The unresolved boundary is prompt observation/result capture for the reset-style interaction.

## Hard fence

Task 176 authorizes **zero destructive actions and zero semantic actions**.

Do not run:

- `cnxclaw.cmd reset`;
- `cnxclaw.cmd uninstall`;
- installer/install-over/reinstall;
- `start`, `stop`, `restart`, `enable`, or `disable` against the live product;
- manual Gateway/Ollama/Supervisor lifecycle commands;
- Dashboard Send, composer input, `chat.inject`, model inference, or recovery/regeneration;
- manual DB/Ticket/config/transcript/delivery mutation;
- product/source/test/workflow/dependency changes;
- release/tag/merge/force push.

Only read-only inspection, disposable temporary harnesses/processes, harmless Python prompt probes, evidence hashing, and Task-176 report publication are authorized.

## Fresh authority preflight

Before diagnosis:

1. read fresh remote branch HEAD;
2. read fresh `ACTIVE.md` and `STATUS.md`;
3. confirm Task 176 is active and its report path is absent;
4. confirm no reset/uninstall process is active;
5. read-only reconfirm installed fingerprint/OpenClaw identity and runtime remains coherent;
6. do not alter the live runtime merely to simplify diagnosis.

If authority changed, report `BLOCKED` and stop.

## Phase A — recover the exact Task-175 harness design

Inspect the temporary wrapper/script/process-launch code and available logs used by Task 175, if preserved.

Record exactly:

- wrapper/script path and SHA-256;
- child command construction;
- shell/cmd invocation boundary;
- stdin/stdout/stderr redirection mode;
- text vs binary mode;
- buffering settings;
- prompt detection algorithm;
- whether reads were line-oriented (`readline`, iteration over lines, etc.) or character/byte/chunk oriented;
- when the wrapper intended to write `y`;
- timeout locations;
- process-tree/wait behavior;
- artifact finalization logic.

Do not infer the harness algorithm from the timeout alone. If the original wrapper is unavailable, state that explicitly and reconstruct the smallest equivalent based on the Task-175 report without claiming byte-for-byte identity.

## Phase B — exact no-newline prompt reproduction

Create a disposable Python child that performs no product import/state access and uses the same prompt shape as reset:

```python
value = input("Continue? [y/N]: ")
print("ACK:" + value)
```

Use a unique non-secret token, not `y`, for diagnostic runs unless a literal `y` is needed only to verify the harmless child. The child must not reference CogentNexus/OpenClaw paths or state.

Exercise the Task-175 prompt-observation strategy against this harmless child.

Record:

- whether prompt bytes/chars become available before newline;
- whether a line-oriented observer returns the prompt before input is sent;
- whether the observer blocks while the child waits for input;
- process states during the block;
- whether sending input without prompt proof would have been required to break the deadlock.

If this reproduces the Task-175 stall, classify the cause as an executor harness prompt-capture defect, not a product reset defect.

## Phase C — qualify a safe prompt/result capture method

Develop or select a **temporary executor harness only** that can interact with the harmless no-newline child while preserving all of the evidence required for a future destructive task.

Acceptable approaches include raw/character/chunk reads, asynchronous stream capture, a PTY/ConPTY mechanism with proven valid stdin, or another method that does not depend on newline termination.

Qualification requires at least two harmless runs with distinct tokens and all of:

1. prompt observed before input is sent;
2. exactly one input line/event sent per run;
3. exact ACK returned;
4. child exit code `0` captured;
5. stdout/stderr retained completely enough to prove the transaction;
6. wrapper/harness result artifact finalized;
7. no timeout or orphan process;
8. no product/runtime/durable mutation.

Do not qualify a method merely because pre-piping input makes the child exit. Future reset acceptance still requires observing the real prompt before sending the one confirmation.

## Phase D — bounded product-adjacent read-only compatibility check

Without launching reset, inspect the installed launcher chain and accepted source sufficiently to answer:

- whether `cnxclaw.cmd reset` ultimately reaches the same Python confirmation routine;
- whether any `cmd.exe`/batch layer changes stdin/stdout inheritance in a way the qualified harness must account for;
- whether stdout buffering could differ materially from the harmless direct-Python child;
- what exact future harness command/process-tree should be used to preserve prompt, confirmation event, child exit code, and output.

This phase is read-only. Do not execute the destructive command to test the answer.

## Required diagnosis result

Task 176 should classify one of:

- `PASS — HARNESS_ROOT_CAUSE_CONFIRMED_AND_CAPTURE_METHOD_QUALIFIED`
- `PARTIAL — HARNESS_DEFECT_FOUND_BUT_CAPTURE_METHOD_NOT_QUALIFIED`
- `UNPROVEN — TASK175_HARNESS_ROOT_CAUSE_NOT_ESTABLISHED`
- `BLOCKED — REQUIRED_NON_DESTRUCTIVE_EVIDENCE_UNAVAILABLE`

A `PASS` means only the execution harness is ready for a future reset task. It does **not** mean reset acceptance passed.

## Evidence requirements

Preserve at minimum:

- exact authority HEAD;
- Task-175 wrapper/script or reconstruction identity and hash;
- harmless child code/hash;
- prompt-capture traces with timestamps;
- evidence showing whether prompt was available without newline;
- process-state evidence for any reproduced stall;
- qualified harness code/hash;
- at least two successful qualified harmless transcripts with unique tokens;
- exact prompt-before-input ordering;
- input event count;
- exit codes;
- stdout/stderr/result artifacts;
- read-only installed launcher/source correlation;
- mutation/action ledger;
- contradictions/residual uncertainty.

## Acceptance matrix

Include at minimum:

| Criterion | Verdict | Evidence |
|---|---|---|
| Fresh authority | PASS/FAIL/BLOCKED | remote HEAD/ACTIVE/STATUS |
| Task-175 harness recovered/reconstructed | PASS/UNPROVEN | script/hash/design |
| No-newline prompt behavior reproduced | PASS/FAIL/UNPROVEN | harmless trace |
| Task-175 stall root cause classified | PASS/UNPROVEN | causal evidence |
| New capture method observes prompt before input | PASS/FAIL | trace |
| Exactly one input per harmless run | PASS/FAIL | event ledger |
| Exit/result capture reliable | PASS/FAIL | two-run evidence |
| No timeout/orphan | PASS/FAIL | process evidence |
| Product launcher compatibility assessed read-only | PASS/UNPROVEN | launcher/source evidence |
| Zero destructive/semantic/live mutation | PASS/FAIL | hard-fence ledger |
| Report-only publication | PASS/FAIL | commit diff |

## Reviewer Verification Packet

Include 5–8 critical claims with exact evidence pointers. At minimum:

1. whether Task-175 used a line-oriented or otherwise blocking prompt observer;
2. whether exact reset-style no-newline prompt reproduces the stall;
3. prompt-before-input proof for the qualified method;
4. two harmless successful runs and exit/result capture;
5. no product/reset/runtime mutation;
6. installed launcher compatibility conclusion;
7. residual uncertainty before another reset authorization;
8. report-only publication fence.

## Required report

Publish only:

`docs/operations/coordination/reports/CNX-20260831-176-hermes-reset-prompt-capture-harness-diagnosis.md`

After publication, stop for ChatGPT review.

No reset, uninstall, reinstall, or semantic action is authorized by Task 176.
