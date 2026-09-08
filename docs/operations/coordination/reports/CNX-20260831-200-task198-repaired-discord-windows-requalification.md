# CNX-20260831-200 — Task 198 Repaired Discord Windows Requalification

- **Task:** CNX-20260831-200
- **Parent:** CNX-20260831-198
- **Authority branch:** `agent/v0.9.3-full-stabilization`
- **Authority tip at start:** `9683c4da0bf64145d36cf5412319dcbcc890633b`
- **Frozen product candidate:** `9f4eaa429b2540540e7d6f6c2af99067960e45fb`
- **Evidence root:** `C:/Users/CDQ-P/AppData/Local/Temp/cnx200-preflight-20260831T`
- **Disposition:** `BLOCKED_EVIDENCE`

## Executive result

Task 200 consumed its one supported install-over invocation, but the installer did not reach a provable terminal completion boundary within the executor observation window. The original PowerShell process remained running, no installer exit-code artifact was produced, and the output stopped before the final enable/gateway/supervisor/status completion checks.

Per the task fence, no retry, kill, second installer invocation, reset, uninstall, fresh reinstall, provider substitution, source edit, or Discord Send was performed. The one human Discord Send phase was **not started** because the install-over completion and managed-runtime convergence were unproven.

## Scope and mutation ledger

### Actions performed

- Fresh authority clone and exact candidate checkout: read-only.
- Artifact download from exact package-proof run: evidence-only.
- Read-only runtime/provenance/health/SQLite probes.
- Exactly one supported invocation:

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -File \
  C:/Users/CDQ-P/AppData/Local/Temp/cnx200-candidate-9f4eaa429b2540540e7d6f6c2af99067960e45fb/scripts/install.ps1 \
  -Workspace C:/Users/CDQ-P/.openclaw/workspace
```

- One report-file write and report-only Git commit/push.

### Actions not performed

```text
Human Discord Send: 0 / 1
Hermes/bot/API send: 0
Retry/regenerate: 0
Second room/message: 0
Injection: 0
Reset: 0
Uninstall: 0
Fresh reinstall: 0
Release/tag mutation: 0
Source/config/test/workflow edit: 0
Artificial SQLite lock: 0
Provider/model substitution: 0
Process termination: 0
```

The install-over mutation itself is consumed and must not be replayed under this task.

## Candidate and package provenance

Candidate checkout:

```text
HEAD: 9f4eaa429b2540540e7d6f6c2af99067960e45fb
```

Package proof was downloaded through `gh run download` from exact Run `33413832703`, artifact ID `9766213750`. The downloaded archive hashes matched the task proof:

```text
cogentnexus-openclaw-v0.9.3.tar.gz
379f0b4a7c12d4f350e0d3065dd25c7ab2bde80089adb16bfa64d6bbc673cdfb

cogentnexus-openclaw-v0.9.3.zip
07bcdc45810c86efb5535075e1e560f9477e65a1f72e5299d75dea6dbc542d3e
```

Candidate source installer SHA-256:

```text
scripts/install.ps1
8cb713b7ddfe5be113530298fe3195094c0055a78ff63cdb393a483debc47e56
```

Candidate source plugin fingerprint:

```text
f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1
```

## Phase A — pre-state

The corrected, derived-root preflight passed:

- OpenClaw: `2026.7.1-2 (0790d9f)`;
- existing host mode: `managed`;
- selected provider: `ollama`;
- Ollama reachable/healthy/ready;
- Gateway healthy on `127.0.0.1:18789`;
- delivery check: `READY`, pending outbox `0`, `readOnly=true`, `stateChanged=false`;
- recovery check: `READY`, no active incident, recovery attempts `0`;
- SQLite `PRAGMA integrity_check`: `ok`;
- known Discord session: `agent:main:discord:channel:1531199905673252946`;
- historical baseline for that session: one existing Ticket and seven events; no new semantic action was performed during preflight.

The first ownership probe used the wrong root (`C:/Users/CDQ-P/.openclaw`) and failed because `ownership.json` is under the derived state root. The corrected probe used:

```text
C:/Users/CDQ-P/.openclaw/workspace/.cogentnexus-openclaw
```

and passed with exit `0`. The failed wrong-root invocation is retained as a harness issue, not product drift.

## Phase B — installer boundary

Installer stdout was captured in `b01-install.stdout`; stderr in `b01-install.stderr`.

Verified completed stages:

```text
ticket-db-bootstrap       exit_code=0
action plugin-npm-pack     exit_code=0
plugin-rollover-prepare   exit_code=0
plugin-install-local-package exit_code=0
plugin-disable-post-install exit_code=0
plugin-rollover-finalize  exit_code=0
owned-runtime-ensure      exit_code=0
```

The installer output then stopped after writing the launcher and a passthrough policy result. No final installer completion line or exit-code file was produced.

At the last process scan, the original invocation still had:

```text
PowerShell PID: 11704  (running)
Child conhost PID: 11588
```

The gateway process was separately identified as PID `21760`; it was not terminated or treated as an installer child. No process was killed because Task 200 does not authorize observer cleanup or process termination.

The current post-install state is partially converged:

- installed version: `0.9.3`;
- installed plugin fingerprint: `f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`;
- installed fingerprint equals the frozen candidate source fingerprint;
- ownership manifest verify: exit `0`;
- installed-at: `2026-08-31T17:09:43.774913+00:00`;
- host mode: `passthrough`;
- startup policy: `disabled`;
- plugin was installed while runtime registration was suppressed by passthrough mode;
- no proof exists that the later installer `enable` and final convergence checks completed.

The installer therefore cannot be classified as successful merely from the intermediate stage markers or installed fingerprint. The live mutation crossed the install boundary, but the final completion/managed convergence boundary is unproven.

## Phase C — Discord Send

Not started. No nonce was generated or sent to the user. No human Discord prompt was issued. No Discord semantic or durable-delivery result is claimed.

This was required because the task explicitly requires installed managed-runtime convergence before preparing the one human Send, and the installer completion boundary remained ambiguous.

## Post-state read-only evidence

Captured after the timeout/ambiguous boundary:

- installed plugin fingerprint matched candidate: `f8267417...`;
- ownership verify passed against derived state root;
- Gateway remained healthy and listening on `127.0.0.1:18789`;
- Ollama remained selected and ready;
- delivery check remained `READY`, pending outbox `0`;
- recovery check remained `READY`, no active incident, attempts `0`;
- SQLite integrity remained `ok`;
- ticket count for the known Discord session remained `1` and its event count remained `7`;
- total direct model calls: `10`;
- total assistant-delivery rows: `7`;
- total outbox rows: `0`;
- total direct-recovery rows: `0`.

These healthy read-only results do not prove installer completion, managed enablement, or Discord requalification.

## Issue register

### I-01 — Installer completion boundary unproven

- **Observed:** executor timed out; `b01-install.exit` was absent; final completion line was absent; PowerShell PID `11704` remained running.
- **Class:** incomplete evidence boundary / installer execution ambiguity.
- **Product mutation impact:** install-over effects were consumed; installed plugin bytes changed to the candidate fingerprint.
- **Corrective action:** none; no retry or termination authorized.
- **Remaining consequence:** final enable, managed convergence, final installer exit code, and subsequent Discord Send are unproven.

### I-02 — Wrong-root ownership probe

- **Observed:** initial `verify --root C:/Users/CDQ-P/.openclaw` failed because `ownership.json` was absent there.
- **Class:** harness/path error.
- **Product impact:** none; no state changed.
- **Corrective action:** reran read-only verification using state root derived by `recovery-preflight`; it passed.
- **Remaining consequence:** initial failure remains part of evidence history but does not determine the product disposition.

### I-03 — Artifact API Accept-header probe

- **Observed:** initial `gh api` artifact download attempt returned `HTTP 415` because the installed `gh` wrapper rejected `Accept: application/zip`.
- **Class:** harness/API invocation error.
- **Product impact:** none.
- **Corrective action:** used supported `gh run download` against exact run/artifact identity; hashes matched task proof.
- **Remaining consequence:** no package provenance gap remains.

### I-04 — SQLite schema collector mismatch

- **Observed:** an early read-only collector queried historical table names (`cnx_ticket`, `cnx_ticket_event`) and received `no such table`.
- **Class:** harness/schema-binding error.
- **Product impact:** none; no state changed.
- **Corrective action:** inspected `sqlite_master`/`PRAGMA table_info` and used current tables (`tickets`, `ticket_events`, etc.).
- **Remaining consequence:** initial failed query is preserved; corrected integrity/count evidence is authoritative.

### I-05 — Bash/Python quoting errors

- **Observed:** two inline collectors failed due Python string quoting and one PowerShell process probe was interrupted by Bash expansion of `$_`.
- **Class:** harness/quoting error.
- **Product impact:** none.
- **Corrective action:** used explicit script files and corrected native paths; no lifecycle action was replayed.
- **Remaining consequence:** these failures are executor-side evidence only.

## Acceptance matrix

| Criterion | Result | Evidence/limitation |
|---|---|---|
| Exact candidate installed through one supported install-over | `UNPROVEN` | Intermediate stages passed; final installer exit/completion missing |
| Active installed identity matches repaired candidate | `PASS` | Candidate and installed fingerprint both `f8267417...` |
| OpenClaw/Gateway/managed Ollama/SQLite healthy | `PARTIAL` | OpenClaw/Gateway/Ollama/SQLite healthy; Host remained passthrough, not managed convergence |
| Exactly one human Discord Send | `NOT PERFORMED` | Correctly not started |
| Exactly one Ticket/model call for tested nonce | `NOT PERFORMED` | No nonce and no Send |
| Native visible Discord nonce result | `NOT PERFORMED` | No Send |
| `response_ready -> delivery_confirmed -> completed` for tested Send | `NOT PERFORMED` | No Send |
| No retry/recovery/duplicate/outbox residue | `PASS` for this task boundary | no new semantic action; outbox `0`, recovery `0` |
| No `before_agent_run hook failed` for tested Send | `NOT APPLICABLE` | no tested Send |
| No destructive lifecycle/publication action outside authorized install-over | `PASS` | no reset/uninstall/release/tag/source mutation |

## Final disposition

```text
BLOCKED_EVIDENCE
```

The exact repaired candidate bytes are installed and fingerprint-matched, but the supported install-over process did not provide a verified terminal completion boundary and left the host in passthrough/disabled state at the last read-only observation. Task 200 therefore stops before the human Discord Send phase. No product root cause or new repair is claimed, and no retry/cleanup/mutation is authorized by this task.

## Evidence manifest

```text
a01-time.*
a02-openclaw-version.*
a03-recovery-preflight.*
a04-ownership-verify.*
a05-installed-fingerprint.*
a06-status.*
a07-delivery.*
a08-recovery.*
a09-provider.*
a10-gateway.*
a11-sqlite-readonly.json
a12-artifact-download-failure.*
a13-download-method.txt
a14-gh-run-download.txt
a15-ownership-verify-derived.*
a16-sqlite-schema-counts.json
a17-installer-help.txt
a18-known-session-baseline.json
b01-install.stdout
b01-install.stderr
b02-process-identity.json
b03-process-scan.ps1
b03-process-scan.json
b04-installer-tree.ps1
b04-installer-tree.json
c-01-time.*
c-02-fingerprint.*
c-03-ownership.*
c-04-status.*
c-05-delivery.*
c-06-recovery.*
c-07-provider.*
c-08-gateway.*
c-09-process-scan.*
c-10-sqlite-post.json
c-11-candidate-fingerprint.*
```

No credentials, tokens, passwords, or connection strings were recorded.
