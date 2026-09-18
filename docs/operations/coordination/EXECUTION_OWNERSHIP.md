# Execution Ownership and Escalation Policy

Updated: 2026-09-18 ICT

## Standing model

Current execution preference is ChatGPT-first when the current ChatGPT session already has the tools and authority needed to complete the work safely.

- **ChatGPT:** default repository-capable executor, independent reviewer, coordinator, successor/rework task framer, and technical adjudication layer.
- **Hermes:** local/live machine executor for tasks that materially require the operator's environment, runtime, UI, filesystem, PowerShell, or other environment-specific access.
- **Human operator:** final authority for fresh intent and ungranted live/destructive/semantic decisions.

When Hermes is assigned, the execution/review behavior in `HERMES_CHATGPT_SINGLE_AGENT_PROTOCOL.md` still applies. Session reuse/new-session and model-strength preferences are defined in `SESSION_EXECUTION_MODEL_GUIDELINES.md`.

Historical Luna/Musethree tasks and reviews remain valid evidence. The old alternating dual-agent baton is retained only for historical interpretation.

## Primary technical ownership

If ChatGPT can safely perform the next repository/source/review/documentation step with its current tools, ChatGPT should do it directly instead of creating an unnecessary Hermes task.

When `ACTIVE.md` assigns a task to Hermes because local/live access is required, Hermes may perform the full technical loop authorized by that task:

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

ChatGPT is both a routine execution lane for tool-accessible repository work and the independent review/coordination layer.

ChatGPT handles:

- direct repository/source/documentation/coordination work that can be completed safely with current tools;
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

The actor that actually executes a bounded step owns its implementation evidence. For Hermes tasks, Hermes owns the primary local/live evidence package. ChatGPT owns independent review and acceptance/rework disposition and may also directly execute repository-capable work when no independent local executor is required. Evidence, not actor identity, determines acceptance.

A Hermes self-review may be included for quality control but never replaces ChatGPT independent review.
