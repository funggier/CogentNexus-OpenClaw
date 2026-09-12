# v0.9.5 Windows Install-Over Acceptance

## Purpose

Prove that a v0.9.4 installation can be upgraded in place to the exact v0.9.5 candidate without changing OpenClaw-owned routing/auth/model configuration and without losing CNX durable identity or continuity state.

This procedure is intentionally separate from automated migration tests: it validates the real supported Windows installation lifecycle.

## Preconditions

- Freeze one exact candidate SHA before installation.
- Start from a known-good v0.9.4 installation.
- Use the supported release-equivalent installer/staging path; do not manually copy selected files.
- Keep secrets out of all evidence.
- Record the candidate SHA and pre-install fingerprints before any mutation.

## Pre-install snapshot

Capture non-secret evidence for:

```text
installed CNX version
installed CNX/plugin fingerprint
OpenClaw provider/model route
hashes or selected non-secret route/auth fields
CNX controller mode and generation
Ticket/session/delivery counts and target identities
Gateway lifecycle state
Ollama process state
```

The purpose of this snapshot is comparison, not migration of user-owned configuration.

## Install-over

Install the exact candidate using the supported Windows install-over mechanism.

The installer must remain transactional: a failed upgrade must not silently adopt unrelated residue, and rollback authority must remain bounded to installer-owned transaction paths.

## Required migration checks

After installation, verify:

1. v0.9.4 managed state becomes the intended active v0.9.5 state.
2. v0.9.4 cloud-pass-through with plugin enabled becomes active CNX state.
3. OpenClaw-owned provider/model/auth routing is unchanged.
4. Ticket IDs, run IDs, session keys/generations, and pending delivery identity remain valid.
5. Installed files and plugin payload correspond to the exact candidate SHA/fingerprint.
6. No legacy generic CNX launcher or obsolete product identity becomes the active entry point.

## Disable parity

Run the supported disable operation (for current OpenClaw integration, `cnxclaw disable`) and prove:

```text
CNX no longer intercepts new turns
OpenClaw continues through its native path
provider/model selection remains OpenClaw-owned
Gateway remains operational unless OpenClaw itself requires a lifecycle change
```

## Re-enable parity

Run the supported enable/start operation and verify:

```text
CNX becomes active without selecting a provider/model
existing OpenClaw route remains authoritative
plugin is enabled and resolved under the current namespace
CNX session/ticket continuity is restored without identity duplication
```

## Failure handling

Any failure in installation, migration, disable parity, re-enable behavior, file identity, or durable-state preservation blocks the release. Repairing the candidate creates a new candidate SHA and restarts exact-candidate verification.

## Evidence handling

Record runtime results in a coordination/acceptance report tied to the exact candidate SHA. Never commit secrets, API credentials, tokens, cookies, or unrestricted authentication configuration.
