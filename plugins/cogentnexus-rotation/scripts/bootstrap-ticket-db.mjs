import { resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { defaultTicketDatabase, TicketStore } from "../dist/ticket-store.js";

export function bootstrapTicketDatabase(workspace) {
  const resolvedWorkspace = resolve(workspace);
  const database = defaultTicketDatabase(resolvedWorkspace);
  const snapshot = new TicketStore(database).snapshot();
  return { workspace: resolvedWorkspace, database, snapshot };
}

function parseWorkspace(argv) {
  const index = argv.indexOf("--workspace");
  if (index < 0 || !argv[index + 1]) {
    throw new Error("Usage: node scripts/bootstrap-ticket-db.mjs --workspace <path>");
  }
  return argv[index + 1];
}

const invokedPath = process.argv[1] ? pathToFileURL(resolve(process.argv[1])).href : null;
if (invokedPath && import.meta.url === invokedPath) {
  try {
    const result = bootstrapTicketDatabase(parseWorkspace(process.argv.slice(2)));
    console.log(JSON.stringify({ result: "ok", ...result }, null, 2));
  } catch (error) {
    console.error(error instanceof Error ? error.stack ?? error.message : String(error));
    process.exitCode = 1;
  }
}
