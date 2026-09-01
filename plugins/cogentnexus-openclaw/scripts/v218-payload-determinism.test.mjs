import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const pluginRoot = path.resolve(import.meta.dirname, '..');
const root = fs.mkdtempSync(path.join(os.tmpdir(), 'cnx-v218-dist-'));
try {
  const dist = path.join(root, 'dist');
  fs.mkdirSync(dist);
  fs.writeFileSync(path.join(dist, 'entry.js'), 'export const answer = 42;\r\n');
  fs.writeFileSync(path.join(dist, 'entry.d.ts'), 'export declare const answer: 42;\r\n');
  const helper = path.join(pluginRoot, 'scripts', 'canonicalize-dist.mjs');
  const result = spawnSync(process.execPath, [helper, '--dist-root', dist], { encoding: 'utf8' });
  assert.equal(result.status, 0, result.stderr || result.stdout);
  assert.equal(fs.readFileSync(path.join(dist, 'entry.js'), 'utf8'), 'export const answer = 42;\n');
  assert.equal(fs.readFileSync(path.join(dist, 'entry.d.ts'), 'utf8'), 'export declare const answer: 42;\n');
  console.log('v218 payload determinism regression: PASS');
} finally {
  fs.rmSync(root, { recursive: true, force: true });
}
