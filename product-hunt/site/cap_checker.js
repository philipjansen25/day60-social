// Live capture of getday60.com/message-checker with an invented draft (Sam to Dana at Northpine).
// Usage: node product-hunt/site/cap_checker.js <out-dir>  (writes checker_full.png + checker_rects.json; build.py uses the crop)
const { chromium } = require('playwright');
const out = process.argv[2];
const SUBJ = "Following up on my application for the Account Executive role at Northpine";
const MSG = "I hope this email finds you well! I wanted to reach out because I recently applied for the Account Executive position and I am very passionate about sales — I believe I would be a great fit — I have 5 years of experience closing deals and exceeding quota. I'd love to pick your brain sometime. Looking forward to hearing from you!";
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1270, height: 900 }, deviceScaleFactor: 2 });
  await p.goto('https://getday60.com/message-checker', { waitUntil: 'networkidle' });
  await p.check('input[name=checker-channel] >> nth=0');
  await p.getByLabel('Subject line').fill(SUBJ);
  await p.getByPlaceholder('Paste your message here.').fill(MSG);
  await p.getByRole('button', { name: 'Check my message' }).click();
  await p.waitForTimeout(1500);
  await p.evaluate(() => window.scrollTo(0, 0));
  await p.waitForTimeout(300);
  const r = await p.evaluate(() => {
    const abs = e => { const b = e.getBoundingClientRect(); return { x: b.left + scrollX, y: b.top + scrollY, w: b.width, h: b.height }; };
    let c = [...document.querySelectorAll('h2')].find(h => h.textContent.includes('Tick’s checklist'));
    while (c && getComputedStyle(c).borderTopWidth === '0px') c = c.parentElement;
    const leaf = t => [...c.querySelectorAll('*')].find(e => e.children.length === 0 && e.textContent.includes(t));
    return { card: abs(c), q: abs(leaf('One clear question is easy')), form: abs(document.querySelector('form')) };
  });
  console.log(JSON.stringify(r));
  await p.screenshot({ path: out + '/checker_full.png', fullPage: true });
  require('fs').writeFileSync(out + '/checker_rects.json', JSON.stringify(r));
  await b.close();
})();
