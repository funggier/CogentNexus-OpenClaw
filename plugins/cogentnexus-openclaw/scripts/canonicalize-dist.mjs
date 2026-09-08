import fs from 'node:fs';
import path from 'node:path';

const marker = '--dist-root';
const index = process.argv.indexOf(marker);
if (index < 0 || !process.argv[index + 1]) {
  throw new Error(`usage: node canonicalize-dist.mjs ${marker} <path>`);
}

const root = path.resolve(process.argv[index + 1]);
const rootStat = fs.lstatSync(root);
if (!rootStat.isDirectory() || rootStat.isSymbolicLink()) throw new Error(`invalid dist root: ${root}`);
let changed = 0;

function walk(directory) {
  const entries = fs.readdirSync(directory, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name));
  for (const entry of entries) {
    const file = path.join(directory, entry.name);
    if (entry.isSymbolicLink()) throw new Error(`indirection is not allowed in dist: ${file}`);
    if (entry.isDirectory()) {
      const stat = fs.lstatSync(file);
      if (!stat.isDirectory() || stat.isSymbolicLink()) throw new Error(`invalid dist directory: ${file}`);
      walk(file);
      continue;
    }
    if (!entry.isFile()) throw new Error(`unsupported dist filesystem entry: ${file}`);
    if (!/\.(?:js|mjs|cjs|d\.ts|js\.map)$/.test(entry.name)) throw new Error(`unsupported generated artifact: ${file}`);
    const before = fs.readFileSync(file);
    const after = Buffer.from(before.toString('utf8').replace(/\r\n/g, '\n'), 'utf8');
    if (!before.equals(after)) {
      fs.writeFileSync(file, after);
      changed += 1;
    }
  }
}

walk(root);
console.log(`canonicalized ${changed} dist text files to LF`);
