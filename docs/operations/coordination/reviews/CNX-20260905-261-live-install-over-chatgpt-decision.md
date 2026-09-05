# CNX-20260905-261 — ChatGPT Live Install-Over Decision

## Decision

`AUTHORIZE_TASK262_ONE_SHOT_LIVE_INSTALL_OVER_REQUALIFICATION`

The Task261 repair and Musethree independent review are accepted as sufficient to cross the deployment authority boundary for one bounded live install-over requalification.

This decision is based on the human operator's explicit instruction to inspect and continue the current work, combined with the accepted Task259–261 evidence. It authorizes only the deployment/requalification action defined in Task262. It does not infer current owner intent for the stale Discord response and does not authorize recovery disposition, replay, redelivery, resend, or semantic acceptance.

## Verified evidence

- Current escalation HEAD: `442ed7321e25408fa972f4b527ce8fad5afbf006`.
- Task261 reviewed publication: `d7cf125393994444178644732d50ffbfb3cb8e03`.
- Exact source candidate: `a87c3930651eecf4563d5d8bafe897e058bbdfe0`.
- Task261 review verdict: `ACCEPT_REPAIR__CI_GREEN_VERIFIED__LIVE_SUCCESSOR_ESCALATION`.
- Publication CI: 9/9 check-runs terminal success; workflow runs `33960828088`, `33960828097`, and `33960828083` terminal success.
- Repair lineage is TDD-shaped and linear: `5a40a21` RED -> `0a03686` minimal production fix -> `a87c393` fixture correction -> `d7cf125` report.
- `scripts/install.ps1` candidate blob: `383f1bd05197381ffd6b4f3fa054ee11ab365c1a`.
- `skills/cogentnexus-openclaw/scripts/host_v091.py` candidate blob: `77d3ad291ce6b2e9109066a0367d5115810c3965`.
- The production fix binds installed plugin fingerprint to the exact candidate before managed activation and forces `activate_current_config()` after lifecycle start so a healthy predecessor Gateway cannot satisfy successful install-over without a fresh process boundary.
- The stale subject recovery row remains semantically unresolved, but under the accepted 15-minute freshness fence it is non-due/non-waking when its owner session remains stale. Deployment alone is not authority to emit or dispose it.

## Why YES rather than HOLD

The prior blocker was specifically that install-over could leave a healthy predecessor Gateway process alive after candidate replacement. Task261 closes that gap on the successful path and binds installed payload identity before activation. The repair is independently reviewed and CI-green. The remaining uncertainty is the exact live-machine transition itself, which is precisely what a bounded one-shot live requalification is intended to establish.

The action remains fail-closed: no automatic second installer attempt, no semantic action, no recovery mutation, and no continuation past postflight drift.

## Authority boundary

Task262 may authorize:

- exactly one supported live install-over attempt from the exact candidate;
- installer-owned Gateway lifecycle/process-boundary transitions required by that attempt;
- read-only and post-install verification of runtime identity, ownership, fingerprint, health, process freshness, SQLite integrity, and recovery non-emission;
- one privileged runner/Scheduled Task registration/start only if required by the established Windows execution pattern.

Task262 does not authorize:

- recovery `dispose`/cancel/clear/claim/replay/redeliver/resend;
- manual SQL mutation;
- Dashboard/Discord/API semantic Send;
- unrelated source repair during the live task;
- release/tag/default-branch mutation;
- automatic live retry after installer failure or ambiguous result;
- force push/history rewrite.

## Next actor

Luna executes Task262. Musethree receives the baton after the Task262 report and independently reviews the live evidence before any further successor is selected.
