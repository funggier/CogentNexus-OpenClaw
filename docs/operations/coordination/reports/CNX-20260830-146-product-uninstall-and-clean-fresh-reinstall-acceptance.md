# CNX-20260830-146 — Product Uninstall and Clean Fresh-Reinstall Acceptance

## Verdict

`FAIL_UNINSTALL`

The installed operator-facing `cnxclaw.cmd uninstall` command was invoked exactly once, but it failed at the interactive confirmation boundary before accepting input. Per the task contract, execution stopped immediately. No `y` was submitted, no retry was attempted, no cleanup/manual deletion was performed, and the fresh-install phase was not started.

## Authority and candidate

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`
- Initial live authority HEAD: `e039ec41ea69d6b9ab0138bfb2ec968fde67d4d2`
- Task: `CNX-20260830-146`
- Gate: `READY_FOR_HERMES`
- Matching report was absent before execution and before publication.
- Accepted implementation SHA: `fb5781c1abd68280760bd5b3b4a65fabd8a60e58`
- Fresh detached source: `C:\Users\CDQ-P\AppData\Local\Temp\cnx146-20260829T180850Z\source`
- Evidence root: `C:\Users\CDQ-P\AppData\Local\Temp\cnx146-20260829T180850Z\evidence`

All timestamps below are UTC.

## Candidate provenance

The exact accepted candidate was freshly cloned and checked out detached. The source tree was clean.

- Node: `v22.23.2`
- npm: `12.0.2`
- Python: `3.11.15`
- `npm ci`: exit `0`
- `npm run plugin:validate`: exit `0`
- package: `openclaw-plugin-cogentnexus-openclaw-0.9.3.tgz`
- package bytes: `200610`
- package SHA-256: `98a00a8a05ef4e7c600be045a4a4bbcbc6cb05f59acce5a3c54aabbacc80c014`
- packed file count: `178`
- candidate plugin fingerprint: `12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0`
- candidate `namespace_ownership.py` SHA-256: `10dda985e6d4553a73a8cdd3ef7f660937482c3ef0c2d2da8d15bcbfe8d39b66`
- candidate `install.ps1` SHA-256: `446c4657db58a8e5895ac8d20e894c18d334f7b84ad72ca618a66f9a55c8b6a3`

The candidate package and fingerprint were recomputed from the fresh source; historical hashes were not used as assumptions.

## Phase-A/B pre-uninstall gate

Read-only preflight ran from approximately `2026-08-29T18:08:50Z` through `2026-08-29T18:13:00Z`.

- Installed launcher help explicitly exposes `cnxclaw.cmd uninstall` and `cnxclaw.cmd reset`.
- Controller mode: `managed`.
- Desired Gateway/provider: `running` / `running`.
- OpenClaw version: `2026.7.1-2`.
- Plugin inventory: exactly one `cogentnexus-openclaw` identity.
- Plugin root: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw`.
- Root attestation: normal directory, `isReparse=false`, no link target.
- Plugin state: `enabled=true`, `status=loaded`, version `0.9.3`.
- Installed fingerprint: `12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0`.
- Ownership `verify`: exit `0`; canonical workspace/state/skill/launcher/plugin paths.
- Recovery preflight: `OWNERSHIP_PRESENT`, exit `0`.
- Gateway: healthy and listening on `127.0.0.1:18789`.
- Ollama: version `0.32.15`, reachable/healthy/ready.
- Recovery check: `READY`, `readOnly=true`, `stateChanged=false`.
- Delivery check: `READY`, `readOnly=true`, `stateChanged=false`, pending `0`.
- CogentNexus supervisor and OpenClaw Gateway scheduled tasks were registered and Ready.

SQLite was opened with `file:<path>?mode=ro`:

```text
PRAGMA integrity_check = ok
size = 159744 bytes
sha256 = 23977de27a131e3f2fd640480f87270ee556c8ec6715bcaf0a0bf0600ebf5215
tickets=2
ticket_events=14
cnx_direct_model_call=2
cnx_direct_recovery=0
cnx_assistant_delivery=0
ticket_outbox=0
cnx_sessions=2
```

The pre-uninstall database and selected state files were copied read-only to the external evidence root for comparison. The evidence copy was not restored or used to alter live state.

Dashboard semantic Send count before uninstall: `0`.

## Operator-facing uninstall attempt

The installed launcher itself was invoked exactly once:

```text
C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd uninstall
```

Execution details:

- invocation count: `1`
- started: `2026-08-29T18:14:19Z` (process timestamp)
- confirmation responses submitted: `0`
- required lowercase `y` submissions: `0`
- process exit code: `1`

The command reached and displayed the real confirmation boundary:

```text
WARNING: This will completely remove CogentNexus-OpenClaw.

CogentNexus-OpenClaw runtime state, configuration, startup integration, OpenClaw plugin,
skill files, backups, and cnxclaw.cmd will be removed.
OpenClaw and Ollama are not removed.

Continue? [y/N]:
```

The process then failed before accepting input:

```text
OSError: [Errno 9] Bad file descriptor
```

Trace boundary:

```text
lifecycle_v091.py, line 109, in confirm
answer = input("Continue? [y/N]: ").strip().lower()
```

This was an executor interactive/PTY boundary failure. It is nevertheless the first observed uninstall failure, so the task token is `FAIL_UNINSTALL` and no subsequent phase is authorized in this execution.

## Post-failure read-only state

Post-failure probes were executed without lifecycle commands, cleanup, or mutation.

- Controller remains `managed`.
- Plugin remains present, canonical, enabled, and loaded.
- Installed fingerprint remains `12c6d1b5b6ffd938353dd60c5d6190c34a609663369f619ff4fc7cbd176119e0`.
- Ownership verification remains exit `0`.
- Gateway remains healthy on `127.0.0.1:18789`.
- OpenClaw remains `2026.7.1-2`.
- Ollama remains version `0.32.15`, reachable/healthy/ready.
- Recovery and delivery remain `READY`, read-only, state unchanged, pending `0`.
- CogentNexus and OpenClaw scheduled tasks remain present/Ready.
- SQLite remains `integrity_check=ok` with the same counts:

```text
tickets=2
ticket_events=14
cnx_direct_model_call=2
cnx_direct_recovery=0
cnx_assistant_delivery=0
ticket_outbox=0
cnx_sessions=2
```

- Dashboard semantic Send count remains `0`.

No evidence indicates that uninstall mutation began; the command failed at confirmation input. No deferred-cleanup wait was started because uninstall did not exit successfully.

## Side-effect accounting

- Operator-facing uninstall invocations: `1`
- Confirmation `y` inputs: `0`
- Fresh-install invocations: `0`
- Installer retries: `0`
- Manual CNX file deletion/cleanup: `0`
- Manual plugin lifecycle commands: `0`
- Dashboard semantic Sends/resends: `0`
- Ticket/workflow/outbox/delivery/recovery/database mutation: `0`
- Crash/recovery injection: `0`
- Reset/uninstall helper substitution: `0`
- Unrelated process/service/task mutation: `0`
- Reboot: `0`
- Credential/secret access: `0`

## Unproven items

Because uninstall failed before confirmation, this execution does not prove:

- successful uninstall;
- product-owned deferred cleanup;
- CNX-absent/native-OpenClaw clean state;
- provider preservation after uninstall;
- fresh installation from the accepted candidate;
- fresh ownership/database creation;
- post-fresh-install managed health.

The task explicitly forbids retrying the uninstall or proceeding to fresh installation after this failure. A future attempt requires independent review and a new narrow authorization/task.

## Evidence index

- `a00-source.txt`
- `a01-npm-ci.txt`
- `a02-plugin-validate.txt`
- `a03-npm-pack.json`
- `a04-package-hash.json`
- `a05-candidate-fingerprint.json`
- `a06-source-hashes.txt`
- `b01-launcher-help.json`
- `b02-status.json`
- `b03-checks.json`
- `b04-openclaw-version.json`
- `b05-openclaw-plugins.json`
- `b06-ownership-verify.json`
- `b07-installed-fingerprint.json`
- `b08-recovery-preflight.json`
- `b09-root-attestation.json`
- `b10-ollama.json`
- `b11-gateway-task.json`
- `b12-filesystem.json`
- `b13-sqlite-readonly.json`
- `uninstall-process-log.txt` (captured process output)
- `f01-status.json` through `f11-sqlite.json`

Per the coordination contract, this report is the only repository change for Task 146. Execution stops here for independent ChatGPT review.
