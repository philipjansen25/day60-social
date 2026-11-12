"""Week 47 résumé builder carousel (HQ, Nov 11: Philip wants the free résumé builder promoted).

p02_resume_builder_1-6.png  1080x1350  "One résumé. Tailored to one job."
Used by IG-resume (Sun Nov 15) and FB-resume (Fri Nov 20). Drafts, not approved.

Slide 2 is a real crop of getday60.com/resume-builder (site/resume_builder_form.png, shot by
site/cap_resume_builder.js with an invented job link typed in, nothing submitted). Slides 3-5 are
rebuilt from tokens: the results screen needs a real submission, so they show the labels HQ gave
("What this job wants", "Keywords you can't claim yet", "Make it stronger") on an invented résumé
and job (Northpine, Customer Success Manager), labeled "Illustrative example".

Run from repo root: python3 2026-11/wk47/build_resume.py
"""
import base64, io, json, os, subprocess, sys, tempfile
from PIL import Image
WK = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(WK))
sys.path.insert(0, os.path.join(ROOT, "design-system"))
from ds import *  # noqa

TMP = tempfile.mkdtemp(prefix="wk47_rb_")
jobs = []
N = 6
URL = "getday60.com/resume-builder"


def out(name, body, bg=CREAM):
    p = os.path.join(TMP, name + ".html"); open(p, "w").write(page(body, bg=bg))
    jobs.append({"html": p, "png": os.path.join(WK, name + ".png"), "w": 1080, "h": 1350})


def sticker(text, bg, x, y, size=28):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px"><span class="sticker" '
            f'style="background:{bg};font-size:{size}px">{text}</span></div>')


def counter(n):
    return f'<div style="position:absolute;right:72px;top:84px;font-size:30px;font-weight:700;color:{MUTED_TEXT}">{n} / {N}</div>'


def step(num, n, head, top=230):
    return (f'<div class="step" style="position:absolute;left:72px;top:72px"><span class="d">{num}</span></div>'
            + counter(n)
            + f'<div class="d" style="position:absolute;left:72px;top:{top}px;width:936px;font-size:92px">{head}</div>')


def chip(text, bg=MINT, x=None):
    icon = check(34, ok=False) if x else ""
    return (f'<span style="display:inline-flex;align-items:center;gap:12px;margin:0 14px 16px 0;padding:10px 22px;'
            f'background:{bg};border:4px solid {INK};border-radius:999px;font-size:30px;font-weight:700">{icon}{text}</span>')


def lbl(text, size=26):
    return (f'<div style="font-size:{size}px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;'
            f'color:{MUTED_TEXT};margin-bottom:14px">{text}</div>')


EX = "Illustrative example"
FOOT = foot(right=URL)

# 1. cover (lime)
out("p02_resume_builder_1",
    sticker("Save this", WHITE, 72, 72)
    + f'<div class="d" style="position:absolute;left:72px;top:200px;width:936px;font-size:118px">'
      f'One résumé. Tailored to one job.</div>'
    + f'<div style="position:absolute;left:76px;top:690px;width:560px;font-size:44px;font-weight:700;line-height:1.2">'
      f'How the free résumé builder works, on an invented résumé and job.</div>'
    + f'<div style="position:absolute;right:60px;top:660px">{tick("thinking", 320)}</div>'
    + spark(870, 110, 70, WHITE)
    + FOOT, bg=LIME)

# 2. add the job and the résumé: live crop of the form
im = Image.open(os.path.join(WK, "site", "resume_builder_form.png")).convert("RGB")
im = im.crop((8, 8, im.width - 8, 930))  # drop the site card's own border and the next label
buf = io.BytesIO(); im.save(buf, "PNG")
src = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
W2 = 520
out("p02_resume_builder_2",
    step("01", 2, "Add the job and your résumé.")
    + f'<div class="card" style="position:absolute;left:72px;top:470px;width:{W2}px;padding:0;overflow:hidden">'
      f'<img src="{src}" style="display:block;width:{W2}px"></div>'
    + sticker(EX, PINK, 636, 470, 24)
    + f'<div class="bubble down" style="position:absolute;left:636px;top:580px;width:372px;font-size:34px;--tail:250px">'
      f'A link to the posting (not LinkedIn) or the posting itself. Then a PDF, a Word file or the text.</div>'
    + f'<div style="position:absolute;right:56px;top:940px">{tick("pointing", 210)}</div>'
    + FOOT)

# 3. what this job wants
problems = ["New customers take too long to get started.",
            "Renewals slip without warning.",
            "Customer feedback reaches the product team late."]
out("p02_resume_builder_3",
    step("02", 3, "See what the job wants.")
    + sticker(EX, PINK, 72, 370, 24)
    + f'<div class="card" style="position:absolute;left:72px;top:460px;width:936px;padding:36px 44px">'
      f'<div class="d" style="font-size:52px;margin-bottom:6px">What this job wants</div>'
      f'<div style="font-size:28px;color:{MUTED_TEXT};margin-bottom:30px">Customer Success Manager at Northpine (invented)</div>'
      + lbl("Keywords")
      + "".join(chip(k) for k in ["Customer onboarding", "Renewals", "Account health", "Product feedback"])
      + f'<div style="height:18px"></div>' + lbl("3 problems this role solves")
      + "".join(f'<div style="display:flex;gap:20px;align-items:flex-start;font-size:34px;font-weight:600;line-height:1.25;margin-bottom:16px">'
                f'<span class="d" style="flex:none;width:52px;height:52px;border:4px solid {INK};border-radius:14px;background:{LIME};'
                f'display:flex;align-items:center;justify-content:center;font-size:32px">{i}</span><span>{t}</span></div>'
                for i, t in enumerate(problems, 1))
    + '</div>'
    + FOOT)


# 4. tailored, only what's true
def pair(top, before, after):
    return (f'<div class="card" style="position:absolute;left:72px;top:{top}px;width:936px;padding:0;overflow:hidden">'
            f'<div class="muted" style="padding:20px 34px;border-bottom:4px solid {INK}">{lbl("From the résumé", 20)}'
            f'<div style="font-size:31px;font-weight:500;line-height:1.25">{before}</div></div>'
            f'<div style="padding:20px 34px">{lbl("For this job", 20)}'
            f'<div style="font-size:33px;font-weight:700;line-height:1.25"><span class="fill">{after}</span></div></div></div>')


out("p02_resume_builder_4",
    step("03", 4, "Tailored, with only what's true.")
    + sticker(EX, PINK, 72, 440, 24)
    + pair(510, "Trained staff at new accounts on the ordering system.",
           "Onboarded new accounts and trained their teams.")
    + pair(780, "Ran 60 small-business accounts, renewals included.",
           "Managed renewals for 60 small-business accounts.")
    + f'<div style="position:absolute;left:72px;top:1068px;width:740px;font-size:36px;font-weight:700;line-height:1.25">'
      f'No new skill, number or title. Only what the résumé and your notes show.</div>'
    + f'<div style="position:absolute;right:64px;top:1052px">{tick("pointing", 136)}</div>'
    + FOOT)

# 5. the gap, and a question
out("p02_resume_builder_5",
    step("04", 5, "Know the gap before they do.")
    + sticker(EX, PINK, 72, 440, 24)
    + f'<div class="card" style="position:absolute;left:72px;top:530px;width:936px;padding:36px 44px">'
      f'<div class="d" style="font-size:46px;margin-bottom:24px">Keywords you can\'t claim yet</div>'
      + chip("Account health scores", WHITE, x=True) + chip("Quarterly business reviews", WHITE, x=True)
      + f'<div style="font-size:32px;font-weight:500;line-height:1.3;margin-top:8px">In the posting, not in the résumé, so they stay off it.</div></div>'
    + f'<div class="card" style="position:absolute;left:72px;top:900px;width:700px;padding:32px 40px;background:{MINT}">'
      f'<div class="d" style="font-size:42px;margin-bottom:14px">Make it stronger</div>'
      f'<div style="font-size:34px;font-weight:700;line-height:1.25">Have you tracked which accounts might not renew?</div>'
      f'<div style="font-size:24px;font-weight:600;margin-top:12px">Example question</div></div>'
    + f'<div style="position:absolute;right:52px;top:930px">{tick("thinking", 200)}</div>'
    + foot(bottom=40, right=URL))

# 6. CTA (dark)
out("p02_resume_builder_6",
    f'<div class="d" style="position:absolute;left:72px;top:150px;width:936px;font-size:112px;color:{CREAM}">'
    f'Read every line.<br><span class="fill" style="color:{INK}">Get a Word file.</span></div>'
    + f'<div style="position:absolute;left:76px;top:600px;width:620px;font-size:44px;font-weight:600;line-height:1.3;color:{CREAM}">'
      f'Free. No account. Nothing you add is kept.</div>'
    + sticker(URL, LIME, 72, 860, 30)
    + sticker("Link in bio", WHITE, 72, 960, 30)
    + f'<div style="position:absolute;right:60px;top:700px">{tick("celebrating", 300)}</div>'
    + spark(900, 110, 64, LIME)
    + foot(dark=True), bg=INK)

if __name__ == "__main__":
    jf = os.path.join(TMP, "jobs.json"); json.dump(jobs, open(jf, "w"))
    subprocess.run(["node", os.path.join(ROOT, "templates", "render_many.js"), jf], check=True)
