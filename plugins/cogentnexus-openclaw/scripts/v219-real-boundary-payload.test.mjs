import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const pluginRoot = path.resolve(import.meta.dirname, '..');
const npm = process.platform === 'win32' ? 'npm.cmd' : 'npm';
const root = fs.mkdtempSync(path.join(os.tmpdir(), 'cnx-v219-boundary-'));

function copyFixture(name, eol) {
  const fixture = path.join(root, name);
  fs.cpSync(pluginRoot, fixture, { recursive: true, filter: (source) => !source.includes(`${path.sep}node_modules`) && !source.includes(`${path.sep}dist`) });
  for (const file of fs.readdirSync(path.join(fixture, 'src'))) {
    const source = path.join(fixture, 'src', file);
    if (file.endsWith('.ts') && fs.statSync(source).isFile()) {
      fs.writeFileSync(source, fs.readFileSync(source).toString('utf8').replace(/\r\n/g, '\n').replace(/\n/g, eol));
    }
  }
  const install = spawnSync(npm, ['ci', '--ignore-scripts'], { cwd: fixture, encoding: 'utf8', shell: true });
  assert.equal(install.status, 0, install.error?.message || install.stderr || install.stdout);
  const build = spawnSync(npm, ['run', 'build'], { cwd: fixture, encoding: 'utf8', shell: true });
  assert.equal(build.status, 0, build.error?.message || build.stderr || build.stdout);
  return fixture;
}

function distHashes(fixture) {
  const result = new Map();
  for (const file of fs.readdirSync(path.join(fixture, 'dist'), { recursive: true }).sort()) {
    const full = path.join(fixture, 'dist', file);
    if (fs.statSync(full).isFile()) result.set(file.replaceAll(path.sep, '/'), Buffer.from(fs.readFileSync(full)).toString('hex'));
  }
  return result;
}

try {
  const lf = distHashes(copyFixture('lf', '\n'));
  const crlf = distHashes(copyFixture('crlf', '\r\n'));
  assert.deepEqual([...crlf.keys()], [...lf.keys()], 'LF/CRLF builds must have equal dist paths');
  const differing = [...lf.keys()].filter((file) => lf.get(file) !== crlf.get(file));
  assert.deepEqual(differing, [], `generated dist bytes differ in ${differing.length} files: ${differing.slice(0, 10).join(', ')}`);
} finally {
  fs.rmSync(root, { recursive: true, force: true });
}
