import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { afterEach, describe, expect, it } from "vitest";

import { TicketStore } from "./ticket-store.js";
import { closeDirectModelCallForRun, recordDirectModelCallEnded, recordDirectModelCallStarted } from "./v091-direct-model-call-lease.js";
import { dueDirectRecovery, nextDirectRecoveryWakeMs } from "./v091-direct-recovery.js";

const tempDirs: string[] = [];

afterEach(() => {
  for (const dir of tempDirs.splice(0)) rmSync(dir, { recursive: true, force: true });
});

function fixture() {
  const dir = mkdtempSync(join(tmpdir(), "cnxclaw-direct-recovery-model-fence-"));
  tempDirs.push(dir);
  const path = join(dir, "tickets.sqlite3");
  const store = new TicketStore(path);
  const ticket = store.accept({
    runId: "run-live-provider",
    ownerSessionKey: "agent:main:dashboard:model-fence",
    prompt: "work",
  });
  store.route(ticket.ticketId, false);

  const db = new DatabaseSync(path);
  db.exec(`
    CREATE TABLE cnx_sessions(
      session_key TEXT PRIMARY KEY,
      state TEXT NOT NULL,
      generation INTEGER NOT NULL,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL
    );
    CREATE TABLE cnx_direct_recovery(
      ticket_id TEXT PRIMARY KEY,
      mode TEXT NOT NULL,
      state TEXT NOT NULL,
      attempt_count INTEGER NOT NULL DEFAULT 0,
      active_run_id TEXT,
      next_attempt_at TEXT,
      last_error TEXT,
      owner_generation INTEGER NOT NULL DEFAULT 0,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL
    );
  `);
  db.prepare(
    "INSERT INTO cnx_sessions(session_key,state,generation,created_at,updated_at) VALUES (?,'active',4,?,?)",
  ).run(
    "agent:main:dashboard:model-fence",
    "2026-08-18T13:00:00.000Z",
    "2026-08-18T13:00:00.000Z",
  );
  db.prepare(`INSERT INTO cnx_direct_recovery(
      ticket_id,mode,state,attempt_count,active_run_id,next_attempt_at,last_error,
      owner_generation,created_at,updated_at
    ) VALUES (?,'resume','pending',0,NULL,?,NULL,4,?,?)`)
    .run(
      ticket.ticketId,
      "2026-08-18T13:00:00.000Z",
      "2026-08-18T13:00:00.000Z",
      "2026-08-18T13:00:00.000Z",
    );
  db.close();

  return { path, ticketId: ticket.ticketId };
}

describe("Direct recovery provider-call ownership fence", () => {
  it("does not select or hot-loop a pending recovery while the original model call is active", () => {
    const { path } = fixture();
    expect(recordDirectModelCallStarted(path, {
      runId: "run-live-provider",
      callId: "call-live-provider",
      now: new Date("2026-08-18T13:00:00.000Z"),
      timeoutMs: 60_000,
    })).toBe(true);

    const now = new Date("2026-08-18T13:00:01.000Z");
    expect(dueDirectRecovery(path, now)).toBeUndefined();
    expect(nextDirectRecoveryWakeMs(path, {}, now)).toBeUndefined();
  });

  it("keeps one durable authority across provider-call ordering interleavings", () => {
    const first = fixture();
    expect(recordDirectModelCallStarted(first.path, { runId: "run-live-provider", callId: "call-order-1", now: new Date("2026-08-18T13:00:00.000Z"), timeoutMs: 60_000 })).toBe(true);
    expect(closeDirectModelCallForRun(first.path, "run-live-provider", "agent_end_error", new Date("2026-08-18T13:00:01.000Z"))).toBe(true);
    expect(dueDirectRecovery(first.path, new Date("2026-08-18T13:00:02.000Z"))).toMatchObject({ ticket_id: first.ticketId });

    const second = fixture();
    expect(recordDirectModelCallStarted(second.path, { runId: "run-live-provider", callId: "call-order-2", now: new Date("2026-08-18T13:00:00.000Z"), timeoutMs: 60_000 })).toBe(true);
    let db = new DatabaseSync(second.path);
    db.prepare("UPDATE cnx_direct_model_call SET state='recovering',recovery_started_at=?,updated_at=? WHERE ticket_id=?").run("2026-08-18T13:01:00.000Z", "2026-08-18T13:01:00.000Z", second.ticketId);
    db.close();
    expect(closeDirectModelCallForRun(second.path, "run-live-provider", "agent_end_error", new Date("2026-08-18T13:01:01.000Z"))).toBe(false);
    db = new DatabaseSync(second.path, { readOnly: true });
    expect((db.prepare("SELECT state FROM cnx_direct_model_call WHERE ticket_id=?").get(second.ticketId) as any).state).toBe("recovering");
    db.close();

    const third = fixture();
    expect(recordDirectModelCallStarted(third.path, { runId: "run-live-provider", callId: "call-order-3", now: new Date("2026-08-18T13:00:00.000Z"), timeoutMs: 60_000 })).toBe(true);
    expect(recordDirectModelCallEnded(third.path, { runId: "run-live-provider", callId: "call-order-3", outcome: "ok", durationMs: 10, now: new Date("2026-08-18T13:00:01.000Z") })).toBe(true);
    expect(closeDirectModelCallForRun(third.path, "run-live-provider", "agent_end_ok", new Date("2026-08-18T13:00:02.000Z"))).toBe(false);
  });
  it("keeps recovery blocked while Host owns classification, then releases it after Host marks the call interrupted", () => {
    const { path, ticketId } = fixture();
    recordDirectModelCallStarted(path, {
      runId: "run-live-provider",
      callId: "call-live-provider",
      now: new Date("2026-08-18T13:00:00.000Z"),
      timeoutMs: 60_000,
    });
    let db = new DatabaseSync(path);
    db.prepare(
      "UPDATE cnx_direct_model_call SET state='recovering',recovery_started_at=?,updated_at=? WHERE ticket_id=?",
    ).run(
      "2026-08-18T13:01:01.000Z",
      "2026-08-18T13:01:01.000Z",
      ticketId,
    );
    db.close();

    const claimed = new Date("2026-08-18T13:01:02.000Z");
    expect(dueDirectRecovery(path, claimed)).toBeUndefined();
    expect(nextDirectRecoveryWakeMs(path, {}, claimed)).toBeUndefined();

    db = new DatabaseSync(path);
    db.prepare(
      "UPDATE cnx_direct_model_call SET state='interrupted',ended_at=?,outcome='host-timeout-authorized',updated_at=? WHERE ticket_id=?",
    ).run(
      "2026-08-18T13:01:03.000Z",
      "2026-08-18T13:01:03.000Z",
      ticketId,
    );
    db.close();

    expect(dueDirectRecovery(path, new Date("2026-08-18T13:01:04.000Z")))
      .toMatchObject({
        ticket_id: ticketId,
        mode: "resume",
        owner_generation: 4,
      });
    expect(nextDirectRecoveryWakeMs(path, {}, new Date("2026-08-18T13:01:04.000Z"))).toBe(25);
  });
});
