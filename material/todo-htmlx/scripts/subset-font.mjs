// Cuts the icon font down to the icons this app draws.
//
// material-symbols ships the full variable font: every icon Google has, ~3.8 MB
// of it. The components render icons as ligatures — the text "delete" becomes
// the trash glyph — so subsetting means keeping the letters those names are
// spelled with, and harfbuzz keeps the ligature glyphs they resolve to.
//
// Which is why ICONS below is the list to maintain: an icon missing from it
// renders as its own name in text, visibly, on the page that uses it.

import { readFile, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import subsetFont from "subset-font";

const ICONS = [
  "add", // the Add button
  "add_task", // the composer field's leading icon
  "check", // drawn inside a selected filter chip and a checked checkbox
  "dark_mode", // the theme toggle, unselected
  "delete", // each row's trailing button
  "light_mode", // the theme toggle, selected
];

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const source = join(
  root, "node_modules", "material-symbols", "material-symbols-outlined.woff2",
);
const target = join(root, "app", "static", "material-symbols-subset.woff2");

const full = await readFile(source);
const subset = await subsetFont(full, ICONS.join(" "), {
  targetFormat: "woff2",
  // Material Symbols is a variable font on four axes, and the variation data is
  // most of what is left after the glyphs go. Nothing in the library sets
  // font-variation-settings, so every icon renders at the defaults — pin them
  // and ship a static instance. Restore an axis here if a component ever needs
  // to animate one (FILL is the usual candidate).
  variationAxes: { opsz: 24, wght: 400, FILL: 0, GRAD: 0 },
});
await writeFile(target, subset);

const kb = (buffer) => `${Math.round(buffer.length / 1024)} KB`;
console.log(
  `static/material-symbols-subset.woff2  ${kb(full)} -> ${kb(subset)}` +
    ` (${ICONS.length} icons)`,
);
