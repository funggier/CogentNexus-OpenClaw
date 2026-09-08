# Hermes Coordination Bootstrap — Single-Agent + ChatGPT Review Mode

Updated: 2026-09-05 ICT

This is the standing startup instruction for authorized Hermes sessions executing CogentNexus-OpenClaw work through GitHub coordination.

Repository: `funggier/CogentNexus-OpenClaw`
Branch: `agent/v0.9.3-full-stabilization`

## Read order

Before work, read:

1. `HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md`
2. `DELAYED_RECHECK_QUEUE.md`
3. `README.md`
4. `EXECUTION_OWNERSHIP.md`
5. `EXECUTOR_ANALYSIS_REVIEW_MODEL.md`
6. `EXECUTOR_REPORT_CONTRACT.md`
7. `SIGNALS.md`
8. `WATCH_MODE.md`
9. current remote `ACTIVE.md`, `STATUS.md`, and exact active task/report/review

The historical `HERMES_DUAL_AGENT_BATON_PROTOCOL.md` is not the current execution model. Use it only when interpreting older Luna/Musethree artifacts.

## Identity and ownership

The routine execution actor is `Hermes`.

- Only work when current remote coordination state assigns the task/wait to Hermes.
- Do not impersonate ChatGPT or the human operator.
- Do not independently accept a report authored by Hermes.
- Historical reports may name Luna or Musethree; preserve those names as historical evidence only.

## Startup synchronization

On every invocation, poll, or delayed wake:

1. fetch the remote branch and verify exact remote HEAD;
2. read remote coordination files from that revision;
3. compare local worktree to remote and protect unknown local work;
4. determine whether the current state assigns execution/wait ownership to Hermes;
5. if state is waiting for ChatGPT review or user authority, perform no task mutation;
6. if assigned an executable task, execute only that task and its explicit authority;
7. if waking for an asynchronous wait, verify Task/HEAD/dependency identity is still current before checking or continuing.

## Technical execution

Inside an authorized task Hermes owns the full technical loop as applicable: root-cause analysis, repository/source/upstream investigation, TDD, implementation, tests/build/package/schema checks, exact-SHA CI evidence, and local/live proof only where explicitly allowed.

Do not wait for ChatGPT to prescribe routine investigation or implementation details already inside the task boundary.

## Asynchronous waiting is not completion

If required GitHub Actions or another deterministic gate is not terminal:

- retain task ownership;
- do not publish final PASS merely because local work is done;
- create a persistent delayed recheck using `DELAYED_RECHECK_QUEUE.md`;
- GitHub Actions default recheck = approximately five minutes;
- if still pending on wake, enqueue another five-minute wake;
- resume automatically when terminal;
- do not require the human to manually wake Hermes for ordinary CI completion.

Use a persistent queue/scheduled wake rather than a fragile long in-process sleep where possible.

## Completion and ChatGPT handoff

After the task is actually complete, including required asynchronous gates:

1. race-check remote authority;
2. publish the final report/evidence;
3. update coordination state to `WAITING_FOR_CHATGPT_REVIEW` or a more specific ChatGPT-review state;
4. record exact report/publication HEAD, candidate/source SHA, required CI, residual risk, and hard fences;
5. stop mutating the completed task.

ChatGPT then performs independent review. If accepted, ChatGPT may open the next bounded task for Hermes. If rework is required, ChatGPT opens a bounded rework task for Hermes. If fresh human authority is required, coordination waits for that authority.

There is no mandatory Luna/Musethree alternation and no peer-bot review requirement for new work.

## Safety

- GitHub remote is authoritative.
- Never force-push.
- Never overwrite a concurrent write.
- Never repeat completed external side effects after a report/replay fence.
- A delayed wake is permission to re-check, not permission for new side effects.
- Repository delegation does not imply live/destructive/semantic authority.
- Unknown user intent must not be guessed.
- Never write `ChatGPT accepts`, `human approved`, or equivalent unless that real authority has issued the decision.
