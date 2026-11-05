"""p17_ext_linkedin_1-5: the two LinkedIn steps in Day60 for Chrome 1.1.0 (live Nov 5).

Claims are the store listing's LinkedIn lines only (1.1.0; nothing from 1.2.0):
on a LinkedIn job, "Find it with Day60" looks for the same job on the company's
own careers page (no posting there: you paste the description); on a LinkedIn
profile, "Add to a job in Day60" adds that person to one of your jobs as hiring
manager, their boss, internal champion or recruiter. It never reads LinkedIn
pages: only the tab's address and title, only when you press its button. Never
fills in forms, applies or sends. You send every message.
Popups are crops of the store screenshots (media/chrome-extension/, no names).
Also writes p17_ext_linkedin.pdf for the LinkedIn document post.

Run from repo root: python3 2026-11/wk46/build_li.py
"""
import json, os, subprocess, sys
WK = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(WK))
sys.path.insert(0, os.path.join(ROOT, "design-system"))
from ds import *  # noqa

TMP = os.path.join(WK, "_li"); os.makedirs(TMP, exist_ok=True)
SITE = os.path.join(WK, "site")
N = 5
jobs = []


def out(name, body, bg=CREAM):
    p = os.path.join(TMP, name + ".html"); open(p, "w").write(page(body, bg=bg))
    jobs.append({"html": p, "png": os.path.join(WK, name + ".png"), "w": 1080, "h": 1350})


def count(i, dark=False):
    return foot(bottom=56, right=f"{i}/{N}", dark=dark)


def head(n, text, top=200, size=70):
    return (f'<div style="position:absolute;left:72px;top:{top}px;right:72px;display:flex;gap:32px;align-items:center">'
            f'<div class="step d" style="flex:none;width:110px;height:110px;font-size:58px">{n}</div>'
            f'<div class="d" style="font-size:{size}px">{text}</div></div>')


def says(pose, text, top, w=160):
    return (f'<div style="position:absolute;left:72px;right:72px;top:{top}px;display:flex;align-items:flex-end;gap:24px">'
            f'{tick(pose, w, "flex:none")}<div class="bubble left" style="--tail:52px;margin-bottom:{int(w*0.55)}px;font-size:36px">{text}</div></div>')


def popup(fname, top, width=720):
    src = os.path.join(SITE, fname)
    return (f'<div class="card" style="position:absolute;left:{(1080-width)//2}px;top:{top}px;width:{width}px;padding:0;overflow:hidden">'
            f'<div style="padding:12px 22px;border-bottom:5px solid {INK};background:{MUTED};font-size:24px;font-weight:700">'
            f'linkedin.com · Day60 for Chrome</div>'
            f'<img src="file://{src}" style="display:block;width:100%"></div>')


# 1 cover
out("p17_ext_linkedin_1",
    f'<div style="position:absolute;left:72px;top:96px"><span class="sticker" style="background:{PINK}">New in Day60 for Chrome</span></div>'
    + spark(890, 90, 70) + spark(975, 220, 40, MINT)
    + f'<div class="d" style="position:absolute;left:72px;right:72px;top:220px;font-size:116px">Found it on LinkedIn? <span class="fill" style="white-space:nowrap">Take it to Day60.</span></div>'
    + f'<div style="position:absolute;left:74px;top:640px;width:560px;font-size:40px;font-weight:700;line-height:1.25">Two new buttons for LinkedIn. One for a job, one for a person.</div>'
    + f'<div style="position:absolute;left:72px;top:1000px"><span class="btn" style="font-size:38px;padding:18px 34px">Swipe →</span></div>'
    + f'<div style="position:absolute;right:80px;top:790px">{tick("pointing", 300)}</div>'
    + count(1))

# 2 LinkedIn job
out("p17_ext_linkedin_2",
    head("01", "On a LinkedIn job, press “Find it with Day60”.", 150)
    + popup("ext_li_job.png", 320, 560)
    + says("thinking", "It looks for the same job on the company's own careers page. Not posted there? You paste the description.", 955, 100)
    + count(2))

# 3 LinkedIn profile
out("p17_ext_linkedin_3",
    head("02", "On a LinkedIn profile, press “Add to a job in Day60”.", 150)
    + popup("ext_li_profile.png", 320, 560)
    + says("celebrating", "Pick the job. Pick their role: hiring manager, their boss, champion or recruiter.", 955, 100)
    + count(3))

# 4 what it never does
NEVER = ["Read LinkedIn pages", "Fill in forms or apply", "Send messages for you"]
rows = "".join(f'<div style="display:flex;gap:22px;align-items:center;font-size:44px;font-weight:700;margin-top:30px">{check(60, False)}{t}</div>' for t in NEVER)
out("p17_ext_linkedin_4",
    f'<div style="position:absolute;left:72px;top:96px"><span class="sticker" style="background:{PINK}">Plain answers</span></div>'
    + spark(900, 100, 60)
    + f'<div class="d" style="position:absolute;left:72px;right:72px;top:210px;font-size:104px">What it never does.</div>'
    + f'<div class="card" style="position:absolute;left:72px;right:72px;top:450px;padding:16px 44px 46px">{rows}'
      f'<div style="border-top:4px solid {INK};margin-top:40px;padding-top:30px;display:flex;gap:22px;align-items:flex-start;font-size:38px;font-weight:700;line-height:1.25">'
      f'{check(60)}<span>On LinkedIn it uses only the tab\'s address and title, and only when you press its button.</span></div></div>'
    + f'<div class="d" style="position:absolute;left:72px;top:1060px;font-size:52px"><span class="fill">You send every message.</span></div>'
    + count(4))

# 5 CTA (dark)
out("p17_ext_linkedin_5",
    spark(900, 110, 60, LIME) + spark(960, 980, 50, PINK)
    + f'<div class="d" style="position:absolute;left:72px;right:72px;top:150px;font-size:100px;color:{CREAM}">Saw it on LinkedIn.<br><span style="color:{LIME}">Work it in Day60.</span></div>'
    + f'<div class="card" style="position:absolute;left:72px;top:720px;padding:32px 40px;background:{CREAM};box-shadow:12px 12px 0 {LIME}">'
      f'<div class="d" style="font-size:56px">Free in the Chrome Web Store.</div>'
      f'<div style="font-size:34px;font-weight:700;margin-top:10px">getday60.com/chrome-extension</div></div>'
    + f'<div class="d" style="position:absolute;left:74px;top:1020px;font-size:40px;color:{CREAM}">Search “Day60” in the store →</div>'
    + f'<div style="position:absolute;right:80px;top:930px">{tick("celebrating", 220)}</div>'
    + count(5, dark=True), bg=D_BG)

if __name__ == "__main__":
    jf = os.path.join(TMP, "jobs.json"); json.dump(jobs, open(jf, "w"))
    subprocess.run(["node", os.path.join(ROOT, "templates", "render_many.js"), jf], check=True)
    from PIL import Image
    ims = [Image.open(os.path.join(WK, f"p17_ext_linkedin_{i}.png")).convert("RGB") for i in range(1, N + 1)]
    ims[0].save(os.path.join(WK, "p17_ext_linkedin.pdf"), save_all=True, append_images=ims[1:], resolution=144)
