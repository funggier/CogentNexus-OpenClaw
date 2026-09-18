import { describe, expect, it, vi } from "vitest";
import { mkdtempSync, mkdirSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import entry from "./v091-release-entry.js";

/**
 * CNX-374 regression test.
 *
 * Root cause: OpenClaw 2026.7.1-2 host gates conversation hooks
 * (before_agent_run, before_agent_start, etc.) on the plugin DEFINITION's
 * `hooks.allowConversationAccess` property. For non-bundled plugins, the
 * hook is blocked at registry time unless this is explicitly true.
 *
 * Source: registry-B8eQDFB4.js lines 4225-4244 (registerTypedHook):
 *   if (isConversationHookName(effectiveHookName)) {
 *     const explicitConversationAccess = policy?.allowConversationAccess;
 *     if (record.origin !== "bundled" && explicitConversationAccess !== true) {
 *       pushDiagnostic({ ... blocked ... });
 *       return;
 *     }
 *   }
 *
 * Source: loader-D8d2EvVh.js line 2240:
 *   hookPolicy: entry?.hooks  // DEFINITION's hooks, NOT runtime config
 *
 * Runtime config plugins.entries.<id>.hooks.allowConversationAccess feeds
 * pluginConfig only; it does NOT affect the gate.
 *
 * The fix: declare `hooks: { allowConversationAccess: true }` on the
 * definePluginEntry object so entry?.hooks.allowConversationAccess === true.
 */

describe("CNX-374 plugin hook registration registry wiring gate", () => {
  it("GREEN: before_agent_run reaches the host registry through the full legacy chain", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx374-"));
    mkdirSync(join(root, "host"), { recursive: true });
    writeFileSync(join(root, "host", "controller.json"), JSON.stringify({
      schemaVersion: 2, cnxMode: "active", generation: 7,
    }));
    mkdirSync(join(root, ".cogentnexus-openclaw", "runtime"), { recursive: true });

    const hooks: string[] = [];
    const api: any = {
      pluginConfig: { cogentNexusOpenClawRoot: root, preInferenceAdmission: true, ticketFirst: true },
      logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
      on: (name: string) => { hooks.push(name); },
      registerService: vi.fn(),
      registerTool: vi.fn(),
      registerGatewayMethod: vi.fn(),
      config: { agents: { defaults: { workspace: root } } },
    };

    (entry as any).register(api);
    expect(hooks).toContain("before_agent_run");
  });
});
