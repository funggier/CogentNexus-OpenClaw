# CNX-20260914-337 — Independent Regression and Registration Verification Report

**Date:** 2026-09-14 05:30 UTC+07 (Asia/Bangkok)  
**Task:** CNX-337 `v0.9.6 Independent Regression and Registration Verification`  
**Status:** `READY_FOR_HERMES` → verified by Hermes (local, evidence-first)  
**Verifier:** Hermes Agent (Nous Research) — independent of CNX-336 author  
**Candidate branch:** `agent/v0.9.6-schema-authority-repair`  
**Baseline fence:** `v0.9.5` tag `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95`  
**Verdict:** `PASS` — all gates satisfied; ready for independent review before Dashboard semantic acceptance. No Dashboard semantic traffic sent. No implementation modified.

---

## 1. Candidate Identity

| Field | Value | Verified |
|---|---|---|
| Branch | `agent/v0.9.6-schema-authority-repair` | `git branch --show-current` → `agent/v0.9.6-schema-authority-repair` |
| Actual full HEAD | `ee19e2075041c95bf27f0a5c4a2d35e75281e3d7` | `git rev-parse HEAD` |
| Expected reported head | `ee19e207` (prefix of full HEAD) | **MATCH** — full HEAD starts with `ee19e207` |
| CNX-336 repair commit | `3efb971eeed55f0d48908281974577fdbed48612` | `git rev-parse 3efb971e` + `git log --oneline -4` |
| Parent of HEAD | `3efb971eeed55f0d48908281974577fdbed48612` | `git rev-parse HEAD^` |
| Parent of repair commit | `979869983d693544541661ba7c8229dcecb9dc0b` | `git rev-parse 3efb971e^` |
| Published release | `v0.9.5` | tag `refs/tags/v0.9.5` |
| Immutable release tag SHA | `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95` | `git rev-parse refs/tags/v0.9.5` + `ls-remote origin refs/tags/v0.9.5` |
| Reported artifact fingerprint (CNX-336) | `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8` | SHA-256 of built `dist/v091-release-entry.js` — **MATCH** (reproduced §10) |

### Git state evidence (2026-09-14 05:26 UTC+07)

```
$ git rev-parse HEAD
ee19e2075041c95bf27f0a5c4a2d35e75281e3d7
$ git rev-parse 3efb971e
3efb971eeed55f0d48908281974577fdbed48612
$ git rev-parse refs/tags/v0.9.5
50be0b973c30fd8d1528aaac3497c0fc3b0b4d95
$ git ls-remote origin refs/tags/v0.9.5
50be0b973c30fd8d1528aaac3497c0fc3b0b4d95	refs/tags/v0.9.5
$ git show-ref --tags | grep v0.9.5
50be0b973c30fd8d1528aaac3497c0fc3b0b4d95 refs/tags/v0.9.5
```

### Branch provenance

* `ee19e207` — `docs: publish CNX-336 schema authority repair report`
* `3efb971e` — `fix(plugin): add bounded schema 2 authority compatibility (CNX-336)`
* `97986998` — `docs: publish CNX-335 schema authority analysis` (origin/temp-check)
* `ff6eae95` — `docs: publish CNX-334 dashboard boundary diagnostic`
* Base: `45442f9bcb0afab76b0c319ebe8aef9471dfb15c` `chore: regenerate v0.9.5 package lockfile`

`45442f9b` is the `v0.9.5` development baseline that was merged into `50be0b97` via merge commit `50be0b97 (tree b1b42871, parents 6439dd96 + fc3f4bc0)`. Therefore:

* `git merge-base 50be0b97 45442f9b` → `45442f9b` (45442f is ancestor of v0.9.5 tag) — verified.
* `git merge-base 45442f9b ee19e207` → `45442f9b` (candidate descends from 45442f) — verified.
* `git merge-base --is-ancestor 50be0b97 ee19e207` → **NO** — candidate is sibling of the merge commit, not descendant of the merge commit itself. This is expected: CNX-336 branched from the development baseline `45442f9b` before the `v0.9.5` merge, not from the merge commit. The document notes this explicitly; it does not constitute a history rewrite and the `v0.9.5` tag remains untouched. Candidate contains no `main` post-v0.9.5 commits and no divergence beyond the CNX-334/335/336 repair chain.

### Remote state discrepancy (not blocking)

```
$ git ls-remote origin | grep v0.9.6
(no output — no remote branch)
$ git fetch origin agent/v0.9.6-schema-authority-repair
fatal: could not find remote ref agent/v0.9.6-schema-authority-repair
```

`agent/v0.9.6-schema-authority-repair` exists **locally only** at `ee19e2075041c95b`; it has **not yet been pushed to origin**. The expected reported head `ee19e207` is therefore verified against the local HEAD, not the remote `FETCH_HEAD`. This is a publication gap, not a SHA mismatch: local HEAD == expected prefix. No force-push detected via `git reflog show agent/v0.9.6-schema-authority-repair`:

```
ee19e207 agent/v0.9.6-schema-authority-repair@{0}: commit: docs: publish CNX-336 schema authority repair report
3efb971e agent/v0.9.6-schema-authority-repair@{1}: commit: fix(plugin): add bounded schema 2 authority compatibility (CNX-336)
97986998 agent/v0.9.6-schema-authority-repair@{2}: branch: Created from HEAD
```

No force-push, no history rewrite, no tag mutation.

### Tag alias check

* `v0.9.5` (`50be0b97`) is NOT an alias of the candidate: candidate HEAD `ee19e207` ≠ `50be0b97`; merge-base analysis confirms sibling lineage, not identity.

### Working tree state

```
$ git status --porcelain
?? docs/operations/coordination/reports/CNX-20260910-repair-checkpoint-final.md
?? docs/operations/coordination/reports/CNX-20260914-331-web-session-qwen38-final-acceptance-report.md
?? plugins/cogentnexus-openclaw/src/v090-reproducer.test.ts
$ git diff HEAD --stat
(empty — no staged or unstaged changes)
```

Three untracked files only; all are pre-existing stray files not part of the candidate commit and not staged. `dist/` is gitignored and not committed, as intended.

---

## 2. Diff Review

### Scope

```
$ git diff --stat 97986998..ee19e207
 docs/operations/coordination/reports/CNX-20260914-336-schema-authority-repair-report.md | 423 +++++
 plugins/cogentnexus-openclaw/src/cnx336-schema-authority.test.ts            | 325 +++++
 plugins/cogentnexus-openclaw/src/v091-release-entry.ts                      |  40 +-
 3 files changed, 781 insertions(+), 7 deletions(-)

$ git diff --stat 97986998..3efb971e
 plugins/cogentnexus-openclaw/src/cnx336-schema-authority.test.ts | 325 +++++
 plugins/cogentnexus-openclaw/src/v091-release-entry.ts           |  40 +-
 2 files changed, 358 insertions(+), 7 deletions(-)

$ git diff --stat 3efb971e..ee19e207
 docs/operations/coordination/reports/CNX-20260914-336-schema-authority-repair-report.md | 423 +++++
 1 file changed, 423 insertions(+)
```

**Expected functional changes (CNX-336 spec):**

* Bounded schema support `{1,2}` — ✅ present
* Canonical `cnxMode` translation `active→managed, disabled→passthrough, maintenance→maintenance` — ✅ present
* Fail-closed validation (type-strict, integer, Set lookup) — ✅ present
* Targeted authority tests (27 tests) — ✅ present

**Expected scope** — `v091-release-entry.ts`, `cnx336-schema-authority.test.ts`, report/documentation — **MATCH**.

**Unexpected changes:** None. Verified:

* No provider logic change
* No timeout logic change
* No TicketStore change
* No Dashboard handling change
* No recovery/ownership/idempotency/controller-persistence refactoring
* No unrelated file touched in repair commit `3efb971e` (exactly 2 files)

**Behavioral scope confirmed** — diff inspects only the authority gate and its tests; all other subsystems unchanged.

### Before/after gate (for reference)

Before (`97986998` / `v0.9.5`):

```ts
const mode = typeof state?.mode === "string" ? state.mode : undefined;
if (state?.schemaVersion !== 1 || !["managed","passthrough","maintenance"].includes(mode ?? "")) {
  return { authorized:false, reason:"invalid", mode, generation, controllerPath };
}
```

After (`ee19e207`):

```ts
const SUPPORTED_CONTROLLER_SCHEMA_VERSIONS = new Set<number>([1, 2]);
const CANONICAL_TO_LEGACY_MODE: Record<string, string> = {
  active: "managed", disabled: "passthrough", maintenance: "maintenance",
};
// ...
const rawSchemaVersion = state?.schemaVersion;
if (typeof rawSchemaVersion !== "number" || !Number.isInteger(rawSchemaVersion) || !SUPPORTED.has(rawSchemaVersion)) {
  return { authorized:false, reason:"invalid", ... };
}
if (rawSchemaVersion === 1) { /* exact prior semantics preserved */ }
// schemaVersion === 2 — canonical Host authority
const cnxMode = typeof state?.cnxMode === "string" ? state.cnxMode : undefined;
const derived = cnxMode !== undefined ? CANONICAL_TO_LEGACY_MODE[cnxMode] : undefined;
if (derived === undefined) return { authorized:false, reason:"invalid", ... };
```

No permissive `schemaVersion != 1 → accept`, no `if (mode exists) → accept`, no `unknown → warning only` path.

---

## 3. Authority Logic Review

Direct source verification of `plugins/cogentnexus-openclaw/src/v091-release-entry.ts` (blob `fb51fbbbd62bb75261e221cd9d4f139be90e803b`, 232 lines):

**Required semantics:**

```
schema 1 → legacy mode validation                         ✅ verified
schema 2 → cnxMode validation → in-memory translation → existing authority decision  ✅ verified
unknown/malformed → fail closed                           ✅ verified
```

**Proven absence of anti-patterns:**

* No `schemaVersion !== 1` branch — grep shows only `SUPPORTED_CONTROLLER_SCHEMA_VERSIONS.has(rawSchemaVersion)` gate, no `!== 1` fallback.
* No `if (mode exists) → accept` — both branches require explicit set membership `["managed","passthrough","maintenance"]` (v1) or `CANONICAL_TO_LEGACY_MODE[cnxMode]` lookup (v2).
* No `unknown schema → warning only` — all unknown/malformed paths return `{ authorized:false, reason:"invalid" }` (or `missing` for ENOENT), no logger warning path that still authorizes.

**Type strictness:**

* `typeof rawSchemaVersion !== "number"` — rejects `null`, `undefined`, `"2"` string
* `!Number.isInteger(rawSchemaVersion)` — rejects `1.5`, floats
* `!SUPPORTED_CONTROLLER_SCHEMA_VERSIONS.has(rawSchemaVersion)` — rejects `3`, `99`, `0`, etc.

**v1 path** — exact preservation of prior semantics: `mode` must be in allowed set; `managed`/`passthrough` → `authorized:true`; `maintenance` → `authorized:false reason:"maintenance"`.

**v2 path** — `cnxMode` lookup via `CANONICAL_TO_LEGACY_MODE`; `derived === undefined` → `invalid`; then same `managed`/`passthrough`/`maintenance` decision on derived `mode`. No second stale consumer found (`grep -rn "schemaVersion !== 1\|schemaVersion === 1"` in `src/` returns only unrelated `index.ts:241 notice.schemaVersion === 1`).

---

## 4. Disk Mutation Review

**Requirement:** Schema 2 translation is in-memory only; must NOT rewrite `controller.json`, persist legacy `mode`, downgrade schema 2, mutate generation, or overwrite canonical Host state. Canonical authority remains with `host_state_v095.py`.

**Evidence:**

* Source `hostPluginAuthority` performs only `readFileSync` + `JSON.parse`, never `writeFileSync`/`atomic_json`. No write path exists in the function.
* Controlled probe `in-memory no mutate` case: `payload { schemaVersion:2, cnxMode:"active", generation:42 }` — `before` vs `after` file content identical, `JSON.parse(after)` has `cnxMode:"active"` and `!hasOwnProperty("mode")` — **PASS**.
* Full matrix smoke (18 cases) — `unchanged=true` for every case including `v2 active`/`v2 disabled`/`v2 maintenance` — **PASS**.
* Canonical Host state owner `skills/cogentnexus-openclaw/scripts/host_state_v095.py` retains `schemaVersion:2` authority; plugin does not replicate `host_state_v095.py` write logic.

**Verdict:** No disk mutation; translation is strictly in-memory.

---

## 5. Registration Review

**Authorized schema — expected sequence:**

```
hostPluginAuthority() → authorized=true → legacyEntry.register(runtimeApi) → before_agent_run registration occurs
```

**Unauthorized schema — expected:**

```
hostPluginAuthority() → authorized=false → registration suppressed → no partial hooks
```

**Source verification (`v091-release-entry.ts` lines 175-229):**

```ts
const authority = hostPluginAuthority(api);
if (!authority.authorized) {
  api.logger.info(`...registration suppressed: Host authority=${authority.reason} ...`);
  return; // ← no register(), no api.on(), no partial guards
}
const register = (legacyEntry as { register?: ... }).register;
if (typeof register !== "function") throw new Error(...);
// ... fences, then register(runtimeApi), then installManagedRuntimeGuards()
```

No registration side effect before authority succeeds — authority is the first operation in `register()`.

**Probe results (dist build, see §8 smoke):**

| Controller | Authority | `api.on` called | `before_agent_run` | Suppression log |
|---|---|---|---|---|
| v1 managed | `authorized:true reason:managed` | ✅ | ✅ | none |
| v1 passthrough | `authorized:true reason:passthrough` | ✅ | ✅ | none |
| v2 active | `authorized:true reason:managed` | ✅ | ✅ | none |
| v2 disabled | `authorized:true reason:passthrough` | ✅ | ✅ | none |
| v3 / 99 / string "2" / null / missing cnxMode / invalid cnxMode | `authorized:false reason:invalid` | ❌ | ❌ | `registration suppressed` |
| v1/v2 maintenance | `authorized:false reason:maintenance` | ❌ | ❌ | `registration suppressed` |
| unreadable / missing file | `authorized:false` | ❌ | ❌ | `registration suppressed` |

**No partial hooks:** For every denied case, `api.on` was not called, `registerService`/`registerTool` not called. Verified via vitest bulk case (`invalid/future schema registers nothing` iterates 6 payloads) and via smoke probe.

---

## 6. Compatibility Matrix

Independently executed via `vitest` targeted suite and via controlled `dist` smoke (node import of built artifact). Both agree.

### Vitest targeted suite

```
$ npm test -- src/cnx336-schema-authority.test.ts
  ✓ src/cnx336-schema-authority.test.ts (27 tests) 276ms
  Test Files 1 passed (1) / Tests 27 passed (27)
```

### Controlled dist smoke (18/18 PASS)

```
PASS v1+managed => authorized=true reason=managed mode=managed gen=5 registered=true suppressed=false unchanged=true
PASS v1+passthrough => authorized=true reason=passthrough mode=passthrough gen=6 registered=true suppressed=false unchanged=true
PASS v1+maintenance => authorized=false reason=maintenance mode=maintenance gen=7 registered=false suppressed=true unchanged=true
PASS v2+active => authorized=true reason=managed mode=managed gen=8 registered=true suppressed=false unchanged=true
PASS v2+disabled => authorized=true reason=passthrough mode=passthrough gen=9 registered=true suppressed=false unchanged=true
PASS v2+maintenance => authorized=false reason=maintenance mode=maintenance gen=10 registered=false suppressed=true unchanged=true
PASS v3 => authorized=false reason=invalid mode=undefined gen=11 registered=false suppressed=true unchanged=true
PASS 99 => authorized=false reason=invalid mode=undefined gen=12 registered=false suppressed=true unchanged=true
PASS missing version => authorized=false reason=invalid mode=managed gen=13 registered=false suppressed=true unchanged=true
PASS string 2 => authorized=false reason=invalid mode=undefined gen=14 registered=false suppressed=true unchanged=true
PASS null => authorized=false reason=invalid mode=undefined gen=15 registered=false suppressed=true unchanged=true
PASS v2 missing cnxMode => authorized=false reason=invalid mode=undefined gen=16 registered=false suppressed=true unchanged=true
PASS v2 invalid cnxMode => authorized=false reason=invalid mode=undefined gen=17 registered=false suppressed=true unchanged=true
PASS unreadable => authorized=false reason=invalid gen=undefined registered=false suppressed=true unchanged=true
PASS missing file => authorized=false reason=missing registered=false suppressed=true unchanged=true
PASS in-memory no mutate => authorized=true reason=managed gen=42 registered=true suppressed=false unchanged=true
PASS equiv v1 managed == v2 active => authorized=true reason=managed gen=50 registered=true suppressed=false unchanged=true
PASS equiv v1 passthrough == v2 disabled => authorized=true reason=passthrough gen=51 registered=true suppressed=false unchanged=true
---SUMMARY---
passed 18/18
```

### Full matrix table

| Controller | Expected | Actual (vitest + smoke) | Result |
|---|---|---|---|
| v1 + managed | authorized | `authorized:true reason:managed mode:managed` | **PASS** |
| v1 + passthrough | authorized | `authorized:true reason:passthrough mode:passthrough` | **PASS** |
| v1 + maintenance | denied | `authorized:false reason:maintenance` | **PASS** |
| v2 + active | authorized | `authorized:true reason:managed` (derived) | **PASS** |
| v2 + disabled | authorized | `authorized:true reason:passthrough` (derived) | **PASS** |
| v2 + maintenance | denied | `authorized:false reason:maintenance` | **PASS** |
| v3 | denied | `authorized:false reason:invalid` | **PASS** |
| 99 | denied | `authorized:false reason:invalid` | **PASS** |
| missing version | denied | `authorized:false reason:invalid` | **PASS** |
| `"2"` (string) | denied | `authorized:false reason:invalid` | **PASS** |
| null | denied | `authorized:false reason:invalid` | **PASS** |
| v2 + missing cnxMode | denied | `authorized:false reason:invalid` | **PASS** |
| v2 + invalid cnxMode | denied | `authorized:false reason:invalid` | **PASS** |
| unreadable file | denied | `authorized:false reason:invalid` | **PASS** |
| missing file | missing/denied | `authorized:false reason:missing` | **PASS** |

**Downstream equivalence:**

```
v1 managed == v2 active  →  authorized:true reason:managed mode:managed  — PASS (generation preserved)
v1 passthrough == v2 disabled → authorized:true reason:passthrough mode:passthrough — PASS
preserves generation across translation → generation 99 retained — PASS (vitest)
bounded set does not accept future schema even with valid cnxMode → v3 active denied — PASS
```

---

## 7. Regression Tests

### Targeted (CNX-336)

```
$ cd plugins/cogentnexus-openclaw && npm test -- src/cnx336-schema-authority.test.ts

 RUN  v3.2.7 C:/Users/CDQ-P/CogentNexus-OpenClaw/plugins/cogentnexus-openclaw

 ✓ src/cnx336-schema-authority.test.ts (27 tests) 276ms

 Test Files  1 passed (1)
      Tests  27 passed (27)
   Duration  1.50s

Coverage breakdown (27 tests):
 - authority matrix: 16 cases
 - registration: 7 cases (valid v1, valid v2 active/disabled, invalid bulk, maintenance, unreadable, missing)
 - downstream equivalence: 4 cases (equiv managed, equiv passthrough, generation, future-bound)
```

### Full repository test suite

```
$ cd plugins/cogentnexus-openclaw && npm test

 Test Files  77 passed (77)
      Tests  366 passed (366)
   Duration  52.12s (transform 624ms, collect 19.78s, tests 20.06s)

Key suites confirming retention:
 - v091-host-authority.test.ts — 5 passed (schema-1 compatibility retained)
 - v091-wiring.test.ts — 5 passed
 - v091-config-schema.test.ts — 3 passed
 - v090-reproducer.test.ts — 2 passed (present as untracked, executed with suite)
 - ticket-store / ticket-runtime / delivery-continuity / v095-* — all green

No failing tests; no skipped gate ignored.
```

### Plugin build

```
$ npm run build
> tsc -p tsconfig.json && node ./scripts/canonicalize-dist.mjs --dist-root ./dist
canonicalized 50 dist text files to LF
exit 0 — no TS errors

$ npm run plugin:build
> npm run build && node ./scripts/verify-v091-schema.mjs
CogentNexus-OpenClaw mixed-plugin artifact verification: PASS (46 config properties, 5 tools)
exit 0
```

### Schema verifier

`scripts/verify-v091-schema.mjs` — **PASS** (same command as plugin:build). No schema drift, 46 config properties, 5 tools.

**Counts recorded:**

* Targeted: **27/27 PASS**, 1 file
* Full suite: **366/366 PASS**, 77 files
* Build: **PASS** (tsc + canonicalize 50 files)
* Schema verifier: **PASS** (46 properties, 5 tools)

---

## 8. Artifact Review

### Generated entry

* File: `plugins/cogentnexus-openclaw/dist/v091-release-entry.js`
* Size: **10 121 bytes**, 199 lines, blob `4c0adb031195e79125b3778d28d8854d3ae5b55d` (dist, git)
* Lines canonicalized to LF via `canonicalize-dist.mjs` (50 files)
* Git blob (src): `fb51fbbbd62bb75261e221cd9d4f139be90e803b` — matches `git hash-object` and `git rev-parse HEAD:plugins/cogentnexus-openclaw/src/v091-release-entry.ts`
* SHA-256 (dist JS): `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8` — **matches reported fingerprint** from CNX-336

```
$ sha256sum plugins/cogentnexus-openclaw/dist/v091-release-entry.js
c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8 *dist/v091-release-entry.js

$ grep -n SUPPORTED_CONTROLLER_SCHEMA_VERSIONS dist/v091-release-entry.js
15: const SUPPORTED_CONTROLLER_SCHEMA_VERSIONS = new Set([1, 2]);

$ grep -n CANONICAL_TO_LEGACY_MODE dist/v091-release-entry.js
16: const CANONICAL_TO_LEGACY_MODE = { active:"managed", disabled:"passthrough", maintenance:"maintenance" };

$ grep -n "schemaVersion !== 1\|schemaVersion === 1" dist/v091-release-entry.js
(no output — stale v0.9.5 implementation not present)
```

### Verification points

* Generated entry contains new authority logic — **PASS** (both constants present, `hostPluginAuthority` updated)
* No stale `v0.9.5` implementation remains in built entry (`schemaVersion !== 1` gate removed) — **PASS**
* Schema verifier passes — **PASS**
* Source/build output agrees — src blob `fb51fb...` compiles to dist containing same constants; runtime smoke via `dist` import behaves identically to `src` tests (18/18 PASS) — **PASS**

`dist/` is **not** committed (gitignored) per repository policy; no commit of generated `dist` was performed.

---

## 9. Static Regression Checks

Search for all remaining references to authority surface:

```
$ grep -rn "schemaVersion !== 1\|schemaVersion === 1" plugins/cogentnexus-openclaw/src
plugins/cogentnexus-openclaw/src/index.ts:241: if (notice.schemaVersion === 1 && ...)  # unrelated: delivery notice version, not controller authority

No stale schemaVersion !==1 / ===1 authority gate in plugin authority code — PASS.
```

```
$ grep -rn "cnxMode" plugins/cogentnexus-openclaw/src
src/cnx336-schema-authority.test.ts — test payloads only
src/v091-release-entry.ts: cnxMode?: string; const cnxMode = ...; CANONICAL_TO_LEGACY_MODE[cnxMode]  # expected only

Single authority consumer — no second stale authority consumer that still rejects schema 2 — PASS.

$ grep -rn "hostPluginAuthority" plugins/cogentnexus-openclaw/src
src/cnx336-schema-authority.test.ts, src/v091-host-authority.test.ts, src/cloud-passthrough-activation.test.ts, src/v091-release-entry.ts
All consumers use the updated function; no duplicated authority check.

$ grep -rn "SUPPORTED_CONTROLLER_SCHEMA_VERSIONS" plugins/cogentnexus-openclaw/src
src/v091-release-entry.ts: const SUPPORTED_CONTROLLER_SCHEMA_VERSIONS = new Set<number>([1, 2]);  # single definition
src/v091-release-entry.ts: if (... || !SUPPORTED_CONTROLLER_SCHEMA_VERSIONS.has(rawSchemaVersion))  # single usage — bounded

$ grep -rn "CANONICAL_TO_LEGACY_MODE" plugins/cogentnexus-openclaw/src
src/v091-release-entry.ts — definition + derived lookup only — PASS.

Nearby release-entry helpers inspected:
 - pluginWorkspace / pluginCogentRoot: workspace resolution unchanged, no schema assumption
 - isDiscordContext / isWebchatContext / LEGACY_*_HOOKS: delivery fences unchanged
 - withDiscordLegacyDeliveryFence / withWebchatLegacyDeliveryFence: unchanged
 - definePluginEntry register(): only addition is `hostPluginAuthority` gate at top — no assumption that schema 1 is always present
```

**Verdict:** No second stale authority consumer; no hidden `schema 1 always present` assumption remains.

---

## 10. Runtime Registration Smoke Test

**Method:** Controlled runtime with candidate build — no Dashboard semantic traffic, read-only/runtime instrumentation only.

* Loaded: `plugins/cogentnexus-openclaw/dist/v091-release-entry.js` (SHA `c15b2f61…`, 10 121 bytes) via `import(pathToFileURL(distPath))`
* Fabricated `OpenClawPluginApi` (`pluginConfig.workspaceDir` = temp `mkdtemp` workspace, `logger.info` captured, `api.on` captured)
* Controller: temp `join(workspace, ".cogentnexus-openclaw/host/controller.json")` per case

**Required evidence:**

```
plugin loaded                  → PASS (dist import succeeded, entry.id=cogentnexus-openclaw)
controller schema = 2          → PASS (tested schemaVersion:2 with cnxMode variants, generation 8-42)
hostPluginAuthority = authorized → PASS only for v2 active / v2 disabled (and v1 managed/passthrough)
legacyEntry.register invoked   → PASS (via api.on registration for authorized cases)
before_agent_run registered    → PASS (events includes before_agent_run for authorized cases; absent for denied cases)
controller.json unchanged      → PASS (before === after for every case; no mode persisted)
```

**Schema 2 active — proof:**

```
payload { schemaVersion:2, cnxMode:"active", generation:8 }
→ hostPluginAuthority = { authorized:true, reason:"managed", mode:"managed", generation:8 }
→ entry.register(api) → api.on includes before_agent_run = true
→ logger.info suppressed = false
→ file unchanged = true
```

**Future/malformed — proof fail-closed:**

```
payload { schemaVersion:3, cnxMode:"active", generation:11 } → authorized:false reason:invalid → hook not registered, suppressed:true
payload { schemaVersion:99 }                                  → authorized:false reason:invalid → not registered
payload { schemaVersion:2, cnxMode:"bogus" }                  → authorized:false reason:invalid → not registered
payload { schemaVersion:"2" (string) }                        → authorized:false reason:invalid → not registered
payload { schemaVersion:2, missing cnxMode }                  → authorized:false reason:invalid → not registered
payload { mode:"managed" (missing version) }                  → authorized:false reason:invalid → not registered
payload unreadable "{ not json "                             → authorized:false reason:invalid → not registered
payload missing file                                          → authorized:false reason:missing → not registered
```

**No Dashboard semantic traffic:** The probe performed zero `TicketStore.accept`, zero `Dashboard` send, zero `openclaw` gateway calls, zero network traffic. Only local `readFileSync`/`JSON.parse` and in-process `register(api)` with fake API. Confirmed by code audit: smoke script imports only `node:fs`, `node:os`, `node:path`, and the local `dist` artifact.

**Full smoke log:** 18/18 PASS, `passed 18/18` (see §6 table). SQLite experimental warning is Node 22 expected noise, not a failure.

---

## 11. Existing Runtime Configuration Fence

**Required invariant (CNX-337 §13):**

```
provider = ollama
model = ollama/qwen3.8:27b
provider timeout = 2700s
agent timeout = 2700s
```

**Verification:**

* `v091-release-entry.ts` diff does not touch provider, timeout, model, workspace, ownership, or controller mode. Grep for `provider`/`timeout`/`ollama` shows only comments about provider ownership boundary and the benign `providerMode` compatibility metadata line:
  ```
  ...(authority.reason === "passthrough" ? { providerMode: undefined } : { providerMode: "managed" as const }),
  ```
  This line is pre-existing (only the preceding authority gate was changed); it normalizes `passthrough` to `undefined` without disabling continuity/recovery.

* `openclaw.plugin.json` unchanged (`version 0.9.5`, `toolMetadata` intact, no provider/timeout fields added).

* No `agents.defaults.timeoutSeconds`, `models.providers.*.timeoutSeconds`, `workspaceDir`, or `providerOwnership` mutation found in the candidate diff.

* CNX-330 established model/transport timeout behavior is preserved — no regression introduced.

**Verdict:** Configuration fence intact; registration correctness only, as required.

---

## 12. Release Protection

```
$ git rev-parse refs/tags/v0.9.5
50be0b973c30fd8d1528aaac3497c0fc3b0b4d95
$ git show-ref --tags | grep v0.9.5
50be0b973c30fd8d1528aaac3497c0fc3b0b4d95 refs/tags/v0.9.5
$ git ls-remote origin refs/tags/v0.9.5
50be0b973c30fd8d1528aaac3497c0fc3b0b4d95	refs/tags/v0.9.5
$ git cat-file -p v0.9.5 | head -n 1
tree b1b428718f9e6c8f5a271a385e1021f2efc75d1d
```

* No tag mutation — `refs/tags/v0.9.5` resolves to `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95` locally and on origin
* No force-push — reflog shows only forward commits, no `forced-update`
* No release modification — candidate lives on `agent/v0.9.6-schema-authority-repair`, no `git tag`, no `gh release` executed
* No merge to `main` — `agent/v0.9.6-schema-authority-repair` is not merged into `origin/main` (`11b0e916`), `main` remains at `11b0e916 docs: distinguish current main from v0.9.5 release baseline`
* No history rewrite — `git log --graph` shows linear CNX-334→335→336 chain on top of `45442f9b`, no rebase of `v0.9.5`

---

## 13. PASS Criteria Checklist (CNX-337 §15)

```
candidate identity verified      → PASS (ee19e2075041c95b matches expected, 3efb971e parent, tag 50be0b97 intact)
diff scope correct               → PASS (2 source files + 1 report, no unrelated behavioral modification)
authority matrix PASS            → PASS (15/15 matrix cases + 3 equivalence/generation — 18/18 smoke + 27 vitest)
fail-closed future schema PASS   → PASS (v3, 99, string "2", null, missing/invalid cnxMode all denied)
registration schema2 PASS        → PASS (v2 active → managed true; v2 disabled → passthrough true; before_agent_run registered)
no partial registration PASS     → PASS (every denied case: api.on not called, no registerService/Tool, suppressed log present)
full tests PASS                  → PASS (366/366, 77 files)
build PASS                       → PASS (tsc + canonicalize 50 files, no TS errors)
artifact verification PASS       → PASS (SHA c15b2f61... contains SUPPORTED set [1,2] + CANONICAL map; no stale v0.9.5 entry)
runtime registration PASS        → PASS (dist import + authority true → hook registered; invalid → not registered)
controller unchanged PASS        → PASS (every case before===after, no mode persisted for v2)
v0.9.5 immutable PASS            → PASS (tag SHA unchanged locally and on origin; no tag/release/mirror mutation)
```

All gates true — CNX-337 is **PASS**.

---

## 14. BLOCK Conditions (CNX-337 §16 — all clear)

* Candidate SHA cannot be verified — **not triggered** (verified `ee19e2075041c95b`)
* Actual diff differs materially from CNX-336 report — **not triggered** (diff stat exactly as CNX-336 reported: 40 lines in entry + 325 lines test + 423 doc)
* Any schema 1 regression — **not triggered** (v1 managed/passthrough/maintenance all behave as before; `v091-host-authority.test.ts` 5 passed)
* Schema 2 active/disabled fails — **not triggered** (both authorized)
* Unknown schema is accepted — **not triggered** (all unknown/malformed fail closed)
* Partial hooks registered before authority — **not triggered** (zero partial hooks in 6-case bulk + maintenance + malformed)
* Build artifact is stale — **not triggered** (dist freshly built 2026-09-14 05:26, SHA matches CNX-336 reported fingerprint, contains new logic)
* Another stale schema-1 authority check remains — **not triggered** (grep confirms no second consumer)
* Runtime registration still suppressed — **not triggered** (v2 active/disabled registers `before_agent_run`)
* Controller state mutates unexpectedly — **not triggered** (all cases unchanged)
* v0.9.5 changes — **not triggered** (tag SHA identical)

---

## 15. Important Gate

CNX-337 proves:

```
v0.9.6 candidate (ee19e2075041c95b)
    ↓
schema 2 authority accepted (active→managed, disabled→passthrough)
    ↓
hook registered (before_agent_run present, legacyEntry.register invoked)
```

Only after this PASS may the next task exercise:

```
Dashboard → before_agent_run → TicketStore.accept → durable lifecycle
```

No Dashboard traffic was sent in this verification. Do not proceed directly to Dashboard acceptance from CNX-336 without this gate — this report is that gate.

---

## 16. Verdict

**`PASS`**

Independent regression and registration verification succeeds on every required dimension. Candidate `agent/v0.9.6-schema-authority-repair` at `ee19e2075041c95bf27f0a5c4a2d35e75281e3d7` (repair `3efb971eeed55f0d48908281974577fdbed48612`) correctly:

* Preserves schema-1 semantics exactly
* Accepts bounded schema 2 (`active`/`disabled`) via in-memory canonical translation
* Fail-closes on every future/malformed/unauthorized schema or mode
* Suppresses all registration side effects until authority succeeds, with no partial hooks
* Leaves canonical `controller.json` (`cnxMode` authority owned by `host_state_v095.py`) untouched on disk
* Passes 27 targeted + 366 full tests, builds without errors, reproduces the reported `c15b2f61…` artifact with verifier PASS
* Does not modify provider/model/timeout/ownership/transport/recovery boundaries
* Leaves `v0.9.5` tag `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95` immutable locally and on origin

**Action:** Publish this report on the candidate branch and stop for independent review before Dashboard semantic acceptance. No merge, no release, no tag creation — as required.

---

## Evidence Anchors

* Branch HEAD: `git rev-parse HEAD` → `ee19e2075041c95bf27f0a5c4a2d35e75281e3d7`
* Tag: `git rev-parse refs/tags/v0.9.5` → `50be0b973c30fd8d1528aaac3497c0fc3b0b4d95` (local + `ls-remote origin`)
* Source blob: `git rev-parse HEAD:plugins/cogentnexus-openclaw/src/v091-release-entry.ts` → `fb51fbbbd62bb75261e221cd9d4f139be90e803b`
* Test file blob: `plugins/cogentnexus-openclaw/src/cnx336-schema-authority.test.ts` (325 lines, untracked → committed in `3efb971e`)
* Dist artifact: `plugins/cogentnexus-openclaw/dist/v091-release-entry.js` → `c15b2f61a1596f301510e9cd392851ef99427c6c129d653d2d336cfefa79b3a8` (SHA-256, 10 121 bytes, 199 lines)
* Log divergence: `git log --oneline 45442f9b..ee19e207` (4 commits), `git log --oneline 50be0b97..ee19e207` divergence documented above
* Exec outputs retained: `vitest` (27 targeted, 366 full), `tsc + canonicalize`, `verify-v091-schema`, `sha256sum`, `grep`, and controlled `node dist/v091-release-entry.js` smoke (18/18)

*End of CNX-337 independent regression verification report.*
