// The custom elements this app uses — nine of the library's seventy-odd.
//
// Each import registers one element and pulls in whatever it uses internally,
// so this list is the whole dependency declaration: esbuild bundles exactly
// these and nothing else. Adding a <material-dialog> to a template means adding
// a line here, and forgetting to is loud — the tag renders as an inert unknown
// element.
//
// The alternative the library ships is cdn/material.min.js: every element,
// eager, in one 590 KB file. Fine for a page that uses most of them; this app
// uses an eighth of them.

import "advanced-material-web/dist/components/material-app-bar.js";
import "advanced-material-web/dist/components/material-button.js";
import "advanced-material-web/dist/components/material-checkbox.js";
import "advanced-material-web/dist/components/material-chip.js";
import "advanced-material-web/dist/components/material-chip-set.js";
import "advanced-material-web/dist/components/material-icon-button.js";
import "advanced-material-web/dist/components/material-list.js";
import "advanced-material-web/dist/components/material-list-item.js";
import "advanced-material-web/dist/components/material-textfield.js";
