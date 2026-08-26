# CNX-20260826-078 — Close Semantic P1s and Provider Readiness

Result: `PASS_SEMANTIC_P1S_REPAIRED_PROVIDER_READY`

Executor: Hermes, after the operator's explicit instruction to continue Task 078

## Scope and safety fence

- Fresh isolated clone/worktree from `origin/agent/v0.9.3-recovery-reality-tests`.
- Coordination task: `CNX-20260826-078-close-semantic-p1s-and-provider-readiness.md`.
- No OpenClaw semantic user message was sent.
- No live OpenClaw configuration, provider, model, plugin, Gateway, Scheduled Task,
  AGENTS policy, primary workspace, or product SQLite state was changed.
- The only live inference activity was the task-authorized bounded direct Ollama
  diagnostic: exactly two inert streaming requests to `qwen3.5:9b`, bypassing
  OpenClaw and CogentNexus and creating no Ticket.

## Heads and provenance

- Starting coordination HEAD: `9e66983d58a703ceb7ae9bfae29f82931f274737`.
- Implementation commit: `e25fbd5ab0c2773ee65d98782ecba942cbe36d58`.
- Branch/worktree: `hermes/task-078-repair` in the fresh Task-078 evidence directory.
- Target branch at preflight matched the remote branch HEAD.
- Final source/test worktree was clean after the implementation commit; the report
  is the only remaining publication change.

## Gate M — delivery marker owner/session binding

### RED/GREEN

Focused registered-hook tests were added before the implementation fixes. The
pre-fix focused run exited nonzero on the new security/idempotency expectations.
The fixed run passed all focused suites.

### Fixed contract

- `TicketStore.bindOutboxRun()` now accepts an expected owner session and updates
  only a pending outbox row whose `owner_session_key` matches.
- Workflow binding verifies the completion notice owner session in addition to task,
  revision, and pending state.
- `before_agent_run` requires a current run and session identity for parsed internal
  delivery markers, passes the session into binding, and returns a bounded
  fail-closed block (`cnxclaw_delivery_integrity`) for invalid, stale, forged, or
  wrong-owner markers instead of allowing ordinary inference.
- Settlement carries the run/session identity and checks the authoritative durable
  owner. Ticket settlement also fences the expected delivery run when present.
- A registered-hook negative test covers an unbindable marker; direct tests cover a
  pending Ticket outbox owned by owner A and a binding attempt from owner B.

No owner authority is derived from marker text.

## Gate R — repeated admission idempotency

- `TicketStore.route()` now makes one SQLite `BEGIN IMMEDIATE` decision over the
  accepted Ticket, existing routed event, and desired lane.
- First route writes one `routed` event, including the direct lane where the schema
  default is zero.
- Repeated same-lane route returns an idempotent no-op and writes no event.
- A conflicting reroute throws `conflicting route transition` rather than silently
  changing durable intent.
- The registered `before_agent_run` test invokes the same owner/session/run twice
  and verifies exactly one `accepted` and one `routed` event.

## Gate T — one timeout/recovery authority

- Registered `agent_end` handling now identifies Ticketed direct runs and suppresses
  generic `cogent-resume-*` scheduling for them.
- Ticket/Host recovery remains the authority for Ticketed direct runs; generic
  auto-resume remains available for non-Ticket runs.
- Internal delivery runs retain their specialized delivery path.
- The registered integration fixture drives a resumable direct timeout and asserts
  that no generic continuation is scheduled alongside the Ticket recovery path.
- The test also verifies one Ticket identity, durable recovery visibility, and no
  fabricated response/delivery completion on timeout.

## Gate L — lease/Host ordering disposition

This candidate was treated as a hypothesis, not patched with a broad redesign.

The executable ordering coverage now includes:

1. model-call start → Gateway/agent-end close → Host recovery eligibility;
2. model-call start → Host-owned `recovering` state → failing agent-end (agent-end
   cannot overwrite Host ownership);
3. model-call start → model-call ended → agent-end (late close is a no-op);
4. existing Host claim/finalize and Host claim/resume fence suites for successful
   response and Host/Gateway races;
5. the registered Ticket timeout promotion path from Gate T.

New lease matrix test: `v091-direct-recovery-model-call-fence.test.ts`.
Existing supporting suites: `v091-host-claim-finalize-fence.test.ts`,
`v091-host-claim-resume-fence.test.ts`, `v091-direct-model-call-lease.test.ts`,
and the Ticket timeout integration in `index.test.ts`.

Observed result: SQLite state fencing and existing Host fences produce one
explainable authority in all exercised interleavings. An `agent_end` fallback does
not close a Host-owned `recovering` lease, and a late close after
`model_call_ended` is rejected. **L is explicitly downgraded from an unresolved
P1 candidate to covered ordering behavior.**

## Gate W — workflow completion idempotency

- Added a bounded exclusive lock file around file-backed completion read/modify/write
  claims and settlement. The lock is local to the completion path and is removed in
  a `finally` block.
- Scheduling validates the on-disk task id, revision, owner, delivery status, and
  retry eligibility against the caller's expected notice before incrementing the
  attempt count.
- Delivered state is never rewritten to pending.
- A repeated/concurrent claim that cannot acquire the lock or sees a newer state
  converges without incrementing attempts again.
- Settlement validates pending state, task/revision, owner session, and delivery run
  identity when present.
- The stale-notice test settles a completion to delivered and then attempts to
  reschedule the old notice; it returns no claim and leaves delivered state intact.
- Existing retry-after behavior remains covered.

## Gate D — registered direct lifecycle

The integrated registered-hook test exercises isolated durable state with a fake
provider boundary and the owner metadata used by Dashboard/WebChat:

`before_agent_run` → one Ticket + one `accepted` + one direct `routed` event →
provider boundary release → successful `agent_end` with visible assistant output →
one `response_ready` → owner/run delivery callback → one `delivery_confirmed` →
`completed`.

A duplicate delivery callback produces no duplicate terminal events or side effects.
The negative coverage includes wrong-owner marker, forged/stale marker, untrusted
CLI/subagent admission behavior, internal continuation handling, and repeated same
owner/run admission.

## Provider Gate P

### P1 — installed OpenClaw 2026.7.1-2 source

Installed runtime: OpenClaw `2026.7.1-2` (`0790d9f`). Relevant source evidence:

- `dist/selection-JInn13lc.js:10802-10805`: default LLM idle timeout is
  `DEFAULT_LLM_IDLE_TIMEOUT_MS = 120000`; local first-event timeout is 300000ms;
  cron timeout is 60000ms.
- `dist/selection-JInn13lc.js:10927-10949`: idle timeout precedence is explicit
  `modelRequestTimeoutMs` first, bounded by run/agent timeout; then bounded run
  timeout; then bounded agent default; local runtime models may disable the
  implicit idle timeout; otherwise the default is 120000ms.
- `dist/selection-JInn13lc.js:10951-10961`: first-event timeout uses the explicit
  model request timeout when present, otherwise local 300000ms versus cloud
  120000ms, bounded by run/agent timeout.
- `dist/selection-JInn13lc.js:13071-13104`: the selected model's
  `params.model.requestTimeoutMs` is passed into both timeout resolvers and the
  resulting idle/first-event wrappers are installed around the stream.
- `dist/selection-JInn13lc.js:10964-10993`: every successful stream `next()` resets
  the idle timer; timeout aborts the provider request and surfaces an LLM idle
  timeout.
- `dist/agent-runner.runtime-DtdxZiBX.js:1755-1757,
  1900-1902,
  2910-2916`: transient HTTP provider failure is retried once after 2500ms.
- `dist/agent-run-terminal-outcome-Dv8Iorx2.js:51`: terminal observation retry grace
  is 15000ms.
- `dist/timeout-0Cw4kcol.js:8-18`: default run timeout is 2880 minutes; it is a
  run ceiling, not proof that the stream-idle watchdog is extended.

### P2 — exact current read-only configuration

Sensitive values were not recorded. Effective relevant fields were:

- selected model: `ollama/qwen3.5:9b`;
- `models.providers.ollama` is not explicitly present in the current config;
- `agents.defaults.models` contains `ollama/*` and `ollama/qwen3.5:9b`, but no
  explicit provider-model `requestTimeoutMs` was configured;
- `models.mode` is `merge`;
- OpenClaw general model list reports `ollama/qwen3.5:9b` as available/configured with
  `local=false`; however, the provider-specific dynamic catalog command
  `openclaw models list --provider ollama --all --json` reports the same model as
  `local=true` with context window 262144. This is a catalog-surface difference,
  not two different selected models.
- Installed source resolves runtime locality from the model's resolved `baseUrl`,
  not from the display flag: `selection-JInn13lc.js:10905-10919`. The Ollama plugin
  default is `http://127.0.0.1:11434` (`extensions/ollama/index.js:152` and
  `:875`), so a dynamically resolved local Ollama model follows the local
  first-event/idle behavior. A static catalog entry without a bound base URL can
  follow the cloud fallback branch. The CLI status surface does not expose the
  fully bound runtime model object, so this distinction is recorded rather than
  silently collapsed.
- The current config has no explicit provider-model `requestTimeoutMs`; no
  configured Ollama `timeoutSeconds` was found.
- No configured Ollama `num_ctx` equivalent was found in the redacted config; the
  provider-specific dynamic catalog reports context window 262144.
- `diagnostics.stuckSessionAbortMs=86400000`.
- `openclaw config validate` passed.
- Ollama modelfile inspection showed the configured model and generation parameters
  but no request timeout setting.

### P3 — Task-076 failed session pressure

Read-only `openclaw sessions --json --all-agents --limit all` identified:

- session key: `agent:main:main`;
- status: `timeout`;
- model/provider: `qwen3.5:9b` / `ollama`;
- context window: 262144;
- input/output/total token counters: zero;
- transcript: 16 JSONL records, 5,154 bytes;
- record composition: 1 session, 1 model change, 1 thinking-level change, 5 custom,
  and 8 message records;
- `systemSent=false`, `abortedLastRun=false`, and `totalTokensFresh=true`.

The failed session was not near a measured context-token limit. The evidence instead
supports a surface/session-path issue: the prior CLI `--session-key` invocation
preserved a session identity but did not establish owner authorization or Dashboard
provenance, and the stored session ended with zero provider tokens. Reuse of that
session is therefore not proven as context overflow; a fresh trusted Dashboard owner
session is the required next acceptance surface.

### P4 — exactly two authorized direct Ollama probes

Both requests used the inert prompt `Reply only: CNX-PROVIDER-PROBE`, streaming,
model `qwen3.5:9b`, and bypassed OpenClaw/CogentNexus.

| Probe | HTTP/done | TTFT | Total | Load | Prompt eval | Eval |
|---|---|---:|---:|---:|---:|---:|
| cold-ish 1 | 200 / true | 7.701s | 48.512s | 0.012s | 7.359s / 22 | 40.709s / 387 |
| immediate warm 2 | 200 / true | 0.198s | 126.017s | 0.002s | 0.159s / 22 | 125.770s / 1205 |

The model produced its first chunk well inside the effective 120s watchdog in both
probes. Probe 2 had high total generation time, but streaming progress continued and
completed with `done=true`; this is not a semantic acceptance result.

### P5 — disposition

`PROVIDER_READY_WITH_FRESH_OWNER_SESSION`

The model itself demonstrated first-chunk readiness at 7.7s cold-ish and 0.2s warm,
inside both plausible OpenClaw first-event watchdog branches (120s cloud fallback and
300s local-runtime branch). The Task-076 failure is more consistent with the
CLI/session/provenance surface and a timed-out zero-token session than with a proven
model inability to produce a first chunk. The next live acceptance must use a fresh
trusted Dashboard/WebChat owner session; it must not reuse `agent:main:main` or infer
owner authority from `--session-key` alone.

This disposition does not authorize a semantic message in Task 078.

## Full verification

| Gate | Result |
|---|---|
| Focused RED/GREEN semantic suites | GREEN; M/R/T/W/D focused coverage passed |
| Plugin full `npm test` Node 24/npm 11 | 49 files, 246 tests passed |
| Plugin `plugin:validate` Node 24/npm 11 | PASS; TypeScript/schema/bootstrap/package gates passed |
| Plugin full `npm test` Node 22.23.2/npm 12.0.2 | 49 files, 246 tests passed |
| Plugin `plugin:validate` Node 22.23.2/npm 12.0.2 | PASS; 45 config properties, 5 tools, 176 packed files |
| Python full pytest | 356 passed, 2 skipped, 4 subtests passed |
| Task 069 fresh transaction coverage | included targeted run; green |
| Task 070 non-fresh installer mode isolation | included targeted run; green |
| Task 071 upgrade/legacy mode isolation | included targeted run; green |
| Task 073 recovery preflight semantics | included targeted run; green |
| Task 069–073 targeted suites | 52 passed |
| `python scripts/check_baseline_consistency.py` | PASS (Bridge v0.9.3) |
| `git diff --check` | PASS |
| final implementation worktree | clean before report publication |

The targeted Python command ran:

`tests/test_fresh_transaction_failure_coverage.py`
`tests/test_installer_transaction_wiring.py`
`tests/test_fresh_install_transaction_recovery.py`
`tests/test_installer_mode_isolation.py`
`tests/test_upgrade_legacy_mode_isolation_proof.py`
`tests/test_recovery_preflight_semantics.py`

and returned `52 passed in 4.16s`.

## Live mutation accounting

- OpenClaw semantic messages: **0**.
- CogentNexus Ticket/product SQLite writes: **0**.
- OpenClaw config/provider/model changes: **0**.
- Plugin install/uninstall/reset/lifecycle changes: **0**.
- Gateway/Scheduled Task/AGENTS/primary workspace changes: **0**.
- Process termination/reboot/merge/tag/release: **0**.
- Authorized direct Ollama diagnostics: **2**, inert, no product-state writes.
- Isolated worktree `npm ci` and generated build/package artifacts were confined to
  the temporary evidence worktree and are not live product mutations.

## Publication fence and successor

Implementation/test changes are in commit `e25fbd5ab0c2773ee65d98782ecba942cbe36d58`.
This catalog-surface correction is a follow-up report-only change and does not alter
source, tests, provider configuration, or live state. Task 078 itself authorizes no
new real semantic message. If an independent review accepts
`PASS_SEMANTIC_P1S_REPAIRED_PROVIDER_READY`, the successor may perform the supported
install-over/source-live parity/health/no-flash gate and prepare a fresh trusted
Dashboard owner session. It must still preserve the final semantic nonce until a
separate live acceptance task explicitly authorizes consumption.
