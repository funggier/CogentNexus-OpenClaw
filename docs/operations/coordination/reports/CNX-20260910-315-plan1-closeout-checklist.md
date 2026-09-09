# CNX-20260910-315 — Plan 1 Closeout Checklist

Plan 1 closes only when all of the following are freshly verified on the resulting commit:

- [ ] Focused CLI ownership tests pass.
- [ ] Full repository validation passes.
- [ ] PS5.1 live runner smoke passes.
- [ ] PS5.1 acceptance smoke passes.
- [ ] Windows installer pack smoke passes.
- [ ] No CNX lifecycle command invokes provider routing transition.
- [ ] No local adapter lifecycle command invokes OpenClaw routing transition.
- [ ] Legacy CNX lifecycle `--provider` input is rejected without transition.
- [ ] Provider list/status remain diagnostic-only.
- [ ] `cloud` remains an explicit OpenClaw authority handoff.

Only after this checklist is green should Plan 2 (`InferenceAttempt → Delivery Core → Session Generation`) begin.
