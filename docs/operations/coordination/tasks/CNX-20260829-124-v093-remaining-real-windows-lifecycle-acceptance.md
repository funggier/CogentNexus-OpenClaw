# CNX-20260829-124 — v0.9.3 Remaining Real-Windows Lifecycle Acceptance

- Status: `READY_FOR_HERMES`
- Execution mode: `LIVE_WINDOWS_ACCEPTANCE_REMAINING_LIFECYCLE`
- Owner / independent reviewer: ChatGPT
- Executor: Hermes/Codex after operator continuation
- Date: 2026-08-29 ICT
- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `agent/v0.9.3-full-stabilization`

## Purpose

Continue the exact-candidate real-Windows acceptance from the coherent installed state proven by Task 123.

This task begins at **reset**. The Task-121 install-over has already been consumed and is permanently out of scope for this lifecycle attempt.

## Accepted predecessor

Task-123 report:

`docs/operations/coordination/reports/CNX-20260829-123-post-install-deterministic-readonly-attestation.md`

Independent review:

`docs/operations/coordination/reviews/CNX-20260829-123-post-install-deterministic-readonly-attestation-review.md`

Accepted verdict:

`ACCEPTED PASS — CURRENT POST-INSTALL STATE IS COHERENT; REMAINING ONE-SHOT LIFECYCLE MAY ADVANCE FROM RESET WITHOUT REPLAYING INSTALL-OVER.`

Task 123 proves the current installed state is coherent with deterministic argument-safe read-only evidence.

## Exact frozen candidate

Retain exactly:

- source SHA: `01d08cd7c82f542c821e3a60f7fffa036efb1d75`;
- package version: `0.9.3`;
- artifact ID: `9691451156`;
- artifact name: `cogentnexus-openclaw-v0.9.3-package-proof-01d08cd7c82f542c821e3a60f7fffa036efb1d75`;
- artifact digest: `sha256:9db9290e14646575586a42160b79cfea691e35f3a0ca7d294f7f941dcae0c87a`;
- package ZIP SHA256: `8e06b186e425170a22bfce06fa3505a7cdac3b097d4bfdc4ccc4d810d502cac1`;
- package tar.gz SHA256: `6a14cb665ca6148ce2912970df62027533aef34fb0c871a2e542d1b149e94f31`;
- payload/plugin fingerprint: `3b78a99ff15af2489b342aedbbdd7f32d35501f98bf79f016c66c301205049d4`;
- payload count: `178`.

No candidate substitution, repacking, or source edit is authorized.

## Carried one-shot ledger

Consumed and **forbidden to replay**:

- install-over: **1 / 1**.

Available in this task, each at most once:

- reset: `0 / 1`;
- uninstall: `0 / 1`;
- fresh reinstall after successful uninstall: `0 / 1`;
- stop: `0 / 1`;
- start: `0 / 1`;
- restart: `0 / 1`;
- recovery harness: `0 / 1`.

## Deterministic verification discipline

The Task-121/122 executor probe-wrapper failures are closed history. Do not reuse those generalized wrappers.

For all post-phase proof in this task:

1. Do not define a helper parameter named `args`/`Args` that collides with PowerShell automatic `$args`.
2. Prefer direct PowerShell call operator `&` with explicit executable/script path and separate literal arguments.
3. Do not use `Start-Process` as a generic command-verification wrapper.
4. Do not invoke bare `python`, bare `openclaw`, or bare `ollama`.
5. For OpenClaw automation, prefer package metadata + direct `node.exe <openclaw dist/index.js> <literal args>` where CLI proof is required.
6. For Ollama readiness/preservation, prefer loopback REST (`/api/version`, `/api/tags`, `/api/ps`) and listener/process proof rather than desktop UI commands.
7. For CNX, direct installed `cnxclaw.cmd` commands with literal arguments are accepted and were proven deterministic in Task 123.
8. Use explicit installed ownership-script path and explicit owned runtime Python path for ownership/SQLite proof.
9. Capture stdout/stderr/exit code and relevant JSON for each probe separately.
10. If any verification invocation itself is malformed or ambiguous, stop; do not infer product failure from the malformed probe.

## Non-negotiable execution rules

- Do not run install-over.
- Every remaining disruptive phase runs at most once.
- Stop immediately on first non-zero exit, failed postcondition, ownership ambiguity, integrity mismatch, or unsafe preservation result.
- Do not replay a completed phase because a shell/session/watchdog restarts.
- Do not manually clean, move, delete, or normalize state to continue.
- Preserve evidence before stopping.
- No Dashboard semantic nonce/message/Send.

## Phase 0 — fresh coordination and pre-reset read-only fence

Before mutation:

- confirm Task 124 is still authoritative in `ACTIVE.md` and `STATUS.md`;
- confirm exact candidate identity remains unchanged;
- confirm Task-121 install-over remains consumed;
- confirm Task-123 accepted current-state evidence remains the latest authoritative live baseline;
- create a fresh external Task-124 evidence root;
- perform a concise deterministic read-only sanity check: CNX status/recovery, ownership verify, installed fingerprint, OpenClaw baseline/plugin uniqueness, Gateway listener, Ollama REST, SQLite integrity.

This is not a replay of Task 123; it is a freshness fence immediately before reset.

If the machine has drifted from the accepted coherent state: `BLOCKED`, zero new mutation.

## Phase 1 — reset exactly once

From the installed workspace run exactly once:

```powershell
.\cnxclaw.cmd reset
```

Provide exactly one normal `y` confirmation.

No provider argument.

Required post-reset proof using the deterministic discipline:

- reset exit code `0`;
- CNX-owned state is reconstructed according to reset contract;
- ownership verifies;
- installed plugin fingerprint still matches the frozen candidate;
- CNX status/recovery is coherent;
- OpenClaw remains exactly `2026.7.1-2`;
- current plugin registration/root remains coherent and unique;
- Gateway and runtime/provider readiness are coherent;
- Ollama models/data remain preserved;
- SQLite integrity is exactly `ok`;
- unrelated workspace/user data remains intact.

On first failure: stop; no reset retry.

## Phase 2 — uninstall exactly once

Only after Phase 1 passes, run exactly once:

```powershell
.\cnxclaw.cmd uninstall
```

Provide exactly one normal `y` confirmation.

Required uninstall proof:

- uninstall exit code `0`;
- current CogentNexus-OpenClaw-owned launcher/state/skill/plugin/service/task surfaces are removed according to contract;
- no active current product plugin registration remains;
- no ambiguous generic historical namespace is left as current product ownership;
- OpenClaw remains installed and exactly `2026.7.1-2`;
- OpenClaw Gateway/external baseline remains coherent according to uninstall contract;
- Ollama runtime, models, and data remain intact;
- unrelated workspace/user data remains intact;
- no manual cleanup is required to claim uninstall success.

Use direct Node/plugin inventory and loopback/listener proof where the CNX launcher no longer exists.

On first failure: stop; no uninstall retry and no manual cleanup.

## Phase 3 — fresh reinstall exact same artifact exactly once

Only after successful uninstall and its preservation proof.

Reverify the same frozen artifact/extraction before execution. Use a clean extraction if needed, but it must resolve to the exact pinned artifact/source/hashes.

Run exactly once:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace "$HOME\.openclaw\workspace"
```

No `-Provider` argument.

This is the authorized **fresh reinstall after uninstall**, not a replay of Task-121 install-over.

Required proof:

- installer exit code `0`;
- ownership verifies;
- installed plugin fingerprint equals the frozen candidate fingerprint;
- exactly one current plugin registration/root exists and is loaded/enabled;
- CNX launcher/state/skill/service surfaces are recreated coherently;
- CNX reaches the expected managed/ready state;
- Gateway is healthy;
- SQLite integrity is exactly `ok`;
- provider/runtime readiness is coherent as a separate runtime fact;
- OpenClaw/provider/models/unrelated data remain preserved.

On first failure: stop; no reinstall retry.

## Phase 4 — stop exactly once

Run exactly once:

```powershell
.\cnxclaw.cmd stop
```

Verify the requested CNX lifecycle state and relevant Gateway/provider expectations from product contract using direct status/listener evidence. Preserve external dependencies/data.

On failure: stop; no stop replay.

## Phase 5 — start exactly once

Run exactly once:

```powershell
.\cnxclaw.cmd start
```

Verify managed/readiness convergence, Gateway, provider, ownership, and SQLite integrity using deterministic probes.

On failure: stop; no start replay.

## Phase 6 — restart exactly once

Run exactly once:

```powershell
.\cnxclaw.cmd restart
```

Verify a completed restart transition with healthy final state and no duplicate/pending effect.

On failure: stop; no restart replay.

## Phase 7 — recovery reality harness exactly once

Only after stop/start/restart pass.

Run the exact candidate harness once:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\test-v093-ollama-recovery-windows-v3.ps1 -Scenario all -RunDisruptive
```

Provider-specific knowledge is legitimate here because this is runtime/recovery behavior.

Do not alter scenarios. Do not manually rerun failed scenarios.

On failure: stop; no harness replay.

## Phase 8 — final deterministic read-only lifecycle snapshot

After successful recovery harness, capture final proof using the Task-123 deterministic discipline:

- exact installed candidate/plugin fingerprint;
- CNX status/provider/recovery;
- ownership verification;
- OpenClaw version exactly `2026.7.1-2`;
- exactly one loaded/enabled current plugin registration/root;
- Gateway listener/process health;
- Ollama loopback version/tags/ps and model preservation;
- SQLite integrity exactly `ok`;
- scheduled-task/service state;
- current/legacy namespace inventory;
- transaction/staging/backup/rollover residue classification;
- no pending/duplicate lifecycle effect;
- no Dashboard semantic Send.

## Phase 9 — report and stop

Publish exactly:

`docs/operations/coordination/reports/CNX-20260829-124-v093-remaining-real-windows-lifecycle-acceptance.md`

The report must include:

- exact candidate/artifact identity;
- fresh evidence root;
- carried one-shot ledger proving install-over was not replayed;
- exact command, timestamp, stdout/stderr, exit code, and attempt count for reset/uninstall/fresh reinstall/stop/start/restart/recovery;
- deterministic postcondition evidence after every completed phase;
- preservation proof for OpenClaw/provider/models/unrelated data;
- final ownership/plugin/SQLite/Gateway/runtime snapshot;
- explicit confirmation no manual cleanup/normalization occurred;
- explicit confirmation no Dashboard semantic Send occurred;
- verdict `PASS`, `FAIL`, or `BLOCKED`;
- exact first failure boundary/root cause if not PASS.

Then stop for independent ChatGPT review.

Do **not** create or execute the final Dashboard durable-delivery task automatically.

## Hard fence

Task 124 does not authorize:

- replay of Task-121 install-over;
- candidate/artifact substitution;
- source edits or ad-hoc live repair;
- manual cleanup/normalization to force continuation;
- replay of completed/failed remaining phases;
- OpenClaw update/downgrade/reinstall/uninstall/rebaseline;
- provider runtime update/reinstall/reconfiguration;
- provider/model/endpoint/timeout changes;
- unrelated plugin/workspace mutation;
- credential/token/password access or re-entry;
- Dashboard semantic nonce/message/Send;
- reboot;
- generic process-tree kill outside the exact reviewed recovery harness safety contract;
- merge/tag/GitHub Release/force push.
