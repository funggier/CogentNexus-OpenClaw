import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { afterEach, describe, expect, it } from "vitest";

import { TicketStore } from "./ticket-store.js";
import { dueDirectRecovery } from "./v091-direct-recovery.js";

const tempDirs: string[] = [];

function fixture() {
  const dir = mkdtempSync(join(tmpdir(), "cnxclaw-host-stall-contract-"));
  tempDirs.push(dir);
  const databasePath = join(dir, "cogentnexus-openclaw.sqlite3");
  const store = new TicketStore(databasePath);
  const accepted = store.accept({
    runId: "run-host-stall",
    ownerSessionKey: "agent:main:dashboard:host-stall",
    prompt: "ตอบเพียง CNX-HOST-STALL-CONTRACT เท่านั้น",
  });
  store.route(accepted.ticketId, false);

  const db = new DatabaseSync(databasePath);
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
    "INSERT INTO cnx_sessions(session_key,state,generation,created_at,updated_at) VALUES (?,'active',7,?,?)",
  ).run(
    "agent:main:dashboard:host-stall",
    "2026-08-18T13:00:00.000Z",
    "2026-08-18T13:16:00.000Z",
  );
  db.prepare(`INSERT INTO cnx_direct_recovery(
      ticket_id,mode,state,attempt_count,active_run_id,next_attempt_at,last_error,
      owner_generation,created_at,updated_at
    ) VALUES (?,'resume','pending',0,NULL,?,'host authorized after quiescence',7,?,?)`)
    .run(
      accepted.ticketId,
      "2026-08-18T13:16:00.000Z",
      "2026-08-18T13:16:00.000Z",
      "2026-08-18T13:16:00.000Z",
    );
  db.close();
  return { databasePath, ticketId: accepted.ticketId };
}

afterEach(() => {
  for (const dir of tempDirs.splice(0)) rmSync(dir, { recursive: true, force: true });
});

describe("Host-authorized Direct stall recovery contract", () => {
  it("is immediately consumable by the Direct Recovery worker without workflow promotion", () => {
    const { databasePath, ticketId } = fixture();

    const recovery = dueDirectRecovery(databasePath, new Date("2026-08-18T13:16:01.000Z"));

    expect(recovery).toEqual({
      ticket_id: ticketId,
      owner_session_key: "agent:main:dashboard:host-stall",
      prompt: "ตอบเพียง CNX-HOST-STALL-CONTRACT เท่านั้น",
      mode: "resume",
      attempt_count: 0,
      owner_generation: 7,
    });

    const db = new DatabaseSync(databasePath, { readOnly: true });
    const ticket = db.prepare(
      "SELECT status,workflow_eligible,workflow_id FROM tickets WHERE ticket_id=?",
    ).get(ticketId) as {
      status: string;
      workflow_eligible: number;
      workflow_id: string | null;
    };
    db.close();

    expect(ticket).toEqual({
      status: "accepted",
      workflow_eligible: 0,
      workflow_id: null,
    });
  });
});
