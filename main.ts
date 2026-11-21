import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(here, "entry.png");
const outputDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const destPath = join(outputDir, "entry.png");

const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47];
const MAX_BYTES = 1024 * 1024; // 1 MiB

function checkPng(filePath, label) {
  if (!existsSync(filePath)) {
    throw new Error(`${label} is missing: ${filePath}`);
  }
  const size = statSync(filePath).size;
  if (size === 0) {
    throw new Error(`${label} is empty: ${filePath}`);
  }
  if (size > MAX_BYTES) {
    throw new Error(`${label} is too large (${size} bytes, limit ${MAX_BYTES}): ${filePath}`);
  }
  const head = readFileSync(filePath).subarray(0, 4);
  for (let i = 0; i < PNG_SIGNATURE.length; i++) {
    if (head[i] !== PNG_SIGNATURE[i]) {
      throw new Error(`${label} does not start with the PNG signature: ${filePath}`);
    }
  }
  return size;
}

const beforeSize = checkPng(sourcePath, "Source entry.png");
mkdirSync(outputDir, { recursive: true });
copyFileSync(sourcePath, destPath);
const afterSize = checkPng(destPath, "Copied entry.png");
console.log(`Copied ${sourcePath} (${beforeSize} bytes) -> ${destPath} (${afterSize} bytes)`);
