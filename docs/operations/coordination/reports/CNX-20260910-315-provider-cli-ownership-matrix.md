# CNX-20260910-315 — Provider / CLI Ownership Matrix

## Purpose

This checkpoint records the v0.9.5 ownership boundary between CogentNexus-OpenClaw lifecycle control, local adapter process control, and OpenClaw provider/model/auth/routing authority.

## Ownership matrix

| Surface | Authority | Allowed responsibility | Explicitly forbidden |
|---|---|---|---|
| `cnxclaw start` | CNX Host | CNX/Gateway lifecycle | Provider/model selection or route mutation |
| `cnxclaw stop` | CNX Host | CNX/Gateway lifecycle | Provider/model selection or route mutation |
| `cnxclaw restart` | CNX Host | CNX/Gateway lifecycle | Provider/model selection or route mutation |
| `cnxclaw status` | CNX + diagnostic surfaces | Host state plus read-only provider metadata | Provider transition |
| `cnxclaw local ollama start` | Local Adapter | Ollama process start | OpenClaw route mutation |
| `cnxclaw local ollama stop` | Local Adapter | Ollama process stop | OpenClaw route mutation |
| `cnxclaw local ollama restart` | Local Adapter | Ollama process restart | OpenClaw route mutation |
| `cnxclaw local ollama status` | Local Adapter | Read-only Ollama status | OpenClaw route mutation |
| `cnxclaw local ollama check` | Local Adapter | Read-only Ollama readiness check | OpenClaw route mutation |
| `cnxclaw provider list` | Diagnostic | Read-only provider metadata | State/routing transition |
| `cnxclaw provider status` | Diagnostic | Read-only provider metadata | State/routing transition |
| `cnxclaw --provider ...` on CNX lifecycle | None | Rejected legacy input | Any lifecycle or routing transition |
| `cnxclaw cloud` | OpenClaw | Explicit authority handoff | CNX routing transition |

## Verification boundary

The focused regression suite asserts that lifecycle and adapter dispatch do not call the OpenClaw route transition surface, that legacy `--provider` lifecycle input is rejected, and that provider list/status remain diagnostic-only.

The compatibility `provider_transition()` implementation remains available for older callers/tests, but the v0.9.5 CLI dispatch does not invoke it. This preserves compatibility without making it a second CLI routing authority.

## Exit condition

Plan 1 is not considered closed from this document alone. Closure requires fresh verification of the focused suite plus the repository CI/acceptance gates on the resulting commit.
