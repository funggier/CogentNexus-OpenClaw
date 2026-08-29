# CNX-20260830-147 — Redirected-Stdin Product Uninstall and Fresh-Reinstall Retry

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_REDIRECTED_STDIN_UNINSTALL_AND_FRESH_REINSTALL_ACCEPTANCE`
Owner: ChatGPT
Executor: Hermes/Codex on the operator's real Windows machine

## Purpose

Repeat the Task-146 operator-facing lifecycle acceptance after its executor PTY failed before delivering confirmation input.

Task 146 did not begin destructive uninstall mutation. This task therefore authorizes one new, independent destructive attempt, but only after the executor proves its non-PTY redirected-stdin harness works with a harmless child process.

The product source is unchanged. Do not patch confirmation code for the Task-146 harness failure.

## Accepted implementation source

Exact accepted production SHA:

`fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

Task-146 post-failure state remained coherent MANAGED and must be re-verified read-only before mutation.

## Remote authority

Before execution:

1. fetch `agent/v0.9.3-full-stabilization` from GitHub;
2. verify `ACTIVE.md` and `STATUS.md` still authorize exact Task 147 and no matching report exists;
3. preserve uncertain local checkout and use a fresh detached source at exact SHA `fb5781c1...` for fresh install/provenance;
4. do not merge/rebase/tag/release/force-push.

## Phase A — read-only live gate

Re-prove materially the Task-146 post-failure boundary:

- installed `cnxclaw.cmd` exists and help exposes `uninstall`/`reset`;
- ownership verify PASS;
- controller MANAGED;
- exactly one canonical non-reparse `cogentnexus-openclaw` plugin, enabled/loaded;
- installed plugin fingerprint and ownership-helper hash match accepted candidate;
- Gateway/OpenClaw/Ollama healthy;
- recovery/delivery READY read-only, pending `0`;
- supervisor/Gateway tasks coherent;
- SQLite opened read-only, integrity `ok`, exact counts recorded;
- Dashboard semantic Sends `0`;
- no unexplained state drift from Task 146.

Preserve evidence outside all CNX live roots because uninstall intentionally deletes product-owned durable state.

If the live gate is ambiguous or unsafe, report `BLOCKED` and stop before mutation.

## Phase B — mandatory harmless stdin-harness qualification

Before invoking any CNX destructive command, validate the exact process-plumbing pattern that will be used for uninstall.

Requirements:

1. Use `System.Diagnostics.Process` or an equivalently deterministic child-process API with:
   - `UseShellExecute=false`;
   - `RedirectStandardInput=true`;
   - stdout/stderr capture;
   - no PTY/interactively attached terminal dependency;
   - exact child exit-code capture.
2. Run a **harmless temporary child** that calls Python `input()` once, emits the received value, and exits `0` only when it received exactly `y`.
3. Send exactly one line `y`, flush/close stdin, wait for exit, and prove:
   - child received `y`;
   - stdout/stderr were captured;
   - exit code is `0`;
   - no extra input was written.
4. The qualification child must not import or mutate CogentNexus/OpenClaw state.

If this harmless qualification fails, report `BLOCKED_HARNESS` and stop. Do not invoke uninstall.

## Phase C — product uninstall exactly once

Use the already-qualified non-PTY process harness to invoke the **installed launcher itself**:

`C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd uninstall`

A recommended Windows process shape is `cmd.exe /d /s /c call "<launcher>" uninstall` under redirected stdin/stdout/stderr. Equivalent deterministic plumbing is acceptable if the actual installed launcher is the command being exercised.

Requirements:

- product uninstall invocation count: exactly `1`;
- stdin confirmation writes: exactly one line `y`;
- close stdin after that line;
- preserve full stdout/stderr and real process exit code;
- prove the real product prompt was reached and confirmation was accepted;
- no second uninstall invocation.

If uninstall exits nonzero, stop immediately and report `FAIL_UNINSTALL`. No retry, no manual cleanup, no fresh install.

## Phase D — product-owned deferred cleanup and native state

After uninstall exit `0`, perform bounded read-only polling only. Do not delete anything manually.

PASS this phase only when evidence proves:

- `cnxclaw.cmd` absent;
- `.cogentnexus-openclaw` live state absent;
- workspace `skills/cogentnexus-openclaw` absent;
- no `cogentnexus-openclaw` registration in OpenClaw inventory;
- canonical plugin root absent and no conflicting product storage;
- CNX supervisor task absent;
- native OpenClaw remains installed, usable, healthy and on restored native route;
- Ollama installation/provider remains present and healthy;
- Dashboard semantic Sends remain `0`.

If product-owned cleanup does not converge within a bounded wait, report `FAIL_UNINSTALL_CLEANUP` and stop. No manual deletion.

## Phase E — one clean fresh install

Only after Phase D passes:

1. recompute/record accepted candidate package, fingerprint and key file hashes from fresh detached exact source `fb5781c1...`;
2. invoke normal `scripts/install.ps1` exactly once with the real workspace;
3. use no skip/staging flags, helper wrapper, alternate installer or retry.

If installer exits nonzero, report `FAIL_FRESH_INSTALL` and stop without manual repair.

## Phase F — fresh-install proof

After installer exit `0`, prove read-only:

- exactly one canonical non-reparse plugin identity exists;
- plugin enabled/loaded version `0.9.3`;
- fingerprint and ownership-helper hash exactly match accepted candidate;
- ownership manifest is newly created and `verify` passes;
- controller MANAGED;
- Gateway/OpenClaw/Ollama healthy;
- recovery READY read-only;
- delivery READY read-only, pending `0`;
- expected scheduled tasks registered/Ready;
- SQLite integrity `ok`;
- live durable database is genuinely fresh and contains no historical Task-145/146 Tickets/events/sessions; record exact counts;
- no stale install/rollover transaction remains;
- Dashboard semantic Sends remain `0`.

## Verdict tokens

Exactly one of:

- `PASS`
- `BLOCKED`
- `BLOCKED_HARNESS`
- `FAIL_UNINSTALL`
- `FAIL_UNINSTALL_CLEANUP`
- `FAIL_FRESH_INSTALL`

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260830-147-redirected-stdin-product-uninstall-and-fresh-reinstall-retry.md`

The report must include remote authority, harmless harness qualification proof, exact uninstall process plumbing/input count/exit, cleanup proof, exact fresh installer command/count/exit, fresh provenance/health/database proof, side-effect accounting, verdict and unproven items.

Then stop for independent ChatGPT review.

## Hard fence

No Dashboard semantic Send/resend; no reset; no crash/recovery injection; no manual Ticket/workflow/outbox/delivery/recovery/database mutation; no manual plugin lifecycle; no manual CNX live-file cleanup; no clean-reinstall helper; no second uninstall attempt; no fresh-install retry; no manual controller/ownership normalization; no unrelated service/process/task mutation; no reboot; no credentials/secrets; no merge/tag/release; no force push.
