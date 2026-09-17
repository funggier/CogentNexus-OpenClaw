# CNX-20260917-384 — Host Hook Policy Projection Repair Report

## Classification

**`HOST_HOOK_POLICY_REPAIR_BLOCKED`**

The host-side projection owner is confirmed, but this repository has no existing supported, tracked, clean-install-reproducible mechanism for changing the OpenClaw loader dependency. No dependency patch, vendor/fork conversion, local `node_modules` edit, or speculative new dependency-management architecture was introduced. No Dashboard Ticket-first semantic success is claimed.

## Authority

- Repository: `funggier/CogentNexus-OpenClaw`
- Branch: `cnx-357-openai-dashboard-ticket-first-requalification-v2`
- Task ID: `CNX-20260917-384`
- Required starting status: `READY_FOR_HERMES` (confirmed)
- Authoritative starting HEAD: `63f7f6134f6445b311b91e06fbc268aa68d52651`
- Starting remote HEAD: `63f7f6134f6445b311b91e06fbc268aa68d52651`
- Final HEAD: `c3bd7fc08acfefce9cd47d83e71fc73445418352` (remote read-back before this report identity update)

`ACTIVE.md`, `STATUS.md`, this task, and the CNX-383, CNX-382, CNX-381, and CNX-374 reports were read from the authoritative branch before action. The required identity was confirmed: `Task ID = CNX-20260917-384`; `Status = READY_FOR_HERMES`.

## Proven boundary and exact host version

OpenClaw is pinned in `plugins/cogentnexus-openclaw/package.json` as devDependency `2026.7.1-2` and in `package-lock.json` as the resolved npm package `openclaw-2026.7.1-2.tgz`. The plugin declares OpenClaw as a peer dependency (`>=2026.5.17`) and packages only its built plugin artifact; it does not package the host runtime.

The already-proven boundary remains:

```text
releaseEntry.hooks.allowConversationAccess=true
  -> normalized.entries[pluginId].hooks is the loader policy source
  -> createApi(... hookPolicy: entry?.hooks)
  -> registerTypedHook(... policy ...)
  -> existing non-bundled gate rejects when policy?.allowConversationAccess !== true
```

CNX-382 and CNX-383 identify the exact installed modules and source locations:

- `loader-D8d2EvVh.js`: `const entry = normalized.entries[pluginId]`; `createApi(... hookPolicy: entry?.hooks)`
- `registry-B8eQDFB4.js`: `api.on` closes over `params.hookPolicy`; `registerTypedHook` applies the existing conversation-hook gate
- Exact OpenClaw base/version: `2026.7.1-2`

Known effective CogentNexus artifact identity, read directly in predecessor evidence and not activated or replaced by this task: SHA-256 `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`.

## Dependency ownership / reproducibility decision

The repository was checked for an already-supported ownership path before implementation:

- `plugins/cogentnexus-openclaw/package.json`: ordinary npm peer/dev dependency; no `overrides`, `resolutions`, `patches`, `patch-package`, vendor directory, fork URL, or OpenClaw source path.
- `plugins/cogentnexus-openclaw/package-lock.json`: ordinary registry lock entry for `openclaw@2026.7.1-2`; no tracked patched package metadata or local replacement.
- Repository workflows (`.github/workflows/validate.yml`, `release.yml`, and Windows package workflow): run `npm ci` in the plugin directory and build/package the CogentNexus plugin; they contain no OpenClaw patch, vendor, fork, or override step.
- Package contents/package model: the plugin artifact is installed into an externally owned OpenClaw runtime; the repository does not package a host runtime.
- Existing patch/override/vendor mechanisms: none found in the package, lockfile, plugin tree, or relevant workflows.

Therefore the only proven owner is the external OpenClaw loader dependency, but there is no existing repository-supported mechanism that can track and reproduce the required host change through clean `npm ci`. Creating a new broad dependency-management system for one field would violate the task's explicit architecture fence. The required repair is blocked before implementation.

## RED evidence

The existing focused regression from CNX-383 remains the exact RED evidence and was re-read as part of this task:

- `plugins/cogentnexus-openclaw/src/cnx383-hook-policy-projection.test.ts`
- executable definition asserts `entry.hooks.allowConversationAccess === true`
- host input models `normalized.entries[entry.id]?.hooks`
- the test asserts that host input is true and fails on the unrepaired projection

Recorded failure:

```text
FAIL src/cnx383-hook-policy-projection.test.ts
expected undefined to be true
Tests: 1 failed
```

This is a projection-boundary failure, not a missing path, install failure, or fixture failure. CNX-381's real loader trace additionally records the native host diagnostic and absence of `before_agent_run` from the typed registry while ordinary typed hooks were accepted.

No new implementation RED was created because the prerequisite ownership decision blocked any authorized repair implementation. No existing test was altered.

## Repair decision

No repair was applied. In particular:

- no `node_modules/openclaw` file was edited;
- no `registerTypedHook` gate was bypassed or hardcoded;
- no second `before_agent_run` registration path was added;
- no broad dependency architecture, fork, vendor tree, or override system was invented;
- no CogentNexus plugin source or built artifact was changed.

The smallest justified host change would be an explicit narrow projection of only `allowConversationAccess` into the normalized host policy object before `createApi`, preserving the existing gate and all unrelated policy fields. This cannot be made reproducible under the current repository installation model without an approved tracked host-dependency mechanism.

## GREEN / validation status

GREEN was not reached because the required host dependency ownership mechanism is absent. Consequently, the following were not run as acceptance evidence for a repaired candidate:

- CNX-384 GREEN regression
- clean-install reproduction of a patched OpenClaw dependency
- plugin build/validation for a repaired artifact
- runtime activation
- host targeted registry tests against a repaired dependency

No false GREEN claim is made. Existing predecessor evidence remains separate: CNX-383 recorded CNX-374 regression PASS and plugin build PASS for the unrepaired artifact, while the focused projection regression remained RED.

## Runtime and production evidence

Runtime activation: **0**. No pre/post activation PID exists for CNX-384. No production restart/reload or configuration mutation occurred.

Previously known production facts, not changed or revalidated by this blocked task:

- PID `27372`
- OpenClaw `2026.7.1-2`
- effective artifact SHA-256 `2841b704ad1c923ba643ca885eaf1d34e2f9565350d501c9d4895746d56c2d95`
- production plugin loaded
- production `hookCount=0`

Pre/post hook inventory for this task: unchanged / no activation; predecessor production inventory is `hookCount=0`, with no claim that a repaired hook is visible. Typed `before_agent_run` acceptance: not proven.

## Counts and hard fences

- Dashboard semantic requests: `0`
- Semantic retries: `0`
- Runtime activations/restarts: `0`
- Production configuration mutations: `0`
- OpenClaw dependency edits: `0`
- CogentNexus source/artifact repair edits: `0`
- New dependency-management architecture: `0`
- TicketStore/admission/routing/auth/provider/model changes: `0`
- Dashboard UI changes: `0`
- Bypass or second registration route: `0`
- Force-push/history rewrite/release/tag/main changes: `0`
- Historical CNX-360 through CNX-383 edits: `0`
- CNX-385 started: `0`

Security/policy preservation evidence: the existing `registerTypedHook` gate was not modified; because no repair was applied, non-authorized plugins remain subject to the same gate. No evidence exists that an authorized hook now passes.

## Remaining uncertainty

The blocker is architectural rather than a proven impossibility of OpenClaw repair: a future authorized task would need to select and document a supported repository-owned host dependency mechanism compatible with this plugin's external-runtime installation model. Until then, no clean-install-reproducible host projection repair can honestly be claimed. The production runtime was not restarted or inspected beyond previously recorded facts, and no Dashboard semantic request was made.

## Closeout

Classification: **`HOST_HOOK_POLICY_REPAIR_BLOCKED`**.

After publication, `ACTIVE.md` and `STATUS.md` are set to `WAITING_FOR_CHATGPT_REVIEW`. No runtime activation, semantic probe, or CNX-385 task was started.
