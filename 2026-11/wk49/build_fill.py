"""Fill-ins for the week of Nov 30 (Social, Fri Nov 27, drafts for HQ). Instagram had no post Fri Dec 4 to Sun Dec 6;
these three cards fill it, and Facebook reuses them on other days (no Facebook-only creative, HQ Nov 26).
None says "Link in bio", so Facebook reuses each card as it is.

2026-11/wk49/p04_under_review_pink.png    IG-review       Fri Dec 4  humor: "Status: under review"
2026-11/wk49/p05_no_attachments_mint.png  IG-attach       Sat Dec 5  message craft: no attachments on a first note
2026-11/wk49/p06_make_stronger_cobalt.png IG-stronger     Sun Dec 6  resume builder: answer its questions

Grid: Tue Dec 1 cream (IG6-r2), Wed lime, Thu coral, Fri pink, Sat mint, Sun cobalt, Mon Dec 7 ink, Tue Dec 8 pink:
any 4 in a row differ; cream once in 5. One lime element per card; lime is never text.

Run from repo root: python3 2026-11/wk49/build_fill.py [names to render, default all]
"""
import json, os, subprocess, sys, tempfile
WK = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(WK))
sys.path.insert(0, os.path.join(ROOT, "design-system"))
from grounds import *  # noqa

TMP = tempfile.mkdtemp(prefix="wk49fill_")
jobs = []


def out(name, html):
    p = os.path.join(TMP, name + ".html"); open(p, "w").write(html)
    jobs.append({"html": p, "png": os.path.join(WK, name + ".png"), "w": 1080, "h": 1350})


def at(x, y, html, right=False):
    return f'<div style="position:absolute;{"right" if right else "left"}:{x}px;top:{y}px">{html}</div>'


def stk(text, bg, x, y, size=28):
    return at(x, y, f'<span class="sticker" style="background:{bg};font-size:{size}px">{text}</span>')


# IG-review · pink, humor. The lime highlight is the one lime element.
g = "pink"
out("p04_under_review_pink", cover_page(
    stk("Application status", WHITE, 72, 72)
    + f'<div class="d c" style="position:absolute;left:72px;right:72px;top:200px;font-size:132px">Under review.</div>'
    + f'<div class="c" style="position:absolute;left:74px;top:400px;width:600px;font-size:46px;font-weight:700;line-height:1.24">'
      f'Last updated: about six weeks ago.</div>'
    + f'<div class="card" style="position:absolute;left:72px;top:640px;width:620px;padding:32px 38px;'
      f'font-size:42px;font-weight:700;line-height:1.35">Don\'t wait on the portal.<br>'
      f'<span class="fill" style="color:{INK}">Write to the hiring manager.</span></div>'
    + at(56, 620, tick("pointing", 290), right=True)
    + spark(900, 110, 64, WHITE) + spark(990, 230, 36, INK)
    + foot_g(g), g))

# IG-attach · mint. The lime highlight is the one lime element.
g = "mint"
out("p05_no_attachments_mint", cover_page(
    stk("Message craft", WHITE, 72, 72)
    + f'<div class="d c" style="position:absolute;left:72px;right:72px;top:200px;font-size:118px">No attachments on a first note.</div>'
    + f'<div class="c" style="position:absolute;left:74px;top:560px;width:600px;font-size:44px;font-weight:700;line-height:1.24">'
      f'A stranger\'s attachment is a file nobody opens.</div>'
    + f'<div class="card" style="position:absolute;left:72px;top:820px;width:620px;padding:32px 38px;'
      f'font-size:42px;font-weight:700;line-height:1.35">Three lines in the body.<br>'
      f'<span class="fill" style="color:{INK}">Send the resume when asked.</span></div>'
    + at(56, 600, tick("celebrating", 290), right=True)
    + spark(900, 110, 60, WHITE) + spark(990, 220, 34, INK)
    + foot_g(g), g))

# IG-stronger · cobalt, resume builder. The lime sticker is the one lime element.
g = "cobalt"
out("p06_make_stronger_cobalt", cover_page(
    stk("Free resume builder", LIME, 72, 72)
    + f'<div class="d c" style="position:absolute;left:72px;right:72px;top:200px;font-size:120px">Your best results are in your head.</div>'
    + f'<div class="card" style="position:absolute;left:72px;top:640px;width:620px;padding:32px 38px;'
      f'font-size:40px;font-weight:700;line-height:1.3">"Have you tracked which accounts might not renew?"'
      f'<div style="font-size:26px;font-weight:600;margin-top:12px">Example question</div></div>'
    + f'<div class="c" style="position:absolute;left:74px;top:960px;width:600px;font-size:38px;font-weight:600;line-height:1.3">'
      f'Answer its questions. Only what\'s true goes in.</div>'
    + at(56, 620, tick("pointing", 290), right=True)
    + spark(900, 110, 60, WHITE) + spark(990, 220, 34, PINK)
    + foot_g(g, right="getday60.com/resume-builder"), g))

if __name__ == "__main__":
    only = sys.argv[1:]
    if only:
        jobs = [j for j in jobs if os.path.basename(j["png"])[:-4] in only]
    jf = os.path.join(TMP, "jobs.json"); json.dump(jobs, open(jf, "w"))
    subprocess.run(["node", os.path.join(ROOT, "templates", "render_many.js"), jf], check=True)


def checker_fb():
    """FB-checker (Wed Dec 2) reuses IG6-r2's 7 checker slides. Slide 7 says "Free sprint: link in bio", which
    doesn't work on Facebook, so the Facebook copy paints that one line out with the slide's own flat ground."""
    from PIL import Image, ImageDraw
    src = os.path.join(ROOT, "2026-11/wk46/p15_checker_7_safe.png")
    im = Image.open(src).convert("RGB")
    bg = im.getpixel((60, 1060))
    ImageDraw.Draw(im).rectangle([100, 985, 560, 1060], fill=bg)
    im.save(os.path.join(WK, "p15_checker_7_fb.png"))


if __name__ == "__main__":
    checker_fb()
