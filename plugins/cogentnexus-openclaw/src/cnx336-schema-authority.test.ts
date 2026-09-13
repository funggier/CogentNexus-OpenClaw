import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it, vi } from "vitest";
import entry, { hostPluginAuthority } from "./v091-release-entry.js";

function hostRoot(workspace: string) {
  return join(workspace, ".cogentnexus-openclaw", "host");
}
function controllerPath(workspace: string) {
  return join(hostRoot(workspace), "controller.json");
}
function writeRaw(workspace: string, data: unknown) {
  mkdirSync(hostRoot(workspace), { recursive: true });
  writeFileSync(controllerPath(workspace), JSON.stringify(data));
}
function writeMalformed(workspace: string, raw: string) {
  mkdirSync(hostRoot(workspace), { recursive: true });
  writeFileSync(controllerPath(workspace), raw);
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
    config: { agents: { defaults: { workspace, model: { primary: "openai/gpt-5.6-luna" } } } },
    runtime: {},
  };
  return new Proxy(base, {
    get(target: any, prop: string | symbol) {
      if (prop in target) return target[prop];
      const fn = vi.fn();
      target[prop] = fn;
      return fn;
    },
  });
}

describe("CNX-336 schema authority compatibility", () => {
  describe("authority matrix", () => {
    it("v1 + managed → authorized", () => {
      const ws = mkdtempSync(join(tmpdir(), "cnx336-v1-managed-"));
      try {
        writeRaw(ws, { schemaVersion: 1, mode: "managed", generation: 5 });
        const api = fakeApi(ws);
        expect(hostPluginAuthority(api)).toMatchObject({ authorized: true, reason: "managed", mode: "managed" });
      } finally { rmSync(ws, { recursive: true, force: true }); }
    });
    it("v1 + passthrough → authorized", () => {
      const ws = mkdtempSync(join(tmpdir(), "cnx336-v1-pass-"));
      try {
        writeRaw(ws, { schemaVersion: 1, mode: "passthrough", generation: 6 });
        const api = fakeApi(ws);
        expect(hostPluginAuthority(api)).toMatchObject({ authorized: true, reason: "passthrough", mode: "passthrough" });
      } finally { rmSync(ws, { recursive: true, force: true }); }
    });
    it("v1 + maintenance → denied", () => {
      const ws = mkdtempSync(join(tmpdir(), "cnx336-v1-maint-"));
      try {
        writeRaw(ws, { schemaVersion: 1, mode: "maintenance", generation: 7 });
        const api = fakeApi(ws);
        expect(hostPluginAuthority(api)).toMatchObject({ authorized: false, reason: "maintenance", mode: "maintenance" });
      } finally { rmSync(ws, { recursive: true, force: true }); }
    });
    it("v2 + active → authorized (derived managed)", () => {
      const ws = mkdtempSync(join(tmpdir(), "cnx336-v2-active-"));
      try {
        writeRaw(ws, { schemaVersion: 2, cnxMode: "active", generation: 8 });
        const api = fakeApi(ws);
        expect(hostPluginAuthority(api)).toMatchObject({ authorized: true, reason: "managed", mode: "managed" });
      } finally { rmSync(ws, { recursive: true, force: true }); }
    });
    it("v2 + disabled → authorized (derived passthrough)", () => {
      const ws = mkdtempSync(join(tmpdir(), "cnx336-v2-disabled-"));
      try {
        writeRaw(ws, { schemaVersion: 2, cnxMode: "disabled", generation: 9 });
        const api = fakeApi(ws);
        expect(hostPluginAuthority(api)).toMatchObject({ authorized: true, reason: "passthrough", mode: "passthrough" });
      } finally { rmSync(ws, { recursive: true, force: true }); }
    });
    it("v2 + maintenance → denied", () => {
      const ws = mkdtempSync(join(tmpdir(), "cnx336-v2-maint-"));
      try {
        writeRaw(ws, { schemaVersion: 2, cnxMode: "maintenance", generation: 10 });
        const api = fakeApi(ws);
        expect(hostPluginAuthority(api)).toMatchObject({ authorized: false, reason: "maintenance", mode: "maintenance" });
      } finally { rmSync(ws, { recursive: true, force: true }); }
    });
    it("v3 → denied (fail closed)", () => {
      const ws = mkdtempSync(join(tmpdir(), "cnx336-v3-"));
      try {
        writeRaw(ws, { schemaVersion: 3, cnxMode: "active", mode: "managed", generation: 11 });
        const api = fakeApi(ws);
        expect(hostPluginAuthority(api)).toMatchObject({ authorized: false, reason: "invalid" });
      } finally { rmSync(ws, { recursive: true, force: true }); }
    });
    it("v99 → denied", () => {
      const ws = mkdtempSync(join(tmpdir(), "cnx336-v99-"));
      try {
        writeRaw(ws, { schemaVersion: 99, cnxMode: "active", generation: 12 });
        const api = fakeApi(ws);
        expect(hostPluginAuthority(api)).toMatchObject({ authorized: false, reason: "invalid" });
      } finally { rmSync(ws, { recursive: true, force: true }); }
    });
    it("missing version → denied", () => {
      const ws = mkdtempSync(join(tmpdir(), "cnx336-missing-ver-"));
      try {
        writeRaw(ws, { mode: "managed", cnxMode: "active", generation: 13 });
        const api = fakeApi(ws);
        expect(hostPluginAuthority(api)).toMatchObject({ authorized: false, reason: "invalid" });
      } finally { rmSync(ws, { recursive: true, force: true }); }
    });
    it("string \"2\" → denied (malformed)", () => {
      const ws = mkdtempSync(join(tmpdir(), "cnx336-str2-"));
      try {
        writeRaw(ws, { schemaVersion: "2" as unknown as number, cnxMode: "active", generation: 14 });
        const api = fakeApi(ws);
        expect(hostPluginAuthority(api)).toMatchObject({ authorized: false, reason: "invalid" });
      } finally { rmSync(ws, { recursive: true, force: true }); }
    });
    it("null version → denied", () => {
      const ws = mkdtempSync(join(tmpdir(), "cnx336-null-"));
      try {
        writeRaw(ws, { schemaVersion: null as unknown as number, cnxMode: "active", generation: 15 });
        const api = fakeApi(ws);
        expect(hostPluginAuthority(api)).toMatchObject({ authorized: false, reason: "invalid" });
      } finally { rmSync(ws, { recursive: true, force: true }); }
    });
    it("v2 + missing cnxMode → denied", () => {
      const ws = mkdtempSync(join(tmpdir(), "cnx336-v2-missmode-"));
      try {
        writeRaw(ws, { schemaVersion: 2, generation: 16 });
        const api = fakeApi(ws);
        expect(hostPluginAuthority(api)).toMatchObject({ authorized: false, reason: "invalid" });
      } finally { rmSync(ws, { recursive: true, force: true }); }
    });
    it("v2 + invalid cnxMode → denied", () => {
      const ws = mkdtempSync(join(tmpdir(), "cnx336-v2-invalidmode-"));
      try {
        writeRaw(ws, { schemaVersion: 2, cnxMode: "bogus", generation: 17 });
        const api = fakeApi(ws);
        expect(hostPluginAuthority(api)).toMatchObject({ authorized: false, reason: "invalid" });
      } finally { rmSync(ws, { recursive: true, force: true }); }
    });
    it("unreadable JSON → denied", () => {
      const ws = mkdtempSync(join(tmpdir(), "cnx336-unreadable-"));
      try {
        writeMalformed(ws, "{ not json ");
        const api = fakeApi(ws);
        expect(hostPluginAuthority(api)).toMatchObject({ authorized: false, reason: "invalid" });
      } finally { rmSync(ws, { recursive: true, force: true }); }
    });
    it("missing controller file → missing", () => {
      const ws = mkdtempSync(join(tmpdir(), "cnx336-missing-file-"));
      try {
        const api = fakeApi(ws);
        expect(hostPluginAuthority(api)).toMatchObject({ authorized: false, reason: "missing" });
      } finally { rmSync(ws, { recursive: true, force: true }); }
    });
    it("does not mutate controller file for v2 (in-memory translation only)", () => {
      const ws = mkdtempSync(join(tmpdir(), "cnx336-nomutate-"));
      try {
        const payload = { schemaVersion: 2, cnxMode: "active", generation: 42 };
        writeRaw(ws, payload);
        const before = readFileSync(controllerPath(ws), "utf8");
        const api = fakeApi(ws);
        const auth = hostPluginAuthority(api);
        expect(auth.authorized).toBe(true);
        const after = readFileSync(controllerPath(ws), "utf8");
        expect(after).toBe(before);
        expect(JSON.parse(after)).not.toHaveProperty("mode");
        expect(JSON.parse(after).cnxMode).toBe("active");
      } finally { rmSync(ws, { recursive: true, force: true }); }
    });
  });

  describe("registration", () => {
    it("valid v1 registers hooks", () => {
      const ws = mkdtempSync(join(tmpdir(), "cnx336-reg-v1-"));
      try {
        writeRaw(ws, { schemaVersion: 1, mode: "managed", generation: 20 });
        const api = fakeApi(ws);
        (entry as any).register(api);
        expect(api.on).toHaveBeenCalled();
        expect(api.logger.info).not.toHaveBeenCalledWith(expect.stringContaining("registration suppressed"));
      } finally { rmSync(ws, { recursive: true, force: true }); }
    });
    it("valid v2 registers hooks", () => {
      const ws = mkdtempSync(join(tmpdir(), "cnx336-reg-v2-"));
      try {
        writeRaw(ws, { schemaVersion: 2, cnxMode: "active", generation: 21 });
        const api = fakeApi(ws);
        (entry as any).register(api);
        expect(api.on).toHaveBeenCalled();
        expect(api.logger.info).not.toHaveBeenCalledWith(expect.stringContaining("registration suppressed"));
      } finally { rmSync(ws, { recursive: true, force: true }); }
    });
    it("valid v2 disabled registers hooks", () => {
      const ws = mkdtempSync(join(tmpdir(), "cnx336-reg-v2-dis-"));
      try {
        writeRaw(ws, { schemaVersion: 2, cnxMode: "disabled", generation: 22 });
        const api = fakeApi(ws);
        (entry as any).register(api);
        expect(api.on).toHaveBeenCalled();
      } finally { rmSync(ws, { recursive: true, force: true }); }
    });
    it("invalid/future schema registers nothing (no partial registration)", () => {
      const cases = [
        { schemaVersion: 3, cnxMode: "active" },
        { schemaVersion: 99, cnxMode: "active" },
        { schemaVersion: "2" as unknown as number, cnxMode: "active" },
        { schemaVersion: 2, cnxMode: "bogus" },
        { schemaVersion: 2 },
        { mode: "managed" },
      ];
      for (const payload of cases) {
        const ws = mkdtempSync(join(tmpdir(), "cnx336-reg-invalid-"));
        try {
          writeRaw(ws, { ...payload, generation: 30 });
          const api = fakeApi(ws);
          (entry as any).register(api);
          expect(api.on).not.toHaveBeenCalled();
          expect(api.registerService).not.toHaveBeenCalled();
          expect(api.registerTool).not.toHaveBeenCalled();
          expect(api.logger.info).toHaveBeenCalledWith(expect.stringContaining("registration suppressed"));
          // reset for next iteration is via new api per ws
        } finally { rmSync(ws, { recursive: true, force: true }); }
      }
    });
    it("maintenance (v1 and v2) suppresses registration", () => {
      for (const payload of [
        { schemaVersion: 1, mode: "maintenance" },
        { schemaVersion: 2, cnxMode: "maintenance" },
      ]) {
        const ws = mkdtempSync(join(tmpdir(), "cnx336-reg-maint-"));
        try {
          writeRaw(ws, { ...payload, generation: 40 });
          const api = fakeApi(ws);
          (entry as any).register(api);
          expect(api.on).not.toHaveBeenCalled();
          expect(api.logger.info).toHaveBeenCalledWith(expect.stringContaining("registration suppressed"));
        } finally { rmSync(ws, { recursive: true, force: true }); }
      }
    });
    it("unreadable JSON suppresses registration", () => {
      const ws = mkdtempSync(join(tmpdir(), "cnx336-reg-unreadable-"));
      try {
        writeMalformed(ws, "{ bad json");
        const api = fakeApi(ws);
        (entry as any).register(api);
        expect(api.on).not.toHaveBeenCalled();
      } finally { rmSync(ws, { recursive: true, force: true }); }
    });
    it("missing file suppresses registration", () => {
      const ws = mkdtempSync(join(tmpdir(), "cnx336-reg-missing-"));
      try {
        const api = fakeApi(ws);
        (entry as any).register(api);
        expect(api.on).not.toHaveBeenCalled();
        expect(hostPluginAuthority(api).reason).toBe("missing");
      } finally { rmSync(ws, { recursive: true, force: true }); }
    });
  });

  describe("downstream equivalence", () => {
    it("v1 managed ≡ v2 active", () => {
      const ws1 = mkdtempSync(join(tmpdir(), "cnx336-equiv1a-"));
      const ws2 = mkdtempSync(join(tmpdir(), "cnx336-equiv1b-"));
      try {
        writeRaw(ws1, { schemaVersion: 1, mode: "managed", generation: 50 });
        writeRaw(ws2, { schemaVersion: 2, cnxMode: "active", generation: 50 });
        const a1 = hostPluginAuthority(fakeApi(ws1));
        const a2 = hostPluginAuthority(fakeApi(ws2));
        expect(a1).toMatchObject({ authorized: true, reason: "managed", mode: "managed" });
        expect(a2).toMatchObject({ authorized: true, reason: "managed", mode: "managed" });
        expect(a1.authorized).toBe(a2.authorized);
        expect(a1.reason).toBe(a2.reason);
        expect(a1.mode).toBe(a2.mode);
      } finally {
        rmSync(ws1, { recursive: true, force: true });
        rmSync(ws2, { recursive: true, force: true });
      }
    });
    it("v1 passthrough ≡ v2 disabled", () => {
      const ws1 = mkdtempSync(join(tmpdir(), "cnx336-equiv2a-"));
      const ws2 = mkdtempSync(join(tmpdir(), "cnx336-equiv2b-"));
      try {
        writeRaw(ws1, { schemaVersion: 1, mode: "passthrough", generation: 51 });
        writeRaw(ws2, { schemaVersion: 2, cnxMode: "disabled", generation: 51 });
        const a1 = hostPluginAuthority(fakeApi(ws1));
        const a2 = hostPluginAuthority(fakeApi(ws2));
        expect(a1).toMatchObject({ authorized: true, reason: "passthrough", mode: "passthrough" });
        expect(a2).toMatchObject({ authorized: true, reason: "passthrough", mode: "passthrough" });
        expect(a1.authorized).toBe(a2.authorized);
        expect(a1.reason).toBe(a2.reason);
        expect(a1.mode).toBe(a2.mode);
      } finally {
        rmSync(ws1, { recursive: true, force: true });
        rmSync(ws2, { recursive: true, force: true });
      }
    });
    it("preserves generation across translation", () => {
      const ws = mkdtempSync(join(tmpdir(), "cnx336-gen-"));
      try {
        writeRaw(ws, { schemaVersion: 2, cnxMode: "active", generation: 99 });
        const auth = hostPluginAuthority(fakeApi(ws));
        expect(auth.generation).toBe(99);
      } finally { rmSync(ws, { recursive: true, force: true }); }
    });
    it("ensures bounded set does not accept future schema even with valid cnxMode", () => {
      const ws = mkdtempSync(join(tmpdir(), "cnx336-future-valid-"));
      try {
        writeRaw(ws, { schemaVersion: 3, cnxMode: "active", generation: 100 });
        const auth = hostPluginAuthority(fakeApi(ws));
        expect(auth.authorized).toBe(false);
        expect(auth.reason).toBe("invalid");
      } finally { rmSync(ws, { recursive: true, force: true }); }
    });
  });
});
