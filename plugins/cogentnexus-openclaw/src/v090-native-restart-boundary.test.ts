import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { describe, expect, it, vi } from "vitest";
import { TicketStore } from "./ticket-store.js";
import {
  OPENCLAW_MAIN_RESTART_RECOVERY_PROMPT,
  installNativeRestartRecoveryBoundary,
  isOpenClawMainRestartRecoveryPrompt,
  reconcileNativeRestartRecoveryTickets,
} from "./v090-native-restart-boundary.js";

describe("CogentNexus-OpenClaw v0.9 native main-session restart boundary", () => {
  it("recognizes only the canonical OpenClaw restart recovery shape", () => {
    expect(isOpenClawMainRestartRecoveryPrompt(OPENCLAW_MAIN_RESTART_RECOVERY_PROMPT)).toBe(true);
    expect(isOpenClawMainRestartRecoveryPrompt(
      `${OPENCLAW_MAIN_RESTART_RECOVERY_PROMPT}\n\nNote: The interrupted final reply was captured: \"partial answer\"`,
    )).toBe(true);
    expect(isOpenClawMainRestartRecoveryPrompt(
      "My previous turn was interrupted by a gateway restart. Please continue it.",
    )).toBe(false);
    expect(isOpenClawMainRestartRecoveryPrompt(
      `${OPENCLAW_MAIN_RESTART_RECOVERY_PROMPT} Please also do something new.`,
    )).toBe(false);
  });

  it("blocks the native recovery before Ticket-first admission and suppresses transcript/output noise", () => {
    const registrations: Array<{name:string;handler:any;options:any}> = [];
    const api = {
      on: vi.fn((name:string, handler:any, options:any) => registrations.push({ name, handler, options })),
    };
    installNativeRestartRecoveryBoundary(api);

    const gate = registrations.find((item) => item.name === "before_agent_run")!;
    expect(gate.options.priority).toBe(10_000);
    expect(gate.handler(
      { prompt:OPENCLAW_MAIN_RESTART_RECOVERY_PROMPT },
      { sessionKey:"agent:main:dashboard:owner", runId:"native-recovery-run" },
    )).toMatchObject({ outcome:"block", category:"cnxclaw_native_restart_recovery_fence" });

    const write = registrations.find((item) => item.name === "before_message_write")!;
    expect(write.handler({
      sessionKey:"agent:main:dashboard:owner",
      message:{ role:"user", content:OPENCLAW_MAIN_RESTART_RECOVERY_PROMPT },
    }, {})).toEqual({ block:true });

    const reply = registrations.find((item) => item.name === "reply_payload_sending")!;
    expect(reply.handler({ runId:"native-recovery-run" })).toMatchObject({ cancel:true });

    expect(gate.handler(
      { prompt:"Fresh human request after restart" },
      { sessionKey:"agent:main:dashboard:owner", runId:"fresh-human" },
    )).toEqual({ outcome:"pass" });
    expect(reply.handler({ runId:"fresh-human" })).toBeUndefined();
  });

  it("does not classify hidden subagent work as owner restart recovery admission", () => {
    const registrations: Array<{name:string;handler:any;options:any}> = [];
    installNativeRestartRecoveryBoundary({
      on: (name:string, handler:any, options:any) => registrations.push({ name, handler, options }),
    });
    const gate = registrations.find((item) => item.name === "before_agent_run")!;
    expect(gate.handler(
      { prompt:OPENCLAW_MAIN_RESTART_RECOVERY_PROMPT },
      { sessionKey:"agent:main:subagent:cnx-test", runId:"hidden" },
    )).toEqual({ outcome:"pass" });
  });

  it("migrates the exact live synthetic Ticket without touching fresh human work", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v090-native-restart-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const synthetic = store.accept({
        runId:"b02d41de-b470-4655-acd1-166f4ba6c76a",
        ownerSessionKey:"agent:main:dashboard:677bd15a-3459-4c29-9426-569b97b03dcc",
        prompt:OPENCLAW_MAIN_RESTART_RECOVERY_PROMPT,
      });
      store.route(synthetic.ticketId, false);
      const human = store.accept({
        runId:"fresh-human",
        ownerSessionKey:"agent:main:dashboard:677bd15a-3459-4c29-9426-569b97b03dcc",
        prompt:"Continue my project, but this is a real human request.",
      });
      store.route(human.ticketId, false);

      const result = reconcileNativeRestartRecoveryTickets(path);
      expect(result.cancelled).toBe(1);

      const db = new DatabaseSync(path, { readOnly:true });
      expect(db.prepare("SELECT status,failure_class FROM tickets WHERE ticket_id=?").get(synthetic.ticketId))
        .toEqual({ status:"cancelled", failure_class:null });
      expect(db.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(human.ticketId))
        .toEqual({ status:"accepted" });
      expect(db.prepare("SELECT count(*) AS count FROM ticket_events WHERE ticket_id=? AND event_type='native_restart_recovery_suppressed'").get(synthetic.ticketId))
        .toEqual({ count:1 });
      db.close();

      expect(reconcileNativeRestartRecoveryTickets(path).cancelled).toBe(0);
    } finally {
      rmSync(root, { recursive:true, force:true });
    }
  });

  it("keeps two sessions isolated while suppressing a synthetic recovery in only one", () => {
    const root = mkdtempSync(join(tmpdir(), "cnx-v090-native-restart-multisession-"));
    try {
      const path = join(root, "tickets.sqlite3");
      const store = new TicketStore(path);
      const a = store.accept({ runId:"recovery-a", ownerSessionKey:"agent:main:dashboard:A", prompt:OPENCLAW_MAIN_RESTART_RECOVERY_PROMPT });
      const b = store.accept({ runId:"human-b", ownerSessionKey:"agent:main:dashboard:B", prompt:"real work in B" });
      store.route(a.ticketId, false);
      store.route(b.ticketId, false);

      expect(reconcileNativeRestartRecoveryTickets(path).cancelled).toBe(1);
      const db = new DatabaseSync(path, { readOnly:true });
      expect(db.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(a.ticketId)).toEqual({ status:"cancelled" });
      expect(db.prepare("SELECT status FROM tickets WHERE ticket_id=?").get(b.ticketId)).toEqual({ status:"accepted" });
      db.close();
    } finally {
      rmSync(root, { recursive:true, force:true });
    }
  });
});
