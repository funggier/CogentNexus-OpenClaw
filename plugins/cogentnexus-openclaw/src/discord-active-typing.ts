import { resolveConfiguredSecretInputString } from "openclaw/plugin-sdk/secret-input-runtime";

type TypingFetchResponse = { ok: boolean; status: number };
type TypingFetch = (
  input: string,
  init: { method: string; headers: Record<string, string>; signal: AbortSignal },
) => Promise<TypingFetchResponse>;

type TypingLogger = {
  warn?: (message: string) => void;
  info?: (message: string) => void;
};

type DiscordTokenResolver = (params: { cfg: any; accountId?: string | null }) => Promise<string | undefined>;

async function resolveDiscordToken(params: { cfg: any; accountId?: string | null }): Promise<string | undefined> {
  const discord = params.cfg?.channels?.discord;
  if (!discord || discord.enabled === false) return undefined;
  const accountId = typeof params.accountId === "string" ? params.accountId.trim() : "";
  const account = accountId && discord.accounts && typeof discord.accounts === "object"
    ? discord.accounts[accountId]
    : undefined;
  if (account?.enabled === false) return undefined;
  const value = account?.token ?? discord.token;
  const path = account?.token !== undefined
    ? `channels.discord.accounts.${accountId}.token`
    : "channels.discord.token";
  if (value === undefined || value === null || value === "") return undefined;
  const resolved = await resolveConfiguredSecretInputString({
    config: params.cfg,
    env: process.env,
    value,
    path,
  });
  return typeof resolved.value === "string" && resolved.value.trim() ? resolved.value.trim() : undefined;
}

export type DiscordActiveTypingManager = {
  start(input: { runId: string; sessionKey?: string; accountId?: string | null; cfg: any }): Promise<boolean>;
  stop(runId: string): void;
  stopAll(): void;
  activeCount(): number;
};

type ActiveTypingState = {
  runId: string;
  channelId: string;
  token: string;
  stopped: boolean;
  inFlight: boolean;
  interval?: ReturnType<typeof setInterval>;
  requestAbort?: AbortController;
  requestTimeout?: ReturnType<typeof setTimeout>;
  lifetime?: ReturnType<typeof setTimeout>;
  lastFailure?: string;
};

export function discordChannelIdFromSessionKey(sessionKey?: string): string | undefined {
  const value = typeof sessionKey === "string" ? sessionKey.trim() : "";
  const match = /^agent:[^:]+:discord:channel:(\d+)$/u.exec(value);
  return match?.[1];
}

export function createDiscordActiveTypingManager(options: {
  fetchImpl?: TypingFetch;
  resolveToken?: DiscordTokenResolver;
  intervalMs?: number;
  requestTimeoutMs?: number;
  maxDurationMs?: number;
  logger?: TypingLogger;
} = {}): DiscordActiveTypingManager {
  const fetchImpl = options.fetchImpl ?? (globalThis.fetch as unknown as TypingFetch);
  const resolveToken = options.resolveToken ?? resolveDiscordToken;
  const intervalMs = Math.max(1000, options.intervalMs ?? 8000);
  const requestTimeoutMs = Math.max(1000, options.requestTimeoutMs ?? 5000);
  const maxDurationMs = Math.max(intervalMs, options.maxDurationMs ?? 30 * 60 * 1000);
  const logger = options.logger;
  const active = new Map<string, ActiveTypingState>();

  const stop = (runId: string) => {
    const state = active.get(runId);
    if (!state) return;
    state.stopped = true;
    if (state.interval) clearInterval(state.interval);
    if (state.requestTimeout) clearTimeout(state.requestTimeout);
    if (state.lifetime) clearTimeout(state.lifetime);
    state.requestAbort?.abort();
    active.delete(runId);
  };

  const send = async (state: ActiveTypingState) => {
    if (state.stopped || state.inFlight) return;
    state.inFlight = true;
    const controller = new AbortController();
    state.requestAbort = controller;
    const timeout = setTimeout(() => controller.abort(), requestTimeoutMs);
    timeout.unref?.();
    state.requestTimeout = timeout;
    try {
      const response = await fetchImpl(
        `https://discord.com/api/v10/channels/${encodeURIComponent(state.channelId)}/typing`,
        {
          method: "POST",
          headers: { Authorization: `Bot ${state.token}` },
          signal: controller.signal,
        },
      );
      if (!response.ok) {
        const failure = `http:${response.status}`;
        if (state.lastFailure !== failure) {
          logger?.warn?.(
            `CogentNexus-OpenClaw Discord active-run typing failed for run ${state.runId}: HTTP ${response.status}`,
          );
          state.lastFailure = failure;
        }
      } else {
        state.lastFailure = undefined;
      }
    } catch (error) {
      if (!state.stopped && !controller.signal.aborted) {
        const failure = error instanceof Error ? error.message : String(error);
        if (state.lastFailure !== failure) {
          logger?.warn?.(
            `CogentNexus-OpenClaw Discord active-run typing failed for run ${state.runId}: ${failure}`,
          );
          state.lastFailure = failure;
        }
      }
    } finally {
      clearTimeout(timeout);
      if (state.requestTimeout === timeout) state.requestTimeout = undefined;
      if (state.requestAbort === controller) state.requestAbort = undefined;
      state.inFlight = false;
    }
  };

  return {
    async start(input) {
      const runId = input.runId.trim();
      if (!runId || active.has(runId)) return Boolean(runId && active.has(runId));
      const channelId = discordChannelIdFromSessionKey(input.sessionKey);
      if (!channelId) return false;

      let token: string | undefined;
      try {
        token = await resolveToken({ cfg: input.cfg, accountId: input.accountId });
      } catch (error) {
        logger?.warn?.(
          `CogentNexus-OpenClaw Discord active-run typing credential resolution failed for run ${runId}: ${error instanceof Error ? error.message : String(error)}`,
        );
        return false;
      }
      if (!token || typeof fetchImpl !== "function") return false;

      const state: ActiveTypingState = {
        runId,
        channelId,
        token,
        stopped: false,
        inFlight: false,
      };
      active.set(runId, state);
      void send(state);
      const interval = setInterval(() => void send(state), intervalMs);
      interval.unref?.();
      state.interval = interval;
      const lifetime = setTimeout(() => stop(runId), maxDurationMs);
      lifetime.unref?.();
      state.lifetime = lifetime;
      return true;
    },
    stop,
    stopAll() {
      for (const runId of [...active.keys()]) stop(runId);
    },
    activeCount() {
      return active.size;
    },
  };
}