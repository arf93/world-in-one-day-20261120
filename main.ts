// Entry point for the news-image-20261120 submission.
//
// The image is rendered ahead of time by render.py and stored in this
// repository as entry.png. This program only moves those exact bytes to
// the output directory, so the entry is byte-identical on every run.
// Node 22 standard library only; nothing is fetched from the network.

import * as fs from "node:fs";
import * as path from "node:path";
import { fileURLToPath } from "node:url";

// The first eight bytes of every PNG file.
const PNG_HEADER = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);

function fail(message) {
  throw new Error(`entry.png check failed: ${message}`);
}

function main() {
  const root = path.dirname(fileURLToPath(import.meta.url));
  const source = path.join(root, "entry.png");

  if (!fs.existsSync(source)) {
    fail(`missing source file ${source}`);
  }

  const image = fs.readFileSync(source);
  if (image.length < PNG_HEADER.length) {
    fail("file is shorter than a PNG header");
  }
  if (!image.subarray(0, PNG_HEADER.length).equals(PNG_HEADER)) {
    fail("first bytes are not the PNG signature");
  }

  const destinationDir =
    process.env.MAKEFUN_OUTPUT_DIR || "/output";
  const destination = path.join(destinationDir, "entry.png");

  fs.mkdirSync(destinationDir, { recursive: true });
  fs.writeFileSync(destination, image);

  const copied = fs.readFileSync(destination);
  if (copied.length !== image.length || !copied.equals(image)) {
    fail("the copied file differs from the source");
  }

  console.log(`copied ${destination} (${copied.length} bytes)`);
}

main();
