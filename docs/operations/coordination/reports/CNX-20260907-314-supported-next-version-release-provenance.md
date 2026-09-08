# CNX-20260907-314 — Supported next-version release provenance

Disposition: `BLOCKED_SUPPORTED_VERSION_PROVENANCE`
Observed UTC: 2026-09-07T23:43Z–23:48Z

## Authority checked

- Remote coordination HEAD before this report: `cf42821fdb068dd64d0c0c87f89a54378c95b44a`.
- Current `VERSION`: `0.9.3`.
- Existing tag: `v0.9.3` -> `26ce64a624255278a3a0266ad38746e0e6ed2e31`.
- Existing GitHub Release: `v0.9.3` exists and is published.
- Release workflow requires exact version alignment across `VERSION`, package, manifest, both lockfile versions, release notes, and release archive names, then refuses publication if the target Release already exists.

## Live predecessor result

Task313 passed exact-candidate live requalification for `1ae54317bd753b2d54f423979d8a968a8c3053da`; its report is published separately. No release workflow was dispatched because duplicate publication would be rejected and moving `v0.9.3` is forbidden.

## Why automatic `0.9.4` selection is blocked

The current repository is not merely labeled `0.9.3` in five metadata files. The v0.9.3 identity is embedded in validation and release contracts, namespace ownership/install migration semantics, operator documentation, workflow names/contracts, scripts, and regression fixtures. A blind or partial bump to `0.9.4` would either fail the authoritative validation gates or create an unreviewed semantic version migration. No repository policy file authorizes that migration automatically.

Therefore this task cannot safely select `0.9.4` by inference, and it must not dispatch `release.yml` with `0.9.3`. No version, tag, release, live installation, or durable state was mutated.

## Required successor authority

A successor must explicitly establish one supported path:

1. authorize and implement a complete, reviewed `0.9.4` metadata/contract migration with RED/GREEN, exact-SHA CI, and new release notes; or
2. provide a supported release-publication exception/path for the already-existing `v0.9.3` Release without moving or duplicating its tag/release (the current workflow provides no such path).

Until one path is authoritative, release status is blocked. No credentials or protected identifiers are included in this report.
