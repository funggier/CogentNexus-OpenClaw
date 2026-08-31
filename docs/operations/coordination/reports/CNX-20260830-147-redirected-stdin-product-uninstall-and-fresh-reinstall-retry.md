# CNX-20260830-147 — Redirected-Stdin Product Uninstall and Fresh-Reinstall Retry

## Verdict

`PASS`

Task 147 completed the authorized lifecycle acceptance using a qualified non-PTY redirected-stdin harness.

## Remote authority

- Repository: `https://github.com/funggier/CogentNexus-OpenClaw.git`
- Coordination branch: `agent/v0.9.3-full-stabilization`
- Live remote HEAD observed before execution: `98990d7b4f48bd3847af4bfe7ff4170f469a7e1a`
- Active task: `CNX-20260830-147`
- Execution mode: `LIVE_WINDOWS_REDIRECTED_STDIN_UNINSTALL_AND_FRESH_REINSTALL_ACCEPTANCE`
- Accepted production source SHA: `fb5781c1abd68280760bd5b3b4a65fabd8a60e58`
- Matching report was absent before publication.

`ACTIVE.md`, `STATUS.md`, and this task authority were read from the freshly fetched GitHub branch. The detached source used for provenance and installation was freshly fetched at the exact accepted SHA; the local checkout was not used as coordination authority.

## Phase A — live preflight

Read-only evidence was preserved outside CNX live roots. The pre-mutation gate proved:

- installed `cnxclaw.cmd` existed and exposed `uninstall` and `reset`;
- ownership verification passed;
- controller was `MANAGED`;
- exactly one canonical non-reparse `cogentnexus-openclaw` plugin was enabled/loaded;
- installed plugin fingerprint matched the accepted candidate;
- Gateway, OpenClaw and Ollama were healthy;
- recovery and delivery checks were `READY`, read-only, with pending outbox `0`;
- supervisor/Gateway task state was coherent;
- SQLite was opened read-only, with `integrity_check=ok`;
- preflight durable counts were the preserved Task-146 baseline: `tickets=2`, `ticket_events=14`, `cnx_direct_model_call=2`, `cnx_direct_recovery=0`, `cnx_assistant_delivery=0`, `ticket_outbox=0`, `cnx_sessions=2`;
- Dashboard semantic Sends were `0`.

## Phase B — harmless redirected-stdin qualification

The exact non-PTY subprocess mechanism used for uninstall was qualified first with a temporary harmless Python child that called `input()` once. The mechanism used captured stdin/stdout/stderr and exact exit status.

Evidence:

- `UseShellExecute=false` equivalent: Python `subprocess.Popen` with pipes;
- stdout and stderr captured;
- exactly one input line written: `y`;
- child output proved `received=y`;
- stderr was empty;
- child exit code was `0`;
- no extra input was written;
- child did not import or mutate CNX/OpenClaw state.

## Phase C — product uninstall

The installed launcher itself was invoked exactly once through the qualified redirected-stdin mechanism:

```text
cmd.exe /d /c C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd uninstall
```

Execution accounting:

- uninstall invocation count: `1`;
- confirmation writes: exactly one line `y`;
- stdin was closed after the line;
- stdout and stderr were captured;
- real process exit code: `0`;
- real product prompt was reached and confirmation accepted;
- output reported `COGENTNEXUS-OPENCLAW UNINSTALL: PASS`;
- no second uninstall attempt.

The uninstall output showed the expected product-owned removal and native preservation boundary: CNX runtime state, configuration, startup integration, plugin, skills, backups and launcher were removed; OpenClaw and Ollama were not removed.

## Phase D — deferred cleanup and native state

Only read-only bounded polling was used after uninstall; no manual deletion or cleanup was performed. Cleanup converged immediately at the first observation:

- `cnxclaw.cmd`: absent;
- `.cogentnexus-openclaw`: absent;
- workspace CNX skill: absent;
- canonical CNX plugin root: absent;
- CNX AppData root: absent;
- CNX supervisor task: absent;
- native OpenClaw remained installed and usable (`2026.7.1-2`);
- native Gateway remained healthy on loopback port `18789`;
- Ollama remained installed, reachable and healthy at `http://127.0.0.1:11434`;
- Ollama model inventory remained present;
- Dashboard semantic Sends remained `0`.

## Phase E — one clean fresh install

The exact accepted detached source was used. Candidate provenance recomputation produced:

- source SHA: `fb5781c1abd68280760bd5b3b4a65fabd8a60e58`;
- package: `openclaw-plugin-cogentnexus-openclaw-0.9.3.tgz`;
- package size: `200610` bytes;
- packed file count: `178`;
- package SHA-256: `98a00a8a05ef4e7c600be045a4a4bbcbc6cb05f59acce5a3c54aabbacc80c014`;
- npm shasum: `407f229ece83e76e435044baa6337eb07f221c6c`;
- candidate plugin fingerprint: `12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0`;
- candidate `namespace_ownership.py` SHA-256: `10dda985e6d4553a73a8cdd3ef7f660937482c3ef0c2d2da8d15bcbfe8d39b66`.

The normal installer was invoked exactly once, without skip/staging flags or a helper installer:

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:/Users/CDQ-P/AppData/Local/Temp/cnx147-live-20260829T182519Z/source/scripts/install.ps1 -Workspace C:/Users/CDQ-P/.openclaw/workspace
```

- fresh-install invocation count: `1`;
- exit code: `0`;
- installer output reported successful completion;
- no fresh-install retry.

The installer recorded the expected npm validation/install output (`352` packages added, `353` audited, four high-severity audit findings). No audit remediation was performed.

## Phase F — fresh-install proof

Read-only post-install evidence proved:

- exactly one canonical CNX plugin identity;
- plugin version `0.9.3`, enabled and loaded;
- installed fingerprint exactly matched the candidate;
- installed ownership helper hash exactly matched the candidate;
- ownership manifest was newly created and `verify` passed;
- controller was `MANAGED`;
- Gateway was healthy, loopback-only on `127.0.0.1:18789`, OpenClaw `2026.7.1-2`;
- Ollama was reachable/healthy/ready with four models;
- recovery check was `READY`, read-only, no active incident;
- delivery check was `READY`, read-only, pending outbox `0`;
- expected `CogentNexus-OpenClaw-Supervisor` and `OpenClaw Gateway` tasks were registered and coherent;
- SQLite `integrity_check=ok`;
- fresh database counts contained no historical Task-145/146 durable rows:
  - `tickets=0`;
  - `ticket_events=0`;
  - `cnx_direct_model_call=0`;
  - `cnx_direct_recovery=0`;
  - `cnx_assistant_delivery=0`;
  - `ticket_outbox=0`;
  - `cnx_sessions=0`;
- no stale install/rollover transaction was observed;
- Dashboard semantic Sends remained `0`.

## Side-effect accounting

- Dashboard semantic Sends: `0`;
- manual database/semantic mutation: `0`;
- manual CNX live-file deletion: `0`;
- manual plugin/controller/ownership normalization: `0`;
- uninstall invocations: `1`;
- uninstall confirmation lines: `1` (`y`);
- fresh installer invocations: `1`;
- retries: `0`;
- reset/crash/recovery injection: `0`;
- alternate installer/clean-reinstall helper: `0`;
- unrelated process/service/task mutation: `0`;
- credentials/secrets disclosed: `0`;
- merge/tag/release/force-push: `0`.

## Evidence locations

Evidence root:

```text
C:/Users/CDQ-P/AppData/Local/Temp/cnx147-live-20260829T182519Z/evidence
```

Important evidence files include `c01-uninstall-run.json`, `c02-deferred-cleanup.json`, `c04-native-openclaw-plugins.json`, `c05-native-gateway.json`, `c06-ollama.json`, `c07-cnx-task-absence.json`, `d01-fresh-installer.json`, `post-status.txt`, `post-check-system.txt`, `post-check-recovery.txt`, `post-check-delivery.txt`, `post-openclaw-plugins.txt`, `post-filesystem.json`, `post-ownership-verify.txt`, `post-plugin-fingerprint.txt`, `post-helper-hashes.txt`, `post-npm-pack.json`, `post-package-sha256.txt`, and `post-db.json`.

## Completion

All Task-147 lifecycle gates passed. This report is the only requested publication. Stop after publication for independent ChatGPT review.
