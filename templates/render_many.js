// Render many HTML files to PNG with Playwright.
// Usage: node templates/render_many.js jobs.json
// jobs.json: [{"html": "/abs/in.html", "png": "/abs/out.png", "w": 1080, "h": 1350}, ...]
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const b = await chromium.launch();
  for (const j of jobs) {
    const p = await b.newPage({ viewport: { width: j.w || 1080, height: j.h || 1350 } });
    await p.goto('file://' + j.html, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(250);
    await p.screenshot({ path: j.png, omitBackground: !!j.transparent });
    await p.close();
    console.log('ok', j.png);
  }
  await b.close();
})();
