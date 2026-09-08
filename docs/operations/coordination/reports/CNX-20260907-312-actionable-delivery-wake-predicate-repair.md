# CNX-20260907-312 — Actionable delivery wake predicate repair

Disposition: `PASS_SOURCE_REPAIR_EXACT_SHA_CI_GREEN`
Observed UTC: 2026-09-07T23:25Z–2026-09-07T23:32Z

## Authority and source

- Remote branch: `agent/v0.9.3-full-stabilization`
- Candidate SHA: `1ae54317bd753b2d54f423979d8a968a8c3053da`
- Candidate was pushed and remote-verified before CI inspection.
- Source repair is limited to `skills/cogentnexus-openclaw/scripts/host_v091.py`.
- RED contract was committed separately at `e189108d7250470deb9fafb6d58379744c8a0ad6`.

## Root cause

The live Task311 observation found `durableWorkHint=true` from one stale pending assistant-delivery row. The row was not actionable under the existing delivery authority: its owner/session freshness was far beyond the 15-minute fence. The prior predicate treated every modern `cnx_assistant_delivery.status='pending'` row as an unconditional heavy-path wake.

## TDD evidence

RED tests added for modern delivery rows:

- fresh exact-generation active owner wakes;
- stale delivery does not wake;
- inactive/deleted owner does not wake;
- generation mismatch does not wake;
- missing owner session does not wake.

The pre-fix run failed exactly on the four non-actionable cases while the fresh case passed. After the minimal fix, the focused actionability suite passed `17 tests`.

The fix performs a read-only, parameterized join over pending deliveries, non-terminal Tickets, and exact active owner sessions, requiring both session and delivery timestamps within the existing 15-minute freshness boundary. Legacy schemas without authority columns retain the conservative pending-row fallback. Workflow tickets, `ticket_outbox`, context-maintenance, direct-recovery, model-call fences, and error-to-heavy-path behavior were not changed.

## Verification

- Correct focused host suites: `56 tests`, `OK`.
- Full Python unittest discover: `264 tests`, exit `0`.
- `py_compile`: pass.
- `git diff --check`: pass.
- Static secret scan: clean.
- Independent exact-diff review: passed, with empty `security_concerns` and `logic_errors`.
- Reviewed production patch SHA-256:
  `873cc6e438cfdd8bf770c226115aff4a9f252b4c0fe2691f9e703d2c75c31fdc`

Required exact-SHA GitHub Actions, all bound to `1ae54317bd753b2d54f423979d8a968a8c3053da`, were terminal success:

| Workflow | Run ID | Conclusion |
|---|---:|---|
| Validate | `34170002421` | success |
| Windows Installer Pack Smoke | `34170002363` | success |
| PS5.1 Acceptance Smoke | `34170002365` | success |

## Observer/tooling notes

A first local CI observer contained a syntax error and was discarded as harness evidence. A corrected bounded observer later timed out at the tool wall-clock; that timeout was not used as a CI result. Direct GitHub query then confirmed all three runs terminal-success.

## Safety boundary

No installer, enable, scheduler, Gateway/Ollama lifecycle, SQLite/Ticket/session/transcript mutation, semantic send, replay, redelivery, disposition, protected Ticket, or protected owner session was touched under Task312. Live installation and spinner requalification require the separate successor authority below.

Successor: `CNX-20260907-313 — Exact Task312 candidate live requalification`.
