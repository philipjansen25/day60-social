"""p14_ext_steps_1-6: Chrome extension "how it works" carousel in Day60's design system.

Claims limited to the live v1.0.0 store listing: on a job on a company's careers
page, click the Day60 icon and press "Find the 4 people with Day60"; Day60 opens
with the job's link filled in. Runs only when you click it. Never reads LinkedIn
pages. Never fills in forms, applies or sends. Invented company, labeled.
p10_chrome_extension.png is untouched (used by the scheduled IGX post).

Run from repo root: python3 2026-11/wk46/build_ext.py
"""
import json, os, subprocess, sys
WK = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(WK))
sys.path.insert(0, os.path.join(ROOT, "design-system"))
from ds import *  # noqa

TMP = os.path.join(WK, "_ext"); os.makedirs(TMP, exist_ok=True)
N = 6
URL = "careers.northpine.example/jobs/account-executive"
EX = (f'<div style="position:absolute;right:72px;top:100px"><span class="sticker" '
      f'style="background:{MUTED};font-size:22px;box-shadow:none">Example · invented company</span></div>')
jobs = []


def out(name, html):
    p = os.path.join(TMP, name + ".html"); open(p, "w").write(html)
    jobs.append({"html": p, "png": os.path.join(WK, name + ".png"), "w": 1080, "h": 1350})


def count(i, dark=False):
    return foot(bottom=56, right=f"{i}/{N}", dark=dark)


def head(n, text, top=200):
    return (f'<div style="position:absolute;left:72px;top:{top}px;right:72px;display:flex;gap:32px;align-items:center">'
            f'<div class="step d" style="flex:none;width:110px;height:110px;font-size:58px">{n}</div>'
            f'<div class="d" style="font-size:76px">{text}</div></div>')


def says(pose, text, top, w=190):
    return (f'<div style="position:absolute;left:72px;right:72px;top:{top}px;display:flex;align-items:flex-end;gap:24px">'
            f'{tick(pose, w, "flex:none")}<div class="bubble left" style="--tail:52px;margin-bottom:{int(w*0.55)}px;font-size:38px">{text}</div></div>')


def browser(inner, url=URL):
    return (f'<div class="card" style="overflow:hidden;padding:0">'
            f'<div style="display:flex;align-items:center;gap:14px;padding:18px 24px;border-bottom:5px solid {INK};background:{MUTED}">'
            f'<span style="width:20px;height:20px;border-radius:50%;border:3px solid {INK};background:{CORAL}"></span>'
            f'<span style="width:20px;height:20px;border-radius:50%;border:3px solid {INK};background:{LIME}"></span>'
            f'<span style="width:20px;height:20px;border-radius:50%;border:3px solid {INK};background:{MINT}"></span>'
            f'<div style="flex:1;margin-left:10px;background:{WHITE};border:3px solid {INK};border-radius:999px;padding:8px 20px;'
            f'font-size:24px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{url}</div>'
            f'<div style="flex:none;width:52px;height:52px;border:3px solid {INK};border-radius:14px;background:{WHITE};'
            f'display:flex;align-items:center;justify-content:center">{tick("waving", 30)}</div></div>{inner}</div>')


JOB_IN = (f'<div class="lbl" style="font-size:26px;color:{MUTED_TEXT}">NORTHPINE · CAREERS</div>'
       f'<div class="d" style="font-size:60px;margin-top:12px">Account Executive</div>'
       f'<div style="font-size:32px;color:{MUTED_TEXT};margin-top:10px">Denver · Full time</div>'
       f'<div style="height:18px;background:{MUTED};border-radius:9px;margin-top:30px;width:92%"></div>'
       f'<div style="height:18px;background:{MUTED};border-radius:9px;margin-top:16px;width:78%"></div>'
       f'<div style="height:18px;background:{MUTED};border-radius:9px;margin-top:16px;width:85%"></div>')
JOB = f'<div style="padding:36px 40px">{JOB_IN}</div>'

# 1 cover
out("p14_ext_steps_1", page(
    f'<div style="position:absolute;left:72px;top:96px"><span class="sticker" style="background:{PINK}">Free Chrome extension</span></div>'
    + spark(890, 90, 70) + spark(975, 220, 40, MINT)
    + f'<div class="d" style="position:absolute;left:72px;right:72px;top:220px;font-size:118px">From a careers page to your sprint. <span class="fill" style="white-space:nowrap">One click.</span></div>'
    + f'<div style="position:absolute;left:74px;top:740px;width:560px;font-size:40px;font-weight:700;line-height:1.25">How the Day60 extension works, in 3 steps.</div>'
    + f'<div style="position:absolute;left:72px;top:1000px"><span class="btn" style="font-size:38px;padding:18px 34px">Swipe →</span></div>'
    + f'<div style="position:absolute;right:80px;top:790px">{tick("pointing", 300)}</div>'
    + count(1)))

# 2 open a job
out("p14_ext_steps_2", page(
    EX + head("01", "Open a job on the company's careers page.", 220)
    + f'<div style="position:absolute;left:72px;right:72px;top:470px">{browser(JOB)}</div>'
    + says("pointing", "Start where the company posts it.", 960)
    + count(2)))

# 3 click the icon
POP = (f'<div style="position:relative;padding:36px 40px;height:390px">'
       f'<div style="opacity:.35">{JOB_IN}</div>'
       f'<div class="card" style="position:absolute;right:28px;top:20px;width:560px;padding:30px 32px">'
       f'<div style="display:flex;align-items:center;gap:14px">{tick("waving", 54)}<div class="d" style="font-size:44px">Day60</div></div>'
       f'<div style="font-size:28px;margin-top:14px;line-height:1.3">Account Executive · Northpine</div>'
       f'<div class="btn" style="display:block;text-align:center;margin-top:22px;font-size:32px;padding:20px 18px">Find the 4 people with Day60</div></div></div>')
out("p14_ext_steps_3", page(
    EX + head("02", "Click the Day60 icon. Press the button.", 220)
    + f'<div style="position:absolute;left:72px;right:72px;top:470px">{browser(POP)}</div>'
    + says("thinking", "It only runs when you click it.", 1000, 160)
    + count(3)))

# 4 opens in Day60
ROLES = [("Hiring manager", PINK), ("Their boss", COBALT), ("Internal champion", MINT), ("Recruiter", LIME)]
chips = "".join(f'<span class="sticker" style="background:{bg};{"color:#FFFFFF;" if bg == COBALT else ""}font-size:19px;box-shadow:none;padding:8px 14px;margin:0 8px 12px 0;letter-spacing:.04em">{r}</span>' for r, bg in ROLES)
APP = (f'<div style="padding:36px 40px"><div class="lbl" style="font-size:28px">Job link</div>'
       f'<div style="border:4px solid {INK};border-radius:18px;padding:20px 24px;font-size:30px;background:{CREAM};margin-top:14px;'
       f'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;display:flex;gap:16px;align-items:center">{check(40)}<span>{URL}</span></div>'
       f'<div class="lbl" style="font-size:28px;margin-top:34px">Next: the 4 people closest to the hire</div>'
       f'<div style="margin-top:18px">{chips}</div></div>')
out("p14_ext_steps_4", page(
    EX + head("03", "The job opens in Day60, link filled in.", 220)
    + f'<div style="position:absolute;left:72px;right:72px;top:470px">{browser(APP, "getday60.com")}</div>'
    + says("celebrating", "Your sprint takes it from there.", 1010, 160)
    + count(4)))

# 5 what it never does
NEVER = ["Read your LinkedIn pages", "Fill in forms or apply for you", "Send messages for you"]
rows = "".join(f'<div style="display:flex;gap:22px;align-items:center;font-size:44px;font-weight:700;margin-top:30px">{check(60, False)}{t}</div>' for t in NEVER)
out("p14_ext_steps_5", page(
    f'<div style="position:absolute;left:72px;top:96px"><span class="sticker" style="background:{PINK}">Plain answers</span></div>'
    + spark(900, 100, 60)
    + f'<div class="d" style="position:absolute;left:72px;right:72px;top:220px;font-size:110px">What it never does.</div>'
    + f'<div class="card" style="position:absolute;left:72px;right:72px;top:470px;padding:16px 44px 46px">{rows}'
      f'<div style="border-top:4px solid {INK};margin-top:40px;padding-top:30px;display:flex;gap:22px;align-items:center;font-size:44px;font-weight:700">'
      f'{check(60)}Runs only when you click it</div></div>'
    + f'<div style="position:absolute;right:80px;top:960px">{tick("waiting", 200)}</div>'
    + count(5)))

# 6 CTA (dark)
out("p14_ext_steps_6", page(
    spark(900, 110, 60, LIME) + spark(960, 980, 50, PINK)
    + f'<div class="d" style="position:absolute;left:72px;right:72px;top:150px;font-size:100px;color:{CREAM}">Find the job.<br><span style="color:{LIME}">One click to start working it.</span></div>'
    + f'<div class="card" style="position:absolute;left:72px;top:720px;padding:32px 40px;background:{CREAM};box-shadow:12px 12px 0 {LIME}">'
      f'<div class="d" style="font-size:56px">Free in the Chrome Web Store.</div>'
      f'<div style="font-size:34px;font-weight:700;margin-top:10px">getday60.com/chrome-extension</div></div>'
    + f'<div class="d" style="position:absolute;left:74px;top:1020px;font-size:40px;color:{CREAM}">Search “Day60” in the store →</div>'
    + f'<div style="position:absolute;right:80px;top:930px">{tick("celebrating", 220)}</div>'
    + count(6, dark=True), bg=D_BG))

if __name__ == "__main__":
    jf = os.path.join(TMP, "jobs.json"); json.dump(jobs, open(jf, "w"))
    subprocess.run(["node", os.path.join(ROOT, "templates", "render_many.js"), jf], check=True)
