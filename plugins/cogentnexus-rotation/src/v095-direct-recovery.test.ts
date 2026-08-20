import { existsSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it } from "vitest";
import {
  installV095DirectRecoveryLaneFence,
  withV095EphemeralEmbeddedSession,
} from "./v095-direct-recovery.js";

describe("v0.9.5 Direct Recovery compatibility boundaries", () => {
  it("supplies an isolated session key/file to embedded recovery and erases the transcript directory", async () => {
    let captured: any;
    let directoryDuringRun = "";
    const api = {
      runtime: {
        agent: {
          runEmbeddedAgent: async (input: any) => {
            captured = input;
            directoryDuringRun = dirname(input.sessionFile);
            expect(input.sessionKey).toMatch(/^temp:cogentnexus-direct-recovery:/u);
            expect(input.sessionFile).toMatch(/session\.jsonl$/u);
            expect(existsSync(directoryDuringRun)).toBe(true);
            expect(input.disableTrajectory).toBe(true);
            return { meta: { durationMs: 1 }, payloads: [{ text: "ok" }] };
          },
        },
      },
    };

    const wrapped = withV095EphemeralEmbeddedSession(api);
    await wrapped.runtime.agent.runEmbeddedAgent({
      sessionId: "cnx-direct-CNXT-test-1-g0",
      runId: "cnx-direct-CNXT-test-1-g0",
    });

    expect(captured.sessionKey).toBe("temp:cogentnexus-direct-recovery:cnx-direct-CNXT-test-1-g0");
    expect(directoryDuringRun).not.toBe("");
    expect(existsSync(directoryDuringRun)).toBe(false);
  });

  it("durably prevents legacy Direct-to-workflow promotion once Direct Recovery owns the Ticket", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v095-lane-"));
    const path = join(root, "tickets.sqlite3");
    try {
      const db = new DatabaseSync(path);
      db.exec(`
        CREATE TABLE tickets(
          ticket_id TEXT PRIMARY KEY,
          status TEXT NOT NULL,
          workflow_eligible INTEGER NOT NULL,
          workflow_id TEXT,
          failure_class TEXT,
          failure_message TEXT,
          updated_at TEXT NOT NULL
        );
        CREATE TABLE cnx_direct_recovery(
          ticket_id TEXT PRIMARY KEY,
          state TEXT NOT NULL
        );
      `);
      db.prepare("INSERT INTO tickets VALUES (?,'accepted',0,NULL,NULL,NULL,?)")
        .run("owned", new Date().toISOString());
      db.prepare("INSERT INTO tickets VALUES (?,'accepted',0,NULL,NULL,NULL,?)")
        .run("legacy", new Date().toISOString());
      db.prepare("INSERT INTO cnx_direct_recovery VALUES (?,'pending')").run("owned");
      db.close();

      installV095DirectRecoveryLaneFence(path);

      const writer = new DatabaseSync(path);
      const stamp = new Date().toISOString();
      const owned = writer.prepare(
        "UPDATE tickets SET status='waiting',workflow_eligible=1,failure_class='interrupted',failure_message='legacy promotion',updated_at=? WHERE ticket_id=? AND status='accepted' AND workflow_eligible=0",
      ).run(stamp, "owned");
      const legacy = writer.prepare(
        "UPDATE tickets SET status='waiting',workflow_eligible=1,failure_class='interrupted',failure_message='legacy promotion',updated_at=? WHERE ticket_id=? AND status='accepted' AND workflow_eligible=0",
      ).run(stamp, "legacy");

      expect(Number(owned.changes)).toBe(0);
      expect(Number(legacy.changes)).toBe(1);
      expect(writer.prepare("SELECT status,workflow_eligible,workflow_id FROM tickets WHERE ticket_id='owned'").get())
        .toMatchObject({ status: "accepted", workflow_eligible: 0, workflow_id: null });
      expect(writer.prepare("SELECT status,workflow_eligible FROM tickets WHERE ticket_id='legacy'").get())
        .toMatchObject({ status: "waiting", workflow_eligible: 1 });

      const linked = writer.prepare("UPDATE tickets SET workflow_id='CNX-AUTO-illegal' WHERE ticket_id='owned'")
        .run();
      expect(Number(linked.changes)).toBe(0);
      expect(writer.prepare("SELECT workflow_id FROM tickets WHERE ticket_id='owned'").get())
        .toMatchObject({ workflow_id: null });
      writer.close();
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});
