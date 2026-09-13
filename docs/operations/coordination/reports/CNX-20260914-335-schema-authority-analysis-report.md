# CNX-335 — Schema Authority Analysis

**Date:** 2026-09-14  
**Classification:** `ARCHITECTURE / COMPATIBILITY ANALYSIS`  
**Scope:** read-only, no source mutation  
**Baseline:** `v0.9.5 → 50be0b973c30fd8d1528aaac3497c0fc3b0b4d95`  
**Diagnostic anchor:** `ff6eae95 / fee65bd9` (CNX-334: `HOOK_NOT_REGISTERED`)

## 1. Question restatement

CNX-334 proved:

```
host controller.json schemaVersion = 2
v0.9.5 release entry hostPluginAuthority()
  accepts only schemaVersion = 1
→ authority rejected
→ legacyEntry.register() not called
→ before_agent_run not registered
→ TicketStore.accept() never called
```

CNX-335 must decide the correct compatibility contract for `v0.9.6` without turning the authority gate into `schemaVersion != 1 → accept`.

## 2. Who owns the controller schema contract

**Owner: Host canonical state.**

* Canonical definition: `skills/cogentnexus-openclaw/scripts/host_state_v095.py`
  * `default_state()` → `schemaVersion: 2`
  * `VALID_MODES = {"active","disabled","maintenance"}`
  * `migrate_v094_state()` is the authoritative translation.
  * `save_state()` persists only canonical fields via atomic replace.
* Compatibility façade: `skills/cogentnexus-openclaw/scripts/host.py`
  * Executes exact `host_legacy_v094.py` payload in its module namespace so existing overlays keep monkey-patching.
  * Replaces only `default_state / load_state / save_state / transition` with translation that derives legacy `mode` in-memory (`_compatibility_view`) and never restores provider authority fields (`desiredProvider`, `selectedProvider`, `providerTransition`, `providerSelection`).
  * `save_state()` forces `candidate["schemaVersion"] = 2` before persisting through `host_state_v095.save_state`.
* Consumer: `plugins/cogentnexus-openclaw/src/v091-release-entry.ts` (`hostPluginAuthority`) is a **consumer** that must track the canonical contract. Its current `v0.9.5` form is stale.

Live proof: `C:\Users\CDQ-P\.openclaw\workspace\.cogentnexus-openclaw\host\controller.json` is schema 2:

```json
{
  "cnxMode": "active",
  "desiredGateway": "running",
  "generation": 101,
  "managedLocalAdapters": {"ollama": "auto"},
  "providerOwnership": "openclaw",
  "schemaVersion": 2,
  "updatedAt": "2026-09-13T15:09:06.411038+00:00"
}
```

## 3. What schema 2 actually represents

Schema 2 is the **provider-independent Host authority** introduced for `v0.9.5`.

Intent: decouple CogentNexus authority from OpenClaw provider routing.

* `mode` (legacy `managed/passthrough/maintenance`) → `cnxMode` (`active/disabled/maintenance`)
  * `managed → active`, `passthrough → disabled` (conditional on `plugin_enabled` during migration), `maintenance → maintenance`
* Removal of provider authority from Host state: `desiredProvider`, `selectedProvider`, `providerTransition`, `providerSelection` are stripped in `_compatibility_view` and not persisted.
* Addition of authority-neutral fields: `providerOwnership: "openclaw"`, `managedLocalAdapters: {"ollama":"auto"}`, `desiredGateway` retained, `generation` retained.

Schema 2 therefore does **not** represent a breaking incompatible Host state; it represents the same authority semantics with provider routing removed from the Host contract.

## 4. Was schema 2 intentional, which release, which fields

* Intentional: yes, part of the `v0.9.5` Host decoupling series.
* Introducing commits:
  * `385a7c0f feat: add v0.9.5 host state migration` — adds `host_state_v095.py`
  * `e3b3c41c feat: bridge v0.9.5 host authority state` — replaces `host.py` with façade + translation, makes `default_state` return schema 2 via `_compatibility_view`
  * `432dbfaf fix: persist translated host state as schema2` — forces `schemaVersion = 2` after legacy translation so `host_state_v095` does not reinterpret an already-translated state
* Published `v0.9.5` tag `50be0b97` contains all three; the release candidate merge is `fc3f4bc0` (fix to accept canonical state in `checks.py`) and `2a1be3b5` (fix to accept canonical state in `scripts/install.ps1`).
* Fields delta (schema 1 → schema 2):

| Dimension | schema 1 | schema 2 |
|---|---|---|
| version | `schemaVersion: 1` | `schemaVersion: 2` |
| authority mode | `mode: managed/passthrough/maintenance` | `cnxMode: active/disabled/maintenance` |
| gateway | `desiredGateway` | `desiredGateway` (same) |
| provider | `desiredProvider/selectedProvider/providerTransition/providerSelection` present | removed; `providerOwnership: "openclaw"` + `managedLocalAdapters: {ollama:auto/disabled}` |
| generation | `generation` | `generation` |

## 5. Semantic compatibility

Semantics are **backward-compatible for authority decisions** when a translator is present:

* `active` ≡ `managed` → authorized (`managed` branch)
* `disabled` ≡ `passthrough` → authorized (`passthrough` branch, but providerMode kept independent per `v0.9.5` comment: `providerMode` is compatibility metadata, not a capability suppressor)
* `maintenance` ≡ `maintenance` → unauthorized
* Provider fields are irrelevant to authorization; their absence must not be treated as invalid.

Raw schema 2 without translation is **not** directly readable by the `v0.9.5` `hostPluginAuthority`, which checks `state.mode` and `state.schemaVersion === 1`. That is the defect: the consumer was not updated while the producer moved to canonical 2.

## 6. Decision for v0.9.6

Required invariant:

```
known compatible schema → authorized
unsupported/unknown     → fail closed
```

The correct `v0.9.6` policy is **(d) support a bounded compatibility set**, implemented as:

```
SUPPORTED_CONTROLLER_SCHEMA_VERSIONS = {1, 2}
```

with explicit translation, not `schemaVersion != 1 → accept`.

Rejected alternatives:

* *(a) accept schema 2 directly* without a bounded set would obscure the authority contract and invites future `schemaVersion: 3` to pass silently.
* *(b) normalize schema 2 to 1 on disk* would mutate canonical state and contradict `host_state_v095` which is the owner; `host.py:save_state` already canonicalizes to 2.
* *(c) migrate schema 2 on read* is already done by `host.py`; the plugin must not re-migrate on disk. It should translate in-memory.
* *(e) reject schema 2 and repair controller generation* would revert the intentional `v0.9.5` provider-decoupling and discard the canonical `controller.json` already at generation 101.

Therefore `v0.9.6` must:

* accept `schemaVersion: 1` with legacy `mode` validation exactly as before;
* accept `schemaVersion: 2` with canonical `cnxMode` validation via the same mapping `host.py` uses (`active→managed`, `disabled→passthrough`, `maintenance→maintenance`);
* derive `mode` internally so downstream `authority.reason`/`authority.mode` keep the legacy vocabulary (`managed/passthrough/maintenance`) without persisting it;
* fail closed for every other case.

## 7. Canonical authority source

* **Persistence authority:** `host_state_v095.py` (`save_state` / `migrate_v094_state` / `load_state`).
* **Compatibility authority:** `host.py` (`_CANONICAL_TO_LEGACY_MODE`, `_LEGACY_TO_CANONICAL_MODE`, `_compatibility_view`).
* **Install-time authority:** `scripts/install.ps1:Get-ExistingCnxMode` already mirrors this (commit `2a1be3b5`: if `mode` missing, derive from `cnxMode`).
* **System-check authority:** `skills/.../scripts/checks.py:read_state` after `fc3f4bc0` derives `mode` from `cnxMode` before validating.

The plugin is the **only** authority consumer that was left behind. Evidence: `checks.py` and `install.ps1` were patched to understand canonical state before the `v0.9.5` merge, but `v091-release-entry.ts:hostPluginAuthority` at tag `50be0b97` still checks `state.schemaVersion !== 1`.

## 8. Expected behavior matrix

`hostPluginAuthority` after `v0.9.6` must behave:

| Controller file | Expected |
|---|---|
| `schemaVersion:1, mode:managed, generation:N` | `authorized:true, reason:managed` |
| `schemaVersion:1, mode:passthrough` | `authorized:true, reason:passthrough` |
| `schemaVersion:1, mode:maintenance` | `authorized:false, reason:maintenance` |
| `schemaVersion:2, cnxMode:active` | `authorized:true, reason:managed` (derived) |
| `schemaVersion:2, cnxMode:disabled` | `authorized:true, reason:passthrough` (derived) |
| `schemaVersion:2, cnxMode:maintenance` | `authorized:false, reason:maintenance` |
| `schemaVersion:3` (future) | `authorized:false, reason:invalid, fail closed` |
| `schemaVersion: missing` | `authorized:false, reason:invalid` |
| `schemaVersion: "2"` (malformed string) | `authorized:false, reason:invalid` |
| `cnxMode: "active"` with `schemaVersion:999` | `authorized:false, reason:invalid` |
| `schemaVersion:2` but `cnxMode` missing/invalid | `authorized:false, reason:invalid` |
| unreadable JSON | `authorized:false, reason:invalid` |
| missing file | `authorized:false, reason:missing` |

No warning-only path. No `schemaVersion != 1 → accept`.

## 9. Registration invariant

```
authorized   → legacyEntry.register(runtimeApi) called
             → api.on("before_agent_run", ...) reachable
             → TicketStore.accept achievable
unauthorized → registration suppressed, no partial hooks
```

`v0.9.6` must not change this shape; it only widens the set of authorized schemas.

## 10. Required compatibility design (answers to §6 of handoff)

Explicit policy for `v0.9.6`:

```ts
const SUPPORTED_CONTROLLER_SCHEMA_VERSIONS = new Set([1, 2] as const);
const CANONICAL_TO_LEGACY_MODE: Record<string, string> = {
  active: "managed",
  disabled: "passthrough",
  maintenance: "maintenance",
};
```

* Exactly supported: `1` (legacy) and `2` (canonical `v0.9.5`). Rationale: `1` preserves valid historical controller files; `2` is the intentional `v0.9.5` canonical form already persisted at generation 101.
* Semantic compatibility: legacy `mode` and canonical `cnxMode` map one-to-one as above; `maintenance` remains unauthorized; `active/disabled` remain authorized.
* Invalid values: any `schemaVersion` not in the set → `invalid`, fail closed. Any `mode/cnxMode` not in the valid sets → `invalid`, fail closed.
* Future schemas: unknown `schemaVersion` → `invalid`, fail closed, never auto-accepted. Adding `3` requires an explicit code change adding it to the set with documented semantics.
* Migration: none required on disk. Plugin translates in-memory; `host_state_v095.migrate_v094_state` already handles on-disk migration. Controller files remain versioned independently from plugin releases, with the Host state module as owner.
* Independence: controller schema versions are not tied 1:1 to plugin versions; the plugin declares which controller schemas it understands via the bounded set.

## 11. Backward compatibility & safety

* Preserve support for schema 1 so downgraded or unmigrated controllers remain valid.
* Unknown/future/malformed schemas fail closed — no inference, no Ticket, no delivery. This is the correct defense.
* Do not convert the gate into `if (mode) accept`. Schema version is part of the authority proof.

## 12. Evidence referenced

* Tag `50be0b97:plugins/.../v091-release-entry.ts` — `hostPluginAuthority` checks `state.schemaVersion !== 1`.
* Tag `50be0b97:skills/.../host_state_v095.py` — `VALID_MODES`, `migrate_v094_state`, `schemaVersion:2`.
* Tag `50be0b97:skills/.../host.py` — façade, `_CANONICAL_TO_LEGACY_MODE`, forced `schemaVersion=2` on save.
* Live `controller.json` — schema 2, `cnxMode:active`, generation 101.
* Commits `e3b3c41c`, `432dbfaf`, `fc3f4bc0`, `2a1be3b5` — show provider-decoupling was intentional and that other consumers were updated while the plugin entry was missed.

## 13. CNX-336 repair direction

Minimal repair is a single boundary change in `plugins/cogentnexus-openclaw/src/v091-release-entry.ts`:

* Extend `HostControllerState` with `cnxMode?: string`.
* Introduce `SUPPORTED_CONTROLLER_SCHEMA_VERSIONS = [1, 2]` and `CANONICAL_TO_LEGACY_MODE` matching `host.py`.
* In `hostPluginAuthority`, branch on `schemaVersion`:
  * `1` → validate `mode` as today.
  * `2` → validate `cnxMode`, derive `mode`, then apply the same managed/passthrough/maintenance authorization.
  * anything else → `invalid`, fail closed.
* Keep all downstream logic (`authority.reason` mapping to `providerMode`, `installV099NativeRestartOwnershipFence`, `legacyEntry.register`) unchanged.

No TicketStore, Dashboard, provider, or timeout changes. Add tests for the matrix in §8 before merging.

## 14. Safety statement

No source, configuration, model, provider, timeout, SQLite, or release/tag mutation was performed in CNX-335. This report is read-only analysis.

