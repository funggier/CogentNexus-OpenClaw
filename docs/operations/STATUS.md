# Current Project Status

**Updated:** 2026-08-23  
**Development line:** v0.9.3 implementation and recovery proof  
**Release target:** v1.0.0 after complete real-Windows lifecycle acceptance  
**Active PR:** #24 — `v0.9.3: Ollama-only recovery reality and provider simplification`  
**Branch:** `agent/v0.9.3-recovery-reality-tests`  
**Status:** Task 038 validating operator-created exact-path Procmon configuration; PR remains Draft

## Current coordination task

Task `CNX-20260824-038` is `READY_FOR_CODEX` with execution mode `AUTO`.

The operator-created exact-path Procmon `.PMC` exists outside the repository with a reviewed expected identity: 2051 bytes and SHA256 `61F3BBB57B65F8DC708E66BC15B5B808AB44E9DC770799E8C32ED40724AE6CBC`.

Codex is authorized only to validate the exact artifact identity, bounded raw structural indicators, zero Procmon process/driver/service state, and absence of capture artifacts. Procmon must not be launched and capture must not start.

A Task 038 PASS validates only the saved configuration artifact. Trace execution still requires a separate exact task and human authorization.

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

## Latest accepted recovery result

Task `CNX-20260822-003` is accepted.

The focused real-Windows Gateway convergence diagnostic proved:

- exact OpenClaw Gateway `node.exe` PID `26384` was validated and stopped without a process-tree kill;
- the replacement Gateway listener appeared as different PID `39108`;
- no manual runtime transition occurred after injection;
- recovery first reported `READY_WITH_WARNINGS` while the intentional marker was active;
- durable recovery naturally converged to `READY` after 8 observations in 14.769 seconds;
- final state remained MANAGED with Ollama selected and both listeners healthy.

Therefore the earlier full-suite `gateway-after` failure is classified as an immediate-assertion defect in the v3 test harness, not a demonstrated runtime durable-state completion defect.


## Latest provider recovery evidence

Task `CNX-20260823-015` is reviewed `REWORK`, but it preserves important partial evidence from the immutable Task 010 TXT/JSON pair:

- healthy MANAGED/Ollama baseline was proven;
- the recorded Ollama listener changed from PID `55264` to replacement PID `46240`;
- runtime/provider health returned and one automatic recovery attempt recorded `success=true`;
- the provider incident remained open;
- every normal convergence observation stayed `READY_WITH_WARNINGS`;
- provider durable-state convergence failed when the 420-second observation fuse expired;
- operator `cnx stop` and explicit `cnx start` scenarios were skipped;
- cleanup returned the system to healthy MANAGED/Ollama state.

The correct current classification is `RUNTIME_RECOVERED_DURABLE_STATE_STUCK`. The complete Ollama exact-PID safety gate is not yet accepted from this evidence because required active-operation persistence and separate kill-exit fields were `NOT_RECORDED`. The provider incident lifecycle is not proven because normal incident closure was not recorded.

The disruptive suite must not be repeated until the offline diagnosis is reviewed and an exact later task authorizes the narrowest required validation.

## Accepted diagnostic

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

- complete Ollama exact-PID crash-safety acceptance (replacement-listener recovery is observed, but required safety fields remain incomplete);
- provider incident closure and durable-state convergence after real Ollama failure;
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

Complete and review Task `CNX-20260824-038`.

If the exact artifact identity and clean poststate pass, ChatGPT will design the separately fenced trace phase. That later phase must preserve the exact-path filter, Drop Filtered Events, bounded duration, no target stimulation, graceful cleanup, and duplicate-execution fence. It is not authorized yet.

Do not repeat Tasks 035–037, restore the 382 paths, launch Procmon during Task 038, broad-capture system activity, guess or stop an unproven watcher/process, or resume recovery/lifecycle execution.

## Queued desktop-memory diagnostic

The human operator observed the Windows ChatGPT desktop process group grow from roughly 2 GB to more than 4 GB and asked Codex to determine whether loaded Project/Chat/Work/Codex sessions or another process role is retaining memory.

The human operator subsequently observed that ChatGPT desktop RAM usage had decreased and directed coordination to continue CogentNexus once the checkout/race issue is safely resolved. This is evidence that immediate pressure improved, but it does not prove root cause.

Task `CNX-20260822-011` remains queued as a deferred conditional diagnostic. It must not interrupt Task 012 or delay the next process-recovery authorization while RAM remains stable. Activate it only if RAM growth recurs, system pressure becomes material, or the recovery sequence reaches a safe pause.

Task 011 is read-only. It inventories registered Git worktrees and Task-created full isolated clones, separates disk accumulation from exact-PID RAM attribution, identifies watchers/indexers/terminals still attached to stale paths, and produces a per-path cleanup manifest. It forbids process kill, process-tree operations, app restart, window closure, chat/project/session/cache deletion, worktree/clone removal or pruning, configuration changes, and CogentNexus/OpenClaw/Ollama actions. Any memory-reclaim or checkout-cleanup action requires a later evidence-based reviewed task naming exact safe targets.
