# CNX-20260831-183 — Qualified-Harness Reset Fresh-State Reacceptance

- **Task ID:** `CNX-20260831-183`
- **Executor:** Hermes/Codex
- **Coordinator / final reviewer:** ChatGPT
- **Execution class:** bounded destructive Windows lifecycle acceptance
- **Accepted repository candidate:** `f6392da3e4112ce441526d5ef19925c90a872b0b`
- **Required active facade SHA-256:** `aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

## Objective

Perform exactly one installed `cnxclaw.cmd reset` through the repaired interactive delegation path, observe the real confirmation prompt, send exactly one literal `y`, and prove the installation reaches a genuine fresh-install MANAGED state without semantic/model/recovery work or damage to external OpenClaw/Ollama assets.

This is a new acceptance action. It is not a retry under Task 175 or Task 178.

## Authority gate

Before any live mutation:

1. Fresh-read remote branch `agent/v0.9.3-full-stabilization` and `ACTIVE.md` / `STATUS.md`.
2. Confirm Task 183 is `READY_HERMES` and the Task-183 report is absent.
3. Confirm installed active facade reached by `cnxclaw.cmd` still has SHA-256 `aa747f8f...`.
4. Confirm no Task-178 observer, reset/uninstall child, prior Task-183 harness, or lifecycle residue is alive.
5. Record pre-reset controller/provider/Gateway/Ollama/ownership/delivery/recovery state and SQLite integrity/counts read-only.
6. Record external-preservation baseline sufficient to prove OpenClaw/Ollama remain installed and usable after reset.

If any gate is materially inconsistent, stop without invoking reset.

## Exact reset action budget

- installed `cnxclaw.cmd reset` root invocation: **exactly 1 maximum**;
- confirmation input: **exactly one literal `y` line maximum**;
- second reset invocation: **forbidden**;
- second confirmation send: **forbidden**;
- semantic/model/recovery action budget: `0`.

Invoke the installed operator path without manually supplying a different provider. v0.9.3 must inject Ollama according to the accepted implementation.

## Required harness architecture

Use the Task-177-qualified architecture adapted to the real repaired installed command:

`persistent supervisory harness -> cmd.exe /d /c -> installed cnxclaw.cmd reset -> repaired v0.9.3/legacy facade -> host_control_v092 -> lifecycle_v092`

Requirements:

- pipe stdin/stdout/stderr for the root `cmd.exe` process;
- drain stdout and stderr concurrently from process start through process exit;
- observe stdout at character/byte granularity so the no-newline prompt is visible;
- do not wait for stdout EOF before consuming stderr;
- maintain an in-memory confirmation-send counter that fails closed if a second send is attempted;
- persist an append-only or atomic incremental event ledger and flush/fsync important transitions before proceeding;
- persist stdout/stderr continuously enough to survive loss of the executor terminal/session;
- record PIDs/process identities and final exit code;
- use a supervisory mechanism whose child lifetime is not destroyed merely because an outer Hermes terminal call returns or times out.

Required ledger events at minimum:

- `harness_started`
- `cmd_process_started`
- `prompt_observed`
- `input_send_intent`
- `input_sent`
- `stdin_closed`
- reset completion marker observed, if present
- `cmd_process_exited`
- `stdout_reader_completed`
- `stderr_reader_completed`
- `orphan_scan_completed`
- `run_finalized`

The durable ledger must prove `prompt_observed` before `input_send_intent`, and `input_send_intent` before `input_sent`.

## Confirmation rule

Do not send input until the exact real lifecycle confirmation prompt is observed:

`Continue? [y/N]: `

Once observed:

1. persist/fsync `prompt_observed`;
2. persist/fsync `input_send_intent` with send count `1`;
3. send exactly `y\n` once;
4. flush stdin;
5. persist/fsync `input_sent`;
6. close stdin;
7. continue draining both output streams until child completion.

## Loss-of-control rule

If the outer executor terminal/session loses contact, times out, or cannot immediately see final completion:

- do **not** launch another reset;
- do **not** send another `y`;
- do **not** kill a still-running reset merely to obtain a tidy report;
- inspect the durable ledger, logs, exact process identities, and live product state;
- continue observing the existing process when safely possible;
- if completion remains unavailable, report `UNPROVEN` with the exact last durable event and process state.

A shell/tool timeout is not authorization for retry.

## PASS requirements

All are required:

### Invocation / prompt / input

- exactly one reset root invocation;
- exact prompt observed through the repaired interactive path;
- exactly one `y` send;
- no second-send attempt;
- no retry;
- child exits `0`;
- stdout contains `COGENTNEXUS-OPENCLAW RESET: PASS`;
- stdout contains `State     : fresh-install MANAGED`;
- stdout reports provider `ollama`.

### Fresh-state proof

After reset, independently prove:

- active installed facade still SHA-256 `aa747f8f...`;
- release remains `0.9.3`;
- OpenClaw remains `2026.7.1-2 (0790d9f)`;
- plugin remains installed, enabled, activated/loaded;
- ownership manifest is valid and legacy namespace remains empty;
- controller mode is MANAGED;
- selected provider is `ollama` and provider transition is committed/null;
- Gateway is healthy on the expected loopback boundary;
- Ollama is reachable/healthy/ready;
- active OpenClaw provider/model route is the expected fresh managed Ollama route;
- delivery/recovery checks are READY with no manufactured pending work;
- SQLite opens read-only and `PRAGMA integrity_check=ok`.

### Reset-owned durable data removed

The pre-reset CogentNexus durable history must be gone according to reset semantics. At minimum prove:

- `tickets = 0`;
- `ticket_events = 0`;
- `ticket_outbox = 0`;
- `cnx_assistant_delivery = 0`;
- `cnx_direct_model_call = 0`;
- `cnx_direct_recovery = 0`;
- `cnx_sessions = 0`;
- Task-171 Ticket `CNXT-b5bf2532-d35d-47db-8951-fcf9f4729abf` is absent;
- Task-171 run `8b69bede-030f-4c20-8bb8-0aa99e12422c` / delivery identity is absent wherever represented.

If bootstrap legitimately creates non-semantic metadata rows outside these reset-owned tables, record them separately; do not reinterpret semantic rows as bootstrap metadata.

### External preservation

Prove reset did not remove or corrupt:

- OpenClaw installation and native data outside CNX-owned state;
- Ollama installation and existing model inventory/data;
- unrelated OpenClaw configuration/namespaces;
- the installed CogentNexus program/release files themselves.

### Action fence

- installer/install-over/reinstall: `0`;
- uninstall: `0`;
- executor-issued start/stop/restart/enable/disable helpers: `0`;
- Dashboard Send/composer/`chat.inject`: `0`;
- model inference: `0`;
- recovery/regeneration: `0`;
- manual DB/config/transcript/route repair: `0`;
- product/source/test/workflow/dependency changes: `0`.

Installer/lifecycle-internal process boundaries performed by the single reset transaction are allowed and must not be replaced by executor helpers.

## Failure / uncertainty handling

If reset exits nonzero after `y`, preserve all evidence and classify the actual failed phase. Do not retry.

If process completion cannot be established, classify `UNPROVEN` rather than success/failure unless durable product state proves a specific terminal outcome. Do not infer success only from a fresh-looking controller state.

If the process is still running after the executor's normal observation window, preserve it and report its exact identity/last durable event; cleanup requires separate authorization unless the process has already reached a proven terminal state and only a dead observer wrapper remains.

## Publication

Report path:

`docs/operations/coordination/reports/CNX-20260831-183-hermes-qualified-harness-reset-fresh-state-reacceptance.md`

Report must include disposition, exact command/invocation count, prompt/input ledger, output markers, process/exit evidence, before/after durable matrix, external-preservation proof, issue register, hard-fence audit, exact authority HEAD, and successor recommendation.

After report publication, stop for ChatGPT review. **Uninstall remains unauthorized.**
