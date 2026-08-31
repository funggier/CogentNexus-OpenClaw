# CNX-20260829-129 — Managed-State Root Authority Read-Only Diagnosis

## Verdict

**PASS — diagnosis complete, read-only only.** The Task-128 BLOCKED result was caused by an executor/probe root mismatch, not by an authoritative live managed-state drift. No runtime, provider, model, configuration, SQLite, scheduled-task, installer, or user-data mutation was performed.

## Authority and scope

- Task: `CNX-20260829-129-managed-state-state-root-authority-readonly-diagnosis`
- Repository branch: `agent/v0.9.3-full-stabilization`
- Accepted Task-127 candidate: `1b922bf400fdbccb1f9c7019b89b69fd67f44070`
- Exact repaired harness blob retained: `622f70b339fea0f2ef7c564253aa3c6bf90ffc97`
- Evidence root: `C:\Users\CDQ-P\AppData\Local\Temp\cnx129-authority-20260829T083000Z`
- Installed launcher inspected: `C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd`
- Installed launcher explicitly resolves the v0.9.3 controller with root:
  `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw`

Fresh coordination state was synchronized before diagnosis. The active task authorized read-only authority diagnosis only; no recovery-suite replay was authorized.

## Root-cause finding

The Task-128 preflight used the workspace parent as the controller root:

```text
--root C:\Users\CDQ-P\.openclaw\workspace
```

The installed launcher uses the state root:

```text
--root C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw
```

The first path has no authoritative managed controller state and therefore produced the misleading snapshot:

- `mode=passthrough`
- `selectedProvider=null`
- `desiredProvider=unchanged`
- `generation=1`
- `sqliteExists=false`

This was a probe false negative. It was not evidence that the managed runtime had drifted.

## Direct installed-launcher evidence

All probes below invoked the installed launcher path directly; no replacement launcher, alternate harness, lifecycle command, or state mutation was used.

- `status`: exit `0`; authoritative state is `managed`, generation `21`, desired gateway `running`, desired provider `ollama`, selected provider `ollama`.
- `provider status --json`: exit `0`; provider selection and provider status are coherent.
- `check recovery --json`: exit `0`; verdict `READY`, `readOnly=true`, `stateChanged=false`, provider incident closed, circuit closed.
- OpenClaw gateway and Ollama listener/task findings remained healthy in the retained preflight evidence.

Raw outputs and probe exits are retained under the evidence root, including `b04-status.txt`, `b05-provider-status.json`, `b06-recovery.json`, and `b07-probe-exits.jsonl`.

## SQLite authority

The authoritative database is:

```text
C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\runtime\cogentnexus-openclaw.sqlite3
```

The file exists. A read-only SQLite connection was opened using URI mode `mode=ro`; `PRAGMA integrity_check` returned `ok`. No write transaction, migration, vacuum, checkpoint, or other database mutation was attempted.

The earlier `sqliteExists=false` result came from deriving the database path beneath the wrong workspace-parent root.

## Installed/runtime identity

- Installed product/plugin fingerprint remained the previously attested exact value:
  `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- Launcher and installed controller path were inspected as read-only files.
- No source or harness edit was made.
- No reinstall or install-over is justified by this diagnosis: the accepted candidate changes the recovery harness contract/CI surfaces, while the installed runtime/provider identity is already the attested v0.9.3 deployment.

## Timeline interpretation

The prior Task-125 provider-crash evidence remains a historical old-harness live-behavior failure. Task 126/127 repaired and proved the harness contract but did not prove product-wide live provider recovery. Task 128 was blocked before suite launch because its preflight used the wrong controller root. This report does not convert any historical failure into a PASS and does not claim a live recovery acceptance.

## Safety ledger

- Task-128 recovery suite launch: `0 / 1`
- Task-128 confirmation `y`: `0`
- Gateway/provider crash injection: `0`
- Operator-stop scenario: `0`
- Install/install-over/reset/uninstall/reinstall: `0` in this task
- Standalone lifecycle operation: `0` in this task
- Cleanup/normalization: `0`
- Dashboard semantic Send: **not performed**

## Disposition

This diagnosis is complete. The next real-Windows recovery acceptance, if desired, requires a separately reviewed and explicitly authorized task that uses the installed launcher/state-root authority (or an exact equivalent with independently verified root semantics), repeats all required read-only gates, and preserves the one-shot recovery-suite fence. No Task-128 recovery replay is performed automatically from this report.

## Evidence inventory

- `authority-probes.ps1`
- `authority-closeout.ps1`
- `b02-metadata.json`
- `b03-launcher-parsed.json`
- `b04-status.txt`
- `b05-provider-status.json`
- `b06-recovery.json`
- `b07-probe-exits.jsonl`
- `b09-competing-roots.txt`
- `b13-sqlite-readonly.txt`

All evidence was collected read-only and secrets were not accessed or recorded.
