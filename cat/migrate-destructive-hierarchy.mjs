#!/usr/bin/env node
/**
 * destructive 与 primary/secondary 同级：
 *   --btn-{variant}-destructive-{state}-{prop}
 * 删除 --btn-{variant}-{level}-destructive-* 及 secondary-destructive 重复套
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const file = process.argv[2] || path.join(path.dirname(fileURLToPath(import.meta.url)), "button-design-editor.html");
let html = fs.readFileSync(file, "utf8");

const LEVELS = ["primary", "secondary", "tertiary", "quaternary"];

function renameDestructiveToken(key) {
  const m = key.match(/^(--btn-[\w-]+?)-(primary|secondary|tertiary|quaternary)-destructive(-.+)$/);
  if (!m) return { key, drop: false };
  if (m[2] !== "primary") return { key, drop: true };
  return { key: `${m[1]}-destructive${m[3]}`, drop: false };
}

function migrateSpecGroup(group) {
  return group.replace(/ · (primary|secondary|tertiary|quaternary) · destructive$/, " · destructive");
}

// ── 1) :root / dark theme CSS variables (line-based) ──
html = html
  .split("\n")
  .filter((line) => {
    const t = line.trim();
    if (!t.startsWith("--btn-")) return true;
    for (const lv of LEVELS) {
      if (t.startsWith(`--btn-`) && t.includes(`-${lv}-destructive-`) && lv !== "primary") {
        if (new RegExp(`--btn-[\\w-]+-${lv}-destructive-`).test(t)) return false;
      }
    }
    return true;
  })
  .map((line) => {
    const m = line.match(/^(\s*)(--btn-[\w-]+?)-(primary|secondary|tertiary|quaternary)-destructive(-[\w-]+:\s*.+;)\s*$/);
    if (m && m[3] === "primary") return `${m[1]}${m[2]}-destructive${m[4]}`;
    return line;
  })
  .join("\n");

html = html.replace(
  /\/\* ── ([\w]+) · (primary|secondary|tertiary|quaternary) · destructive ── \*\//g,
  "/* ── $1 · destructive ── */"
);

// ── 2) var() in CSS rules ──
html = html.replace(/var\((--btn-[\w-]+?)-(primary|secondary|tertiary|quaternary)-destructive(-[\w-]+)\)/g, (full, p, lv, suf) => {
  if (lv !== "primary") return full; // secondary blocks removed below
  return `var(${p}-destructive${suf})`;
});

// ── 3) Remove secondary/tertiary/quaternary destructive CSS rule blocks ──
for (const lv of ["secondary", "tertiary", "quaternary"]) {
  const blockRe = new RegExp(
    `\\n\\s*\\.fc-btn\\[data-variant="[^"]+"\\]\\[data-hierarchy="${lv}"\\]\\[data-destructive="true"\\][\\s\\S]*?\\n\\s*\\}`,
    "g"
  );
  html = html.replace(blockRe, "\n");
}

// ── 4) destructive selectors: primary+destructive → hierarchy destructive ──
html = html.replace(
  /\[data-hierarchy="(primary|secondary|tertiary|quaternary)"\]\[data-destructive="true"\]/g,
  '[data-hierarchy="destructive"]'
);
html = html.replace(/\[data-destructive="false"\]/g, "");

// ── 5) COLOR_DEFAULTS ──
function parseJsonConst(src, name, open, close) {
  const marker = `const ${name} = `;
  const idx = src.indexOf(marker);
  const start = idx + marker.length;
  let depth = 0;
  let end = start;
  for (let i = start; i < src.length; i++) {
    if (src[i] === open) depth++;
    else if (src[i] === close) {
      depth--;
      if (depth === 0) {
        end = i + 1;
        break;
      }
    }
  }
  return { start: idx, end, value: JSON.parse(src.slice(start, end)) };
}

function patchJsonConst(h, name, open, close, value) {
  const marker = `const ${name} = `;
  const idx = h.indexOf(marker);
  const start = idx + marker.length;
  let depth = 0;
  let end = start;
  for (let i = start; i < h.length; i++) {
    if (h[i] === open) depth++;
    else if (h[i] === close) {
      depth--;
      if (depth === 0) {
        end = i + 1;
        break;
      }
    }
  }
  const after = h[end] === ";" ? end + 1 : end;
  const serialized = open === "{" ? JSON.stringify(value) : JSON.stringify(value);
  return h.slice(0, idx) + `const ${name} = ${serialized};` + h.slice(after);
}

const { value: defaults } = parseJsonConst(html, "COLOR_DEFAULTS", "{", "}");
const nextDefaults = {};
for (const [k, v] of Object.entries(defaults)) {
  const { key, drop } = renameDestructiveToken(k);
  if (drop) continue;
  if (nextDefaults[key] === undefined) nextDefaults[key] = v;
}
html = patchJsonConst(html, "COLOR_DEFAULTS", "{", "}", nextDefaults);

// ── 6) SPEC_ROWS ──
const { value: specRows } = parseJsonConst(html, "SPEC_ROWS", "[", "]");
const nextSpec = [];
const seenSpecKeys = new Set();
for (const [group, key, label] of specRows) {
  if (/-(secondary|tertiary|quaternary)-destructive-/.test(key)) continue;
  const { key: nk, drop } = renameDestructiveToken(key);
  if (drop || seenSpecKeys.has(nk)) continue;
  seenSpecKeys.add(nk);
  nextSpec.push([migrateSpecGroup(group), nk, label]);
}
html = patchJsonConst(html, "SPEC_ROWS", "[", "]", nextSpec);

// ── 7) UNIFIED_COLOR_KEYS — rebuild from keys that exist in defaults ──
const unifiedKeys = Object.keys(nextDefaults).filter((k) => !SHARED_KEYS_FROM_HTML(html).has(k));
// skip UNIFIED rebuild — filter existing set
const unifiedMatch = html.match(/const UNIFIED_COLOR_KEYS = new Set\(\[([\s\S]*?)\]\);/);
if (unifiedMatch) {
  const oldKeys = [...unifiedMatch[1].matchAll(/"([^"]+)"/g)].map((m) => m[1]);
  const filtered = oldKeys.filter((k) => {
    const { drop } = renameDestructiveToken(k);
    return !drop && nextDefaults[k] !== undefined;
  }).map((k) => {
    const { key } = renameDestructiveToken(k);
    return key || k;
  });
  const unique = [...new Set(filtered)];
  html = html.replace(
    /const UNIFIED_COLOR_KEYS = new Set\(\[[\s\S]*?\]\);/,
    `const UNIFIED_COLOR_KEYS = new Set(${JSON.stringify(unique)});`
  );
}

function SHARED_KEYS_FROM_HTML(h) {
  const m = h.match(/const SHARED_KEYS = new Set\(\[([\s\S]*?)\]\);/);
  if (!m) return new Set();
  return new Set([...m[1].matchAll(/"([^"]+)"/g)].map((x) => x[1]));
}

// ── 8) JS: remove DESTRUCTIVE_TOKEN_BASE, simplify resolveButtonAttrs & renderButtonHtml ──
html = html.replace(
  /\s*\/\*\* destructive 等级映射[\s\S]*?const DESTRUCTIVE_TOKEN_BASE = \{[\s\S]*?\};\n/,
  "\n"
);
html = html.replace(
  /function resolveButtonAttrs\(variant, hierarchy\) \{\s*if \(hierarchy === "destructive"\) \{\s*const base = DESTRUCTIVE_TOKEN_BASE\[variant\] \|\| "primary";\s*return \{ variant, hierarchy: base, destructive: true \};\s*\}\s*return \{ variant, hierarchy, destructive: false \};\s*\}/,
  `function resolveButtonAttrs(variant, hierarchy) {
      return { variant, hierarchy };
    }`
);
html = html.replace(
  /const \{ variant, hierarchy, destructive \} = resolveButtonAttrs\(v0, h0\);/,
  "const { variant, hierarchy } = resolveButtonAttrs(v0, h0);"
);
html = html.replace(
  /const dest = destructive \? ' data-destructive="true"' : ' data-destructive="false"';\n/g,
  ""
);
html = html.replace(
  /\$\{iconAttr\}\$\{dest\}\$\{ariaDisabled\}/,
  "${iconAttr}${ariaDisabled}"
);

// bump schema if present
html = html.replace(/const STORAGE_SCHEMA_VERSION = \d+;/, (m) => {
  const n = parseInt(m.match(/\d+/)[0], 10);
  return `const STORAGE_SCHEMA_VERSION = ${n + 1};`;
});

// clean double newlines in style
html = html.replace(/\n{3,}/g, "\n\n");

fs.writeFileSync(file, html);
console.log("OK:", file);

// verify
const left = (html.match(/-(primary|secondary|tertiary|quaternary)-destructive-/g) || []).length;
const leftSel = (html.match(/data-destructive/g) || []).length;
console.log("remaining *-level-destructive tokens:", left);
console.log("remaining data-destructive attrs:", leftSel);
