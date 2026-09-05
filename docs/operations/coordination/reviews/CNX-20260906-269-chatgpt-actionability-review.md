# CNX-20260906-269 — ChatGPT Independent Review

## Verdict

`REWORK_REQUIRED__MINIMUM_DELETING_OWNER_PROOF_MISSING`

Task269's production direction is accepted provisionally, but the task is not contract-complete because one explicitly required regression case is missing.

## Accepted evidence

- RED commit `518e6aaa401b0031bf630566551bffe994d4ed3e` preceded production repair.
- Production commit `454643bf3615f8cec88cc9b64566ae9e243ad2f5` narrowed Host Direct-recovery actionability to accepted Direct lane + active exact generation + 15-minute owner freshness + due time + model-call fence.
- Corrective commit `08a25a66b17ccea73f22fde6ca00ccdd63fe15e4` repaired legacy-schema compatibility after the first exact-SHA Validate failure.
- Final exact-SHA workflows all succeeded on `08a25a66b17ccea73f22fde6ca00ccdd63fe15e4`: Validate `33983861309`, PS5.1 `33983861333`, Windows Installer Pack `33983861332`.
- Healthy runtime with stale Direct state is explicitly tested to stay on the Host idle fast path.
- The stale live Ticket/recovery and all live runtime surfaces remained untouched.

## Blocking review gap

Task269 required at minimum proof that a `deleted/deleting` owner cannot wake Host Direct recovery. The new suite proves `deleted`, but contains no explicit `deleting` case.

The current SQL uses `s.state='active'`, so review expects `deleting` to be rejected. However, this task deliberately treats session lifecycle states as safety boundaries. The stated test contract must therefore prove the transient `deleting` state directly rather than infer it from the predicate.

No production rework is requested unless the missing test exposes an actual defect.

## Residual note

Plugin-side `idleWorkHint()` remains broader than the Host predicate, but it governs in-process event-worker scheduling and is not the external PT1M Host heavy-process wave established as the APPSTARTING cause. It is not a blocker for this Task269 review, but may be considered separately as an efficiency/semantic-unification follow-up.

## Required successor

Open a bounded test-contract closure task:

1. add a regression case for owner session state `deleting` with otherwise fresh/exact/due Direct recovery and prove `durable_work_hint()` returns false;
2. prove healthy supervisor remains idle for that shape without invoking legacy heavy reconciliation;
3. do not change production source unless the new test fails;
4. rerun focused Host tests, full Python validation appropriate to the surface, `git diff --check`, and exact-SHA branch workflows;
5. keep all live/destructive/semantic fences at zero.
