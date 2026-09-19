# Coordination Channel Status

Status: `IN_PROGRESS`
State: `CNX427_EXTERNAL_INGRESS_AND_TAILSCALE_PROFILE_REPAIR`
Execution mode: `TDD_AND_BOUNDED_LIVE_REPAIR`
Task ID: `CNX-20260919-427`
Parent: `CNX-20260919-426`
Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`

## Current evidence

Discord:

- external Discord ingress is received by OpenClaw;
- both current traces fail in CNX `reply_dispatch` with `missing-run-id`;
- no current CNX Ticket/model run is created;
- OpenClaw later releases the stale lane via watchdog.

Tailscale remote UI:

- HTTPS/WebSocket transport reaches the Gateway;
- `gateway.tailscale.mode=serve`;
- session RPCs fail with `AUTHENTICATED_PROFILE_UNAVAILABLE`;
- OpenClaw source shows this state means GitHub identity sync is present while `authenticatedUserProfile` is still absent.

## Work in progress

Track A: RED test and minimal deferred-admission repair.

Track B: durable identity/profile inspection and narrow OpenClaw/Tailscale profile convergence repair.

No security relaxation, provider routing change, force push, tag, release, or main mutation is authorized.
