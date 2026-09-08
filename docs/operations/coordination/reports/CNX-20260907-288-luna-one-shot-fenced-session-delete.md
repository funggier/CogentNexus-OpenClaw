# CNX-20260907-288 — Luna One-Shot Fenced Session Delete

## Disposition

`BLOCKED__CHAT_UI_INPUT_MISROUTED_AND_PLUGIN_REJECTED__NO_DELETE__WAITING_FOR_CHATGPT_REVIEW`

The authorized one-shot `sessions.delete` was **not called**. The task is stopped and requires ChatGPT review before any further action.

## Authority and provenance

- task: `CNX-20260907-288`
- executor: `Luna`
- reviewer/escalation: `ChatGPT`
- branch: `agent/v0.9.3-full-stabilization`
- remote HEAD at fresh re-anchor: `b02c49769bd564bf11fec34105a048815c3c927b`
- inherited immutable handoff: `CNX-20260907-287-suna-preflight-handoff.md`
- observation time: `2026-09-07T06:16:15+07:00`

## What happened

Luna opened the already-authenticated OpenClaw Control UI in the paired Firefox profile. A navigation attempt to `/sessions` was misrouted into the current Chat input rather than the browser address bar. The UI visibly rejected the resulting input and displayed:

> `Your message could not be sent: blocked by cogentnexus-openclaw`

The same rejection was visible in the target chat pane; no assistant response or successful message delivery was observed. This is recorded as a blocked semantic-send attempt, not silently counted as zero interaction.

No `sessions.delete` call was made before or after the rejection. No retry, reset, cancel substitute, credential readout/change, manual durable-state mutation, protected-session mutation, replay/redelivery, installer, release, or force push was performed.

## Live-operation ledger

- `sessions.delete` calls: `0`
- delete attempt consumed: `0`
- semantic-send attempts: `1` (UI input was rejected by `cogentnexus-openclaw`)
- successful semantic sends: `0` observed
- Ticket/session/SQLite/transcript mutation: `0` observed
- protected/prior session mutation: `0`
- reset: `0`
- cancel substitute: `0`
- credential exposure/change: `0`
- replay/redelivery/disposition: `0`
- installer/release/force push: `0`

## Required ChatGPT decision

Stop. Do not retry the UI navigation or attempt the Delete. ChatGPT must review the misrouted-input evidence and issue a fresh, explicit authority/task boundary before any further live operation. The original Task288 one-shot fence remains unused, but the semantic-send hard fence was approached and the plugin rejection must be adjudicated independently.

Actor completed: `Luna`  
Actor next: `ChatGPT review`  
ChatGPT review required: `YES`
