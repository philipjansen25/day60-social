#!/usr/bin/env node
// Day60 Reddit scan (4-day window by default; HQ, Nov 6): finds fresh Reddit threads through Google's index (SerpAPI, Google engine).
// It never fetches reddit.com, never uses mirrors, never stores usernames.
//
// Usage:
//   SERPAPI_API_KEY=... node scripts/reddit-scan.mjs [--days 4] [--max 5] [--out file.json]
//   node scripts/reddit-scan.mjs --fixture scripts/fixtures/serpapi-sample.json   (offline test)
//   node scripts/reddit-scan.mjs --queries   (print the Google queries, no key needed)
//   add --debug [file] to write why each result was dropped (reason, subreddit, title, age; no snippets,
//   no usernames) to a JSON file outside the repo. Default: <os tmpdir>/reddit-scan-debug.json. Never commit it.
//
// Output: JSON array of {title, url, subreddit, date, snippet, score, matched} on stdout (or --out).
// Exit codes: 0 ok, 2 SERPAPI_API_KEY not set, 3 SerpAPI error.

import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const args = Object.fromEntries(process.argv.slice(2).reduce((acc, a, i, all) => {
  if (a.startsWith('--')) acc.push([a.slice(2), all[i + 1] && !all[i + 1].startsWith('--') ? all[i + 1] : true]);
  return acc;
}, []));
const DAYS = Number(args.days || 4);
const MAX = Number(args.max || 5);
const MIN_SCORE = 2;
const MAX_PER_SUB = Number(args['per-sub'] || 2);
const MAX_AGE_DAYS = 7;

// Subreddits come from reddit/subreddits.md (table rows that start with "| r/").
function readSubs() {
  const md = fs.readFileSync(path.join(ROOT, 'reddit/subreddits.md'), 'utf8');
  return [...md.matchAll(/^\| r\/([A-Za-z0-9_]+) \|/gm)].map(m => m[1]);
}
// r/SideProject and r/startups are for value posts later, not question threads.
const SKIP_FOR_REPLIES = new Set(['SideProject', 'startups']);

// Topics Day60's method answers. Each becomes part of a Google query.
const TOPICS = [
  { key: 'no-replies', q: '("no response" OR "no responses" OR "no replies" OR ghosted OR "no interviews") applications' },
  { key: 'reach-people', q: '("hiring manager" OR recruiter) (message OR email OR "reach out" OR "cold") LinkedIn' },
];
// Signals used to score fit from the title + snippet.
const SIGNALS = [
  [/hiring manager/i, 3], [/recruiter/i, 2], [/cold (email|message|outreach|call)/i, 3], [/reach(ing)? out/i, 2],
  [/linkedin (message|dm|inmail)/i, 2], [/no (response|responses|replies|callbacks|interviews)/i, 3], [/ghost(ed|ing)?/i, 2],
  [/follow(ing)?[- ]up/i, 2], [/referral/i, 1], [/applied to \d+|hundreds of (jobs|applications)/i, 2], [/\?/, 1],
];
const NEGATIVE = [/\bhiring\b.*\[hiring\]|\[for hire\]|\bmegathread\b|\bweekly\b.*thread/i, /\bscam\b/i];

function chunk(list, n) { const out = []; for (let i = 0; i < list.length; i += n) out.push(list.slice(i, i + n)); return out; }

function queries(subs) {
  const groups = chunk(subs.filter(s => !SKIP_FOR_REPLIES.has(s)), 4).slice(0, 3); // 3 sub groups x 2 topics = 6 searches
  const qs = [];
  for (const g of groups) for (const t of TOPICS) {
    // inurl:comments keeps Google to thread pages, not sub front pages or how-to pages (HQ, Nov 10).
    qs.push({ topic: t.key, q: `(${g.map(s => `site:reddit.com/r/${s}`).join(' OR ')}) inurl:comments ${t.q}` });
  }
  return qs;
}

const scrub = s => String(s || '').replace(/\bu\/[A-Za-z0-9_-]+/g, 'u/[user]').replace(/\s+/g, ' ').trim();

function threadFrom(r) {
  const m = String(r.link || '').match(/^https?:\/\/(?:www\.|old\.)?reddit\.com\/r\/([A-Za-z0-9_]+)\/comments\/([a-z0-9]+)(?:\/([^/?#]*))?/i);
  if (!m) return null;
  return {
    title: scrub(r.title).replace(/\s*:\s*r\/\w+\s*$/i, '').replace(/\s*-\s*Reddit\s*$/i, ''),
    url: `https://www.reddit.com/r/${m[1]}/comments/${m[2]}/${m[3] || ''}`.replace(/\/$/, '/'),
    id: m[2].toLowerCase(),
    subreddit: m[1],
    date: r.date || null,
    snippet: scrub(r.snippet),
  };
}

function alreadyUsedIds() {
  const dir = path.join(ROOT, 'reddit');
  const ids = new Set();
  for (const f of fs.readdirSync(dir).filter(f => /^\d{4}-\d{2}-\d{2}\.md$/.test(f))) {
    for (const m of fs.readFileSync(path.join(dir, f), 'utf8').matchAll(/reddit\.com\/r\/\w+\/comments\/([a-z0-9]+)/gi)) ids.add(m[1].toLowerCase());
  }
  return ids;
}

// Age in days from Google's date field or an "Xmo ago"-style marker in the snippet; null if unknown.
function ageDays(t) {
  // Only Google's date field or the date prefix Google puts at the start of a snippet ("3mo ago · ...").
  const text = t.date ? String(t.date) : String(t.snippet || '').slice(0, 24);
  const rel = text.match(/\b(\d+)\s*(h|hr|hrs|hours?|d|days?|w|wk|weeks?|mo|months?|y|yr|years?)\s+ago\b/i);
  if (rel) {
    const n = Number(rel[1]), u = rel[2].toLowerCase();
    if (u.startsWith('h')) return n / 24;
    if (u.startsWith('d')) return n;
    if (u.startsWith('w')) return n * 7;
    if (u.startsWith('mo')) return n * 30;
    if (u.startsWith('y')) return n * 365;
  }
  const abs = Date.parse(String(t.date || ''));
  return Number.isNaN(abs) ? null : (Date.now() - abs) / 864e5;
}

// Where ageDays() read the age from: Google's date field, the snippet's date prefix, or nowhere.
function ageSource(t) {
  if (t.date) return 'google-date';
  return /\b\d+\s*(h|hr|hrs|hours?|d|days?|w|wk|weeks?|mo|months?|y|yr|years?)\s+ago\b/i.test(String(t.snippet || '').slice(0, 24)) ? 'snippet-prefix' : null;
}

function debugPath() {
  const p = path.resolve(args.debug === true ? path.join(os.tmpdir(), 'reddit-scan-debug.json') : String(args.debug));
  // The repo is public. Inside it, only the git-ignored name reddit-scan-debug*.json is allowed.
  if ((p + path.sep).startsWith(ROOT + path.sep) && !/^reddit-scan-debug.*\.json$/.test(path.basename(p))) {
    console.error(`--debug: refusing to write ${p} inside the repo. Use a path outside it (or a reddit-scan-debug*.json name, which is git-ignored).`);
    process.exit(4);
  }
  return p;
}

function score(t) {
  const text = `${t.title} ${t.snippet}`;
  if (NEGATIVE.some(re => re.test(text))) return { score: -1, matched: [] };
  let s = 0; const matched = [];
  for (const [re, w] of SIGNALS) if (re.test(text)) { s += w; matched.push(re.source); }
  return { score: s, matched };
}

async function serp(q, key) {
  const u = new URL('https://serpapi.com/search.json');
  u.search = new URLSearchParams({ engine: 'google', q, tbs: `qdr:d${DAYS}`, num: '10', hl: 'en', gl: 'us', api_key: key }).toString();
  const res = await fetch(u);
  if (!res.ok) throw new Error(`SerpAPI HTTP ${res.status}`);
  const j = await res.json();
  if (j.error && !/hasn't returned any results/i.test(j.error)) throw new Error(`SerpAPI: ${j.error}`);
  return j.organic_results || [];
}

async function main() {
  if (args.queries) { for (const q of queries(readSubs())) console.log(`[${q.topic}] ${q.q}`); return; }
  let results = [];
  if (args.fixture) {
    results = JSON.parse(fs.readFileSync(path.resolve(String(args.fixture)), 'utf8')).organic_results || [];
  } else {
    const key = process.env.SERPAPI_API_KEY;
    if (!key) {
      console.error('SERPAPI_API_KEY not set. Skipping the scan: use the fallback (search links + reply bank in reddit/YYYY-MM-DD.md).');
      process.exit(2);
    }
    for (const { q } of queries(readSubs())) {
      try { results.push(...await serp(q, key)); }
      catch (e) { console.error(String(e.message || e).replace(key, '[key]')); process.exit(3); }
    }
  }
  const used = alreadyUsedIds();
  const seen = new Set();
  const seenSub = {};
  const dropped = [];
  const drop = (reasons, t) => dropped.push({
    reason: reasons[0], reasons, subreddit: t.subreddit || null, title: t.title,
    ageDays: t.ageDays == null ? null : Math.round(t.ageDays * 10) / 10, ageSource: t.ageSource ?? null,
  });
  const candidates = [];
  for (const r of results) {
    const t = threadFrom(r);
    if (!t) {
      const sub = String(r.link || '').match(/reddit\.com\/r\/([A-Za-z0-9_]+)/i);
      drop(['not-thread-url'], { subreddit: sub ? sub[1] : null, title: scrub(r.title) });
      continue;
    }
    if (used.has(t.id)) { drop(['already-used'], t); continue; }
    if (seen.has(t.id)) { drop(['duplicate'], t); continue; }
    seen.add(t.id);
    const s = { ...t, ...score(t), ageDays: ageDays(t), ageSource: ageSource(t) };
    const reasons = [];
    if (s.score < 0) reasons.push('negative-match');
    if (s.ageDays !== null && s.ageDays > MAX_AGE_DAYS) reasons.push('too-old');
    if (s.score >= 0 && s.score < MIN_SCORE) reasons.push('low-score');
    if (reasons.length) { drop(reasons, s); continue; }
    candidates.push(s);
  }
  candidates.sort((a, b) => b.score - a.score);
  const picked = [];
  for (const t of candidates) {
    const n = (seenSub[t.subreddit] = (seenSub[t.subreddit] || 0) + 1);
    if (n > MAX_PER_SUB) { drop(['per-sub-cap'], t); continue; }
    if (picked.length >= MAX) { drop(['over-max'], t); continue; }
    const { id, ageSource: _src, ...keep } = t;
    picked.push(keep);
  }
  const out = JSON.stringify(picked, null, 2);
  if (args.out) fs.writeFileSync(String(args.out), out + '\n'); else console.log(out);
  console.error(`${DAYS}-day window: ${picked.length} thread(s) kept from ${results.length} search result(s).${picked.length < 3 ? ' Fewer than 3 fit: say so to HQ, do not pad.' : ''}`);
  if (args.debug) {
    const counts = {};
    for (const d of dropped) counts[d.reason] = (counts[d.reason] || 0) + 1;
    const file = debugPath();
    fs.writeFileSync(file, JSON.stringify({ window_days: DAYS, results: results.length, kept: picked.length, dropped_by_reason: counts, dropped }, null, 2) + '\n');
    console.error(`Dropped by reason: ${Object.entries(counts).map(([k, v]) => `${k} ${v}`).join(', ') || 'none'}. Debug file (do not commit): ${file}`);
  }
}

main();
