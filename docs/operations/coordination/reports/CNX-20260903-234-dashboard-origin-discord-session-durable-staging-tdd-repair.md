# CNX-20260903-234 — Dashboard-origin Discord-session durable staging TDD repair

## Disposition

`PASS_DASHBOARD_ORIGIN_DISCORD_SESSION_DURABLE_STAGING_REPAIR_GREEN`

This is a repository/TDD repair result only. No live installation, semantic send,
replay, recovery repair, Ticket mutation, release, tag, asset publication, or
force-push was performed under Task 234.

## Authority and scope

- Successor task: `CNX-20260903-234`
- Accepted predecessor repair: `9a8510f1317c8e53c01c233b080ec20357cd22df`
- Predecessor Task-233 report head: `827577a053979517a46f419a6f63564bd7420570`
- Public `v0.9.3` remained immutable at `26ce64a624255278a3a0266ad38746e0e6ed2e31`
- Branch: `agent/v0.9.3-full-stabilization`
- Live mutation budget used: zero

The exact Task-233 failure lineage remained historical and untouched:
Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`, run
`e225013e-8d50-4479-b227-ca9a10b89a46`, owner
`agent:main:discord:channel:1531199905673252946`. Task 234 did not resend or
replay it.

## Root-cause proof

OpenClaw hook documentation for the installed `2026.7.1-2` contract exposes
trusted run context fields `ctx.channel`, `ctx.channelId`, and
`ctx.messageProvider`. The accepted source correctly recognized a Discord-owner
Ticket in `before_agent_finalize`, but the later `before_message_write` staging
path re-resolved only through `dashboardTicket()`, which rejects
`agent:*:discord:channel:*`. Thus a Dashboard-origin native result could be
visible while durable staging was absent.

The repair preserves the owner/session identity and does not broaden
`isDashboardSession()`. It carries the trusted ingress surface with the native
transcript candidate and permits the Discord-associated owner only when the
trusted context identifies Dashboard/WebChat origin. A real Discord-origin
context is excluded from Dashboard staging; legacy no-provider Discord
sentinel behavior remains covered by the existing regression suite. Unknown
surface does not grant the new Dashboard exception.

## TDD evidence

### Genuine RED

Test-only commit:
`6b1e496fa67b0f09678268ba918a98a824610286`

The new production-shaped tests initially produced one genuine failure:
Dashboard-origin context with a Discord-associated owner returned no durable
`cogentnexus-openclaw-delivery` staging result. The paired real Discord-origin
case passed (no Dashboard staging). Test harness-only issues discovered during
RED setup (async hook awaiting, schema absence treated as zero, and the
`IntakeTicket` snake_case/run-id fixture) were corrected without changing
production behavior.

### Minimal repair

Repair commits:

- `278a235fa9df75990a3ea7f1a8e3930441ead76b` — ingress-aware production repair
  plus regression test
- `43fd1d6f988431c7a94d24abc8a6811de46f78fa` — final TypeScript candidate type
  annotation; pushed without force

Production file changed by repair: `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`

Regression file: `plugins/cogentnexus-openclaw/src/task234-dashboard-discord-ingress.test.ts`

## Validation

Local final tree:

- `npm test`: **57 test files passed, 282 tests passed**
- targeted Task-234 and required dashboard/Discord boundary suite:
  **7 files, 23 tests passed**
- `npm run build`: **PASS**
- `npm run evaluation`: **PASS**
- `npm run plugin:validate`: **PASS**
- `npm audit --omit=dev`: **0 vulnerabilities**
- `npm pack --dry-run`: **PASS**, package `openclaw-plugin-cogentnexus-openclaw-0.9.3.tgz`, 194 packed files
- POSIX shell syntax and Python compile checks: **PASS**
- repository Python validation with project dependencies and `PYTHONPATH=.`:
  **504 passed, 5 skipped, 4 subtests passed**
- `git diff --check`: **PASS**

The historical Task-233 Windows/Python 3.14 `v093-response-ready-boundary`
timeout did not reproduce. The final local run passed without changing its
time contract.

## Exact GitHub Actions authority for final SHA

Final repair SHA: `43fd1d6f988431c7a94d24abc8a6811de46f78fa`

All workflows below were read from GitHub and matched that exact SHA:

- Validate run `33760819493`: **SUCCESS**
  - Linux/macOS/Windows Python 3.11 and 3.14 matrix passed
  - Windows PowerShell syntax, PS5.1 acceptance serializer, and numeric
    root-process capture passed
  - npm test/evaluation/audit/plugin validation passed
- Windows Installer Pack Smoke run `33760819324`: **SUCCESS**
- PS5.1 Acceptance Smoke run `33760819312`: **SUCCESS**

Non-blocking CI annotation: `actions/upload-artifact@v4` is being forced onto
Node.js 24 because Node.js 20 is deprecated. It did not affect conclusions.
No workflow was manually dispatched.

## Provenance and publication

- Final local HEAD: `43fd1d6f988431c7a94d24abc8a6811de46f78fa`
- Final remote HEAD: `43fd1d6f988431c7a94d24abc8a6811de46f78fa`
- Source plugin fingerprint after repair:
  `964d471f9e330cfeffd270f2200d563dea8c3e7b9252409660df96f1173f58b7`
- Accepted predecessor plugin fingerprint:
  `e3bcce04c3af57a7c0dd596203464e197c80e9d2c903593f73e032caa96f9386`
- Package identity changed because the source payload changed; version remained
  `0.9.3` and public tag/assets were not changed.
- Final worktree: clean
- No release/tag/asset mutation; no force-push

## Retry/side-effect ledger

```text
Dashboard semantic Sends: 0
Discord semantic Sends: 0
direct operator Sends: 0
semantic resubmissions: 0
recovery replay/resend: 0
manual Ticket/outbox/recovery/SQLite writes: 0
live install/enable/disable/uninstall: 0
provider/model substitution: 0
process termination: 0
Task-223/Task-233 forensic evidence mutation: 0
release/tag/asset mutation: 0
force-push/history rewrite: 0
```

## Stop boundary

Task 234 is complete and must stop here for independent ChatGPT review. A
future live install or semantic requalification requires separate authority and
must not be inferred from this repository GREEN result.
