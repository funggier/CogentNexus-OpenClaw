# CNX-20260826-081 — Supported Install-Over, Semantic Candidate Live Parity and No-Flash Acceptance

Status: `READY_FOR_HERMES`

Execution mode: `LIVE_SUPPORTED_INSTALL_OVER_SEMANTIC_CANDIDATE_PARITY`

Current authorization: `ONE_SUPPORTED_INSTALL_OVER_AND_LIVE_PARITY_AUTHORIZED`

Owner: ChatGPT

Executor: Hermes/Codex after operator continuation

## Goal

Install the accepted Task-078/079/080 semantic candidate onto the existing MANAGED CogentNexus/OpenClaw installation through exactly one supported normal install-over, then prove source/live package parity, ownership/runtime integrity, MANAGED health, natural no-flash operation, and readiness of a fresh authenticated Dashboard/WebChat owner surface.

This task does **not** perform final semantic acceptance and must not send any user prompt to OpenClaw.

Accepted semantic production candidate:

`70d02e76233ca1084da445d488f88b628455f4aa`

Accepted current live baseline before this task remains Task-075 source:

`79b51ed06363f6e8862c491ee0a313ddb412c806`

## Predecessor acceptance

Task 080 report HEAD:

`1798bfd4bb2ef69fb579b151f5d0423f0fc196f8`

Task 080 independent review:

Decision: `ACCEPT`

Disposition:

`ACCEPT_CRASH_SAFE_DELIVERY_FENCING_CLOSED`

Review path:

`docs/operations/coordination/reviews/CNX-20260826-080-close-crash-safe-lock-and-exact-delivery-run-fencing.md`

Preserve the accepted candidate behavior:

- owner/session-bound delivery-marker fail-closed behavior;
- repeated owner Ticket admission/routing idempotency;
- one Ticket/Host timeout-recovery authority;
- direct model-call lease ordering/fencing;
- direct `accepted -> routed -> response_ready -> delivery_confirmed -> completed` lifecycle and duplicate convergence;
- workflow scheduling/binding/settlement atomicity;
- crash-safe canonical completion-lock publication and bounded dead-owner recovery;
- exact workflow and Ticket outbox delivery-run settlement fencing;
- CLI/subagent negative owner security;
- provider disposition `PROVIDER_READY_WITH_FRESH_OWNER_SESSION` from exactly two already-consumed Task-078 direct Ollama probes.

No additional provider probe is authorized in Task 081.

---

# Absolute semantic fence

Task 081 is a live install/parity task, **not** a semantic test.

Do NOT:

- send any Dashboard/WebChat message;
- call `chat.send`, `openclaw agent`, `sessions_send`, channel send, or any equivalent user-message surface;
- create a Ticket by synthetic/direct DB/API calls;
- call Ollama directly;
- reuse Task-076 run/session/nonce;
- generate or consume the final semantic acceptance nonce;
- change configured model/provider/timeouts;
- perform a semantic LLM smoke after installation;
- manually edit product SQLite/Ticket/session state;
- uninstall, clean reset, manual residue cleanup or reinstall-from-zero;
- reboot;
- merge/tag/release.

The only product-changing operation authorized is **one supported normal install-over** from the exact accepted candidate source, plus installer-supported ownership-safe plugin/runtime lifecycle actions inherently performed by that install-over.

If the install-over fails after causing a partial state, do not run it again automatically. Capture exact state and report a blocker.

---

# Phase A — read-only preflight and live baseline re-proof

Before any mutation, record exact coordination execution HEAD and prove no unexpected actor has changed the accepted live system.

Record at minimum:

1. `openclaw --version` must remain `2026.7.1-2`;
2. CogentNexus controller state/mode/generation;
3. Gateway Scheduled Task/service state and dashboard HTTP health;
4. Ollama version/process health and exact installed model list;
5. Supervisor Scheduled Task identity, execute path, arguments, trigger and `LastTaskResult`;
6. launcher path/content/runtime interpreter binding;
7. current canonical CogentNexus plugin generation/path/version and enabled state;
8. current plugin configuration values relevant to Ticket-first/MANAGED semantics;
9. ownership manifest verification;
10. AGENTS managed block count and stripped-baseline hash;
11. authoritative CogentNexus SQLite integrity and table/count snapshot;
12. current live Ticket/event/outbox counts;
13. Task-076 timed-out OpenClaw session remains historical only and is not reused;
14. no current semantic run is active.

Expected baseline characteristics include:

- controller MANAGED;
- Gateway healthy/Ready on the existing loopback endpoint;
- Ollama healthy with the accepted four-model set unchanged;
- product-owned runtime/launcher/task paths with no Hermes/Codex/temp durable binding;
- one canonical enabled CogentNexus plugin generation;
- ownership verification passes;
- SQLite integrity is `ok`.

If meaningful baseline drift is found before installation, stop and report `BLOCKED_LIVE_BASELINE_DRIFT` rather than normalizing it silently.

---

# Phase B — exact candidate source and installer fence

Use a fresh isolated deployment worktree/check-out at exact commit:

`70d02e76233ca1084da445d488f88b628455f4aa`

Before installation:

1. verify `git rev-parse HEAD` equals the exact candidate commit;
2. verify clean worktree;
3. verify Task-078/079/080 production changes are present;
4. verify no later unreviewed production source is mixed in;
5. record candidate plugin package/version identity (`0.9.3`);
6. build/pack only as the normal installer requires; do not manually copy plugin files into the live generation.

Read-only ownership-mode evidence before invoking the installer must establish:

- recovery preflight resolves the existing product as ownership-present / non-fresh;
- install classification resolves to `upgrade`;
- no fresh-install transaction should be started for this install-over.

Prefer recording these from the supported installer/preflight surfaces; do not manually create or edit transaction markers.

If classification is not `upgrade`, stop before mutation and report `BLOCKED_INSTALL_MODE_MISMATCH`.

---

# Phase C — exactly one supported normal install-over

Run exactly once from the candidate deployment worktree:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace C:\Users\CDQ-P\.openclaw\workspace
```

Equivalent invocation through the currently supported PowerShell host is acceptable only if it executes the same script/arguments exactly.

Do not use:

- uninstall;
- reset;
- clean-reinstall;
- skip/link/developer bypass flags;
- manual plugin path edits;
- manual Scheduled Task replacement;
- manual AGENTS edits;
- manual ownership edits.

Record complete installer exit status and the important semantic milestones:

- recovery-preflight result;
- install classification;
- whether any fresh transaction was started (expected no);
- plugin rollover/retirement plan and result;
- ownership verification;
- controller lifecycle transitions;
- final install success/failure.

If the command returns nonzero, do not repeat it. Capture post-failure state read-only and report `BLOCKED_SUPPORTED_INSTALL_OVER`.

---

# Phase D — source/live parity of the semantic candidate

After successful install-over, prove the live plugin is exactly built from the accepted Task-080 candidate, not merely version-equal.

## D1 — canonical runtime selection

Record:

- exactly one active canonical `cogentnexus-openclaw@0.9.3` generation;
- exact generation path;
- OpenClaw plugin-info/list evidence showing that generation is the one loaded/enabled;
- any retired previous generation is outside active resolution and preserved only through the supported rollover mechanism.

No stale generation may win module resolution.

## D2 — package/tree parity

Create a clean expected package artifact from exact candidate source using the same package/build semantics required by the installer. Compare the installed canonical plugin package against that expected artifact.

The parity proof must cover all runtime-relevant files, not only `package.json`.

Preferred evidence:

- normalized relative-file manifest;
- SHA-256 per runtime-relevant file;
- aggregate tree digest or zero-difference file-by-file comparison;
- explicit check of `dist` entry files and package metadata;
- where source files are packed, verify them too.

At minimum explicitly prove that the installed runtime contains the Task-078/079/080 fixes for:

- owner-bound delivery marker handling;
- route idempotency;
- timeout authority handling;
- workflow schedule/bind/settle atomicity;
- crash-safe lock publication;
- exact workflow/Ticket run settlement fencing.

If any runtime-relevant source/live difference exists, stop and report `BLOCKED_SOURCE_LIVE_PARITY`.

## D3 — installed skill/ownership parity

Re-prove:

- ownership manifest verification passes;
- installed CogentNexus skill tree matches the accepted source where applicable;
- launcher/runtime paths remain those recorded by ownership;
- no unowned residue or duplicate active plugin path was introduced.

---

# Phase E — runtime, ownership and no-flash acceptance

The semantic source repair must not regress the accepted Task-072/075 runtime boundary.

Verify after install-over:

- product runtime foreground interpreter remains under `%LOCALAPPDATA%\CogentNexus-OpenClaw\runtime\python\...\python.exe`;
- background interpreter remains the corresponding product-owned `pythonw.exe`;
- launcher uses the owned foreground interpreter;
- Supervisor Scheduled Task uses the owned background interpreter;
- no Hermes venv, Codex path, temporary worktree, npm build path, `cmd.exe`, PowerShell wrapper or console Python is a durable Supervisor dependency.

Then observe **at least five natural PT1M Supervisor ticks** after installation.

Do not force-run the task as a substitute for the natural evidence window.

For each tick correlate:

- task run timestamp;
- `LastTaskResult`;
- Supervisor process ancestry/descendants as available;
- absence of causal `conhost.exe`/console Python/Hermes/uv-agent trampoline/cmd/PowerShell wrapper caused by the Supervisor tick.

Required disposition:

`NO_FLASH_MULTI_TICK_PROVEN`

Operator visual observation may corroborate but does not replace process/tick evidence.

Any causal console-flash regression is `BLOCKED_RUNTIME_NO_FLASH`.

---

# Phase F — post-install MANAGED health and durable state

After the natural-tick window prove:

1. controller is MANAGED;
2. desired Gateway/provider states are running as expected;
3. Gateway Scheduled Task/service is Ready/healthy;
4. dashboard HTTP endpoint returns success;
5. Ollama remains healthy and the accepted model list is unchanged;
6. `qwen3.5:9b` remains the configured conversational model; do not change it;
7. exactly one canonical CogentNexus plugin generation is enabled;
8. Ticket-first/pre-inference/auto-completion/enforced/auto-resume configuration remains the accepted values;
9. ownership verification passes;
10. AGENTS managed block appears exactly once and stripped baseline remains correct;
11. SQLite `PRAGMA integrity_check` is `ok`;
12. no unexpected Ticket/outbox/workflow rows were created by installation;
13. Task-076 historical failed session was not resumed/reused;
14. no semantic/model run occurred during Task 081.

Do not clear historical OpenClaw session state merely to make the final test cleaner.

---

# Phase G — fresh authenticated Dashboard/WebChat owner-surface readiness

Prepare the final semantic path without sending a prompt.

Inspect exact installed OpenClaw `2026.7.1-2` runtime/source and current Dashboard behavior to re-confirm:

- Dashboard/WebChat connection authenticates through the control-UI/admin-scope path identified by Task 077;
- the future chat path reaches the normal `before_agent_run`, `agent_end`, `reply_dispatch` and/or `message_sent` lifecycle relied upon by CogentNexus;
- owner trust is not inferred from a user-chosen session key;
- `openclaw agent --session-key agent:main:main` remains explicitly disallowed for final semantic acceptance.

If OpenClaw supports creating/selecting a fresh empty Dashboard conversation/session **without sending a user message or starting inference**, it is authorized to prepare that empty session. Record:

- exact session key/identity;
- authenticated owner/admin provenance;
- zero new Ticket rows;
- zero provider/model runs;
- zero user messages;
- zero assistant responses.

The fresh session must not be `agent:main:main` and must not reuse the Task-076 failed session.

If OpenClaw creates the Dashboard session only on first `chat.send`, do **not** fabricate or pre-create one through internal DB/state mutation. Instead report:

`DASHBOARD_OWNER_SURFACE_READY_FIRST_SEND_CREATES_SESSION`

and provide the exact supported UI/control path that the final semantic task must use.

Any uncertainty about whether the intended final path is authenticated owner traffic is `BLOCKED_DASHBOARD_OWNER_SURFACE_READINESS`.

---

# Phase H — publication fence

Task 081 is expected to have **no source/test commit**.

After live execution:

1. record coordination execution HEAD;
2. verify no product source or coordination file was modified by the executor before report publication;
3. publish exactly one report-only commit at:

`docs/operations/coordination/reports/CNX-20260826-081-install-over-semantic-candidate-live-parity.md`

The report must include:

- exact execution/report HEADs;
- Phase-A preflight snapshot;
- exact candidate source commit;
- one-install-over command/exit result;
- preflight/classification evidence (`ownership present`, `upgrade`, no fresh transaction);
- plugin generation rollover evidence;
- complete source/live package parity evidence;
- ownership/runtime/AGENTS/SQLite evidence;
- at least five natural PT1M ticks and no-flash classification;
- post-install MANAGED/Gateway/Ollama/plugin health;
- Dashboard/WebChat owner-surface readiness disposition;
- explicit accounting showing zero semantic messages/provider probes in Task 081;
- report-only publication fence.

## Result tokens

Use exactly one:

- `PASS_LIVE_PARITY_SEMANTIC_CANDIDATE_READY`
- `BLOCKED_LIVE_BASELINE_DRIFT`
- `BLOCKED_INSTALL_MODE_MISMATCH`
- `BLOCKED_SUPPORTED_INSTALL_OVER`
- `BLOCKED_SOURCE_LIVE_PARITY`
- `BLOCKED_RUNTIME_NO_FLASH`
- `BLOCKED_MANAGED_HEALTH`
- `BLOCKED_DASHBOARD_OWNER_SURFACE_READINESS`
- `BLOCKED_EVIDENCE_PUBLICATION_UNSAFE`

## Successor logic

Only if independent review accepts `PASS_LIVE_PARITY_SEMANTIC_CANDIDATE_READY` may the next task authorize one final real semantic owner message.

The final task must use the proven fresh authenticated Dashboard/WebChat owner path, create a new one-use nonce at execution time, and prove from durable/runtime evidence:

`owner message -> Ticket accepted before provider -> Ollama inference -> response_ready -> exact owner/run delivery -> delivery_confirmed -> completed -> visible response`

No final semantic message is authorized by Task 081 itself.
