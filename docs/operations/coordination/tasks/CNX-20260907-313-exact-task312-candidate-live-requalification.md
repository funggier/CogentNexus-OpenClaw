# CNX-20260907-313 — Exact Task312 candidate live requalification

Status: `READY_FOR_HERMES`
Parent: `CNX-20260907-312`
Executor: `Hermes`
Candidate SHA: `1ae54317bd753b2d54f423979d8a968a8c3053da`

## Goal

Install the exact Task312 candidate through the supported installer, verify installed/source identity, health, scheduler state, and unchanged protected durable state, then run a bounded live process observation proving whether the PT1M heavy wake and user-visible spinner are closed.

## Required method

1. Re-anchor remote `ACTIVE.md`, `STATUS.md`, this task, and Task312 report.
2. Materialize a detached candidate checkout at the exact candidate SHA; preserve it as immutable evidence.
3. Capture preinstall health, scheduler, ownership/fingerprint, and normalized durable/protected-state evidence.
4. Invoke the supported installer exactly once from the detached exact candidate, with no invented source flag.
5. Capture postinstall identity/health/task/durable evidence and verify exact protected-state preservation.
6. Observe at least three PT1M cycles with a bounded read-only process/task observer. Preserve the first observer failure if any; do not infer spinner closure from installer exit `0` alone.
7. Publish the live report with exact evidence paths, hashes, process topology, and user-visible disposition.

## Hard fence

Installer is authorized exactly once. Controlled Scheduled Task disable/restore is authorized only if needed for bounded observation and must be fully read back and restored healthy. No manual live-file patch, SQLite/Ticket/session/transcript mutation, semantic send, replay, redelivery, disposition, protected Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`, protected owner session `agent:main:discord:channel:1531199905673252946`, force-push, tag movement, version change, or release dispatch. Do not retry the installer after it starts.
