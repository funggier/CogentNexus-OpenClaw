# CogentNexus Rotation Controller

OpenClaw tool plugin that admits obvious durable requests before conversational inference, starts owner-bound workflows, and bridges verified `ROTATE` handoffs to managed TaskFlow workers.

Safety properties:

- derives the owner session from trusted OpenClaw tool context;
- validates the handoff through the deterministic Python runtime;
- defaults to dry-run;
- rejects non-`ROTATE`, tampered, claimed, or completed handoffs;
- fences duplicate starts by task generation and deterministic run id;
- launches the worker without a visible console window on Windows.
- monitors bound durable tasks after successful owner turns and automatically rotates only verified `ROTATE` generations;
- records the worker as a managed TaskFlow child and schedules one compact verified-result turn back to the owner;
- exposes rotation state through `phase3.py context rotations` for one management surface.
- classifies explicit multi-phase, numerically constrained, interruption-sensitive requests before the selected conversational model runs;
- persists the original request, compiles bounded worker components plus deterministic assembly, and returns a workflow receipt immediately;
- detects software, EA/trading, file-management, analysis, fiction, design, and translation work and applies domain-specific specification, production, and QA components;
- compiles arbitrary safe relative artifact paths instead of depending on a travel-specific filename set, then validates artifact existence and supported formats externally;
- keeps worker capability choice per workflow instead of globally enabling lean mode;
- excludes internal continuation/subagent turns and supports the explicit `#cogent-direct` override;
- makes admission retries idempotent by run-derived task identity and trusted owner binding.

Temporary Codex/TaskFlow rotation is disabled by default. Normal durable work runs through the deterministic CogentNexus controller and Ollama directly. Set `autoRotate: true` only when an explicit clean-session Codex repair worker is required; bound context monitoring otherwise remains checkpoint/observation-only.

This keeps the normal execution path small and deterministic: `OpenClaw -> CogentNexus controller -> Ollama -> validator -> owner continuation`. It prevents temporary Codex workers from competing for CPU/RAM, inheriting inconsistent approval state, or becoming detached from a deleted owner session. Automatically admitted Ollama steps also use a 30-minute overall timeout, a 3-minute inactivity timeout, streamed progress checkpoints, and request-hash deduplication across sessions. Operators can terminate a durable workflow with `workflow.py cancel <task-id> --reason <reason>`; cancellation is recorded in the ledger, creates the owner completion notice, and is terminal to the supervisor.

Pre-inference durable admission is enabled by default. Configure `preInferenceAdmission: false` to disable it, `admissionMinimumScore` to tune the conservative deterministic threshold, or `durableWorkerModel` to select the Ollama worker model. These settings affect automatically admitted components only; they do not remove tools from the conversational agent or other workers.

### WebChat admission notice

On current OpenClaw releases, a successfully admitted request can be displayed
as:

> Your message could not be sent: CogentNexus admitted this as durable workflow
> ... (blocked by cogentnexus-rotation)

This wording does not by itself mean the workflow failed. Pre-inference
admission intentionally returns a `block` hook decision so the conversational
model does not also execute the same request. OpenClaw currently prefixes every
such decision with `Your message could not be sent`, even when the replacement
message is a successful durable-workflow receipt.

Use the workflow identifier in the notice to inspect
`.cogent/workflows/<id>/state.json`. A healthy admission has an owner-bound
state such as `running`; verified completion is delivered to the bound owner
session automatically. Treat the notice as a real failure only when the
workflow directory is absent or its durable state is `failed` or `blocked` with
corresponding evidence.

This is a presentation limitation at the OpenClaw hook/UI boundary. A future
OpenClaw `handled` or `accepted-without-inference` outcome would allow the same
safety behavior to render as a normal receipt instead of a warning.

Build and validate:

```bash
npm install
npm run plugin:build
npm run plugin:validate
npm test
```

Install from the plugin directory with `openclaw plugins install --link .`. A gateway restart is required after installation.
