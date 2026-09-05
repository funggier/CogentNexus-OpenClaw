# Hermes + ChatGPT Single-Agent Coordination Protocol

Updated: 2026-09-05 ICT

## Authority and precedence

This is the standing coordination policy requested by the human operator for future CogentNexus-OpenClaw work.

For work after this policy is published, this protocol supersedes the previous `HERMES_DUAL_AGENT_BATON_PROTOCOL.md` alternating Luna/Musethree model. Historical tasks, reports, reviews, and actor names remain valid evidence under the contract that produced them.

GitHub remote state is authoritative. The human operator remains final authority.

Read `DELAYED_RECHECK_QUEUE.md` together with this protocol for asynchronous CI/external waits.

## Roles

- **Hermes — sole routine execution agent.** Hermes owns repository/source/test/CI implementation work that is explicitly assigned in `ACTIVE.md` and within the task hard fences.
- **ChatGPT — routine independent reviewer, coordinator, and decision layer.** ChatGPT reviews Hermes reports, verifies critical evidence, decides acceptance/rework, frames successor tasks, and adjudicates authority boundaries.
- **Human operator — final authority.** Human intent controls new semantic/product direction and any live/destructive/semantic authority that is not already explicit.

Luna and Musethree are historical Hermes actor labels only after this protocol. New coordination state should use `Hermes` unless a historical artifact is being cited verbatim.

## Core loop

```text
Human / ChatGPT establishes or updates the goal
  -> ChatGPT opens/assigns a bounded task to Hermes
Hermes executes the assigned task
  -> if CI/external gate pending: Hermes self-wakes/rechecks until terminal
  -> Hermes publishes evidence-rich report
  -> state becomes WAITING_FOR_CHATGPT_REVIEW
ChatGPT independently reviews the report
  -> ACCEPT: close task and either open the next bounded task for Hermes or stop at an authority/final boundary
  -> REWORK: open a bounded repair/rework task for Hermes
  -> BLOCKED: publish decision packet and obtain required human authority/intent
  -> FINAL: perform project-level final acceptance when appropriate
```

Hermes MUST NOT independently review or accept its own report. A Hermes self-check may support evidence quality but cannot satisfy independent acceptance.

## Hermes task authority

Inside an assigned task Hermes may perform the full technical loop that the task authorizes:

- fresh remote synchronization and race checks;
- root-cause investigation;
- repository/source/upstream analysis;
- TDD RED -> minimal fix -> GREEN for production repair;
- tests/build/package/schema/plugin validation;
- exact-SHA GitHub Actions inspection;
- evidence/provenance analysis;
- local/live proof only when explicitly authorized by the active task;
- publication of the matching report.

Hermes does not need a ChatGPT micro-decision for routine implementation details already inside the task boundary.

## Required report-to-review handoff

When an assigned task is complete, including required asynchronous gates:

1. Hermes race-checks remote authority.
2. Hermes publishes the final `reports/*.md` evidence artifact.
3. Hermes updates `ACTIVE.md` / `STATUS.md` to `WAITING_FOR_CHATGPT_REVIEW` or a more specific ChatGPT-review state.
4. The handoff records exact Task ID, report path/publication HEAD, exact candidate/source SHA, required CI status, hard fences, and residual uncertainty.
5. Hermes stops mutation of the completed task.
6. The human may notify ChatGPT, or ChatGPT may inspect the state directly when already present in the conversation.

There is no routine peer-bot handoff and no requirement to invoke Luna/Musethree alternately.

## ChatGPT review and successor authority

ChatGPT independently verifies the report using progressive depth:

1. current remote authority and lineage;
2. task contract and hard-fence compliance;
3. exact candidate diff / critical implementation claims;
4. TDD or other required validation evidence;
5. exact-SHA CI terminal result;
6. live evidence when the task claims live acceptance.

If accepted, ChatGPT may create the next bounded task for Hermes when it is a deterministic continuation of already-approved intent and does not require inventing new human authority.

If a source/report defect is found, ChatGPT may open a bounded rework task for Hermes.

If the next step requires fresh user intent or new live/destructive/semantic authority, ChatGPT must not invent it. Set a durable waiting/decision state and ask the human operator only for the missing authority.

## Asynchronous dependency continuity

Queued/in-progress GitHub Actions or another deterministic asynchronous dependency is an in-task wait, not task completion.

Hermes retains task ownership and follows `DELAYED_RECHECK_QUEUE.md`:

- default GitHub Actions cadence about 5 minutes;
- persistent delayed wake when available;
- fresh remote authority on every wake;
- stale wake exits without mutation;
- no heartbeat commits;
- no blind rerun of deterministic failures;
- no repeated live/semantic side effect while waiting.

Hermes does not hand the task to ChatGPT merely because CI is still running. The handoff occurs after required gates are terminal or when a genuine decision/authority boundary blocks further progress.

## Mandatory ChatGPT / human boundaries

Hermes must stop and hand control to ChatGPT when:

- the assigned task is complete and needs independent acceptance;
- evidence is materially contradictory and no safe bounded diagnostic remains;
- a new architecture/product/semantic direction must be chosen;
- a successor needs authority not already granted;
- live/destructive/semantic side effects exceed the current task fence;
- irreversible release/tag/default-branch promotion is proposed without authority;
- the overall goal appears complete and project-level final acceptance is required.

ChatGPT may resolve technical/review decisions itself. When the missing input is specifically human consent or fresh semantic intent, ChatGPT records that boundary and asks the human operator.

## Final-authority provenance guard

Hermes may prepare an acceptance proposal and evidence packet but MUST NOT write that ChatGPT or the human approved something unless that real authority has actually issued the decision.

Hermes MUST NOT:

- change a pending ChatGPT/human decision into final acceptance on their behalf;
- write `ChatGPT accepts`, `ChatGPT authorized`, `human approved`, or equivalent without real provenance;
- fabricate a future approval because the likely answer seems obvious;
- continue past a mandatory authority boundary.

## Race prevention

- GitHub remote is authoritative.
- Only the actor named in the active coordination state mutates the active task.
- Fetch before every write and delayed-wake continuation.
- If remote moved, re-read `ACTIVE.md` / `STATUS.md` and do not overwrite newer work.
- Preserve fast-forward history; never force push.
- A completed report is a replay fence for external side effects.

## Live and semantic authority

Single-agent coordination changes who performs/reviews work, not what side effects are authorized.

Install/uninstall/reset, Gateway/provider/service lifecycle, DB/durable-state mutation, recovery replay/redelivery/disposition, OpenClaw session delete/reset, Discord/Dashboard/API semantic sends, release/tag/default-branch promotion, and similar disruptive actions still require explicit task authority and all stated preconditions.

Unknown owner/user intent is never inferred from a generic continuation request.
