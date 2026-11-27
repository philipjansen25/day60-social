"""Week 53 cards (Mon Dec 28, 2026 to Sun Jan 3, 2027). Drafts for HQ, Social, Nov 27.

Seven 1080x1350 Instagram cards; Facebook reuses the same files (no "Link in bio" on any card, so no _fb variants).
Grounds in posting order: cobalt (Mon), mint (Tue), coral (Wed), ink (Thu), pink (Fri), lime (Sat), mint (Sun):
any 4 in a row differ. One lime element per card: the highlight, or the whole ground on lime.

Run from repo root: python3 2026-12/wk53/build_w53.py [names to render, default all]
"""
import json, os, subprocess, sys, tempfile
WK = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(WK))
sys.path.insert(0, os.path.join(ROOT, "design-system"))
from grounds import *  # noqa

TMP = tempfile.mkdtemp(prefix="wk53_")
jobs = []


def out(name, html):
    p = os.path.join(TMP, name + ".html"); open(p, "w").write(html)
    jobs.append({"html": p, "png": os.path.join(WK, name + ".png"), "w": 1080, "h": 1350})


def at(x, y, html, right=False):
    return f'<div style="position:absolute;{"right" if right else "left"}:{x}px;top:{y}px">{html}</div>'


def stk(text, bg, x=72, y=72, size=30):
    return at(x, y, f'<span class="sticker" style="background:{bg};font-size:{size}px">{text}</span>')


def card(name, g, sticker, sticker_bg, head, head_size, sub, sub_top, box, box_top, pose, tick_top, sparks):
    color = GROUNDS[g]["text"]
    out(name, cover_page(
        stk(sticker, sticker_bg)
        + f'<div class="d" style="position:absolute;left:72px;right:72px;top:200px;font-size:{head_size}px;color:{color}">{head}</div>'
        + f'<div style="position:absolute;left:74px;top:{sub_top}px;width:600px;font-size:44px;font-weight:700;line-height:1.24;color:{color}">{sub}</div>'
        + f'<div class="card" style="position:absolute;left:72px;top:{box_top}px;width:600px;padding:32px 38px;'
          f'font-size:40px;font-weight:700;line-height:1.28">{box}</div>'
        + at(56, tick_top, tick(pose, 290), right=True)
        + sparks
        + foot_g(g), g))


def F(t):
    return f'<span class="fill" style="color:{INK}">{t}</span>'


# Mon Dec 28 · IG-ooo · cobalt · humor
card("p01_out_of_office_cobalt", "cobalt", "Out of office", WHITE,
     "Back on Jan 4.", 128, "(Probably the 6th.)", 420,
     f"Note the date. {F('Follow up the day after.')}", 700, "running", 560,
     spark(900, 110, 60, WHITE) + spark(990, 220, 34, PINK))
# Tue Dec 29 · IG-keywords · mint · resume tool
card("p02_keywords_mint", "mint", "Resume tip", WHITE,
     "Not every keyword belongs on your resume.", 104, "If the posting asks for it and you haven't done it, leave it off.", 650,
     f"Tailor with {F('what&rsquo;s true.')}", 930, "pointing", 760,
     spark(900, 110, 60, WHITE) + spark(990, 220, 34, INK))
# Wed Dec 30 · IG-yearlist · coral
card("p03_year_list_coral", "coral", "Before the year ends", WHITE,
     "Write down 3 things you did this year.", 108, "Each one: the problem, what you did, what changed.", 640,
     f"That's your next {F('resume bullet.')}", 900, "celebrating", 700,
     spark(900, 110, 60, WHITE) + spark(990, 220, 34, INK))
# Thu Dec 31 · IG-lastcall · ink · humor
card("p04_last_call_ink", "ink", "Last call", PINK,
     "The application portal is closed for the night.", 100, "So are you. Happy New Year.", 650,
     f"Back to {F('one job')} on Monday.", 900, "celebrating", 640,
     spark(900, 110, 60, PINK) + spark(990, 220, 34, MINT))
# Fri Jan 1 · IG-newyear · pink
card("p05_new_year_pink", "pink", "Happy New Year", WHITE,
     "Rest today.", 150, "The postings will still be there on Monday.", 470,
     f"So will {F('the people who decide.')}", 760, "waving", 640,
     spark(900, 110, 60, WHITE) + spark(990, 220, 34, INK))
# Sat Jan 2 · IG-five · lime (the ground is the one lime element; no highlight)
card("p06_one_job_lime", "lime", "New year", WHITE,
     "One job at a time.", 130, "Start with a short list: 5 jobs you'd actually take.", 500,
     "Then one short note to the person who decides.", 800, "pointing", 650,
     spark(900, 110, 60, WHITE) + spark(990, 220, 34, PINK))
# Sun Jan 3 · IG-readline · mint · resume tool
card("p07_read_every_line_mint", "mint", "Resume tip", WHITE,
     "Read every line.", 140, "A tailored resume is still your resume.", 470,
     f"If a line isn't true, {F('cut it.')}", 760, "pointing", 640,
     spark(900, 110, 60, WHITE) + spark(990, 220, 34, PINK))

if __name__ == "__main__":
    only = sys.argv[1:]
    if only:
        jobs = [j for j in jobs if os.path.basename(j["png"])[:-4] in only]
    jf = os.path.join(TMP, "jobs.json"); json.dump(jobs, open(jf, "w"))
    subprocess.run(["node", os.path.join(ROOT, "templates", "render_many.js"), jf], check=True)
