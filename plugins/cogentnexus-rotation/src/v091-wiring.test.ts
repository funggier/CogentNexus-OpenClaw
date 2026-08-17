import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it, vi } from "vitest";
import { DIRECT_RECOVERY_ID } from "./v091-direct-recovery.js";
import entry, {
  HOST_RECONCILIATION_ID,
  TICKET_RECOVERY_ID,
  WORKFLOW_COMPLETION_ID,
  idleWorkHint,
  isAdaptiveHostReconciliation,
  isEventDrivenService,
} from "./v091-final-entry.js";

describe("v0.9.1 production wiring", () => {
  it("replaces production polling services with event-driven workers at real register time", () => {
    const services: any[] = [];
    const events: string[] = [];
    const base: any = {
      pluginConfig: { ticketFirst: true, enforcedMode: true, workspaceDir: process.cwd() },
      logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
      registerService: (service: any) => services.push(service),
      registerTool: vi.fn(), registerCommand: vi.fn(), registerCli: vi.fn(), registerGatewayMethod: vi.fn(),
      on: vi.fn((name: string) => { events.push(name); }), config: {},
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

    const host = services.filter((service) => service?.id === HOST_RECONCILIATION_ID);
    const workflow = services.filter((service) => service?.id === WORKFLOW_COMPLETION_ID);
    const tickets = services.filter((service) => service?.id === TICKET_RECOVERY_ID);
    const direct = services.filter((service) => service?.id === DIRECT_RECOVERY_ID);
    const context = services.filter((service) => service?.id === "cogentnexus-context-maintenance-v091");

    expect(host).toHaveLength(1);
    expect(workflow).toHaveLength(1);
    expect(tickets).toHaveLength(1);
    expect(direct).toHaveLength(1);
    expect(context).toHaveLength(1);
    expect(isAdaptiveHostReconciliation(host[0])).toBe(true);
    expect(isEventDrivenService(host[0])).toBe(true);
    expect(isEventDrivenService(workflow[0])).toBe(true);
    expect(isEventDrivenService(tickets[0])).toBe(true);
    expect(isEventDrivenService(direct[0])).toBe(true);
    expect(events).toContain("agent_end");
    expect(events).toContain("message_sent");
    expect(events).toContain("after_compaction");
  });

  it("keeps v0.9.1 context and Direct Recovery free of periodic setInterval polling", () => {
    const contextSource = readFileSync(new URL("./v091-context-guard.ts", import.meta.url), "utf8");
    const directSource = readFileSync(new URL("./v091-direct-recovery.ts", import.meta.url), "utf8");
    expect(contextSource).not.toContain("setInterval(");
    expect(contextSource).toContain("queueMicrotask(()=>pulse?.())");
    expect(contextSource).toContain("nextDueDelay");
    expect(directSource).not.toContain("setInterval(");
    expect(directSource).toContain("nextDirectRecoveryWakeMs");
  });

  it("treats Ticket outbox and assistant delivery as actionable work even when every Ticket is terminal", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v091-idle-hint-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const db = new DatabaseSync(path);
      db.exec("CREATE TABLE tickets(status TEXT NOT NULL)");
      db.exec("CREATE TABLE ticket_outbox(delivery_status TEXT NOT NULL)");
      db.exec("CREATE TABLE cnx_assistant_delivery(status TEXT NOT NULL)");
      db.prepare("INSERT INTO tickets(status) VALUES (?)").run("completed");
      expect(idleWorkHint(path)).toBe(false);
      db.prepare("INSERT INTO cnx_assistant_delivery(status) VALUES (?)").run("pending");
      expect(idleWorkHint(path)).toBe(true);
      db.prepare("UPDATE cnx_assistant_delivery SET status='delivered'").run();
      db.prepare("INSERT INTO ticket_outbox(delivery_status) VALUES (?)").run("pending");
      db.close();
      expect(idleWorkHint(path)).toBe(true);
    } finally { rmSync(root, { recursive: true, force: true }); }
  });

  it("treats a missing database as truly idle without creating it", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v091-missing-db-"));
    try { expect(idleWorkHint(join(root, "does-not-exist.sqlite3"))).toBe(false); }
    finally { rmSync(root, { recursive: true, force: true }); }
  });
});
