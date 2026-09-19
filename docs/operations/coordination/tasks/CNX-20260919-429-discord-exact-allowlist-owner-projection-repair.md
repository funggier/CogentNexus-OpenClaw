# CNX-20260919-429 — Discord Exact-Allowlist Owner Projection Repair

Status: `IN_PROGRESS`

Parent: `CNX-20260919-427`

## Trigger

The genuine Discord final-acceptance turn on OpenClaw `2026.9.5` reached the authoritative `before_agent_run` hook, but CogentNexus-OpenClaw skipped Ticket-first admission because OpenClaw projected:

- `senderIsOwner=false`

for an ingress whose exact Discord sender ID was already present in the configured Discord `allowFrom` list.

Authoritative live run:

- session key: `agent:main:discord:channel:1391855033993138217`
- physical session: `8fc2e9fe-e413-4979-b7ce-e2baeb960418`
- run: `333a96e8-728a-44d9-8f58-7a1e4728fe75`
- admission trace: `900db118-e890-4d2b-af3c-6386765dfad4`

Observed:

- `reply_dispatch` correctly deferred before authoritative run identity existed;
- `before_agent_run` executed with the authoritative run ID;
- `senderIsOwner=false`;
- admission outcome became `ineligible`;
- no CNX Ticket was created;
- inference bridge then warned that no accepted Ticket existed.

## Authoritative identity evidence

The persisted transcript for the same human turn contained:

- senderId: `407472087322722318`
- senderName: `GN`
- senderUsername: `funggier`
- senderIdentity.type: `observation`
- senderIdentity.pluginId: `discord`
- senderIdentity.accountId: `default`
- transport.channel: `discord`
- senderIsOwner: `false`

OpenClaw configuration for the same Discord account contains exact:

`channels.discord.allowFrom = ["407472087322722318"]`

Therefore the ingress authorization and exact actor identity were both available, but the owner boolean projected to `before_agent_run` was not.

## OpenClaw 9.5 hook contract

The OpenClaw 2026.9.5 `before_agent_run` event supplies:

- `channelId`
- `accountId`
- `senderId`
- `senderIsOwner`

CNX can therefore recover the narrow missing owner authority without trusting arbitrary Discord participants.

## Required semantics

1. Existing `senderIsOwner=true` behavior remains authoritative.
2. Existing dashboard owner fallback remains unchanged.
3. When `senderIsOwner=false`, CNX MAY recover owner authority only when:
   - the session namespace is Discord;
   - the hook supplies an exact sender ID;
   - that sender ID exactly matches a string entry in the configured Discord account/top-level `allowFrom`.
4. `allowFrom=["*"]` MUST NOT confer owner authority.
5. A different Discord sender MUST remain ineligible.
6. A matching sender ID in a non-Discord session namespace MUST remain ineligible.
7. Group/guild channel access policy MUST NOT be treated as owner authority.
8. No global "all Discord users are owners" fallback is allowed.

## TDD evidence

Initial RED suite:

`src/cnx429-discord-owner-allowlist-fallback.test.ts`

Result before production repair:

- 1 failed;
- 3 passed.

The sole failing positive case proved that an exact configured owner sender remained ineligible.

The three negative cases already passed:

- different sender remains ineligible;
- wildcard `*` does not grant owner authority;
- non-Discord session namespace does not grant owner authority.

## Minimal production repair

Candidate commit:

`89a68b778e0df3fe2ec07f04775152ac0fe5a40b`

Changed:

- `plugins/cogentnexus-openclaw/src/index.ts`
- `plugins/cogentnexus-openclaw/src/cnx429-discord-owner-allowlist-fallback.test.ts`

Added helper:

`discordExactAllowFromOwnerFallback()`

The helper performs only exact string matching against the applicable Discord `allowFrom` list and rejects wildcard promotion.

## GREEN evidence

Focused CNX-429/CNX-427/CNX-423:

`17/17 PASS`

Additional targeted regression:

`64/64 PASS`

Included:

- `index.test.ts`
- CNX-422 reply_dispatch admission
- Discord delivery
- Discord inference attempt
- session generation wiring

`npm run build` — PASS

`npm run plugin:validate` — PASS

Plugin validation evidence:

- TypeScript build PASS;
- mixed-plugin verification PASS;
- 46 config properties;
- 5 tools;
- Ticket DB bootstrap PASS;
- package verification PASS;
- packed file count: 270.

## Live qualification

Pending exact-candidate install-over and one new genuine operator-originated Discord acceptance turn.

The failed pre-repair acceptance turn MUST NOT be replayed or counted as repaired evidence.

## Final classification

PASS target:

`DISCORD_EXACT_ALLOWLIST_OWNER_PROJECTION_GREEN`

Parent CNX-427 can close only after the subsequent genuine Discord turn also proves one authoritative run, one Ticket before inference, one model execution, one visible Discord delivery, terminal Ticket state, and no duplicate/stale lane.
