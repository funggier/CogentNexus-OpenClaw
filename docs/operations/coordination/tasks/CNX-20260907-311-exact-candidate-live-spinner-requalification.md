# CNX-20260907-311 — Exact candidate live spinner requalification

Status: `READY_FOR_HERMES`
Parent: `CNX-20260907-310`
Executor: `Hermes`
Exact candidate: `79ddec2190b226b2f5cc906144a04859b3eca748`

## Authority

The operator authorized continuous execution through release. Task310 passed independent review and exact-SHA CI. This task authorizes one supported install-over from a detached exact-candidate worktree and bounded live requalification.

## Required sequence

1. Re-anchor remote HEAD, ACTIVE/STATUS and exact candidate.
2. Capture pre-install task state, health, installed source hashes and durable normalized evidence without exposing protected content.
3. Create a detached exact-candidate worktree; verify HEAD and clean state.
4. Invoke the supported installer exactly once. No retry after product failure.
5. Verify installed version/source byte parity, plugin fingerprint, MANAGED health, Gateway/Ollama, Scheduled Task enabled/ready and quiescence release.
6. Observe at least two PT1M cycles and capture supervisor process chains. PASS requires the removed Host delegate layer not to recur; report any residual cursor-visible process boundaries honestly.
7. Re-capture durable normalized evidence and protected predicates; no protected mutation is permitted.
8. Publish evidence/report and either open release-preparation successor or stop fail-closed.

## Hard fence

No manual installed-file edit; no uninstall/reset; no repeated installer; no manual SQLite/Ticket/session/transcript mutation; no semantic send/replay/redelivery; no protected Ticket/session action; no tag/version/release dispatch in Task311.
