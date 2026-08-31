export type GuardAction = "CONTINUE" | "CHECKPOINT" | "HANDOFF" | "ROTATE";

export type SessionSnapshot = {
  key: string;
  parentSessionKey?: string;
  status?: string;
  updatedAt?: number;
  totalTokens?: number | null;
  totalTokensFresh?: boolean;
  contextTokens?: number | null;
  transcriptBytes?: number;
  compactionCount?: number;
  contextLengthExceeded?: boolean;
};

export type GuardPolicy = {
  softLimit: number;
  handoffLimit: number;
  criticalLimit: number;
  transcriptSoftBytes: number;
  transcriptHandoffBytes: number;
  transcriptCriticalBytes: number;
  compactionHandoffCount: number;
  compactionCriticalCount: number;
};

export const DEFAULT_GUARD_POLICY: GuardPolicy = {
  softLimit: 0.25,
  handoffLimit: 0.35,
  criticalLimit: 0.45,
  transcriptSoftBytes: 2 * 1024 * 1024,
  transcriptHandoffBytes: 4 * 1024 * 1024,
  transcriptCriticalBytes: 6 * 1024 * 1024,
  compactionHandoffCount: 1,
  compactionCriticalCount: 2,
};

const rank: Record<GuardAction, number> = { CONTINUE: 0, CHECKPOINT: 1, HANDOFF: 2, ROTATE: 3 };

function promote(current: GuardAction, candidate: GuardAction): GuardAction {
  return rank[candidate] > rank[current] ? candidate : current;
}

export function selectActiveDescendant(boundKey: string, sessions: SessionSnapshot[]): SessionSnapshot | undefined {
  const byKey = new Map(sessions.map((session) => [session.key, session]));
  const descendsFrom = (session: SessionSnapshot) => {
    const seen = new Set<string>();
    let parent = session.parentSessionKey;
    while (parent && !seen.has(parent)) {
      if (parent === boundKey) return true;
      seen.add(parent);
      parent = byKey.get(parent)?.parentSessionKey;
    }
    return false;
  };
  return sessions
    .filter((session) => session.key === boundKey || descendsFrom(session))
    .sort((a, b) => Number(b.status === "running") - Number(a.status === "running") || (b.updatedAt ?? 0) - (a.updatedAt ?? 0))[0];
}

export function assessSession(session: SessionSnapshot, policy: GuardPolicy = DEFAULT_GUARD_POLICY) {
  let action: GuardAction = "CONTINUE";
  const reasons: string[] = [];
  const used = session.totalTokens;
  const maximum = session.contextTokens;
  const ratio = session.totalTokensFresh === true && typeof used === "number" && typeof maximum === "number" && maximum > 0
    ? used / maximum
    : null;
  if (ratio !== null) {
    if (ratio >= policy.criticalLimit) action = promote(action, "ROTATE");
    else if (ratio >= policy.handoffLimit) action = promote(action, "HANDOFF");
    else if (ratio >= policy.softLimit) action = promote(action, "CHECKPOINT");
    if (action !== "CONTINUE") reasons.push(`token-ratio:${ratio.toFixed(6)}`);
  }
  const bytes = session.transcriptBytes ?? 0;
  if (bytes >= policy.transcriptCriticalBytes) action = promote(action, "ROTATE");
  else if (bytes >= policy.transcriptHandoffBytes) action = promote(action, "HANDOFF");
  else if (bytes >= policy.transcriptSoftBytes) action = promote(action, "CHECKPOINT");
  if (bytes >= policy.transcriptSoftBytes) reasons.push(`transcript-bytes:${bytes}`);
  const compactions = session.compactionCount ?? 0;
  if (compactions >= policy.compactionCriticalCount) action = promote(action, "ROTATE");
  else if (compactions >= policy.compactionHandoffCount) action = promote(action, "HANDOFF");
  if (compactions > 0) reasons.push(`compactions:${compactions}`);
  if (session.contextLengthExceeded) {
    action = "ROTATE";
    reasons.push("context-length-exceeded");
  }
  return { action, ratio, transcriptBytes: bytes, compactionCount: compactions, reasons };
}
