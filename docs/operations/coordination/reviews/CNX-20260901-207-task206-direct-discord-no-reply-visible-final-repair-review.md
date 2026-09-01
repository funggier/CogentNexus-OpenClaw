# Review — CNX-20260901-207 Direct Discord NO_REPLY Visible-Final Repair

Date: 2026-09-01 ICT
Reviewer: ChatGPT
Disposition: `PASS_REPOSITORY__WINDOWS_REQUALIFICATION_REQUIRED`

## Independent review

Task 207 is accepted as a repository-side repair candidate at:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Public `v0.9.3` remains immutable at `26ce64a624255278a3a0266ad38746e0e6ed2e31`.

### Root-cause fit

Task 206 bound the Task-205 failure to a direct Discord run whose natural assistant final was exact bare `NO_REPLY`, with no messaging-tool send, no queued native reply payload and no native Discord message ID. The existing Task-191 finalization repair was Dashboard-only. Extending that bounded visible-final invariant to exact direct Discord owner Tickets is therefore the correct first repair layer. Delivery-correlation code must remain separate until a visible payload exists and live evidence proves settlement still fails.

### TDD lineage

RED commit:

`7b53a0eadfd640c92f77e48d2d02a162362dcf86`

The commit adds only:

`plugins/cogentnexus-openclaw/src/v207-direct-discord-no-reply.test.ts`

The focused pre-fix result recorded by the executor was `4 tests; 1 failed, 3 passed`, with the intended positive Discord assertion failing because the Dashboard-only implementation returned no revision. Commit/source inspection independently confirms this is the deterministic pre-fix behavior.

Implementation commit:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

The RED commit is the direct merge-base/parent lineage: compare `7b53a0e... -> 27fe018...` is one commit and changes only:

`plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts`

Production diff: `+25 / -4`.

### Production scope

The repair:

- requires canonical numeric Discord channel session shape `agent:<agent>:discord:channel:<id>`;
- requires exact `run_id` and exact `owner_session_key` equality;
- requires an accepted direct Ticket with `workflow_eligible=0` and `workflow_id IS NULL`;
- revises only exact bare `NO_REPLY`/`no_reply` after trim;
- uses deterministic `cnxclaw-discord-visible-final:<runId>` idempotency and `maxAttempts: 1`;
- leaves the model responsible for the user-visible answer;
- preserves the Dashboard idempotency key and Task-191 behavior;
- does not change Dashboard staging/markers/native settlement, `reply_dispatch`, `message_sent`, direct recovery, lifecycle, provider, schema, installer, or release workflow.

Negative regression coverage includes visible text, mixed sentinel text, non-ticketed run and session mismatch. Source-level fences additionally exclude nonnumeric/noncanonical Discord sessions and workflow Tickets.

### GREEN authority

Exact implementation SHA `27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`:

- Validate `33483589170`: `completed/success`, seven jobs, no failed job;
- Windows Installer Pack Smoke `33483589124`: `completed/success`;
- PS5.1 Acceptance Smoke `33483589138`: `completed/success`;
- retained package-proof artifact `9790881384`, digest `sha256:1733897690890f9adcb12176b79db2b43e27799a4022743c4597fad44d2d5a34`, bound to exact implementation SHA.

Package proof recorded:

- payload-v2 `d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b`;
- file count `192`;
- tar.gz SHA-256 `0ab3884621a518b4cfd46949e3c8e3e7f9f52995bee257743960dd7636794dcf`;
- zip SHA-256 `0321028fc6214e18dbc965ad79a6d04328a05a84dce6a9efc058fb1122237986`.

## Evidence-process note

The Task-207 design requested a remote CI RED run for the test-only commit. GitHub currently reports zero Actions runs for exact RED SHA `7b53a0e...`; RED evidence is local focused execution plus independently verifiable commit ordering and deterministic pre-fix source semantics. This is a process/evidence deviation, not a product-code failure, and does not invalidate the exact-head GREEN candidate. No retroactive candidate mutation is warranted solely to manufacture a remote RED run.

## Remaining acceptance boundary

Repository correctness is not final live acceptance. A separate bounded Windows task must:

1. prove there is no pre-existing pending/running Task-205 recovery capable of producing delayed Discord output;
2. install-over exact candidate `27fe018...` from its validated package proof without reset/uninstall/fresh reinstall;
3. prove installed provenance and managed health;
4. prove exact numeric Discord channel `1531199905673252946`;
5. consume exactly one fresh human Send;
6. prove one Ticket and one run, allowing at most one same-run finalization revision if the first natural final is bare `NO_REPLY`;
7. prove one visible native Discord reply;
8. then independently prove `delivery_confirmed -> completed`.

If a visible reply is produced but durable settlement still fails, stop and reopen the separate reply-dispatch/message-sent correlation defect. Do not fold that repair into Task 207.
