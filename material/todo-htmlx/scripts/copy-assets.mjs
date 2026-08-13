// Copies the assets that need no processing into app/static/, which FastAPI
// serves. The components go through esbuild instead (see src/app.js); these two
// are already exactly what the browser should get.
//
// A Node script rather than `cp` so `npm run build` behaves the same on Windows.

import { copyFile, mkdir } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const dest = join(root, "app", "static");

const assets = [
  // Shipped as one file on purpose: htmx is used whole, so there is no subset
  // to take and nothing for a bundler to do.
  "htmx.org/dist/htmx.min.js",
];

await mkdir(dest, { recursive: true });

for (const asset of assets) {
  const file = asset.slice(asset.lastIndexOf("/") + 1);
  await copyFile(join(root, "node_modules", asset), join(dest, file));
  console.log(`static/${file}  <-  ${asset}`);
}
