# CNX-20260828-107 — v0.9.3 Real-Windows Lifecycle Acceptance Retry

Status: `FAIL`

## Task identity

- Task ID: `CNX-20260828-107`
- Branch: `agent/v0.9.3-full-stabilization`
- Pinned source: `b14a711f24b3fd1cd0aaa51ce636c8502ba42404`
- Executor: Hermes/Codex
- Evidence root: `C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw-Acceptance-Evidence\CNX-20260828-107\20260828T073925Z`

## Exact provenance and artifact

- Detached source HEAD: `b14a711f24b3fd1cd0aaa51ce636c8502ba42404`
- Recovery harness Git blob SHA: `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`
- Package-proof artifact ID: `9677072214`
- Package-proof artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-b14a711f24b3fd1cd0aaa51ce636c8502ba42404`
- Outer artifact SHA256: `b02dc802e2ea71ed18a12071ab570236864cea5c72416b8fae6ac9607f710b76`
- Inner ZIP SHA256: `3079ea8289d3ed465337b4621cb771eb1971d4ba7d86eb09d94d81875c049e1b`
- Package tar.gz SHA256: `5a010879d6effd3ee0ecbc449a6cffb30ecd26e91b90fb08765636c31d6a3b05`
- Package version: `0.9.3`
- Payload file count: `178`
- Payload-v2 fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`
- Package identity source commit: `b14a711f24b3fd1cd0aaa51ce636c8502ba42404`

The inner ZIP was hash-verified before extraction. The old Task-105 artifact ID `9669312785` was not reused.

## Tool versions observed

- OpenClaw: `2026.7.1-2` (`0790d9f`)
- Ollama: `0.32.15`
- Node: `v22.23.2`
- npm: `12.0.2`
- Python: `3.11.15`

## Phase 0 — provenance and residue re-entry: PASS

Read-only checks all returned root exit code `0` unless noted:

- source detached checkout and exact SHA verification: `0`;
- recovery harness blob verification: `0`;
- authenticated artifact download: `0`;
- outer and inner artifact hash verification: `0`;
- `cnxclaw status`: `0`;
- `cnxclaw provider status`: `0`;
- `cnxclaw check openclaw`: `0`;
- `cnxclaw check gateway`: `0`;
- `cnxclaw check recovery`: `0`;
- `cnxclaw check delivery`: `0`;
- `cnxclaw check resources`: `0`;
- `namespace_ownership.py verify --root ... --workspace ...`: `0`;
- read-only SQLite `pragma integrity_check`: `ok`;
- Supervisor task query: absent, matching Task-105 boundary.

The live machine matched the preserved Task-105 boundary before mutation: CNX `passthrough`, generation `25`, desired provider `unchanged`, selected provider Ollama, Gateway healthy, Ollama healthy/ready, SQLite healthy, ownership manifest present/coherent, Supervisor absent, and installer residue retained. The candidate installer was independently confirmed to contain the repaired local archive invocation:

```text
openclaw plugins install $packagePath --force
```

and not the superseded `npm-pack:` executable invocation.

Evidence: `a01-artifact-outer.sha256`, `a02-package-identity.json`, `a03-payload-identity.json`, `a04-published-sha256sums.txt`, `a05-inner-zip.sha256`, `a06-preflight-*`, `a07-ownership-verify.txt`, `a08-sqlite-integrity.txt`, `a09-supervisor.txt`, `a10-candidate-contract.txt`.

## Phase 1 — evidence/backup boundary: PASS

A new external evidence root was created and retained. Baseline hashes/listings were captured before mutation. Task-105 residue was not manually cleaned or normalized.

## Phase 2 — fixed-candidate install-over: FAIL

Exact command, executed once:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace C:\Users\CDQ-P\.openclaw\workspace
```

Native Node/npm path was pinned with `C:\Program Files\nodejs` first in `PATH`.

Root exit code: `1`.

Observed sequence:

1. Candidate npm preparation and plugin validation passed.
2. The fixed local `.tgz` install path was reached and succeeded:
   - package extracted;
   - plugin installed to `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw`;
   - plugin dependencies installed;
   - OpenClaw peer dependency linked;
   - plugin installed and then disabled because current CNX mode was passthrough.
3. The installer removed the previous plugin generation directory:
   `~\.openclaw\npm\projects\openclaw-plugin-cogentnexus-openclaw__openclaw-generation__g-8e5adec878a7c4e3\node_modules\openclaw-plugin-cogentnexus-openclaw`.
4. The subsequent ownership-safe rollover plan failed closed because the existing ownership manifest still referenced that removed generation:

```text
RuntimeError: owned installation is incomplete; refusing mutation:
['c:\\users\\cdq-p\\.openclaw\\npm\\projects\\openclaw-plugin-cogentnexus-openclaw__openclaw-generation__g-8e5adec878a7c4e3\\node_modules\\openclaw-plugin-cogentnexus-openclaw']
ownership-safe plugin generation rollover plan was rejected
install.ps1:388
ROOT_EXIT_CODE=1
```

Full installer evidence: `b01-install-over.txt`.

This was the single authorized install-over attempt. The installer was not rerun and no manual repair/deletion/configuration edit was attempted.

## Phases 3–7 — NOT EXECUTED

Because Phase 2 returned non-zero and left the lifecycle outside required managed convergence, reset, uninstall, fresh reinstall, normal stop/start/restart, and disruptive recovery were not executed. No recovery-harness verdict exists for this attempt.

## Post-failure state

Read-only post-failure checks returned root exit code `0`:

- CNX remains `passthrough`, generation `25`;
- selected provider remains Ollama and Ollama remains healthy/ready;
- OpenClaw remains exactly `2026.7.1-2`;
- Gateway remains healthy and listening on loopback;
- recovery check remains `READY` for passthrough;
- delivery has no pending terminal deliveries;
- SQLite integrity remains `ok`;
- ownership verifier remains exit `0` for the manifest itself;
- Supervisor task remains absent;
- installer backup/staging residue remains retained.

Evidence: `a13-postfailure-*`, `a14-after-baseline.json`, `a15-after-supervisor.xml`.

## Safety confirmations

- OpenClaw was not updated, reinstalled, uninstalled, or rebaselined.
- Ollama was not updated, reinstalled, uninstalled, stopped, or changed.
- The supported installer did alter CNX-owned plugin/config integration state as part of the one install-over attempt; no unsupported manual mutation was used.
- No Dashboard semantic nonce/Send, `chat.send`, semantic artifact reuse, or provider inference occurred.
- No credentials, tokens, passwords, or private session payloads were accessed or published.
- No process-tree kill, reboot, force push, or manual residue cleanup occurred.

## Final verdict

`FAIL`

Task 107 failed at the ownership-safe plugin generation rollover boundary after the repaired local archive installation path itself succeeded. The exact failure is preserved as evidence; later lifecycle and recovery acceptance remain unproven. Recommended next step is independent ChatGPT review and a separately authorized repair task for the stale ownership/plugin-generation transition. Do not replay Task 107 destructive phases from this attempt without a new explicit task and verified safe starting state.
