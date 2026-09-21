# CogentNexus Coordination Layer

GitHub coordination files are the durable handoff surface between ChatGPT, Hermes, and the human operator.

## Canonical standing model

- Repository: `funggier/CogentNexus-OpenClaw`
- Working branch: always read the current branch from `ACTIVE.md` / `STATUS.md`; do not hard-code a historical branch
- Current authority: remote `ACTIVE.md` + `STATUS.md` + linked active task
- Repository/documentation/review executor: ChatGPT when current tools permit
- Local/live machine executor: Hermes when bounded local execution is required
- Human operator: final authority

## Retired watcher

The old Codex `CogentNexus coordination watch` automation that polled every minute was retired and removed on 2026-09-21. Historical references to that automation explain past operation only.

Do **not** recreate the retired watcher merely because an old task/report mentions it.

Asynchronous CI/external waits should use the currently available bounded scheduling/recheck mechanism only when the active task actually requires one.

## Intended loop

```text
Human intent
  -> current GitHub coordination task
  -> ChatGPT executes directly when safe/possible
  -> Hermes bounded local/live execution when required
  -> evidence/report
  -> ChatGPT independent verification
  -> next bounded task or completion
```

## Standing documents

- `SESSION_EXECUTION_MODEL_GUIDELINES.md` — operator workflow preferences.
- `HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md` — bounded Hermes handoff rules.
- `DELAYED_RECHECK_QUEUE.md` — asynchronous wait semantics where an active task needs them.
- `EXECUTION_OWNERSHIP.md` — ownership/race/live-authority boundaries.
- `EXECUTOR_REPORT_CONTRACT.md` — report/evidence interface.
- `CODEX_BOOTSTRAP.md` — startup synchronization guidance; despite the legacy filename, it must not hard-code an obsolete branch.
- `WATCH_MODE.md` — historical/optional watch semantics; the old persistent watcher is retired.
- `PROBLEM_LOOP.md` — blocker handling.
- `SIGNALS.md` — operator signal meanings.
- `HERMES_DUAL_AGENT_BATON_PROTOCOL.md` — historical dual-agent protocol only.

## Key invariants

- Remote GitHub truth outranks stale conversational memory.
- Read the current branch/task from authoritative coordination state.
- Do not infer fresh live/destructive/semantic authority.
- Do not force-push.
- Do not repeat a completed external side effect after matching terminal evidence.
- Historical tasks/reports/reviews remain historical evidence.
- A watcher or scheduled task is never implicit authority for a successor task.

## Current state

Read [ACTIVE.md](ACTIVE.md) and [STATUS.md](STATUS.md). They supersede old READY/WAITING examples in completed historical artifacts.
