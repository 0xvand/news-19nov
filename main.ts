// THE DAILY SUM — entry program for make.fun's news-image-20261119 bounty.
//
// The picture of the day is entry.png, drawn by draw.py from the headlines
// of Thursday 19 November 2026 (see SOURCES.md). This program's whole job
// is to place that exact file at the grader's output path, byte for byte,
// on every run — no network, no clock, no randomness.
//
// Run it the way the grader does:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// (MAKEFUN_OUTPUT_DIR stands in for /output outside the grader's box.)

import { copyFileSync, statSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const here = fileURLToPath(new URL(".", import.meta.url));
const src = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const dst = join(outDir, "entry.png");

copyFileSync(src, dst);
console.log(`entry.png -> ${dst} (${statSync(dst).size} bytes)`);
