# CNX-20260907-291 — Luna Post-Delete Lifecycle Analysis

## Disposition

`PASS_POST_DELETE_LIFECYCLE_CONSISTENT__TASK292_SUNA_READ_ONLY_RECREATION_PREFLIGHT`

Task291 performed read-only repository and runtime analysis only. The confirmed user deletion is consistent with the source lifecycle contract. No new session, message, Delete, reset, or other live mutation was attempted.

## Authority and provenance

- task: `CNX-20260907-291`
- executor: `Luna`
- next executor: `Suna` under proposed Task292
- reviewer: `ChatGPT`
- branch: `agent/v0.9.3-full-stabilization`
- fresh remote HEAD at re-anchor: `84f28cd9a5877c290f8b7a09bbf6777461eeae0a`
- live read-only observation: `2026-09-07` local session

## Fresh durable/runtime evidence

Read-only SQLite opened with `mode=ro` against:

`C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\runtime\cogentnexus-openclaw.sqlite3`

- `PRAGMA integrity_check`: `ok`
- target key `agent:main:discord:channel:1391855033993138217`: `state=deleted`, `generation=1`, `session_id=c7a72073-64e4-4c2b-ba83-58f030e6eef0`
- target `deleted_at=2026-09-07T00:54:15.815Z`
- target `delete_reason=OpenClaw owner session deleted`
- setup Ticket `CNXT-e25a0459-6f72-41ab-961f-661432cf6d0a`: `completed`
- setup Ticket delivery: `1` row, `1` delivered; outbox: `0`
- setup Ticket recovery: `mode=redeliver`, `state=cancelled`, `attempt_count=1`, `owner_generation=0`
- protected key `agent:main:discord:channel:1531199905673252946`: `state=active`, `generation=1`, no session ID, no deletion timestamp
- protected Ticket `CNXT-dc11c9a0-8a89-4df5-9c48-345260725be4`: `accepted`; delivery `0`; outbox `0`
- protected recovery: `mode=redeliver`, `state=pending`, `attempt_count=0`, `owner_generation=1`
- Gateway health remained separately healthy in Task290: HTTP 200 / `{"ok":true,"status":"live"}`; no health mutation was performed here

Task290's fresh OpenClaw inventory is also accepted as current evidence: `count=8`, `totalCount=8`, `hasMore=false`, with neither the target key nor the pre-delete session ID and no replacement target entry.

## Source-contract analysis

The exact accepted source (`plugins/cogentnexus-openclaw/src/v090.ts`) implements the required lifecycle barrier:

1. `session_end` with `reason === "deleted"` calls `deleteSessionByKey`, cancels timers and session-tagged workflows, suppresses completion paths, cancels tracked synthetic work, then calls `finalizeSessionDeletion` with reason `OpenClaw owner session deleted`.
2. Deletion is a tombstone, not an ownership transfer. The source tests require deleted-session work to be cancelled while another session remains unaffected.
3. A deleted row with the same session ID is rejected (`accepted=false`, `lifecycleMatches=false`). A genuinely new session ID may reactivate the same key at `generation + 1`; the old ID and any later mismatched ID remain stale and are rejected.
4. The source tests require the old Ticket to remain cancelled and permit a fresh Ticket only after the new lifecycle is established. This is a future recreation gate, not permission to recreate during Task291.

The live state matches these invariants: the old owner is tombstoned at generation 1, its completed/delivered Ticket is not reopened, its recovery is cancelled, and the protected owner remains independent.

## Safe next lifecycle step

A new message/session is **not** admitted by this task. A future clean recreation may be proposed only through the normal OpenClaw lifecycle with a fresh session ID, while retaining these stale fences:

- reject the deleted session ID `c7a72073-64e4-4c2b-ba83-58f030e6eef0`;
- reject generation-1 late work/delivery from the deleted lifecycle;
- do not reopen or redeliver the completed setup Ticket;
- do not touch the protected Ticket/session or its pending recovery;
- do not use `sessions.delete`, reset, cancel-as-delete, manual SQLite edits, replay, or semantic send as a recreation shortcut.

## Proposed bounded successor

Propose `CNX-20260907-292` to Suna for a fresh **read-only recreation preflight** only. It should re-read OpenClaw inventory, target tombstone/generation, protected state, Ticket/delivery/outbox/recovery state, and Gateway health, then determine whether a separately authorized clean recreation task can be drafted. It must not create a session, send a message, reopen a Ticket, or mutate any durable state.

## Hard-fence ledger

- `sessions.delete`: `0`
- session creation: `0`
- semantic sends: `0`
- reset/cancel substitute: `0`
- Ticket/session/SQLite/transcript mutation: `0`
- replay/redelivery/disposition: `0`
- credential action: `0`
- protected/prior session mutation: `0`
- installer/release/force push: `0`

Actor completed: `Luna`  
Actor next: `Suna` under Task292 read-only preflight  
ChatGPT review required after Task292: `YES`
