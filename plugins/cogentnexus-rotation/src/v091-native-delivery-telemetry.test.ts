import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterEach, describe, expect, it, vi } from "vitest";
import {
  buildV091DeliveryTelemetryRecord,
  installV091NativeDeliveryTelemetry,
  v091DeliveryTelemetryPath,
} from "./v091-native-delivery-telemetry.js";

const dirs: string[] = [];

afterEach(() => {
  vi.restoreAllMocks();
  for (const dir of dirs.splice(0)) rmSync(dir, { recursive: true, force: true });
});

function tempRoot() {
  const dir = mkdtempSync(join(tmpdir(), "cnx-v091-delivery-telemetry-"));
  dirs.push(dir);
  return dir;
}

describe("v0.9.1 native delivery hook telemetry", () => {
  it("records delivery correlation metadata without raw prompt/reply/error text", () => {
    const secretPrompt = "สวัสดีครับ SECRET-PROMPT";
    const secretReply = "SECRET-REPLY ไม่ควรถูกบันทึก";
    const secretError = "SECRET-ERROR";
    const record = buildV091DeliveryTelemetryRecord(
      "reply_payload_sending",
      {
        runId: "run-1",
        sessionKey: "agent:main:dashboard:test",
        payload: { text: secretReply, mediaUrls: [] },
        prompt: secretPrompt,
        error: secretError,
        success: true,
      },
      {
        sessionKey: "agent:main:dashboard:test",
        channelId: "webchat",
        conversationId: "conversation-1",
      },
      new Date("2026-08-20T00:00:00.000Z"),
    );

    const serialized = JSON.stringify(record);
    expect(serialized).not.toContain(secretPrompt);
    expect(serialized).not.toContain(secretReply);
    expect(serialized).not.toContain(secretError);
    expect(record.payload.text).toMatchObject({ present: true, chars: secretReply.length });
    expect(record.payload.text.sha256).toMatch(/^[a-f0-9]{64}$/u);
    expect(record.error?.sha256).toMatch(/^[a-f0-9]{64}$/u);
    expect(record.eventRunId).toBe("run-1");
    expect(record.eventSessionKey).toBe("agent:main:dashboard:test");
  });

  it("registers observation-only hooks and writes UTF-8 JSONL", () => {
    const root = tempRoot();
    const handlers = new Map<string, { fn: (event: any, ctx: any) => unknown; options: any }>();
    const api = {
      on: vi.fn((name: string, fn: any, options: any) => {
        handlers.set(name, { fn, options });
      }),
    };

    installV091NativeDeliveryTelemetry(api, root);

    expect([...handlers.keys()].sort()).toEqual([
      "agent_end",
      "before_agent_run",
      "message_sent",
      "model_call_ended",
      "model_call_started",
      "reply_dispatch",
      "reply_payload_sending",
    ]);

    const reply = handlers.get("reply_payload_sending");
    expect(reply?.options?.priority).toBe(-20_000);
    expect(
      reply?.fn(
        {
          runId: "run-telemetry",
          sessionKey: "agent:main:dashboard:telemetry",
          payload: { text: "PRIVATE-REPLY" },
        },
        { sessionKey: "agent:main:dashboard:telemetry", channelId: "webchat" },
      ),
    ).toBeUndefined();

    const path = v091DeliveryTelemetryPath(root);
    const text = readFileSync(path, "utf8");
    expect(text).not.toContain("PRIVATE-REPLY");
    const parsed = JSON.parse(text.trim());
    expect(parsed.hook).toBe("reply_payload_sending");
    expect(parsed.eventRunId).toBe("run-telemetry");
    expect(parsed.payload.text.sha256).toMatch(/^[a-f0-9]{64}$/u);
  });
});
