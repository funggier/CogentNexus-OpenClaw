import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { afterEach, describe, expect, it, vi } from "vitest";
import {
  OPENCLAW_NATIVE_RESTART_RESUME_BODY,
  OPENCLAW_QUEUED_USER_PREFIX,
  authoritativeCnxDirectRecovery,
  installV099NativeRestartOwnershipFence,
  isOpenClawNativeRestartDispatch,
} from "./v099-native-restart-ownership.js";

const TEST_ORIGINAL_PROMPT = "CNX-V099-FIXTURE-ORIGINAL";

const dirs: string[] = [];
afterEach(() => {
  vi.restoreAllMocks();
  for (const dir of dirs.splice(0)) rmSync(dir, { recursive: true, force: true });
});

function fixture() {
  const dir = mkdtempSync(join(tmpdir(), "cnx-v099-"));
  dirs.push(dir);
  const path = join(dir, "cogentnexus-openclaw.sqlite3");
  const db = new DatabaseSync(path);

  db.exec(`
    CREATE TABLE tickets (
      ticket_id TEXT PRIMARY KEY,
      owner_session_key TEXT NOT NULL,
      prompt TEXT NOT NULL,
      status TEXT NOT NULL,
      workflow_eligible INTEGER NOT NULL,
      workflow_id TEXT,
      created_at TEXT NOT NULL
    );
    CREATE TABLE cnx_sessions (
      session_key TEXT PRIMARY KEY,
      state TEXT NOT NULL,
      generation INTEGER NOT NULL
    );
    CREATE TABLE cnx_direct_recovery (
      ticket_id TEXT PRIMARY KEY,
      mode TEXT NOT NULL,
      state TEXT NOT NULL,
      owner_generation INTEGER NOT NULL,
      next_attempt_at TEXT,
      created_at TEXT NOT NULL
    );
    CREATE TABLE cnx_direct_model_call (
      ticket_id TEXT NOT NULL,
      state TEXT NOT NULL,
      outcome TEXT
    );
  `);

  const sessionKey = "agent:main:dashboard:test-owner";
  db.prepare(
    "INSERT INTO cnx_sessions(session_key,state,generation) VALUES(?,?,?)",
  ).run(sessionKey, "active", 0);
  db.prepare(
    `INSERT INTO tickets(
       ticket_id,owner_session_key,prompt,status,workflow_eligible,workflow_id,created_at
     ) VALUES(?,?,?,?,?,?,?)`,
  ).run(
    "CNXT-parent",
    sessionKey,
    TEST_ORIGINAL_PROMPT,
    "accepted",
    0,
    null,
    "2026-08-20T00:00:00Z",
  );
  db.prepare(
    `INSERT INTO cnx_direct_recovery(
       ticket_id,mode,state,owner_generation,next_attempt_at,created_at
     ) VALUES(?,?,?,?,?,?)`,
  ).run("CNXT-parent", "resume", "running", 0, null, "2026-08-20T00:00:01Z");
  db.prepare(
    "INSERT INTO cnx_direct_model_call(ticket_id,state,outcome) VALUES(?,?,?)",
  ).run("CNXT-parent", "interrupted", "host-timeout-authorized");

  db.close();
  return { dir, path, sessionKey };
}

describe("v0.9.9 native restart ownership fence", () => {
  it("matches only the exact OpenClaw restart continuation shape", () => {
    expect(isOpenClawNativeRestartDispatch(OPENCLAW_NATIVE_RESTART_RESUME_BODY)).toBe(true);
    expect(
      isOpenClawNativeRestartDispatch(
        `[System] ${OPENCLAW_NATIVE_RESTART_RESUME_BODY}`,
      ),
    ).toBe(true);
    expect(isOpenClawNativeRestartDispatch("gateway restart happened")).toBe(false);
    expect(
      isOpenClawNativeRestartDispatch(
        `Please explain: ${OPENCLAW_NATIVE_RESTART_RESUME_BODY}`,
      ),
    ).toBe(false);
  });

  it("recognizes same-session Host-authorized pending/running Direct recovery", () => {
    const { path, sessionKey } = fixture();
    expect(authoritativeCnxDirectRecovery(path, sessionKey)).toEqual({
      ticketId: "CNXT-parent",
      recoveryState: "running",
      ownerGeneration: 0,
      originalPrompt: TEST_ORIGINAL_PROMPT,
    });
  });

  it("does not claim authority for another session", () => {
    const { path } = fixture();
    expect(
      authoritativeCnxDirectRecovery(path, "agent:main:dashboard:other"),
    ).toBeUndefined();
  });

  it("does not claim authority after Direct recovery becomes terminal", () => {
    const { path, sessionKey } = fixture();
    const db = new DatabaseSync(path);
    db.prepare("UPDATE cnx_direct_recovery SET state='done' WHERE ticket_id=?").run(
      "CNXT-parent",
    );
    db.close();
    expect(authoritativeCnxDirectRecovery(path, sessionKey)).toBeUndefined();
  });

  it("does not claim authority across owner-generation drift", () => {
    const { path, sessionKey } = fixture();
    const db = new DatabaseSync(path);
    db.prepare("UPDATE cnx_sessions SET generation=1 WHERE session_key=?").run(
      sessionKey,
    );
    db.close();
    expect(authoritativeCnxDirectRecovery(path, sessionKey)).toBeUndefined();
  });

  it("does not suppress when original model call lacks Host timeout authority", () => {
    const { path, sessionKey } = fixture();
    const db = new DatabaseSync(path);
    db.prepare("UPDATE cnx_direct_model_call SET outcome='other' WHERE ticket_id=?").run(
      "CNXT-parent",
    );
    db.close();
    expect(authoritativeCnxDirectRecovery(path, sessionKey)).toBeUndefined();
  });

  it("fails open to native recovery on unreadable/missing DB", () => {
    expect(
      authoritativeCnxDirectRecovery(
        join(tmpdir(), "cnx-v099-does-not-exist.sqlite3"),
        "agent:main:dashboard:x",
      ),
    ).toBeUndefined();
  });

  it("consumes exact native restart dispatch when CNXCLAW owns recovery", () => {
    const { dir, sessionKey } = fixture();
    let handler: ((event: any, ctx: any) => any) | undefined;
    let options: any;
    const info = vi.fn();
    const api = {
      config: { agents: { defaults: { workspace: dir } } },
      logger: { info },
      on: vi.fn((name: string, fn: any, opts: any) => {
        expect(name).toBe("before_agent_run");
        handler = fn;
        options = opts;
      }),
    };

    installV099NativeRestartOwnershipFence(api, {
      workspaceDir: dir,
      ticketDatabasePath: join(dir, "cogentnexus-openclaw.sqlite3"),
    });

    expect(options?.priority).toBe(20_000);
    expect(handler).toBeDefined();
    expect(
      handler?.(
        { prompt: `[System] ${OPENCLAW_NATIVE_RESTART_RESUME_BODY}`, sessionKey },
        { sessionKey },
      ),
    ).toMatchObject({ outcome: "block", category: "cogentnexus_v099_native_restart_ownership" });
    expect(info).toHaveBeenCalledWith(
      expect.stringContaining("suppressed OpenClaw native restart recovery"),
    );
  });

  it("passes ordinary messages even while CNXCLAW owns recovery", () => {
    const { dir, sessionKey } = fixture();
    let handler: ((event: any, ctx: any) => any) | undefined;
    const api = {
      config: { agents: { defaults: { workspace: dir } } },
      logger: { info: vi.fn() },
      on: (_name: string, fn: any) => {
        handler = fn;
      },
    };
    installV099NativeRestartOwnershipFence(api, {
      workspaceDir: dir,
      ticketDatabasePath: join(dir, "cogentnexus-openclaw.sqlite3"),
    });
    expect(handler?.({ content: "normal user message", sessionKey }, { sessionKey })).toBeUndefined();
  });

  it("recognizes the queued-user restart envelope observed in Test A v12", () => {
    const content =
      `${OPENCLAW_QUEUED_USER_PREFIX}${TEST_ORIGINAL_PROMPT}` +
      `\n\n[System] ${OPENCLAW_NATIVE_RESTART_RESUME_BODY}`;

    expect(isOpenClawNativeRestartDispatch(content)).toBe(true);
  });

  it("consumes queued restart only when queued prompt matches durable original", () => {
    const { dir, path, sessionKey } = fixture();

    let handler: ((event: any, ctx: any) => any) | undefined;
    const info = vi.fn();

    const api = {
      config: { agents: { defaults: { workspace: dir } } },
      logger: { info },
      on: (name: string, fn: any, opts: any) => {
        expect(name).toBe("before_agent_run");
        expect(opts?.priority).toBe(20_000);
        handler = fn;
      },
    };

    installV099NativeRestartOwnershipFence(api, {
      workspaceDir: dir,
      ticketDatabasePath: path,
    });

    const exactEnvelope =
      `${OPENCLAW_QUEUED_USER_PREFIX}${TEST_ORIGINAL_PROMPT}` +
      `\n\n[System] ${OPENCLAW_NATIVE_RESTART_RESUME_BODY}`;

    expect(
      handler?.(
        { prompt: exactEnvelope, sessionKey },
        { sessionKey },
      ),
    ).toMatchObject({ outcome: "block", category: "cogentnexus_v099_native_restart_ownership" });

    const genuinelyNewEnvelope =
      `${OPENCLAW_QUEUED_USER_PREFIX}GENUINELY-NEW-USER-MESSAGE` +
      `\n\n[System] ${OPENCLAW_NATIVE_RESTART_RESUME_BODY}`;

    expect(
      handler?.(
        { prompt: genuinelyNewEnvelope, sessionKey },
        { sessionKey },
      ),
    ).toBeUndefined();

    expect(info).toHaveBeenCalledTimes(1);
  });
});
