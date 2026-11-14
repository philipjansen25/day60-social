"""Week 47 replacement carousel for the Tue Nov 17 slot (Product Hunt moved to Dec 1).

p01_four_people_1-6.png  1080x1350  "Every job has 4 people who decide if you get it."
Used by IG-four (Tue Nov 17) and FB-four (Wed Nov 18). Drafts, not approved.

Run from repo root: python3 2026-11/wk47/build.py
"""
import json, os, subprocess, sys, tempfile
WK = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(WK))
sys.path.insert(0, os.path.join(ROOT, "design-system"))
from ds import *  # noqa
from grounds import INK_KEYLINES  # noqa

TMP = tempfile.mkdtemp(prefix="wk47_")
jobs = []


def out(name, body, bg=CREAM):
    p = os.path.join(TMP, name + ".html"); open(p, "w").write(page(body, bg=bg))
    jobs.append({"html": p, "png": os.path.join(WK, name + ".png"), "w": 1080, "h": 1350})


def sticker(text, bg, x, y, size=28):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px"><span class="sticker" '
            f'style="background:{bg};font-size:{size}px">{text}</span></div>')


def counter(n):
    return f'<div style="position:absolute;right:72px;top:84px;font-size:30px;font-weight:700;color:{MUTED_TEXT}">{n} / 6</div>'


# 1. cover (lime)
out("p01_four_people_1",
    sticker("Save this", WHITE, 72, 72)
    + f'<div class="d" style="position:absolute;left:72px;top:200px;width:936px;font-size:112px">'
      f'Every job has 4 people who decide if you get it.</div>'
    + f'<div style="position:absolute;left:76px;top:760px;width:560px;font-size:44px;font-weight:700;line-height:1.2">'
      f'An application reaches one of them. Maybe.</div>'
    + f'<div style="position:absolute;right:60px;top:690px">{tick("pointing", 330)}</div>'
    + spark(860, 120, 70, WHITE)
    + foot(), bg=LIME)

ROLES = [
    ("01", "The hiring manager", MINT, "Feels the empty seat.",
     "They work with whoever gets the job. Make your note about their team: one thing you noticed, one line of proof, one clear question.", "thinking"),
    ("02", "Their boss", PINK, "Approved the role.",
     "Keep it shorter. Say why their team's goal is the one you want to work on.", "waiting"),
    ("03", "An internal champion", MINT, "Knows what the job really needs.",
     "Someone on the team. Ask one real question about the work. People answer questions they're good at.", "pointing"),
    ("04", "The recruiter", PINK, "Runs the process.",
     "Tell them you applied and why. Make their job easy: the role, one line on fit, when you're free to talk.", "waving"),
]
for k, (num, role, col, head, body, pose) in enumerate(ROLES):
    out(f"p01_four_people_{k + 2}",
        f'<div class="step" style="position:absolute;left:72px;top:72px"><span class="d">{num}</span></div>'
        + counter(k + 2)
        + sticker(role, col, 72, 250, 30)
        + f'<div class="d" style="position:absolute;left:72px;top:360px;width:936px;font-size:104px">{head}</div>'
        + f'<div class="card" style="position:absolute;left:72px;top:{690 if len(head) > 22 else 600}px;width:680px;padding:36px 40px;'
          f'font-size:40px;font-weight:600;line-height:1.3">{body}</div>'
        + f'<div style="position:absolute;right:56px;bottom:150px">{tick(pose, 230)}</div>'
        + foot())

# 6. CTA (dark). v2 (HQ, Nov 13): cream keylines on ink; the old p01_four_people_6.png stays on disk.
out("p01_four_people_6_v2",
    INK_KEYLINES + f'<div class="d" style="position:absolute;left:72px;top:150px;width:936px;font-size:112px;color:{CREAM}">'
    f'Paste a job link.<br><span class="fill" style="color:{INK}">Get your 4 people.</span></div>'
    + f'<div style="position:absolute;left:76px;top:640px;width:620px;font-size:44px;font-weight:600;line-height:1.3;color:{CREAM}">'
      f'A short note to each, in your voice. You send every message.</div>'
    + sticker("Link in bio", LIME, 72, 900, 34)
    + f'<div style="position:absolute;right:60px;top:760px">{tick("celebrating", 300)}</div>'
    + spark(900, 110, 64, LIME)
    + foot(dark=True), bg=INK)

if __name__ == "__main__":
    only = sys.argv[1:]  # optional: output names to render, e.g. p14_ext_steps_6_v2 (default: all)
    if only:
        jobs = [j for j in jobs if os.path.basename(j["png"])[:-4] in only]
    jf = os.path.join(TMP, "jobs.json"); json.dump(jobs, open(jf, "w"))
    subprocess.run(["node", os.path.join(ROOT, "templates", "render_many.js"), jf], check=True)
