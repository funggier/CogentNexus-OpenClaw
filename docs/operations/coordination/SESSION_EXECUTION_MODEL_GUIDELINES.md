# Session, Execution, and Model-Use Guidelines

Updated: 2026-09-18 ICT

This document records the operator's current working preferences for dividing work between ChatGPT and Hermes, choosing whether Hermes should continue an existing session or start a new one, and deciding when a stronger reasoning model is warranted.

These are standing workflow preferences. They do not override task-specific hard fences, live/destructive authority boundaries, or the current `ACTIVE.md` / `STATUS.md` coordination state.

## 1. ChatGPT-first for work available in the current ChatGPT session

When ChatGPT can safely complete work with the tools available in its current session, ChatGPT should do that work directly instead of delegating it to Hermes merely for process consistency.

Typical ChatGPT-owned work includes:

- reading and reviewing GitHub source, reports, tasks, reviews, commits, and CI evidence;
- repository/source analysis that does not require the operator's local machine;
- architecture and root-cause analysis from available evidence;
- independent review and acceptance/rework decisions;
- documentation and coordination updates;
- creating bounded successor tasks;
- repository edits that the available GitHub tools can safely perform;
- checking branch/HEAD/current remote coordination state;
- preparing focused Hermes prompts when local/live execution is actually needed.

Do not create unnecessary Hermes work when ChatGPT can already complete the step directly.

## 2. Use Hermes for environment-specific execution

Hermes should be used when the task materially requires access that ChatGPT does not have in the current session, especially:

- the operator's Windows filesystem or local checkout;
- PowerShell or local CLI execution;
- installed OpenClaw/CogentNexus runtime inspection;
- live Gateway/provider/service state;
- Dashboard/browser interaction;
- local logs or machine-specific artifacts not present in GitHub;
- install/update/uninstall/reset/lifecycle actions;
- hardware/device/permission work;
- explicitly authorized live semantic/provider/model requests;
- long-running local validation that depends on the real machine.

Task-specific authorization and hard fences still govern these actions.

## 3. Hermes session reuse rule

Prefer the **same Hermes session** when the new work is a direct continuation of the current task and the existing local reasoning/context materially reduces risk of losing the thread.

Examples:

- continuing the same root-cause investigation;
- implementing the repair immediately derived from the investigation when the task remains continuous;
- finishing validation/reporting for the same bounded task;
- continuing work where local runtime observations from the current session are still active and important.

## 4. New Hermes session rule

Prefer a **new Hermes session** when the work is a new bounded task or a distinct phase whose required context can be reconstructed from GitHub.

Examples:

- moving from one completed CNX task to its reviewed successor;
- changing from lifecycle debugging to provider-runtime archaeology;
- beginning a new implementation phase after a completed review;
- starting work whose inputs are already captured in Task / Report / Review / architecture documents.

The purpose is to reduce context cost and context pollution.

A new Hermes session should not receive a large conversational history dump. It should bootstrap from the smallest durable GitHub set needed for the task, normally:

1. current remote branch HEAD;
2. `ACTIVE.md`;
3. `STATUS.md`;
4. active task specification;
5. relevant parent report/review;
6. referenced goal/architecture documents;
7. only the additional source/evidence documents needed by that task.

GitHub is the durable project memory. Chat history is temporary working context.

## 5. Model selection rule

Use the least expensive/fastest model that can reliably complete the bounded task, but escalate before complexity starts to reduce evidence quality.

Current examples:

### Luna-friendly work

A faster/lighter reasoning model such as GPT-5.6 Luna is generally suitable for:

- bounded repository archaeology;
- source tracing and call-graph construction;
- evidence collection;
- deterministic test execution;
- focused regression work;
- small repairs with an already-established root cause;
- report generation from well-bounded evidence;
- tasks with explicit inputs, outputs, and hard fences.

### Stronger-model work

Prefer a stronger reasoning configuration such as GPT-5.6 Sol / higher reasoning effort when work involves:

- several competing root-cause hypotheses;
- contradictory or incomplete evidence across multiple subsystems;
- architecture decisions with broad long-term consequences;
- concurrency, race, lifecycle, cache, registry, or recovery interactions that are difficult to isolate;
- large cross-system repairs;
- high-risk production mutation planning;
- release/final-acceptance decisions;
- situations where a weak local choice could create substantial downstream rework.

Model names may change over time; the capability rule matters more than a specific model label.

## 6. ChatGPT should proactively flag heavy work

The operator should not have to continually decide whether Hermes needs a stronger model.

When ChatGPT sees that the next Hermes task has crossed from bounded/deterministic work into materially difficult reasoning, ChatGPT should explicitly tell the operator that the task is now heavy and recommend a stronger model/reasoning level.

Likewise, if the task remains suitable for Luna, ChatGPT may say so briefly when useful.

## 7. Prompt handoff rule

When Hermes should start a new session, ChatGPT should prepare a focused bootstrap prompt.

That prompt should:

- point to authoritative GitHub state;
- name the exact active task;
- name only the relevant reports/reviews/goals;
- restate the current objective and hard fences;
- avoid replaying unnecessary historical context;
- tell Hermes to prefer GitHub evidence over the prompt if they differ;
- include the required closeout/report contract.

When Hermes should continue the same session, prefer a concise continuation instruction rather than re-sending the full task context.

## 8. Practical decision table

| Situation | Default action |
|---|---|
| ChatGPT can do the work safely with current tools | ChatGPT does it directly |
| Requires local Windows/runtime/UI access | Hermes |
| Same task and active investigation continues | Reuse Hermes session |
| New task / new phase with durable GitHub handoff | New Hermes session |
| Bounded evidence/source/test work | Luna-class model is normally sufficient |
| Multi-hypothesis/cross-system/high-risk reasoning | Escalate to stronger model |
| Model difficulty is unclear | ChatGPT assesses and tells the operator |
| Important context must survive sessions | Write it to GitHub, not only chat |

## 9. Coordination precedence

For current task identity and authority:

`remote GitHub branch -> ACTIVE.md / STATUS.md -> active task -> report/review -> these standing preferences -> conversational memory`

Task-specific hard fences always remain authoritative for side effects.

These guidelines are intended to reduce context waste, prevent unnecessary delegation, and keep execution aligned with the operator's current working style.
