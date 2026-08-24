# CNX-20260824-050 — Fresh-Install Current CogentNexus-OpenClaw v0.9.3

Status: **BLOCKED**

Result: `BLOCKED_POSTINSTALL_RUNTIME`

Fetched start HEAD: `0b71bf28aaa15650460939276c94cf472d5aa4cb`

Repository: `C:\Users\CDQ-P\AppData\Local\Temp\cnx050-clone-20260824T120441Z`

Branch: `agent/v0.9.3-recovery-reality-tests`

## Authority, source, and duplicate fence

The exact coordination `ACTIVE.md`, coordination `STATUS.md`, and Task 050 identified `CNX-20260824-050` as `READY_FOR_CODEX`; the operator's authorization `1` was recorded. No matching report existed. A new isolated full clone was used; the primary workspace Git checkout was not mutated.

Required implementation `4c825f8ec1ed6b43a419ad52e0bb85cee28007c1` was an ancestor (exit `0`), and non-coordination drift after it was empty. `VERSION`, plugin/package manifests, canonical skill metadata, and installer identified CogentNexus-OpenClaw v0.9.3 and plugin/package `cogentnexus-openclaw` / `openclaw-plugin-cogentnexus-openclaw` v0.9.3. Windows PowerShell parser reported zero installer errors. `python scripts\check_namespace_isolation.py` exited `0` before and after installation. Concurrent lifecycle/report-publisher/Procmon count was zero.

## Accepted fresh baseline

Before mutation:

- classifier exited `0`: `mode=fresh`, `new=[]`, `legacy=[]`;
- native registry was `fresh`, 71 persisted plugins, zero refresh reasons;
- native plugin list returned valid JSON for 71 plugins, with zero current or legacy CogentNexus id;
- launcher/skill/state/application-data/plugin/task/config residue for both current and legacy products was absent;
- `AGENTS.md` was 7,196 bytes, SHA-256 `C9A664B73200AE5D6B0DA0908DE3256CDB4DDA8BA6FE99F5E6C5115C3983604C`, with zero current/legacy markers;
- Task 049 backup existed and manifest hash was `7525DAB74EE1801A26B4B1CF824CB22155E971BCB63697149580ED1B9F42BA3A`;
- OpenClaw/Gateway `2026.7.1-2` was healthy at PID 32936;
- Ollama was healthy with active `qwen3.5:9b` and the same four models;
- unrelated plugin count was 71 and managed npm project count was 7;
- primary repository was `master` with its pre-existing untracked status.

No registry refresh, doctor fix, upgrade, repair, or workaround ran.

## Single installer invocation

Exact command, invoked once from the isolated clone:

`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "C:\Users\CDQ-P\.openclaw\workspace"`

- invocation count: `1`
- exact child PID: `45576`
- start UTC: `2026-08-24T12:05:45.2952218Z`
- final stdout mtime: `2026-08-24T12:10:47.6998122Z` (approximately 302.4 seconds)
- stdout: 87,462 bytes; stderr: 719 bytes
- stdout terminal stage: `CogentNexus-OpenClaw v0.9.3 installation completed successfully (Ollama-only).`
- stderr contained only npm `allow-scripts` warnings; no installer error was printed.

The PowerShell launch wrapper returned successfully after the child ended, but it did not retain the terminated child's `ExitCode` property. Therefore the exact installer child exit code is **unobserved**, not asserted as zero. Durable stage output and all poststate checks prove the installer body completed, but Task 050 explicitly requires an observed installer exit code `0` for PASS. The installer was not retried.

Installer output recorded successful skill/state/policy staging, npm plugin packaging/installation, ownership creation, MANAGED authority commit, canonical supervisor registration, Gateway reloads with exit `0`, already-healthy Ollama lifecycle, and final integration verification.

## Ownership and canonical namespace proof

Classifier exited `0` with exact `mode=upgrade`, current launcher/skill/state/npm package/wrapper evidence, and `legacy=[]`.

Installed ownership verification:

`python ...\namespace_ownership.py verify --root ...\.cogentnexus-openclaw --workspace ...\workspace`

exited `0` and reported product `cogentnexus-openclaw`, display name `CogentNexus-OpenClaw`, version `0.9.3`, canonical workspace/state/skill/launcher/plugin paths, expected task/service identities, UTC install time, and `migrationSource: null`.

Native inventory contained 72 plugins: exactly one enabled/loaded `cogentnexus-openclaw` v0.9.3 at the canonical managed npm root, zero legacy plugin, and zero differences in the 71 unrelated plugin identities. Managed npm projects changed only by adding `openclaw-plugin-cogentnexus-openclaw` (7 to 8).

`cnxclaw.cmd` points to canonical `cnxclaw_v093.py` and contains no legacy state/launcher reference. `cnxclaw.cmd status` exited `0`; `check provider ollama` exited `0`; provider status identified only selected Ollama, healthy with four models.

`CogentNexus-OpenClaw-Supervisor` exists, enabled/Ready, last result `0`, using canonical `host_control_v092.py` and `.cogentnexus-openclaw` root. Legacy supervisor and all legacy launcher/skill/state/plugin identities remain absent.

## Required check mismatch and exact blocker

Task 050 requires:

`cnxclaw.cmd check cogentnexus`

The exact command returned exit `3`, `SYSTEM READINESS: INDETERMINATE`. JSON-mode evidence identified the deterministic cause:

`unsupported check component: cogentnexus`

Installed v0.9.3 `checks.component_check()` maps the canonical component name `cogentnexus-openclaw`, not the legacy/generic name `cogentnexus`. The read-only canonical comparison:

`cnxclaw.cmd --json check cogentnexus-openclaw`

returned exit `0`, verdict `READY`, with PASS for core/provider/check scripts and PASS for MANAGED controller state (`selectedProvider=ollama`, desired Gateway/provider running).

This is a Task 050 command-specification mismatch, not evidence of an unhealthy installed runtime. Nevertheless, the exact required command did not succeed and no source repair is authorized, so the result cannot be PASS.

## MANAGED runtime and preservation

Controller is `managed`, desired Gateway/provider `running`, selected provider `ollama`, transition null, generation `6`. Gateway is reachable and healthy at PID 52324. Ollama endpoint is healthy; no model pull/delete/reconfiguration occurred and the same four-model inventory remains.

AGENTS has exactly one canonical begin/end marker pair and zero legacy markers. Removing the canonical block in memory reproduces exactly 7,196 bytes and baseline SHA-256 `C9A664B...3604C`. New install backup `AGENTS.pre-host-change-20260824T120921Z.md` has the same size/hash.

OpenClaw config contains only the new `cogentnexus-openclaw` entry in addition to the prior unrelated entries; no legacy entry/load path exists. Task 049 backup manifest remains byte-identical at `7525DAB...F42BA3A`. Source namespace lint passes. Primary repository branch/status remains unchanged. No installer/npm/plugin-install/CogentNexus lifecycle orphan and no Procmon process remains. HermesAgent, Ecosystem, staged-capability-loop, retained evidence, unrelated workspace data, and unrelated OpenClaw plugin identities were not acted on.

Key created hashes:

- `cnxclaw.cmd`: `8DB1F256BB56C298FFFB14E8A761CAA7DBEC56EA334B0F4558C3CDA563AA46EF`
- installed `SKILL.md`: `05FB55B2E92A66874AEEB2E3B0A778DDAEBFB506980108A1CA0A6D2200E4EB57`
- ownership manifest: `D299F290D508C783AE33124FCC7E582349BF9C7A73C47D07DD38207EBF2F4207`

## Mutation and retry accounting

- default installer: 1
- second installer/clean reinstall/migration/Release installer: 0
- manual partial completion: 0
- plugin repair/registry refresh/doctor fix: 0
- reset/uninstall/disable/stop/restart acceptance test: 0
- force kill/broad cleanup/automatic legacy restore: 0
- manual SQLite/config edit: 0
- Ollama/model mutation: 0

No external side effect was repeated.

## Recommendation

Blocker type: task/specification command mismatch plus installer-exit observation gap.

Recommended narrow successor: accept the durable installation evidence, replace the obsolete required command with canonical `cnxclaw.cmd check cogentnexus-openclaw`, and run a read-only acceptance task that also captures process exit code with a wait-and-record wrapper. Do not reinstall, repair, enable, restart, or manually complete the already-installed product.

Human decision required: **NO**. ChatGPT can issue the corrected read-only acceptance task from this evidence.

Remaining uncertainty: the exact terminated installer child exit code was not retained. The installed/runtime state itself is fully materialized and healthy under the canonical component check.
