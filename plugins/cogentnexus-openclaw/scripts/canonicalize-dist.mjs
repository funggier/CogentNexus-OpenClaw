import fs from 'node:fs';
import path from 'node:path';

const marker = '--package-root';
const index = process.argv.indexOf(marker);
if (index < 0 || !process.argv[index + 1]) {
  throw new Error(`usage: node canonicalize-dist.mjs ${marker} <path>`);
}

const root = path.resolve(process.argv[index + 1]);
const packageJson = JSON.parse(fs.readFileSync(path.join(root, 'package.json'), 'utf8'));
const declared = new Set(['package.json']);
for (const pattern of packageJson.files ?? []) {
  const target = path.join(root, pattern);
  if (fs.existsSync(target) && fs.statSync(target).isFile()) declared.add(pattern);
  if (fs.existsSync(target) && fs.statSync(target).isDirectory()) {
    for (const entry of fs.readdirSync(target, { recursive: true })) {
      const full = path.join(target, entry);
      if (fs.existsSync(full) && fs.statSync(full).isFile()) {
        declared.add(path.relative(root, full).split(path.sep).join('/'));
      }
    }
  }
}
let changed = 0;
for (const relative of declared) {
  const file = path.join(root, relative);
  if (!file.endsWith('.js') && !file.endsWith('.mjs') && !file.endsWith('.d.ts') && !file.endsWith('.js.map') && !file.endsWith('.json') && !file.endsWith('.md')) continue;
  const before = fs.readFileSync(file);
  const after = Buffer.from(before.toString('utf8').replace(/\r\n/g, '\n'), 'utf8');
  if (!before.equals(after)) {
    fs.writeFileSync(file, after);
    changed += 1;
  }
}
console.log(`canonicalized ${changed} package text files to LF`);
