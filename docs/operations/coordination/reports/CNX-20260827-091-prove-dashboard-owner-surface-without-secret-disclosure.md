# CNX-20260827-091 — Prove Dashboard Owner Surface Without Secret Disclosure

Result: `PASS_DASHBOARD_OWNER_SURFACE_READY_NO_SECRET_DISCLOSURE`

Phase-D readiness token: `DASHBOARD_OWNER_SURFACE_READY`

Phase-E fresh-session token: `DASHBOARD_OWNER_SURFACE_READY_FIRST_SEND_CREATES_SESSION`

## Execution and publication

- Execution HEAD before report: `4f707b14a465e9130187629be160934ed6208e23`
- Installed OpenClaw: `2026.7.1-2 (0790d9f)`
- Product source commit: none
- This task used one report-only commit.
- No installer, reset, uninstall, manual repair, config mutation, provider mutation, or model/runtime mutation occurred.

## Installed-source findings

The exact installed Control UI documentation and runtime behavior establish:

- the page is served by the Gateway on `http://127.0.0.1:18789/`;
- the UI connects directly to the Gateway WebSocket;
- authentication is supplied during the WebSocket handshake;
- a paired browser profile is remembered and does not require a new approval;
- `sessions.list` is a read-only RPC;
- a fresh Dashboard/WebChat session is created by the UI flow and its first non-command message supplies the generated title.

No newer or alternate OpenClaw source was used for this determination.

## Authentication/handoff path

The existing paired Firefox browser profile was reused. No pairing approval was needed and no new pairing request was created.

Non-secret paired-device metadata:

- client: `openclaw-control-ui`
- client mode: `webchat`
- role: `operator`
- effective scopes: `operator.admin`, `operator.read`, `operator.write`, `operator.approvals`, `operator.pairing`
- last-seen reason: `device-token-auth`
- pending pairing requests: `0`

Credential accounting:

- shared token/password value read: `0`
- credential value copied: `0`
- credential value entered by the agent: `0`
- credential-bearing URL or command persisted: `0`
- credential-bearing value written to report/evidence: `0`

## Actual authenticated Control UI proof

The browser opened a new localhost Dashboard tab using the existing paired profile. The rendered page was OpenClaw Control with the existing Main Session and session history.

Gateway correlation from the same operation showed:

- `webchat connected`
- `client=openclaw-control-ui`
- localhost peer and Control UI origin
- a successful `sessions.list` response on the authenticated connection

The Gateway log also correlates the successful connection to the existing UI client. The successful read-only RPC proves this was not merely HTTP page reachability.

No `chat.send`, `chat.inject`, `sessions.patch`, `sessions.create`, provider inference, or semantic operation was issued.

## Owner/admin scope proof

The paired device metadata independently proves the installed Control UI operator role and includes both `operator.read` and `operator.admin`. The installed-source owner/admin derivation treats the admin operator scope as satisfying the owner/admin gate. The successful `sessions.list` RPC was executed through that authenticated Control UI connection.

## Fresh-session behavior

The exact installed UI behavior was determined without sending content:

- the existing Main Session was not reused as a substitute for a fresh owner session;
- Task-076 session `f829224b-064f-4bb4-a845-2955be2a2c7f` was not used;
- no new session was fabricated through a CLI command;
- the UI documentation confirms first non-command message behavior for a new Dashboard session.

Therefore the next task must create/use the fresh Dashboard/WebChat session at the first authorized `chat.send`; this task does not send that message.

## Preservation and zero-accounting

Task-090 accepted preservation remains authoritative and was not disturbed by this read-only proof:

- controller remained `managed`;
- one canonical source-exact plugin generation remained loaded;
- Supervisor remained healthy;
- Gateway and Ollama remained healthy;
- five natural PT1M no-flash cycles remained accepted;
- SQLite integrity remained `ok`;
- Tickets/outbox remained zero;
- semantic messages remained zero;
- provider calls/probes remained zero.

Task-091 added only browser navigation and read-only Control UI/Gateway observation. No live product mutation occurred.

## Publication fence

This report is the only intended change in the publication commit. The report must be independently checked remotely so that execution HEAD to report HEAD is exactly one report-only commit.

Successor gate: only after independent acceptance of `PASS_DASHBOARD_OWNER_SURFACE_READY_NO_SECRET_DISCLOSURE` may the final semantic acceptance task send exactly one fresh authenticated Dashboard/WebChat owner message with a newly generated execution-time nonce.
