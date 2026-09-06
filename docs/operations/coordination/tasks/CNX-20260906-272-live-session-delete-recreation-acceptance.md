# CNX-20260906-272 — Live Session Delete/Recreation Acceptance

## Status

`WAITING_FOR_USER_AUTHORITY`

Parent: `CNX-20260906-271`
Executor after authorization: `Hermes`
Reviewer: `ChatGPT`

## Objective

Live-accept the Tasks263–265 lifecycle repair on Windows/OpenClaw by proving that a manually deleted OpenClaw Discord owner session is tombstoned safely and that the first owner message in the genuinely new lifecycle is admitted successfully without requiring a second-message workaround.

## Required acceptance semantics

A successful bounded live proof must establish:

1. pre-state exact `sessionKey`, current `sessionId`, generation, and relevant Ticket/recovery/delivery counts;
2. one authorized manual OpenClaw session Delete/reset boundary for the chosen sacrificial owner session;
3. old lifecycle becomes tombstoned/revoked and cannot regain authority;
4. one authorized first semantic owner message after recreation creates/uses a genuinely new OpenClaw `sessionId` on the same canonical key;
5. that first message is admitted on its first attempt and gets a fresh Ticket/reply path; no second-message workaround is allowed;
6. CNX generation advances exactly once for the new lifecycle;
7. delayed/stale old lifecycle identity cannot hijack the new active lifecycle;
8. no old recovery/delivery/workflow evidence leaks into the new lifecycle;
9. Gateway/provider remain healthy and no unrelated lifecycle mutation is performed.

## Safety topology requirement

Prefer an isolated/sacrificial Discord owner session with no nonterminal historical work if an exact supported topology is available. Do not manufacture a different topology that fails to exercise the same OpenClaw `session_end(reason="deleted")` -> new `sessionId` -> first-turn `before_agent_run` contract.

The existing session containing old Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` must NOT be deleted unless the human operator explicitly authorizes abandoning/cancelling that old session work as an unavoidable consequence of deleting that exact owner session. Its owner intent remains unproven.

## Authority required

No live execution is authorized by opening this task.

Fresh explicit human authority is required for whichever exact topology is selected, including:

- one live OpenClaw session Delete/reset;
- the resulting CNX lifecycle/session/Ticket state changes;
- one bounded semantic Discord owner message needed to prove first-turn recreation;
- if the chosen existing owner session contains the old unproven-intent Ticket, explicit acknowledgement that deleting that session will cancel/abandon its old nonterminal work.

## Still forbidden unless explicitly included in fresh authority

```text
uninstall/reset product-wide                     = 0
extra semantic sends beyond bounded proof        = 0
manual SQLite edits                              = 0
manual Ticket dispose/redeliver/replay            = 0
Scheduled Task cadence/enablement changes        = 0
ad-hoc process/service kills                     = 0
release/tag/default-branch promotion             = 0
force push/history rewrite                       = 0
```

## Completion after authorization

Hermes publishes a bounded live report and sets coordination to `WAITING_FOR_CHATGPT_REVIEW`. If the selected safe topology cannot be proven before mutation, stop without deleting or sending and report the blocker.
