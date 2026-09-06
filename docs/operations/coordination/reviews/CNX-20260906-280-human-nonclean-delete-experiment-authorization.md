# CNX-20260906-280 — Human Non-Clean Delete Experiment Authorization

## Human observation and direction

The human confirmed that the normal assistant reply was successfully visible in Discord for the new sacrificial channel, while the later CogentNexus terminal-status announcement appeared only in Web Chat and not in Discord.

The human then explicitly requested to try deleting the current non-clean sacrificial session to observe what actually happens.

## Target

Only this disposable session is authorized for the experiment:

- session key: `agent:main:discord:channel:1391855033993138217`
- session ID observed by Task280: `5438cad2-52b1-4fcf-9145-2d3c65f6ddf2`
- setup Ticket: `CNXT-e25a0459-6f72-41ab-961f-661432cf6d0a`

The protected old owner session `agent:main:discord:channel:1531199905673252946` remains excluded.

## Authorization

Hermes may perform one bounded experiment:

1. fresh read-only snapshot of the exact target session/Ticket/recovery/delivery/outbox state, including any state transition that happened after the Task280 report;
2. verify the current OpenClaw session identity still matches the target above and is not the protected owner;
3. perform exactly one supported OpenClaw session Delete/reset on this target even though the session is not clean;
4. allow only lifecycle-owned consequences of that Delete, including tombstone/revocation/generation changes and cancellation/revocation of nonterminal work belonging to this exact target if the product contract causes them;
5. perform read-only post-Delete observation and publish exactly what changed.

## Experimental meaning

This Delete is intentionally **not** counted as the original clean-session Task272 acceptance proof. It is a diagnostic lifecycle experiment on a non-clean disposable session.

The experiment must preserve the distinction observed by the human:

- the normal assistant answer reached Discord;
- durable delivery confirmation did not record that success;
- a later terminal-status announcement appeared in Web Chat only.

## Still forbidden

- Hermes-generated semantic Discord/Dashboard sends;
- manual Ticket/session/SQLite mutation;
- manual Ticket cancellation/disposition outside lifecycle-owned Delete effects;
- recovery replay/redelivery/disposition;
- mutation of the protected old Ticket/session;
- mutation of prior sacrificial session `agent:main:discord:channel:1366635842554036314`;
- uninstall/reset/broad cleanup;
- installer/install-over;
- Scheduled Task mutation outside supported lifecycle behavior;
- release/tag/default-branch promotion during this experiment;
- force push/history rewrite.

## Stop boundary

After one Delete and post-Delete read-only observation, stop for ChatGPT review. Do not send a recreation test message until the resulting state has been reviewed.
