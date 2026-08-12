import { spawnSync } from "node:child_process";
import { DatabaseSync } from "node:sqlite";
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";

const workspace = resolve(process.argv[2] ?? process.cwd());
const marker = process.argv[3] ?? "CONTROLLED-RECOVERY-TEST";
const expectedOwnerSessionKey = process.argv[4];
const timeoutMs = Number(process.argv[5] ?? 30 * 60_000);
const revalidateExisting = process.argv[6] === "--revalidate-existing";
if (!expectedOwnerSessionKey || !/^agent:[^:]+:dashboard:[^:]+$/u.test(expectedOwnerSessionKey)) {
  throw new Error("expected owner session key must use agent:<id>:dashboard:<id>");
}

const evidencePath = join(workspace, ".cogent", "runtime", "controlled-live-ticket-recovery.json");
const databasePath = join(workspace, ".cogent", "runtime", "cogentnexus.sqlite3");
const runtimePath = join(workspace, "skills", "cogentnexus", "scripts", "runtime.py");
const workflowPath = join(workspace, "skills", "cogentnexus", "scripts", "workflow.py");
const deadline = Date.now() + timeoutMs;
const startedAt = new Date().toISOString();
const priorEvidence = revalidateExisting && existsSync(evidencePath)
  ? JSON.parse(readFileSync(evidencePath, "utf8"))
  : undefined;
let restarted = priorEvidence?.restarted === true;
let ticketId = priorEvidence?.ticketId;

function save(status, details = {}) {
  writeFileSync(evidencePath, `${JSON.stringify({
    marker, expectedOwnerSessionKey, startedAt, updatedAt: new Date().toISOString(),
    status, restarted, ticketId, ...details,
  }, null, 2)}\n`, "utf8");
}

function latestTicket() {
  if (!existsSync(databasePath)) return undefined;
  const db = new DatabaseSync(databasePath, { readOnly: true });
  try {
    return db.prepare(`SELECT ticket_id,run_id,owner_session_key,status,workflow_eligible,workflow_id,manifest_path,
      lease_generation,attempt_count,result_json,failure_class,failure_message,created_at,updated_at
      FROM tickets WHERE prompt LIKE ? ORDER BY created_at DESC LIMIT 1`).get(`%${marker}%`);
  } finally { db.close(); }
}

function inspectWorkflow(workflowId) {
  if (!workflowId) return { valid: false, error: "workflow is not linked" };
  const result = spawnSync("python", [workflowPath, "--root", workspace, "inspect", workflowId], {
    cwd: workspace, encoding: "utf8", windowsHide: true, timeout: 30_000,
  });
  if (result.status !== 0) return { valid: false, exitCode: result.status, stdout: result.stdout, stderr: result.stderr, error: result.error?.message };
  try {
    const inspection = JSON.parse(result.stdout);
    return { valid: inspection.completionVerified === true && inspection.manifestIntegrity === true && inspection.artifactIntegrity === true, inspection };
  } catch (error) {
    return { valid: false, stdout: result.stdout, stderr: result.stderr, error: error.message };
  }
}

if (revalidateExisting) {
  if (priorEvidence?.marker !== marker || priorEvidence?.expectedOwnerSessionKey !== expectedOwnerSessionKey) {
    throw new Error("existing evidence does not match marker and owner");
  }
  const ticket = latestTicket();
  const workflow = inspectWorkflow(ticket?.workflow_id);
  const success = ticket?.status === "completed" && restarted && workflow.valid;
  save(success ? "completed_verified_after_restart" : "terminal_not_verified", { ticket, workflow, revalidated: true });
  process.exit(success ? 0 : 4);
}

save("waiting_for_owner_bound_ticket", { databasePath, timeoutMs });
while (Date.now() < deadline) {
  const ticket = latestTicket();
  if (ticket) {
    ticketId = ticket.ticket_id;
    if (ticket.owner_session_key !== expectedOwnerSessionKey) {
      save("owner_binding_mismatch", { ticket });
      process.exit(6);
    }
  }
  if (ticket?.status === "running" && ticket.workflow_id && ticket.manifest_path && !restarted) {
    save("linked_ticket_observed_restart_starting", { ticket });
    const restart = spawnSync("python", [runtimePath, "lifecycle", "restart", "--reason", `controlled live Ticket recovery ${ticket.ticket_id}`], {
      cwd: workspace, encoding: "utf8", windowsHide: true, timeout: 180_000,
    });
    restarted = restart.status === 0;
    save(restarted ? "gateway_restarted_monitoring_recovery" : "gateway_restart_failed", {
      ticket, lifecycle: { exitCode: restart.status, signal: restart.signal, stdout: restart.stdout, stderr: restart.stderr, error: restart.error?.message },
    });
    if (!restarted) process.exit(3);
  }
  if (ticket && ["completed", "failed", "cancelled"].includes(ticket.status)) {
    const workflow = inspectWorkflow(ticket.workflow_id);
    const success = ticket.status === "completed" && restarted && workflow.valid;
    save(success ? "completed_verified_after_restart" : "terminal_not_verified", { ticket, workflow });
    process.exit(success ? 0 : 4);
  }
  await new Promise((done) => setTimeout(done, 1000));
}

const terminalTicket = latestTicket();
save("timed_out", { ticket: terminalTicket, workflow: inspectWorkflow(terminalTicket?.workflow_id) });
process.exit(2);
