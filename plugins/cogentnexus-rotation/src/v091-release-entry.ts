import { definePluginEntry, type OpenClawPluginApi } from "openclaw/plugin-sdk/plugin-entry";
import legacyEntry from "./v091-final-entry.js";

/**
 * v0.9.1 public mixed-plugin boundary.
 *
 * CogentNexus registers tools together with hooks and services, so the shipped
 * runtime entry must use OpenClaw's mixed-plugin contract rather than the
 * defineToolPlugin metadata generator. Configuration remains authoritative in
 * openclaw.plugin.json, which OpenClaw reads before runtime code is loaded.
 *
 * All Ticket/recovery/delivery behavior remains in the already-tested v0.9.1
 * compatibility chain; this entry changes only the public plugin boundary.
 */
const releaseEntry: ReturnType<typeof definePluginEntry> = definePluginEntry({
  id: "cogentnexus-rotation",
  name: "CogentNexus OpenClaw Bridge",
  description:
    "Ticket-first OpenClaw bridge for CogentNexus Host-managed continuity, durable execution, recovery, context handoff, and verified delivery.",
  register(api: OpenClawPluginApi) {
    const register = (legacyEntry as { register?: (runtimeApi: OpenClawPluginApi) => void | Promise<void> }).register;
    if (typeof register !== "function") {
      throw new Error("CogentNexus v0.9.1 compatibility entry does not expose register(api)");
    }
    return register(api);
  },
});

export default releaseEntry;
