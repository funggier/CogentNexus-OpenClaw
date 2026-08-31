import { spawnSync } from "node:child_process";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const packageRoot = resolve(here, "..");
const npmArgs = ["pack", "--dry-run", "--json"];

function npmInvocation() {
  // npm exposes the exact CLI entrypoint to npm-run scripts. Invoking that JS
  // file through the current Node executable avoids direct .cmd execution,
  // which Node 24 rejects with spawnSync EINVAL on Windows.
  if (process.env.npm_execpath) {
    return { command: process.execPath, args: [process.env.npm_execpath, ...npmArgs], shell: false };
  }
  // Manual invocation outside npm-run has no npm_execpath. Static arguments
  // make a platform shell fallback safe here while preserving PATH lookup.
  return {
    command: "npm",
    args: npmArgs,
    shell: process.platform === "win32",
  };
}

const invocation = npmInvocation();
const result = spawnSync(invocation.command, invocation.args, {
  cwd: packageRoot,
  encoding: "utf8",
  windowsHide: true,
  shell: invocation.shell,
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

// npm >= 12 emits a single-entry object keyed by package name instead of an
// array. Normalize both shapes so package-content verification stays
// reproducible across the supported npm 11 and npm 12 toolchains.
if (packed !== null && typeof packed === "object" && !Array.isArray(packed)) {
  const values = Object.values(packed);
  if (values.length === 1) {
    packed = values;
  }
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
