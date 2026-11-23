"""The first humor cards (Philip, Nov 22, via HQ: "humorous, yet professional and politically correct").
Drafts for HQ's approval, Social, Nov 23. Playbook §4 Humor: the joke is on the process, never the person
looking for work, and every card ends on one useful point.

2026-11/wk48/p06_pass_the_stuffing_pink.png  1080x1350  IG-thanksgiving, Thu Nov 26 (a one-line seasonal card)
2026-11/wk49/p02_breaking_lime.png           1080x1350  IG-breaking, Mon Nov 30, then FB-breaking, Tue Dec 1
                                                        ("breaking news" with Tick; no "Link in bio", so Facebook
                                                        can reuse it)

Grounds: the Instagram grid runs mint (Wed), the card (Thu), ink (Fri), coral (Sat), cobalt (Sun), then Mon.
Pink on Thu and lime on Mon keep any 4 in a row different. On pink, the lime highlight is the one lime element.

Run from repo root: python3 2026-11/wk49/build_humor.py [names to render, default all]
"""
import json, os, subprocess, sys, tempfile
WK = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(WK))
WK48 = os.path.join(ROOT, "2026-11", "wk48")
sys.path.insert(0, os.path.join(ROOT, "design-system"))
from grounds import *  # noqa  (also brings in ds: page, tick, spark, foot and the colors)

TMP = tempfile.mkdtemp(prefix="wk49_humor_")
jobs = []


def out(folder, name, html):
    p = os.path.join(TMP, name + ".html"); open(p, "w").write(html)
    jobs.append({"html": p, "png": os.path.join(folder, name + ".png"), "w": 1080, "h": 1350})


def at(x, y, html, right=False):
    return f'<div style="position:absolute;{"right" if right else "left"}:{x}px;top:{y}px">{html}</div>'


def stk(text, bg, x, y, size=28):
    return at(x, y, f'<span class="sticker" style="background:{bg};font-size:{size}px">{text}</span>')


# IG-thanksgiving · pink. "Pass the stuffing?" is the easiest question anyone answers this week.
g = "pink"
out(WK48, "p06_pass_the_stuffing_pink", cover_page(
    stk("Happy Thanksgiving", WHITE, 72, 72)
    + f'<div class="d" style="position:absolute;left:72px;right:72px;top:200px;font-size:140px">'
      f'“Pass the stuffing?”</div>'
    + f'<div style="position:absolute;left:74px;top:540px;width:600px;font-size:46px;font-weight:700;line-height:1.22">'
      f'The easiest question anyone will answer this week.</div>'
    + f'<div class="card" style="position:absolute;left:72px;top:800px;width:600px;padding:34px 38px;'
      f'font-size:40px;font-weight:700;line-height:1.28">End your next note with a question '
      f'<span class="fill" style="color:{INK}">that easy.</span></div>'
    + at(64, 620, tick("celebrating", 300), right=True)
    + spark(900, 110, 64, WHITE) + spark(990, 230, 36, INK)
    + foot_g(g), g))

# IG-breaking / FB-breaking · lime. The whole ground is the lime element; no lime text.
g = "lime"
out(WK, "p02_breaking_lime", cover_page(
    stk("Breaking news", CORAL, 72, 72, 30)
    + f'<div class="d" style="position:absolute;left:72px;right:72px;top:200px;font-size:118px">'
      f'Hiring manager answers cold email.</div>'
    + f'<div class="card" style="position:absolute;left:72px;top:640px;width:620px;padding:34px 38px;'
      f'font-size:40px;font-weight:600;line-height:1.3">It was three lines long and ended with one easy question.</div>'
    + at(60, 700, tick("celebrating", 290), right=True)
    + spark(900, 110, 60, INK) + spark(990, 220, 34, WHITE)
    + foot_g(g), g))

if __name__ == "__main__":
    only = sys.argv[1:]
    if only:
        jobs = [j for j in jobs if os.path.basename(j["png"])[:-4] in only]
    jf = os.path.join(TMP, "jobs.json"); json.dump(jobs, open(jf, "w"))
    subprocess.run(["node", os.path.join(ROOT, "templates", "render_many.js"), jf], check=True)
