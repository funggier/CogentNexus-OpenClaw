# CNX-20260831-180 — Repaired Candidate Windows Install-Over Provenance & Health

- **Task:** `CNX-20260831-180`
- **Disposition:** `BLOCKED — PREINSTALL_TASK178_OUTER_HARNESS_REMAINS_ALIVE`
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Branch:** `agent/v0.9.3-full-stabilization`
- **Authority HEAD at final pre-publication check:** `a7918285acb962b82ede8e398311a1f6f8171724`
- **Task-179 repair candidate:** `f6392da3e4112ce441526d5ef19925c90a872b0b`
- **Evidence root:** `C:\Users\CDQ-P\AppData\Local\Temp\cnx180-evidence-20260831T061500Z`
- **Installer invocations:** `0`
- **Semantic action count:** `0`
- **Live product mutation:** `0`

## Disposition

Task-180 was blocked before the supported install-over. Fresh authority and source/provenance preflight were performed, but the exact Task-178 outer reset observer remains alive after the Task-178 reset child tree was retired in Task-179. Task-180 explicitly requires no live Task-178/179 reset/uninstall process before mutation, while Task-180 does not authorize another process termination. Therefore the install-over was not started.

No installer command, reset, uninstall, reinstall, lifecycle helper, Gateway/Ollama restart, semantic action, model call, recovery action, or live product repair was performed.

## Authority

Fresh remote fetch/read at final pre-publication check:

```text
REMOTE_HEAD=a7918285acb962b82ede8e398311a1f6f8171724
ACTIVE status: READY_HERMES
ACTIVE task: CNX-20260831-180
execution mode: WINDOWS_REPAIRED_CANDIDATE_INSTALL_OVER_PROVENANCE_HEALTH_HERMES
STATUS state: READY_HERMES
report at authority tip: absent before publication
```

Task-180 remained the authoritative active task. Its accepted candidate was:

```text
f6392da3e4112ce441526d5ef19925c90a872b0b
```

## Preflight provenance

A clean detached worktree was materialized from exact candidate `f6392da...`.

Candidate facade:

```text
skills/cogentnexus-openclaw/scripts/cnxclaw.py
bytes: 17425
sha256: aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f
Git blob recorded by authority: 879083d6186589d4b2774b8fd87fa93692dd2f
```

Candidate release was `0.9.3`.

The active installed launcher was read-only inspected and resolved to:

```text
C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\runtime\python\Scripts\python.exe
C:\Users\CDQ-P\.openclaw\workspace\skills\cogentnexus-openclaw\scripts\cnxclaw_v093.py
```

The currently installed facade was:

```text
C:\Users\CDQ-P\.openclaw\workspace\skills\cogentnexus-openclaw\scripts\cnxclaw.py
sha256: e15e8af49e18925fb569cd405b18fe5c57172d1a0e4644e359703b692cacb032
```

This does **not** equal the candidate facade hash. That mismatch is expected at the pre-install boundary because Task-180's baseline states that the Task-179 facade has not yet been installed. It is a gate to prove after install-over, not evidence of an attempted or failed install.

Previously accepted unchanged package provenance remained:

```text
release: 0.9.3
package SHA-256: 8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91
plugin fingerprint: e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19
OpenClaw: 2026.7.1-2
```

The unchanged package/fingerprint was not used to claim the Python facade repair was installed.

## Live runtime and durable preflight

Read-only probes completed with the following state:

- recovery preflight: `OWNERSHIP_PRESENT`;
- ownership inventory: new launcher/skill/state/application-data/direct-plugin paths present; legacy inventory empty;
- controller: `managed`, generation `36`;
- desired Gateway/provider: `running`;
- selected provider: `ollama`;
- provider transition: `null`;
- Gateway: healthy on loopback `127.0.0.1:18789`;
- Ollama: reachable/healthy/ready;
- delivery: `READY`, pending outbox `0`, `stateChanged=false`;
- recovery: `READY`, no active incident, `stateChanged=false`;
- OpenClaw pin: `2026.7.1-2`;
- SQLite state remained the prior pre-reset state and was not mutated.

Previously retained pre-reset counts were:

```text
tickets                  4
ticket_events           29
ticket_outbox            0
cnx_assistant_delivery   1
cnx_direct_model_call    4
cnx_direct_recovery      0
cnx_sessions             4
```

The Task-171 historical Ticket/delivery state remained present, as required before a future reset. No semantic/model/recovery work was created.

## Complete issue register

### Issue 1 — Initial preflight verifier parser error

The first `preflight180.ps1` invocation did not execute because the process-scan `if/else` pipeline was syntactically invalid in PowerShell:

```text
An empty pipe element is not allowed.
FullyQualifiedErrorId: EmptyPipeElement
```

No installer action occurred before or after this error. The verifier was corrected by assigning the conditional result to `$processReport` before piping to `Set-Content`, then rerun successfully. This is recorded as an executor-side harness correction, not product evidence.

### Issue 2 — Task-178 outer observer remains alive

The corrected preflight process scan found this historical observer chain still alive:

```text
outer bash PID 14196
  -> bash PID 22832
      -> Python PID 17052: run_reset178.py
          -> Python PID 17444: run_reset178.py
```

The exact Task-178 reset command descendants (`cmd.exe 17864`, installed facade child `13628`, nested lifecycle child `5360`) were already retired in Task-179. The outer `run_reset178.py` observer did not exit naturally after that cleanup.

A further read-only 60-second observation window was performed. The same outer observer chain remained alive. No input was sent and no product command was issued during this window.

Task-180 requires no live Task-178/179 reset/uninstall process before install-over, but its hard fence does not authorize killing this remaining observer. Continuing to install-over would violate the preflight gate, so the task is blocked.

### Issue 3 — Candidate and installed facade hashes differ at pre-install boundary

Candidate facade SHA-256:

```text
aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f
```

Installed facade SHA-256:

```text
e15e8af49e18925fb569cd405b18fe5c57172d1a0e4644e359703b692cacb032
```

This is the expected baseline before Task-180 install-over and confirms why the install gate exists. It is not classified as an install failure because the installer was never invoked.

### Issue 4 — No install-over completion evidence exists

Because the preflight gate did not pass, there is no installer stdout/stderr, stage ledger, exit code, post-install ownership transition, active-facade equality proof, or post-install health result. These criteria are `UNPROVEN`, not `PASS` or `FAIL`.

### Issue 5 — Full-suite/CI status is inherited, not run by Task-180

Task-179 exact-SHA CI was accepted by fresh authority:

- Validate `33361090584`: success;
- Windows Installer Pack Smoke `33361090561`: success;
- PS5.1 Acceptance Smoke `33361090569`: success.

Task-180 did not modify source and did not dispatch new CI. No new CI was required or run after the blocked preflight.

## Actions explicitly not performed

The following counts are all zero for Task-180:

- supported installer invocation: `0`;
- second installer/retry: `0`;
- reset: `0`;
- uninstall/reinstall/rollback: `0`;
- executor lifecycle helper: `0`;
- Gateway/Ollama restart: `0`;
- Dashboard Send/composer input/`chat.inject`: `0`;
- model inference/recovery/regeneration: `0`;
- manual durable/config/transcript/route/DB repair: `0`;
- source/test/workflow/dependency edit: `0`;
- release/tag/merge/force push: `0`.

## Acceptance matrix

| Criterion | Verdict | Evidence |
|---|---|---|
| Fresh authority/task gate | `PASS` | Remote tip `a791828...`, ACTIVE/STATUS identify READY Task-180 |
| Report absent before work | `PASS` | Remote tree check at `a791828...` |
| Exact candidate checkout | `PASS` | Detached worktree at `f6392da...` |
| Candidate facade hash recorded | `PASS` | SHA-256 `aa747f...` |
| Current installed baseline inspected | `PASS` | Launcher, installed facade, package/fingerprint probes |
| Candidate facade already installed | `FAIL/PRECONDITION NOT MET` | Installed hash `e15e8a...` differs as expected baseline |
| Task-178 exact reset descendants gone | `PASS` | PIDs `17864`, `13628`, `5360` absent |
| No Task-178/179 reset observer remains | `BLOCKED` | Outer `run_reset178.py` chain PIDs `14196/22832/17052/17444` remains |
| Runtime/provider preflight | `PASS` | Managed generation 36; Gateway/Ollama healthy |
| Delivery/recovery preflight | `PASS` | `READY`, outbox 0, no incident, stateChanged false |
| SQLite preflight/history | `PASS` | Prior integrity/counts/history retained read-only |
| Exactly one supported install-over | `NOT PERFORMED` | Preflight blocked; installer count 0 |
| Post-install facade byte identity | `UNPROVEN` | Install-over not started |
| Post-install ownership/runtime health | `UNPROVEN` | Install-over not started |
| Post-install package/fingerprint proof | `UNPROVEN` | Install-over not started |
| Semantic/model/recovery action fence | `PASS` | All counts 0 |
| Report-only publication fence | `PASS` | Only this report will be published |

## Reviewer Verification Packet

1. Fresh remote authority at final check is `a7918285acb962b82ede8e398311a1f6f8171724`, with Task-180 still `READY_HERMES` and report absent before creation.
2. Candidate source was materialized at exact `f6392da3e4112ce441526d5ef19925c90a872b0b`; candidate facade SHA is `aa747f8f...`.
3. Installed launcher chain was read-only resolved to the expected v0.9.3 workspace facade, whose pre-install hash is `e15e8af4...`; mismatch is expected and proves install-over had not occurred.
4. The exact Task-178 reset children were gone, but the historical outer `run_reset178.py` observer chain remained alive after a further 60-second natural-exit observation.
5. Task-180 does not authorize killing the remaining observer, so the install-over was correctly not launched.
6. Runtime, provider, ownership, delivery, recovery, and SQLite preflight remained healthy/read-only; Task-171 history remained present.
7. The initial PowerShell parser error was corrected and recorded as a harness issue; it did not execute an installer or mutate product state.
8. No new source, test, workflow, dependency, lifecycle, semantic, model, recovery, or database action occurred in Task-180.
9. Task-179's accepted exact-SHA CI remains inherited authority evidence; no new Task-180 CI was needed after the preflight block.
10. Publication is report-only and the next action requires a successor explicitly authorizing cleanup of the remaining observer and a new preflight/install-over attempt.

## Proposed successor

Create a successor task that explicitly authorizes safe retirement of the remaining exact Task-178 outer observer chain (`run_reset178.py` and its known wrapper descendants), with exact identity verification and no product lifecycle action. After that successor establishes a clean process boundary, a new task may authorize one supported install-over of candidate `f6392da...`. Do not infer install success from the current package/fingerprint, and do not start reset until the installed facade byte identity is proven.

## Hard-fence declaration

Task-180 performed no install-over because the preflight gate was blocked. No reset, uninstall, retry, helper lifecycle command, Gateway/Ollama restart, semantic action, model/recovery action, manual state repair, source/test/workflow edit, release, merge, or force push was performed.
