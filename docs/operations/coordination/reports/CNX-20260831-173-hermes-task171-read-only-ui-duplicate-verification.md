# CNX-20260831-173 — Task-171 Read-Only UI Duplicate Verification

- **Disposition:** `PASS`
- **Executor:** Hermes/Codex
- **Execution mode:** `TASK171_READ_ONLY_UI_DUPLICATE_VERIFICATION_HERMES`
- **Observed:** 2026-08-31 ICT
- **Evidence root:** `C:\Users\CDQ-P\AppData\Local\Temp\cnx172-evidence-20260831T024020Z`

## Objective and authority

Fresh GitHub readback identified Task-173 as the active task at remote HEAD `bfb15e4d22f93479770c6502dac8e9e57a67afec`. The remote `ACTIVE.md` and `STATUS.md` both report `READY_HERMES` and authorize only read-only Dashboard/history observation, screenshots/accessibility extraction, identity correlation, evidence hashing, and publication of this report.

Task-171 remains the only semantic action under review. Its Send count is permanently frozen at exactly `1`. Task-173 performed zero semantic actions.

Frozen Task-171 identity:

- Nonce: `T171-20260831T020446Z-3142A528`
- Expected response: `CNX-171-ACK-T171-20260831T020446Z-3142A528`
- Session: `agent:main:dashboard:13b27c98-c09c-431e-928f-446175ed1937`
- Ticket: `CNXT-b5bf2532-d35d-47db-8951-fcf9f4729abf`
- Run: `8b69bede-030f-4c20-8bb8-0aa99e12422c`
- Product repair SHA: `231761fca24c315e90536955d3e384f55e2e232e`
- Installed fingerprint: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`
- OpenClaw: `2026.7.1-2`

Before writing, this Task-173 report path was confirmed absent from the authoritative remote tree. No source/product/test/workflow drift was introduced by this task.

## Read-only Dashboard observation

The existing Firefox Dashboard session was observed without creating a replacement session, navigating, typing, pasting, submitting, or activating any semantic control.

Session URL/session key matched the frozen Task-171 session:

`http://127.0.0.1:18789/chat?session=agent%3Amain%3Adashboard%3A13b27c98-c09c-431e-928f-446175ed1937`

The fresh screenshot visibly shows the relevant history containing:

1. exactly one user bubble with the Task-171 prompt containing the frozen nonce;
2. exactly one assistant bubble with the expected ACK and one persisted CogentNexus delivery marker;
3. no second user nonce bubble;
4. no second assistant expected-response bubble.

Accessibility evidence provides node-level counts rather than substring counts. In the 206-element tree, the relevant message nodes are:

- one `Edit` node containing the full Task-171 user prompt and nonce, bounds `[3565,407,780,19]`;
- one `Edit` node containing the exact expected assistant response, bounds `[2897,508,310,19]`;
- no additional message node containing the frozen nonce/expected response;
- session identity is present and matches the frozen key.

The nonce and expected response each occur twice as raw substrings in the accessibility labels because the prompt itself repeats the nonce/expected answer in its instruction. The message-node count is therefore the authoritative UI count: one user node and one assistant node.

## UI duplicate result

The Task-171 assistant node contains:

`CNX-171-ACK-T171-20260831T020446Z-3142A528`

and one marker:

`cogentnexus-openclaw-delivery:d3c50a5cae5a5c4084fb30460cc772cb`

There is no second visible assistant result and no second visible user nonce node in the current rendered session history. The result is consistent with the immutable native transcript, which contains exactly one nonce-bearing user record and one expected-response assistant record.

## Correlation to native/durable authority

Task-172's preserved packet remains authoritative for the durable half of the criterion:

- Native transcript SHA-256: `0da04a930e521ab146f9c3684a776ab974f091b8266fa6d62fe84ca3adb875f6`
- Native trajectory SHA-256: `aaca650d8b72543fd3875bde086de8f4bdc3fa33f75fc83a4f2175497c9f0b02`
- User record count: `1`
- Assistant expected-response record count: `1`
- Full model-call ID: `8b69bede-030f-4c20-8bb8-0aa99e12422c:model:1`
- Delivery row count for the Ticket: `1`
- Delivery status: `delivered`
- Ticket status: `completed`
- `delivery_confirmed_at`: `2026-08-31T02:14:45.082Z`
- Run-scoped recovery rows: `0`
- Run-scoped conflicting outbox rows: `0`

The visible assistant marker identity matches the native marker and is bound to the same Task-171 Ticket/run through the previously verified delivery row and `delivery_confirmed` event.

## Task-171 criterion 8 closure

The previously incomplete conjunctive criterion was:

> no duplicate UI/native result, second inference, recovery reinjection, or conflicting outbox/delivery.

Task-173 closes the UI portion with read-only evidence:

- visible user nonce message nodes: exactly `1`;
- visible expected assistant result nodes: exactly `1`;
- visible duplicate user nonce nodes: `0`;
- visible duplicate assistant result nodes: `0`;
- native user/assistant records: `1/1`;
- native model execution: exactly `1`;
- durable delivery rows: exactly `1`;
- recovery/outbox conflicts: `0/0`.

Therefore the UI/native duplicate criterion is `PASS` when combined with Task-172's native/durable evidence. No inference is made from aggregate text substring counts; message-node identity and bounds are used.

## Evidence and hashes

| Artifact | SHA-256 |
|---|---|
| Task-173 accessibility extraction `c03-task173-ui-accessibility.json` | `5618d9459ae9b413eb6d92697d47aa5080f6df4cb4e528f4c2421f67fb50955f` (source tree extraction) |
| Task-173 screenshot `computer_use_76ca42b35c1b4111b27bd306432e5e01.png` | `cc389ba0f171ba5396c92d387b54718c0423a2809b1ed792d95f344d68b017ee` |
| Task-171 transcript | `0da04a930e521ab146f9c3684a776ab974f091b8266fa6d62fe84ca3adb875f6` |
| Task-171 trajectory | `aaca650d8b72543fd3875bde086de8f4bdc3fa33f75fc83a4f2175497c9f0b02` |
| Task-171 frozen send ledger | `6eaa1a249a8f0fcbb9504c431192369c39e38ffc7461b8e4997fccdf3f304b5e` |
| Task-171 native settlement packet | `6571f30f112880bb18004559a4daa8660cd6f1baa47d63f0a070ecfb7fcc35b5` |
| Task-172 contract packet | `b01-contract-packet.json` in the Task-172 evidence root; packet hash and field-level identities preserved there |

The accessibility source contains 206 elements and the two relevant message nodes listed above. The screenshot is the fresh read-only Firefox capture used for visual confirmation.

## Acceptance matrix

| Criterion | Result | Exact evidence |
|---|---|---|
| One visible user message containing frozen nonce | `PASS` | Task-173 accessibility extraction: one nonce-bearing `Edit` message node; screenshot hash above |
| One visible assistant message containing exact expected result | `PASS` | Task-173 accessibility extraction: one expected-response `Edit` message node; screenshot hash above |
| No duplicate visible assistant result | `PASS` | Accessibility message-node inventory and screenshot show one assistant result only |
| No duplicate visible user nonce | `PASS` | Accessibility message-node inventory shows one user prompt node only |
| UI history is the frozen Task-171 session | `PASS` | URL/session key and session-label evidence match exact frozen session |
| UI result agrees with native transcript | `PASS` | Marker-bearing visible ACK matches Task-171 immutable transcript and marker identity |
| No second semantic action was performed by Task-173 | `PASS` | Task-173 hard-fence ledger: Send/Enter/type/paste/model/recovery actions all `0` |

## Anomalies and limitations

The current UI accessibility inventory exposes both the visible message node and its text `Edit` representation in the broader tree; counts were deduplicated by message-node role/bounds and not by raw substring occurrences. The raw nonce/expected text appears twice per instruction/response because the prompt explicitly repeats the expected answer. This does not indicate duplicate messages.

The earlier Task-171 post-send screenshot was stale and did not prove final visible counts. Task-173's fresh screenshot and accessibility inventory now show the persisted Task-171 user/assistant pair directly. No scroll, navigation, reload, or mutation was required, and history virtualization did not prevent the relevant pair from being visible.

## Hard-fence compliance

Task-173 performed:

- Dashboard Send: `0`
- Enter submission: `0`
- Composer typing/paste: `0`
- `chat.inject`: `0`
- Alternate semantic input: `0`
- Model invocation: `0`
- Recovery/regeneration: `0`
- Installer/lifecycle/restart/reset: `0`
- Manual durable-state mutation: `0`
- Source/product/test/workflow change: `0`

Only read-only Dashboard observation, screenshot/accessibility extraction, hashing, identity correlation, and this report publication were performed.

## Disposition and next gate

The only remaining Task-171 review gap—the visible UI duplicate/count condition—is proven `PASS` by this read-only checkpoint. Combined with Task-172's native/durable evidence, all Task-171 acceptance criteria are now complete.

Recommended next step: ChatGPT may perform the final review and combine Tasks 171–173 into final semantic durable-delivery acceptance. No new Send, inference, recovery, lifecycle operation, or product modification is authorized by Task-173.

## Publication state

This report is the only Task-173 repository artifact authorized for publication. It must be staged and published alone, then verified by remote HEAD, report blob SHA, commit parent, and changed-path scope before claiming completion.
