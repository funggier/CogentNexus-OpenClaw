# Hermes Coordination Bootstrap — Current Single-Agent + ChatGPT Review Mode

Updated: 2026-09-21 ICT

This is the standing startup instruction for a Hermes session explicitly assigned current CogentNexus-OpenClaw work.

Repository: `funggier/CogentNexus-OpenClaw`
Branch: **read from current remote `ACTIVE.md` / `STATUS.md`; never hard-code a historical branch**

## Read order

1. `README.md`
2. `SESSION_EXECUTION_MODEL_GUIDELINES.md`
3. `HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md`
4. `EXECUTION_OWNERSHIP.md`
5. `EXECUTOR_REPORT_CONTRACT.md`
6. current remote `ACTIVE.md`
7. current remote `STATUS.md`
8. the exact linked task/report/review

Historical watcher/dual-agent documents are context only unless the active task explicitly reactivates a bounded mechanism.

## Startup synchronization

On invocation:

1. identify the branch named by remote coordination authority;
2. fetch that branch and verify exact remote HEAD;
3. read current coordination files from that revision;
4. protect unknown local work;
5. execute only work assigned to Hermes;
6. stop when authority moves to ChatGPT or the operator.

## Technical execution

Within an authorized task, Hermes may perform root-cause analysis, TDD, implementation, tests/build/package/schema checks, and bounded local/live proof allowed by that task.

Do not wait for ChatGPT to prescribe routine technical steps already inside the task boundary.

## Asynchronous waits

The retired one-minute `CogentNexus coordination watch` automation is not active and must not be recreated automatically.

If the current task requires CI/external rechecks, use the currently supported bounded delayed-recheck mechanism and always re-read remote authority before continuing.

## Completion

After a Hermes-owned task completes:

1. race-check remote authority;
2. publish evidence/report if the task requires it;
3. hand control to ChatGPT review;
4. stop mutation of the completed task.

## Safety

- GitHub remote authority is canonical.
- Never force-push.
- Never overwrite concurrent work.
- Never repeat completed side effects after terminal evidence.
- Repository authority does not imply destructive/live authority.
- Unknown intent must not be guessed.
