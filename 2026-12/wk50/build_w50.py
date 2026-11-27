"""Week 50 Instagram cards (Social, Nov 27; drafts for HQ). Facebook reuses the same files (no "Link in bio" on any).

p01_tailor_pink.png     IG-tailor    Tue Dec 8   resume builder: tailor it, don't fake it
p02_rounds_cobalt.png   IG-rounds    Wed Dec 9   humor: final round (round 7 of 9)
p03_keywords_coral.png  IG-keywords  Fri Dec 11  resume builder: keywords you can't claim yet
p04_first_line_lime.png IG-firstline Sat Dec 12  message craft: your first line is about them
p05_sticky_pink.png     IG-sticky    Sun Dec 13  light humor: Monday's plan fits on a sticky note

Grounds in posting order: ink (IG-four-r2), pink, cobalt, mint (IG5-r2), coral, lime, pink: any 4 in a row differ.
One lime element per image at most; lime is never text. Run from repo root: python3 2026-12/wk50/build_w50.py [names]
"""
import json, os, subprocess, sys, tempfile
WK = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(WK))
sys.path.insert(0, os.path.join(ROOT, "design-system"))
from grounds import *  # noqa

TMP = tempfile.mkdtemp(prefix="wk50_")
jobs = []
RB = "getday60.com/resume-builder"


def out(name, html):
    p = os.path.join(TMP, name + ".html"); open(p, "w").write(html)
    jobs.append({"html": p, "png": os.path.join(WK, name + ".png"), "w": 1080, "h": 1350})


def at(x, y, html, right=False):
    return f'<div style="position:absolute;{"right" if right else "left"}:{x}px;top:{y}px">{html}</div>'


def stk(text, bg, x, y, size=30):
    return at(x, y, f'<span class="sticker" style="background:{bg};font-size:{size}px">{text}</span>')


def head(text, top, size):
    return f'<div class="d" style="position:absolute;left:72px;right:72px;top:{top}px;font-size:{size}px">{text}</div>'


def sub(text, top, size=42, width=600):
    return (f'<div style="position:absolute;left:74px;top:{top}px;width:{width}px;font-size:{size}px;'
            f'font-weight:700;line-height:1.24">{text}</div>')


def card(html, top, width=620, size=40, bg=None, left=72):
    b = f"background:{bg};" if bg else ""
    return (f'<div class="card" style="position:absolute;left:{left}px;top:{top}px;width:{width}px;padding:32px 38px;{b}'
            f'font-size:{size}px;font-weight:700;line-height:1.28">{html}</div>')


# IG-tailor · pink (resume builder). The lime element: the highlight in the card.
g = "pink"
out("p01_tailor_pink", cover_page(
    stk("Free resume builder", WHITE, 72, 72)
    + head("Tailor it.<br>Don't fake it.", 190, 124)
    + sub("Skills the job wants that you can't claim yet stay off the page.", 560)
    + card(f'Read every line.<br><span class="fill" style="color:{INK}">Add only what\'s true.</span>', 880, 600, 44)
    + at(60, 600, tick("pointing", 280), right=True)
    + spark(900, 110, 60, WHITE) + spark(990, 220, 34, INK)
    + foot_g(g, right=RB), g))

# IG-rounds · cobalt, humor. The lime element: the sticker (ink text).
g = "cobalt"
out("p02_rounds_cobalt", cover_page(
    stk("Interview update", LIME, 72, 72)
    + head("Final round.<br>(Round 7 of 9.)", 190, 128)
    + card("Ask in the first call: how many rounds, and who makes the final call?", 640, 640, 40, WHITE)
    + at(56, 690, tick("celebrating", 270), right=True)
    + spark(900, 110, 60, WHITE) + spark(990, 220, 34, PINK)
    + foot_g(g), g))

# IG-keywords · coral (resume builder). Ink text only. The lime element: the highlight.
g = "coral"
out("p03_keywords_coral", cover_page(
    stk("Resume tip", WHITE, 72, 72)
    + head("Some keywords belong off your resume.", 190, 116)
    + sub("The free resume builder lists the ones you can't claim yet.", 580)
    + card(f'Learn it first.<br><span class="fill" style="color:{INK}">Then add it.</span>', 880, 560, 44)
    + at(56, 640, tick("pointing", 270), right=True)
    + spark(900, 110, 60, WHITE) + spark(990, 220, 34, INK)
    + foot_g(g, right=RB), g))

# IG-firstline · lime. The whole ground is the lime element; no lime fills.
g = "lime"
out("p04_first_line_lime", cover_page(
    stk("Message tip", WHITE, 72, 72)
    + head("Your first line is about them.", 190, 124)
    + sub("Not your life story. One thing their team is working on.", 560)
    + card('<div style="font-size:24px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;margin-bottom:12px">'
           'Illustrative example</div>"Saw your team is opening a second support office this spring."', 800, 640, 38, WHITE)
    + at(56, 560, tick("waving", 250), right=True)
    + spark(900, 110, 60, WHITE) + spark(990, 220, 34, PINK)
    + foot_g(g), g))

# IG-sticky · pink, light humor. A sticky note (pale yellow card, slight tilt). No lime used.
g = "pink"
note = ('<div class="card" style="position:absolute;left:96px;top:560px;width:560px;padding:40px 44px;background:#FFF6B8;'
        'transform:rotate(-3deg);font-size:44px;font-weight:700;line-height:1.5">'
        '1. Pick one job.<br>2. Find the hiring manager.<br>3. Send three lines.</div>')
out("p05_sticky_pink", cover_page(
    stk("Monday plan", WHITE, 72, 72)
    + head("The whole plan fits on a sticky note.", 190, 112)
    + note
    + sub("Bad handwriting still counts.", 1010, 40)
    + at(56, 620, tick("running", 260), right=True)
    + spark(900, 110, 60, WHITE) + spark(990, 220, 34, INK)
    + foot_g(g), g))

if __name__ == "__main__":
    only = sys.argv[1:]
    if only:
        jobs = [j for j in jobs if os.path.basename(j["png"])[:-4] in only]
    jf = os.path.join(TMP, "jobs.json"); json.dump(jobs, open(jf, "w"))
    subprocess.run(["node", os.path.join(ROOT, "templates", "render_many.js"), jf], check=True)
