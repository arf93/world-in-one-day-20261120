// main.ts — entrypoint for news-image-20261120.
// Copies the pre-rendered entry.png (in this repository) to the output
// directory. Node 22 standard library only; no network; deterministic:
// the same bytes are written on every run.

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// PNG signature: 89 50 4E 47 0D 0A 1A 0A
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

const here = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(here, "entry.png");

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const outPath = join(outDir, "entry.png");

const bytes = readFileSync(sourcePath);

if (bytes.length < PNG_MAGIC.length || !bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error("entry.png is not a PNG: bad magic bytes");
}

mkdirSync(outDir, { recursive: true });
writeFileSync(outPath, bytes);

const written = readFileSync(outPath);
if (written.length !== bytes.length || !written.equals(bytes)) {
  throw new Error("output is not byte-identical to the source image");
}

console.log(`wrote ${outPath} (${written.length} bytes)`);
