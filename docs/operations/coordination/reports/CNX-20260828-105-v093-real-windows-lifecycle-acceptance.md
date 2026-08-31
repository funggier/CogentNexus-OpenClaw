# CNX-20260828-105 — v0.9.3 Real-Windows Lifecycle Acceptance

Status: `FAIL`

## Task identity

- Task ID: `CNX-20260828-105`
- Branch: `agent/v0.9.3-full-stabilization`
- Pinned source SHA: `c4d37b0005afeffcd183848dfce5476cbe2b85cd`
- Repository path: `C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw-Acceptance-Evidence\CNX-20260828-105\20260828T061230Z\source-clone`
- Executor: Hermes/Codex
- Evidence root: `C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw-Acceptance-Evidence\CNX-20260828-105\20260828T061230Z`

## Exact artifact provenance

The authenticated GitHub Actions artifact ID `9669312785` was downloaded and retained as `artifact-outer/package-proof.zip`.

- outer artifact SHA256: `7e42f79da070bdcfb5f18d2f7f1fbbdb6e21f810915b5bfd84f4b84652d49d44`
- inner artifact: `cogentnexus-openclaw-v0.9.3.zip`
- inner ZIP SHA256, verified by streaming before extraction: `c6151fac1cc3b5cd37a2d82aa366bb547adff1f885b9d2b33209c83601606133`
- tar.gz SHA256 recorded from published `SHA256SUMS.txt`: `c022a5225703311607a2b69a00cdeb3462a0449fd4995d558f67fc99d3d5e625`
- package identity: version `0.9.3`, payload file count `178`, payload-v2 fingerprint `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`, source commit `c4d37b0005afeffcd183848dfce5476cbe2b85cd`
- source harness Git blob SHA: `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`
- source detached checkout HEAD: `c4d37b0005afeffcd183848dfce5476cbe2b85cd`

Evidence: `a01-artifact-outer.sha256`, `a03-package-identity.json`, `a04-payload-identity.json`, `a05-published-sha256sums.txt`, `a06-inner-zip.sha256`, `a09-source-head.txt`, `a22-ownership-verify.txt`.

## Tool versions

- OpenClaw: `2026.7.1-2` (`0790d9f`)
- Ollama: `0.32.15`
- Node: `v22.23.2`
- npm: `12.0.2`
- Python runtime used by launcher: `3.11.15`

## Phase results

### Phase 0 — provenance and read-only preflight: PASS

Read-only actions and root exit codes:

- authenticated `gh auth status`: `0`
- remote branch lookup: `0`
- detached checkout at pinned source: `0`
- source `HEAD` verification: `0`
- recovery harness blob verification: `0`
- artifact download: `0`
- pre-extraction inner ZIP hash verification: `0` (exact match)
- `cnxclaw status`: `0`
- `cnxclaw provider status`: `0`
- `cnxclaw check openclaw`: `0`
- `cnxclaw check gateway`: `0`
- `cnxclaw check recovery`: `0`
- `cnxclaw check delivery`: `0`
- `cnxclaw check resources`: `0`
- `namespace_ownership.py verify --root ... --workspace ...`: `0`
- SQLite read-only `pragma integrity_check`: `ok`

Before mutation the deployment was coherent: installed version `0.9.3`, controller `managed`, selected provider `ollama`, Gateway healthy/listening on loopback, Ollama healthy/ready, recovery `READY`, pending outbox `0`, and the canonical Windows Supervisor task was `Ready`/enabled/hidden with the owned `pythonw.exe` binding. The three manifest identities are platform identities; Windows task lookup is case-insensitive and the two Windows spellings resolved to the same task. The macOS launchd spelling was absent as expected.

Before-state hashes and task XML: `a23-before-baseline.json`, `a24-before-supervisor.xml`, `a25`-series preflight files.

### Phase 1 — evidence/backup boundary: PASS

A fresh evidence root outside the runtime root was created before mutation. The exact artifact was staged there. Existing state was recorded by metadata, hashes, read-only SQLite integrity, and redacted task XML. The installer-created backup boundary was retained under the owned state root; no private session/config contents were copied into the repository or report.

### Phase 2 — install-over proof: FAIL (stop condition)

Exact command, run once:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace C:\Users\CDQ-P\.openclaw\workspace
```

The command was run from the extracted, hash-verified CI ZIP package with native `C:\Program Files\nodejs` first in `PATH`.

Root exit code: `1`.

Observed sequence:

1. Candidate npm preparation and plugin validation passed.
2. Supported native handoff changed the existing CNX controller from `managed` to `passthrough`, disabled the CNX startup adapter, and restarted the native OpenClaw Gateway successfully.
3. Existing skill backup was created at `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\install-backups\cogentnexus-openclaw-20260828-131845` and the candidate skill was installed.
4. Candidate validation passed.
5. Installer then reported `npm pack metadata read produced incomplete package metadata`, followed by `plugin installation from npm-pack artifact failed` at `scripts\install.ps1:354`.

The installer was not rerun. No manual repair, direct config/SQLite edit, deletion, or alternative lifecycle command was attempted.

Full installer output: `b01-install-over.txt`.

### Phases 3–7 — NOT EXECUTED

Per the task's stop-on-failure and no-replay rules, reset, uninstall, fresh reinstall, normal stop/start/restart, and disruptive recovery harness were not executed after Phase 2 failed. There is no recovery-harness verdict for this attempt.

## After-failure state and preservation observations

Read-only post-failure checks all returned root exit code `0`:

- controller: `passthrough`; desired provider: `unchanged`; generation advanced from `24` to `25` as a natural installer effect;
- Gateway: healthy, loopback listener present, OpenClaw still `2026.7.1-2`;
- Ollama: installed, reachable, healthy/ready, selected provider remains `ollama`, four-model inventory observed;
- recovery check: `READY` for the now-passthrough state;
- delivery check: no pending terminal deliveries;
- SQLite: read-only integrity `ok`;
- ownership verifier: exit `0` and manifest remains present;
- Supervisor task: absent after the supported native handoff (`a28-after-supervisor.xml` records no XML task result);
- install staging and installer backup directories remain as residue and were not manually cleaned.

Post-failure evidence: `a27-after-failure-baseline.json`, `a28-after-supervisor.xml`, `postinstall-status.txt`, `postinstall-provider-status.txt`, `postinstall-check-*.txt`, `a25-postinstall-ownership.txt`.

OpenClaw and Ollama were preserved: neither was updated, reinstalled, uninstalled, rebaselined, or otherwise directly mutated. The supported installer did restart the OpenClaw Gateway during the native handoff; it remained healthy. Ollama was not stopped or changed.

No Dashboard semantic nonce/Send, sent sentinel, `chat.send`, semantic artifact reuse, or provider inference was performed.

## Safety and classification

Final verdict: `FAIL`.

The failure is at the supported install-over plugin npm-pack boundary. Because the lifecycle command returned non-zero and the post-failure state is no longer the required managed convergence, all later mandatory phases are unproven. The observed passthrough/startup-disabled residue is preserved for independent review; it was not hidden by a retry or manual cleanup.

Recommended next step: independent ChatGPT review and a separately authorized repair/recovery task for the npm-pack installation boundary. Do not replay Task 105 destructive phases from this attempt without a new explicit task and verified safe starting state.
