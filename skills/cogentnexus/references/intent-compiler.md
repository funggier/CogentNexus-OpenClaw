# Intent Compiler

Use when the user expresses an outcome without an execution specification.

Capture the outcome, observable acceptance criteria, current state, constraints, authority, executor capability, and validators. Do not turn optional preferences into requirements.

Choose Direct for one reversible observable action; Verified for dependent artifacts, generated code/data, or integration; Durable for long, detached, interruption-prone, or costly-to-duplicate work.

For Verified or Durable work, define the dependency manifest, assign the smallest complete component to each executor, create deterministic validators where practical, preserve passing checkpoints, integrate only verified units, and run end-to-end acceptance tests.

On first validator failure, return exact bounded evidence once. On repeated symptoms, change strategy. Record deterministic repair separately from model output. Never admit an unverified component.

Do not require the user to decompose work or write model prompts. Ask only for missing authority, irreversible external action, consequential product choice, or an undiscoverable required input.
