# Execution Ownership and Escalation Policy

Updated: 2026-09-05 ICT

## Standing model

Future Hermes coordination uses the dual-agent baton model in `HERMES_DUAL_AGENT_BATON_PROTOCOL.md`.

- **Luna:** primary/default entry agent.
- **Musethree:** supporting/alternate agent.
- **Current baton holder:** sole task-mutation owner for the assigned task.
- **Peer actor:** independent reviewer of the predecessor actor's report and next baton holder.
- **ChatGPT:** escalation/adjudication/final-acceptance layer, not a mandatory reviewer between every task.
- **Human operator:** final authority.

Historical reports/reviews remain valid. Where older coordination files say that ChatGPT must review/open every successor, the dual-agent baton protocol supersedes that rule for future tasks.

## Alternating ownership

A task executed by Luna must hand off to Musethree. A task executed by Musethree must hand off to Luna.

The receiving peer:

1. fetches fresh remote authority;
2. independently reviews the predecessor report;
3. publishes the durable review;
4. if the next action is clear and already authorized, creates a bounded successor assigned to itself and continues;
5. after its own report, hands the baton back.

No actor may independently accept its own report.

## Primary technical ownership

The assigned actor may perform the full technical loop authorized by the task:

- fresh remote synchronization;
- source/repository/upstream investigation;
- root-cause analysis;
- TDD RED -> minimal fix -> GREEN;
- source/test/config/installer/CI repair inside scope;
- targeted/full validation and exact-SHA Actions inspection;
- package/build/plugin/schema evidence;
- local/runtime/lifecycle proof only when explicitly authorized;
- risk and residual-uncertainty analysis;
- matching evidence-rich report publication.

## Successor autonomy

The peer may open and execute a successor without ChatGPT only when it is a deterministic continuation of approved intent, bounded by existing authority, and does not require guessing semantic/user intent or widening disruptive authority.

Safe rework and bounded diagnostics may also continue in the peer loop.

## ChatGPT lane

ChatGPT is called when:

- the peer cannot determine one safe authorized successor;
- evidence or contracts conflict materially;
- a new architecture/policy/semantic choice is required;
- fresh human intent/consent is needed;
- a disruptive/live/semantic boundary lacks explicit authority;
- project-level final acceptance/closure is reached.

The escalation must be durable in `ACTIVE.md` / `STATUS.md` and include a concise decision packet.

## Local/live authority

The baton protocol does not broaden side-effect authority. Explicit task authorization is still required for install/update/uninstall/reset, Gateway/provider/controller/service mutation, recovery replay/redelivery/disposition, DB/durable-state mutation, Dashboard/Discord/API semantic sends, releases/tags, hardware/permission changes, and similar operations.

## Race prevention

- remote branch is authoritative;
- only current baton holder mutates the active task;
- fetch before every write/push;
- preserve fast-forward history;
- never force-push;
- never reset away unknown peer/local work;
- if remote moved, re-read baton ownership before continuing;
- a matching completed report prevents repeating external side effects.

## Evidence ownership

The executing actor owns implementation and the primary evidence package. The receiving peer owns independent review of that predecessor report. Evidence, not actor identity, determines acceptance.

If an actor must review work it authored, it must be labeled self-review and cannot satisfy a requirement for independent peer review.
