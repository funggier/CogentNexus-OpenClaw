import { afterEach, describe, expect, it, vi } from "vitest";
import { createDiscordActiveTypingManager, discordChannelIdFromSessionKey } from "./discord-active-typing.js";

describe("Discord active-run typing", () => {
  afterEach(() => {
    vi.useRealTimers();
  });

  it("extracts only canonical Discord channel session ids", () => {
    expect(discordChannelIdFromSessionKey("agent:main:discord:channel:1391855033993138217"))
      .toBe("1391855033993138217");
    expect(discordChannelIdFromSessionKey("agent:main:webchat:channel:1391855033993138217")).toBeUndefined();
    expect(discordChannelIdFromSessionKey("agent:main:discord:channel:not-a-number")).toBeUndefined();
  });

  it("starts only for an active Discord run, refreshes, and stops at terminal lifecycle", async () => {
    vi.useFakeTimers();
    const fetchImpl = vi.fn(async (_input: string, _init: any) => ({ ok: true, status: 204 }));
    const manager = createDiscordActiveTypingManager({
      fetchImpl,
      intervalMs: 8000,
      requestTimeoutMs: 5000,
      resolveToken: async () => "test-token",
    });

    expect(await manager.start({
      runId: "run-1",
      sessionKey: "agent:main:discord:channel:42",
      accountId: "default",
      cfg: {},
    })).toBe(true);
    expect(manager.activeCount()).toBe(1);
    expect(fetchImpl).toHaveBeenCalledTimes(1);
    expect(fetchImpl.mock.calls[0]?.[0]).toBe("https://discord.com/api/v10/channels/42/typing");
    expect(fetchImpl.mock.calls[0]?.[1]?.headers.Authorization).toBe("Bot test-token");

    await vi.advanceTimersByTimeAsync(8000);
    expect(fetchImpl).toHaveBeenCalledTimes(2);

    manager.stop("run-1");
    expect(manager.activeCount()).toBe(0);
    await vi.advanceTimersByTimeAsync(24000);
    expect(fetchImpl).toHaveBeenCalledTimes(2);
  });

  it("never emits typing for queued/non-Discord identities before active execution", async () => {
    vi.useFakeTimers();
    const fetchImpl = vi.fn(async (_input: string, _init: any) => ({ ok: true, status: 204 }));
    const manager = createDiscordActiveTypingManager({
      fetchImpl,
      resolveToken: async () => "test-token",
    });

    expect(await manager.start({ runId:"run-web", sessionKey:"agent:main:webchat:42", cfg:{} })).toBe(false);
    expect(await manager.start({ runId:"", sessionKey:"agent:main:discord:channel:42", cfg:{} })).toBe(false);
    expect(manager.activeCount()).toBe(0);
    expect(fetchImpl).not.toHaveBeenCalled();
  });

  it("uses the public OpenClaw SecretInput resolver for a configured Discord token", async () => {
    vi.useFakeTimers();
    const fetchImpl = vi.fn(async (_input: string, _init: any) => ({ ok: true, status: 204 }));
    const manager = createDiscordActiveTypingManager({ fetchImpl });

    expect(await manager.start({
      runId:"run-secret-input",
      sessionKey:"agent:main:discord:channel:123",
      accountId:"default",
      cfg:{ channels:{ discord:{ enabled:true, token:"plain-test-token" } } },
    })).toBe(true);
    expect(fetchImpl).toHaveBeenCalledTimes(1);
    manager.stopAll();
  });

  it("is idempotent per run and never logs or persists the credential", async () => {
    vi.useFakeTimers();
    const fetchImpl = vi.fn(async (_input: string, _init: any) => ({ ok: false, status: 429 }));
    const warn = vi.fn();
    const manager = createDiscordActiveTypingManager({
      fetchImpl,
      logger: { warn },
      resolveToken: async () => "secret-never-log",
    });

    const input = { runId:"run-2", sessionKey:"agent:main:discord:channel:99", cfg:{} };
    expect(await manager.start(input)).toBe(true);
    expect(await manager.start(input)).toBe(true);
    expect(manager.activeCount()).toBe(1);
    await Promise.resolve();
    expect(warn.mock.calls.flat().join(" ")).not.toContain("secret-never-log");
    manager.stopAll();
  });
});