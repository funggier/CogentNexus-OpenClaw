# Independent Review — CNX-20260901-213 Task-212 Installer Source + Detached-Launch Root-Cause Adjudication

## Verdict

`ACCEPT_PASS_DETACHED_LAUNCH_HARNESS_DEFECT_PROVEN__QUALIFY_DURABLE_WINDOWS_LAUNCHER_BEFORE_INSTALLER`

Task 213 closes the Task-212 empty-stream/rapid-disappearance boundary without attributing it to CogentNexus product code.

## Accepted findings

The following findings are accepted as sufficiently evidenced:

1. The Task-212 executed installer path belonged to a clean Git descendant of the Task-207 candidate and the relevant source files were byte-identical to candidate `27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`:
   - `scripts/install.ps1` SHA-256 `8cb713b7ddfe5be113530298fe3195094c0055a78ff63cdb393a483debc47e56`;
   - `plugins/cogentnexus-openclaw/src/v091-dashboard-verified-delivery.ts` SHA-256 `157460ee24a37472830b30dd19fec06172e3245b0f25447ddc0db1280b43473a`;
   - `plugins/cogentnexus-openclaw/openclaw.plugin.json` SHA-256 `1f35d3a2a8ed2550f4afc906a2f9a339e3e0f1a44e240994aab9a4fbaf771e`.
2. The executed checkout's ignored generated plugin tree fingerprint differed from the verified Task-207 package fingerprint. This is correctly treated as a source/build-output distinction and is not accepted as installed-package provenance.
3. The Task-212 launcher used `subprocess.Popen` with `stdin=DEVNULL`, redirected stdout/stderr, `close_fds=true`, `DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP` (`0x208`), no wait, no cwd override, and immediate launcher exit.
4. A harmless PowerShell child using the same launch topology reproduced the decisive failure shape:
   - immediate PowerShell identity was observed;
   - expected lifetime was >=65 seconds;
   - child was gone before the 10-second sample;
   - stdout/stderr remained zero bytes;
   - no start/end markers were emitted;
   - the launcher itself returned `0` and could not retain the child's intended exit code `23`.
5. This reproduction did not access CogentNexus/OpenClaw product paths and is therefore sufficient to classify the detached launch/stream topology as defective or incompatible with the current Windows executor environment.
6. Live product state remained preserved: PASSTHROUGH, old live fingerprint `f82674172a3946e00ddcb3a94fd14c8476bf91abc11ed7d44b5fa53acb74eaf1`, Gateway healthy, delivery/recovery READY, SQLite integrity `ok`, Task-205 recovery cancelled/inert, and no relevant lifecycle residue.

## Interpretation

Task 212 is not accepted as an installer attempt that reached or failed inside the installer body. The empty streams and rapid disappearance are fully explained by a launcher boundary that independently fails for a harmless child.

No CogentNexus installer source defect is established by Tasks 212–213.

The Task-207 product candidate remains repository-GREEN and unchanged:

`27fe0181b3b65d555a3b0cc8354f6f7945c21c0b`

Candidate plugin fingerprint remains:

`d0677581d60d3d5535c65e3261dae6f50d7aeb245b8680adac0cace4c040643b`

## Required successor boundary

Do not authorize another CogentNexus installer yet.

A successor must first qualify a durable Windows launch mechanism using a harmless process only. The qualified mechanism must prove all of the following before it may be reused for the installer:

- child lifetime is independent from the executor command/session;
- immediate OS identity is captured;
- stdout and stderr are durably observable while the child is running;
- the child survives for the intended >=60-second interval;
- terminal result/exit code is recoverable after completion;
- observer reconnects do not kill or restart the child;
- no PID-only interpretation is allowed without creation-time/executable/argv binding;
- harness artifacts are cleaned up without touching product state.

Windows Task Scheduler is an appropriate next topology to qualify because its task service owns the launched process independently from the Hermes executor session and exposes task state/`LastTaskResult`. It must be tested with a harmless child before any product installer is placed behind it.

## Authorization decision

Task 213 is accepted as diagnostic PASS only.

No installer, lifecycle action, plugin mutation, ownership mutation, SQLite write, Gateway restart, provider/model change, or Discord Send is authorized by this review.
