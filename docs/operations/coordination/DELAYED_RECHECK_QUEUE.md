# Hermes Delayed Recheck Queue

Updated: 2026-09-05 ICT

## Purpose

Prevent Luna or Musethree from becoming dormant merely because an authorized task is waiting on an asynchronous external dependency such as GitHub Actions.

The default GitHub Actions wait cadence is **5 minutes**. Waiting is not task completion and does not transfer the baton by itself.

This policy is subordinate to the active task's hard fences. It never creates new live, destructive, semantic, release, or user-intent authority.

## Default rule

When the current baton holder reaches a point where the only remaining requirement is an asynchronous condition expected to change without further product mutation, the actor MUST create a persistent delayed recheck instead of simply stopping and waiting for the human to wake it.

For GitHub Actions:

```text
observe required run/check still queued or in_progress
  -> enqueue one wake for +5 minutes
  -> end the current compute turn
  -> wake
  -> fetch fresh remote authority and exact CI state
  -> terminal? continue
  -> still queued/in_progress? enqueue another +5 minute wake
  -> repeat
```

Do not implement this as an in-process `sleep 300` if a persistent Hermes queue/scheduled wake is available. The wake should survive the current chat/run ending.

## Baton retention

The actor waiting on CI keeps the baton until the required asynchronous gate reaches a usable terminal state or another durable coordination write explicitly transfers ownership.

Pending CI alone is **not** a reason to:

- publish a final PASS report;
- hand the baton to the peer;
- set `WAITING_FOR_CHATGPT`;
- ask the human to send another manual `ต่อ`;
- repeat the operation that originally triggered the CI.

The peer must not take over merely because the waiting actor is sleeping between rechecks.

## Durable wait identity

A wait episode must be bound to immutable enough identity to reject stale wakes:

- repository and branch;
- Task ID;
- baton owner (`Luna` or `Musethree`);
- exact candidate/HEAD SHA being checked;
- required workflow/check/run identifiers when known;
- dependency class, e.g. `github-actions`;
- recheck interval (`PT5M` by default);
- a dedupe key equivalent to `task-id:head-sha:dependency`.

At most one pending delayed wake should exist for the same dedupe key. Re-enqueue replaces or supersedes an older equivalent wake rather than multiplying wake jobs.

GitHub coordination may record entry into a wait state such as `WAITING_FOR_CI_RECHECK`, but unchanged five-minute rechecks should not create a new Git commit each time. The persistent wake queue/scheduler is the timing mechanism; GitHub remains the authority for task/baton/HEAD state.

## Wake algorithm

Every delayed wake MUST start from fresh authority:

1. fetch the remote working branch;
2. read current `ACTIVE.md`, `STATUS.md`, baton owner, exact task, report/review state;
3. compare the current task/HEAD/dependency identity with the queued wake identity;
4. if the branch, task, baton owner, or relevant candidate has changed, classify the wake as stale and exit without mutation;
5. if a matching completion/report already proves the action finished, do not repeat it;
6. query GitHub Actions/check state for the exact required SHA/run IDs;
7. choose exactly one branch below.

### A. All required checks terminal success

- clear/consume the wait entry;
- resume the same actor's task/review at the post-CI step;
- perform remaining evidence checks;
- only then publish the final report/review and hand off normally.

### B. Any required check terminal failure/cancelled/timed_out/action_required

- stop passive waiting;
- inspect the exact failing workflow/job/log evidence;
- classify product/test failure vs CI/tooling/infrastructure failure;
- perform root-cause/TDD repair when already authorized;
- use only bounded CI retry allowed by standing/task policy;
- never convert a terminal failure into another blind five-minute wait.

### C. Required checks still queued/in_progress/pending

- perform no product/runtime side effect;
- enqueue exactly one new wake for approximately +5 minutes using the same dedupe identity;
- end the current compute turn.

### D. Expected check/run missing for the exact SHA

Do not wait forever for an object that was never created. Perform bounded diagnosis of workflow triggering/path filters/check-suite state. If the cause can be corrected within current repository/CI authority, correct it. If new authority is needed, follow normal peer review/escalation rules.

## Stalled-CI behavior

A long-running but genuinely `queued`/`in_progress` workflow does not require the human merely because time passed. Continue five-minute rechecks.

After approximately **12 unchanged rechecks / 60 minutes** with no meaningful state change, additionally enter `CI_STALLED_DIAGNOSIS` for one bounded diagnostic pass while retaining the delayed recheck loop. Inspect, as available:

- workflow/run state and attempt;
- job queue/start timestamps;
- runner availability symptoms;
- GitHub outage/service evidence if available;
- cancellation/action-required/stale conditions;
- whether expected jobs were created for the exact SHA.

If the run is still legitimately active after diagnosis, keep rechecking every five minutes. Do not escalate solely because the run is slow.

Escalate only when a decision/authority boundary in `HERMES_DUAL_AGENT_BATON_PROTOCOL.md` is actually reached.

## Bounded CI retry

Automatic retry is for clearly transient tooling/harness/CI failures only and must remain bounded.

- Never blindly retry a deterministic test/product failure; repair first.
- Never retry an installer/runtime/semantic side effect under the label of CI retry.
- Do not create an unbounded rerun loop.
- A retry must be tied to the same exact evidence/cause and recorded in the final report.

If the active task contains stricter retry limits, the task wins.

## Supported wait classes

This mechanism may also be used for other non-semantic asynchronous dependencies when the next action is deterministic and already authorized, for example:

- artifact publication/availability;
- package indexing after an already-authorized publish step;
- delayed external validation status;
- a peer handoff watcher waiting for a known GitHub state transition.

The interval may differ only when a task/policy explicitly requires another cadence. GitHub Actions defaults to 5 minutes.

## Do not use delayed recheck for

Do not poll around a decision that requires human/ChatGPT authority. Immediate escalation is required instead when waiting for:

- fresh user semantic intent or consent;
- architecture/product-direction choice;
- approval for a broader destructive/live action;
- release/promotion authority not already granted;
- final project acceptance.

Do not turn `WAITING_FOR_CHATGPT` or `GOAL_COMPLETE_PENDING_CHATGPT_FINAL` into an automatic five-minute polling loop.

## Persistence fallback

Preferred order:

1. Hermes persistent delayed queue / scheduled wake;
2. an already-enabled Luna/Musethree watcher capable of polling at approximately five-minute cadence;
3. durable GitHub wait state plus the narrowest available scheduler that can wake the same actor.

If no persistent wake mechanism exists at all, record `WAIT_RECHECK_WAKE_UNAVAILABLE` with the exact missing capability instead of pretending a wake was scheduled.

## Core invariant

```text
Asynchronous waiting may suspend compute,
but it must not silently terminate coordination continuity.
```
