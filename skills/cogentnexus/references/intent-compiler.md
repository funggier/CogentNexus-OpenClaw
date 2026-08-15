# Intent Compiler

Use this only when the request is not already an obvious DIRECT turn or when execution scope must be resolved.

The first job is **lane selection**, not workflow construction.

## Lanes

- **DIRECT** — conversational/low-risk work answerable from current context. No execution contract or runtime probe by default.
- **LOOKUP** — focused read-only retrieval with the minimum necessary source/tool surface.
- **ACTION** — bounded reversible execution with proportionate verification.
- **STAGED** — multi-step, consequential, interruption-prone, dependency-heavy, externally mutating, repeatedly failing, or independently reviewed work.

Choose the lightest reliable lane. Escalate only when observed complexity/risk requires it.

## STAGED compilation

For STAGED work, capture only what is required to execute safely and recoverably:

- requested outcome and observable acceptance criteria;
- current state and durable inputs;
- constraints and authority;
- dependencies and exact outputs;
- executor capability;
- deterministic validators and reviewer policy when needed;
- external-side-effect boundaries;
- recovery/cancellation semantics.

Do not turn optional preferences into requirements. Do not require the user to decompose work or write model prompts.

Ask only when information is genuinely undiscoverable or when missing authority/product choice materially changes the action. Otherwise make the smallest safe executable step and progress from committed state.

On validator failure, preserve exact evidence. Repeated identical symptoms should trigger a strategy change rather than unbounded retry. Never promote an unverified component to PASS.
