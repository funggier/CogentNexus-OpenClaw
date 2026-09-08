# CNX-20260907-312 — Actionable delivery wake predicate repair

Status: `READY_FOR_HERMES`
Parent: `CNX-20260907-311`
Executor: `Hermes`
Baseline branch HEAD: `4b5c6bf1cc0032010048bb8d99016839d5e8cbaf`

## Goal

Stop perpetual PT1M heavy supervisor wake caused by non-actionable stale pending assistant-delivery rows, while preserving every actionable delivery/recovery/workflow wake and all ownership/generation/session fences.

## Required method

1. Re-anchor remote ACTIVE/STATUS/report.
2. Write genuine RED tests proving stale/inactive/wrong-generation/missing-session pending delivery is not a wake and recent exact-generation active delivery remains a wake.
3. Implement the minimum read-only SQL predicate in `host_v091.durable_work_hint` aligned with delivery due authority, including session freshness.
4. Run focused/full Python, plugin, validation/evaluation/audit.
5. Obtain fresh independent review of current diff.
6. Commit/push exact candidate and require Validate, Windows Installer Pack Smoke and PS5.1 Acceptance Smoke success on exact SHA.
7. Publish report and open a new one-shot live requalification successor.

## Hard fence

Source-only. No installer/enable/task mutation; no manual SQLite/Ticket/session/transcript mutation; no send/replay/redelivery/disposition; do not touch protected Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` or owner session `agent:main:discord:channel:1531199905673252946`; no version/tag/release dispatch.
