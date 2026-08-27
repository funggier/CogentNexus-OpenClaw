# Active Coordination Task

Status: `READY_FOR_HERMES`
Execution mode: `SOURCE_TDD_DASHBOARD_DURABLE_PAYLOAD_STAGING_REPAIR`
Current authorization: `TASK092_DASHBOARD_DELIVERY_STAGING_DIAGNOSIS_AND_REPAIR_AUTHORIZED`
Task ID: `CNX-20260827-093`
Updated: 2026-08-27 ICT
Owner: ChatGPT
Executor: Hermes/Codex after operator continuation

## Authoritative coordination files

Only:

- `docs/operations/coordination/ACTIVE.md`
- `docs/operations/coordination/STATUS.md`

`docs/operations/STATUS.md` remains narrative and is not a coordination gate.

## Active task

[`tasks/CNX-20260827-093-repair-dashboard-durable-payload-staging-boundary.md`](tasks/CNX-20260827-093-repair-dashboard-durable-payload-staging-boundary.md)

## Task 092 accepted blocker

Task 092 report:

`0939c8b0659f0254c754dd7bbf44dc422648c4da`

Independent review:

Decision: `ACCEPT`

Disposition:

`ACCEPT_BLOCKER_DASHBOARD_DURABLE_PAYLOAD_STAGING`

Review path:

[`reviews/CNX-20260827-092-final-fresh-session-semantic-acceptance.md`](reviews/CNX-20260827-092-final-fresh-session-semantic-acceptance.md)

Publication fence is accepted: execution `e1c970d3...` -> report `0939c8b0...` is exactly one report-only commit.

## Accepted Task-092 semantic evidence

The first fresh-session path materially passed:

- authenticated Control UI/WebChat owner surface remained valid;
- New chat entered a clean staged state before send;
- fresh session `agent:main:dashboard:76932fbc-9df2-4415-9020-b6c1d7228505` was used;
- no stale/unknown/missing-parent failure;
- no fallback to Main Session;
- exactly one semantic message;
- exactly one Ticket `CNXT-90b73131-5460-4d0d-8669-2bc86a544754`;
- exactly one run `a2ea6b32-fd1a-4235-a6c5-820d475ea4cc`;
- one `accepted` and one `routed` event before provider start;
- exactly one correlated `ollama/qwen3.5:9b` Direct model call;
- exact nonce visibly rendered once;
- exactly one `response_ready`.

Task 092 did not pass final delivery because:

- `cnx_assistant_delivery` rows = `0`;
- `delivery_confirmed_at = null`;
- Ticket ended `failed` with permanent fail-closed unverifiable-delivery classification;
- no duplicate regeneration/output occurred.

The post-completion second New Session gate was correctly not executed because the Ticket never reached `completed`.

Task-092 nonce/session/Ticket/run are retired evidence and must not be reused or manually rewritten.

## Root-cause direction

Accepted source `d6daf8f93fcd5578f267b2017c6cc82e5de20095` intends the Dashboard Direct exact final payload to be staged in `cnx_assistant_delivery` from the verified-delivery `reply_dispatch` boundary before native transport.

Live Task 092 showed the V091 finalization/recovery behavior was active but the durable Direct-result row was absent.

Strong candidate H1:

`installV091DashboardVerifiedDelivery()` uses one `PATCH` marker on `TicketStore.prototype` to guard both prototype monkey-patching and runtime `reply_dispatch` hook registration. A legitimate later plugin registration in the same process can therefore retain patched TicketStore behavior while losing hook registration if the function returns on the existing prototype marker.

Task 093 must prove or falsify H1 against exact installed OpenClaw plugin reload/hook lifetime and executable repeated-registration behavior before editing source.

If H1 is false, Task 093 must inspect the actual WebChat `reply_dispatch` event/context/payload and every handler early-return predicate. Do not patch multiple hypotheses at once.

## Task 093 requirements

Task 093 is source/test-only plus read-only installed-source/log/DB inspection.

It must:

1. preserve Task-092 failed evidence unchanged;
2. inspect exact OpenClaw `2026.7.1-2` WebChat delivery and plugin reload lifecycle;
3. prove one exact missing-staging root cause;
4. create a production-implementation RED that reproduces visible/native final without durable staging under current source;
5. apply one minimal root-cause fix only after RED;
6. guarantee exact final text is durable before native visibility;
7. preserve exact Ticket/run/owner-session-generation binding;
8. preserve no-regeneration/fail-closed behavior;
9. make legitimate runtime re-registration retain exactly one active staging hook without duplication;
10. preserve fresh `agent:main:dashboard:<uuid>` session behavior and session successor logic;
11. run full plugin/Python/PowerShell/package/baseline regressions;
12. publish source/tests first and report separately.

## Hard live and semantic fence

No semantic message is authorized in Task 093.

No Dashboard/WebChat send, `chat.send`, `chat.inject`, `openclaw agent`, `sessions_send`, channel send, new nonce, direct Ollama call or synthetic Ticket mutation.

No install/install-over/uninstall/reset/cleanup, live plugin generation mutation, controller/startup/Supervisor/AGENTS/ownership/runtime/config edit, provider/model/timeout change, reboot, merge, tag or release.

Read-only exact installed source, Gateway logs and SQLite evidence may be inspected. Never expose Gateway bearer secrets.

## Successor gate

Only independent acceptance of:

`PASS_DASHBOARD_DURABLE_PAYLOAD_STAGING_REPAIRED`

may authorize a supported live install-over of the repaired exact source.

No new final semantic message is authorized until that new source is installed and live source/parity/MANAGED health are independently accepted.
