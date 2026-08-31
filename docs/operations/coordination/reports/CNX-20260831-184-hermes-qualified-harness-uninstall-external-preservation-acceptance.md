# CNX-20260831-184 — Qualified-Harness Uninstall & External Preservation Acceptance

- **Task:** `CNX-20260831-184`
- **Disposition:** `PASS — QUALIFIED_HARNESS_UNINSTALL_EXTERNAL_PRESERVATION_ACCEPTED`
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Branch:** `agent/v0.9.3-full-stabilization`
- **Authority HEAD before activation:** `0f2c4af3b647a1f76d4b8474e6aad7990d11acc1`
- **Evidence root:** `C:\Users\CDQ-P\AppData\Local\Temp\cnx184-evidence-20260831T080000Z`
- **Executor:** Hermes/Codex
- **Coordinator / final reviewer:** ChatGPT

## Disposition

The installed `cnxclaw.cmd uninstall` path completed exactly one authorized uninstall through the qualified incremental character-prompt harness. The real confirmation prompt was observed before input, exactly one literal `y` line was sent, the process exited `0`, and stdout contained both the CogentNexus uninstall PASS marker and the native OpenClaw healthy marker.

Implementation-owned delayed cleanup converged within the bounded observation interval. The CNX-owned launcher, skill, extension payload, state root, application-data/runtime root, scheduled task, and plugin registration/config reference are absent. Native OpenClaw, Gateway, Ollama, model inventory, unrelated plugin inventory, and gateway command surface remain preserved and usable. Reinstall was not performed and remains unauthorized.

## Fresh authority and entering state

Fresh remote authority before activation:

```text
REMOTE_HEAD=0f2c4af3b647a1f76d4b8474e6aad7990d11acc1
ACTIVE status=READY_HERMES
ACTIVE task=CNX-20260831-184
execution mode=WINDOWS_QUALIFIED_HARNESS_UNINSTALL_EXTERNAL_PRESERVATION_HERMES
STATUS state=READY_HERMES
```

The Task-184 report was absent at the authority tip before creation. Pre-uninstall read-only process scan returned:

```text
NO_OBSERVER_OR_LIFECYCLE_PROCESS
```

Entering state:

```text
active facade sha256: aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f
release: 0.9.3
OpenClaw: 2026.7.1-2 (0790d9f)
plugin fingerprint: e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19
controller: managed, generation 3
selected provider: ollama, transition null
Gateway: healthy
Ollama: reachable/healthy/ready
ownership: OWNERSHIP_PRESENT; legacy=[]
delivery: READY; pending outbox 0
recovery: READY
SQLite integrity: ok
```

Pre-uninstall reset-owned durable counts were all zero:

```text
tickets                  0
ticket_events            0
ticket_outbox             0
cnx_assistant_delivery    0
cnx_direct_model_call     0
cnx_direct_recovery       0
cnx_sessions              0
```

## External-preservation freeze

Before uninstall, the following read-only preservation evidence was captured:

- OpenClaw version: `OpenClaw 2026.7.1-2 (0790d9f)`;
- Ollama complete model inventory JSON and digest;
- unrelated OpenClaw plugin inventory with the CNX plugin excluded;
- OpenClaw gateway command file hash;
- OpenClaw configuration surface hash, retained only as a raw hash because uninstall is expected to remove the CNX registration from that file;
- exact CNX-owned paths expected to be removed.

The pre-uninstall Ollama inventory SHA-256 was:

```text
a9f2214d57e1f279d896e5de687f546066a5e3f35b366eea95fc487deaba935a
```

The unrelated plugin inventory contained `71` entries and had normalized comparison hash:

```text
8d58154632fff0eb998af72dce688326d055707d76e7a4fba464d8f63bd53752
```

## Exactly one qualified uninstall

Exact root command:

```text
C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd uninstall
```

Harness topology:

```text
persistent Python supervisory harness
  -> cmd.exe /d /c installed cnxclaw.cmd uninstall
      -> repaired v0.9.3/legacy facade
          -> host_control_v092
              -> lifecycle_v092
```

Evidence:

```text
b01-uninstall.events.jsonl
b01-uninstall.stdout.log
b01-uninstall.stderr.log
b01-uninstall.result.json
```

Result:

```text
invocationCount=1
promptObserved=true
inputSendIntentCount=1
inputSentCount=1
stdinClosed=true
exitCode=0
uninstallPassMarker=true
nativeOpenClawHealthyMarker=true
stdoutBytes=3172
stderrBytes=0
durationSeconds=67.63555407524109
```

The durable event order proved:

```text
harness_started
cmd_process_started
prompt_observed
input_send_intent
input_sent
stdin_closed
...
uninstall_pass_marker_observed
native_openclaw_healthy_marker_observed
cmd_process_exited
orphan_scan_completed
run_finalized
```

No second `y`, retry, or second uninstall occurred.

## Delayed cleanup convergence

After uninstall exit, only the implementation-owned delayed cleanup observation interval was used. No manual deletion or repair was performed.

After convergence, all ownership-defined CNX surfaces were absent:

| CNX-owned surface | Before | After | Result |
|---|---|---|---|
| `C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd` | present | absent | removed |
| workspace skill `skills\cogentnexus-openclaw` | present | absent | removed |
| direct extension `extensions\cogentnexus-openclaw` | present | absent | removed |
| CNX state root `.cogentnexus-openclaw` | present | absent | removed |
| local application-data/runtime root | present | absent | removed |
| CNX scheduled task | present | absent | removed |
| CNX cleanup/uninstall/lifecycle process | running during boundary | absent | converged |

Independent process-file scan returned:

```text
NO_CNX_CLEANUP_OR_LIFECYCLE_PROCESS
```

OpenClaw plugin inventory contained no `cogentnexus-openclaw` entry after uninstall. The read-only config lookup returned `Config path not found: plugins.entries.cogentnexus-openclaw`, which is consistent with removal of the CNX registration and is not treated as a probe failure.

## Native runtime and external preservation

Post-uninstall read-only checks:

```text
OpenClaw version: 2026.7.1-2 (0790d9f)
Gateway status: healthy, loopback 127.0.0.1:18789, connectivity probe ok
Ollama API: HTTP 200
Ollama model inventory SHA-256: a9f2214d57e1f279d896e5de687f546066a5e3f35b366eea95fc487deaba935a
Unrelated plugin inventory: 71 entries, normalized hash unchanged
Gateway command hash: cf91e215a19bf767791efc671479ba65db110894e5448e3c72218c99a40fbb77
```

The Ollama inventory digest before and after was identical. No Ollama model/data removal occurred. The native OpenClaw installation and Gateway remained available and healthy. The gateway command surface was byte-unchanged.

The full OpenClaw configuration file hash changed from:

```text
pre:  cec9f00520b02231c47ba5ed293c015f9ade38ed52a38a2e4608d58101bcc0c6
post: 5c6016fd7d0422dd31a9697b469b014db1ca9298b3774b62dd79e105b1b288d9
```

This is expected because uninstall removes the CNX-owned plugin registration/config surface. The report does not claim full-file config identity. The targeted unrelated plugin inventory remained unchanged, and the CNX config reference was absent after uninstall.

## Complete issue register

### Issue 1 — Initial broad process probe was self-matching

- **Observed symptom:** the first post-cleanup inline process probe captured its own shell command because the regex text appeared in that command line.
- **Product state impact:** none.
- **Correction:** replaced it with an independent PowerShell script-file probe whose command line did not contain the matching patterns.
- **Final result:** `NO_CNX_CLEANUP_OR_LIFECYCLE_PROCESS`.
- **Remaining consequence:** the initial probe is not used as authoritative evidence; the corrected probe is.

### Issue 2 — OpenClaw configuration hash changed

- **Observed symptom:** full `openclaw.json` hash changed after uninstall.
- **Product state impact:** expected CNX registration removal; no evidence of unrelated namespace loss.
- **Correction/classification:** reported explicitly rather than incorrectly claiming full-file preservation; compared unrelated plugin inventory and gateway command surface separately.
- **Remaining consequence:** any later reinstall must recreate only the authorized CNX registration through the supported installer.

### Issue 3 — Config lookup returned path-not-found

- **Observed symptom:** `openclaw config get plugins.entries.cogentnexus-openclaw` returned a path-not-found message.
- **Product state impact:** none; this is the expected absence check after uninstall.
- **Classification:** positive removal evidence, not a failure.
- **Remaining consequence:** none for Task-184.

No uninstall timeout, missing prompt, missing completion marker, second-send attempt, process orphan, stderr output, product failure, or preservation mismatch was observed.

## Acceptance matrix

| Criterion | Result | Evidence |
|---|---|---|
| Fresh Task-184 authority and READY gate | PASS | remote `0f2c4af3...`, ACTIVE/STATUS |
| Task-184 report absent before work | PASS | remote `git ls-tree` |
| Pre-uninstall facade/provenance | PASS | `a01-facade-sha.txt`, version/plugin probes |
| Clean process boundary | PASS | `a02-process.txt` |
| Fresh managed/zero durable state | PASS | `a03`–`a11` evidence |
| External-preservation freeze | PASS | OpenClaw/Ollama/plugin/config/gateway evidence |
| Exactly one uninstall invocation | PASS | `b01-uninstall.result.json` |
| Exact prompt observed before input | PASS | incremental ledger |
| Exactly one literal `y` | PASS | ledger/result count `1` |
| Uninstall exit code `0` | PASS | result and process-exit event |
| Uninstall PASS marker | PASS | stdout and ledger |
| Native OpenClaw healthy marker | PASS | stdout and ledger |
| Delayed cleanup converged | PASS | `c01-owned-paths.json`, independent process scan |
| CNX-owned launcher/skill/plugin/state/runtime removed | PASS | owned-path matrix |
| CNX scheduled task removed | PASS | `c12-scheduled-tasks.txt` |
| CNX plugin registration/load removed | PASS | `c05-plugins.json`, `c13-plugin-config.txt` |
| Native OpenClaw preserved | PASS | version and Gateway status |
| Gateway healthy | PASS | `c04-gateway-status.txt` |
| Ollama preserved and healthy | PASS | HTTP/API and inventory digest |
| Model inventory unchanged | PASS | pre/post identical SHA-256 |
| Unrelated plugin inventory unchanged | PASS | normalized hash unchanged |
| Gateway command surface unchanged | PASS | identical hash |
| Semantic/model/recovery work | PASS — zero | hard-fence audit |

## Reviewer Verification Packet

1. Verify remote authority and Task-184 READY state at `0f2c4af3...`.
2. Read `a01`–`a11` and confirm the fresh managed/zero-state entering baseline.
3. Read `b01-uninstall.events.jsonl` and verify prompt → intent → sent ordering and one-send budget.
4. Read `b01-uninstall.result.json`; confirm invocation `1`, exit `0`, and both required markers.
5. Read `c01-owned-paths.json`; confirm all CNX-owned paths are absent.
6. Read `c08-independent-process.txt` and confirm no cleanup/lifecycle process remains.
7. Read `c05-plugins.json` and `c13-plugin-config.txt`; confirm CNX is not registered/loaded.
8. Read `c03-openclaw-version.txt` and `c04-gateway-status.txt`; confirm native OpenClaw remains healthy.
9. Compare `a11-ollama-tags.json` and `c06-ollama-tags.json`; confirm identical model inventory digest.
10. Confirm no reinstall, reset, second uninstall, manual deletion/repair, Dashboard, model, recovery, or source mutation occurred.

## Hard-fence audit

```text
uninstall root invocations: 1 authorized
confirmation input sends: 1 literal y line
implementation-owned delayed cleanup: 1 convergence boundary
reinstall/install/install-over: 0
reset: 0
second uninstall/retry: 0
second confirmation send: 0
executor-issued lifecycle helper: 0
manual Gateway/Ollama lifecycle action: 0
manual deletion/repair: 0
Dashboard Send/composer input/chat.inject: 0
model inference/recovery/regeneration: 0
manual DB/config/transcript/route repair: 0
product/source/test/workflow/dependency changes: 0
release/tag/merge/force push: 0
```

## Publication fence and successor boundary

This report is the only repository path authorized for Task-184 publication. After publication, stop for ChatGPT review. The uninstall and external-preservation boundary is proven. Reinstall remains unauthorized and requires a later explicit coordination task.
