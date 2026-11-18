"""Week 49 carousel: "Email the person. But which one?" (HQ brief, Nov 18).

A job-search post going around says: stop applying, email the person who posted the job, keep it short and a
little messy. It never says which person, or what to say. This carousel answers that with the 4 people.
No names, no numbers beyond the 4 people, and nothing from the original post but the idea.

p01_which_person_1_ink.png     1080x1350  cover on ink (grid: cobalt, mint, coral come before it)
p01_which_person_2-5.png       1080x1350  one person each, cream
p01_which_person_6.png         1080x1350  ink, "Link in bio"   (IG-email)
p01_which_person_6_fb.png      1080x1350  ink, "getday60.com"  (FB-email: "Link in bio" doesn't work there)

Used by IG-email (Mon Nov 30) and FB-email (Tue Dec 1). Drafts, not approved.
One lime element per image: the cover's highlight, the step block on 2 to 5, the sticker on 6.

Run from repo root: python3 2026-11/wk49/build.py [names to render, default all]
"""
import json, os, subprocess, sys, tempfile
WK = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(WK))
sys.path.insert(0, os.path.join(ROOT, "design-system"))
from grounds import *  # noqa  (also brings in ds: page, tick, spark, foot and the colors)

TMP = tempfile.mkdtemp(prefix="wk49_")
jobs = []


def out(name, html):
    p = os.path.join(TMP, name + ".html"); open(p, "w").write(html)
    jobs.append({"html": p, "png": os.path.join(WK, name + ".png"), "w": 1080, "h": 1350})


def at(x, y, html, right=False):
    return f'<div style="position:absolute;{"right" if right else "left"}:{x}px;top:{y}px">{html}</div>'


def stk(text, bg, x, y, size=28):
    return at(x, y, f'<span class="sticker" style="background:{bg};font-size:{size}px">{text}</span>')


def counter(n, color=MUTED_TEXT):
    return f'<div style="position:absolute;right:72px;top:84px;font-size:30px;font-weight:700;color:{color}">{n} / 6</div>'


# 1. Cover · ink (the method). The lime highlight is the one lime element.
g = "ink"
out("p01_which_person_1_ink", cover_page(
    dial(880, 1010, 400, g)
    + stk("The part they left out", WHITE, 72, 72)
    + f'<div class="d" style="position:absolute;left:72px;right:72px;top:200px;font-size:124px">'
      f'Email the person.<br><span class="fill" style="color:{INK};white-space:nowrap">But which one?</span></div>'
    + f'<div style="position:absolute;left:74px;top:560px;width:560px;font-size:44px;font-weight:700;line-height:1.2">'
      f'Every job has 4 people who decide if you get it. Here\'s what to say to each.</div>'
    + at(60, 690, tick("thinking", 330), right=True)
    + spark(860, 120, 70, WHITE) + spark(960, 250, 40, MINT)
    + foot_g(g), g))

# 2 to 5. One person each. The step block is the slide's lime element; stickers are mint or pink.
PEOPLE = [
    ("01", "The hiring manager", MINT, "Name their problem.",
     "One problem their team has (the posting usually tells you). One line of proof you can help. One easy question.",
     "thinking"),
    ("02", "Their boss", PINK, "Lead with their goal.",
     "They approved the role. Say why their team's goal is the one you want to work on. Keep it shorter.",
     "waiting"),
    ("03", "Someone on the team", MINT, "Ask one real question.",
     "They know what the job is really like. Ask about the work, not for a favor. Save the referral for later.",
     "pointing"),
    ("04", "The recruiter", PINK, "Make the fit easy.",
     "Say you applied and why: the role, one line on fit, and when you're free to talk.",
     "waving"),
]
for k, (num, role, col, headline, body, pose) in enumerate(PEOPLE):
    out(f"p01_which_person_{k + 2}", page(
        f'<div class="step" style="position:absolute;left:72px;top:72px"><span class="d">{num}</span></div>'
        + counter(k + 2)
        + stk(role, col, 72, 250, 30)
        + f'<div class="d" style="position:absolute;left:72px;top:360px;width:936px;font-size:104px">{headline}</div>'
        + f'<div class="card" style="position:absolute;left:72px;top:600px;width:680px;'
          f'padding:36px 40px;font-size:40px;font-weight:600;line-height:1.3">{body}</div>'
        + at(56, 900, tick(pose, 230), right=True)
        + foot()))


# 6. Last slide · ink, cream keylines. The sticker is the one lime element.
def last(name, label):
    out(name, page(
        INK_KEYLINES + counter(6, D_MUTED_TEXT)
        + f'<div class="d" style="position:absolute;left:72px;top:170px;width:936px;font-size:112px;color:{CREAM}">'
          f'Short. Plain.<br>Sounds like you.</div>'
        + f'<div style="position:absolute;left:76px;top:470px;width:640px;font-size:42px;font-weight:600;line-height:1.3;color:{CREAM}">'
          f'Day60 finds all 4 for one job and drafts a first note to each. You make it yours and send it.</div>'
        + f'<div style="position:absolute;left:76px;top:760px;width:600px;font-size:34px;font-weight:600;line-height:1.3;color:{D_MUTED_TEXT}">'
          f'The skills still count. This gets the right people to see them.</div>'
        + stk(label, LIME, 72, 940, 34)
        + at(60, 760, tick("celebrating", 300), right=True)
        + spark(900, 110, 64, PINK) + spark(990, 220, 36, MINT)
        + foot(dark=True), bg=INK))


last("p01_which_person_6", "Link in bio")
last("p01_which_person_6_fb", "getday60.com")

if __name__ == "__main__":
    only = sys.argv[1:]
    if only:
        jobs = [j for j in jobs if os.path.basename(j["png"])[:-4] in only]
    jf = os.path.join(TMP, "jobs.json"); json.dump(jobs, open(jf, "w"))
    subprocess.run(["node", os.path.join(ROOT, "templates", "render_many.js"), jf], check=True)
