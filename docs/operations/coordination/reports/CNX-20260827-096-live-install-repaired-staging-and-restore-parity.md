# CNX-20260827-096 — Live Install Repaired Dashboard Staging and Restore Parity

Result: `BLOCKED_OWNER_SURFACE_READINESS`

## Scope and one-shot fence

The exact supported normal install-over was invoked exactly once from implementation SHA `32212a4331e1f32b5a130bd30d271d4cbc56f6c1`. It exited `0`. No retry, second installer invocation, manual lifecycle repair, manual generation deletion/move, ownership rewrite, reset/uninstall/cleanup, direct SQLite mutation, provider/model/timeout change, direct Ollama/provider inference, semantic message, semantic nonce, merge, tag, release or force push was performed.

The one authorized live mutation occurred. All remaining checks were read-only.

## A1 — exact source and toolchain

- Exact deploy checkout: `32212a4331e1f32b5a130bd30d271d4cbc56f6c1`.
- Exact checkout was clean before installer execution.
- Windows: `10.0.19045.6466`.
- Windows PowerShell: `5.1.19041.6456`.
- Node/npm used by installer: Node `v24.18.0`, npm `11.16.0`.
- Candidate `npm ci --ignore-scripts` and `npm run plugin:validate` passed before classification.
- Candidate v2 fingerprint: `df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4`.
- Candidate canonical payload file count: `176`.

## A2/A3 — pre-mutation live proof

Read-only preflight showed a coherent current deployment:

- controller: `managed`, generation `18`, provider `ollama`, desired gateway/provider running;
- startup/Supervisor: installed, enabled, Ready;
- Gateway: healthy, loopback port `18789`, connectivity probe `ok`;
- SQLite integrity: `ok`;
- current canonical CogentNexus generation: exactly one valid registered generation;
- ownership manifest: present and bound to the current `g-7257c4555ca8ad21` plugin path;
- Ollama: healthy/ready, accepted inventory of 4 models, no direct model invocation;
- baseline ticket state: 1 failed retired Task-092 ticket, pending outbox 0.

Live pre-install v2 fingerprint was recomputed from the manifest-owned plugin:

```text
6a22a74c874b54468c02a5126a4c867af8a3afe33a15532afe8936e30e85e3fc
```

It differed from the candidate fingerprint.

The exact production classifier returned:

```json
{
  "mode": "upgrade",
  "pendingRollover": false,
  "pluginAlreadyExact": false
}
```

The exact production lifecycle resolver returned:

```json
{
  "mode": "upgrade",
  "pendingRollover": false,
  "pluginAlreadyExact": false,
  "skipPlugin": false,
  "installPlugin": true,
  "rolloverPlugin": true
}
```

The production installer boundary was inspected before mutation: package installation is under `installPlugin`, rollover is independently under `rolloverPlugin`, rollover is not nested under installation, and rollover precedes strict final plugin resolution.

## B — supported install-over

Invocation:

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Workspace C:\Users\CDQ-P\.openclaw\workspace -Provider ollama
```

- supported installer invocation count: `1`;
- retry count: `0`;
- exit status: `0`;
- installer output explicitly proved `npm pack`, installation from the produced npm-pack artifact, plugin disable during replacement, ownership-safe rollover, runtime provisioning, and final successful installation.

The installer output included:

```text
Installing ...openclaw-plugin-cogentnexus-openclaw-0.9.3.tgz into ...g-8e5adec878a7c4e3...
Installed plugin: cogentnexus-openclaw
Retired the exact prior plugin generation into the CogentNexus-OpenClaw backup boundary.
CogentNexus-OpenClaw v0.9.3 installation completed successfully (Ollama-only).
installer_exit=0
```

## C/D — post-install parity and health

Read-only post-install verification proved:

- final ownership manifest resolves to `g-8e5adec878a7c4e3`;
- final installed fingerprint equals candidate exactly:

```text
df2600da3ae78e1613793b4a7e5d1ebe61f66f71f0903e1d5d2cd5f0d5f4f4b4
```

- final payload file count: `176`;
- `namespace_ownership.py resolve-plugin`: returned the candidate root and exact fingerprint;
- `namespace_ownership.py verify`: passed;
- controller: `managed`, generation `24`, desired gateway/provider running, selected provider `ollama`;
- startup policy: enabled, Supervisor task Ready, enabled and hidden;
- Gateway: healthy, probe `ok`, listening on `127.0.0.1:18789`;
- SQLite integrity: `ok`;
- ticket count remained `1`, ticket outbox remained `0`;
- no semantic/provider tables were present in this schema beyond the existing ticket/ticket-event state;
- Ollama model inventory remained the accepted four-model set and no model was invoked;
- retired `g-7257c4555ca8ad21` generation was present under the reviewed application-data rollover backup boundary;
- no third CogentNexus payload generation was registered. An older `g-bbc979095f8845a1` project wrapper remains on disk but contains no CogentNexus plugin manifest/payload and was not manually removed because manual cleanup is forbidden.

The installer-owned backup boundary contained the retired prior generation:

```text
C:\Users\CDQ-P\AppData\Local\CogentNexus-OpenClaw\plugin-generation-rollover-backups\openclaw-plugin-cogentnexus-openclaw__openclaw-generation__g-7257c4555ca8ad21-20260827t071933627331z
```

## E — natural multi-tick proof

Five natural PT1M observations completed after restoration. Every sample showed:

```text
controller_mode=managed
generation=24
task=Ready
sqlite=ok
tickets=1
outbox=0
```

No semantic rows, outbox work, provider activity, generation churn, or recovery churn appeared. Machine-observable stability therefore passed the natural observation portion and produced:

```text
NO_FLASH_MULTI_TICK_REPROVEN
```

No visible flashing was reported during the observation window.

## F — Dashboard owner readiness blocker

The existing Firefox OpenClaw Control window remained at the Gateway Dashboard connection screen. It displayed:

```text
Could not connect
The browser could not complete the Gateway connection.
```

The operator entered a token in the UI, but the connection still did not complete. No token value was read, recorded, exposed, guessed, or re-entered by Hermes. No password or credential was requested from the operator in chat.

Because the authenticated owner/control surface could not be proven, the required readiness token could not be issued:

```text
DASHBOARD_OWNER_FRESH_SESSION_READY_NO_SEND
```

This is the decisive Task-096 blocker. No Send/New Chat control was exercised and no semantic/provider action occurred.

## Final disposition

The live repaired source was installed successfully and restored to MANAGED parity/health, but Task 096 cannot be accepted as ready for the semantic successor until authenticated Dashboard owner readiness is independently proven.

Task-092 retired evidence was not repaired or rewritten. No new Task-096 semantic/provider activity was created.

The successor gate remains closed. The next allowed result requires independent acceptance of:

```text
PASS_REPAIRED_STAGING_LIVE_INSTALLED_PARITY_READY
```

No final semantic attempt is authorized by this report.
