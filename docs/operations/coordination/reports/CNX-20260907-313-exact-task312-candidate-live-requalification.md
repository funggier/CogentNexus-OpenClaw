# CNX-20260907-313 — Exact Task312 candidate live requalification

Disposition: `PASS_LIVE_REQUALIFICATION_EXACT_CANDIDATE`
Observed UTC: 2026-09-07T23:35Z–23:42Z
Candidate: `1ae54317bd753b2d54f423979d8a968a8c3053da`

## Installation and identity

- Detached candidate checkout was pinned to the exact candidate SHA and kept immutable.
- Supported `scripts/install.ps1` invocation count: `1`.
- Installer exit: `0`.
- Installed version: `0.9.3`.
- Installed plugin fingerprint:
  `9af4712dd3265afc577a233b4716279901b9eab1128ad6640c63e0ba846f0f33`
- All seven owner files were byte-exact after installation.
- Installer stdout SHA-256:
  `3ecab04a4f689257cdde5bcf71587c183fa10ff6e220d88b437c25f6c36e9687`
- Installer stderr SHA-256:
  `e1560447196cc1dc1886bbbae82b2ef3aa3cf183696717a3f0d624279e22b42c`

## Health and scheduler

Preinstall, postinstall, and post-observation health checks returned HTTP `200` for both Gateway and Ollama. The Scheduled Task remained enabled and returned `Ready` with `LastResult=0` throughout postinstall and observation.

The bounded read-only observer ran for `135` seconds, collected `175` task samples, and covered at least three PT1M cycles:

- relevant new process starts matching CogentNexus/host/runtime/openclaw: `0`;
- process names observed: none;
- task state samples: `Ready=175`;
- observed last results: `{0}`.

This closes the previously observed PT1M redundant/heavy process-chain symptom in the tested window. No foreground cursor instrumentation was available; the technical live disposition is therefore bound to scheduler/process evidence rather than an unrecorded UI claim.

## Durable safety

Preinstall, postinstall, and post-observation normalized durable SHA-256 remained:

`6779f2dcd573526e8aea67bc2499355d2096ab34805906e632cb23835bd42e1f`

SQLite integrity remained `ok`; protected promotion and protected delivery-due predicates remained `false` before and after. No protected Ticket/session, semantic transport, replay, redelivery, disposition, or manual database mutation occurred.

Evidence root:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx-release-20260907T134252Z\task313-evidence`

Key evidence:

- `preinstall-console.json`
- `postinstall-console.json`
- `postobserve-console.json`
- `process-observation-poll.json`
- `task-preinstall.json`
- `task-postinstall.json`
- `task-postobserve.json`
- `installer.stdout`
- `installer.stderr`
- `installer.exit`

## Release boundary

Live acceptance passed, but release publication was not attempted. Fresh GitHub authority reports:

- `VERSION`: `0.9.3`;
- existing tag `v0.9.3` points to `26ce64a624255278a3a0266ad38746e0e6ed2e31`;
- GitHub Release `v0.9.3` already exists;
- `.github/workflows/release.yml` refuses duplicate release publication;
- moving the existing tag is forbidden.

A separate successor must establish a supported new version/tag provenance before release dispatch. No release workflow, tag movement, or version mutation was performed under Task313.

Successor: `CNX-20260907-314 — Supported next-version release provenance`.
