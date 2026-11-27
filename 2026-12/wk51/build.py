"""Week 51 Instagram cards, drafts for HQ (Social, Nov 27; HQ's Thursday verdict: more resume-tool posts,
message craft, about 1 in 4 humor). None says "Link in bio", so Facebook reuses each card as it is.

2026-12/wk51/p01_tailor_coral.png         IG-tailor    Tue Dec 15  resume builder: only what's true
2026-12/wk51/p02_keyword_gap_cobalt.png   IG-gap       Wed Dec 16  resume builder: the keyword gap
2026-12/wk51/p03_seven_rounds_pink.png    IG-rounds    Fri Dec 18  humor: round 7, ask before round one
2026-12/wk51/p04_first_line_mint.png      IG-firstline Sat Dec 19  message craft: the first line is about them
2026-12/wk51/p05_wishlist_ink.png         IG-wishlist  Sun Dec 20  humor, seasonal: Tick's holiday wish list

Grid: Mon cream (IG4-r2), Tue coral, Wed cobalt, Thu lime (IG-firstjob-r2), Fri pink, Sat mint, Sun ink:
any 4 in a row differ. One lime element per card; lime is never text.

Run from repo root: python3 2026-12/wk51/build.py [names to render, default all]
"""
import json, os, subprocess, sys, tempfile
WK = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(WK))
sys.path.insert(0, os.path.join(ROOT, "design-system"))
from grounds import *  # noqa

TMP = tempfile.mkdtemp(prefix="wk51_")
jobs = []


def out(name, html):
    p = os.path.join(TMP, name + ".html"); open(p, "w").write(html)
    jobs.append({"html": p, "png": os.path.join(WK, name + ".png"), "w": 1080, "h": 1350})


def at(x, y, html, right=False):
    return f'<div style="position:absolute;{"right" if right else "left"}:{x}px;top:{y}px">{html}</div>'


def stk(text, bg, x, y, size=28):
    return at(x, y, f'<span class="sticker" style="background:{bg};font-size:{size}px">{text}</span>')


RB = "getday60.com/resume-builder"

# IG-tailor · coral (ink text only). The lime highlight is the one lime element.
g = "coral"
out("p01_tailor_coral", cover_page(
    stk("Free resume builder", WHITE, 72, 72)
    + f'<div class="d" style="position:absolute;left:72px;right:72px;top:200px;font-size:132px">Tailor it. Don\'t invent it.</div>'
    + f'<div style="position:absolute;left:74px;top:560px;width:600px;font-size:42px;font-weight:700;line-height:1.24">'
      f'It rewrites your bullets for one job, using only what your resume and your notes show.</div>'
    + f'<div class="card" style="position:absolute;left:72px;top:860px;width:610px;padding:32px 38px;'
      f'font-size:40px;font-weight:700;line-height:1.28">No new skill, number or title. '
      f'<span class="fill" style="color:{INK}">Only what\'s true.</span></div>'
    + at(56, 640, tick("pointing", 290), right=True)
    + spark(900, 110, 60, WHITE) + spark(990, 220, 34, INK)
    + foot_g(g, right=RB), g))

# IG-gap · cobalt (white text). The lime sticker is the one lime element.
g = "cobalt"
out("p02_keyword_gap_cobalt", cover_page(
    stk("The keyword gap", LIME, 72, 72)
    + f'<div class="d c" style="position:absolute;left:72px;right:72px;top:200px;font-size:112px">Not on your resume yet? It stays off.</div>'
    + f'<div class="c" style="position:absolute;left:74px;top:590px;width:610px;font-size:40px;font-weight:600;line-height:1.26">'
      f'Words the posting asks for that your resume can\'t back up get their own list: keywords you can\'t claim yet.</div>'
    + f'<div class="card" style="position:absolute;left:72px;top:900px;width:610px;padding:32px 38px;'
      f'font-size:40px;font-weight:700;line-height:1.28">Treat that list as homework, not as words to paste in.</div>'
    + at(56, 660, tick("pointing", 290), right=True)
    + spark(900, 110, 60, WHITE) + spark(990, 220, 34, PINK)
    + foot_g(g, right=RB), g))

# IG-rounds · pink, humor. The lime highlight is the one lime element.
g = "pink"
out("p03_seven_rounds_pink", cover_page(
    stk("Interview update", WHITE, 72, 72)
    + f'<div class="d" style="position:absolute;left:72px;right:72px;top:200px;font-size:118px">Round 7: “a quick chat with the team.”</div>'
    + f'<div style="position:absolute;left:74px;top:600px;width:600px;font-size:44px;font-weight:700;line-height:1.24">'
      f'Nobody plans seven rounds. They just happen.</div>'
    + f'<div class="card" style="position:absolute;left:72px;top:840px;width:620px;padding:32px 38px;'
      f'font-size:40px;font-weight:700;line-height:1.3">Before round one, ask how many rounds there are and '
      f'<span class="fill" style="color:{INK}">who decides.</span></div>'
    + at(56, 620, tick("celebrating", 290), right=True)
    + spark(900, 110, 64, WHITE) + spark(990, 230, 36, INK)
    + foot_g(g), g))

# IG-firstline · mint. The lime highlight on "about them" is the one lime element.
g = "mint"
out("p04_first_line_mint", cover_page(
    stk("Message craft", WHITE, 72, 72)
    + f'<div class="d" style="position:absolute;left:72px;right:72px;top:200px;font-size:118px">'
      f'Your first line is <span class="fill">about them.</span></div>'
    + f'<div class="card" style="position:absolute;left:72px;top:520px;width:660px;padding:28px 36px;'
      f'font-size:34px;font-weight:600;line-height:1.3"><div class="lbl" style="font-size:26px;letter-spacing:.06em">NOT THIS</div>'
      f'“I\'m reaching out to express my strong interest in the role.”</div>'
    + f'<div class="card" style="position:absolute;left:72px;top:790px;width:660px;padding:28px 36px;'
      f'font-size:34px;font-weight:700;line-height:1.3"><div class="lbl" style="font-size:26px;letter-spacing:.06em">THIS</div>'
      f'“Saw your support team is hiring two leads after the launch.”</div>'
    + f'<div style="position:absolute;left:74px;top:1050px;font-size:26px;font-weight:700">Illustrative example</div>'
    + at(40, 700, tick("pointing", 250), right=True)
    + spark(900, 110, 60, WHITE) + spark(990, 220, 34, INK)
    + foot_g(g), g))

# IG-wishlist · ink, humor, seasonal. The lime highlight is the one lime element.
g = "ink"
out("p05_wishlist_ink", cover_page(
    stk("Holiday edition", PINK, 72, 72)
    + f'<div class="d c" style="position:absolute;left:72px;right:72px;top:200px;font-size:122px">Tick\'s holiday<br>wish list</div>'
    + f'<div class="card" style="position:absolute;left:72px;top:560px;width:640px;padding:36px 42px;'
      f'font-size:44px;font-weight:700;line-height:1.5">1. Short notes.<br>'
      f'2. <span class="fill" style="color:{INK}">One easy question.</span><br>'
      f'3. Never “just following up.”</div>'
    + f'<div class="c" style="position:absolute;left:74px;top:960px;width:600px;font-size:38px;font-weight:600;line-height:1.3">'
      f'Your next message can tick all three.</div>'
    + at(60, 620, tick("celebrating", 290), right=True)
    + spark(900, 110, 64, PINK) + spark(990, 230, 36, MINT)
    + foot_g(g), g))

if __name__ == "__main__":
    only = sys.argv[1:]
    if only:
        jobs = [j for j in jobs if os.path.basename(j["png"])[:-4] in only]
    jf = os.path.join(TMP, "jobs.json"); json.dump(jobs, open(jf, "w"))
    subprocess.run(["node", os.path.join(ROOT, "templates", "render_many.js"), jf], check=True)
