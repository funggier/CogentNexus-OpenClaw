# Runtime Lifecycle

Lifecycle control exists to distinguish **operator intent** from **runtime failure**.

Current Host-level modes are:

- **MANAGED** — desired managed runtime is active; unplanned failure may be reconciled.
- **PASSTHROUGH** — CogentNexus relinquishes interception/background ownership; native OpenClaw owns its lifecycle.
- **MAINTENANCE** — deliberate managed stop; supervisor must not restart the runtime against operator intent.

## Preferred operator surface

Use the Host Controller launcher when installed:

```text
cnx status
cnx start
cnx stop
cnx restart
cnx gateway start
cnx gateway stop
cnx gateway restart
cnx disable
cnx enable
```

Semantics:

- `start` -> persist MANAGED/running intent, start/reconcile provider + Gateway, verify health, resume eligible committed work.
- `stop` -> persist MAINTENANCE/stopped intent before stopping managed components.
- `restart` -> keep MANAGED/running intent, write recoverable lifecycle state, restart, verify, then resume eligible work.
- `disable` -> persist PASSTHROUGH, disable CogentNexus interception/startup ownership, remove managed policy, keep native OpenClaw usable.
- `enable` -> persist MANAGED/running, restore policy/plugin/startup ownership, reconcile runtime.

Gateway-only commands change Gateway lifecycle while preserving the current Host ownership semantics.

## Low-level runtime commands

The underlying deterministic runtime remains available for adapters/tests:

```text
python skills/cogentnexus/scripts/runtime.py lifecycle status
python skills/cogentnexus/scripts/runtime.py lifecycle prepare --reason "planned shutdown"
python skills/cogentnexus/scripts/runtime.py lifecycle stop --provider
python skills/cogentnexus/scripts/runtime.py lifecycle restart --reason "configuration reload"
python skills/cogentnexus/scripts/runtime.py lifecycle start --provider
python skills/cogentnexus/scripts/runtime.py lifecycle cancel
```

Normal users should prefer `cnx` because Host state and runtime lifecycle state must stay aligned.

## Recovery rules

- Persist desired state **before** destructive lifecycle action.
- MAINTENANCE is authoritative: periodic supervision returns without restarting managed services.
- A recoverable restart marker may be cleared only after required health probes pass.
- Provider/Gateway warm-up uses bounded readiness polling.
- Cloud providers are never stopped as local processes.
- Managed Ollama lifecycle uses the supported platform adapter.
- Do not duplicate external side effects merely because lifecycle recovery occurred.
- When a response is already durable, retry delivery rather than model execution.

For planned machine shutdown, use `cnx stop` when you want the next state to remain intentionally stopped. If you want CogentNexus to resume managed operation after the next normal login/boot, leave Host desired state MANAGED/running and rely on the configured startup supervisor.
