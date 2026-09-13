# CNX-20260912 — Release Readiness Audit

Date: 2026-09-12
Repository: `funggier/CogentNexus-OpenClaw`

## Verified base

- `main` remains `d3153958416dbf9c08b851c845be82f08dd03a0e`.
- Public release baseline remains v0.9.4.
- No v0.9.5 tag or public release is authorized by this report.

## Verified completed architecture work

Plan 2 identity/delivery safety is closed. The durable `cnx_sessions` generation fence protects inference and delivery across delete/recreate, and ambiguous Web Chat/Discord identity fails closed.

Plan 3 Supervisor single-wake work has been merged into `main`, including canonical wake authority routing and quiescence-oriented tests.

PR #34 added a real ambiguous Discord receipt fixture and proved that staging rejects the ambiguous run without creating a delivery row.

## Current release-preparation state

The repository execution index requires the following sequence before publication:

1. Complete v0.9.5 metadata convergence.
2. Prove v0.9.4 -> v0.9.5 migration safety and full source validation.
3. Freeze one exact candidate SHA.
4. Pass GitHub CI for that exact SHA.
5. Pass Windows install-over acceptance from v0.9.4.
6. Pass live provider-switch acceptance.
7. Pass idle-quiescence acceptance.
8. Perform final candidate review and only then create the release/tag.

## Blocking metadata drift observed on main

The following authoritative surfaces are still v0.9.4 on `main`:

- `VERSION`
- `plugins/cogentnexus-openclaw/package.json`
- `plugins/cogentnexus-openclaw/openclaw.plugin.json`
- `skills/cogentnexus-openclaw/scripts/namespace_ownership.py`
- `plugins/cogentnexus-openclaw/package-lock.json` root package version

Therefore `main` is not a v0.9.5 candidate.

## Safety boundary

Do not compensate for metadata drift by declaring the existing implementation release-ready. Do not create a tag, release, or force-push. Any source, test, documentation, or metadata change after candidate freeze requires a new candidate SHA and restarts exact-candidate acceptance.

## Next implementation boundary

The next safe implementation task is an exact full-file metadata convergence change, including lockfile and namespace ownership, followed by the repository consistency check and plugin validation. The resulting commit must then be treated as the new candidate lineage; no earlier SHA may be reused as a release candidate.
