# CNX-20260824-054 — Repeat v0.9.3 Install-Over with Durable Evidence

Status: **BLOCKED**

Result: `BLOCKED_INSTALLER_EXIT_UNOBSERVED`

Repository: `funggier/CogentNexus-OpenClaw`
Branch: `agent/v0.9.3-recovery-reality-tests`
Fetched start HEAD: `28addfa49d682dffa87d8f513259eaa82f39ba2f`

## Source and essential preflight

- New isolated full clone: `C:\Users\CDQ-P\AppData\Local\Temp\cnx054-clone-20260824T130456Z`.
- Task 051 implementation `6d90025f832bb36c477176809a0af2e6c1858c19`, Task 053 report `7b999b783e1e3d0ece8777fa81ee7741e0cbea1a`, and Task 053 review commit `0e5390e7d7e170553b285aba37c80d6d8440131a` were present/ancestors.
- `ACTIVE.md`, coordination `STATUS.md`, and Task 054 agreed on `READY_FOR_CODEX / MANUAL_WITH_HUMAN_GATE`. The matching report was absent (`git cat-file -e` exit `128`), clone clean, local/remote HEAD equal, and concurrent installer/lifecycle/publisher count zero.
- Classifier exited `0`: exact `mode=upgrade`, `legacy=[]`. Ownership verifier exited `0`, installed v0.9.3, canonical paths, `migrationSource: null`.
- Live help files were the Task 050 blobs `f732aeef...` and `70ddc450...`; isolated source contained Task 051 blobs `fed54bec...` and `bad87488...`.
- Controller was MANAGED generation 6 with Ollama selected and desired Gateway/provider running. Gateway status exited `0` and was healthy at PID 52324.
- SQLite URI read-only integrity was `ok`; tickets/events/outbox/sessions were all zero and schema migrations 6.
- AGENTS contained one canonical marker pair and zero legacy markers; stripped baseline was exactly 7,196 bytes, SHA-256 `C9A664B73200AE5D6B0DA0908DE3256CDB4DDA8BA6FE99F5E6C5115C3983604C`.
- Plugin inventory was 72 total: one loaded canonical v0.9.3 plus 71 unrelated; four Ollama models were present.
- Task 049 manifest SHA-256 was `7525DAB74EE1801A26B4B1CF824CB22155E971BCB63697149580ED1B9F42BA3A`. Primary repository remained on `master` with its pre-existing untracked state.

## Durable evidence and exact invocation

Evidence directory created before launch and retained:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx054-evidence-20260824T130631Z`

It contains preflight JSON, report draft, wrapper, stdout/stderr, and atomic wrapper poststate. Evidence hashes include:

- `preflight.json`: 1,919 bytes, SHA-256 `6EFFC89BAF80642660206295DFD5D89D52E1B5B4833F281B8D594C4434806BBD`;
- `installer.stdout.log`: 6,033 bytes, SHA-256 `99BC794CD56C735F3DCEFD58A0DF23DFFDA4FE2DEF1117428DE2E40BED19FE72`;
- `installer.stderr.log`: 2,700 bytes, SHA-256 `4BC0ED73CD02FAF852F16B9B53A9EDA8679BB9DDFD6C0734A73D969247CB842F`;
- `wrapper-poststate.json`: 515 bytes, SHA-256 `5A581BE722EAB48BEB33C887152E322848520095E3E560D85CCE33F7F96B5477`;
- wrapper: SHA-256 `96C80C027A95ABDD8C89113C6C1C60FF703B5A5438D1F5A71B8664CD1EC303B0`.

The retained process wrapper invoked exactly once:

`powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "C:\Users\CDQ-P\.openclaw\workspace"`

Child PID: `29240`
Start UTC: `2026-08-24T13:07:40.9648342Z`
End UTC: `2026-08-24T13:10:16.7435106Z`
Duration: `155.779` seconds
Invocation count: `1`

The exact child ended and no longer exists, but the retained wrapper poststate recorded `observedExitCode: null`; the wrapper consequently returned exit `0` from a null value. The required exact installer exit code is therefore unobserved and is not inferred.

## Installer stages and failure evidence

Stdout proves the installer body entered and performed these authorized stages:

1. detected existing MANAGED installation and entered PASSTHROUGH/native boundary (`Pre-install native handoff: PASS`);
2. disabled startup and preserved a scheduler backup;
3. backed up the existing Task 050 skill to `...\install-backups\cogentnexus-openclaw-20260824-200834`;
4. installed the Task 051 skill; validation passed;
5. built/validated/packed the v0.9.3 plugin and installed it into a new generated npm project;
6. disabled the newly registered plugin while PASSTHROUGH and recreated the launcher.

The installer then stopped at ownership verification. Stderr records two canonical v0.9.3 payload roots with the same fingerprint `0e5746d063af1bf6d82e0901ce4e5f3def57a9ecb41ec2d4bdd70ffcd6599ddb`:

- prior root `...\npm\projects\openclaw-plugin-cogentnexus-openclaw\node_modules\openclaw-plugin-cogentnexus-openclaw`;
- new generated root `...\npm\projects\openclaw-plugin-cogentnexus-openclaw__openclaw-generation__g-bbc979095f8845a1\node_modules\openclaw-plugin-cogentnexus-openclaw`.

`namespace_ownership.py` rejected this as `installed plugin path is ambiguous; refusing ownership`. The installer did not reach ownership recreation, MANAGED re-enable, canonical supervisor return, or final integration verification.

## Bounded poststate

- Classifier and ownership verifier now exit `1` on the same two-root ambiguity.
- Both installed help files are byte-content identical to Task 051 source (`git diff --no-index --ignore-space-at-eol`, exit `0` for each).
- Controller is PASSTHROUGH, generation 7, desired Gateway `running`, desired provider `unchanged`; startup policy is disabled and supervisor adapter absent.
- Native plugin inventory still exposes one canonical entry, now disabled and resolving to the new generated root; both physical payload roots remain. No cleanup was attempted.
- Gateway remains healthy/reachable at PID 47292. Ollama remains healthy with the same four models.
- SQLite remains byte-identical to prestate, SHA-256 `630398BC4304AD2BDEFF01D55431597BE3464BA783107E01C5EF475C2F0C1613`, integrity `ok`, with zero tickets/events/outbox/sessions.
- Registered policy remains byte-identical, SHA-256 `14EDEAD0180690C3D9565E864D2BDAAAE60E32DF9EF2C64EBD2A1238DF5CD8B4`.
- AGENTS is now the accepted stripped 7,196-byte baseline with zero managed markers, the expected PASSTHROUGH effect. The prior full AGENTS was backed up as `AGENTS.pre-host-change-20260824T130747Z.md`.
- Ownership manifest remained the pre-install file, SHA-256 `D299F290D508C783AE33124FCC7E582349BF9C7A73C47D07DD38207EBF2F4207`; launcher content hash remained `8DB1F256BB56C298FFFB14E8A761CAA7DBEC56EA334B0F4558C3CDA563AA46EF` although its timestamp advanced.
- The install-over skill backup exists and contains the prior Task 050-prefix help files.
- Task 049 manifest remains byte-identical. Four-model inventory remains unchanged. No installer/lifecycle/plugin-install orphan was found.

The poststate is safe native/PASSTHROUGH but partial and ownership-ambiguous. It does not satisfy Task 054 acceptance.

## Safety and command accounting

- installer invocations: **1**
- retries/second installers: **0**
- installer-owned disable/plugin replacement/backup/launcher actions: **1 sequence**
- manual lifecycle commands outside installer: **0**
- manual repair/restore/config/database/AGENTS/plugin/task edits: **0**
- reset/uninstall/clean/fresh install/migration commands: **0**
- process termination/force-kill commands: **0**
- Procmon/Task 027/038 or excluded-system actions: **0**
- primary-repository mutations: **0**

No side effect was repeated. The isolated clone and durable evidence directory are retained pending remote report verification.

## Blocker and recommendation

Blocker types:

- **evidence-wrapper defect** — the exact terminated child exit code was not retained as a numeric value;
- **product/installer partial-state defect** — install-over created a second same-version/same-fingerprint managed npm root before ownership verification, causing ambiguity and leaving PASSTHROUGH/startup-disabled state.

Safest narrow remedy: ChatGPT should review this durable evidence and publish a separate diagnostic/remediation task that first adjudicates the two exact plugin roots and installer generation behavior, then authorizes only the narrow ownership-safe cleanup/recovery needed to return the already-installed Task 051 skill to coherent MANAGED state. Do not rerun the installer or manually delete either root without that reviewed task.

Human decision required: **NO** for recording this blocker; a new reviewed task is required before any recovery mutation.

Remaining uncertainty: exact child exit code is unobserved. The durable Python/PowerShell error proves installer failure semantics, but it is not substituted for the missing numeric exit code.
