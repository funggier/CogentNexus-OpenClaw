# CNX-20260829-125 — v0.9.3 Recovery Reality Interactive Confirmation Acceptance

- Status: `READY_FOR_HERMES`
- Execution mode: `LIVE_WINDOWS_RECOVERY_ACCEPTANCE_ONLY`
- Owner / independent reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-29 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Complete only the still-unproven v0.9.3 recovery-reality acceptance after Task 124 successfully completed reset, uninstall, exact-candidate fresh reinstall, stop, start, and restart once each.

Task 124 invoked the exact recovery harness once, but the harness cancelled inside its interactive confirmation gate before any disruptive scenario began. Task 125 is a new explicit authorization for one recovery-suite execution with that exact confirmation contract satisfied.

This task does **not** authorize replay of any previously completed lifecycle phase.

## Accepted predecessor

Task-124 report:

`docs/operations/coordination/reports/CNX-20260829-124-v093-remaining-real-windows-lifecycle-acceptance.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-124-v093-remaining-real-windows-lifecycle-acceptance-review.md`

Accepted verdict:

`ACCEPTED PARTIAL PASS — RESET / UNINSTALL / FRESH REINSTALL / STOP / START / RESTART PASSED ONCE; RECOVERY PRODUCT BEHAVIOR WAS NOT TESTED BECAUSE THE EXACT HARNESS CANCELLED AT ITS UNSATISFIED INTERACTIVE CONFIRMATION GATE.`

## Exact frozen candidate

Retain exactly:

- source SHA: `01d08cd7c82f542c821e3a60f7fffa036efb1d75`;
- package version: `0.9.3`;
- artifact ID: `9691451156`;
- artifact digest: `sha256:9db9290e14646575586a42160b79cfea691e35f3a0ca7d294f7f941dcae0c87a`;
- package ZIP SHA256: `8e06b186e425170a22bfce06fa3505a7cdac3b097d4bfdc4ccc4d810d502cac1`;
- package tar.gz SHA256: `6a14cb665ca6148ce2912970df62027533aef34fb0c871a2e542d1b149e94f31`;
- payload/plugin fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- recovery harness Git blob: `80da4a2a23f5b5e936d725dcbd695a631bad1cb6`.

No source edit, repack, substitution, or harness modification is authorized.

## Carried consumed ledger

Consumed and forbidden to replay:

- Task-121 install-over: `1 / 1`;
- Task-124 reset: `1 / 1`;
- Task-124 uninstall: `1 / 1`;
- Task-124 fresh reinstall: `1 / 1`;
- Task-124 stop: `1 / 1`;
- Task-124 start: `1 / 1`;
- Task-124 restart: `1 / 1`;
- Task-124 recovery-harness process invocation: `1 / 1` under Task 124, cancelled before disruptive confirmation/scenario execution.

Task-124 disruptive scenario counts:

- explicit disruptive confirmation PASS: `0`;
- gateway-crash: `0`;
- provider-crash: `0`;
- operator-stop: `0`.

Task 125 grants exactly **one new recovery-suite execution** because Task 124 never entered any disruptive scenario. This authorization does not reopen any other consumed phase.

## Confirmation contract

The exact candidate harness uses:

```powershell
$answer=Read-Host 'Type y to continue'
if($answer -cne 'y'){throw 'Disruptive suite cancelled.'}
```

Therefore Task 125 requires a **true interactive PowerShell TTY/console session**.

Rules:

1. Do not invoke the harness until the executor has verified that the process has an interactive TTY capable of satisfying `Read-Host`.
2. Run the exact harness directly; do not wrap it in a generic command runner.
3. When the exact prompt `Type y to continue:` appears, enter exactly one lowercase literal `y` followed by Enter.
4. Do not send confirmation before the prompt appears.
5. Require the harness evidence step `explicit-disruptive-confirmation` to record `PASS`, confirmation `y`, and the requested disruptive scenarios before treating scenario execution as authorized.
6. Do not pipe `y`, redirect stdin as a workaround, synthesize host input, monkey-patch `Read-Host`, edit the harness, or create a replacement harness.
7. If a true interactive confirmation channel cannot be provided, stop `BLOCKED` **before invoking the disruptive suite**.

## Deterministic verification discipline

Use the accepted Task-123 direct-probe discipline for all non-harness evidence:

- no generalized wrapper parameter named `args`/`Args`;
- no generic `Start-Process` command-proof wrapper;
- direct `&` calls with explicit paths/literal arguments;
- CNX JSON status/provider/recovery commands;
- explicit ownership verify/fingerprint;
- OpenClaw package metadata/direct Node/listener proof;
- Ollama loopback REST/listener proof;
- explicit SQLite `PRAGMA integrity_check`.

## Phase 0 — fresh coordination and read-only recovery fence

Before the disruptive suite:

- confirm Task 125 is still authoritative in `ACTIVE.md` and `STATUS.md`;
- confirm no candidate/source substitution;
- confirm Task-124 consumed ledger;
- confirm current exact installed plugin fingerprint;
- confirm CNX managed state and recovery `READY`;
- confirm ownership verifies;
- confirm OpenClaw exactly `2026.7.1-2`;
- confirm exactly one loaded/enabled current CogentNexus-OpenClaw plugin root;
- confirm Gateway listener/process healthy;
- confirm Ollama REST/listener healthy and models preserved;
- confirm SQLite integrity exactly `ok`;
- confirm no unsafe pending lifecycle/recovery transition.

This phase is read-only. If it fails, stop `BLOCKED` with zero new recovery-suite execution.

Do **not** run start/restart to make the precondition pass. Current state must already be coherent.

## Phase 1 — exact recovery reality harness once

Use the exact retained candidate harness only.

Canonical command:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test-v093-ollama-recovery-windows-v3.ps1 -Scenario all -RunDisruptive
```

Execute it once in a true interactive TTY and satisfy the exact `Read-Host` prompt with one lowercase `y` as specified above.

Expected scenario set from `-Scenario all`:

- baseline;
- gateway-crash;
- provider-crash;
- operator-stop.

Required evidence:

- prechecks pass;
- `explicit-disruptive-confirmation` PASS;
- exact validated Gateway PID is killed only in the gateway-crash scenario;
- Gateway is observed recovered with a different PID and durable READY convergence;
- exact validated Ollama listener PID is killed only in the provider-crash scenario;
- Ollama is observed recovered with a different PID and provider recovery remains non-circuit-open;
- intentional operator stop remains stopped for the observation window and does not auto-recover;
- harness-supported start after intentional stop restores managed READY state;
- each named scenario records PASS;
- final suite result is PASS and process exit code is `0`.

The process/PID kills inside this exact reviewed harness are authorized only for the scenario being executed. No generic process-tree kill is authorized.

### Failure handling

If the harness reaches `explicit-disruptive-confirmation=PASS` and a scenario fails, treat that as a genuine recovery-acceptance failure boundary unless evidence proves a separate harness defect. Stop; do not rerun the suite or any scenario.

If the harness fails before `explicit-disruptive-confirmation=PASS`, stop and classify the boundary without inventing product failure evidence. No alternate confirmation method is authorized.

## Phase 2 — final deterministic read-only snapshot

Only after the recovery suite exits `0`, capture final proof:

- exact installed candidate/plugin fingerprint;
- CNX status/provider/recovery READY;
- ownership verification;
- OpenClaw exactly `2026.7.1-2`;
- exactly one loaded/enabled current plugin registration/root;
- Gateway listener/process health;
- Ollama loopback version/tags/ps and model preservation;
- SQLite integrity exactly `ok`;
- scheduled task/service state;
- namespace/residue classification;
- no pending/duplicate recovery effect;
- no Dashboard semantic Send.

No lifecycle command may be used to repair the final snapshot.

## Phase 3 — report and stop

Publish exactly:

`docs/operations/coordination/reports/CNX-20260829-125-v093-recovery-reality-interactive-confirmation-acceptance.md`

The report must include:

- exact candidate and harness identities;
- fresh evidence root;
- pre-recovery deterministic fence;
- proof of true interactive confirmation boundary;
- exact prompt and the single lowercase `y` confirmation event;
- harness log/JSON paths;
- explicit-disruptive-confirmation evidence;
- per-scenario results and relevant exact PID/recovery observations;
- suite exit code/result;
- final deterministic snapshot;
- carried consumed lifecycle ledger proving no reset/uninstall/reinstall/stop/start/restart replay;
- explicit confirmation no Dashboard semantic Send occurred;
- verdict `PASS`, `FAIL`, or `BLOCKED`;
- exact first failure boundary if not PASS.

Then stop for independent ChatGPT review.

Do not create or execute the final Dashboard durable-delivery task automatically.

## Hard fence

Task 125 does not authorize:

- install/install-over;
- reset/uninstall/reinstall;
- standalone stop/start/restart outside the exact recovery harness's own reviewed operator-stop scenario;
- source/harness edits;
- alternate/piped/synthesized confirmation mechanisms;
- manual cleanup/normalization;
- candidate/artifact substitution;
- OpenClaw update/rebaseline;
- provider runtime/config/model/endpoint/timeout changes;
- unrelated plugin/workspace mutation;
- credential/secret access;
- Dashboard semantic Send;
- reboot;
- generic process-tree kill;
- merge/tag/release/force push.
