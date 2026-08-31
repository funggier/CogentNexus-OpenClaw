# CNX-20260822-011 — ChatGPT Desktop Memory Attribution

Status: QUEUED  
Owner: ChatGPT  
Executor: Codex  
Priority: deferred conditional follow-up; must not block CogentNexus recovery work while RAM remains stable  
Requested by: human operator  
Predecessor: `CNX-20260823-012` must first resolve the Task 010 collision ambiguity

## Objective

Determine why the Windows ChatGPT desktop process group increased from roughly 2 GB to more than 4 GB, distinguish normal loaded-session/cache use from an inactive renderer, background task, or leak, and identify the narrowest safe way to reclaim memory without losing chats, deleting project history, interrupting coordination, or killing unrelated processes.

This task is diagnostic only until its report is reviewed. It does not authorize process termination, app restart, chat deletion, project deletion, cache deletion, session-file deletion, or operating-system cleanup.

## Operator observation and priority

On 2026-08-23, the human operator reported that ChatGPT desktop RAM usage had decreased and directed coordination to continue CogentNexus once the checkout/race issue is safely resolved.

Treat the lower RAM observation as evidence that immediate pressure improved, not as proof of root cause or permanent remediation. This task is now a deferred conditional diagnostic and must not delay the v0.9.3 process-recovery gates while memory remains stable.

## Activation condition

This queued task must not execute merely because this file exists.

ChatGPT may activate it only when:

1. Task 012 has been reviewed and proves no overlapping recovery execution remains;
2. no Windows recovery suite or other Codex/Work task is executing;
3. RAM growth recurs, system pressure becomes material, or the process-recovery sequence reaches a safe pause where this diagnostic adds value;
4. `ACTIVE.md` is explicitly updated to this exact Task ID with `READY_FOR_CODEX`;
5. this task's duplicate-execution fence is preserved.

If RAM remains stable after Task 012, continue the narrow CogentNexus process-recovery plan before activating Task 011.

## Product boundary

Official OpenAI documentation establishes that Projects retain chats/files as project context, Work may use cloud or local chats, and Codex history is separate from ChatGPT history. It does not establish that each stored project chat consumes a persistent local renderer or a fixed amount of RAM.

Official OpenAI documentation also states that scheduled tasks can create many worktrees over time, that worktrees can contain their own dependencies and build caches, and that Codex-managed worktrees have a configurable retention/automatic-cleanup policy. Those guarantees apply to Codex-managed worktrees. Full clones or worktrees created directly by CogentNexus coordination tasks under the established `.openclaw\worktrees` parent must be inventoried separately and must not be assumed to be automatically managed.

Therefore do not assume that deleting chats will reclaim memory. Attribute the memory to exact local processes first, distinguish disk accumulation from resident process memory, and test whether watchers, indexers, terminals, or active sessions remain attached to old checkout paths.

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

## Worktree and isolated-clone attribution

Perform this section read-only and only after the process samples above. Do not traverse arbitrary user directories.

Inventory:

1. the repository's registered worktrees using `git worktree list --porcelain`;
2. Task-created directories under the already established CogentNexus checkout/worktree parent, including known Task 007–010 paths and any additional path named by an accepted task/report;
3. full isolated clones separately from Git-linked worktrees;
4. Codex-managed worktrees separately from Task-created full clones or permanent worktrees.

For each candidate, record only the metadata needed for safe attribution:

- exact path;
- type: `CODEX_MANAGED_WORKTREE`, `PERMANENT_WORKTREE`, `GIT_WORKTREE`, `FULL_CLONE`, or `UNKNOWN`;
- owning repository and redacted origin identity;
- exact HEAD and branch/detached state;
- clean/dirty/unreadable status;
- creation/last-write age where obtainable without reading file contents;
- total disk size and file count using metadata-only enumeration;
- matching coordination Task ID;
- matching report/review presence and terminal status;
- whether the path is named by the currently active task;
- exact PIDs of any safely observable ChatGPT/Codex renderer, watcher, indexer, terminal, shell, Git, editor, or other process whose working directory, executable metadata, or open-handle metadata demonstrably references the path;
- aggregate working set/private bytes for those exact attached PIDs.

Do not infer RAM use from directory size. A checkout with no attached process is a disk-usage finding only. A path/process relationship is a RAM finding only when exact-PID evidence supports it.

Create a cleanup manifest with exactly one disposition per path:

- `KEEP_ACTIVE`: current task, active process, in-progress/pinned/permanent chat, or otherwise required;
- `KEEP_DIRTY`: uncommitted/unreviewed work or unreadable state;
- `POSSIBLE_REMOVE_AFTER_REVIEW`: clean, terminally reviewed, inactive, and not referenced by ACTIVE;
- `UNKNOWN_DO_NOT_REMOVE`: ownership or safety cannot be proven.

Task 008's damaged checkout and every Task 010 checkout remain `KEEP_ACTIVE` or `UNKNOWN_DO_NOT_REMOVE` unless a later task explicitly proves that their evidence obligations are complete. Do not repair them to make them removable.

This task must not execute `git worktree remove`, `git worktree prune`, `git clean`, `git reset`, directory deletion, archive/pin changes, project removal, chat archival, or any other cleanup. The report may propose a later narrow cleanup task naming exact reviewed paths only.

## Attribution criteria

Classify the result as one or more of:

- `ACTIVE_WORKLOAD`: memory corresponds to currently running Work/Codex/tool execution;
- `LOADED_UI`: memory is concentrated in visible/loaded renderer or UI processes;
- `CACHE_RETENTION`: memory is stable and retained after work completes, without continued growth;
- `SUSPECTED_LEAK`: one exact process shows continued growth across idle samples without active work;
- `SYSTEM_PRESSURE`: high total commit or low available RAM is the main risk;
- `WORKTREE_DISK_ACCUMULATION`: stale checkout paths consume disk but no attached process proves a RAM relationship;
- `PATH_BOUND_BACKGROUND_PROCESS`: exact-PID evidence proves a watcher, indexer, terminal, renderer, or session remains attached to one or more old paths;
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
- open a focused support/bug report with exact app version and process metrics;
- authorize a later exact cleanup task for only paths marked `POSSIBLE_REMOVE_AFTER_REVIEW`, using the correct Git/Codex lifecycle operation for each path type.

Deleting project chats, deleting sessions, deleting caches, force-closing the app, `Stop-Process`, `taskkill`, process-tree termination, service termination, and reboot are not authorized recommendations unless a later human-reviewed task explicitly permits one exact reversible action.

## Prohibited actions

- no process kill of any kind;
- no process-tree operation;
- no ChatGPT/Codex/Work app restart;
- no window close or UI mutation;
- no chat, session, project, worktree, clone, cache, cookie, credential, or history deletion;
- no `git worktree remove`, `git worktree prune`, `git clean`, `git reset`, broad recursive deletion, or Task 007–010 checkout repair/reuse;
- no package install or app update;
- no Registry, scheduled-task, service, startup, or configuration change;
- no CogentNexus/OpenClaw/Ollama command or runtime action;
- no reset, uninstall, reinstall, merge, tag, or release;
- no force-push.

## Acceptance criteria

PASS requires exact-PID multi-sample memory evidence, process-role attribution or an explicit `UNATTRIBUTED` result, system-pressure context, registered-worktree and Task-created-clone inventory, exact path/process correlation, a per-path cleanup manifest, complete safety accounting, and one evidence-based narrow recommendation.

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
- registered worktree and isolated-clone inventory;
- exact path-to-PID correlation table;
- disk-only versus RAM-supported findings;
- per-path cleanup manifest;
- classification;
- safety notes;
- recommended next action;
- what remains unproven.

Only this matching Codex report may change. Commit message must begin:

`report: CNX-20260822-011`

Never force-push. Stop after publishing the report.
