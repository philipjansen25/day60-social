// Render many HTML files to PNG with Playwright.
// Usage: node templates/render_many.js jobs.json
// jobs.json: [{"html": "/abs/in.html", "png": "/abs/out.png", "w": 1080, "h": 1350}, ...]
//
// Feed safe area (HQ, Nov 16): Instagram may show a 1080x1350 feed post as its centered square. On every page
// built with design-system page() at 1080x1350, this calls d60Safe.fit() (shrinks the content layer just enough
// to sit inside y 150 to 1200), then d60Safe.measure(). Any non-decorative element still outside fails the
// render: no PNG is written and the run exits 1. Each PNG that passes is recorded, with its SHA-256, in
// design-system/safe-area.json; scripts/check-library.mjs reads that record for every feed PNG still to post.
// D60_OUT_SUFFIX=_safe writes x.png as x_safe.png (new files beside the old ones).
// D60_SAFE_REPORT=1 only reports: it measures each 1080x1350 page as laid out (no fit, scale 1), prints what
// crosses y 150 to 1200, and writes no PNG and no record. Use it to check a file rendered before the rule.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ROOT = path.resolve(__dirname, '..');
const RECORDS = path.join(ROOT, 'design-system', 'safe-area.json');
const SUFFIX = process.env.D60_OUT_SUFFIX || '';
const REPORT = process.env.D60_SAFE_REPORT === '1';

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const rec = fs.existsSync(RECORDS) ? JSON.parse(fs.readFileSync(RECORDS, 'utf8')) : { files: {}, waived: {} };
  const b = await chromium.launch();
  let failed = 0;
  for (const j of jobs) {
    const png = SUFFIX ? j.png.replace(/\.png$/, `${SUFFIX}.png`) : j.png;
    const p = await b.newPage({ viewport: { width: j.w || 1080, height: j.h || 1350 } });
    await p.goto('file://' + j.html, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(250);
    if (REPORT) {
      const bad = await p.evaluate(() => (window.d60Safe ? window.d60Safe.measure() : null));
      const name = path.relative(ROOT, png);
      if (bad === null) console.log(`report ${name}: not a 1080x1350 page() slide`);
      else if (!bad.length) console.log(`report ${name}: inside y 150 to 1200 at scale 1`);
      else {
        console.log(`report ${name}: CROSSES at scale 1`);
        for (const x of bad) console.log(`  <${x.tag} class="${x.cls}"> y ${x.top} to ${x.bottom} "${x.text}"`);
      }
      await p.close();
      continue;
    }
    const scale = await p.evaluate(() => (window.d60Safe ? window.d60Safe.fit() : null));
    if (scale !== null) {
      await p.waitForTimeout(50);
      const bad = await p.evaluate(() => window.d60Safe.measure());
      if (bad.length) {
        failed++;
        console.error(`FAIL safe area (y 150 to 1200) ${png}`);
        for (const x of bad) console.error(`  <${x.tag} class="${x.cls}"> y ${x.top} to ${x.bottom} "${x.text}"`);
        await p.close();
        continue;
      }
    }
    await p.screenshot({ path: png, omitBackground: !!j.transparent });
    await p.close();
    const rel = path.relative(ROOT, png);
    if (scale !== null && !rel.startsWith('..')) {
      const sha256 = crypto.createHash('sha256').update(fs.readFileSync(png)).digest('hex');
      rec.files[rel] = { sha256, scale, checked: new Date().toISOString().slice(0, 10) };
    }
    console.log('ok', png, scale !== null ? `(safe area ok, scale ${scale})` : '');
  }
  await b.close();
  if (REPORT) return;
  rec.files = Object.fromEntries(Object.entries(rec.files).sort());
  fs.writeFileSync(RECORDS, JSON.stringify(rec, null, 1) + '\n');
  if (failed) {
    console.error(`${failed} render(s) failed the safe-area check`);
    process.exit(1);
  }
})();
