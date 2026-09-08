# CNX-20260906-279 — ChatGPT Managed Re-entry Review

## Verdict

`ACCEPT_TASK279_MANAGED_REENTRY__RETURN_TO_TASK272_CLEAN_SACRIFICIAL_SETUP_REQUIRED`

Task279 is accepted.

Hermes used the smallest supported recovery path: the canonical installed launcher `cnxclaw.cmd enable` was invoked exactly once and returned exit code `0`. The authorized reinstall fallback was not used.

Post-action evidence shows the accepted candidate payload remained exact and ownership-verified, the plugin is `enabled=true` / `status=loaded`, Host mode is `managed`, Gateway and Ollama are healthy/reachable, the managed supervisor is Ready with last result `0`, SQLite integrity is `ok`, and Ticket/recovery/outbox counts did not change semantically.

The protected old Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4` remains untouched. The earlier Task272 sacrificial session `agent:main:discord:channel:1366635842554036314` also remains untouched but is still non-clean because its pre-repair setup Ticket is accepted/interrupted with unconfirmed delivery.

## Task272 continuation decision

Do not dispose, cancel, replay, redeliver, reset, or Delete the old sacrificial setup lineage merely to satisfy the clean-session gate.

Instead, create a fresh disposable Discord topology after the repaired candidate is live. The human should send exactly one benign setup message in a NEW disposable Discord channel/thread/key visible to the bot. That setup message is only for creating a clean sacrificial session; it is not the post-Delete acceptance message.

After the setup turn settles, Hermes must read live state and prove the new session is clean under the repaired durable-delivery boundary. Only then may the already-recorded Task272 Delete authority be consumed exactly once. After Delete, stop at `WAITING_FOR_USER_TEST_MESSAGE` so the human can send exactly one post-Delete first-turn message.

No release action is authorized yet. The human's conditional final-release direction remains parked until Task272 recreation/durable-delivery acceptance and final repository acceptance both pass.
