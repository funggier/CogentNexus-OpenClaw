# Hermes Dual-Agent Baton Protocol

Updated: 2026-09-05 ICT

## Authority and precedence

This is the standing coordination policy requested by the human operator for the Hermes agents **Luna** and **Musethree**.

For future work after this file is published, this protocol supersedes older coordination language that requires every executor report to stop for ChatGPT review or requires ChatGPT to open every successor task. Historical task/review evidence remains valid under the contract that produced it.

GitHub remote state remains authoritative. The human operator remains final authority.

Read `DELAYED_RECHECK_QUEUE.md` together with this protocol for asynchronous CI/external waits.

## Roles

- **Luna — primary agent.** Default first baton holder after a human/ChatGPT decision or a workflow restart.
- **Musethree — supporting/alternate agent.** Full technical authority when the baton is assigned to Musethree, within the active task's hard fences.
- **ChatGPT — escalation/adjudication layer.** Not a routine hop between tasks. ChatGPT is used when the two-agent loop cannot make a safe, uniquely authorized decision, when a new human-intent/policy decision is required, or when the project reaches a terminal acceptance boundary.
- **Human operator — final authority.** Provides intent and is notified when ChatGPT escalation/final review is required.

Luna and Musethree are peers for evidence quality. `primary` means Luna is the default restart/entry actor, not that Musethree may ignore an assigned task or that Luna may overwrite Musethree's work.

## Core baton loop

```text
Luna executes assigned task
  -> if async gate pending: Luna self-wakes/rechecks until terminal
  -> publishes report
  -> hands baton to Musethree
Musethree independently reviews Luna's report
  -> if async review gate pending: Musethree self-wakes/rechecks until terminal
  -> if decision is clear and authorized, opens/executes the next bounded task
  -> publishes report
  -> hands baton to Luna
Luna independently reviews Musethree's report
  -> ...repeat...
```

The actor receiving the baton MUST review the predecessor actor's report before opening or executing a successor based on it.

An actor MUST NOT independently review or accept its own task report.

## Asynchronous dependency continuity

Waiting for GitHub Actions or another deterministic asynchronous dependency is an **in-task wait**, not a handoff or terminal stop.

The waiting actor retains baton ownership and follows `DELAYED_RECHECK_QUEUE.md`:

- default GitHub Actions cadence: approximately 5 minutes;
- use a persistent delayed wake/scheduler, not a fragile long in-process sleep when avoidable;
- re-fetch remote authority on every wake;
- reject stale wakes when task/HEAD/baton changed;
- if still queued/in-progress, enqueue one new +5 minute wake;
- if terminal success, resume the same task/review;
- if terminal failure, inspect and repair/route according to evidence rather than blindly waiting again.

A final report/review that depends on required CI must not be declared PASS while those required checks remain non-terminal.

Do not send the baton to the peer merely to make the peer wait for the same unfinished CI unless a task explicitly assigns independent parallel work that does not violate ownership.

## Required handoff sequence

When an actor actually finishes an assigned task:

1. Complete validation, including all required asynchronous gates, and publish the matching `reports/*.md` artifact.
2. Re-fetch/race-check the remote branch before the final coordination write.
3. Update `ACTIVE.md` and `STATUS.md` to a durable handoff state naming:
   - completed Task ID;
   - report path and exact report/publication HEAD;
   - `Handoff from` actor;
   - `Next actor` peer;
   - hard fences that remain in force.
4. Invoke/call the other Hermes agent through the available Hermes handoff mechanism when that capability exists.
5. The finishing actor stops mutating that completed task after handoff. The peer owns the next coordination decision.

If direct peer invocation is temporarily unavailable, the durable GitHub handoff state remains authoritative and the peer's watcher/manual pickup may consume it. Never claim a direct call occurred unless it actually did.

## Peer review and successor authority

After receiving the baton, the peer must fetch fresh remote truth and independently review the predecessor report using the verification packet and exact evidence.

The peer may then continue without ChatGPT when **all** of the following hold:

- the next action is a clear continuation of the already-approved project goal;
- the action is supported by the predecessor evidence/review result;
- required authority is already present in standing policy, operator intent, or a task-specific fence;
- there is one safe bounded successor or a safe rework/diagnostic successor;
- the successor does not require guessing current user semantic intent;
- the successor does not silently broaden destructive/live/semantic authority;
- race/lineage and exact-candidate requirements can be stated precisely.

The receiving peer may publish the independent review, create/update the bounded successor task and `ACTIVE.md`/`STATUS.md`, assign the successor to itself, and execute it. This is the normal baton continuation path.

## When to continue autonomously

Examples that normally stay inside the Luna/Musethree loop when already within approved boundaries:

- source/test/CI repair;
- root-cause investigation;
- TDD RED -> minimal fix -> GREEN;
- evidence/provenance requalification;
- bounded read-only live preflight;
- deterministic successor after an accepted report;
- rework required by a reviewer finding;
- installer/runtime validation explicitly authorized by a successor task whose safety preconditions are proven;
- five-minute delayed rechecks of queued/in-progress GitHub Actions.

## Mandatory escalation to ChatGPT

The peer must stop fail-closed and set `ACTIVE.md` / `STATUS.md` to `WAITING_FOR_CHATGPT` (or a more specific `*_ESCALATE_TO_CHATGPT` state) when any of these apply:

- Luna and Musethree cannot determine a safe next action from durable evidence;
- evidence is materially contradictory and no bounded diagnostic can resolve it safely;
- a new architecture/policy/semantic direction must be chosen;
- the action requires fresh human intent or consent that is not already established;
- a live/destructive/semantic side effect would exceed existing explicit authority;
- multiple materially different successors are plausible and choosing among them changes product direction or user-visible semantics;
- an irreversible release/promotion/default-branch boundary is reached without standing authority;
- the overall acceptance goal appears complete and final disposition should be confirmed.

Ordinary CI waiting, even when long, is not by itself an escalation condition. Use delayed recheck plus stalled-CI diagnosis first.

The escalation state must contain a compact decision packet: exact HEAD, current task/report/review, the decision that cannot be made, evidence for each viable option, hard fences, and a recommended question/decision for ChatGPT.

Then the agent must tell the human operator that the workflow needs ChatGPT and ask the operator to notify ChatGPT. The agents must not continue past that escalation boundary until ChatGPT/human authority is published durably.

## Terminal completion

When the receiving peer independently concludes that the overall stabilization/final-acceptance goal is complete:

1. publish the final peer review/evidence;
2. set state to `GOAL_COMPLETE_PENDING_CHATGPT_FINAL`;
3. do not invent additional work merely to keep the loop running;
4. notify the human operator to contact ChatGPT for final project-level acceptance/closure.

This is the intended final handoff to ChatGPT.

## Race prevention

- Only the actor named by the current baton/active task may perform task mutations.
- Before every push/write and every delayed wake continuation, fetch remote HEAD and verify expected ancestry/state.
- If another actor has advanced the branch, do not overwrite it; re-read coordination state and obey the new baton owner.
- Never force-push to resolve a baton race.
- A completed report is a replay fence: do not repeat completed external side effects.
- A delayed wake is not authority; it is only permission to re-check whether the already-authorized task can continue.

## Live and semantic authority

The baton protocol changes **who decides the next bounded task**, not what side effects are allowed.

Install/uninstall/reset, Gateway/provider/service lifecycle changes, DB/durable-state mutation, recovery replay/redelivery/disposition, Dashboard/Discord/API semantic sends, release/tag mutation, and other disruptive actions still require explicit task authority and all stated preconditions.

Unknown owner intent is never inferred from the existence of this autonomous loop or from repeated delayed wakes.
