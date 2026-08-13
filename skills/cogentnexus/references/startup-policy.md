# Startup policy

Machine startup is optional and independent from maintenance.

- enabled: install and reconcile the native hidden background supervisor.
- disabled: remove only CogentNexus-owned automatic triggers.
- unset: report choice-required; never silently enable.

Use `scripts/startup.py status|enable|disable|ensure`. Manual lifecycle start remains available in every policy state.

On Windows, least-privilege background operation uses Task Scheduler at user logon and `pythonw.exe`, preventing console flashes. True pre-login machine boot needs a separately provisioned service identity. Linux uses a systemd user timer. Other packaged adapters must preserve the same policy and evidence contract.

Disabling startup preserves workflows, checkpoints, ledgers, artifacts, configuration, providers, and manual launchers. GitHub updates must preserve the stored policy and run `ensure` only to reconcile that policy.
