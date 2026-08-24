import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { afterEach, describe, expect, it, vi } from "vitest";
import { TicketStore } from "./ticket-store.js";
import {
  DIRECT_RECOVERY_LIVENESS_ID,
  directRecoveryStartupState,
  installV097DirectRecoveryStartupLiveness,
  startupLivenessDelayMs,
} from "./v097-direct-recovery-liveness.js";

afterEach(() => vi.useRealTimers());

function seed(path: string) {
  const store = new TicketStore(path);
  const ticket = store.accept({
    runId: "run-v097",
    ownerSessionKey: "agent:main:dashboard:v097",
    prompt: "fixture",
  });
  store.route(ticket.ticketId, false);
  const db = new DatabaseSync(path);
  const stamp = new Date().toISOString();
  db.exec(`
    CREATE TABLE cnx_sessions(
      session_key TEXT PRIMARY KEY,
      state TEXT NOT NULL,
      generation INTEGER NOT NULL
    );
    CREATE TABLE cnx_direct_recovery(
      ticket_id TEXT PRIMARY KEY,
      mode TEXT NOT NULL,
      state TEXT NOT NULL,
      attempt_count INTEGER NOT NULL,
      active_run_id TEXT,
      next_attempt_at TEXT,
      last_error TEXT,
      owner_generation INTEGER NOT NULL,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL
    );
    CREATE TABLE cnx_direct_model_call(
      ticket_id TEXT NOT NULL,
      call_id TEXT NOT NULL,
      state TEXT NOT NULL
    );
  `);
  db.prepare("INSERT INTO cnx_sessions VALUES (?,?,?)")
    .run("agent:main:dashboard:v097", "recovering", 4);
  db.prepare("INSERT INTO cnx_direct_recovery VALUES (?,?,?,?,?,?,?,?,?,?)")
    .run(ticket.ticketId, "resume", "pending", 0, null, stamp, null, 4, stamp, stamp);
  db.prepare("INSERT INTO cnx_direct_model_call VALUES (?,?,?)")
    .run(ticket.ticketId, "call-v097", "recovering");
  return { db, ticketId: ticket.ticketId };
}

describe("v0.9.7 Direct Recovery startup liveness", () => {
  it("keeps a bounded wake source while durable recovery exists but startup readiness is still settling", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v097-state-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const { db, ticketId } = seed(path);

      expect(directRecoveryStartupState(path)).toBe("waiting");

      db.prepare("UPDATE cnx_sessions SET state='active'").run();
      expect(directRecoveryStartupState(path)).toBe("waiting");

      db.prepare("UPDATE cnx_direct_model_call SET state='interrupted'").run();
      expect(directRecoveryStartupState(path)).toBe("ready");

      db.prepare("UPDATE cnx_sessions SET generation=5").run();
      expect(directRecoveryStartupState(path)).toBe("idle");

      db.prepare("UPDATE cnx_sessions SET generation=4").run();
      db.prepare("UPDATE tickets SET status='cancelled' WHERE ticket_id=?").run(ticketId);
      expect(directRecoveryStartupState(path)).toBe("idle");
      db.close();
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });

  it("uses bounded startup backoff instead of an idle interval", () => {
    expect(startupLivenessDelayMs(0)).toBe(250);
    expect(startupLivenessDelayMs(1)).toBe(1000);
    expect(startupLivenessDelayMs(2)).toBe(3000);
    expect(startupLivenessDelayMs(3)).toBe(10000);
    expect(startupLivenessDelayMs(4)).toBe(30000);
    expect(startupLivenessDelayMs(99)).toBe(30000);
  });

  it("pulses only while a durable pending recovery remains and stops cleanly", async () => {
    vi.useFakeTimers();
    const root = mkdtempSync(join(tmpdir(), "cnx-v097-service-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const { db, ticketId } = seed(path);
      let service: any;
      let pulses = 0;
      const api = {
        registerService(value: any) { service = value; },
      };

      installV097DirectRecoveryStartupLiveness(
        api,
        { workspaceDir: root, ticketDatabasePath: path },
        () => { pulses += 1; },
      );
      expect(service.id).toBe(DIRECT_RECOVERY_LIVENESS_ID);
      await service.start({ config: {} });

      await vi.advanceTimersByTimeAsync(250);
      expect(pulses).toBe(1);

      db.prepare("UPDATE cnx_sessions SET state='active'").run();
      db.prepare("UPDATE cnx_direct_model_call SET state='interrupted'").run();
      await vi.advanceTimersByTimeAsync(250);
      expect(pulses).toBe(2);

      db.prepare("UPDATE tickets SET status='cancelled' WHERE ticket_id=?").run(ticketId);
      await vi.advanceTimersByTimeAsync(1000);
      expect(pulses).toBe(2);

      await service.stop();
      expect(vi.getTimerCount()).toBe(0);
      db.close();
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});
