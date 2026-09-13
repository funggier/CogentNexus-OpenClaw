# CNX-20260914-336 — v0.9.6 Schema Authority Compatibility Repair Report

**Date:** 2026-09-14 05:07 UTC (22:07 UTC prior query, 05:07 SEAST local)  
**Task:** CNX-336  
**Status:** `PASS — repair implemented, verified, report published`  
**Release target:** `v0.9.6`  
**Baseline fence:** `v0.9.5` tag `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95` — **untouched**  
**Branch:** `agent/v0.9.6-schema-authority-repair`  
**Fix commit:** `3efb971eeed55f0d48908281974577fdbed48612`  
**Authority:** local repair on Hermes (ChatGPT handoff CNX-335 + CNX-336 spec)

---

## 1. Exact Source Commit Under Repair

* Published baseline: `v0.9.5` (`50be0b973c30fd8d1528aaac3497c0fc3b0b4d95`, refs/tags/v0.9.5)
* Parent of fix: `979869983d693544541661ba7c8229dcecb9dc0b` (docs: CNX-335 analysis) → `ff6eae95` (CNX-334 diagnostic)
* Fix commit: `3efb971eeed55f0d48908281974577fdbed48612` — `fix(plugin): add bounded schema 2 authority compatibility (CNX-336)`
* Tag verification (evidence, 2026-09-13T22:07:07Z):

```
50be0b973c30fd8d1528aaac3497c0fc3b0b4d95 refs/tags/v0.9.5
50be0b973c30fd8d1528aaac3497c0fc3b0b4d95 (HEAD~2, confirmed cat-file tree b1b4287...)
```

* No tag force-push, no release mutation, no merge yet. `git show-ref --tags | grep v0.9.5` unchanged.

---

## 2. Proven Defect (Before)

`plugins/cogentnexus-openclaw/src/v091-release-entry.ts` at `50be0b97`:

```ts
if (state?.schemaVersion !== 1 || !["managed","passthrough","maintenance"].includes(mode ?? "")) {
  return { authorized: false, reason: "invalid", mode, generation, controllerPath };
}
```

* Host canonical producer `skills/cogentnexus-openclaw/scripts/host_state_v095.py` persists `schemaVersion: 2` with `cnxMode: active|disabled|maintenance` (provider-independent design).
* Compatibility façade `skills/.../host.py` already translates `cnxMode → mode` in-memory (`active→managed`, `disabled→passthrough`), forces `schemaVersion=2` on save, and strips provider fields. Other consumers (`skills/.../scripts/checks.py` at `fc3f4bc0`, `scripts/install.ps1` at `2a1be3b5`) were updated.
* Live `~/.openclaw/workspace/.cogentnexus-openclaw/host/controller.json` at generation 101 is schema 2:

```json
{ "cnxMode":"active","desiredGateway":"running","generation":101,"managedLocalAdapters":{"ollama":"auto"},"providerOwnership":"openclaw","schemaVersion":2,"updatedAt":"2026-09-13T15:09:06.411038+00:00" }
```

* Consumer `hostPluginAuthority()` rejected schema 2 → `authorized=false` → `legacyEntry.register(runtimeApi)` never called → `api.on("before_agent_run", …)` never registered → `TicketStore.accept()` unavailable (CNX-334 `HOOK_NOT_REGISTERED`).

---

## 3. Required Compatibility Policy (After)

Bounded set, no permissive fallback:

```ts
const SUPPORTED_CONTROLLER_SCHEMA_VERSIONS = new Set<number>([1, 2]);

const CANONICAL_TO_LEGACY_MODE: Record<string, string> = {
  active: "managed",
  disabled: "passthrough",
  maintenance: "maintenance",
};
```

* `schemaVersion` type-strict: `typeof === "number" && Number.isInteger && Set.has` — string `"2"`, `null`, missing, `3`, `99`, `1.5` all → `invalid`, fail closed.
* Branch by version:

| schema | input | derived `mode` | decision |
|---|---|---|---|
| 1 | `mode=managed` | `managed` | `authorized=true reason=managed` |
| 1 | `mode=passthrough` | `passthrough` | `authorized=true reason=passthrough` |
| 1 | `mode=maintenance` | `maintenance` | `authorized=false reason=maintenance` |
| 2 | `cnxMode=active` | `managed` | `authorized=true reason=managed` |
| 2 | `cnxMode=disabled` | `passthrough` | `authorized=true reason=passthrough` |
| 2 | `cnxMode=maintenance` | `maintenance` | `authorized=false reason=maintenance` |

* Invalid/future branch (`3`, `99`, missing, `"2"`, `null`, missing/invalid `cnxMode`, unreadable JSON, missing file) → `authorized=false reason=invalid` (or `missing` for ENOENT), no partial hook.

* Translation is in-memory only; no write-back of legacy `mode`, no mutation of canonical Host state, no provider/timeout change, no TicketStore/Dashboard/transport change. Registration sequence preserved exactly:

```
authorized → hostPluginAuthority true → legacyEntry.register(runtimeApi) → api.on("before_agent_run",…) → managed guards installed
unauthorized → registration suppressed → no partial hook
```

---

## 4. Before/After Authority Behaviour

| Input | Before (v0.9.5) | After (v0.9.6 fix) |
|---|---|---|
| `schemaVersion:1 mode:managed` | PASS authorized | PASS authorized |
| `schemaVersion:1 mode:passthrough` | PASS authorized | PASS authorized |
| `schemaVersion:1 mode:maintenance` | denied maintenance | denied maintenance |
| `schemaVersion:2 cnxMode:active` | **FAIL — invalid, suppressed** | **PASS authorized managed** |
| `schemaVersion:2 cnxMode:disabled` | **FAIL — invalid, suppressed** | **PASS authorized passthrough** |
| `schemaVersion:2 cnxMode:maintenance` | **FAIL — invalid** | denied maintenance |
| `schemaVersion:3` | denied invalid | denied invalid |
| `schemaVersion:99` | denied invalid | denied invalid |
| `schemaVersion missing` | denied invalid | denied invalid |
| `schemaVersion "2"` (string) | denied invalid (type) | denied invalid |
| `schemaVersion null` | denied invalid | denied invalid |
| `schemaVersion 2 missing cnxMode` | denied invalid (mode undefined) | denied invalid |
| `schemaVersion 2 invalid cnxMode` | denied invalid | denied invalid |
| unreadable JSON | denied invalid | denied invalid |
| missing file | denied missing | denied missing |

Fix widens authorized set only for known-compatible schema 2, via explicit canonical translation matching `host.py:_CANONICAL_TO_LEGACY_MODE`. Unknown/future remains fail-closed.

---

## 5. Compatibility Matrix (Source of Truth)

Canonical semantic mapping (per CNX-335 and `host.py`):

```
schema 2: active → managed, disabled → passthrough, maintenance → maintenance
```

Downstream equivalence proven:

* `v1 managed` ≡ `v2 active` → `authorized:true reason:managed mode:managed`
* `v1 passthrough` ≡ `v2 disabled` → `authorized:true reason:passthrough mode:passthrough`

No providerMode suppression: both paths set `providerMode=undefined` for passthrough branch, `providerMode="managed"` otherwise, preserving existing capability.

---

## 6. Minimal Source Scope

*Primary source changed:*

`plugins/cogentnexus-openclaw/src/v091-release-entry.ts` — blob `fb51fbbbd62bb75261e221cd9d4f139be90e803b`

* Diff vs `v0.9.5` (33 insertions, 7 deletions):

```diff
-type HostControllerState = { schemaVersion?: number; mode?: string; generation?: number; }
+type HostControllerState = { schemaVersion?: unknown; mode?: string; cnxMode?: string; generation?: number; }
+const SUPPORTED_CONTROLLER_SCHEMA_VERSIONS = new Set<number>([1, 2]);
+const CANONICAL_TO_LEGACY_MODE = { active:"managed", disabled:"passthrough", maintenance:"maintenance" };
-export function hostPluginAuthority(...) {
-  const mode = typeof state?.mode === "string" ? state.mode : undefined;
-  if (state?.schemaVersion !== 1 || !["managed",...].includes(mode ?? "")) return {invalid};
+  const generation = Number.isSafeInteger(state?.generation) ? ...
+  const rawSchemaVersion = state?.schemaVersion;
+  if (typeof rawSchemaVersion !== "number" || !Number.isInteger(rawSchemaVersion) || !SUPPORTED.has(rawSchemaVersion)) return {invalid};
+  if (rawSchemaVersion === 1) { /* preserve existing schema-1 semantics exactly */ }
+  // schemaVersion === 2 — canonical v0.9.5 authority
+  const cnxMode = typeof state?.cnxMode === "string" ? ... : undefined;
+  const derived = cnxMode !== undefined ? CANONICAL_TO_LEGACY_MODE[cnxMode] : undefined;
+  if (derived === undefined) return {invalid};
+  const mode = derived;
+  if (mode === "managed" || mode === "passthrough") return {authorized true};
+  if (mode === "maintenance") return {authorized false maintenance};
```

*Tests added (not source scope):*

`plugins/cogentnexus-openclaw/src/cnx336-schema-authority.test.ts` — blob `b1d7d26973e99570ba13afdba14141f96d6dcfe4` (325 lines, 27 tests)

*Unchanged by design (verified via `git diff --stat HEAD`):*

TicketStore, Dashboard code, provider transport, timeout values, `host_state_v095.py`, `host.py`, SQLite schema, recovery/delivery architecture, `openclaw.plugin.json`, `package.json`, `VERSION`.

*No unrelated file changes in commit:*

```
2 files changed, 358 insertions(+), 7 deletions(-)
 plugins/cogentnexus-openclaw/src/cnx336-schema-authority.test.ts | 325 +++
 plugins/cogentnexus-openclaw/src/v091-release-entry.ts           |  40 ++-
```

Untracked files left **not staged** (pre-existing stray, not part of commit, verified `git status -sb`):

```
?? docs/operations/coordination/reports/CNX-20260910-repair-checkpoint-final.md
?? docs/operations/coordination/reports/CNX-20260914-331-web-session-qwen38-final-acceptance-report.md
?? plugins/cogentnexus-openclaw/src/v090-reproducer.test.ts
```

`dist/` is gitignored and not committed; it is reproduced via build.

---

## 7. Tests Executed

### 7.1 Targeted (CNX-336 matrix)

```
npm test -- src/cnx336-schema-authority.test.ts
  ✓ src/cnx336-schema-authority.test.ts (27 tests) 314ms
  Test Files 1 passed (1) / Tests 27 passed (27)
```

Coverage:

* Authority matrix: 16 cases (v1 managed/passthrough/maintenance, v2 active/disabled/maintenance, v3, v99, missing version, string "2", null, v2 missing cnxMode, v2 invalid, unreadable, missing, no-mutate).
* Registration: valid v1, valid v2 active, valid v2 disabled, invalid/future bulk, maintenance both schemas, unreadable, missing.
* Downstream equivalence: v1 managed ≡ v2 active, v1 passthrough ≡ v2 disabled, generation preserved, future schema never accepted.

### 7.2 Complete relevant test suite

```
npm test (plugins/cogentnexus-openclaw, vitest.config.ts, testTimeout 60s on win32)

  ✓ 77 test files passed
  ✓ 366 tests passed
  Duration 49.97s (transform 626ms, collect 19.57s, tests 18.24s)
```

Key suites confirming retention:

* `v091-host-authority.test.ts` — 5 passed (schema-1 compatibility retained)
* `v091-wiring.test.ts` — 5 passed
* `ticket-store.test.ts`, `ticket-runtime.test.ts`, `delivery-continuity`, `v095-*`, etc. — all green

No failing tests; no skipped gate ignored.

---

## 8. Registration Test Evidence

Validated via both vitest and controlled-dist runtime probe (see §9).

Vitest extracts (from `cnx336-schema-authority.test.ts`):

* `valid v1 registers hooks` — `api.on` called, no suppression log
* `valid v2 registers hooks` — same for `schemaVersion:2 cnxMode:active` and `disabled`
* `invalid/future schema registers nothing` — for 6 payloads (`3`, `99`, `"2"`, `bogus`, missing, no version) `api.on` not called, `registerService` not called, `logger.info` contains `registration suppressed`, **no partial hook**
* `maintenance suppresses` — both schemas

Dist probe evidence (node import of `dist/v091-release-entry.js`, sha `c15b2f61…`):

```
schema2 active: authorized=true reason=managed mode=managed gen=101 → registration onCalled=true suppressed=false
schema2 disabled: authorized=true reason=passthrough mode=passthrough gen=102 → onCalled=true suppressed=false
schema2 maintenance: authorized=false reason=maintenance mode=maintenance gen=103 → onCalled=false suppressed=true
schema1 managed: authorized=true reason=managed → onCalled=true
schema1 passthrough: authorized=true reason=passthrough → onCalled=true
schema3 future: authorized=false reason=invalid mode=undefined gen=106 → onCalled=false suppressed=true
schema2 missing cnxMode: authorized=false reason=invalid → onCalled=false suppressed=true
schema2 invalid cnxMode: authorized=false reason=invalid → onCalled=false suppressed=true
string version: authorized=false reason=invalid → onCalled=false suppressed=true
missing file: authorized=false reason=missing → onCalled=false (suppressed)
```

`before_agent_run` registration proven:

```
events=[ "before_agent_run", "before_agent_run", "before_message_write", "reply_payload_sending", … ]
includes before_agent_run=true
```

In-memory translation check: file content before/after `hostPluginAuthority` identical, no `mode` added to disk for schema-2 payload.

---

## 9. Runtime Verification (Controlled Installation)

*No Dashboard traffic sent* — per CNX-336 fence.

Procedure: `mkdtemp` workspace with controller.json, import `dist/v091-release-entry.js`, call `hostPluginAuthority`, then `entry.register` with fake `OpenClawPluginApi` capturing `api.on` names.

Required evidence (met):

```
plugin loaded               → PASS (dist import succeeded, entry.id=cogentnexus-openclaw)
plugin enabled              → PASS (Host authority authorized=true for valid schema)
controller schema = 2       → PASS (schemaVersion:2 cnxMode:active, generation 101/200)
hostPluginAuthority = authorized → PASS (managed)
registration succeeds       → PASS (legacyEntry.register called, managed guards installed)
before_agent_run registered → PASS (events includes before_agent_run)
```

The same probe also confirms fail-closed for every invalid/future/malformed case (see §8). No Dashboard `TicketStore.accept` was invoked; acceptance remains a separate task boundary.

---

## 10. Build Verification

```
npm run build → tsc -p tsconfig.json && node ./scripts/canonicalize-dist.mjs --dist-root ./dist → canonicalized 50 dist text files to LF
npm run plugin:build → build + node ./scripts/verify-v091-schema.mjs
  → CogentNexus-OpenClaw mixed-plugin artifact verification: PASS (46 config properties, 5 tools)
```

*No TS errors, no schema drift.*

**Artifact:**

* File: `plugins/cogentnexus-openclaw/dist/v091-release-entry.js`
* Size: 10 121 bytes, 199 lines
* Git blob (src): `fb51fbbbd62bb75261e221cd9d4f139be90e803b`
* SHA-256 (dist JS): `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8`
* Artifact check:

```
grep -n SUPPORTED_CONTROLLER_SCHEMA_VERSIONS dist/v091-release-entry.js → 15: const SUPPORTED_CONTROLLER_SCHEMA_VERSIONS = new Set([1, 2]);
grep -n CANONICAL_TO_LEGACY_MODE → 16: const CANONICAL_TO_LEGACY_MODE = { active:"managed", disabled:"passthrough", maintenance:"maintenance" };
```

---

## 11. Regression Guard

Retained:

* Fail-closed unknown schema — strict `Set([1,2])` gate, no `!==1` permissive fallback, no warning-only path.
* Schema 1 compatibility — exact prior semantics preserved (managed/passthrough authorized, maintenance denied, invalid → invalid).
* Schema 2 canonical compatibility — via `active→managed` etc., matching `host.py`.
* Authority reason mapping — `managed`/`passthrough`/`maintenance`/`missing`/`invalid` unchanged for downstream `providerMode` handling.
* Installation/ownership fences — not touched (`installV099NativeRestart…`, delivery fences).
* Ticket-first admission — not touched; guard is registration-level only.
* No model/provider/timeout/SQLite/recovery/delivery mutation.

---

## 12. Release/Branch Policy

* Branch: `agent/v0.9.6-schema-authority-repair` (created 2026-09-14 from `97986998`, ahead of `v0.9.5` only by docs + fix)
* Head: `3efb971eeed55f0d48908281974577fdbed48612`
* Log `v0.9.5..HEAD`: `3efb971e` + `97986998` (CNX-335) + `ff6eae95` (CNX-334) — no other commits
* Diff `v0.9.5` stat shows only expected docs plus `src/v091-release-entry.ts` (+ fix) — no tag history rewrite
* Verification steps before branch: `git rev-parse v0.9.5` → `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95`, `show-ref --tags` confirms same
* No force-push, no release creation, no tag creation, no merge until independent review — as required

Working tree after fix commit: `??` only stray pre-existing files (see §6); staged diff is empty.

---

## 13. Changed Files (Committed)

```
commit 3efb971eeed55f0d48908281974577fdbed48612
Author: KITTIWAT KITIKUN <funggier@gmail.com>
Date:   Mon Sep 14 05:06:57 +0700

    fix(plugin): add bounded schema 2 authority compatibility (CNX-336)

plugins/cogentnexus-openclaw/src/cnx336-schema-authority.test.ts  | 325 +++
plugins/cogentnexus-openclaw/src/v091-release-entry.ts            |  40 ++-
```

*Exact blob state at HEAD:*

* `plugins/cogentnexus-openclaw/src/v091-release-entry.ts` → `fb51fbbbd62bb75261e221cd9d4f139be90e803b`
* `plugins/cogentnexus-openclaw/src/cnx336-schema-authority.test.ts` → `b1d7d26973e99570ba13afdba14141f96d6dcfe4`
* Dist artifact not versioned: `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8 *dist/v091-release-entry.js`

Do NOT modify, move, rewrite, or force-push `v0.9.5` — enforced and verified.

---

## 14. Explicit Immutability Statement

**`v0.9.5` tag and release were untouched.** Verified:

```
$ git rev-parse v0.9.5
50be0b973c30fd8d1528aaac3497c0fc3b0b4d95
$ git show-ref --tags | grep v0.9.5
50be0b973c30fd8d1528aaac3497c0fc3b0b4d95 refs/tags/v0.9.5
$ git cat-file -p v0.9.5 | head
tree b1b428718f9e6c8f5a271a385e1021f2efc75d1d
```

No new tag was created, no release was published, no force-push occurred. Fix lives solely on `agent/v0.9.6-schema-authority-repair` branch.

---

## 15. Success Criteria (CNX-336)

```
schema 1 valid      → PASS (managed/passthrough authorized, maintenance denied)
schema 2 valid      → PASS (active→managed, disabled→passthrough authorized)
unknown schema      → FAIL CLOSED (3,99 → invalid)
malformed schema    → FAIL CLOSED (string "2", null, missing, invalid cnxMode, unreadable, missing file)
registration v2     → PASS (hooks registered, no suppression)
before_agent_run    → registered (events includes before_agent_run)
tests               → PASS (27 targeted + 366 full, 77 files)
build               → PASS (tsc + verify-v091-schema PASS, 50 files canonicalized)
v0.9.5 immutable    → PASS (tag 50be0b97 unchanged)
```

Dashboard acceptance **not claimed** — per §16, it remains a separate single-send task.

---

## 16. Next Task Boundary

When independent review passes CNX-336:

* Next step is **runtime registration verification / candidate installation** (controlled single host with real OpenClaw gateway).
* Only after that may we proceed to single-send:

```
Dashboard → before_agent_run → TicketStore.accept → Ticket → model call → durable result → delivery → completed
```

No additional Dashboard semantic request was performed in CNX-336; the only traffic was local `hostPluginAuthority`/`register` probes in a temp workspace.

---

## 17. Final Notes

* Implementation keeps authority boundary explicit: bounded `Set([1,2])`, no `schemaVersion !==1 → accept`, no removal of validation, no warning-only fallback, no silent future acceptance.
* Unknown schemas remain fail-closed; adding future schema `3` requires explicit code change adding it to the set with documented semantics.
* Translation is in-memory only; canonical disk state remains `cnxMode` authority as owned by `host_state_v095.py`.
* No changes to model/provider/timeout behavior.

*End of CNX-336 report. Stopping for independent review.*

---

**Evidence anchors:**

* CNX-335 analysis: `docs/operations/coordination/reports/CNX-20260914-335-schema-authority-analysis-report.md`
* Fix diff: `git show HEAD -- plugins/cogentnexus-openclaw/src/v091-release-entry.ts`
* Test file: `plugins/cogentnexus-openclaw/src/cnx336-schema-authority.test.ts`
* Build fingerprint: `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8`

