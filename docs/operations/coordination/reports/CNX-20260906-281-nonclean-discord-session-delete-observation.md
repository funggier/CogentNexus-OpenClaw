# CNX-20260906-281 — Non-Clean Discord Session Delete Observation

## Disposition

`BLOCKED_DELETE_NOT_PERFORMED_BY_SUPPORTED_BOUNDARY__NO_RETRY__WAITING_FOR_CHATGPT_REVIEW`

Task281 authorized one bounded Delete experiment on the exact disposable session after its setup Ticket became durably clean. Phase A passed. Hermes invoked the only available supported lifecycle command exactly once. The command exited `0` but returned `cancelled: []` and produced no session deletion/revocation/tombstone effect. Hermes did not retry or substitute another command.

## Exact target and pre-Delete proof

- session key: `agent:main:discord:channel:1391855033993138217`
- expected OpenClaw session ID: `5438cad2-52b1-4fcf-9145-2d3c65f6ddf2`
- setup Ticket: `CNXT-e25a0459-6f72-41ab-961f-661432cf6d0a`
- CNX generation: `0`
- session state: `active`

The target was distinct from the protected old owner and the prior non-clean sacrificial session.

Setup Ticket had become durably clean before the Delete attempt:

- status: `completed`
- run: `5859d200-2f53-4afc-977f-3bc063800346`
- model call: `ended`, outcome `completed`
- response-ready event present
- `delivery_confirmed_at`: `2026-09-06T13:50:55.341502+00:00`
- `cnx_assistant_delivery`: one delivered `direct_result` row
- owner generation: `0`
- exact idempotency key: `cnxclaw-direct-result:CNXT-e25a0459-6f72-41ab-961f-661432cf6d0a:g0`
- target direct recovery row: `cancelled`, `last_error=terminal ticket fence`
- pending outbox: `0`

## One supported Delete attempt

The `openclaw sessions` CLI exposes listing/maintenance only and has no Delete command. The supported installed CogentNexus lifecycle interface exposed:

`cnxclaw.cmd session cancel --help`

Hermes invoked exactly once:

`C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd session cancel agent:main:discord:channel:1391855033993138217 --reason "CNX-20260906-281 bounded non-clean Discord session delete observation"`

Transcript:

`C:\Users\CDQ-P\AppData\Local\Temp\cnx-task281-delete-transcript.txt`

Terminal result:

- `DELETE_EXIT_CODE=0`
- output: `{"sessionKey":"agent:main:discord:channel:1391855033993138217","cancelled":[]}`

Because the command returned an empty cancellation set, this is not evidence of Delete success. No alternate Delete/reset command was guessed or invoked.

## Post-attempt readback

Fresh read-only readback showed no lifecycle effect:

- target session still `active`
- session ID still `5438cad2-52b1-4fcf-9145-2d3c65f6ddf2`
- generation still `0`
- `deleted_at=null`
- `delete_reason=null`
- setup Ticket still `completed`
- setup delivery still `delivered`
- setup recovery still `cancelled`
- no tombstone, revocation, session-ID nulling, or generation advance
- ticket counts: `accepted=2`, `cancelled=2`, `completed=12`
- Gateway health: HTTP `200`, `{"ok":true,"status":"live"}`

The output is consistent with a supported cancel operation that only targets nonterminal Tickets; because the target Ticket was already terminal, it performed no cancellation and did not delete the OpenClaw session. This interpretation is evidence-based from the exact output and post-readback, not an assumption of success.

## Protected-state preservation

Protected old Ticket remained distinct and untouched:

- `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`
- owner key `agent:main:discord:channel:1531199905673252946`
- status `accepted/interrupted`
- `delivery_confirmed_at=null`

The prior non-clean sacrificial session `agent:main:discord:channel:1366635842554036314` was not selected or mutated. No semantic message was sent by Hermes. No recovery/replay/redelivery, manual SQLite mutation, or unrelated service/process mutation occurred.

## Hard-fence ledger

- supported session-cancel/Delete attempt: `1` (returned `cancelled=[]`; no Delete effect proven)
- extra Delete/reset: `0`
- Hermes semantic sends: `0`
- protected old Ticket/session mutation: `0`
- prior sacrificial session mutation: `0`
- manual SQLite/Ticket/session edits: `0`
- recovery replay/redelivery/disposition: `0`
- installer/install-over: `0`
- unrelated process/service mutation: `0`
- release/tag/default-branch promotion: `0`
- force push/history rewrite: `0`

## Stop boundary

Task281 is blocked at the supported lifecycle boundary and handed to ChatGPT review. Do not retry the cancel command, guess a different Delete API, send a post-Delete message, or mutate the target manually. A successor task must explicitly define and authorize the correct supported session deletion operation before Task272 recreation acceptance can continue.
