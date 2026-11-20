"""Week 49 carousel: guide of the week 1, "How to find the hiring manager for a job" (HQ, Nov 19).

Every word comes from the guide (getday60.com/guides/how-to-find-the-hiring-manager, read Nov 19) or the playbook.
No numbers, no names, no invented example.

p02_find_hm_1_lime.png   1080x1350  cover on lime, "Save this" (grid: coral, ink come before it)
p02_find_hm_2-5.png      1080x1350  one step each, cream
p02_find_hm_6.png        1080x1350  cream, "Not sure who leads the team?"
p02_find_hm_7.png        1080x1350  ink, "Link in bio"   (IG-findhm)
p02_find_hm_7_fb.png     1080x1350  ink, "getday60.com"  (FB-findhm: "Link in bio" doesn't work there)

Used by IG-findhm (Wed Dec 2) and FB-findhm (Thu Dec 3). Drafts, not approved.
One lime element per image: the ground on 1, the step block on 2 to 5, the highlight on 6, the sticker on 7.

Run from repo root: python3 2026-11/wk49/build_guide1.py [names to render, default all]
"""
import json, os, subprocess, sys, tempfile
WK = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(WK))
sys.path.insert(0, os.path.join(ROOT, "design-system"))
from grounds import *  # noqa  (also brings in ds: page, tick, spark, check, foot and the colors)

TMP = tempfile.mkdtemp(prefix="wk49g_")
jobs = []
N = 7


def out(name, html):
    p = os.path.join(TMP, name + ".html"); open(p, "w").write(html)
    jobs.append({"html": p, "png": os.path.join(WK, name + ".png"), "w": 1080, "h": 1350})


def at(x, y, html, right=False):
    return f'<div style="position:absolute;{"right" if right else "left"}:{x}px;top:{y}px">{html}</div>'


def stk(text, bg, x, y, size=28):
    return at(x, y, f'<span class="sticker" style="background:{bg};font-size:{size}px">{text}</span>')


def counter(n, color=MUTED_TEXT):
    return f'<div style="position:absolute;right:72px;top:84px;font-size:30px;font-weight:700;color:{color}">{n} / {N}</div>'


def rows(items, ok=True):
    return "".join(f'<div style="display:flex;align-items:center;gap:22px;margin-top:{0 if i == 0 else 22}px">'
                   f'{check(46, ok)}<span>{t}</span></div>' for i, t in enumerate(items))


# 1. Cover · lime ("save this"). The ground is the one lime element; the sticker and the highlight are white.
g = "lime"
out("p02_find_hm_1_lime", cover_page(
    dial(880, 1010, 400, g)
    + stk("Save this", WHITE, 72, 72)
    + counter(1, INK)
    + f'<div class="d" style="position:absolute;left:72px;right:72px;top:200px;font-size:118px">'
      f'How to find the<br><span class="fill" style="white-space:nowrap">hiring manager</span><br>for a job</div>'
    + f'<div style="position:absolute;left:74px;top:640px;width:560px;font-size:42px;font-weight:700;line-height:1.22">'
      f'From the posting, the company’s own pages and a LinkedIn search you run yourself.</div>'
    + at(60, 720, tick("thinking", 300), right=True)
    + spark(860, 130, 64, WHITE) + spark(960, 250, 36, PINK)
    + foot_g(g), g))

# 2 to 5. One step each. The step block is the slide's lime element; stickers are mint or pink.
STEPS = [
    ("01", "The job posting", MINT, "Read it twice.",
     'Once for the job and once for the people. Look for:'
     + f'<div style="margin-top:22px;font-weight:700">{rows(["The title and team", "A “reports to” line", "Any name you see", "The level of the role"])}</div>',
     "thinking"),
    ("02", "The company’s own pages", PINK, "Find the team’s leader.",
     "Team pages, the leadership page, announcements and the blog. A leader who announced a launch or a new team is a strong lead.",
     "pointing"),
    ("03", "Every step by hand", MINT, "Search LinkedIn yourself.",
     "Open the company’s page, then People. Search a short title keyword, then try manager, director, head of and VP.",
     "running"),
    ("04", "Before you write", PINK, "Confirm three things.",
     f'<div style="font-weight:700">{rows(["They still work there.", "Their title fits the team in the posting.", "Their location makes sense for the role."])}</div>',
     "waving"),
]
for k, (num, label, col, headline, body, pose) in enumerate(STEPS):
    out(f"p02_find_hm_{k + 2}", page(
        f'<div class="step" style="position:absolute;left:72px;top:72px"><span class="d">{num}</span></div>'
        + counter(k + 2)
        + stk(label, col, 72, 250, 30)
        + f'<div class="d" style="position:absolute;left:72px;top:360px;width:936px;font-size:100px">{headline}</div>'
        + f'<div class="card" style="position:absolute;left:72px;top:{620 if "LinkedIn" in headline else 520}px;width:700px;'
          f'padding:36px 40px;font-size:38px;font-weight:600;line-height:1.3">{body}</div>'
        + at(56, 940, tick(pose, 210), right=True)
        + foot()))

# 6. The tip. The highlight is the one lime element.
out("p02_find_hm_6", page(
    counter(6)
    + stk("Before you write", PINK, 72, 72, 30)
    + f'<div class="d" style="position:absolute;left:72px;top:200px;width:936px;font-size:104px">Not sure who leads the team?</div>'
    + f'<div class="card" style="position:absolute;left:72px;top:520px;width:720px;padding:36px 40px;font-size:40px;font-weight:600;line-height:1.3">'
      f'Write to the recruiter or someone on the team first, and ask who the right person is.</div>'
    + f'<div class="d" style="position:absolute;left:72px;top:820px;width:640px;font-size:56px;line-height:1.12">'
      f'<span class="fill">A short question</span> costs less than a message to the wrong person.</div>'
    + at(56, 900, tick("thinking", 220), right=True)
    + foot()))


# 7. Last slide · ink, cream keylines. The sticker is the one lime element.
def last(name, label):
    out(name, page(
        INK_KEYLINES + counter(7, D_MUTED_TEXT)
        + f'<div class="d" style="position:absolute;left:72px;top:170px;width:936px;font-size:108px;color:{CREAM}">'
          f'Then write one short message.</div>'
        + f'<div style="position:absolute;left:76px;top:440px;width:640px;font-size:42px;font-weight:600;line-height:1.3;color:{CREAM}">'
          f'The full guide has every step and an example, start to finish: getday60.com/guides</div>'
        + f'<div style="position:absolute;left:76px;top:700px;width:600px;font-size:34px;font-weight:600;line-height:1.3;color:{D_MUTED_TEXT}">'
          f'Day60 helps you identify the four people closest to the hire. Paste a job link. Get your 4 people.</div>'
        + stk(label, LIME, 72, 940, 34)
        + at(60, 760, tick("celebrating", 290), right=True)
        + spark(900, 110, 64, PINK) + spark(990, 220, 36, MINT)
        + foot(dark=True), bg=INK))


last("p02_find_hm_7", "Link in bio")
last("p02_find_hm_7_fb", "getday60.com")

if __name__ == "__main__":
    only = sys.argv[1:]
    if only:
        jobs = [j for j in jobs if os.path.basename(j["png"])[:-4] in only]
    jf = os.path.join(TMP, "jobs.json"); json.dump(jobs, open(jf, "w"))
    subprocess.run(["node", os.path.join(ROOT, "templates", "render_many.js"), jf], check=True)
