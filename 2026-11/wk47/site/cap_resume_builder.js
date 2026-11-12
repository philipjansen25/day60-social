// Live crop of getday60.com/resume-builder for IG-resume slide 2 (shot at 390px wide, 2x).
// Types an invented job link into the Job link field; nothing is submitted.
// Run from repo root: NODE_EXTRA_CA_CERTS=<proxy CA> node 2026-11/wk47/site/cap_resume_builder.js
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;
  const b = await chromium.launch({ proxy });
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage();
  await p.goto('https://getday60.com/resume-builder', { waitUntil: 'domcontentloaded', timeout: 45000 });
  await p.waitForTimeout(4000);
  const f = p.getByLabel('Job link');
  await f.fill('https://northpine.example/jobs/csm');
  await f.evaluate((el) => { el.blur(); el.scrollLeft = 0; });
  await p.waitForTimeout(500);
  const top = await p.getByText('The job', { exact: true }).boundingBox();
  const end = await p.getByText('A PDF or Word (.docx) file, up to 5 MB.').boundingBox();
  const card = await p.locator('form').first().boundingBox();
  const clip = { x: card.x, y: top.y - 24, width: card.width, height: end.y + end.height + 20 - (top.y - 24) };
  await p.screenshot({ path: path.join(__dirname, 'resume_builder_form.png'), clip, fullPage: true });
  console.log(JSON.stringify({ card, clip }));
  await b.close();
})().catch((e) => { console.error(e.message); process.exit(1); });
