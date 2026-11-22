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
// Sizes per channel (HQ, Nov 22, after Meta Business Suite cropped the natively scheduled Instagram posts): every
// post still to post (draft or approved, dated today or later in Chicago) is checked file by file against its
// channel and format, by the size read from the file's own bytes (PNG and JPEG headers, a PDF's page boxes, an
// MP4's video track), never by its name. Any mismatch fails the run. The table is SIZE_RULES below and playbook §9b.
// The feed record must also confirm the Instagram grid's 3:4 view (key content inside x 34 to 1046: grid: true),
// and an Instagram Reel's cover needs a record in reelCovers (key content inside the center 1080x1440, y 240 to 1680).
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
const OPTIONAL = ['guide'];
// Guide of the week (HQ, Nov 19; playbook §5 and §7b): the guides in getday60.com/guides reading order, no comparison guides
const GUIDES = ['how-to-find-the-hiring-manager', 'how-to-message-a-hiring-manager', 'follow-up-after-no-reply',
  '500-applications-no-interviews', 'how-to-message-a-recruiter', 'linkedin-connection-note-examples',
  'hiring-manager-message-examples-by-role', 'how-to-follow-up-after-applying', 'thank-you-message-after-linkedin-connection',
  'how-to-ask-for-an-informational-interview', 'how-to-ask-for-a-referral', 'how-to-write-a-thank-you-note-after-an-interview'];

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

// ---- real file sizes, read from the bytes ----
function mp4Size(b) {
  const boxes = (s, e) => {
    const out = [];
    for (let i = s; i + 8 <= e;) {
      let size = b.readUInt32BE(i), hdr = 8;
      const type = b.toString('latin1', i + 4, i + 8);
      if (size === 1) { size = Number(b.readBigUInt64BE(i + 8)); hdr = 16; } else if (size === 0) size = e - i;
      if (size < hdr) break;
      out.push({ type, s: i + hdr, e: Math.min(i + size, e) });
      i += size;
    }
    return out;
  };
  for (const moov of boxes(0, b.length).filter((x) => x.type === 'moov')) {
    for (const trak of boxes(moov.s, moov.e).filter((x) => x.type === 'trak')) {
      const kids = boxes(trak.s, trak.e);
      const mdia = kids.find((x) => x.type === 'mdia');
      const hdlr = mdia && boxes(mdia.s, mdia.e).find((x) => x.type === 'hdlr');
      const tkhd = kids.find((x) => x.type === 'tkhd');
      if (!hdlr || !tkhd || b.toString('latin1', hdlr.s + 8, hdlr.s + 12) !== 'vide') continue;
      const m = tkhd.s + (b[tkhd.s] === 1 ? 36 : 24) + 16; // the matrix, after the times, ids, layer and volume
      let w = Math.round(b.readUInt32BE(m + 36) / 65536), h = Math.round(b.readUInt32BE(m + 40) / 65536);
      if (b.readInt32BE(m) === 0 && b.readInt32BE(m + 4) !== 0) [w, h] = [h, w]; // rotated 90 degrees
      return { w, h };
    }
  }
  return { w: 0, h: 0 };
}
function mediaInfo(abs) {
  const b = fs.readFileSync(abs);
  if (b.length > 24 && b.readUInt32BE(0) === 0x89504e47) return { kind: 'image', w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
  if (b[0] === 0xff && b[1] === 0xd8) {
    for (let i = 2; i + 9 < b.length;) {
      if (b[i] !== 0xff) { i++; continue; }
      const mk = b[i + 1];
      if (mk === 0xff || mk === 0x01 || (mk >= 0xd0 && mk <= 0xd8)) { i += mk === 0xff ? 1 : 2; continue; }
      if (mk >= 0xc0 && mk <= 0xcf && ![0xc4, 0xc8, 0xcc].includes(mk)) return { kind: 'image', w: b.readUInt16BE(i + 7), h: b.readUInt16BE(i + 5) };
      i += 2 + b.readUInt16BE(i + 2);
    }
    return { kind: 'image', w: 0, h: 0 };
  }
  if (b.toString('latin1', 4, 8) === 'ftyp') return { kind: 'video', ...mp4Size(b) };
  if (b.toString('latin1', 0, 5) === '%PDF-') {
    const t = b.toString('latin1');
    const pages = (t.match(/\/Type\s*\/Page(?![A-Za-z])/g) || []).length;
    const boxes = [...t.matchAll(/\/MediaBox\s*\[\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*\]/g)]
      .map((m) => ({ w: +m[3] - +m[1], h: +m[4] - +m[2] }));
    return { kind: 'pdf', pages, boxes };
  }
  return { kind: 'unknown' };
}
// Per channel and format (HQ, Nov 22; playbook §9b). feed/video/cover/page: the allowed WxH of those files.
const SIZE_RULES = {
  instagram: { image: { feed: ['1080x1350'] }, carousel: { feed: ['1080x1350'] },
    video: { video: ['1080x1920'], cover: ['1080x1920'], coverRequired: true } },
  facebook: { text: {}, image: { feed: ['1080x1350'] }, carousel: { feed: ['1080x1350'] },
    video: { video: ['1080x1920'], cover: ['1080x1920'] } },
  linkedin: { text: {}, image: { feed: ['1080x1350', '1200x1200'] }, document: { pdf: true, page: ['1080x1350'] },
    video: { video: ['1080x1350', '1080x1920'] } },
};
function checkSizes(p) {
  const rule = SIZE_RULES[p.channel]?.[p.format];
  if (!rule) return [`no ${p.channel} ${p.format} posts (no size rule for it)`];
  const out = [], files = p.files ?? [];
  const info = files.map((f) => ({ path: f.path, ...(fs.existsSync(path.join(ROOT, f.path)) ? mediaInfo(path.join(ROOT, f.path)) : { kind: 'missing' }) }));
  const dim = (x) => `${x.w}x${x.h}`;
  const want = (x, sizes, what) => { if (!sizes.includes(dim(x))) out.push(`${x.path} is ${dim(x)}; ${p.channel} ${what} must be ${sizes.join(' or ')}`); };
  const kind = (x, k) => { if (x.kind !== k) { out.push(`${x.path} is ${x.kind === 'unknown' ? 'not an image, video or PDF' : `a ${x.kind}`}, expected a ${k}`); return false; } return true; };
  if (p.format === 'text') {
    if (files.length) out.push(`a text post lists ${files.length} file(s); a text or link post has none`);
  } else if (p.format === 'image' || p.format === 'carousel') {
    if (p.format === 'image' && files.length !== 1) out.push(`an image post has ${files.length} files, not 1`);
    if (p.format === 'carousel' && (files.length < 2 || files.length > 10)) out.push(`a carousel has ${files.length} slides (2 to 10)`);
    for (const x of info) if (kind(x, 'image')) want(x, rule.feed, p.format === 'carousel' ? 'carousel slides' : 'images');
  } else if (p.format === 'video') {
    const [v, ...rest] = info;
    if (!v) out.push('a video post with no video');
    else if (kind(v, 'video')) want(v, rule.video, 'video');
    if (rule.coverRequired && rest.length !== 1) out.push(`a Reel lists ${rest.length} cover file(s), not 1`);
    for (const x of rest) if (kind(x, 'image')) want(x, rule.cover, 'Reel covers');
  } else if (p.format === 'document') {
    const [d, ...pages] = info;
    if (d && kind(d, 'pdf')) {
      if (!d.pages || !d.boxes.length) out.push(`${d.path}: can't read its page size`);
      for (const bx of d.boxes) if (Math.abs(bx.w / bx.h - 0.8) > 0.004) out.push(`${d.path} has a ${bx.w}x${bx.h} pt page; pages must be 1080x1350 (4:5)`);
    }
    for (const x of pages) if (kind(x, 'image')) want(x, rule.page, 'document pages');
  }
  return out;
}
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
  const extra = keys.filter((k) => !KEYS.includes(k) && !OPTIONAL.includes(k));
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

  // guide of the week: LinkedIn and Facebook link the guide with UTMs; Instagram's caption names getday60.com/guides
  if ('guide' in p) {
    const esc = (x) => x.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const url = new RegExp(`https://getday60\\.com/guides/${esc(String(p.guide))}\\?utm_source=${p.channel}&utm_medium=social&utm_campaign=\\d{4}-w\\d{2}&utm_content=[a-z0-9-]+`);
    if (!GUIDES.includes(p.guide)) err(id, `guide "${p.guide}" is not one of the ${GUIDES.length} guides in reading order (no comparison guides)`);
    else if (p.channel === 'instagram') {
      if (!/getday60\.com\/guides\b/.test(p.text)) err(id, 'guide post: the Instagram caption says the full guide is at getday60.com/guides');
    } else if (!url.test(p.text)) err(id, `guide post: the text links https://getday60.com/guides/${p.guide} with this channel's UTMs`);
  }
  if (p.firstComment !== p.firstComment.trim()) err(id, 'firstComment has leading or trailing whitespace');
  if ((/<[^>]*>/.test(p.firstComment) || (live && /<[^>]*>/.test(p.text))) && !/placeholder/i.test(p.notes)) {
    err(id, 'a placeholder in the text or first comment, but the notes don\'t say so');
  }
}

// sizes per channel and format, for every post still to post
const SAFE = path.join(ROOT, 'design-system', 'safe-area.json');
const safe = fs.existsSync(SAFE) ? JSON.parse(fs.readFileSync(SAFE, 'utf8')) : { files: {}, waived: {}, reelCovers: {} };
const today = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Chicago' }).format(new Date());
const toPost = lib.filter((p) => ['draft', 'approved'].includes(p?.status) && typeof p?.date === 'string' && p.date >= today);
let sizeOk = 0;
for (const p of toPost) {
  const bad = checkSizes(p);
  for (const b of bad) err(p.id, `size: ${b}`);
  // an Instagram Reel's cover: key content inside the center 1080x1440 the grid shows (HQ, Nov 22)
  if (p.channel === 'instagram' && p.format === 'video') {
    for (const f of (p.files ?? []).slice(1)) {
      const abs = path.join(ROOT, f.path);
      if (!fs.existsSync(abs)) continue;
      const rec = safe.reelCovers?.[f.path];
      const sha = crypto.createHash('sha256').update(fs.readFileSync(abs)).digest('hex');
      if (!rec || rec.sha256 !== sha) { bad.push('cover'); err(p.id, `${f.path} has no passing Reel-cover record (key content inside y 240 to 1680) in design-system/safe-area.json`); }
    }
  }
  if (!bad.length) sizeOk++;
}
const sizeLine = `sizes: ${toPost.length} post(s) still to post, ${sizeOk} at their channel's sizes`;

// feed safe area
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
  if (rec && rec.sha256 === sha && rec.grid) safeOk.push(file);
  else if (rec && rec.sha256 === sha) err(ids.join(', '), `${file} has no 3:4 grid check (key content inside x 34 to 1046): render it again with templates/render_many.js`);
  else if (safe.waived?.[file]) waived.push(`${file} (${ids.join(', ')}): ${safe.waived[file]}`);
  else err(ids.join(', '), `${file} (${w}x${h}) has no passing safe-area record: render it with templates/render_many.js (content inside y 150 to 1200)`);
}
const safeLine = `safe area: ${feed.size} feed PNG(s) still to post, ${safeOk.length} pass, ${waived.length} waived`;
if (waived.length) {
  console.warn(`${safeLine}. Waived (they cross y 150 to 1200; see design-system/safe-area.json):`);
  for (const x of waived) console.warn(`  ${x}`);
}

if (errors.length) {
  console.error(sizeLine);
  console.error(safeLine);
  console.error(`library.json: ${errors.length} problem(s)`);
  for (const e of errors) console.error(`  ${e}`);
  process.exit(1);
}
console.log(`library.json OK: ${lib.length} posts, text matches posts.md, every file exists; ${sizeLine}; ${safeLine}.`);
