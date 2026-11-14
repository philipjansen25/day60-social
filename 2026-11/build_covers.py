"""New covers on palette grounds (Philip, Fri Nov 13 via HQ: "too much cream background" in the Instagram grid).

Every unpublished Instagram post gets a cover on a non-cream ground; Facebook posts that reuse an Instagram
cover use the same new file. Inner slides, captions and the words on each cover stay as they were. The old
cream covers stay in place (never renamed or deleted), so any post can go back.

Posting order and grounds (any four in a row differ; no cream; see design-system/grounds.py):
  1 IG7        Tue Nov 10* cobalt  2026-11/wk46/p17_ext_linkedin_1_cobalt.png   (*date is Philip's; not live yet)
  2 IG5        Sat Nov 14  mint    2026-11/wk46/p14_ext_steps_1_mint.png
  3 IG-resume  Sun Nov 15  lime    2026-11/wk47/p02_resume_builder_1_lime.png
  4 IG-four    Tue Nov 17  ink     2026-11/wk47/p01_four_people_1_ink.png
  5 IG-onejob  Wed Nov 18  coral   2026-11/wk47/p03_one_job_cover_coral.png   (Reel cover, 1080x1920)
  6 IG-redpen  Thu Nov 19  mint    2026-11/wk47/p04_red_pen_cover_mint.png    (Reel cover)
  7 IG-firstjob Sat Nov 21 lime    2026-11/wk47/p05_first_job_1_lime.png
  8 IG-thanks  Sun Nov 22  pink    2026-11/wk48/p01_thanks_1_pink.png
  9 IG-which   Mon Nov 23  ink     2026-11/wk48/p02_which_ink.png
 10 IG-rb-reel Tue Nov 24  cobalt  2026-11/wk48/p03_resume_cover_cobalt.png   (Reel cover)
 11 IG-onelink Wed Nov 25  mint    2026-11/wk48/p04_one_link_cover_mint.png   (Reel cover)
 12 IG-shortlist Sat Nov 28 coral  2026-11/wk48/p05_short_list_coral.png
 Extra: the published Reel IG2 (Nov 9), optional swap: 2026-11/wk46/p13_how_it_works_cover_ink.png

Reel covers are 1080x1920; the profile grid shows the middle 1080x1440, so everything that matters sits there.

Run from repo root: python3 2026-11/build_covers.py [names to render, default all]
"""
import json, os, subprocess, sys, tempfile
MONTH = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(MONTH)
sys.path.insert(0, os.path.join(ROOT, "design-system"))
from grounds import *  # noqa
from reel import tick_says, EXAMPLE, JOB_URL  # noqa

TMP = tempfile.mkdtemp(prefix="covers_")
jobs = []
COVERS = {}


def out(name, wk, g, body, h=1350):
    p = os.path.join(TMP, name + ".html")
    open(p, "w").write(cover_page(body, g, 1080, h))
    png = os.path.join(MONTH, wk, f"{name}_{g}.png")
    jobs.append({"html": p, "png": png, "w": 1080, "h": h})
    COVERS[name] = os.path.relpath(png, ROOT)


def stk(text, bg, x, y, size=28, right=False):
    side = "right" if right else "left"
    return (f'<div style="position:absolute;{side}:{x}px;top:{y}px"><span class="sticker" '
            f'style="background:{bg};font-size:{size}px">{text}</span></div>')


def at(x, y, html, right=False):
    side = "right" if right else "left"
    return f'<div style="position:absolute;{side}:{x}px;top:{y}px">{html}</div>'


def swipe(y=1000):
    return at(72, y, '<span class="btn" style="font-size:38px;padding:18px 34px">Swipe →</span>')


def head(text, top, size, right=72):
    return f'<div class="d" style="position:absolute;left:72px;right:{right}px;top:{top}px;font-size:{size}px">{text}</div>'


def sub(text, top, size=40, width=560, lh=1.25):
    return (f'<div style="position:absolute;left:74px;top:{top}px;width:{width}px;font-size:{size}px;'
            f'font-weight:700;line-height:{lh}">{text}</div>')


# 1. IG7 · cobalt (product news). Same words as p17_ext_linkedin_1.
g = "cobalt"
out("p17_ext_linkedin_1", "wk46", g,
    dial(900, 1060, 400, g)
    + stk("New in Day60 for Chrome", PINK, 72, 96)
    + spark(890, 90, 70) + spark(975, 220, 40, MINT)
    + head('Found it on LinkedIn? <span class="fill" style="white-space:nowrap">Take it to Day60.</span>', 220, 116)
    + sub("Two new buttons for LinkedIn. One for a job, one for a person.", 640)
    + swipe()
    + at(80, 790, tick("pointing", 300), right=True)
    + foot_g(g, bottom=56, right="1/5"))

# 2. IG5 · mint (how-to). Same words as p14_ext_steps_1. Lanes: careers page to sprint, one click.
g = "mint"
out("p14_ext_steps_1", "wk46", g,
    lanes(880, 3, 110, g)
    + stk("Free Chrome extension", PINK, 72, 96)
    + spark(890, 90, 70) + spark(975, 220, 40, COBALT)
    + head('From a careers page to your sprint. <span class="fill" style="white-space:nowrap">One click.</span>', 220, 118)
    + sub("How the Day60 extension works, in 3 steps.", 740)
    + swipe()
    + at(80, 790, tick("pointing", 300), right=True)
    + foot_g(g, bottom=56, right="1/6"))

# 3. IG-resume · lime (save this). Same words as p02_resume_builder_1.
g = "lime"
out("p02_resume_builder_1", "wk47", g,
    dial(860, 1010, 380, g, opacity=0.10)
    + stk("Save this", WHITE, 72, 72)
    + head("One résumé. Tailored to one job.", 200, 118)
    + sub("How the free résumé builder works, on an invented résumé and job.", 690, 44, 560, 1.2)
    + at(60, 660, tick("thinking", 320), right=True)
    + spark(870, 110, 70, WHITE) + spark(140, 1080, 44, PINK)
    + foot_g(g, right="getday60.com/resume-builder"))

# 4. IG-four · ink (the method). Same words as p01_four_people_1; "4 people" gets the lime highlight.
g = "ink"
out("p01_four_people_1", "wk47", g,
    dial(880, 1010, 400, g)
    + stk("Save this", WHITE, 72, 72)
    + head('Every job has <span class="fill" style="white-space:nowrap">4 people</span> who decide if you get it.', 200, 112, 72)
    + sub("An application reaches one of them. Maybe.", 760, 44, 560, 1.2)
    + at(60, 690, tick("pointing", 330), right=True)
    + spark(860, 120, 70) + spark(960, 250, 40, MINT)
    + confetti([(110, 1090, "dot", PINK, 44, 0), (190, 1120, "dot", COBALT, 44, 0), (270, 1090, "dot", MINT, 44, 0),
                (350, 1120, "dot", WHITE, 44, 0)])
    + foot_g(g))

# 5. IG-onejob Reel cover · coral. Same words as the Reel's first scene.
g = "coral"
out("p03_one_job_cover", "wk47", g,
    dial(170, 1430, 420, g)
    + stk("Where to start", WHITE, 72, 290)
    + head("Don't start with 50 jobs.", 410, 150)
    + head('<span class="fill">Start with one.</span>', 940, 150)
    + spark(900, 330, 80, WHITE) + spark(150, 1230, 50, MINT)
    + at(80, 1190, tick("thinking", 330), right=True)
    + foot_g(g), 1920)

# 6. IG-redpen Reel cover · mint. Same words as the Reel's first scene.
g = "mint"
out("p04_red_pen_cover", "wk47", g,
    dial(950, 1520, 380, g)
    + stk("Tick's red pen", PINK, 72, 290)
    + head('Your first message is <span class="fill">too long.</span>', 410, 156)
    + spark(900, 330, 80, CORAL)
    + tick_says("pointing", "Watch me cut it to 3 lines.", 1090, 310, 90)
    + foot_g(g), 1920)

# 7. IG-firstjob · lime (save this, step by step). Same words as p05_first_job_1. Track lanes and finish tape.
g = "lime"
out("p05_first_job_1", "wk47", g,
    lanes(960, 2, 120, g, opacity=0.16) + tape(560, 930, 300, PINK)
    + stk("Save this", WHITE, 72, 72)
    + head("One job. Four people. One message.", 200, 124, 72)
    + sub("Your first job in Day60, step by step.", 780, 46, 560, 1.2)
    + at(60, 700, tick("running", 320), right=True)
    + spark(880, 110, 70, WHITE)
    + foot_g(g))

# 8. IG-thanks · pink (warmth). Same words as p01_thanks_1. Confetti in the accents.
g = "pink"
out("p01_thanks_1", "wk48", g,
    stk("Save this", WHITE, 72, 72) + stk("Thanksgiving week", MINT, 290, 72)
    + head('Send one <span style="white-space:nowrap">thank-you</span> this week.', 210, 126, 72)
    + sub("3 people in your job search worth thanking, and what to say.", 790, 44, 560, 1.2)
    + at(60, 700, tick("celebrating", 320), right=True)
    + spark(900, 170, 64, WHITE)
    + confetti([(760, 640, "bar", MINT, 54, -20), (990, 600, "dot", COBALT, 40, 0), (690, 760, "ring", WHITE, 46, 0),
                (1000, 760, "bar", CORAL, 50, 30), (980, 1110, "dot", MINT, 36, 0), (640, 1060, "bar", WHITE, 46, 70)])
    + foot_g(g))

# 9. IG-which · ink (the method). Same words as p02_which.
g = "ink"


def opt(letter, bg, text):
    return (f'<div class="card" style="padding:34px 38px;display:flex;gap:30px;align-items:center;margin-bottom:46px;color:{INK}">'
            f'<div class="d" style="flex:none;width:110px;height:110px;border-radius:50%;border:5px solid {INK};background:{bg};'
            f'display:flex;align-items:center;justify-content:center;font-size:64px;letter-spacing:0">{letter}</div>'
            f'<div style="font-size:42px;font-weight:700;line-height:1.25">"{text}"</div></div>')


out("p02_which", "wk48", g,
    head("Which would you answer?", 110, 112, 72)
    + f'<div class="soft" style="position:absolute;left:76px;top:370px;width:900px;font-size:36px;font-weight:600;line-height:1.3">'
      f'Two ways to end a first message to a hiring manager.</div>'
    + stk(EXAMPLE, PINK, 72, 470, 24)
    + f'<div style="position:absolute;left:72px;width:920px;top:566px">'
      + opt("A", PINK, "Would you have 30 minutes this week to tell me about opportunities on your team?")
      + opt("B", MINT, "Is onboarding or renewals the bigger fire on your team right now?") + '</div>'
    + f'<div style="position:absolute;left:76px;top:1120px;font-size:40px;font-weight:700">Tell us: A or B?</div>'
    + at(64, 1030, tick("thinking", 170), right=True)
    + spark(930, 130, 60, PINK) + spark(990, 250, 36, MINT)
    + foot_g(g, bottom=40))

# 10. IG-rb-reel Reel cover · cobalt (free tool). Same words as the Reel's first scene.
g = "cobalt"
out("p03_resume_cover", "wk48", g,
    dial(880, 1480, 420, g)
    + stk("Free résumé builder", WHITE, 72, 290)
    + head("Tailor your résumé to one job.", 410, 150)
    + head('<span class="fill">No account.</span>', 1010, 120)
    + at(80, 1200, tick("thinking", 320), right=True)
    + spark(900, 330, 70, PINK) + spark(140, 1330, 44, MINT)
    + foot_g(g), 1920)

# 11. IG-onelink Reel cover · mint (how it works). Same words as the Reel's first scene.
g = "mint"
out("p04_one_link_cover", "wk48", g,
    lanes(1200, 3, 120, g)
    + stk(EXAMPLE, MUTED, 64, 290, 24, right=True)
    + head("One job link.", 390, 150)
    + f'<div style="position:absolute;left:72px;right:72px;top:640px">'
      f'<div class="card" style="padding:40px">'
      f'<div style="font-size:30px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;margin-bottom:14px">Job link</div>'
      f'<div style="border:4px solid {INK};border-radius:20px;padding:28px 30px;font-size:40px;background:{CREAM};white-space:nowrap;overflow:hidden">'
      f'<span style="color:{MUTED_TEXT}">Paste a job link</span></div></div></div>'
    + at(80, 990, tick("pointing", 340), right=True)
    + spark(130, 1060, 60, PINK) + spark(250, 1150, 36, COBALT)
    + foot_g(g), 1920)

# 12. IG-shortlist · coral (holiday). Same words as p05_short_list.
g = "coral"
items = ["Pick one job you'd say yes to.", "Paste its link. See your 4 people.", "Send the hiring manager one short note."]
rows = "".join(f'<div style="display:flex;gap:28px;align-items:center;margin-bottom:34px">'
               f'<span style="flex:none;width:70px;height:70px;border:5px solid {INK};border-radius:16px;background:{WHITE}"></span>'
               f'<span style="font-size:46px;font-weight:700;line-height:1.2">{t}</span></div>' for t in items)
out("p05_short_list", "wk48", g,
    stk("Holiday weekend", WHITE, 72, 72)
    + head('Long weekend.<br><span class="fill">Short list.</span>', 190, 136, 72)
    + f'<div class="card" style="position:absolute;left:72px;width:936px;top:560px;padding:46px 46px 16px">{rows}</div>'
    + f'<div style="position:absolute;left:76px;top:1060px;width:600px;font-size:42px;font-weight:700">Then back to the leftovers.</div>'
    + at(64, 990, tick("waving", 200), right=True)
    + spark(940, 96, 64, WHITE) + spark(640, 420, 40, MINT)
    + foot_g(g, bottom=40))

# Extra. IG2 (published Reel, Nov 9) · ink: optional cover swap. Same words as the Reel's first scene.
g = "ink"
out("p13_how_it_works_cover", "wk46", g,
    dial(170, 1500, 400, g)
    + stk("How Day60 works", PINK, 72, 280)
    + head('Paste a job link.<br>Meet the <span class="fill" style="white-space:nowrap">4 people</span> who decide.', 400, 150)
    + spark(880, 330, 80) + spark(960, 980, 54, MINT)
    + tick_says("waving", "Hi, I'm Tick. Here's one job, start to finish.", 1070, 310, 90)
    + foot_g(g), 1920)

if __name__ == "__main__":
    only = sys.argv[1:]
    if only:
        jobs = [j for j in jobs if any(os.path.basename(j["png"]).startswith(n) for n in only)]
    jf = os.path.join(TMP, "jobs.json"); json.dump(jobs, open(jf, "w"))
    subprocess.run(["node", os.path.join(ROOT, "templates", "render_many.js"), jf], check=True)
    print(json.dumps(COVERS, indent=1))
