#!/usr/bin/env node
// Checks library.json against the posts.md files. Run before every push:
//   node scripts/check-library.mjs
// Fails (exit 1) if a post's text differs from its posts.md code block, a listed file is
// missing, a field is malformed, a LinkedIn draft/approved post has a link anywhere but its last line,
// or a placeholder isn't marked in the notes.
// HQ, Nov 19 (Buffer's plan can't post a LinkedIn first comment): every LinkedIn draft/approved post dated after
// the natively scheduled ones (through Nov 28) is text only, has no first comment and never mentions one; a link,
// if the post's point is one, is the body's last line before the hashtags.
// Feed safe area (HQ, Nov 16): every feed PNG still to post (an Instagram or Facebook image or carousel, draft or
// approved, dated today or later in Chicago) must have a passing record in design-system/safe-area.json with the
// file's SHA-256. templates/render_many.js writes that record only when every non-decorative element sits inside
// y 150 to 1200 of the 1080x1350 canvas. A waived file is listed with its reason but doesn't fail.
import crypto from 'node:crypto';
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
  const y = week.slice(0, 4), wk = `wk${week.slice(-2)}`;
  const dirs = fs.readdirSync(ROOT).filter((d) => /^\d{4}-\d{2}$/.test(d)).sort();
  // a week's folder is in its own year, or in the December before it (an ISO week 1 can start there)
  for (const d of dirs.filter((d) => d.startsWith(y) || d === `${Number(y) - 1}-12`)) {
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
const NATIVE_UNTIL = '2026-11-28'; // posts through this date were scheduled natively (Philip, Nov 11 to 16) and stay as they are

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
  if (p.notes.split('\n').some((l) => /^\s*(\d+[.)]|[-*•])\s/.test(l))) err(id, 'notes: one instruction per line, no numbering or bullets');
  const words = p.title.trim().split(/\s+/).length;
  if (words < 3 || words > 6) err(id, `title has ${words} words (3 to 6)`);

  // text: byte for byte with the first code block under "### <post id> ·" in the posts.md of the week it's filed in.
  // The id never changes: it keeps the week the post was first planned in, even after the post moves (2026-w49-LI-PH in 2027-w02).
  const m = /^(\d{4}-w\d{2})-(.+)$/.exec(id);
  const pid = m ? m[2] : null;
  const dir = weekDir(p.week);
  if (!pid) err(id, 'id must be "<week>-<post id>"');
  else if (m[1] > p.week) err(id, `id's week ${m[1]} is after the week it's filed in (${p.week}); posts only move later`);
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

  const live = ['draft', 'approved'].includes(p.status);
  const LINK = /https?:\/\/|getday60\.com|<[^>]*link[^>]*>/i;
  if (p.channel === 'linkedin' && live) {
    // a link only as the body's last line before the hashtags (HQ, Nov 19)
    const body = p.text.split('\n');
    while (body.length && (/^\s*$/.test(body.at(-1)) || /^(#\w+\s*)+$/.test(body.at(-1).trim()))) body.pop();
    const at = body.map((l, i) => (LINK.test(l) ? i : -1)).filter((i) => i >= 0);
    if (at.some((i) => i !== body.length - 1)) err(id, 'LinkedIn link is not the body\'s last line (before the hashtags)');
  }
  if (p.channel === 'linkedin' && live && p.date > NATIVE_UNTIL) {
    if (p.firstComment) err(id, 'LinkedIn first comment: Buffer\'s plan can\'t post one (HQ, Nov 19); leave firstComment empty');
    if (/first comment/i.test(p.text)) err(id, 'LinkedIn text points to a first comment (HQ, Nov 19: never)');
    if (p.format !== 'text') err(id, `LinkedIn is text only from Nov 19 (HQ), not ${p.format}`);
  }

  if (p.firstComment !== p.firstComment.trim()) err(id, 'firstComment has leading or trailing whitespace');
  if ((/<[^>]*>/.test(p.firstComment) || (live && /<[^>]*>/.test(p.text))) && !/placeholder/i.test(p.notes)) {
    err(id, 'a placeholder in the text or first comment, but the notes don\'t say so');
  }
}

// feed safe area
const SAFE = path.join(ROOT, 'design-system', 'safe-area.json');
const safe = fs.existsSync(SAFE) ? JSON.parse(fs.readFileSync(SAFE, 'utf8')) : { files: {}, waived: {} };
const today = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Chicago' }).format(new Date());
const feed = new Map();
for (const p of lib) {
  if (!['instagram', 'facebook'].includes(p.channel) || !['image', 'carousel'].includes(p.format)) continue;
  if (!['draft', 'approved'].includes(p.status) || p.date < today) continue;
  for (const f of p.files ?? []) {
    if (f.path.endsWith('.png') && fs.existsSync(path.join(ROOT, f.path))) feed.set(f.path, [...(feed.get(f.path) ?? []), p.id]);
  }
}
// The Nov 16 expand-step check is gone (Philip, Nov 18): posts publish through Buffer, which sends the full 4:5,
// so there is no phone-app step. The feed safe area below is what keeps every word visible.
const safeOk = [], waived = [];
for (const [file, ids] of feed) {
  const buf = fs.readFileSync(path.join(ROOT, file));
  const w = buf.readUInt32BE(16), h = buf.readUInt32BE(20);
  if (h <= w) { safeOk.push(file); continue; } // square or landscape: nothing to crop
  const rec = safe.files?.[file];
  const sha = crypto.createHash('sha256').update(buf).digest('hex');
  if (rec && rec.sha256 === sha) safeOk.push(file);
  else if (safe.waived?.[file]) waived.push(`${file} (${ids.join(', ')}): ${safe.waived[file]}`);
  else err(ids.join(', '), `${file} (${w}x${h}) has no passing safe-area record: render it with templates/render_many.js (content inside y 150 to 1200)`);
}
const safeLine = `safe area: ${feed.size} feed PNG(s) still to post, ${safeOk.length} pass, ${waived.length} waived`;
if (waived.length) {
  console.warn(`${safeLine}. Waived (they cross y 150 to 1200; see design-system/safe-area.json):`);
  for (const x of waived) console.warn(`  ${x}`);
}

if (errors.length) {
  console.error(safeLine);
  console.error(`library.json: ${errors.length} problem(s)`);
  for (const e of errors) console.error(`  ${e}`);
  process.exit(1);
}
console.log(`library.json OK: ${lib.length} posts, text matches posts.md, every file exists; ${safeLine}.`);
