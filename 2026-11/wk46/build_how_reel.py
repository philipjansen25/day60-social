"""p13_how_it_works_reel.mp4: replaces the retired /try phone clip (IG2, FB4).

Cards from Day60 design tokens (design-system/ds.py). Invented company and
people, labeled as an example. Steps follow getday60.com/how-it-works:
paste a job link -> Day60 finds the 4 people -> Tick checks the message -> you send it.

Run from repo root: python3 2026-11/wk46/build_how_reel.py
"""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "design-system"))
from ds import *  # noqa

OUT = os.path.join(ROOT, "2026-11", "wk46")
TMP = os.path.join(OUT, "_how")
os.makedirs(TMP, exist_ok=True)
W, H = 1080, 1920

EXAMPLE = (f'<div style="position:absolute;right:64px;top:84px"><span class="sticker" '
           f'style="background:{MUTED};font-size:24px">Example · invented company &amp; people</span></div>')
COMPANY = "Northpine"
URL = "careers.northpine.example/jobs/account-executive"


def head(n, text):
    return (f'<div style="position:absolute;left:72px;top:200px;right:72px;display:flex;gap:36px;align-items:center">'
            f'<div class="step d">{n}</div><div class="d" style="font-size:84px">{text}</div></div>')


def tick_says(pose, text, top, w=250, tail=70):
    return (f'<div style="position:absolute;left:64px;right:64px;top:{top}px;display:flex;align-items:flex-end;gap:26px">'
            f'{tick(pose, w, "flex:none")}<div class="bubble left" style="--tail:{tail}px;margin-bottom:{int(w*0.55)}px">{text}</div></div>')


def s_hook():
    return page(
        f'<div style="position:absolute;left:72px;top:150px"><span class="sticker" style="background:{PINK}">How Day60 works</span></div>'
        f'<div class="d" style="position:absolute;left:72px;right:72px;top:300px;font-size:150px">Paste a job link.<br>'
        f'Meet the <span class="fill" style="white-space:nowrap">4 people</span> who decide.</div>'
        + spark(880, 260, 80) + spark(960, 820, 54, MINT)
        + tick_says("waving", "Hi, I'm Tick. Here's one job, start to finish.", 1050, 330, 90)
        + foot(), W, H)


def s_paste(filled):
    field = (f'<span style="color:{INK}">{URL}</span>' if filled else
             f'<span style="color:{MUTED_TEXT}">Paste a job link</span>')
    job = (f'<div class="card" style="margin-top:44px;padding:34px 40px;display:flex;align-items:center;gap:28px">'
           f'<div style="width:96px;height:96px;border:4px solid {INK};border-radius:24px;background:{MINT};'
           f'display:flex;align-items:center;justify-content:center;font-size:54px" class="d">N</div>'
           f'<div><div class="d" style="font-size:56px">Account Executive</div>'
           f'<div style="font-size:36px;color:{MUTED_TEXT};margin-top:8px">{COMPANY} · Denver</div></div></div>') if filled else ""
    return page(
        EXAMPLE + head("01", "Paste a job link.")
        + f'<div style="position:absolute;left:72px;right:72px;top:470px">'
          f'<div class="card" style="padding:40px"><div class="lbl" style="font-size:32px;margin-bottom:20px">Job link</div>'
          f'<div style="border:4px solid {INK};border-radius:20px;padding:26px 28px;font-size:34px;background:{CREAM};'
          f'white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{field}</div></div>{job}</div>'
        + tick_says("pointing", "Start with the company's own careers page.", 1150)
        + foot(), W, H)


PEOPLE = [("MO", "Maya Ortiz", "Head of Sales", "Hiring manager", PINK, INK),
          ("DR", "Dev Raman", "VP Revenue", "Their boss", COBALT, WHITE),
          ("JK", "Jess Kowalski", "Senior Account Executive", "Internal champion", MINT, INK),
          ("PH", "Priya Hale", "Talent Partner", "Recruiter", LIME, INK)]


def s_people(k):
    rows = ""
    for i, (ini, name, title, role, bg, fg) in enumerate(PEOPLE[:k]):
        rows += (f'<div class="card" style="padding:26px 32px;display:flex;align-items:center;gap:28px;margin-bottom:30px">'
                 f'<div class="d" style="flex:none;width:104px;height:104px;border-radius:50%;border:4px solid {INK};'
                 f'background:{bg};color:{fg};display:flex;align-items:center;justify-content:center;font-size:44px;letter-spacing:0">{ini}</div>'
                 f'<div style="flex:1"><div class="lbl" style="font-size:42px">{name}</div>'
                 f'<div style="font-size:31px;color:{MUTED_TEXT};margin-top:4px">{title}, {COMPANY}</div></div>'
                 f'<span class="sticker" style="background:{MUTED};font-size:22px;box-shadow:none;padding:10px 18px">{role}</span></div>')
    bub = (tick_says("celebrating", "The 4 people closest to the hire.", 1330, 230) if k == 4 else "")
    return page(EXAMPLE + head("02", "Day60 finds the 4 people.")
                + f'<div style="position:absolute;left:72px;right:72px;top:450px">{rows}</div>' + bub + foot(), W, H)


CHECKS = ["Asks one clear question", "The question comes last", "Fits the length limit", "No links"]


def s_check(done):
    msg = ("Hi Maya, saw Northpine opened its Denver showroom in October. "
           "At my last company I grew a new territory to $1.2M in year one. "
           "Worth 10 minutes to talk about the Account Executive role?")
    items = "".join(f'<div style="display:flex;gap:20px;align-items:center;font-size:36px;font-weight:700;margin-top:18px">'
                    f'{check(50)}{c}</div>' for c in CHECKS) if done else ""
    say = (tick_says("celebrating", "Checked. Edit it, then you send it.", 1380, 230) if done
           else tick_says("thinking", "Checking it against the rules…", 1380, 230))
    return page(EXAMPLE + head("03", "Tick checks the message.")
                + f'<div style="position:absolute;left:72px;right:72px;top:450px">'
                  f'<div class="card" style="padding:38px 40px"><div class="lbl" style="font-size:30px;color:{MUTED_TEXT}">'
                  f'To Maya Ortiz · Head of Sales</div><div style="font-size:38px;line-height:1.38;margin-top:16px">{msg}</div></div>'
                  f'<div style="margin-top:34px;padding-left:8px">{items}</div></div>'
                + say + foot(), W, H)


def s_end():
    return page(
        f'<div class="d" style="position:absolute;left:72px;right:72px;top:250px;font-size:170px">You<br><span class="fill">send it.</span></div>'
        f'<div style="position:absolute;left:72px;right:72px;top:720px;font-size:48px;line-height:1.3">'
        f'Day60 never logs in to LinkedIn and never sends anything for you.</div>'
        f'<div style="position:absolute;left:72px;top:1010px"><span class="btn">Try one job free →</span>'
        f'<div style="font-size:38px;font-weight:700;margin-top:34px">getday60.com/try · No account. No card.</div></div>'
        + spark(860, 230, 84) + spark(940, 560, 50, MINT)
        + f'<div style="position:absolute;right:80px;top:1240px">{tick("celebrating", 360)}</div>'
        + foot(), W, H)


SCENES = [("hook", s_hook(), 2.8),
          ("paste0", s_paste(False), 1.2), ("paste1", s_paste(True), 2.4),
          ("people1", s_people(1), 0.6), ("people2", s_people(2), 0.6), ("people3", s_people(3), 0.6), ("people4", s_people(4), 2.6),
          ("check0", s_check(False), 1.6), ("check1", s_check(True), 3.0),
          ("end", s_end(), 3.2)]

if __name__ == "__main__":
    jobs = []
    for name, html, _ in SCENES:
        p = os.path.join(TMP, name + ".html"); open(p, "w").write(html)
        jobs.append({"html": p, "png": os.path.join(TMP, name + ".png"), "w": W, "h": H})
    jf = os.path.join(TMP, "jobs.json"); json.dump(jobs, open(jf, "w"))
    subprocess.run(["node", os.path.join(ROOT, "templates", "render_many.js"), jf], check=True)
    lst = os.path.join(TMP, "list.txt")
    with open(lst, "w") as f:
        for name, _, d in SCENES:
            f.write(f"file '{name}.png'\nduration {d}\n")
        f.write(f"file '{SCENES[-1][0]}.png'\n")
    out = os.path.join(OUT, "p13_how_it_works_reel.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                    "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-shortest",
                    "-movflags", "+faststart", out], check=True)
    print("wrote", out)
