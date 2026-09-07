# CNX-20260907-314 — Supported next-version release provenance

Status: `READY_FOR_HERMES`
Parent: `CNX-20260907-313`
Executor: `Hermes`
Candidate baseline: `1ae54317bd753b2d54f423979d8a968a8c3053da`

## Goal

Resolve release provenance without moving existing tag `v0.9.3` or attempting a duplicate GitHub Release. Establish the next supported semantic version/tag from repository authority, update all required version metadata and release notes through source control only, then require fresh review and exact-SHA CI before dispatching `.github/workflows/release.yml`.

## Required method

1. Re-anchor GitHub `ACTIVE.md`, `STATUS.md`, Task313 report, current branch HEAD, `VERSION`, package/manifest/lock versions, existing tags, releases, and `release.yml`.
2. Select a unique next version consistent with repository release policy; do not infer or silently choose a version if policy is absent.
3. Write RED metadata-consistency tests before version changes where needed.
4. Update only source-controlled version metadata/release notes required for the supported next release; do not move `v0.9.3`.
5. Run independent review, full validation, plugin/evaluation/audit, and exact-SHA required workflows.
6. Dispatch `release.yml` with the exact unique version and exact candidate SHA only after all gates pass.
7. Verify the created tag/release target, artifact assets, SHA256SUMS, and workflow result from GitHub.

## Hard fence

No force-push, no existing tag movement/deletion, no duplicate `v0.9.3` publication, no live installer/enable/task mutation, no protected Ticket/session or durable mutation, and no release dispatch until unique-version provenance and exact metadata consistency are proven.
