import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const pluginRoot = path.resolve(import.meta.dirname, '..');
const npm = process.platform === 'win32' ? 'npm.cmd' : 'npm';
const root = fs.mkdtempSync(path.join(os.tmpdir(), 'cnx-v222-static-guard-'));
const fixture = path.join(root, 'plugin');

try {
  fs.cpSync(pluginRoot, fixture, {
    recursive: true,
    filter: (source) => !source.includes(`${path.sep}node_modules`),
  });

  const readme = path.join(fixture, 'README.md');
  const lf = fs.readFileSync(readme, 'utf8').replace(/\r\n/g, '\n');
  fs.writeFileSync(readme, lf.replace(/\n/g, '\r\n'));

  const result = spawnSync(process.execPath, ['scripts/verify-package-contents.mjs'], {
    cwd: fixture,
    encoding: 'utf8',
    shell: false,
  });

  assert.notEqual(
    result.status,
    0,
    `static CRLF contamination was accepted by package validation:\n${result.stdout}\n${result.stderr}`,
  );
  assert.match(
    `${result.stdout}\n${result.stderr}`,
    /README\.md|noncanonical|CRLF/i,
    'failure must identify the contaminated static path or byte policy',
  );
} finally {
  fs.rmSync(root, { recursive: true, force: true });
}
