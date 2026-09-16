# CNX-366 — Dashboard Fresh Session Establishment

Status: `READY_FOR_HERMES`
Parent: `CNX-20260915-365`
Base: `CNX366_DASHBOARD_FRESH_SESSION_ESTABLISHMENT`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
Executor: `Hermes`
Reviewer: `ChatGPT`
Human final authority: `Operator`

## Objective

Establish and independently verify a genuinely fresh, blank Dashboard conversation and its exact UI/session identity after CNX-365 ended `UNRESOLVED/BLOCKED` at the evidence boundary. This task is preparation only. It must not perform CNX-365 again and must not send any semantic message.

## Required preparation proof

Before any future semantic authorization, the retained read-only evidence must show all of the following:

1. A fresh blank Dashboard conversation was established, not an existing or prefilled conversation.
2. The exact Dashboard session key and/or session ID is observable and recorded before any semantic request.
3. The rendered conversation has no prior turns and the composer is empty at the fresh-session boundary.
4. The composer target and focus are independently observable from a fresh UI capture or equivalent independent control evidence; a presumed coordinate or unverifiable click is insufficient.
5. Provider and model selection are observable and recorded before any semantic request.
6. Preparation produced zero model/OpenAI requests and zero Dashboard semantic requests.
7. Runtime mutation count is zero, including no lifecycle, installer, controller, provider/auth/routing, hook/main, or release action.

If any required identity or blank-session condition cannot be proven, classify the task `BLOCKED` and stop. Do not send a test message to resolve ambiguity.

## Allowed scope

- Read current GitHub authority and task state.
- Use bounded UI observation/control solely to establish or verify a fresh blank Dashboard session, without sending a message.
- Capture exact session/UI/provider/model identity and read-only before/after request and mutation counts.
- Publish the matching preparation report and stop.

## Forbidden scope

- Do not retry, resend, or otherwise re-run CNX-365 semantic execution.
- Do not type or send the CNX-365 exact semantic message or any other semantic message.
- Do not click Send, press Enter, invoke a model, or issue any Dashboard/model/API semantic request.
- Do not mutate runtime state or enable, disable, start, stop, restart, reinstall, normalize, or repair anything.
- Do not edit controller.json, provider/auth/routing, hooks, main, or release/tag state.
- Do not modify CNX-360 through CNX-365 historical task/report records.
- Do not force-push or rewrite history.

## Deliverable and stop gate

Publish a report under `docs/operations/coordination/reports/` with the exact branch/head, fresh-session proof, session key/ID, blank conversation/composer proof, independent composer-target/focus proof, provider/model identity, zero-request and zero-mutation accounting, and the explicit no-semantic-request boundary. Stop after publication. Semantic execution requires a separate explicit authorization and must not be performed by CNX-366.
