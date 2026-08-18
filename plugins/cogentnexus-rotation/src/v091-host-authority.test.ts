import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it, vi } from "vitest";
import entry, { hostPluginAuthority } from "./v091-release-entry.js";

function writeController(workspace: string, mode: "managed" | "passthrough" | "maintenance") {
  const host = join(workspace, ".cogent", "host");
  mkdirSync(host, { recursive: true });
  writeFileSync(join(host, "controller.json"), JSON.stringify({
    schemaVersion: 1,
    mode,
    desiredGateway: mode === "maintenance" ? "stopped" : "running",
    desiredProvider: mode === "managed" ? "running" : "unchanged",
    generation: 7,
    updatedAt: "2026-08-18T12:00:00.000Z",
  }));
}

function fakeApi(workspace: string) {
  const base: any = {
    pluginConfig: { workspaceDir: workspace, ticketFirst: true, enforcedMode: true },
    logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
    registerService: vi.fn(),
    registerTool: vi.fn(),
    registerCommand: vi.fn(),
    registerCli: vi.fn(),
    registerGatewayMethod: vi.fn(),
    on: vi.fn(),
    config: { agents: { defaults: { workspace } } },
    runtime: {},
  };
  return new Proxy(base, {
    get(target, property) {
      if (property in target) return target[property as keyof typeof target];
      const fallback = vi.fn();
      target[property as keyof typeof target] = fallback;
      return fallback;
    },
  });
}

describe("v0.9.1 Host single-recovery-authority boundary", () => {
  it("fails closed when Host controller state is missing", () => {
    const workspace = mkdtempSync(join(tmpdir(), "cnx-v091-host-missing-"));
    try {
      const api = fakeApi(workspace);
      expect(hostPluginAuthority(api)).toMatchObject({ authorized: false, reason: "missing" });
      (entry as any).register(api);
      expect(api.registerService).not.toHaveBeenCalled();
      expect(api.registerTool).not.toHaveBeenCalled();
      expect(api.on).not.toHaveBeenCalled();
    } finally { rmSync(workspace, { recursive: true, force: true }); }
  });

  it("keeps native plugin install/hot-reload inert in clean PASSTHROUGH", () => {
    const workspace = mkdtempSync(join(tmpdir(), "cnx-v091-host-passthrough-"));
    try {
      writeController(workspace, "passthrough");
      const api = fakeApi(workspace);
      expect(hostPluginAuthority(api)).toMatchObject({ authorized: false, reason: "passthrough", mode: "passthrough" });
      (entry as any).register(api);
      expect(api.registerService).not.toHaveBeenCalled();
      expect(api.registerTool).not.toHaveBeenCalled();
      expect(api.registerCommand).not.toHaveBeenCalled();
      expect(api.on).not.toHaveBeenCalled();
      expect(api.logger.info).toHaveBeenCalledWith(expect.stringContaining("registration suppressed"));
    } finally { rmSync(workspace, { recursive: true, force: true }); }
  });

  it("keeps MAINTENANCE inert even if a stale managed policy marker exists", () => {
    const workspace = mkdtempSync(join(tmpdir(), "cnx-v091-host-maintenance-"));
    try {
      writeController(workspace, "maintenance");
      writeFileSync(join(workspace, "AGENTS.md"), "<!-- cogentnexus:begin -->\nstale\n<!-- cogentnexus:end -->\n");
      const api = fakeApi(workspace);
      expect(hostPluginAuthority(api)).toMatchObject({ authorized: false, reason: "maintenance" });
      (entry as any).register(api);
      expect(api.registerService).not.toHaveBeenCalled();
      expect(api.on).not.toHaveBeenCalled();
    } finally { rmSync(workspace, { recursive: true, force: true }); }
  });

  it("accepts steady-state MANAGED Host authority", () => {
    const workspace = mkdtempSync(join(tmpdir(), "cnx-v091-host-managed-"));
    try {
      writeController(workspace, "managed");
      const api = fakeApi(workspace);
      expect(hostPluginAuthority(api)).toMatchObject({ authorized: true, reason: "managed", mode: "managed" });
    } finally { rmSync(workspace, { recursive: true, force: true }); }
  });

  it("accepts only the transactional Host activation window while PASSTHROUGH", () => {
    const workspace = mkdtempSync(join(tmpdir(), "cnx-v091-host-activating-"));
    try {
      writeController(workspace, "passthrough");
      writeFileSync(join(workspace, "AGENTS.md"), "before\n<!-- cogentnexus:begin -->\nmanaged policy\n<!-- cogentnexus:end -->\nafter\n");
      const api = fakeApi(workspace);
      expect(hostPluginAuthority(api)).toMatchObject({
        authorized: true,
        reason: "host-activation-staged",
        mode: "passthrough",
      });
    } finally { rmSync(workspace, { recursive: true, force: true }); }
  });
});
