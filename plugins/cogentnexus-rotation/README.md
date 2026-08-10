# CogentNexus Rotation Controller

OpenClaw tool plugin that bridges a verified CogentNexus `ROTATE` handoff to a managed TaskFlow and a fresh background agent session.

Safety properties:

- derives the owner session from trusted OpenClaw tool context;
- validates the handoff through the deterministic Python runtime;
- defaults to dry-run;
- rejects non-`ROTATE`, tampered, claimed, or completed handoffs;
- fences duplicate starts by task generation and deterministic run id;
- launches the worker without a visible console window on Windows.

Build and validate:

```bash
npm install
npm run plugin:build
npm run plugin:validate
npm test
```

Install from the plugin directory with `openclaw plugins install --link .`. A gateway restart is required after installation.
