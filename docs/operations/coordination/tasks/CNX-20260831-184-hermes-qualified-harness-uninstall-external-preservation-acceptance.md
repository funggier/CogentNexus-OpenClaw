# CNX-20260831-184 — Qualified-Harness Uninstall & External Preservation Acceptance

- **Task:** `CNX-20260831-184`
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Branch:** `agent/v0.9.3-full-stabilization`
- **Executor:** Hermes/Codex
- **Coordinator / final reviewer:** ChatGPT
- **Execution class:** destructive live-Windows lifecycle acceptance

## Objective

Prove exactly one real Windows `cnxclaw.cmd uninstall` from the accepted post-reset fresh state, with explicit one-shot confirmation, then prove that only CogentNexus-OpenClaw-owned surfaces are removed while native OpenClaw, Ollama, model inventory, and unrelated data remain intact.

This task does **not** authorize reinstall. Reinstall is a separate successor only after ChatGPT accepts this uninstall boundary.

## Accepted entering state

Accepted repository repair candidate:

`f6392da3e4112ce441526d5ef19925c90a872b0b`

Accepted active installed facade SHA-256 before uninstall:

`aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

Task 183:

`ACCEPTED_PASS — QUALIFIED_HARNESS_RESET_FRESH_STATE_REACCEPTED`

Entering runtime is expected to be fresh-install MANAGED with zero reset-owned Ticket/event/delivery/model-call/recovery/session rows, OpenClaw `2026.7.1-2`, Ollama healthy, and model inventory preserved.

## Phase A — fresh read-only preflight

Before any destructive action:

1. fetch fresh remote HEAD, `ACTIVE.md`, `STATUS.md`, and this task;
2. confirm Task-184 report is absent;
3. confirm no conflicting authorization;
4. confirm no observer/reset/uninstall/lifecycle residue is alive;
5. confirm installed launcher/facade identity and facade SHA-256 `aa747f8f...`;
6. confirm release `0.9.3`, OpenClaw `2026.7.1-2`, plugin loaded/enabled, ownership valid, legacy namespace empty;
7. confirm controller MANAGED, selected provider Ollama, no transition, Gateway healthy, Ollama healthy/ready;
8. confirm delivery/recovery READY and pending outbox `0`;
9. open SQLite read-only and confirm integrity `ok` plus fresh-state zero durable counts;
10. freeze external-preservation evidence before uninstall, including:
    - OpenClaw executable/version and native configuration surfaces needed for later comparison;
    - Ollama API health and complete model inventory digest;
    - unrelated workspace / `.openclaw` paths or namespace inventory selected by the repository ownership contract;
    - exact CogentNexus-owned paths expected to be removed.

If any identity or state is ambiguous, publish `BLOCKED` without launching uninstall.

## Phase B — exactly one qualified uninstall

Use the Task-177-qualified incremental character-prompt harness architecture against exactly:

```text
C:\Users\CDQ-P\.openclaw\workspace\cnxclaw.cmd uninstall
```

Requirements:

- uninstall root invocation budget: `1`;
- observe exact real `Continue? [y/N]: ` prompt before any input;
- persist/fsync `prompt_observed` and `input_send_intent` before input;
- send exactly one literal `y` line;
- confirmation send budget: `1`;
- continuously drain stdout/stderr and persist an incremental ledger;
- record process identities, command line, exit code, output markers, and final orphan scan.

If an outer shell/session loses contact or times out, do **not** launch another uninstall and do **not** send another input. Continue from the same durable ledger/process evidence only.

## Required uninstall execution proof

PASS requires:

- exactly one uninstall invocation;
- prompt observed before input;
- exactly one literal `y` sent;
- child exit `0`;
- stdout contains `COGENTNEXUS-OPENCLAW UNINSTALL: PASS`;
- stdout confirms native OpenClaw healthy boundary;
- no second uninstall, no retry, no second confirmation.

## Phase C — Windows delayed-cleanup completion

The implementation schedules Windows cleanup after command exit because the running launcher/module cannot delete itself synchronously.

After uninstall exits:

- wait only a bounded observation interval for the scheduled cleanup process to converge;
- do not invoke uninstall again;
- verify no CogentNexus cleanup process remains after convergence;
- verify the ownership-defined CogentNexus surfaces are absent, including the launcher, installed skill, extension/plugin payload, CNX state root, installer-owned local backup/runtime root, and startup integration as applicable to the accepted ownership contract;
- verify plugin registration/load-path/config references for `cogentnexus-openclaw` are removed;
- record any already-absent path as converged, not as a reason to repeat cleanup.

If cleanup remains ambiguous after the bounded interval, report `UNPROVEN/BLOCKED`; do not rerun uninstall and do not perform manual deletion.

## Phase D — external preservation and native runtime proof

Use native/read-only probes only; the CogentNexus launcher is expected to be gone.

PASS requires:

- OpenClaw executable remains installed and reports `2026.7.1-2 (0790d9f)`;
- native OpenClaw Gateway is healthy after the uninstall boundary;
- CogentNexus plugin is not registered/loaded;
- Ollama remains installed/reachable/healthy;
- pre/post Ollama model inventory digest is identical;
- no Ollama model/data removal occurred;
- unrelated workspace/`.openclaw` namespaces selected in preflight remain present and unchanged according to the frozen comparison;
- no CogentNexus-owned state/plugin/launcher/startup residue remains beyond any explicitly documented non-owned historical evidence files outside the ownership boundary;
- no semantic/model/recovery work is manufactured.

## UI policy

No Dashboard/UI action is required or authorized in Task 184.

For later Dashboard acceptance, UI navigation/click actions such as New Session, selecting the composer, and Send are human-controlled by the user; Hermes may type only after the user has focused the intended text field, and Hermes must not press Send.

## Hard fence

Authorized live mutation:

- exactly one installed `cnxclaw.cmd uninstall` and its implementation-owned delayed cleanup.

Not authorized:

- reinstall/install/install-over;
- second uninstall or retry;
- reset;
- second confirmation input;
- executor-issued start/stop/restart/enable/disable helpers outside uninstall internals;
- manual Gateway/Ollama lifecycle action;
- manual deletion/repair of CNX paths after uninstall;
- Dashboard Send/composer semantic action;
- model inference/recovery/regeneration;
- manual DB/config/transcript/route repair;
- product/source/test/workflow/dependency edits;
- release/tag/merge/force push.

Semantic/model/recovery action budget: `0`.

## Report contract

Publish only:

`docs/operations/coordination/reports/CNX-20260831-184-hermes-qualified-harness-uninstall-external-preservation-acceptance.md`

Include disposition, exact authority HEAD, preflight, one-shot event ledger summary, prompt/input ordering, exit/output markers, delayed-cleanup evidence, owned-path before/after matrix, plugin/config/startup removal proof, OpenClaw/Ollama/model/unrelated-data preservation matrix, complete issue register, hard-fence audit, Reviewer Verification Packet, and exact successor recommendation.

After report publication, stop for ChatGPT review. Reinstall remains unauthorized.
