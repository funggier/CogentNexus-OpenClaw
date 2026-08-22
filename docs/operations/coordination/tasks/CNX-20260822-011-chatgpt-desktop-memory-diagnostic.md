# CNX-20260822-011 — ChatGPT Desktop Memory Attribution

Status: QUEUED  
Owner: ChatGPT  
Executor: Codex  
Priority: next operational diagnostic after Task 010 reaches a terminal reviewed state  
Requested by: human operator  
Predecessor: `CNX-20260822-010` must not be interrupted or superseded

## Objective

Determine why the Windows ChatGPT desktop process group increased from roughly 2 GB to more than 4 GB, distinguish normal loaded-session/cache use from an inactive renderer, background task, or leak, and identify the narrowest safe way to reclaim memory without losing chats, deleting project history, interrupting coordination, or killing unrelated processes.

This task is diagnostic only until its report is reviewed. It does not authorize process termination, app restart, chat deletion, project deletion, cache deletion, session-file deletion, or operating-system cleanup.

## Activation condition

This queued task must not execute merely because this file exists.

ChatGPT must first:

1. review the matching Task 010 report;
2. confirm no Windows recovery suite or other Codex/Work task is still executing;
3. update `ACTIVE.md` to this exact Task ID with `READY_FOR_CODEX`;
4. preserve this task's duplicate-execution fence.

Until then, Task 010 remains the only active task.

## Product boundary

Official OpenAI documentation establishes that Projects retain chats/files as project context, Work may use cloud or local chats, and Codex history is separate from ChatGPT history. It does not establish that each stored project chat consumes a persistent local renderer or a fixed amount of RAM.

Therefore do not assume that deleting chats will reclaim memory. Attribute the memory to exact local processes first.

## Duplicate-execution fence

Before any diagnostic action, fetch the branch and check for:

`docs/operations/coordination/reports/CNX-20260822-011-chatgpt-desktop-memory-diagnostic.md`

If it exists, perform no local observation, UI action, sampling, restart, cleanup, or other side effect. Stop awaiting ChatGPT review.

## Required read-only diagnostic

Record the exact Task 011 start HEAD and confirm this task is ACTIVE before local inspection.

Capture a bounded inventory of the ChatGPT desktop process group using exact PIDs. For each relevant process record:

- PID and parent PID;
- executable/process name;
- executable path where accessible;
- process start time and elapsed age;
- main-window title where non-sensitive;
- working set;
- private working set/private bytes where available;
- paged and non-paged memory where available;
- virtual memory;
- CPU time;
- handle count;
- thread count;
- responding state;
- child-process role if it can be established from non-sensitive executable metadata.

Redact command-line tokens, account identifiers, repository credentials, chat text, and file contents.

Take at least three samples at bounded intervals, with no interval longer than 30 seconds, and record whether memory is stable, increasing, or falling while no new user action is performed.

Also record:

- ChatGPT desktop app version if obtainable without changing state;
- count of visible ChatGPT windows and exact owning PIDs;
- whether Chat, Work, Codex, voice, browser, terminal, image, or other active tasks are visibly running;
- whether the coordination watcher or another scheduled task is currently active;
- aggregate memory by process role and for the whole ChatGPT process group;
- system total/available physical memory and committed-memory pressure;
- the five largest processes on the machine by working set, without exposing sensitive command lines.

Do not read chat bodies, project files, browser history, credentials, cookies, tokens, or message databases. Metadata-only directory size/file-count observation is allowed only when the exact path is already documented by the installed app and no contents are opened.

## Attribution criteria

Classify the result as one or more of:

- `ACTIVE_WORKLOAD`: memory corresponds to currently running Work/Codex/tool execution;
- `LOADED_UI`: memory is concentrated in visible/loaded renderer or UI processes;
- `CACHE_RETENTION`: memory is stable and retained after work completes, without continued growth;
- `SUSPECTED_LEAK`: one exact process shows continued growth across idle samples without active work;
- `SYSTEM_PRESSURE`: high total commit or low available RAM is the main risk;
- `UNATTRIBUTED`: evidence cannot safely determine the cause.

Do not classify from process name alone.

## Safe recommendation only

The report may recommend one narrow next action, but this task must not perform it.

Possible recommendations, only when supported by evidence:

- close one specifically identified unused visible window through normal UI;
- finish/archive an inactive task while preserving its chat;
- gracefully restart ChatGPT after all active tasks stop;
- update the desktop app if an applicable release note supports a fix;
- preserve the current state because memory is stable and system pressure is low;
- open a focused support/bug report with exact app version and process metrics.

Deleting project chats, deleting sessions, deleting caches, force-closing the app, `Stop-Process`, `taskkill`, process-tree termination, service termination, and reboot are not authorized recommendations unless a later human-reviewed task explicitly permits one exact reversible action.

## Prohibited actions

- no process kill of any kind;
- no process-tree operation;
- no ChatGPT/Codex/Work app restart;
- no window close or UI mutation;
- no chat, session, project, worktree, cache, cookie, credential, or history deletion;
- no package install or app update;
- no Registry, scheduled-task, service, startup, or configuration change;
- no CogentNexus/OpenClaw/Ollama command or runtime action;
- no reset, uninstall, reinstall, merge, tag, or release;
- no force-push.

## Acceptance criteria

PASS requires exact-PID multi-sample memory evidence, process-role attribution or an explicit `UNATTRIBUTED` result, system-pressure context, complete safety accounting, and one evidence-based narrow recommendation.

Do not claim that stored Project chats themselves caused the RAM increase unless the evidence directly establishes that relationship.

## Report

Write only:

`docs/operations/coordination/reports/CNX-20260822-011-chatgpt-desktop-memory-diagnostic.md`

Include:

- start HEAD and ACTIVE verification;
- exact commands and exit codes;
- per-PID sample table;
- aggregate and system-memory table;
- visible-window/active-work accounting;
- classification;
- safety notes;
- recommended next action;
- what remains unproven.

Only this matching Codex report may change. Commit message must begin:

`report: CNX-20260822-011`

Never force-push. Stop after publishing the report.
