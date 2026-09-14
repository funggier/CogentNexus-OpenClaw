# CNX-340D — Dashboard UI Control Requalification Report

- Task: `CNX-340D`
- Branch: `agent/v0.9.6-ui-control-requalification`
- Authority HEAD at execution start: `f43a54bfd661b1ba0fbd0c6afc377b12bac8f6c9`
- Executor: Hermes
- Reviewer: ChatGPT
- Execution window: `2026-09-14T08:20:30Z` (UTC capture point)
- Result: **BLOCKED**
- Classification: `UI_NEW_SESSION_NOT_VERIFIABLE`, `UI_FRESH_SESSION_STATE_NOT_VERIFIABLE`
- Stop rule: ambiguous activation was consumed; no retry was made.

## Scope and prior evidence inspection

The exact remote branch was cloned at `f43a54bfd661b1ba0fbd0c6afc377b12bac8f6c9` and `ACTIVE.md`, `STATUS.md`, and the CNX-340D task were read before any UI action. `ACTIVE.md` identifies CNX-340D as `READY_FOR_HERMES` and explicitly prohibits replaying CNX-340C.

The branch contains the CNX-340C task specification and references the prior CNX-339 evidence, but no published CNX-340C report or CNX-339B report was present in the checked-out coordination report directory. The visible Dashboard session itself showed the historical CNX-339 lifecycle acceptance conversation; it was not used for semantic input.

## Target process/window identity

Read-only command:

```text
tasklist /v /fo csv | grep -i -E "firefox.exe|node.exe" | grep -E "17040|3172" || true
```

Exit code: `0`

Relevant output:

```text
"firefox.exe","17040","Console","1","241,024 K","Running","CDQ-P\\CDQ-P","1:36:11","OpenClaw Control - Mozilla Firefox"
"node.exe","3172","Console","1","171,708 K","Unknown","CDQ-P\\CDQ-P","0:03:06","N/A"
```

`computer_use list_windows` independently returned:

```text
app_name=firefox.exe
pid=17040
window_id=3736650
title=OpenClaw Control — Mozilla Firefox
off_screen=false
z_index=12
```

The target was therefore bound to Firefox PID `17040`, native window ID `3736650`, title `OpenClaw Control — Mozilla Firefox`. A fresh SOM capture identified the Dashboard document and the supported `New session` button. The capture also reported that bounds were native desktop coordinates, not screenshot coordinates.

## Pre-action session identity and state

Fresh capture immediately before the control action:

- Address URL: `http://127.0.0.1:18789/chat?session=agent%3Amain%3Adashboard%3A77a53ce6-57b3-4fc9-9e70-8356f76e67ef`
- Session key: `agent:main:dashboard:77a53ce6-57b3-4fc9-9e70-8356f76e67ef`
- Visible selected conversation contained prior CNX-339 user and assistant turns.
- Composer was empty (`Message Assistant`).
- Supported control identified: `New session`, native bounds `[2578,254,187,34]`.

Foreground ownership was checked before the state-changing action. `focus_app` returned:

```text
bring_to_front: pid 17040 hwnd 0x39044a is now foreground (was 0x39044a)
landed_on_target=true
now_fg_hwnd=0x39044a
target_hwnd=0x39044a
target_selected=true
```

A recapture after that focus operation still showed the same target window and pre-action session URL.

## Exact control action sequence

1. `computer_use list_windows` to resolve Firefox PID/window identity.
2. `computer_use capture(mode=som, app=firefox.exe, pid=17040, window_id=3736650)`.
3. `computer_use focus_app(app=firefox.exe, pid=17040, window_id=3736650, raise_window=true)`; foreground ownership confirmed.
4. Fresh `capture(mode=som)`; revalidated the URL, old session identity, empty composer, and `New session` control.
5. An element-index-only click was refused by the driver because a snapshot token was required; it did not reach the application and is recorded as a tooling refusal, not an activation.
6. Using the freshly captured native bounds, one background coordinate click was delivered at `[2671,271]`, the center of the `New session` control. The driver returned `effect=unverifiable`.
7. Per the task hard fence, this ambiguous activation was consumed. No second click, Enter, Send, prompt, keyboard fallback, or alternate transport was used.
8. A read-only three-second wait and final fresh capture were performed.

The click result was:

```text
ok=true
action=click
message=Posted click to pid 17040.
effect=unverifiable
route=synthetic_events
verdict=verify_fresh_state
```

## Post-action identity and fresh-session proof

The final capture after the ambiguous click and observation window showed:

- URL unchanged: `http://127.0.0.1:18789/chat?session=agent%3Amain%3Adashboard%3A77a53ce6-57b3-4fc9-9e70-8356f76e67ef`
- Session key unchanged: `agent:main:dashboard:77a53ce6-57b3-4fc9-9e70-8356f76e67ef`
- Sidebar still showed the same session list and `New session` control.
- The visible conversation still contained the prior CNX-339 turns.
- The composer remained empty.

Therefore no independent marker proved a new session. The required fresh-session condition was not met: URL/session identity did not change, and the rendered conversation was not empty. This is classified as `UI_NEW_SESSION_NOT_VERIFIABLE` and `UI_FRESH_SESSION_STATE_NOT_VERIFIABLE`, not as a successful requalification.

## Traffic and mutation fences

- Semantic input: **0**. No prompt, text, Enter, Send, or semantic request was issued.
- Inference: **0 initiated by this task**. No OpenAI/Ollama inference was invoked.
- Provider/model/config/timeout/controller: **not modified**.
- Repository production code/test seam: **not modified**.
- Installation/release/tag: **not modified**.
- Production DB: no semantic action was issued and the UI/session URL/history remained byte-for-byte equivalent in the available captures; a direct production-DB read-back was not performed because the runtime database path was not exposed by the task and no DB mutation path was authorized. Accordingly, DB unchanged is not claimed as independently proven; this remains a limitation of the blocked evidence.

## Repository provenance and diff scope

Pre-publication checkout checks:

```text
git ls-remote ... refs/heads/agent/v0.9.6-ui-control-requalification
f43a54bfd661b1ba0fbd0c6afc377b12bac8f6c9

git status --short
<empty before report>
```

The execution checkout was clean at the authority commit. This report is the only task-result file added. No production code, configuration, controller, provider/model setting, timeout, or test seam was changed.

## Disposition

`BLOCKED — UI_NEW_SESSION_NOT_VERIFIABLE; UI_FRESH_SESSION_STATE_NOT_VERIFIABLE`

CNX-340D did not rerun CNX-340C and did not self-accept. The ambiguous `New session` activation remains consumed. Stop for independent ChatGPT review.
