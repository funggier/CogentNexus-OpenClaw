# CNX-20260830-149 — Independent Review

Disposition: **ACCEPT**

Reviewed: 2026-08-30 ICT
Reviewer: ChatGPT

## Scope

Independent review of:

- Task: `docs/operations/coordination/tasks/CNX-20260830-149-proven-launcher-product-reset-fresh-state-retry.md`
- Report: `docs/operations/coordination/reports/CNX-20260830-149-proven-launcher-product-reset-fresh-state-retry.md`
- Accepted production SHA: `fb5781c1abd68280760bd5b3b4a65fabd8a60e58`
- Report publication commit: `9c14162ec8c94aae506086c166fda3cee7995ab6`

The publication commit adds only the matching Task-149 report. No production source, installer, configuration, or coordination authority changed during executor publication.

## Findings

Task 149 satisfies the reset acceptance contract.

1. **Fresh authority and safe starting state**
   - Execution began from the active Task-149 coordination state and used GitHub remote authority rather than a stale local checkout.
   - Pre-reset ownership, plugin, Gateway, Ollama, recovery, delivery, SQLite, and semantic-count evidence was coherent.
   - The accepted candidate was singular, canonical, enabled/loaded, and exact before mutation.

2. **The real product reset command executed once**
   - The launcher form already proven by Task 147 was used: `cmd.exe /d /c C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd reset`.
   - Exactly one reset invocation occurred.
   - Exactly one lowercase `y` confirmation was delivered.
   - The real product prompt was reached and accepted.
   - Exit code was `0` and the product reported `COGENTNEXUS-OPENCLAW RESET: PASS` with state `fresh-install MANAGED`.
   - No uninstall, install, reinstall, helper substitution, manual deletion, or retry occurred.

3. **Fresh-state recreation is proven independently of content equality**
   - Controller generation changed from `6` to `3` and its creation time/file ID changed.
   - SQLite creation time/file ID changed and its SHA-256 changed.
   - This proves the CNX state and durable database were recreated rather than merely edited in place.
   - SQLite remained structurally valid and all semantic tables remained at zero rows.

4. **Installed release provenance was preserved**
   - Launcher remained present with unchanged SHA-256.
   - Workspace skill remained installed.
   - Plugin remained singular, canonical/non-reparse, enabled/loaded at version `0.9.3`.
   - Plugin fingerprint and installed `namespace_ownership.py` hash remained equal to the accepted candidate.
   - Ownership verification passed after reset.

5. **Runtime returned to the intended fresh managed state**
   - Controller returned to `MANAGED`.
   - Desired Gateway/provider state is running.
   - Ollama is selected with selection source `reset` and is healthy/ready.
   - Gateway is healthy and loopback-only on `127.0.0.1:18789`.
   - Recovery and delivery are `READY`, pending outbox is `0`, and SQLite integrity is `ok`.
   - No stale reset/install/rollover transaction residue was found.
   - Dashboard semantic Sends remained `0`.

## Accepted conclusion

The operator-facing `cnxclaw.cmd reset` command now has real-Windows acceptance evidence. It recreates CogentNexus-OpenClaw runtime/durable state to a fresh-install condition while preserving the installed accepted release payload and restoring healthy MANAGED Ollama operation.

Task 149 therefore closes the reset lifecycle acceptance gate.

## Still unproven

Task 149 does not prove the complete normal runtime transition sequence on the accepted fresh installation:

- `stop` → intentional MAINTENANCE with verified Gateway/Ollama stop;
- `start` → MANAGED recovery with Gateway/Ollama healthy;
- `restart` → verified Gateway process boundary while remaining MANAGED;
- `disable` → PASSTHROUGH/native OpenClaw with CNX interception disabled;
- `enable` → MANAGED restoration with plugin/policy/route/runtime healthy;
- final real Dashboard one-Send durable-delivery acceptance.

## Next task

Open one bounded real-Windows runtime lifecycle acceptance task covering `stop → start → restart → disable → enable` in that order. Each command is invoked once; each phase must be independently verified before the next begins. Stop on the first failure. No Dashboard semantic Send is authorized in that task.
