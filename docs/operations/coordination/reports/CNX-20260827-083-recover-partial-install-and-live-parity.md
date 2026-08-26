# CNX-20260827-083 — Recover Partial Install and Prove Live Parity

Result: `BLOCKED_SUPPORTED_RECOVERY_INSTALL_OVER`

## Scope and exact source

Task 083 was authorized to perform exactly one supported normal recovery install-over from the accepted Task-082 implementation:

`df412ed10522d79a722e1b48d681e7553cb79ae2`

Execution checkout:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx083-preflight-20260826T183022Z\candidate`

The checkout was detached at the exact source commit and clean before installation. No later unreviewed production source was mixed in.

Execution coordination HEAD before report publication:

`58533e25bb23f00606bccf236193e5c2d1a17f86`

## Phase A — pre-install partial-state re-proof

Evidence:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx083-preflight-20260826T183022Z\a01-live-preflight.txt`

Observed expected Task-081/082 partial state:

- PowerShell `5.1.19041.6456`
- Node `v24.18.0`
- npm `11.16.0`
- OpenClaw `2026.7.1-2 (0790d9f)`
- ownership verification: passed
- `recovery-preflight`: `OWNERSHIP_PRESENT`
- classification: `upgrade`
- controller: `passthrough`, generation `13`
- startup policy disabled
- Supervisor Scheduled Task absent
- AGENTS managed markers `0/0`
- prior canonical plugin generation registered but disabled
- launcher present and bound to the product-owned runtime
- Gateway Scheduled Task present/Ready; gateway connectivity healthy
- dashboard HTTP `200`
- Ollama `0.32.15`; accepted four-model inventory unchanged
- SQLite `integrity=ok`
- tickets `0`
- outbox `0`

No meaningful pre-install partial-state drift was found.

## Phase B — candidate preflight

Candidate source checks passed before live mutation:

- `scripts/resolve-npm-pack-artifact.ps1` present and PowerShell 5.1 syntax-valid
- `scripts/install.ps1` uses the resolver after `npm pack --json` and before rollover
- candidate `npm ci`: passed
- candidate `npm run plugin:validate`: passed
- focused Task-082 boundary tests: `6 passed`
- isolated candidate `npm pack --json`: one artifact named `openclaw-plugin-cogentnexus-openclaw-0.9.3.tgz`
- isolated artifact was removed before the live installer invocation

## Phase C — exactly one recovery install-over

The only authorized product-changing operation was invoked exactly once:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace C:\Users\CDQ-P\.openclaw\workspace -Provider ollama
```

Complete installer evidence:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx083-preflight-20260826T183022Z\a03-recovery-install-over.txt`

Milestones reached:

1. Existing PASSTHROUGH state was accepted; no pre-install handoff was required.
2. Existing skill was backed up.
3. Candidate skill was copied and validated.
4. Ticket DB bootstrap passed with zero existing Tickets/outbox.
5. Candidate artifact was packed and resolved by the repaired npm-pack boundary.
6. Exact artifact was installed through `openclaw plugins install`.
7. Plugin was disabled as required while the Host remained PASSTHROUGH.
8. Ownership-safe plugin rollover planning failed closed.

Failure:

```text
RuntimeError: replacement payload conflicts with the manifest-owned same-version payload
ownership-safe plugin generation rollover plan was rejected
```

Installer exit status: `1`.

The installer was not retried.

## Post-failure state

Evidence:

- `a04-post-failure.txt`
- `a04-residue-list.json`

The supported operation left a second same-version plugin generation in the OpenClaw npm project area. The ownership resolver correctly failed closed because it found two v0.9.3 generations with different fingerprints:

- prior generation: `g-5593cbcfff5b35d5`
- newly installed generation: `g-7257c4555ca8ad21`

The current plugin inventory showed the newly installed generation as registered but disabled. The previous generation remained in the ownership/backup boundary. Because the installer failed before rollover and ownership publication, the live state is not accepted as canonical parity.

Other post-failure observations:

- Gateway remained Ready and dashboard HTTP remained `200`.
- Ollama remained `0.32.15` with the same four models.
- SQLite remained `integrity=ok`.
- Tickets remained `0`.
- Outbox remained `0`.
- Controller remained `passthrough`, generation `13`.
- AGENTS markers remained `0/0`.
- Supervisor Scheduled Task remained absent.
- No manual repair, cleanup, uninstall, reset, enable, or second installer invocation was performed.

The live partial state now includes the installer-created ambiguous plugin-generation condition and must be handled only by a separately authorized recovery/repair task. Task 083 stops here as required after a nonzero install-over result.

## Phases D–H disposition

The following gates cannot be accepted after the supported installer failure:

- canonical plugin rollover and source/live package parity;
- ownership publication against one canonical generation;
- MANAGED controller restoration;
- startup policy and Supervisor Scheduled Task restoration;
- AGENTS managed policy restoration;
- five natural PT1M Supervisor ticks and `NO_FLASH_MULTI_TICK_PROVEN`;
- authenticated Dashboard/WebChat owner-surface readiness.

No final semantic task is authorized by this result.

## Semantic/provider accounting

Task 083 performed:

- semantic/user messages: `0`
- Dashboard/WebChat sends: `0`
- CLI semantic runs: `0`
- direct Ollama/provider probes: `0`
- model/provider/timeout changes: `0`
- synthetic Ticket or SQLite mutations: `0`
- installer invocations: `1`
- manual repair/cleanup operations: `0`
- installer retries: `0`

The installer’s normal package/bootstrap actions created no Ticket or outbox rows.

## Publication fence

Task 083 produced no source/test commit. Only this coordination report is published.

Final disposition:

`BLOCKED_SUPPORTED_RECOVERY_INSTALL_OVER`

A successor repair/recovery task must address the ownership-safe same-version plugin-generation conflict and explicitly authorize the supported restoration path. It must not infer MANAGED health, no-flash acceptance, or Dashboard owner readiness from this failed attempt.
