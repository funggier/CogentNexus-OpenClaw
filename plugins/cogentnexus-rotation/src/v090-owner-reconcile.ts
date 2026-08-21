import { spawnSync } from "node:child_process";
import { existsSync, readFileSync, renameSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { deleteSessionByKey, finalizeSessionDeletion } from "./v090.js";
import { TicketStore } from "./ticket-store.js";

type OwnerReconcileConfig = {
  pythonCommand?: string;
};

function activeOwnerSessionKeys(databasePath: string) {
  new TicketStore(databasePath).snapshot();
  const db = new DatabaseSync(databasePath, { readOnly:true });
  try {
    const sessionTable = db.prepare("SELECT 1 FROM sqlite_master WHERE type='table' AND name='cnx_sessions'").get();
    if (sessionTable) {
      return (db.prepare("SELECT session_key FROM cnx_sessions WHERE state='active' ORDER BY session_key").all() as Array<{session_key:string}>)
        .map((row) => row.session_key)
        .filter(Boolean);
    }
    return (db.prepare("SELECT DISTINCT owner_session_key FROM tickets WHERE owner_session_key<>'' ORDER BY owner_session_key").all() as Array<{owner_session_key:string}>)
      .map((row) => row.owner_session_key)
      .filter(Boolean);
  } finally { db.close(); }
}

function suppressWorkflowCompletion(workspaceDir: string, workflowId: string, reason: string) {
  const path = resolve(workspaceDir, ".cogent", "workflows", workflowId, "completion.json");
  if (!existsSync(path)) return;
  try {
    const value = JSON.parse(readFileSync(path, "utf8"));
    if (value?.deliveryStatus === "delivered") return;
    value.deliveryStatus = "delivered";
    value.deliveredAt = new Date().toISOString();
    value.suppressedBy = "owner-session-missing";
    value.suppressionReason = reason;
    delete value.scheduledAt;
    delete value.deliveryRunId;
    const temporary = `${path}.${process.pid}.owner-missing.tmp`;
    writeFileSync(temporary, `${JSON.stringify(value, null, 2)}\n`);
    renameSync(temporary, path);
  } catch {}
}

function cancelWorkflow(workspaceDir: string, workflowId: string, reason: string, config: OwnerReconcileConfig) {
  if (!/^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/u.test(workflowId)) return { ok:false, error:"invalid workflow id" };
  const runtime = resolve(workspaceDir, "skills", "cogentnexus", "scripts", "workflow.py");
  const result = spawnSync(config.pythonCommand ?? "python", [runtime, "--root", workspaceDir, "cancel", workflowId, "--reason", reason], {
    encoding:"utf8", windowsHide:true, timeout:30_000,
  });
  const ok = !result.error && result.status === 0;
  if (ok) suppressWorkflowCompletion(workspaceDir, workflowId, reason);
  return {
    ok,
    error:ok ? undefined : (result.error?.message ?? result.stderr ?? result.stdout ?? "workflow cancellation failed").trim().slice(0,2000),
  };
}

function agentIdFromSessionKey(sessionKey: string): string | undefined {
  return /^agent:([^:]+):/u.exec(sessionKey)?.[1];
}

/**
 * Reconcile CNX owner tombstones against OpenClaw's supported plugin session
 * accessor. Do not use runtime.gateway.request(): OpenClaw 2026.7.1-2 reserves
 * trusted Gateway RPC for bundled/official plugins, while
 * api.runtime.agent.session.getSessionEntry is the public third-party seam.
 */
export async function reconcileMissingOwnerSessions(
  api: any,
  databasePath: string,
  workspaceDir: string,
  config: OwnerReconcileConfig = {},
): Promise<{supported:boolean;checked:number;deleted:number;workflowFailures:number;failed:number}> {
  const getSessionEntry = api.runtime?.agent?.session?.getSessionEntry;
  if (typeof getSessionEntry !== "function") return {supported:false,checked:0,deleted:0,workflowFailures:0,failed:0};
  let checked = 0, deleted = 0, workflowFailures = 0, failed = 0;

  for (const sessionKey of activeOwnerSessionKeys(databasePath)) {
    checked++;
    const agentId = agentIdFromSessionKey(sessionKey);
    if (!agentId) {
      failed++;
      api.logger.warn?.(`CogentNexus owner reconciliation could not resolve agent id from ${sessionKey}`);
      continue;
    }

    let entry: any;
    try {
      entry = getSessionEntry({ agentId, sessionKey, readConsistency:"latest" });
    } catch (error) {
      failed++;
      api.logger.warn?.(`CogentNexus owner reconciliation could not read ${sessionKey}: ${error instanceof Error ? error.message : String(error)}`);
      continue;
    }
    if (entry !== undefined && entry !== null) continue;

    const reason = "OpenClaw owner session no longer exists";
    try {
      const deletion = deleteSessionByKey(databasePath, { sessionKey, message:reason });
      for (const workflowId of deletion.workflowIds) {
        const result = cancelWorkflow(workspaceDir, workflowId, reason, config);
        if (!result.ok) {
          workflowFailures++;
          api.logger.warn?.(`CogentNexus missing-owner workflow cancellation failed for ${workflowId}: ${result.error}`);
        }
      }
      finalizeSessionDeletion(databasePath, sessionKey, reason);
      deleted++;
      api.logger.info?.(`CogentNexus tombstoned missing OpenClaw owner ${sessionKey}: generation=${deletion.generation} tickets=${deletion.cancelled.length} assistantSuppressed=${deletion.assistantSuppressed}`);
    } catch (error) {
      failed++;
      api.logger.warn?.(`CogentNexus missing-owner deletion barrier failed for ${sessionKey}: ${error instanceof Error ? error.message : String(error)}`);
    }
  }
  return {supported:true,checked,deleted,workflowFailures,failed};
}
