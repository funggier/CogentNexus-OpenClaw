# CNX-20260831-185 — Fresh Reinstall Post-Uninstall Reacceptance

- **Task:** `CNX-20260831-185`
- **Executor:** Hermes/Codex
- **Coordinator / final reviewer:** ChatGPT
- **Repository:** `funggier/CogentNexus-OpenClaw`
- **Branch:** `agent/v0.9.3-full-stabilization`
- **Execution mode:** `WINDOWS_FRESH_REINSTALL_POST_UNINSTALL_REACCEPTANCE_HERMES`
- **Authorization:** `CNX-20260831-185_HERMES_FRESH_REINSTALL_POST_UNINSTALL_REACCEPTANCE`

## Objective

From the accepted Task-184 native-OpenClaw post-uninstall boundary, perform exactly one supported fresh reinstall of the exact frozen candidate, then prove the installed candidate identity, ownership, plugin/controller/runtime health, fresh durable-state boundary, and preservation of external OpenClaw/Ollama/unrelated surfaces.

This task does **not** perform the final Dashboard semantic/durable-delivery acceptance.

## Accepted authority

Exact candidate:

`f6392da3e4112ce441526d5ef19925c90a872b0b`

Candidate facade:

- path: `skills/cogentnexus-openclaw/scripts/cnxclaw.py`
- Git blob: `879083d6186589d4b2774b8fd87fa93692dd2dfc`
- SHA-256: `aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`

Supporting accepted provenance:

- release: `0.9.3`
- npm package SHA-256: `8f6d0b8e64b1b53199ab1841a41bc1032241d107eac68603066fdd2ea642ca91`
- plugin fingerprint: `e7d7d6c115040368e35232c83cacec315f6667c92452a5641f7a48a6947baf19`
- OpenClaw: `2026.7.1-2 (0790d9f)`

Task-184 accepted post-uninstall preservation baseline:

- native OpenClaw/Gateway healthy;
- Ollama healthy;
- Ollama model inventory SHA-256 `a9f2214d57e1f279d896e5de687f546066a5e3f35b366eea95fc487deaba935a`;
- unrelated plugin inventory normalized hash `8d58154632fff0eb998af72dce688326d055707d76e7a4fba464d8f63bd53752`;
- Gateway command hash `cf91e215a19bf767791efc671479ba65db110894e5448e3c72218c99a40fbb77`;
- CNX-owned launcher/skill/plugin/state/runtime/scheduled-task/config surfaces absent.

## Phase A — fresh preflight, read-only

Before any installer mutation:

1. Fresh-fetch remote branch HEAD and prove `ACTIVE.md` / `STATUS.md` authorize Task 185.
2. Prove the Task-185 report path is absent.
3. Materialize a detached clean checkout of exact candidate `f6392da...` and independently verify its commit and facade SHA-256.
4. Fresh process scan must show no Task-184 cleanup/uninstall/lifecycle residue.
5. Re-prove the post-uninstall boundary:
   - `cnxclaw.cmd` absent;
   - CNX skill/extension/state/local-runtime roots absent;
   - CNX scheduled task absent;
   - CNX plugin registration/config reference absent.
6. Re-prove native OpenClaw version/Gateway health.
7. Re-prove Ollama health and freeze complete model inventory; it must still match the accepted Task-184 digest unless a clearly external user change is detected and reported before mutation.
8. Freeze unrelated plugin inventory excluding CNX and the Gateway command surface.

If process identity, uninstall convergence, candidate identity, or native/external preservation is ambiguous, publish a faithful `BLOCKED` report and invoke no installer.

## Phase B — exactly one supported fresh install

Only after every Phase-A gate passes, invoke exactly once:

`<detached-candidate>/scripts/install.ps1 -Workspace C:/Users/CDQ-P/.openclaw/workspace`

Use the repository-supported installer path. Do not supply runtime provider policy to the installer. Installer-owned internal lifecycle operations are authorized only within this one supported invocation.

Installer root invocation budget: `1`.

No retry is authorized for timeout, shell disconnect, missing outer watcher result, or partial evidence. Inspect the same invocation/process/evidence if supervision is interrupted.

## Phase C — post-install acceptance

PASS requires independent post-install proof of all of the following:

### Candidate identity / active chain

- workspace `cnxclaw.cmd` exists;
- launcher resolves through the owned runtime Python and installed `cnxclaw_v093.py` to the installed legacy facade;
- active installed `cnxclaw.py` SHA-256 is exactly `aa747f8f30080ef839a8d2cbf5758f9981a007ca01f41a988576f42edea8682f`;
- release remains `0.9.3`;
- plugin version/fingerprint match accepted provenance;
- plugin `cogentnexus-openclaw` is loaded and enabled.

### Ownership/runtime

- ownership status `OWNERSHIP_PRESENT`;
- legacy namespace entries `[]`;
- controller is `managed` and coherent;
- selected provider is `ollama`;
- provider transition is `null`;
- desired Gateway/provider state is running;
- Gateway loopback is healthy;
- Ollama is reachable/healthy/ready.

### Fresh durable state

Open SQLite read-only and require `PRAGMA integrity_check=ok`.

Fresh install must not manufacture semantic work. Require zero rows/items for reset-owned semantic/runtime history unless an installer-owned schema row is explicitly documented and non-semantic:

- `tickets = 0`
- `ticket_events = 0`
- `ticket_outbox = 0`
- `cnx_assistant_delivery = 0`
- `cnx_direct_model_call = 0`
- `cnx_direct_recovery = 0`
- `cnx_sessions = 0`

Require delivery/recovery read-only checks to report healthy/READY, pending outbox `0`, and no manufactured recovery incident.

### External preservation

- OpenClaw remains `2026.7.1-2 (0790d9f)`;
- Ollama model inventory remains byte/normalized-equivalent to the Phase-A freeze and the accepted Task-184 baseline unless a pre-mutation external change was explicitly detected;
- unrelated plugin inventory remains equivalent when CNX itself is excluded;
- Gateway command surface remains byte-identical to the accepted Task-184 baseline;
- no unrelated namespace/data removal or mutation is attributed to the installer.

## UI policy

No Dashboard/UI semantic action is required or authorized in Task 185.

For the later final Dashboard acceptance:

- the user controls New Session/navigation and UI clicks;
- the user focuses/selects the intended text field;
- Hermes may enter the test text only after that focus is established;
- Hermes must not press Send;
- the user presses Send exactly once;
- evidence collection then verifies Ticket/model/delivery multiplicity.

## Hard fence

```text
supported fresh-install root invocations: maximum 1
reset: 0
uninstall: 0
second install/retry: 0
executor-issued lifecycle helper outside installer: 0
manual Gateway/Ollama lifecycle action: 0
Dashboard Send/composer input/chat.inject: 0
model inference/recovery/regeneration: 0
manual DB/config/transcript/route repair: 0
source/product/test/workflow/dependency edits: 0
release/tag/merge/force push: 0
```

## Required report

Publish only:

`docs/operations/coordination/reports/CNX-20260831-185-hermes-fresh-reinstall-post-uninstall-reacceptance.md`

Include disposition, exact authority/candidate, installer invocation count/result, active-facade proof, ownership/runtime/plugin/provider health, SQLite/delivery/recovery state, external-preservation comparisons, complete anomalies/issues, hard-fence audit, Reviewer Verification Packet, and successor recommendation.

After report publication, stop for ChatGPT review. Final Dashboard semantic acceptance remains unauthorized until a later task.

## PASS label

`PASS — FRESH_REINSTALL_POST_UNINSTALL_CANDIDATE_REACCEPTED`
