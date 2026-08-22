# Current Project Status

**Updated:** 2026-08-22  
**Development line:** v0.9.3 implementation and recovery proof  
**Release target:** v1.0.0 after complete real-Windows lifecycle acceptance  
**Active PR:** #24 — `v0.9.3: Ollama-only recovery reality and provider simplification`  
**Branch:** `agent/v0.9.3-recovery-reality-tests`  
**Status:** development / evidence gathering; PR remains Draft

## Stable foundation

### v0.9.2

v0.9.2 is the frozen Golden Baseline.

It has completed Windows acceptance and release publication. Do not rewrite or patch the released tag merely to simplify v0.9.3 development.

Release/base commit:

```text
986f3c7be8389866f3ffe4f9b372ff1264ddbe8e
```

## v0.9.3 direction

v0.9.3 intentionally narrows the managed local provider surface to **Ollama only**.

LM Studio support remains historical v0.9.2 behavior. v0.9.3 operator-facing paths should not select, start, stop, probe, advertise, or test LM Studio. Existing LM Studio installations on a user's machine are left untouched.

The purpose of the simplification is to reduce provider-specific lifecycle complexity while recovery/continuity semantics are being proven on real Windows systems.

## v1.0.0 acceptance target

The human-authorized release objective is now `v1.0.0`, but the project is not release-ready yet.

In addition to the current process-recovery gates, the exact release candidate must prove on the real Windows target:

- installation from the actual release/consumer path;
- safe installation over an existing CogentNexus deployment without first uninstalling;
- `cnx reset` with explicit `y` confirmation and a verified fresh-install state;
- clean CogentNexus uninstall with explicit `y` confirmation;
- removal of CogentNexus-owned tasks, package/plugin state, launchers, and managed artifacts;
- preservation of external OpenClaw and Ollama installations and user data;
- reinstall from the actual release/consumer path after uninstall;
- MANAGED/Ollama/Gateway health and recovery verdict `READY` after reinstall;
- exact artifact/source provenance, SHA256 evidence, and green CI.

The coordination loop will prepare the accepted candidate for final human review. It must not merge, tag, or publish `v1.0.0` automatically.

## Proven on the current real-Windows test path

The following have direct evidence on the target machine:

- v0.9.3 Ollama-only candidate installs and loads;
- OpenClaw configuration validates;
- Ollama is reachable and selected as the managed provider;
- MANAGED baseline reaches `READY`;
- Gateway and Ollama listeners are identified through exact listener PIDs;
- disruptive harness kill safety no longer uses process-tree termination;
- Gateway hard-crash injection targeted the validated OpenClaw `node.exe` PID only;
- the killed Gateway returned with a different PID;
- cleanup after the interrupted suite restored MANAGED + Ollama + Gateway to `READY`.

## Current blocking question

The current investigation is **Gateway durable-state convergence after physical runtime recovery**.

Observed sequence:

```text
Gateway healthy
   ↓
exact Gateway PID hard-killed
   ↓
Gateway listener returns with new PID
   ↓
`cnx check recovery` still reports READY_WITH_WARNINGS
   ↓
maintenance/recovery marker still active
```

The marker reported:

```text
reason: CogentNexus external supervisor confirmed an unresponsive Gateway
recoveryPolicy: healthy-runtime
```

The previous full v3 harness asserted `READY` shortly after the listener returned and therefore failed at `gateway-after`.

This does **not** prove that Gateway recovery failed. Gateway process recovery itself succeeded.

What remains unknown is whether the durable marker:

1. converges to `READY` naturally after additional supervisor reconciliation, or
2. remains stuck until an operator transition such as `cnx start` occurs.

That distinction determines whether the next fix belongs in the test harness or in the runtime state machine.

## Active diagnostic

A focused diagnostic now exists:

```text
scripts/test-v093-gateway-convergence-windows.ps1
```

Its job is intentionally narrow:

1. confirm healthy MANAGED/Ollama baseline;
2. validate exact Gateway listener process identity;
3. hard-kill only that PID;
4. observe the replacement Gateway listener;
5. do **not** call `cnx start` during convergence observation;
6. poll `cnx check recovery --json` read-only;
7. determine whether durable recovery state reaches `READY` by itself.

The observation fuse is a test safety bound only. It must not become recovery authority.

## Current repository gate

At development head `306b091352a652a898c353aa49323c8d6a389106`, all eight current CI workflows completed successfully, including the dedicated Gateway Convergence smoke test.

The operations-doc commits after that head contain documentation only; runtime conclusions must continue to reference the tested implementation/evidence head where appropriate.

## Not yet proven in the current v0.9.3 real-Windows suite

Do not claim these as passed yet:

- Ollama listener hard-crash recovery;
- provider incident lifecycle under real Ollama failure;
- intentional `cnx stop` no-auto-recovery behavior in the current full suite;
- operator `cnx start` continuation after that stop scenario;
- active LLM-call continuation when Gateway dies;
- active LLM-call continuation when Ollama dies;
- Host/supervisor death and reconciliation;
- result committed but delivery interrupted;
- Windows reboot / abrupt power-loss continuation;
- exactly-once behavior for arbitrary external side effects.

## Safety state

The current disruptive harness design requires exact process identity before kill and forbids process-tree kill.

Protected process classes include PowerShell, cmd, conhost, Firefox, Explorer, Windows Terminal/OpenConsole, the harness itself, and harness ancestors.

This hardening was introduced after an early harness terminated unrelated interactive processes. That old harness must not be reused.

## Immediate next step

Run the focused Gateway Convergence diagnostic on the real Windows target and classify the result:

- **Natural convergence to `READY`** → adjust full-suite timing/observation semantics; do not modify recovery authority unnecessarily.
- **No natural convergence inside the evidence fuse** → treat as a runtime durable-state completion bug and fix the recovery boundary before continuing to provider-crash tests.

After this blocker is closed, return to the process-level suite: Gateway crash → Ollama crash → intentional stop/start.

After the process-level evidence is accepted, continue through the v1.0.0 lifecycle sequence: release-path install → install-over-existing → reset → clean uninstall → release-path reinstall → post-reinstall verification → exact-artifact CI/review.