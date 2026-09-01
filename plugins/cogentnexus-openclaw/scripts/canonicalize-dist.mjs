import fs from 'node:fs';
import path from 'node:path';

const marker = '--dist-root';
const index = process.argv.indexOf(marker);
if (index < 0 || !process.argv[index + 1]) {
  throw new Error(`usage: node canonicalize-dist.mjs ${marker} <path>`);
}

const root = path.resolve(process.argv[index + 1]);
const textExtensions = new Set(['.js', '.d.ts', '.js.map']);
let changed = 0;

function visit(directory) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const file = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      visit(file);
      continue;
    }
    if (!textExtensions.has(path.extname(file)) && !file.endsWith('.d.ts')) continue;
    const before = fs.readFileSync(file);
    const after = Buffer.from(before.toString('utf8').replace(/\r\n/g, '\n'), 'utf8');
    if (!before.equals(after)) {
      fs.writeFileSync(file, after);
      changed += 1;
    }
  }
}

visit(root);
console.log(`canonicalized ${changed} dist files to LF`);
