# CNX-20260915-360 — Runtime Activation Verification Report

## Classification

`BLOCKED — SUPPORTED INSTALLER FAILED BEFORE CANDIDATE ACTIVATION`

The live runtime is **not proven** to load candidate `1aa7b37c23e2bb2abdd150a893f1f37102731089`. No Dashboard request or model inference was performed in CNX-360.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Coordination-authority commit: `7f2e670f88e0e5b923b452c2f6dc04084ce19530`
- Candidate source commit: `1aa7b37c23e2bb2abdd150a893f1f37102731089`
- Candidate checkout: detached exact candidate checkout under `cnx360-candidate`
- No `main`, tag/release `v0.9.5`, force-push, or history rewrite touched.

## Source and package evidence

Candidate checkout verification:

- `git rev-parse HEAD`: `1aa7b37c23e2bb2abdd150a893f1f37102731089`
- `npm run plugin:validate`: PASS
- Package version: `0.9.5`
- Package entry count: `246`
- Required package entry `dist/v091-release-entry.js`: present
- Candidate package path: `openclaw-plugin-cogentnexus-openclaw-0.9.5.tgz`
- Candidate package bytes: `240401`
- Candidate package SHA-256: `210e890278485e7e4ad31458923b633cbedee5ab1ea5dcd11367402fabfe6945`

This proves `SOURCE COMMIT -> PACKAGE`, not installation or active loading.

## Supported lifecycle used

Repository README identifies `scripts/install.ps1` as the supported installer; no undocumented install command was used. The exact candidate checkout's `scripts/install.ps1` was invoked with the existing workspace:

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -File cnx360-install.ps1
```

The installer performed its normal transactional pre-install native handoff and Gateway restart boundary. It then failed closed at:

```text
stage=plugin-rollover-prepare
exit_code=1
RuntimeError: plugin generation rollover requires PASSTHROUGH mode; observed None
```

The exact installer transcript is retained in the task execution output; decisive timestamps were:

- `plugin-npm-pack` start `2026-09-15T15:48:08.3799267Z`, complete exit `0`
- `plugin-rollover-prepare` start `2026-09-15T15:48:09.0207712Z`, complete exit `1`

No retry, manual repair, direct plugin install, configuration workaround, or second lifecycle invocation was performed.

## Installed artifact evidence

The existing artifact remained at:

`C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\openclaw-plugin-cogentnexus-openclaw-0.9.5.tgz`

- Installed artifact bytes: `241911`
- Installed artifact SHA-256: `74c9aebd4a4539ccc47f547537a29e293a1ddfa373ae86411367402fabfe6945`
- Byte comparison with the exact candidate package: `False`

Therefore the candidate package is not proven to be the installed artifact.

## Active runtime/plugin identity

Read-only `openclaw plugins list --json` after the failed lifecycle reported:

- plugin id: `cogentnexus-openclaw`
- version: `0.9.5`
- source: `C:\Users\CDQ-P\.openclaw\extensions\cogentnexus-openclaw\dist\v091-release-entry.js`
- origin: `global`
- `enabled: false`
- `status: disabled`
- `hookNames: []`
- `hookCount: 0`

The active runtime therefore does not load the candidate plugin. A source-commit identity for the active module is unavailable, and the installed artifact hash differs from the candidate package hash.

## Gateway and managed-state evidence

Post-lifecycle read-only checks:

- Gateway: `running`, Scheduled Task registered, PID `19844`
- Gateway version: `2026.7.1-2`
- Connectivity probe: `ok`
- Listening: `127.0.0.1:18789`
- Controller: `cnxMode=disabled`, `mode=passthrough`, `desiredGateway=running`, generation `102`
- Controller SHA-256: `f5e7a5704fbe180766dba3b0bf3d6a621f1702dfb784ef462be349e0463b5e6a`
- `openclaw.json` plugin config: `ticketFirst=true`, `preInferenceAdmission=true`, but plugin entry `enabled=false` and `providerMode=passthrough`
- `openclaw.json` SHA-256: `7d5c35307163487cea9962856ccc698ba9b82e8803e21c6e6f528cc0e585302c`

Gateway health returned after the installer-triggered reload/restart, but that health result does not prove candidate activation. The before-state was managed/active/generation `101`; the post-state is disabled/passthrough/generation `102`. This runtime-state change is recorded as installer-owned partial state, not repaired manually.

## Evidence-chain verdict

| Edge | Result | Evidence |
|---|---|---|
| SOURCE COMMIT -> PACKAGE | PASS | exact detached HEAD and candidate package SHA-256 |
| PACKAGE -> INSTALLED ARTIFACT | FAIL | candidate SHA `210e8902...` differs from installed SHA `74c9aebd...` |
| INSTALLED ARTIFACT -> ACTIVE RUNTIME | FAIL | plugin is `enabled=false`, `status=disabled`, no hooks |
| ACTIVE RUNTIME -> candidate source commit | UNPROVEN | no active candidate module identity; runtime disabled |

## Stop / handoff

Remain `BLOCKED`. Do not send `CNX360-DONE`, do not reuse `CNX359-DONE`, and do not create a repair task from this result. Operator Dashboard handoff is **not authorized** because active candidate identity was not proven. A successor task with explicit authority is required to reconcile the supported lifecycle failure and the installer-owned passthrough/disabled state before any Dashboard test.
