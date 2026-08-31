# CNX-20260831-177 — Hermes Windows CMD/Batch Incremental Harness Qualification

Status: `READY_HERMES`

Execution mode: `WINDOWS_CMD_BATCH_INCREMENTAL_HARNESS_QUALIFICATION_HERMES`

Authorization: `CNX-20260831-177_HERMES_CMD_BATCH_INCREMENTAL_HARNESS_QUALIFICATION`

Executor: Hermes/Codex

Coordinator / final reviewer: ChatGPT

## Objective

Qualify, without invoking CogentNexus-OpenClaw reset or any other destructive lifecycle action, the exact Windows process topology and incremental evidence architecture intended for the next reset acceptance attempt.

Task 176 proved that character-level prompt capture works for a direct disposable Python child, but it did not harmlessly exercise the remaining Task-175 uncertainty boundary:

`outer harness → cmd.exe /d /c → .cmd batch file → Python input() child`

Task 177 must reproduce that topology with disposable files outside the repository/live product state and prove that the harness can observe the no-newline prompt, send exactly one input line, concurrently drain stdout/stderr, retain incremental evidence before final process exit, and finish without timeout/orphan.

This task does **not** authorize reset.

## Accepted baseline

- Product repair SHA: `231761fca24c315e90536955d3e384f55e2e232e`
- Installed fingerprint: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`
- Accepted package SHA-256: `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`
- Installed release: `0.9.3`
- OpenClaw: `2026.7.1-2`
- Task 174: `ACCEPTED_BLOCKED — RESET_CONFIRMATION_STDIN_BOUNDARY_FAILED_BEFORE_DESTRUCTIVE_MUTATION`
- Task 175: `ACCEPTED_UNPROVEN — RESET_COMPLETION_BOUNDARY_UNAVAILABLE_AFTER_QUALIFIED_STDIN`
- Task 176: `ACCEPTED_DIAGNOSTIC_PASS — CHARACTER_PROMPT_CAPTURE_QUALIFIED_TASK175_ROOT_CAUSE_REMAINS_UNPROVEN`

Task-171 semantic Send count remains permanently frozen at exactly `1`.

## Reviewer-side history anomaly already neutralized

After Task-176 report publication, a reviewer-side connector accidentally created an empty root file `__noop__` in commit `4d16bded6b0909f599a5703d82d44ef7145f2d03` and immediately removed it in `5f8aaacf24e90cab8764817c0f9777c0366d10f1`.

Independent compare `3fdc8b56f40c90b6d7af4136b1412d20bd9187c8 -> 5f8aaacf24e90cab8764817c0f9777c0366d10f1` shows effective changed files `[]`.

Treat this as historical reviewer coordination noise only. Do not modify or rewrite history and do not use force push.

## Fresh authority preflight

Before diagnostics:

1. fetch fresh remote branch HEAD;
2. read fresh `ACTIVE.md` and `STATUS.md`;
3. confirm Task 177 remains active;
4. confirm Task-177 report path is absent;
5. confirm no successor/conflicting authorization exists;
6. perform read-only identity/health sanity checks sufficient to prove no unexpected lifecycle mutation occurred since Task 176;
7. confirm no active reset/uninstall process exists.

If authority conflicts, report `BLOCKED` and stop.

## Required disposable topology

Create all diagnostic files under a new temporary evidence directory outside the repository and outside CogentNexus/OpenClaw owned state.

The harmless test topology must be equivalent to:

```text
outer Python harness
  → cmd.exe /d /c <disposable-test.cmd>
      → Python <disposable-input-child.py>
```

The disposable Python child must perform only:

```python
value = input("Continue? [y/N]: ")
print("ACK:" + value)
```

It must not import CogentNexus/OpenClaw modules, read/write live state, invoke a model/provider, or run any product command.

The disposable `.cmd` must do nothing except invoke the disposable Python child and propagate its exit code.

## Harness architecture required for qualification

Use the architecture intended for the future reset attempt, with these mandatory properties:

1. launch `cmd.exe /d /c` around the disposable `.cmd`;
2. pipe stdin/stdout/stderr;
3. consume stdout at character/byte granularity so the no-newline prompt is observable;
4. drain stdout and stderr concurrently from process start through process exit;
5. do not wait for stdout EOF before beginning stderr consumption;
6. detect the exact prompt `Continue? [y/N]: ` before supplying input;
7. supply exactly one unique non-secret token line after prompt observation;
8. maintain an in-memory input-send counter initialized to zero and fail closed if a second send would occur;
9. persist an append-only or atomically replaced event ledger incrementally, not only after child exit;
10. persist stdout/stderr capture incrementally enough that an outer tool timeout would still leave prompt/input/progress evidence;
11. record process/PID identity and final exit code;
12. scan for orphaned diagnostic cmd/Python children after completion;
13. never kill a healthy live product process; only disposable diagnostic children belong to this task.

### Required critical event ledger

At minimum persist ordered events for:

- `harness_started`
- `cmd_process_started`
- `prompt_observed`
- `input_send_intent`
- `input_sent`
- `stdin_closed`
- `cmd_process_exited`
- `stdout_reader_completed`
- `stderr_reader_completed`
- `orphan_scan_completed`
- `run_finalized`

Each event must include a timestamp and run identity. Record `input_send_count` in the final result.

The ledger must exist and contain prompt/input events **before** relying on final process completion.

## Required runs

Perform at least **two independent** harmless runs with distinct tokens.

Each run may PASS only if all are proven:

- exact prompt observed before input;
- exactly one input event/line;
- exact ACK for that run token;
- stdout/stderr readers complete;
- exit code `0`;
- no timeout;
- no orphaned disposable cmd/Python process;
- incremental ledger contains ordered prompt/input/exit evidence;
- no product/runtime/durable mutation.

If either run fails, do not repeat indefinitely. A maximum of two qualification runs is authorized unless the first failure is caused solely by a disposable-script syntax/setup error that occurred before any child input boundary; classify and report rather than looping.

## Read-only installed-launcher correlation

After harmless qualification, inspect the installed launcher chain read-only and record enough to show whether the qualified process topology is materially representative of:

```text
cmd.exe /d /c C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd reset
```

At minimum record:

- installed `cnxclaw.cmd` SHA-256;
- launcher command chain to Python/v0.9.3 facade;
- installed lifecycle confirmation still uses `input("Continue? [y/N]: ")`;
- any material topology difference between disposable chain and real launcher that could invalidate the qualification.

If a material unqualified difference remains, report `UNPROVEN`; do not run reset.

## PASS contract

Task 177 may report:

`PASS — CMD_BATCH_INCREMENTAL_HARNESS_QUALIFIED`

only if:

1. fresh authority is valid;
2. two independent disposable cmd/batch/Python runs pass;
3. prompt-before-input and exactly-one input are durably recorded before process exit;
4. stdout/stderr are drained concurrently;
5. complete exit/result evidence is retained;
6. no timeout/orphan occurs;
7. installed launcher correlation reveals no material unqualified topology difference;
8. destructive action count is `0`;
9. semantic action count is `0`;
10. product/source/test/workflow/live runtime/durable state are unchanged.

If any required property remains uncertain, report `UNPROVEN` or `BLOCKED` and stop.

## Hard fence

Task 177 destructive action budget: `0`.
Task 177 semantic action budget: `0`.

Do not run:

- `cnxclaw reset`;
- `cnxclaw uninstall`;
- installer/install-over/reinstall;
- `start`, `stop`, `restart`, `enable`, `disable`;
- Gateway/Ollama/Supervisor/OpenClaw lifecycle mutation;
- Dashboard Send or composer submission;
- `chat.inject`;
- model inference;
- recovery/regeneration;
- manual durable/config/transcript mutation;
- product/source/test/workflow/dependency change;
- upgrade;
- release/tag/package publication;
- merge;
- force push.

Only read-only live inspection, disposable temporary cmd/Python diagnostics, evidence hashing, and Task-177 report publication are authorized.

## Evidence requirements

Preserve:

- exact remote authority;
- disposable `.cmd`, child Python, and harness hashes;
- run tokens;
- event ledgers for both runs;
- incremental stdout/stderr logs/results;
- process/PID identities;
- exact ACK/exit results;
- orphan scans;
- installed launcher/source hashes and read-only topology correlation;
- explicit mutation/action ledger;
- hashes of critical evidence files;
- contradictions/residual uncertainty.

## Reviewer Verification Packet

Include 5–10 critical claims with exact evidence pointers, prioritizing:

1. exact disposable cmd/batch/Python topology;
2. concurrent stdout/stderr consumption;
3. prompt-before-input in run 1;
4. prompt-before-input in run 2;
5. exactly one input per run;
6. incremental ledger durability before process exit;
7. exact ACK/exit 0/no orphan for both runs;
8. installed launcher topology correlation;
9. zero destructive/semantic/live mutation;
10. report-only publication fence.

## Required report

Publish only:

`docs/operations/coordination/reports/CNX-20260831-177-hermes-cmd-batch-incremental-harness-qualification.md`

After publication, stop for ChatGPT review. Another reset remains unauthorized until a separate successor task is opened after this report is accepted.
