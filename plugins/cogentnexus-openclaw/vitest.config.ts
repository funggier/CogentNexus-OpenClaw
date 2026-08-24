import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "node",
    include: ["src/**/*.test.ts"],
    fileParallelism: false,
    // Windows hosted runners show materially higher node:sqlite latency under
    // the full serial suite: the same unchanged integration tests can cross
    // Vitest's 5s default while completing successfully on rerun or another
    // Windows/Python matrix. Keep a bounded Windows-only budget rather than
    // weakening production timeouts or globally masking hangs on other OSes.
    testTimeout: process.platform === "win32" ? 15_000 : 5_000,
  },
});