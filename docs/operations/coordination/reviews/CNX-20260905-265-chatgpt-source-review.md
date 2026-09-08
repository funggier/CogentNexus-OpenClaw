# CNX-20260905-265 — ChatGPT Source Review

## Verdict

`ACCEPT_SOURCE_REPAIR__LIVE_PREFLIGHT_REQUIRED`

## Reviewed evidence

ChatGPT independently reviewed Task265 report, RED commit `f5f0c236921b89f446b1fd424863aa12965bc198`, production candidate `ec1fdbb2ea036c6dcd1c375b8171868335d63fc8`, and exact-candidate GitHub Actions.

The RED regression correctly reproduces the first-turn ordering race by invoking registered `before_agent_run(B)` after deleted lifecycle A and before any `session_start(B)` callback. The production repair changes the model-admission boundary from read-only lifecycle lookup to the same transactional `reactivateSessionForLifecycle()` primitive used by `session_start`, then gates on `accepted`.

This closes the ordering defect identified in the Task264 review:

- deleted A + first owner turn B can establish B and proceed without waiting for asynchronous `session_start(B)`;
- active B + B remains idempotent;
- stale A / unrelated C remain rejected by exact lifecycle identity;
- delayed `session_start(B)` does not increment generation again;
- existing deletion/generation/recovery/delivery fences remain covered by the full suite.

Exact-candidate Actions all completed successfully on `ec1fdbb2ea036c6dcd1c375b8171868335d63fc8`:

- PS5.1 Acceptance Smoke `33977733180` — success
- Windows Installer Pack Smoke `33977733182` — success
- Validate `33977733191` — success

Task265 hard fences were respected; no live runtime or semantic action occurred.

## Residual boundary

Task265 proves source semantics, not the live user-visible flow. Before any Delete -> first Discord message acceptance test, the reviewer requires a read-only live preflight to determine:

1. whether the installed CogentNexus plugin actually matches Task265 candidate semantics/fingerprint;
2. current Gateway/plugin/runtime identity;
3. current Discord owner session identity and whether any nonterminal work would be abandoned by deletion;
4. exact bounded deployment/delete/test actions that would be required.

No live installer, Gateway mutation, session deletion, DB mutation, replay/redelivery, or Discord/Dashboard/API semantic send is authorized by this review.

## Disposition

Task265 source repair is accepted. Open a separate read-only live preflight successor. Any later install-over, Gateway boundary, session delete, or semantic test message requires explicit bounded live authority.
