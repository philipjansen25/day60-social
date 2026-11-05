"""Week 46 rebuild in Day60's design system (HQ, Nov 5).

Rebuilds p01 (is/isn't carousel), p02 (is/isn't card), p04 (where it fits) and
p06 (3 touches carousel + LinkedIn PDF) with design-system/ds.py.
Same filenames, so posts.md is unchanged. Copy is unchanged from build.py.

Run from repo root: python3 2026-11/wk46/build_v2.py
"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "design-system"))
from ds import *  # noqa
HERE = os.path.dirname(os.path.abspath(__file__))

TMP = os.path.join(HERE, "_v2"); os.makedirs(TMP, exist_ok=True)
jobs = []


def out(name, html):
    p = os.path.join(TMP, name + ".html"); open(p, "w").write(html)
    jobs.append({"html": p, "png": os.path.join(HERE, name + ".png"), "w": 1080, "h": 1350})


def count(i, n, dark=False):
    return foot(bottom=56, right=f"{i}/{n}", dark=dark)


def sticker(text, bg, x=72, y=96, size=28):
    return f'<div style="position:absolute;left:{x}px;top:{y}px"><span class="sticker" style="background:{bg};font-size:{size}px">{text}</span></div>'


def bubble_tick(pose, text, top, w=210, left=72):
    return (f'<div style="position:absolute;left:{left}px;right:72px;top:{top}px;display:flex;align-items:flex-end;gap:24px">'
            f'{tick(pose, w, "flex:none")}<div class="bubble left" style="--tail:56px;margin-bottom:{int(w*0.5)}px;font-size:38px">{text}</div></div>')


def cover(i, n, label, title_html, sub, pose):
    return page(
        sticker(label, PINK) + spark(880, 90, 70) + spark(970, 230, 40, MINT)
        + f'<div class="d" style="position:absolute;left:72px;top:230px;right:72px;font-size:128px">{title_html}</div>'
        + f'<div style="position:absolute;left:74px;top:720px;width:560px;font-size:40px;font-weight:700;line-height:1.25">{sub}</div>'
        + f'<div style="position:absolute;left:72px;top:1010px"><span class="btn" style="font-size:38px;padding:18px 34px">Swipe →</span></div>'
        + f'<div style="position:absolute;right:80px;top:800px">{tick(pose, 300)}</div>'
        + count(i, n))


def end_dark(i, n, top_html, card_title, card_sub, cta):
    return page(
        spark(900, 110, 60, LIME) + spark(960, 1000, 50, PINK)
        + f'<div class="d" style="position:absolute;left:72px;top:150px;right:72px;font-size:90px;line-height:1.02;color:{CREAM}">{top_html}</div>'
        + f'<div class="card" style="position:absolute;left:72px;top:760px;padding:32px 40px;background:{CREAM};box-shadow:12px 12px 0 {LIME}">'
          f'<div class="d" style="font-size:56px">{card_title}</div><div style="font-size:34px;font-weight:700;margin-top:10px">{card_sub}</div></div>'
        + f'<div class="d" style="position:absolute;left:74px;top:1060px;font-size:46px;color:{CREAM}">{cta}</div>'
        + f'<div style="position:absolute;right:80px;top:940px">{tick("celebrating", 220)}</div>'
        + count(i, n, dark=True), bg=D_BG)


# ---------- P01 is / isn't carousel ----------
N = 7
out("p01_is_isnt_1", cover(1, N, "The short version",
    'What Day60 <span class="fill">is.</span><br>And what it isn\'t.',
    "Five slides. No jargon. Save it for the next time someone asks.", "waving"))


def is_slide(i, ok, title, body, pose):
    lab = ("It is", MINT) if ok else ("It isn't", PINK)
    return page(
        f'<div style="position:absolute;left:72px;top:96px;display:flex;gap:22px;align-items:center">'
        f'{check(58, ok)}<span class="sticker" style="background:{lab[1]}">{lab[0]}</span></div>'
        + spark(940, 100, 52, MINT if ok else PINK)
        + f'<div style="position:absolute;left:72px;right:72px;top:240px"><div class="d" style="font-size:104px">{title}</div>'
          f'<div class="card" style="margin-top:56px;padding:40px 44px;font-size:42px;line-height:1.32">{body}</div></div>'
        + f'<div style="position:absolute;right:80px;top:930px">{tick(pose, 220)}</div>'
        + count(i, N))


out("p01_is_isnt_2", is_slide(2, True, "A 60-day job-search sprint.",
    "Pick up to 3 new jobs a day, up to 60 in a sprint. A plan with a start, a finish and a job for every day.", "running"))
out("p01_is_isnt_3", is_slide(3, True, "The 4 people closest to the hire.",
    "For every job: the hiring manager, their boss, an internal champion and the recruiter. Verified work emails where available.", "pointing"))
out("p01_is_isnt_4", is_slide(4, True, "A short note, in your voice.",
    "Tick checks every draft against the writing rules. Then you hit send. Three touches per person, max: day 0, day 2, day 7.", "thinking"))
out("p01_is_isnt_5", is_slide(5, False, "An auto-apply bot.",
    "Day60 never applies for you and never sends anything. Every message goes out from you, to one person, on purpose.", "waiting"))
out("p01_is_isnt_6", is_slide(6, False, "A LinkedIn hack.",
    "It never logs in to LinkedIn, scrapes it or automates it. No mass messages. No keyword stuffing.", "waiting"))
out("p01_is_isnt_7", end_dark(7, N,
    'Keep your tracker and your résumé tool.<br><br><span class="fill" style="color:#16133A">Day60 is the part after you find the job.</span>',
    "Day60 Sprint. Free.", "No card. Nothing to cancel.", "Link in bio →"))

# ---------- P02 is / isn't card ----------
rows_is = ["A 60-day sprint", "The 4 people closest to the hire", "A short note in your voice", "You hit send"]
rows_not = ["An auto-apply bot", "A LinkedIn login", "Mass messages", "Keyword stuffing"]


def col(x, title, rows, ok, lab_bg):
    items = "".join(f'<div style="display:flex;gap:18px;align-items:center;margin-top:28px;font-size:36px;font-weight:700;line-height:1.15">'
                    f'{check(48, ok)}<span>{r}</span></div>' for r in rows)
    return (f'<div class="card" style="position:absolute;left:{x}px;top:330px;width:440px;height:600px;padding:34px 30px">'
            f'<span class="sticker" style="background:{lab_bg};box-shadow:none">{title}</span>{items}</div>')


out("p02_is_isnt_card", page(
    sticker("Day60, in one picture", PINK) + spark(900, 96, 60) + spark(975, 210, 36, MINT)
    + f'<div class="d" style="position:absolute;left:72px;top:185px;font-size:96px">Is. Isn\'t.</div>'
    + col(72, "It is", rows_is, True, MINT) + col(568, "It isn't", rows_not, False, PINK)
    + f'<div class="d" style="position:absolute;left:72px;top:1000px;width:700px;font-size:50px;line-height:1.1">'
      f'Every other tool makes applying faster. <span class="fill">Day60 gets you to the person who decides.</span></div>'
    + f'<div style="position:absolute;right:76px;top:980px">{tick("pointing", 190)}</div>'
    + foot()))

# ---------- P04 where Day60 fits ----------
steps = [("Find the job", "your job board"), ("Tailor your résumé", "your résumé tool"),
         ("Track it", "your tracker"), ("Reach the people who decide", "Day60")]
flow = ""
for k, (a, b) in enumerate(steps):
    y = 260 + k * 172
    me = k == 3
    flow += (f'<div class="card" style="position:absolute;left:72px;right:72px;top:{y}px;height:140px;padding:0 34px;'
             f'display:flex;align-items:center;justify-content:space-between;{"background:"+LIME if me else ""}">'
             f'<div style="display:flex;align-items:center;gap:28px"><div class="step d" style="width:96px;height:96px;font-size:52px;'
             f'background:{WHITE if me else LIME};box-shadow:none">{k+1}</div>'
             f'<div style="font-size:40px;font-weight:700;{"max-width:430px;line-height:1.1" if me else ""}">{a}</div></div>'
             + (f'<div class="d" style="font-size:52px">Day60</div>' if me else
                f'<div style="font-size:32px;font-weight:700;color:{MUTED_TEXT}">{b}</div>') + '</div>')
out("p04_where_it_fits", page(
    spark(910, 96, 60) + spark(980, 200, 36, MINT)
    + f'<div class="d" style="position:absolute;left:72px;top:100px;font-size:112px">Where Day60 fits.</div>'
    + flow
    + bubble_tick("pointing", "Keep your tools. Day60 is the part after you find the job.", 935, 150)
    + foot()))

# ---------- P06 3 touches ----------
N6 = 6
out("p06_three_touches_1", cover(1, N6, "Save this", '3 touches.<br><span class="fill">Then stop.</span>',
    "The follow-up rhythm that's persistent, not pushy.", "running"))


def touch(i, n, day, title, body, pose):
    return page(
        f'<div style="position:absolute;left:72px;top:96px;display:flex;gap:28px;align-items:center">'
        f'<div class="step d" style="width:auto;padding:0 34px;font-size:60px">{day}</div>'
        f'<span class="sticker" style="background:{MINT}">Touch {n} of 3</span></div>'
        + spark(940, 100, 52)
        + f'<div style="position:absolute;left:72px;right:72px;top:290px"><div class="d" style="font-size:110px">{title}</div>'
          f'<div class="card" style="margin-top:56px;padding:40px 44px;font-size:42px;line-height:1.32">{body}</div></div>'
        + f'<div style="position:absolute;right:80px;top:900px">{tick(pose, 220)}</div>'
        + count(i, N6))


out("p06_three_touches_2", touch(2, 1, "Day 0", "The first note.",
    "Their problem, one line of proof, one easy ask. Short enough to read on a phone between meetings.", "pointing"))
out("p06_three_touches_3", touch(3, 2, "Day 2", "The nudge.",
    'Two lines. Add something new: a number, a link, a sharper question. Never "just following up."', "thinking"))
out("p06_three_touches_4", touch(4, 3, "Day 7", "The last word.",
    "Close the loop kindly and leave the door open. People remember who made it easy to say no.", "waving"))
out("p06_three_touches_5", page(
    sticker("The rule", PINK) + spark(900, 110, 60)
    + f'<div class="d" style="position:absolute;left:72px;top:220px;right:72px;font-size:140px">Then stop.</div>'
    + f'<div style="position:absolute;left:74px;top:420px;width:880px;font-size:48px;line-height:1.3;font-weight:700">'
      f'Three touches is persistence. Ten is spam.</div>'
    + bubble_tick("waiting", "Day60 keeps it to 3 touches per person: day 0, day 2, day 7. Across four people, that's plenty of chances to be the one who got answered.", 600, 200)
    + count(5, N6)))
out("p06_three_touches_6", end_dark(6, N6,
    'Four people. Three touches.<br><br><span class="fill" style="color:#16133A">You send every one.</span>',
    "Try one job free.", "getday60.com/try · No account needed.", ""))

if __name__ == "__main__":
    jf = os.path.join(TMP, "jobs.json"); json.dump(jobs, open(jf, "w"))
    subprocess.run(["node", os.path.join(ROOT, "templates", "render_many.js"), jf], check=True)
    from PIL import Image
    ims = [Image.open(os.path.join(HERE, f"p06_three_touches_{i}.png")).convert("RGB") for i in range(1, 7)]
    ims[0].save(os.path.join(HERE, "p06_three_touches_linkedin.pdf"), save_all=True, append_images=ims[1:], resolution=144)
    print("pdf ok")
