#!/usr/bin/env node
// Checks library.json against the posts.md files. Run before every push:
//   node scripts/check-library.mjs
// Fails (exit 1) if a post's text differs from its posts.md code block, a listed file is
// missing, a field is malformed, or a LinkedIn draft/approved post has a link in its body.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const WEEK_DIR = { '2026-w45': '2026-11/wk1' }; // week 1 kept its first folder name

const ENUMS = {
  channel: ['linkedin', 'instagram', 'facebook'],
  status: ['posted', 'approved', 'draft', 'replaced'],
  format: ['text', 'image', 'carousel', 'document', 'video'],
  postedVia: ['buffer', 'native', ''],
};
const KEYS = ['id', 'week', 'channel', 'topic', 'date', 'time', 'status', 'title', 'format',
  'text', 'firstComment', 'link', 'files', 'notes', 'postedVia'];

function weekDir(week) {
  if (WEEK_DIR[week]) return WEEK_DIR[week];
  const wk = `wk${week.slice(-2)}`;
  for (const d of fs.readdirSync(ROOT).filter((d) => /^\d{4}-\d{2}$/.test(d)).sort()) {
    if (fs.existsSync(path.join(ROOT, d, wk, 'posts.md'))) return `${d}/${wk}`;
  }
  return null;
}

const cache = new Map();
function sections(file) {
  if (cache.has(file)) return cache.get(file);
  const lines = fs.readFileSync(path.join(ROOT, file), 'utf8').split('\n');
  const map = new Map();
  for (let i = 0; i < lines.length; i++) {
    if (!lines[i].startsWith('### ')) continue;
    const id = lines[i].slice(4).split(' · ')[0].replace(/\s*\(.*?\)$/, '');
    let j = i + 1;
    while (j < lines.length && !lines[j].startsWith('## ') && !lines[j].startsWith('### ')) j++;
    const sec = lines.slice(i + 1, j);
    const a = sec.findIndex((l) => l.startsWith('```'));
    let text = '';
    if (a >= 0) {
      const b = sec.findIndex((l, k) => k > a && l.startsWith('```'));
      text = b > a ? sec.slice(a + 1, b).join('\n') : null;
    }
    if (map.has(id)) map.set(id, { dup: true });
    else map.set(id, { text });
  }
  cache.set(file, map);
  return map;
}

const errors = [];
const err = (id, msg) => errors.push(`${id}: ${msg}`);

let lib;
try {
  lib = JSON.parse(fs.readFileSync(path.join(ROOT, 'library.json'), 'utf8'));
} catch (e) {
  console.error(`library.json: ${e.message}`);
  process.exit(1);
}
if (!Array.isArray(lib)) {
  console.error('library.json: not an array');
  process.exit(1);
}

const seen = new Set();
for (const p of lib) {
  const id = p?.id ?? '(no id)';
  const keys = Object.keys(p ?? {});
  const missing = KEYS.filter((k) => !keys.includes(k));
  const extra = keys.filter((k) => !KEYS.includes(k));
  if (missing.length) err(id, `missing ${missing.join(', ')}`);
  if (extra.length) err(id, `unknown field ${extra.join(', ')}`);
  if (missing.length) continue;

  if (seen.has(id)) err(id, 'duplicate id');
  seen.add(id);
  for (const [k, vals] of Object.entries(ENUMS)) if (!vals.includes(p[k])) err(id, `bad ${k} "${p[k]}"`);
  if (!/^\d{4}-w\d{2}$/.test(p.week)) err(id, `bad week "${p.week}"`);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(p.date)) err(id, `bad date "${p.date}"`);
  if (!/^\d{2}:\d{2}$/.test(p.time)) err(id, `bad time "${p.time}"`);
  if (p.status === 'posted' && !p.postedVia) err(id, 'posted but postedVia is empty');
  const words = p.title.trim().split(/\s+/).length;
  if (words < 3 || words > 6) err(id, `title has ${words} words (3 to 6)`);

  // text: byte for byte with the first code block under "### <post id> ·" in that week's posts.md
  const pid = id.startsWith(`${p.week}-`) ? id.slice(p.week.length + 1) : null;
  const dir = weekDir(p.week);
  if (!pid) err(id, `id must start with "${p.week}-"`);
  else if (!dir) err(id, `no posts.md for ${p.week}`);
  else {
    const sec = sections(`${dir}/posts.md`).get(pid);
    if (!sec) err(id, `no "### ${pid} ·" heading in ${dir}/posts.md`);
    else if (sec.dup) err(id, `"### ${pid}" appears twice in ${dir}/posts.md`);
    else if (sec.text === null) err(id, `unclosed code block in ${dir}/posts.md`);
    else if (sec.text !== p.text) {
      const a = sec.text, b = p.text;
      let k = 0;
      while (k < a.length && a[k] === b[k]) k++;
      err(id, `text differs from ${dir}/posts.md at character ${k}: posts.md ${JSON.stringify(a.slice(k, k + 40))} vs library ${JSON.stringify(b.slice(k, k + 40))}`);
    }
  }

  // files: relative to the repo root and present
  if (!Array.isArray(p.files)) err(id, 'files is not an array');
  else {
    p.files.forEach((f, i) => {
      if (typeof f?.path !== 'string' || typeof f?.alt !== 'string') return err(id, `files[${i}] needs path and alt`);
      if (f.path.startsWith('/') || f.path.includes('..')) err(id, `files[${i}] path must be relative to the repo root`);
      else if (!fs.existsSync(path.join(ROOT, f.path))) err(id, `missing file ${f.path}`);
    });
    if (p.format === 'document' && !p.files[0]?.path.endsWith('.pdf')) err(id, 'document post: the PDF must be listed first');
    if (['image', 'carousel', 'document', 'video'].includes(p.format) && p.files.length === 0) err(id, `${p.format} post with no files`);
  }

  if (p.channel === 'linkedin' && ['draft', 'approved'].includes(p.status) && /https?:\/\/|getday60\.com/.test(p.text)) {
    err(id, 'LinkedIn body has a link (it goes in the first comment)');
  }
}

if (errors.length) {
  console.error(`library.json: ${errors.length} problem(s)`);
  for (const e of errors) console.error(`  ${e}`);
  process.exit(1);
}
console.log(`library.json OK: ${lib.length} posts, text matches posts.md, every file exists.`);
