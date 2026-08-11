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
- keeps worker capability choice per workflow instead of globally enabling lean mode;
- excludes internal continuation/subagent turns and supports the explicit `#cogent-direct` override;
- makes admission retries idempotent by run-derived task identity and trusted owner binding.

Automatic rotation is enabled by default and applies only to tasks explicitly bound with `phase3.py context bind`. Set `autoRotate: false` in plugin config for observation/manual-tool mode.

Pre-inference durable admission is enabled by default. Configure `preInferenceAdmission: false` to disable it, `admissionMinimumScore` to tune the conservative deterministic threshold, or `durableWorkerModel` to select the Ollama worker model. These settings affect automatically admitted components only; they do not remove tools from the conversational agent or other workers.

Build and validate:

```bash
npm install
npm run plugin:build
npm run plugin:validate
npm test
```

Install from the plugin directory with `openclaw plugins install --link .`. A gateway restart is required after installation.
