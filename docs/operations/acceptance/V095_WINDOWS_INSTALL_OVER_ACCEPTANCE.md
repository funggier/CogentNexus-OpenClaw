# v0.9.5 Windows Install-Over Acceptance

## Purpose

Verify that the v0.9.4 Windows installation can be upgraded in place to the exact v0.9.5 candidate without losing durable CNX state, changing OpenClaw-owned provider/auth/model routing, or leaving an unbounded installation residue.

This document defines the acceptance protocol. It is not evidence that the install-over test has passed.

## Preconditions

- A known-good v0.9.4 installation is present on the target Windows machine.
- The target machine uses the same Windows account/context intended for the v0.9.5 installation.
- A controlled backup of the pre-upgrade workspace and CNX durable state is retained.
- The exact v0.9.5 candidate SHA and package artifact are recorded before installation.
- OpenClaw provider/model/auth configuration is recorded by identifiers only; do not copy secrets into the acceptance record.
- No public `v0.9.5` GitHub Release or tag is required for this test.

## Baseline capture

Record:

- v0.9.4 installed version and ownership manifest;
- target v0.9.5 candidate SHA;
- workspace and CNX state roots;
- plugin path and registration identity;
- OpenClaw state path and provider/auth/model identifiers;
- active session keys and generations required by the controlled test;
- durable Ticket count and representative Ticket IDs/statuses;
- pending delivery/recovery rows relevant to the test;
- installed launcher names and Task Service identities.

## Install-over sequence

1. Stop only the processes explicitly required by the v0.9.5 installer contract.
2. Preserve the v0.9.4 workspace and durable CNX state in place unless the installer transaction explicitly owns a path for replacement.
3. Install the exact v0.9.5 candidate using the supported Windows installer path.
4. Allow the installer transaction/rollback mechanism to complete before starting the upgraded runtime.
5. Verify the ownership manifest reports the new product version and the expected namespace.
6. Start OpenClaw Gateway and the upgraded CogentNexus-OpenClaw plugin/runtime.
7. Verify the pre-existing durable Ticket/session state is still readable and remains bound to the expected owner identity/generation.
8. Submit one controlled Direct request and one controlled Durable request.
9. Verify normal delivery and controlled recovery behavior using the exact post-upgrade session identity.

## Acceptance invariants

The test passes only when all applicable observations hold:

- the installed product identity remains `cogentnexus-openclaw`;
- the installed version is exactly `0.9.5`;
- no stale v0.9.4 plugin registration remains active alongside the replacement registration;
- the ownership manifest, plugin path, and launcher namespace are internally consistent;
- durable Ticket/session/delivery state from v0.9.4 remains readable after upgrade;
- pre-existing session generations are not incremented merely because an install-over occurred;
- OpenClaw provider/model/auth routing remains outside CNX migration authority;
- failed installation paths do not delete shared parent directories or unrelated application data;
- a successful upgrade leaves no unowned temporary transaction residue;
- the upgraded runtime can process both Direct and Durable requests under the expected ownership boundaries.

## Recovery and rollback evidence

For any simulated installer failure, retain the transaction marker before/after evidence and verify that rollback removes only marker-recorded owned paths. A markerless partial installation must not be silently adopted or broadly deleted.

## Failure classification

Classify observed failures precisely:

- **Migration-loss:** durable Ticket/session/delivery state is missing or changed unexpectedly.
- **Ownership drift:** provider/auth/model/Gateway state is mutated outside its OpenClaw owner.
- **Registration residue:** stale plugin or launcher registration remains active.
- **Rollback-boundary violation:** rollback deletes a shared/unowned path.
- **Lifecycle drift:** session generation changes without the required physical lifecycle boundary.
- **Evidence failure:** required exact candidate or pre/post state evidence is missing.

## Release gate

Windows install-over acceptance must be completed against the exact candidate after metadata consistency, behavior matrix, and source validation are green and before any public `v0.9.5` release/tag is published.
