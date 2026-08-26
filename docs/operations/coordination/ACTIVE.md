# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_SUPPORTED_INSTALL_OVER_SEMANTIC_CANDIDATE_PARITY`
Current authorization: `ONE_SUPPORTED_INSTALL_OVER_AND_LIVE_PARITY_AUTHORIZED`
Task ID: `CNX-20260826-081`
Updated: 2026-08-26 23:56 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260826-081-install-over-semantic-candidate-live-parity.md`](tasks/CNX-20260826-081-install-over-semantic-candidate-live-parity.md)

## Task 080 acceptance

Task 080 reported:

`PASS_CRASH_SAFE_DELIVERY_FENCING_CLOSED`

Implementation HEAD:

`70d02e76233ca1084da445d488f88b628455f4aa`

Report HEAD:

`1798bfd4bb2ef69fb579b151f5d0423f0fc196f8`

Independent review:

Decision: `ACCEPT`

Disposition:

`ACCEPT_CRASH_SAFE_DELIVERY_FENCING_CLOSED`

Review path:

[`reviews/CNX-20260826-080-close-crash-safe-lock-and-exact-delivery-run-fencing.md`](reviews/CNX-20260826-080-close-crash-safe-lock-and-exact-delivery-run-fencing.md)

## Accepted semantic candidate

The exact production candidate authorized for the live parity gate is:

`70d02e76233ca1084da445d488f88b628455f4aa`

It carries the accepted Task-078/079/080 behavior:

- owner/session-bound internal delivery-marker fail-closed behavior;
- Ticket admission/routing idempotency;
- one Ticket/Host timeout recovery authority;
- direct model-call lease ordering/fencing;
- registered direct semantic lifecycle and duplicate convergence;
- crash-safe workflow completion scheduling/binding/settlement;
- atomic complete-record canonical completion-lock publication;
- exact workflow and Ticket outbox delivery-run settlement fencing;
- owner/CLI/subagent negative security coverage;
- provider disposition `PROVIDER_READY_WITH_FRESH_OWNER_SESSION` from the two already-consumed Task-078 direct Ollama probes.

No additional provider probe is required or authorized.

## Current live baseline before Task 081

Accepted live production remains Task-075 source:

`79b51ed06363f6e8862c491ee0a313ddb412c806`

It is MANAGED with previously accepted Gateway/Ollama health, product-owned Supervisor runtime, one canonical v0.9.3 plugin generation, ownership verification and no-flash behavior.

Task 076's timed-out CLI-targeted session is historical and must not be reused. The final semantic owner surface is Dashboard/WebChat, not `openclaw agent --session-key agent:main:main`.

## Task 081 live authorization

Task 081 may perform exactly one normal supported install-over from the exact candidate source and installer-supported ownership-safe lifecycle actions inherent to that install-over.

It must prove:

- pre-install baseline has not drifted unexpectedly;
- recovery preflight/ownership is existing/non-fresh and classification is `upgrade`;
- exactly one supported normal `scripts/install.ps1 -Workspace C:\Users\CDQ-P\.openclaw\workspace` install-over succeeds;
- no fresh transaction is started;
- live canonical plugin package is byte/tree-equivalent to the accepted candidate artifact;
- one canonical plugin generation wins runtime resolution;
- ownership/runtime/launcher/Scheduled Task/AGENTS/SQLite state remains correct;
- at least five natural PT1M Supervisor ticks remain no-flash;
- MANAGED/Gateway/Ollama/plugin health remains good;
- a fresh authenticated Dashboard/WebChat owner surface is proven/prepared without sending a prompt.

## Absolute semantic fence

Task 081 must send **zero** semantic/user messages.

No Dashboard/WebChat chat message, no `chat.send`, no CLI semantic run, no `sessions_send`, no channel send, no direct Ollama probe, no synthetic Ticket creation, no model/provider/timeout change, no uninstall/reset/clean reinstall, no reboot, merge, tag or release.

If a fresh Dashboard session can only be created by the first user message, do not fabricate it; record that the final semantic task must create it on first send through the proven owner surface.

## Successor gate

Only after Task 081 independently passes may a separate final semantic task authorize exactly one fresh Dashboard/WebChat owner message and prove:

`owner message -> Ticket accepted before provider -> Ollama inference -> response_ready -> exact owner/run delivery -> delivery_confirmed -> completed -> visible response`.
