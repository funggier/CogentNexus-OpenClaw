# Runtime Supervisor

The supervisor is an external deterministic controller. Its healthy periodic path performs no model inference.

## Responsibilities

- read desired mode/runtime state;
- probe Gateway/provider health cheaply;
- inspect durable actionable work;
- respect cooldown/retry/circuit-breaker policy;
- wake recovery/delivery/runtime workers only when state warrants it;
- never override deliberate MAINTENANCE or PASSTHROUGH intent.

A slow model call is not automatically a hang from Ticket age alone. Recovery requires the relevant durable/endpoint evidence.

When Host authority is committed, late OpenClaw observations cannot silently steal recovery ownership. Transient SQLite authority-read BUSY is not an ownership change.
