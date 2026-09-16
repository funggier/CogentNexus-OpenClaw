import { describe, expect, it, vi } from "vitest";
import { mkdirSync, mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import entry, { hostPluginAuthority } from "./v091-release-entry.js";

function api(root: string) {
  const hooks: string[] = [];
  const base: any = {
    pluginConfig: { cogentNexusOpenClawRoot: root, preInferenceAdmission: true, ticketFirst: true },
    logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
    on: (name: string) => { hooks.push(name); },
    registerService: vi.fn(), registerTool: vi.fn(), registerCommand: vi.fn(), registerCli: vi.fn(), registerGatewayMethod: vi.fn(),
    config: { agents: { defaults: { workspace: root, model: { primary: "openai/gpt-5.6-luna" } } } },
    hooks,
  };
  return new Proxy(base, { get(target, property) { if (property in target) return target[property]; const fallback = vi.fn(); target[property] = fallback; return fallback; } });
}

describe("CNX-368 ticket-first admission boundary", () => {
  it("accepts the canonical v0.9.5 active controller and registers before_agent_run", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx368-"));
    mkdirSync(join(root, "host"), { recursive: true });
    writeFileSync(join(root, "host", "controller.json"), JSON.stringify({
      schemaVersion: 2, cnxMode: "active", generation: 7,
    }));
    const runtime = api(root);
    expect(hostPluginAuthority(runtime)).toMatchObject({ authorized: true, reason: "managed", mode: "managed" });
    (entry as any).register(runtime);
    expect(runtime.hooks).toContain("before_agent_run");
  });
});
