import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it, vi } from "vitest";
import entry, {
  HOST_RECONCILIATION_ID,
  idleWorkHint,
  isAdaptiveHostReconciliation,
} from "./v091-final-entry.js";

describe("v0.9.1 production wiring", () => {
  it("replaces the legacy Host reconciliation service at real register time", () => {
    const services: any[] = [];
    const base: any = {
      pluginConfig: {
        ticketFirst: true,
        enforcedMode: true,
        workspaceDir: process.cwd(),
      },
      logger: {
        info: vi.fn(),
        warn: vi.fn(),
        error: vi.fn(),
        debug: vi.fn(),
      },
      registerService: (service: any) => services.push(service),
      registerTool: vi.fn(),
      registerCommand: vi.fn(),
      registerCli: vi.fn(),
      registerGatewayMethod: vi.fn(),
      on: vi.fn(),
      config: {},
    };
    const api = new Proxy(base, {
      get(target, property) {
        if (property in target) return target[property as keyof typeof target];
        const fallback = vi.fn();
        target[property as keyof typeof target] = fallback;
        return fallback;
      },
    });

    entry.register?.(api);

    const hostServices = services.filter((service) => service?.id === HOST_RECONCILIATION_ID);
    expect(hostServices).toHaveLength(1);
    expect(isAdaptiveHostReconciliation(hostServices[0])).toBe(true);
  });

  it("treats pending delivery as actionable work even when every Ticket is terminal", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v091-idle-hint-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const db = new DatabaseSync(path);
      db.exec("CREATE TABLE tickets(status TEXT NOT NULL)");
      db.exec("CREATE TABLE ticket_outbox(delivery_status TEXT NOT NULL)");
      db.prepare("INSERT INTO tickets(status) VALUES (?)").run("completed");
      expect(idleWorkHint(path)).toBe(false);
      db.prepare("INSERT INTO ticket_outbox(delivery_status) VALUES (?)").run("pending");
      db.close();
      expect(idleWorkHint(path)).toBe(true);
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });

  it("treats a missing database as truly idle without creating it", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v091-missing-db-"));
    try {
      expect(idleWorkHint(join(root, "does-not-exist.sqlite3"))).toBe(false);
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});
