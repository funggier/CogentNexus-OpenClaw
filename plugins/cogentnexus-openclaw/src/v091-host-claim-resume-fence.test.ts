import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { afterEach, describe, expect, it } from "vitest";

import { TicketStore } from "./ticket-store.js";
import {
  hostRecoveryOwnsResumeTag,
  installV091DirectModelCallLease,
  recordDirectModelCallStarted,
} from "./v091-direct-model-call-lease.js";

const tempDirs: string[] = [];

afterEach(() => {
  for (const dir of tempDirs.splice(0)) rmSync(dir, { recursive: true, force: true });
});

function fixture(runId: string) {
  const dir = mkdtempSync(join(tmpdir(), "cnxclaw-host-resume-fence-"));
  tempDirs.push(dir);
  const databasePath = join(dir, "tickets.sqlite3");
  const store = new TicketStore(databasePath);
  const ticket = store.accept({
    runId,
    ownerSessionKey: "agent:main:dashboard:resume-fence",
    prompt: "work",
  });
  store.route(ticket.ticketId, false);
  recordDirectModelCallStarted(databasePath, {
    runId,
    callId: "call-1",
    now: new Date("2026-08-18T13:00:00.000Z"),
  });
  return { databasePath, ticketId: ticket.ticketId };
}

describe("Host Direct recovery legacy auto-resume fence", () => {
  it("suppresses cogent-resume scheduling while Host owns the run", async () => {
    const runId = "run-host-resume";
    const { databasePath, ticketId } = fixture(runId);
    const db = new DatabaseSync(databasePath);
    db.prepare(
      "UPDATE cnx_direct_model_call SET state='recovering',recovery_started_at=?,updated_at=? WHERE ticket_id=?",
    ).run(
      "2026-08-18T13:16:00.000Z",
      "2026-08-18T13:16:00.000Z",
      ticketId,
    );
    db.close();

    const delegated: any[] = [];
    const workflow = {
      async scheduleSessionTurn(input: any) {
        delegated.push(input);
        return { scheduled: true };
      },
    };
    installV091DirectModelCallLease({
      pluginConfig: { ticketDatabasePath: databasePath },
      session: { workflow },
      on() {},
      logger: {},
    });

    const tag = "cogent-resume-run-host-resume";
    expect(hostRecoveryOwnsResumeTag(databasePath, tag)).toBe(true);
    await expect(workflow.scheduleSessionTurn({ tag, sessionKey: "owner" }))
      .resolves.toEqual({
        scheduled: false,
        suppressed: true,
        reason: "host-direct-model-recovery-claim",
      });
    expect(delegated).toEqual([]);
  });

  it("delegates unrelated and unclaimed resume scheduling", async () => {
    const runId = "run-unclaimed-resume";
    const { databasePath } = fixture(runId);
    const delegated: any[] = [];
    const workflow = {
      async scheduleSessionTurn(input: any) {
        delegated.push(input);
        return { scheduled: true, tag: input.tag };
      },
    };
    installV091DirectModelCallLease({
      pluginConfig: { ticketDatabasePath: databasePath },
      session: { workflow },
      on() {},
      logger: {},
    });

    await expect(workflow.scheduleSessionTurn({
      tag: "cogent-resume-run-unclaimed-resume",
      sessionKey: "owner",
    })).resolves.toEqual({
      scheduled: true,
      tag: "cogent-resume-run-unclaimed-resume",
    });
    await expect(workflow.scheduleSessionTurn({
      tag: "other-tag",
      sessionKey: "owner",
    })).resolves.toEqual({ scheduled: true, tag: "other-tag" });
    expect(delegated).toHaveLength(2);
  });
});
