# Execution Ownership and Escalation Policy

Updated: 2026-09-05 ICT

## Standing model

Future Hermes coordination uses the single-agent model in `HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md`.

- **Hermes:** sole routine execution agent for new tasks.
- **ChatGPT:** independent reviewer, coordinator, successor/rework task framer, and technical adjudication layer.
- **Human operator:** final authority for fresh intent and ungranted live/destructive/semantic decisions.

Historical Luna/Musethree tasks and reviews remain valid evidence. The old alternating dual-agent baton is retained only for historical interpretation.

## Primary technical ownership

When `ACTIVE.md` assigns a task to Hermes, Hermes may perform the full technical loop authorized by that task:

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

## Review ownership

Hermes cannot independently accept its own completed report.

After required gates are terminal, Hermes publishes its report and hands the task to ChatGPT using `WAITING_FOR_CHATGPT_REVIEW` or an equivalent state.

ChatGPT owns independent acceptance/rework review by checking current remote authority, lineage, task contract, critical diff/evidence, required tests/CI, hard-fence compliance, and live evidence where claimed.

## Successor framing

After accepting a Hermes report, ChatGPT may create the next bounded task for Hermes when it is a deterministic continuation of already-approved intent and stays inside established authority.

If rework is needed, ChatGPT opens a bounded repair/rework task for Hermes.

If the next step requires new human intent or authority, ChatGPT records the missing decision and asks the human operator rather than inventing consent.

## ChatGPT lane

ChatGPT is a routine review hop under this model, not merely an exceptional escalation layer.

ChatGPT handles:

- independent review of every completed Hermes task report;
- acceptance/rework disposition;
- bounded successor task framing;
- contradictory evidence adjudication;
- architecture/policy/semantic decisions when sufficient authority already exists;
- project-level final acceptance;
- identification of any missing human consent/intent.

## Local/live authority

The coordination model does not broaden side-effect authority. Explicit task authorization is still required for install/update/uninstall/reset, Gateway/provider/controller/service mutation, recovery replay/redelivery/disposition, DB/durable-state mutation, OpenClaw session delete/reset, Dashboard/Discord/API semantic sends, releases/tags/default-branch promotion, hardware/permission changes, and similar operations.

## Race prevention

- remote branch is authoritative;
- only the currently assigned execution/review actor mutates its assigned coordination phase;
- fetch before every write/push;
- preserve fast-forward history;
- never force-push;
- never reset away unknown local/remote work;
- if remote moved, re-read `ACTIVE.md` / `STATUS.md` before continuing;
- a matching completed report prevents repeating external side effects.

## Evidence ownership

Hermes owns implementation and the primary evidence package. ChatGPT owns independent review and acceptance/rework disposition. Evidence, not actor identity, determines acceptance.

A Hermes self-review may be included for quality control but never replaces ChatGPT independent review.
