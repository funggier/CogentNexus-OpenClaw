import { spawnSync } from "node:child_process";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const packageRoot = resolve(here, "..");
const npmCommand = process.platform === "win32" ? "npm.cmd" : "npm";

const result = spawnSync(npmCommand, ["pack", "--dry-run", "--json"], {
  cwd: packageRoot,
  encoding: "utf8",
  windowsHide: true,
});

if (result.error) {
  throw result.error;
}
if (result.status !== 0) {
  throw new Error(
    `npm pack --dry-run failed with exit code ${result.status}: ${result.stderr || result.stdout}`,
  );
}

let packed;
try {
  packed = JSON.parse(result.stdout);
} catch (error) {
  throw new Error(`npm pack --dry-run returned invalid JSON: ${result.stdout}`, { cause: error });
}

if (!Array.isArray(packed) || packed.length !== 1 || !Array.isArray(packed[0]?.files)) {
  throw new Error(`Unexpected npm pack --dry-run shape: ${result.stdout}`);
}

const paths = new Set(
  packed[0].files
    .map((entry) => entry?.path)
    .filter((entry) => typeof entry === "string")
    .map((entry) => entry.replaceAll("\\", "/")),
);

const required = [
  "dist/v091-release-entry.js",
  "scripts/bootstrap-ticket-db.mjs",
  "openclaw.plugin.json",
  "README.md",
];
const missing = required.filter((path) => !paths.has(path));

if (missing.length > 0) {
  throw new Error(`Published plugin package is missing required files: ${missing.join(", ")}`);
}

console.log(
  JSON.stringify(
    {
      result: "ok",
      package: packed[0].filename ?? null,
      required,
      packedFileCount: paths.size,
    },
    null,
    2,
  ),
);
