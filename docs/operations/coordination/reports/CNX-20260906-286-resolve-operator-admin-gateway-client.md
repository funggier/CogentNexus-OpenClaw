# CNX-20260906-286 — Resolve Operator-Admin Gateway Client Boundary

## Disposition

`NEEDS_CHATGPT__CREDENTIAL_OR_AUTHORITY_BOUNDARY__NO_MUTATION`

Task286 was executed by Luna as a bounded read-only diagnostic. The installed OpenClaw Gateway is healthy and reachable, but the default CLI client does not hold an operator scope. The machine has paired operator devices advertising `operator.admin`; selecting or supplying one of those credentials requires an explicit credential/authority decision and was not attempted.

## Authority and provenance

- branch: `agent/v0.9.3-full-stabilization`
- preflight remote HEAD: `adea860db54d03c45efbdbb3eadf54877558d6ec`
- active task: `CNX-20260906-286`
- executor: `Luna`
- installed OpenClaw: `2026.7.1-2` (`0790d9f`)
- diagnostic date: `2026-09-07` local session

## Read-only findings

### Gateway and client boundary

`openclaw gateway status` reported:

- service: registered Scheduled Task and runtime `Ready`;
- Gateway version equals CLI version `2026.7.1-2`;
- loopback endpoint `127.0.0.1:18789` is listening;
- connectivity probe: `ok`;
- capability: `connected-no-operator-scope`.

`openclaw gateway probe` reported:

- Gateway reachable: `yes`;
- capability: `connected-no-operator-scope`;
- local connection: `ok`;
- read probe: limited because `operator.read` is missing;
- remediation hint: pair device identity or use credentials with `operator.read`.

The supported `openclaw gateway call` client exposes explicit `--token`, `--password`, and `--url` options. No call was made to a mutating or privileged method.

### Supported authority inventory

Read-only `openclaw devices list` showed four paired device entries. Their displayed roles/scopes include operator devices with `operator.admin`, `operator.read`, `operator.write`, `operator.approvals`, and `operator.pairing`; one displayed local entry is `Windows Node (CDQ-P)` with `operator.admin` and `operator.pairing`.

Only redacted inventory metadata was retained. No token, password, or credential value was printed, copied, rotated, revoked, or changed.

### Configuration boundary

The installed configuration contains gateway authentication metadata and a gateway token field, but values were suppressed. Environment presence checks showed `OPENCLAW_GATEWAY_TOKEN` absent and `OPENCLAW_GATEWAY_PASSWORD` present; the password value was not read or displayed. This does not prove that the current CLI invocation has a usable operator-admin credential.

The Control UI is a supported client path (`openclaw dashboard`), and the Gateway CLI supports explicit credential options. Choosing which paired identity or credential to use for an operator-admin connection requires human authorization and must not be guessed.

## Mutation ledger

- `sessions.delete`: `0`
- reset/cancel substitute: `0`
- semantic sends: `0`
- Ticket/session/SQLite/transcript mutation: `0`
- protected or sacrificial session mutation: `0`
- credential readout/guess/rotation/revocation: `0`
- installer/uninstall/release/force push: `0`

## Decision and required ChatGPT action

Luna cannot safely resolve the boundary without either selecting an existing paired operator-admin identity or using a credential supplied/approved by an authorized human. This is a credential/authority decision under Task286's stop rule.

Set coordination to `NEEDS_CHATGPT`. ChatGPT must decide whether to authorize a supported operator-admin client path and, if so, define the non-secret acquisition/configuration boundary. No Delete retry is authorized by this report. After ChatGPT provides authority, a fresh successor task must re-read the exact remote state and keep the one-shot Delete fence intact.
