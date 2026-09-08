import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const pluginRoot = path.resolve(import.meta.dirname, '..');
const root = fs.mkdtempSync(path.join(os.tmpdir(), 'cnx-v218-payload-'));
try {
  const dist = path.join(root, 'dist');
  fs.mkdirSync(dist);
  fs.writeFileSync(path.join(dist, 'entry.js'), 'export const answer = 42;\r\n');
  fs.writeFileSync(path.join(dist, 'entry.d.ts'), 'export declare const answer: 42;\r\n');
  fs.writeFileSync(path.join(root, 'package.json'), '{\r\n  "name": "fixture",\r\n  "files": ["dist", "README.md", "scripts/bootstrap-ticket-db.mjs"]\r\n}\r\n');
  fs.mkdirSync(path.join(root, 'scripts'));
  fs.writeFileSync(path.join(root, 'scripts', 'bootstrap-ticket-db.mjs'), 'export const ready = true;\r\n');
  fs.writeFileSync(path.join(root, 'README.md'), '# fixture\r\n');
  const helper = path.join(pluginRoot, 'scripts', 'canonicalize-dist.mjs');
  const result = spawnSync(process.execPath, [helper, '--package-root', root], { encoding: 'utf8' });
  assert.equal(result.status, 0, result.stderr || result.stdout);
  for (const file of ['dist/entry.js', 'dist/entry.d.ts', 'package.json', 'README.md', 'scripts/bootstrap-ticket-db.mjs']) {
    assert.equal(fs.readFileSync(path.join(root, file), 'utf8'), fs.readFileSync(path.join(root, file), 'utf8').replace(/\r\n/g, '\n'));
  }
  console.log('v218 payload determinism regression: PASS');
} finally {
  fs.rmSync(root, { recursive: true, force: true });
}
