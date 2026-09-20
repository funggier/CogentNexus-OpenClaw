type SessionRuntimeApi = {
  resolveStorePath?: (store?: string, opts?: { agentId?: string }) => string;
  getSessionEntry?: (params: Record<string, unknown>) => any;
  patchSessionEntry?: (params: Record<string, unknown>) => Promise<any>;
  listSessionEntries?: (params?: Record<string, unknown>) => Array<{ sessionKey: string; entry: any }>;
};

function agentIdFromSessionKey(sessionKey: string): string | undefined {
  const match = /^agent:([^:]+):/u.exec(sessionKey.trim());
  return match?.[1];
}

export function ownerConversationSessionEligible(sessionKey: string | undefined): boolean {
  const key = typeof sessionKey === "string" ? sessionKey.trim() : "";
  if (!key || !/^agent:[^:]+:/u.test(key)) return false;
  const lower = key.toLowerCase();
  if (lower.includes(":subagent:")) return false;
  if (/^agent:[^:]+:cron:/u.test(lower)) return false;
  if (/^agent:[^:]+:heartbeat:/u.test(lower)) return false;
  if (/^agent:[^:]+:cogent-rotate(?:[:_-]|$)/u.test(lower)) return false;
  return true;
}

export async function enforceOwnerSessionFollowupQueue(api: any, sessionKey: string) {
  if (!ownerConversationSessionEligible(sessionKey)) {
    return { state: "skipped" as const, reason: "ineligible-session" as const };
  }
  const sessionApi: SessionRuntimeApi | undefined = api?.runtime?.agent?.session;
  if (!sessionApi?.getSessionEntry || !sessionApi?.patchSessionEntry) {
    return { state: "skipped" as const, reason: "session-api-unavailable" as const };
  }
  const agentId = agentIdFromSessionKey(sessionKey);
  const storePath = sessionApi.resolveStorePath?.(undefined, { agentId });
  const params = { sessionKey, agentId, ...(storePath ? { storePath } : {}), readConsistency: "latest" as const };
  const entry = sessionApi.getSessionEntry(params);
  if (!entry) return { state: "missing" as const, sessionKey };
  if (entry.queueMode === "followup") {
    return { state: "unchanged" as const, sessionKey, queueMode: "followup" as const };
  }
  const updated = await sessionApi.patchSessionEntry({
    ...params,
    preserveActivity: true,
    update: () => ({ queueMode: "followup" }),
  });
  if (!updated) return { state: "missing" as const, sessionKey };
  return { state: "updated" as const, sessionKey, queueMode: "followup" as const };
}

export async function reconcileOwnerSessionFollowupQueues(api: any) {
  const sessionApi: SessionRuntimeApi | undefined = api?.runtime?.agent?.session;
  if (!sessionApi?.listSessionEntries) return { scanned: 0, updated: 0, skipped: 0 };
  const entries = sessionApi.listSessionEntries({ readOnly: true, readConsistency: "latest" }) ?? [];
  let updated = 0;
  let skipped = 0;
  for (const item of entries) {
    if (!ownerConversationSessionEligible(item?.sessionKey)) {
      skipped += 1;
      continue;
    }
    const result = await enforceOwnerSessionFollowupQueue(api, item.sessionKey);
    if (result.state === "updated") updated += 1;
  }
  return { scanned: entries.length, updated, skipped };
}

export function installV095SessionSerialization(api: any) {
  const apply = async (sessionKey: string | undefined) => {
    if (!sessionKey) return;
    try {
      const result = await enforceOwnerSessionFollowupQueue(api, sessionKey);
      if (result.state === "updated") {
        api.logger?.info?.(`CogentNexus-OpenClaw session serialization set followup queue mode for ${sessionKey}`);
      }
    } catch (error) {
      api.logger?.warn?.(`CogentNexus-OpenClaw session serialization failed for ${sessionKey}: ${error instanceof Error ? error.message : String(error)}`);
    }
  };

  api.on?.("session_start", async (event: any, ctx: any) => {
    await apply(event?.sessionKey ?? ctx?.sessionKey);
  }, { priority: 2500, timeoutMs: 10_000, registrationId: "cogentnexus-openclaw-v095-session-followup" });

  api.registerService?.({
    id: "cogentnexus-openclaw-session-serialization",
    start: async () => {
      try {
        const result = await reconcileOwnerSessionFollowupQueues(api);
        api.logger?.info?.(
          `CogentNexus-OpenClaw session serialization baseline: scanned=${result.scanned} updated=${result.updated} skipped=${result.skipped}`,
        );
      } catch (error) {
        api.logger?.warn?.(`CogentNexus-OpenClaw session serialization baseline failed: ${error instanceof Error ? error.message : String(error)}`);
      }
    },
    stop: async () => {},
  });
}
