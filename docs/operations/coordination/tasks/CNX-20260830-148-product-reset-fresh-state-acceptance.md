# CNX-20260830-148 — Product Reset Fresh-State Acceptance

Status: `READY_FOR_HERMES`
Execution mode: `LIVE_WINDOWS_PRODUCT_RESET_FRESH_STATE_ACCEPTANCE`
Owner: ChatGPT
Executor: Hermes/Codex on the operator's real Windows machine

## Purpose

Prove the accepted installed candidate's real operator-facing `cnxclaw.cmd reset` lifecycle on Windows.

The reset must demonstrate that CogentNexus-OpenClaw state is destroyed and recreated as a fresh-install MANAGED state while the installed program/skill/plugin provenance remains installed and exact. This task must not substitute uninstall/reinstall for reset and must not seed semantic Dashboard/Ticket data merely to make the reset visible.

## Accepted starting boundary

Task 147 is independently ACCEPTed and last proved a genuinely fresh installation of exact production SHA:

`fb5781c1abd68280760bd5b3b4a65fabd8a60e58`

Last proven live state:

- exactly one canonical `cogentnexus-openclaw` plugin, version `0.9.3`, enabled/loaded;
- plugin fingerprint `12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0`;
- installed `namespace_ownership.py` SHA-256 `10dda985e6d4553a73a8cdd3ef7f660937482c3ef0c2d2da8d15bcbfe8d39b66`;
- ownership verify PASS;
- controller `MANAGED`;
- Gateway/OpenClaw/Ollama healthy;
- recovery/delivery READY, pending `0`;
- SQLite integrity `ok`;
- semantic table counts all `0`;
- Dashboard semantic Sends `0`.

This boundary is historical evidence only. Re-verify read-only before mutation.

## Remote authority

Before live mutation:

1. fetch `agent/v0.9.3-full-stabilization`;
2. verify `ACTIVE.md` and `STATUS.md` still authorize this exact Task 148 and no matching report exists;
3. do not use a stale local checkout as authority;
4. do not merge/rebase/tag/release/force-push.

## Phase A — read-only pre-reset proof

Capture without changing live state:

- launcher path and help proving `reset` is exposed;
- ownership manifest and exact verify result;
- controller status/state, including generation and `updatedAt`;
- plugin inventory, raw canonical root, enabled/loaded status and non-reparse attestation;
- installed plugin fingerprint and installed ownership-helper hash;
- workspace skill/launcher file hashes needed to prove program files remain installed through reset;
- Gateway/OpenClaw version/health/listener;
- selected Ollama/provider health;
- recovery and delivery checks read-only, pending count;
- supervisor/Gateway scheduled task state;
- SQLite `PRAGMA integrity_check`, semantic counts and DB SHA-256;
- Windows state-file identity evidence for at least the durable SQLite DB and controller state file where present: creation time plus a read-only file identity/file ID when available (for example `fsutil file queryfileid` or equivalent). If a file-ID mechanism is unavailable, record creation time, last-write time, length and hash and explicitly state the limitation;
- Dashboard semantic Send count `0`.

Do not create Ticket/session/workflow/outbox/delivery rows for this task.

If ownership/storage/runtime is incoherent or unsafe, publish `BLOCKED` before mutation.

## Phase B — qualify reset confirmation harness

Use the same deterministic non-PTY redirected-stdin mechanism accepted in Task 147, but qualify it again first with a harmless temporary Python child that performs one `input()` call.

Qualification must prove:

- exactly one line `y` is written;
- stdin is then closed;
- child reports receiving `y`;
- stdout/stderr and true exit code are captured;
- child exits `0`;
- no CNX/OpenClaw state is imported or mutated.

If qualification fails, publish `BLOCKED_HARNESS` and do not invoke reset.

## Phase C — operator-facing reset, exactly once

Invoke the installed launcher itself:

`<workspace>\cnxclaw.cmd reset`

Use the qualified redirected-stdin harness.

Requirements:

- reset invocation count: **1**;
- explicit confirmation input: exactly one lowercase `y` line;
- no `--provider` override unless the installed v0.9.3 facade itself requires it unexpectedly; the public default should select/force Ollama;
- capture real stdout/stderr and exit code;
- no second reset attempt;
- no uninstall/install/clean-reinstall helper;
- no manual deletion or state normalization.

If reset exits nonzero, stop immediately and publish `FAIL_RESET` with read-only post-failure evidence. Do not retry or repair.

## Phase D — prove true fresh-state recreation without reinstall

If reset exits `0`, prove read-only that reset recreated state rather than reinstalling the product.

### Program/ownership preservation

- `cnxclaw.cmd` still exists;
- workspace skill still exists;
- exactly one canonical plugin still exists;
- plugin remains version `0.9.3`, enabled/loaded;
- plugin fingerprint is unchanged and equals accepted candidate;
- installed ownership-helper hash is unchanged and equals accepted candidate;
- ownership verify passes;
- no plugin uninstall/install/rollover transaction occurred;
- no fresh `scripts/install.ps1` invocation occurred.

### State recreation

- controller is fresh-install `MANAGED` with desired Gateway/provider running;
- selected provider is Ollama;
- Gateway and Ollama are healthy/ready;
- recovery is READY and read-only;
- delivery is READY, read-only, pending `0`;
- SQLite integrity is `ok`;
- semantic counts remain/reset to `0`;
- state-root/controller timestamps reflect the new reset generation;
- durable DB/controller file identity evidence demonstrates recreation. Prefer a changed Windows file ID or new creation timestamp relative to Phase A. Do not rely only on content hash because an empty freshly bootstrapped database may reproduce identical logical content;
- no stale reset/install/rollover transaction remains;
- Dashboard semantic Sends remain `0`.

### Native product preservation

- OpenClaw remains installed and healthy;
- Ollama installation/model inventory remains present;
- no unrelated process/service/task was removed;
- expected CNX supervisor/Gateway scheduled tasks are coherent after reset.

## PASS criteria

`PASS` requires all of:

1. fresh GitHub authority and coherent pre-reset state;
2. harmless redirected-stdin qualification succeeds;
3. exactly one real `cnxclaw.cmd reset` invocation;
4. exactly one lowercase `y` confirmation;
5. reset exit code `0`;
6. state root/durable DB is proven recreated using file identity/timestamp evidence;
7. installed program/skill/plugin accepted provenance is preserved without reinstall;
8. controller returns to fresh MANAGED Ollama state;
9. Gateway/Ollama/recovery/delivery/SQLite healthy, pending `0`;
10. semantic counts `0`, Dashboard semantic Sends `0`;
11. no retry/manual normalization/uninstall/install helper path.

## Required report

Publish exactly:

`docs/operations/coordination/reports/CNX-20260830-148-product-reset-fresh-state-acceptance.md`

Report must include:

- exact authority HEAD;
- complete pre-reset evidence;
- harmless harness qualification;
- exact reset command, input count and exit code;
- pre/post state-file identity/timestamp comparison;
- program/plugin/ownership provenance preservation proof;
- complete post-reset runtime/provider/recovery/delivery/database evidence;
- side-effect accounting;
- verdict exactly one of `PASS`, `FAIL_RESET`, `BLOCKED_HARNESS`, `BLOCKED`;
- unproven items.

Then stop for independent ChatGPT review.

## Hard fence

No Dashboard semantic Send/resend; no Ticket/workflow/outbox/delivery/recovery semantic mutation; no uninstall; no install/reinstall; no clean-reinstall helper; no manual live-state deletion; no manual plugin/controller/ownership normalization; no reset retry; no crash/recovery injection; no unrelated process/service/task mutation; no reboot; no credentials/secrets; no merge/tag/GitHub Release; no force push.
