// Render print HTML to PDF with Playwright, and check each piece before it's written.
// Usage: node print/fairs/render_pdf.js jobs.json
// jobs.json: [{"html": "/abs/in.html", "pdf": "/abs/out.pdf", "w": "8.5in", "h": "11in"}, ...]
//
// Every page in the HTML is a <div class="pg" data-safe="N">. The checks, per piece (all its pages together):
// - no text is lime (#D9FF3F): lime is a fill only (HQ, Nov 13 and Nov 19)
// - exactly one lime element outside Tick (HQ, Nov 19: one lime element per piece)
// - every word, the QR code, Tick and every card sits at least N px (96 px = 1 in) inside its page's edge;
//   background art (class "bleed-art") may run to the edge
// Any failure writes no PDF and exits 1.
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const b = await chromium.launch();
  let failed = 0;
  for (const j of jobs) {
    const p = await b.newPage();
    await p.goto('file://' + j.html, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(250);
    const bad = await p.evaluate(() => {
      const out = [];
      const LIME = 'rgb(217, 255, 63)';
      const isLime = (c) => (c || '').replace(/\s+/g, ' ').toLowerCase() === LIME || /#d9ff3f/i.test(c || '');
      let limes = [];
      document.querySelectorAll('.pg *').forEach((el) => {
        if (el.closest('.d60-tick')) return; // Tick is the character, not a lime element
        const cs = getComputedStyle(el);
        const own = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
        if (own && isLime(cs.color)) out.push(`lime text: "${el.textContent.trim().slice(0, 40)}"`);
        if (isLime(cs.backgroundColor) || isLime(el.getAttribute('fill'))) limes.push(el.textContent.trim().slice(0, 40) || el.tagName);
      });
      if (limes.length !== 1) out.push(`lime elements: ${limes.length} (want 1): ${JSON.stringify(limes)}`);
      document.querySelectorAll('.pg').forEach((pg, i) => {
        const inset = parseFloat(pg.dataset.safe || '0');
        const P = pg.getBoundingClientRect();
        pg.querySelectorAll('*').forEach((el) => {
          if (el.closest('.bleed-art')) return;
          const tag = el.tagName.toLowerCase();
          if (tag !== 'svg' && el.closest('svg')) return;
          const cs = getComputedStyle(el);
          const own = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
          const boxed = parseFloat(cs.borderTopWidth) > 0 || cs.backgroundColor !== 'rgba(0, 0, 0, 0)';
          if (!(own || boxed || tag === 'svg')) return;
          const r = el.getBoundingClientRect();
          if (r.width < 1 || r.height < 1) return;
          const sh = parseFloat(el.dataset.shadow || '0'); // hard offset shadow, right and down
          if (r.left < P.left + inset - 0.5 || r.top < P.top + inset - 0.5 ||
              r.right + sh > P.right - inset + 0.5 || r.bottom + sh > P.bottom - inset + 0.5) {
            out.push(`page ${i + 1}: <${tag}> "${(el.textContent || '').trim().slice(0, 30)}" outside the ${inset}px margin ` +
              `(l ${Math.round(r.left - P.left)}, t ${Math.round(r.top - P.top)}, r ${Math.round(P.right - r.right - sh)}, b ${Math.round(P.bottom - r.bottom - sh)})`);
          }
        });
        if (pg.scrollHeight > pg.clientHeight + 1) out.push(`page ${i + 1}: content taller than the page`);
      });
      return out;
    });
    if (bad.length) {
      failed++;
      console.error(`FAIL ${j.pdf}`);
      for (const x of bad) console.error('  ' + x);
    } else {
      await p.pdf({ path: j.pdf, width: j.w, height: j.h, printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
      console.log(`ok ${j.pdf}`);
    }
    await p.close();
  }
  await b.close();
  process.exit(failed ? 1 : 0);
})();
