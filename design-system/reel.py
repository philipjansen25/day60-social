"""Shared pieces for token-built posts: Reels (1080x1920 scenes -> silent MP4) and slide helpers.

    from reel import *
    render(jobs)                                   # [{"html", "png", "w", "h"}] via templates/render_many.js
    make_reel([(name, html, seconds), ...], out_mp4, tmp_dir)

Hard cuts between scenes, 30 fps, silent AAC track (Instagram wants one), cover = first frame.
"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from ds import *  # noqa

RW, RH = 1080, 1920


def render(jobs, tmp):
    jf = os.path.join(tmp, "jobs.json")
    json.dump(jobs, open(jf, "w"))
    subprocess.run(["node", os.path.join(ROOT, "templates", "render_many.js"), jf], check=True)


def make_reel(scenes, out_mp4, tmp):
    os.makedirs(tmp, exist_ok=True)
    jobs = []
    for name, html, _ in scenes:
        p = os.path.join(tmp, name + ".html"); open(p, "w").write(html)
        jobs.append({"html": p, "png": os.path.join(tmp, name + ".png"), "w": RW, "h": RH})
    render(jobs, tmp)
    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w") as f:
        for name, _, d in scenes:
            f.write(f"file '{name}.png'\nduration {d}\n")
        f.write(f"file '{scenes[-1][0]}.png'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                    "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-shortest",
                    "-movflags", "+faststart", out_mp4], check=True)
    print("wrote", out_mp4, f"{sum(d for _, _, d in scenes):.1f} s")


def sticker(text, bg, x, y, size=28, right=False):
    side = "right" if right else "left"
    return (f'<div style="position:absolute;{side}:{x}px;top:{y}px"><span class="sticker" '
            f'style="background:{bg};font-size:{size}px">{text}</span></div>')


def tick_says(pose, text, top, w=250, tail=70, size=46):
    return (f'<div style="position:absolute;left:64px;right:64px;top:{top}px;display:flex;align-items:flex-end;gap:26px">'
            f'{tick(pose, w, "flex:none")}<div class="bubble left" style="--tail:{tail}px;margin-bottom:{int(w*0.55)}px;'
            f'font-size:{size}px">{text}</div></div>')


def step_head(n, text, top=200, size=84):
    return (f'<div style="position:absolute;left:72px;top:{top}px;right:72px;display:flex;gap:36px;align-items:center">'
            f'<div class="step d" style="flex:none">{n}</div><div class="d" style="font-size:{size}px">{text}</div></div>')


def lbl(text, size=26, color=MUTED_TEXT):
    return (f'<div style="font-size:{size}px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;'
            f'color:{color};margin-bottom:14px">{text}</div>')


EXAMPLE = "Illustrative example"
COMPANY = "Northpine"
JOB = "Customer Success Manager"
JOB_URL = "careers.northpine.example/jobs/csm"
# Invented people for the Northpine Customer Success Manager example (same names as the week 46 Reel).
PEOPLE = [("MO", "Maya Ortiz", "Head of Customer Success", "Hiring manager", PINK, INK),
          ("DR", "Dev Raman", "VP Customer Experience", "Their boss", COBALT, WHITE),
          ("JK", "Jess Kowalski", "Senior Customer Success Manager", "Internal champion", MINT, INK),
          ("PH", "Priya Hale", "Talent Partner", "Recruiter", LIME, INK)]


def person_row(p, scale=1.0, email=True, mb=26):
    ini, name, title, role, bg, fg = p
    s = lambda v: int(v * scale)
    mail = (f'<div style="display:flex;align-items:center;gap:10px;font-size:{s(26)}px;font-weight:700;margin-top:8px">'
            f'{check(s(30))}Verified work email</div>') if email else ""
    return (f'<div class="card" style="padding:{s(22)}px {s(28)}px;display:flex;align-items:center;gap:{s(24)}px;margin-bottom:{mb}px">'
            f'<div class="d" style="flex:none;width:{s(96)}px;height:{s(96)}px;border-radius:50%;border:4px solid {INK};'
            f'background:{bg};color:{fg};display:flex;align-items:center;justify-content:center;font-size:{s(40)}px;letter-spacing:0">{ini}</div>'
            f'<div style="flex:1;min-width:0"><div class="lbl" style="font-size:{s(38)}px">{name}</div>'
            f'<div style="font-size:{s(27)}px;color:{MUTED_TEXT};margin-top:2px">{title}</div>{mail}</div>'
            f'<span class="sticker" style="flex:none;background:{MUTED};font-size:{s(20)}px;box-shadow:none;padding:8px 16px">{role}</span></div>')
