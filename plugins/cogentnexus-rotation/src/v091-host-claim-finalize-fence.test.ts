import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { afterEach, describe, expect, it } from "vitest";

import { TicketStore } from "./ticket-store.js";
import {
  hostRecoveryOwnsRun,
  installV091DirectModelCallLease,
  recordDirectModelCallStarted,
} from "./v091-direct-model-call-lease.js";

const tempDirs: string[] = [];

function createStore() {
  const dir = mkdtempSync(join(tmpdir(), "cnx-host-finalize-fence-"));
  tempDirs.push(dir);
  const databasePath = join(dir, "cogentnexus.sqlite3");
  return { databasePath, store: new TicketStore(databasePath) };
}

afterEach(() => {
  for (const dir of tempDirs.splice(0)) rmSync(dir, { recursive: true, force: true });
});

describe("Host Direct recovery claim finalization fence", () => {
  it("prevents shutdown agent_end finalization from mutating a Host-claimed Ticket", () => {
    const { databasePath, store } = createStore();
    const accepted = store.accept({
      runId: "run-host-claimed",
      ownerSessionKey: "agent:main:dashboard:claimed",
      prompt: "ตอบเพียง HOST-CLAIMED เท่านั้น",
    });
    store.route(accepted.ticketId, false);
    expect(recordDirectModelCallStarted(databasePath, {
      runId: "run-host-claimed",
      callId: "call-host-claimed",
      now: new Date("2026-08-18T13:00:00.000Z"),
    })).toBe(true);

    const db = new DatabaseSync(databasePath);
    db.prepare(
      "UPDATE cnx_direct_model_call SET state='recovering',recovery_started_at=?,updated_at=? WHERE ticket_id=?",
    ).run(
      "2026-08-18T13:16:00.000Z",
      "2026-08-18T13:16:00.000Z",
      accepted.ticketId,
    );
    db.close();

    const hooks: Array<{ name: string; handler: (...args: any[]) => unknown }> = [];
    installV091DirectModelCallLease({
      pluginConfig: { ticketDatabasePath: databasePath },
      on(name: string, handler: (...args: any[]) => unknown) {
        hooks.push({ name, handler });
      },
      logger: {},
    });

    expect(hostRecoveryOwnsRun(databasePath, "run-host-claimed")).toBe(true);
    expect(store.finalizeDirectRun({
      runId: "run-host-claimed",
      success: false,
      interrupted: false,
      message: "gateway stopped during Host quiescence",
    })).toBe("unchanged");

    const verify = new DatabaseSync(databasePath, { readOnly: true });
    const ticket = verify.prepare(
      "SELECT status,workflow_eligible,failure_class,response_ready_at FROM tickets WHERE ticket_id=?",
    ).get(accepted.ticketId) as {
      status: string;
      workflow_eligible: number;
      failure_class: string | null;
      response_ready_at: string | null;
    };
    const modelCall = verify.prepare(
      "SELECT state FROM cnx_direct_model_call WHERE ticket_id=?",
    ).get(accepted.ticketId) as { state: string };
    verify.close();

    expect(ticket).toEqual({
      status: "accepted",
      workflow_eligible: 0,
      failure_class: null,
      response_ready_at: null,
    });
    expect(modelCall.state).toBe("recovering");
    expect(hooks.map((hook) => hook.name)).toEqual([
      "model_call_started",
      "model_call_ended",
      "agent_end",
    ]);
  });

  it("delegates normal Direct finalization when no Host claim exists", () => {
    const { databasePath, store } = createStore();
    const accepted = store.accept({
      runId: "run-normal-finalize",
      ownerSessionKey: "agent:main:dashboard:normal",
      prompt: "ตอบเพียง NORMAL-FINALIZE เท่านั้น",
    });
    store.route(accepted.ticketId, false);

    installV091DirectModelCallLease({
      pluginConfig: { ticketDatabasePath: databasePath },
      on() {},
      logger: {},
    });

    expect(hostRecoveryOwnsRun(databasePath, "run-normal-finalize")).toBe(false);
    expect(store.finalizeDirectRun({
      runId: "run-normal-finalize",
      success: false,
      interrupted: false,
      message: "provider error",
    })).toBe("failed");

    const db = new DatabaseSync(databasePath, { readOnly: true });
    const status = (db.prepare("SELECT status FROM tickets WHERE ticket_id=?")
      .get(accepted.ticketId) as { status: string }).status;
    db.close();
    expect(status).toBe("failed");
  });
});
