"""Product Hunt gallery (launch Tue Dec 1, moved from Nov 17 on Nov 11; Philip approved the kit Nov 7).

Builds, in Day60's design system (design-system/ds.py):
  01_hero.png           1270x760  tagline, Tick pointing at 4 role cards (invented names), "You send every message"
  02_is_isnt.png        1270x760  the week-46 is/isn't card, landscape, same words (with the Nov 5 line fix)
  03_one_click.png      1270x760  media/chrome-extension/screenshot-0-one-click.png, fitted on cream
  04_checker.png        1270x760  live getday60.com/message-checker crop (site/checker_checklist.png) on an invented draft
  05_linkedin_job.png   1270x760  media/chrome-extension/screenshot-3-linkedin-job.png, fitted on cream
  06_linkedin_profile.png 1270x760 media/chrome-extension/screenshot-4-linkedin-profile.png, fitted on cream
  thumbnail.png         240x240   Tick waving on lime
  ig_launch_day.png     1080x1350 portrait hero for the launch-day Instagram and Facebook posts

Run from repo root: python3 product-hunt/build.py
"""
import base64, json, os, subprocess, sys
PH = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(PH)
sys.path.insert(0, os.path.join(ROOT, "design-system"))
from ds import *  # noqa

TMP = os.path.join(PH, "_build"); os.makedirs(TMP, exist_ok=True)
jobs = []
W, H = 1270, 760

ROLES = [("Hiring manager", "Maya Torres"), ("Their boss", "Chris Patel"),
         ("Internal champion", "Dana Kim"), ("Recruiter", "Sam Rivera")]   # invented, same as the store screenshot


def out(name, body, w=W, h=H, bg=CREAM):
    p = os.path.join(TMP, name + ".html"); open(p, "w").write(page(body, w=w, h=h, bg=bg))
    jobs.append({"html": p, "png": os.path.join(PH, name + ".png"), "w": w, "h": h})


def data_uri(path):
    return "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()


def sticker(text, bg, x, y, size=22, shadow=True):
    sh = "" if shadow else "box-shadow:none;"
    return (f'<div style="position:absolute;left:{x}px;top:{y}px"><span class="sticker" '
            f'style="background:{bg};font-size:{size}px;padding:9px 20px;border-width:3px;{sh}">{text}</span></div>')


def logo(x=60, bottom=34, size=38):
    return (f'<div class="logo d" style="position:absolute;left:{x}px;bottom:{bottom}px;font-size:{size}px;gap:14px">'
            f'{tick("waving", 44)}Day60</div>')


def url(text="getday60.com", right=60, bottom=44, size=26):
    return f'<div class="url" style="position:absolute;right:{right}px;bottom:{bottom}px;font-size:{size}px">{text}</div>'


def role_card(x, y, w, h, role, name, fs=1.0):
    return (f'<div class="card" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'padding:{int(20*fs)}px {int(22*fs)}px;border-width:4px;border-radius:24px;box-shadow:8px 8px 0 {INK}">'
            f'<span class="sticker" style="background:{LIME};font-size:{int(15*fs)}px;padding:{int(6*fs)}px {int(14*fs)}px;'
            f'border-width:3px;box-shadow:none;letter-spacing:.06em;white-space:nowrap">{role}</span>'
            f'<div class="d" style="font-size:{int(34*fs)}px;margin-top:{int(16*fs)}px">{name}</div>'
            f'<div style="display:flex;gap:10px;align-items:center;margin-top:{int(14*fs)}px;font-size:{int(19*fs)}px;font-weight:700">'
            f'{check(int(28*fs))}<span>Verified work email</span></div>'
            f'<div style="display:flex;gap:10px;align-items:center;margin-top:{int(8*fs)}px;font-size:{int(19*fs)}px;font-weight:700">'
            f'{check(int(28*fs))}<span>Short note drafted</span></div></div>')


def role_grid(x, y, cw, ch, gap, fs=1.0):
    s = ""
    for k, (r, n) in enumerate(ROLES):
        s += role_card(x + (k % 2) * (cw + gap), y + (k // 2) * (ch + gap), cw, ch, r, n, fs)
    return s


def job_pill(x, y, size=22):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;display:flex;align-items:center;gap:12px;'
            f'background:{WHITE};border:3px solid {INK};border-radius:999px;padding:9px 20px;font-size:{size}px;font-weight:700">'
            f'<span style="color:{MUTED_TEXT}">Job link</span><span>Account Executive · Acme</span></div>')


# ---------- 01 hero ----------
out("01_hero",
    f'<div class="d" style="position:absolute;left:60px;top:70px;width:540px;font-size:62px">'
    f'Paste a job link. <span class="fill">Meet the 4 people closest to the hire.</span></div>'
    + f'<div style="position:absolute;left:62px;top:300px;width:390px;font-size:24px;font-weight:600;line-height:1.35">'
      f'Verified work emails. A short note to each, in your voice. Tick checks every draft.</div>'
    + sticker("You send every message", MINT, 60, 452, 21)
    + f'<div style="position:absolute;left:462px;top:446px">{tick("pointing", 146)}</div>'
    + job_pill(640, 56)
    + role_grid(640, 126, 274, 202, 22)
    + f'<div style="position:absolute;left:642px;top:572px;font-size:18px;font-weight:700;color:{MUTED_TEXT}">'
      f'Illustrative example · invented names</div>'
    + spark(1196, 28, 34) + spark(1130, 600, 26, MINT)
    + logo() + url())

# ---------- 02 is / isn't (landscape) ----------
rows_is = ["A 60-day sprint", "The 4 people closest to the hire", "A short note in your voice", "You hit send"]
rows_not = ["An auto-apply bot", "A LinkedIn login", "Mass messages", "Keyword stuffing"]


def col(x, title, rows, ok, lab_bg):
    items = "".join(f'<div style="display:flex;gap:14px;align-items:center;margin-top:24px;font-size:28px;font-weight:700;line-height:1.15">'
                    f'{check(40, ok)}<span>{r}</span></div>' for r in rows)
    return (f'<div class="card" style="position:absolute;left:{x}px;top:64px;width:340px;height:560px;padding:28px 26px;'
            f'border-width:4px;border-radius:28px;box-shadow:10px 10px 0 {INK}">'
            f'<span class="sticker" style="background:{lab_bg};box-shadow:none;font-size:20px;padding:8px 18px;border-width:3px">{title}</span>{items}</div>')


out("02_is_isnt",
    sticker("Day60, in one picture", PINK, 60, 64, 20)
    + f'<div class="d" style="position:absolute;left:60px;top:130px;font-size:104px">Is. Isn\'t.</div>'
    + f'<div class="d" style="position:absolute;left:60px;top:268px;width:400px;font-size:38px;line-height:1.12">'
      f'Most job tools make applying faster. <span class="fill">Day60 gets you to the person who decides.</span></div>'
    + f'<div style="position:absolute;left:318px;top:500px">{tick("pointing", 118)}</div>'
    + col(500, "It is", rows_is, True, MINT) + col(870, "It isn't", rows_not, False, PINK)
    + logo() + url())

# ---------- 03 / 05 / 06 store screenshots, fitted on cream (their edges are cream) ----------
for name, src in [("03_one_click", "screenshot-0-one-click.png"),
                  ("05_linkedin_job", "screenshot-3-linkedin-job.png"),
                  ("06_linkedin_profile", "screenshot-4-linkedin-profile.png")]:
    img = data_uri(os.path.join(ROOT, "media", "chrome-extension", src))
    out(name, f'<img src="{img}" style="position:absolute;left:{(W-1216)//2}px;top:0;width:1216px;height:760px">')

# ---------- 04 message checker (live crop) ----------
DRAFT_SUBJ = "Following up on my application for the Account Executive role at Northpine"
DRAFT = "I hope this email finds you well! I wanted to reach out because I recently applied for the Account Executive position…"
crop = data_uri(os.path.join(PH, "site", "checker_checklist.png"))
out("04_checker",
    sticker("Example · invented message", MUTED, 60, 60, 18, shadow=False)
    + f'<div class="d" style="position:absolute;left:60px;top:118px;width:470px;font-size:64px">Tick checks every draft.</div>'
    + f'<div style="position:absolute;left:62px;top:268px;width:440px;font-size:23px;font-weight:600;line-height:1.35">'
      f'The same rules Day60 uses on every note. You fix it, then you send it.</div>'
    + f'<div class="card" style="position:absolute;left:60px;top:378px;width:440px;padding:20px 24px;border-width:4px;'
      f'border-radius:22px;box-shadow:8px 8px 0 {INK};font-size:18px;line-height:1.4">'
      f'<div style="font-weight:700;color:{MUTED_TEXT}">Subject</div><div style="font-weight:700">{DRAFT_SUBJ}</div>'
      f'<div style="margin-top:10px">{DRAFT}</div></div>'
    + f'<div style="position:absolute;left:62px;top:596px;width:460px;font-size:21px;font-weight:700;line-height:1.3">'
      f'Free on its own:<br>getday60.com/message-checker</div>'
    + f'<div style="position:absolute;left:556px;top:56px;width:654px;height:590px;overflow:hidden">'
      f'<img src="{crop}" style="width:654px;display:block">'
      f'<div style="position:absolute;left:0;right:0;bottom:0;height:120px;background:linear-gradient(rgba(255,248,236,0),{CREAM} 85%)"></div></div>'
    + logo())

# ---------- thumbnail ----------
out("thumbnail",
    f'<div style="position:absolute;inset:0;background:{LIME};border:6px solid {INK};border-radius:44px"></div>'
    f'<div style="position:absolute;left:47px;top:22px">{tick("waving", 146)}</div>', w=240, h=240, bg=LIME)

# ---------- Instagram / Facebook launch-day portrait ----------
out("ig_launch_day",
    sticker("On Product Hunt today", PINK, 72, 84, 28)
    + spark(900, 70, 60) + spark(990, 40, 32, MINT)
    + f'<div class="d" style="position:absolute;left:72px;top:176px;width:936px;font-size:86px">'
      f'Paste a job link.<br><span class="fill">Meet the 4 people closest to the hire.</span></div>'
    + job_pill(72, 470, 26)
    + role_grid(72, 550, 455, 230, 24, fs=1.15)
    + f'<div style="position:absolute;left:74px;top:1048px;font-size:22px;font-weight:700;color:{MUTED_TEXT}">'
      f'Illustrative example · invented names</div>'
    + sticker("You send every message", MINT, 72, 1092, 26)
    + f'<div class="d" style="position:absolute;left:72px;top:1180px;width:720px;font-size:44px;line-height:1.1">'
      f'Search Day60 on Product Hunt.<br>Tell us what you think.</div>'
    + f'<div style="position:absolute;right:70px;top:1066px">{tick("pointing", 164)}</div>',
    w=1080, h=1350)

if __name__ == "__main__":
    jf = os.path.join(TMP, "jobs.json"); json.dump(jobs, open(jf, "w"))
    subprocess.run(["node", os.path.join(ROOT, "templates", "render_many.js"), jf], check=True)
