"""Week 52 holiday cards (Social, Nov 27; drafts for HQ). Six Instagram cards, each reused once on Facebook.

2026-12/wk52/p02_quiet_resume_mint.png    IG-quietresume Tue Dec 22  (FB-quietresume Mon Dec 21)   resume tool
2026-12/wk52/p03_wish_list_ink.png        IG-wishlist    Wed Dec 23  (FB-wishlist Thu Dec 24)      humor
2026-12/wk52/p04_holiday_table_coral.png  IG-table       Thu Dec 24  (FB-table Wed Dec 23)         for people helping someone look
2026-12/wk52/p05_merry_christmas_cobalt.png IG-christmas Fri Dec 25                                seasonal
2026-12/wk52/p06_returns_desk_lime.png    IG-returns     Sat Dec 26  (FB-returns Sun Dec 27)       humor
2026-12/wk52/p07_three_jobs_pink.png      IG-threejobs   Sun Dec 27  (FB-threejobs Sat Dec 26)

No card says "Link in bio", so Facebook reuses each file as it is (no _fb variants).
Grounds, Instagram Mon to Sun: pink (IG-thanks-r2), mint, ink, coral, cobalt, lime, pink: any 4 in a row differ, no cream.
One lime element per card (the highlight, or the lime ground itself); lime is never text.

Run from the repo root: python3 2026-12/wk52/build_holiday.py [names to render, default all]
"""
import json, os, subprocess, sys, tempfile
WK = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(WK))
sys.path.insert(0, os.path.join(ROOT, "design-system"))
from grounds import *  # noqa  (also brings in ds: page, tick, spark, foot and the colors)

TMP = tempfile.mkdtemp(prefix="wk52_holiday_")
jobs = []


def out(name, html):
    p = os.path.join(TMP, name + ".html"); open(p, "w").write(html)
    jobs.append({"html": p, "png": os.path.join(WK, name + ".png"), "w": 1080, "h": 1350})


def at(x, y, html, right=False):
    return f'<div style="position:absolute;{"right" if right else "left"}:{x}px;top:{y}px">{html}</div>'


def stk(text, bg, x=72, y=72, size=30):
    return at(x, y, f'<span class="sticker" style="background:{bg};font-size:{size}px">{text}</span>')


def head(html, top, size, width=None):
    w = f"width:{width}px" if width else "right:72px"
    return f'<div class="d c" style="position:absolute;left:72px;{w};top:{top}px;font-size:{size}px">{html}</div>'


def sub(html, top, size=44, width=620, weight=700):
    return (f'<div class="c" style="position:absolute;left:74px;top:{top}px;width:{width}px;font-size:{size}px;'
            f'font-weight:{weight};line-height:1.24">{html}</div>')


def card(html, top, width=640, size=40):
    return (f'<div class="card" style="position:absolute;left:72px;top:{top}px;width:{width}px;padding:32px 38px;'
            f'font-size:{size}px;font-weight:700;line-height:1.28">{html}</div>')


# IG-quietresume · mint. The free resume builder, in the words its slides already use.
g = "mint"
out("p02_quiet_resume_mint", cover_page(
    stk("Quiet week project", WHITE)
    + head('Tailor your resume to <span class="fill">one job.</span>', 200, 118)
    + card('<div style="font-size:30px;font-weight:600;margin-bottom:14px">The free resume builder shows you:</div>'
           '1. What this job wants<br>2. Keywords you can\'t claim yet<br>3. How to make it stronger', 520, 660, 40)
    + at(56, 820, tick("pointing", 270), right=True)
    + spark(900, 120, 60, WHITE) + spark(990, 240, 34, INK)
    + foot_g(g, right="getday60.com/resume-builder"), g))

# IG-wishlist · ink. Humor: the joke is on ghosting, never on the person looking.
g = "ink"
out("p03_wish_list_ink", cover_page(
    stk("Holiday wish list", PINK)
    + head("1. A reply.<br>2. Any reply.<br>3. Even a no.", 190, 116)
    + card('Best way to get one: three lines to the person who decides, ending with '
           '<span class="fill" style="white-space:nowrap">an easy question.</span>', 760, 640, 40)
    + at(60, 700, tick("celebrating", 280), right=True)
    + spark(900, 110, 60, PINK) + spark(990, 230, 34, CREAM)
    + foot_g(g), g))

# IG-table · coral. For the friend or parent of someone who's looking.
g = "coral"
out("p04_holiday_table_coral", cover_page(
    stk("For the holiday table", WHITE)
    + head("Skip “Any luck yet?”", 200, 122)
    + sub("Someone at the table is looking for work. Try this instead:", 520, 44, 640)
    + card('“Which job would you most like?” Then think of '
           '<span class="fill" style="white-space:nowrap">one person</span> you could introduce them to.', 740, 640, 40)
    + at(60, 690, tick("waving", 280), right=True)
    + spark(900, 110, 60, WHITE) + spark(990, 230, 34, INK)
    + foot_g(g), g))

# IG-christmas · cobalt. A one-line seasonal card.
g = "cobalt"
out("p05_merry_christmas_cobalt", cover_page(
    stk("Merry Christmas", WHITE)
    + head('Today’s only task: <span class="fill">rest.</span>', 220, 136)
    + sub("From Tick and Phil at Day60.", 640, 46, 600)
    + at(70, 700, tick("celebrating", 320), right=True)
    + spark(900, 110, 64, WHITE) + spark(990, 240, 36, PINK) + spark(150, 1040, 40, WHITE)
    + foot_g(g), g))

# IG-returns · lime. Humor. The lime ground is the card's one lime element, so no highlight.
g = "lime"
out("p06_returns_desk_lime", cover_page(
    stk("Returns desk", WHITE)
    + head("Returning: 40 applications, unopened.", 200, 112)
    + card('<div style="font-size:30px;font-weight:600;margin-bottom:12px">Exchanging for:</div>'
           'One short note to the person who decides. Three lines, one easy question.', 720, 640, 40)
    + at(60, 660, tick("pointing", 280), right=True)
    + spark(900, 110, 60, WHITE) + spark(990, 230, 34, INK)
    + foot_g(g), g))

# IG-threejobs · pink. Plan for January.
g = "pink"
out("p07_three_jobs_pink", cover_page(
    stk("Plan for January", WHITE)
    + head('<span class="fill">Three jobs.</span><br>Not thirty.', 200, 132)
    + card("1. Pick three jobs you’d say yes to.<br>2. Find each hiring manager’s name.<br>"
           "3. Write one short note for Monday.", 600, 760, 38)
    + at(48, 930, tick("running", 210), right=True)
    + spark(900, 110, 60, WHITE) + spark(990, 230, 34, INK)
    + foot_g(g), g))

if __name__ == "__main__":
    only = sys.argv[1:]
    if only:
        jobs = [j for j in jobs if os.path.basename(j["png"])[:-4] in only]
    jf = os.path.join(TMP, "jobs.json"); json.dump(jobs, open(jf, "w"))
    subprocess.run(["node", os.path.join(ROOT, "templates", "render_many.js"), jf], check=True)
