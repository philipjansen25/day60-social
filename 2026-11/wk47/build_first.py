"""Week 47, the first action (HQ brief, Thu Nov 12: paste one job link, see the 4 people, send one message).

p03_one_job_reel.mp4     IG-onejob    Wed Nov 18  "Start with one job."
p04_red_pen_reel.mp4     IG-redpen    Thu Nov 19  "Your first message, cut to 3 lines."
p05_first_job_1-6.png    IG-firstjob  Sat Nov 21  "One job. Four people. One message."

Token-built (design-system/ds.py + reel.py). Invented company and people (Northpine), labeled
"Illustrative example". No "Link in bio" on carousel images, so Facebook can reuse them.

Run from repo root: python3 2026-11/wk47/build_first.py [onejob|redpen|firstjob ...]
"""
import os, sys, tempfile
WK = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(WK))
sys.path.insert(0, os.path.join(ROOT, "design-system"))
from reel import *  # noqa
from grounds import INK_KEYLINES  # noqa

TMP = tempfile.mkdtemp(prefix="wk47_first_")
EX_R = sticker(EXAMPLE, MUTED, 64, 84, 24, right=True)


def rpage(body, bg=CREAM):
    # v2 (HQ, Nov 13): every ink scene gets cream keylines on Tick, cards and stickers.
    return page((INK_KEYLINES if bg == INK else "") + body + foot(dark=(bg == INK)), RW, RH, bg)


# ---------- IG-onejob: Start with one job ----------
TIPS = [("Pick one you'd say yes to tomorrow.", "Not fifty. One you really want."),
        ("Find it on the company's own careers page.", "Saw it on LinkedIn? Look for the same job on their site."),
        ("Paste that one link into Day60.", "See the 4 people closest to the hire.")]


def oj_hook():
    return rpage(
        sticker("Where to start", PINK, 72, 150)
        + f'<div class="d" style="position:absolute;left:72px;right:72px;top:300px;font-size:150px">Don\'t start with 50 jobs.</div>'
        + f'<div class="d" style="position:absolute;left:72px;right:72px;top:820px;font-size:150px"><span class="fill">Start with one.</span></div>'
        + spark(900, 210, 80) + spark(930, 1120, 50, MINT)
        + f'<div style="position:absolute;right:80px;top:1220px">{tick("thinking", 340)}</div>')


def oj_tips(k):
    cards = ""
    for i, (a, b) in enumerate(TIPS[:k], 1):
        cards += (f'<div class="card" style="padding:34px 38px;margin-bottom:40px;display:flex;gap:30px;align-items:flex-start">'
                  f'<div class="step d" style="flex:none;width:96px;height:96px;font-size:52px;box-shadow:6px 6px 0 {INK}">{i}</div>'
                  f'<div><div class="d" style="font-size:58px;line-height:1.02">{a}</div>'
                  f'<div style="font-size:36px;font-weight:600;line-height:1.3;margin-top:14px;color:{MUTED_TEXT}">{b}</div></div></div>')
    return rpage(
        f'<div class="d" style="position:absolute;left:72px;right:72px;top:190px;font-size:104px">Start with <span class="fill">one job.</span></div>'
        + f'<div style="position:absolute;left:72px;right:72px;top:430px">{cards}</div>'
        + (f'<div style="position:absolute;right:80px;top:1420px">{tick("pointing", 230)}</div>' if k < 3 else
           f'<div style="position:absolute;right:80px;top:1400px">{tick("running", 250)}</div>'))


def oj_end():
    return rpage(
        f'<div class="d" style="position:absolute;left:72px;right:72px;top:240px;font-size:132px;color:{CREAM}">One job.<br>Four people.<br>'
        f'<span class="fill" style="color:{INK}">One message.</span></div>'
        + f'<div style="position:absolute;left:76px;top:900px;width:900px;font-size:50px;font-weight:600;line-height:1.3;color:{CREAM}">'
          f'Paste a job link. Get your 4 people. You send every message.</div>'
        + sticker("Link in bio", LIME, 72, 1130, 34)
        + spark(900, 160, 70, LIME)
        + f'<div style="position:absolute;right:80px;top:1240px">{tick("running", 330)}</div>', bg=INK)


ONEJOB = [("oj_hook", oj_hook(), 2.8), ("oj_t1", oj_tips(1), 2.8), ("oj_t2", oj_tips(2), 3.2),
          ("oj_t3", oj_tips(3), 3.2), ("oj_end", oj_end(), 3.4)]

# ---------- IG-redpen: Your first message, cut to 3 lines ----------
LINES = [("Hi Maya,", None),
         ("I hope this finds you well.", False),
         ("I'm very passionate about this opportunity, and I'm a fast learner.", False),
         ("Your posting says new customers take too long to get started.", "What you noticed"),
         ("I've attached my résumé for your consideration.", False),
         ("At my last job, I onboarded new accounts and trained their teams.", "One line of proof"),
         ("Please let me know if there are any opportunities to connect.", False),
         ("Where do new customers get stuck most: setup or training?", "One clear question")]


def rp_hook():
    return rpage(
        sticker("Tick's red pen", PINK, 72, 150)
        + f'<div class="d" style="position:absolute;left:72px;right:72px;top:300px;font-size:156px">Your first message is <span class="fill">too long.</span></div>'
        + spark(900, 220, 80, CORAL)
        + tick_says("pointing", "Watch me cut it to 3 lines.", 1080, 320, 90))


def rp_msg(stage):
    rows = ""
    for text, keep in LINES:
        if keep is None:
            rows += f'<div style="font-size:40px;font-weight:600;margin-bottom:18px">{text}</div>'
        elif keep is False:
            if stage == 0:
                rows += f'<div style="font-size:40px;line-height:1.3;margin-bottom:18px">{text}</div>'
            else:
                rows += (f'<div style="font-size:40px;line-height:1.3;margin-bottom:18px;color:{MUTED_TEXT};'
                         f'text-decoration:line-through;text-decoration-color:{CORAL};text-decoration-thickness:6px">{text}</div>')
        else:
            mark = (f'<span style="background:{LIME};padding:0 8px;border-radius:8px;box-decoration-break:clone;'
                    f'-webkit-box-decoration-break:clone">{text}</span>') if stage == 1 else text
            rows += f'<div style="font-size:40px;line-height:1.3;margin-bottom:18px;font-weight:{700 if stage else 500}">{mark}</div>'
    head = "Before." if stage == 0 else "Cut the filler."
    say = (tick_says("thinking", "Hmm.", 1400, 200, 60, 42) if stage == 0 else
           tick_says("pointing", "Keep what's about them.", 1400, 200, 60, 42))
    return rpage(
        EX_R + f'<div class="d" style="position:absolute;left:72px;right:72px;top:200px;font-size:96px">{head}</div>'
        + f'<div class="card" style="position:absolute;left:72px;right:72px;top:420px;padding:36px 40px">'
          + lbl(f"To Maya Ortiz · Hiring manager, {COMPANY}", 24) + rows + '</div>'
        + say)


def rp_after():
    rows = '<div style="font-size:42px;font-weight:600;margin-bottom:26px">Hi Maya,</div>'
    for text, keep in LINES:
        if isinstance(keep, str):
            rows += (f'<div style="margin-bottom:30px">{lbl(keep, 24)}'
                     f'<div style="font-size:44px;font-weight:700;line-height:1.28">{text}</div></div>')
    return rpage(
        EX_R + f'<div class="d" style="position:absolute;left:72px;right:72px;top:200px;font-size:110px">After: <span class="fill">3 lines.</span></div>'
        + f'<div class="card" style="position:absolute;left:72px;right:72px;top:450px;padding:40px 44px">{rows}</div>'
        + tick_says("celebrating", "Short enough to read. Easy to answer.", 1360, 250, 70, 42))


def rp_end():
    return rpage(
        f'<div class="d" style="position:absolute;left:72px;right:72px;top:260px;font-size:150px;color:{CREAM}">3 lines.<br>'
        f'<span class="fill" style="color:{INK}">Send one today.</span></div>'
        + f'<div style="position:absolute;left:76px;top:820px;width:900px;font-size:48px;font-weight:600;line-height:1.32;color:{CREAM}">'
          f'Day60 drafts a short note to each of the 4 people closest to the hire. Tick checks every draft. You send every message.</div>'
        + sticker("Link in bio", LIME, 72, 1180, 34)
        + spark(910, 170, 70, LIME)
        + f'<div style="position:absolute;right:80px;top:1260px">{tick("celebrating", 320)}</div>', bg=INK)


REDPEN = [("rp_hook", rp_hook(), 2.6), ("rp_msg0", rp_msg(0), 3.4), ("rp_msg1", rp_msg(1), 3.6),
          ("rp_after", rp_after(), 3.8), ("rp_end", rp_end(), 3.4)]

# ---------- IG-firstjob: carousel, 6 slides ----------
N = 6
FOOT = foot()


def counter(n, dark=False):
    return (f'<div style="position:absolute;right:72px;top:84px;font-size:30px;font-weight:700;'
            f'color:{D_MUTED_TEXT if dark else MUTED_TEXT}">{n} / {N}</div>')


def slide_head(num, n, head, size=88):
    return (f'<div class="step" style="position:absolute;left:72px;top:72px"><span class="d">{num}</span></div>' + counter(n)
            + f'<div class="d" style="position:absolute;left:72px;top:230px;width:936px;font-size:{size}px">{head}</div>')


DRAFT = ("Hi Maya, your posting says new customers take too long to get started. "
         "At my last job, I onboarded new accounts and trained their teams. "
         "Where do new customers get stuck most: setup or training?")
CHECKS = ["Asks one clear question", "The question comes last", "Fits the length limit", "No links"]


def fj_slides():
    s = []
    s.append(("p05_first_job_1", page(
        sticker("Save this", WHITE, 72, 72)
        + f'<div class="d" style="position:absolute;left:72px;top:200px;width:936px;font-size:124px">One job. Four people. One message.</div>'
        + f'<div style="position:absolute;left:76px;top:780px;width:560px;font-size:46px;font-weight:700;line-height:1.2">'
          f'Your first job in Day60, step by step.</div>'
        + f'<div style="position:absolute;right:60px;top:700px">{tick("running", 320)}</div>'
        + spark(880, 110, 70, WHITE) + FOOT, bg=LIME)))
    job = (f'<div class="card" style="margin-top:34px;padding:28px 34px;display:flex;align-items:center;gap:26px">'
           f'<div class="d" style="flex:none;width:88px;height:88px;border:4px solid {INK};border-radius:22px;background:{MINT};'
           f'display:flex;align-items:center;justify-content:center;font-size:50px">N</div>'
           f'<div><div class="d" style="font-size:50px">{JOB}</div>'
           f'<div style="font-size:32px;color:{MUTED_TEXT};margin-top:6px">{COMPANY} · Remote</div></div></div>')
    s.append(("p05_first_job_2", page(
        slide_head("01", 2, "Paste one job link.")
        + sticker(EXAMPLE, PINK, 72, 370, 24)
        + f'<div style="position:absolute;left:72px;width:936px;top:460px">'
          f'<div class="card" style="padding:34px 36px">{lbl("Job link", 26, INK)}'
          f'<div style="border:4px solid {INK};border-radius:20px;padding:22px 26px;font-size:31px;background:{CREAM};'
          f'white-space:nowrap;overflow:hidden">{JOB_URL}</div></div>{job}</div>'
        + f'<div class="bubble down" style="position:absolute;left:72px;top:960px;width:640px;font-size:36px;--tail:520px">'
          f'Use the link from the company\'s own site.</div>'
        + f'<div style="position:absolute;right:70px;top:1000px">{tick("pointing", 190)}</div>'
        + FOOT)))
    rows = "".join(person_row(p, 0.82, True, 20) for p in PEOPLE)
    s.append(("p05_first_job_3", page(
        slide_head("02", 3, "Meet your 4 people.")
        + sticker(EXAMPLE, PINK, 72, 360, 24)
        + f'<div style="position:absolute;left:72px;width:936px;top:440px">{rows}</div>'
        + foot(bottom=40))))
    s.append(("p05_first_job_4", page(
        slide_head("03", 4, "Start with the hiring manager.")
        + sticker(EXAMPLE, PINK, 72, 450, 24)
        + f'<div style="position:absolute;left:72px;width:936px;top:540px">{person_row(PEOPLE[0], 0.95, True, 0)}</div>'
        + f'<div style="position:absolute;left:76px;top:800px;width:660px;font-size:40px;font-weight:600;line-height:1.3">'
          f'The hiring manager feels the empty seat. Day60 drafts a short note to Maya, in your voice.</div>'
        + f'<div style="position:absolute;right:64px;top:820px">{tick("thinking", 220)}</div>'
        + FOOT)))
    items = "".join(f'<div style="display:flex;gap:14px;align-items:center;font-size:28px;font-weight:700;margin-top:12px">'
                    f'{check(36)}{c}</div>' for c in CHECKS)
    s.append(("p05_first_job_5", page(
        slide_head("04", 5, "Make it yours. Send it.", 84)
        + sticker(EXAMPLE, PINK, 72, 440, 24)
        + f'<div class="card" style="position:absolute;left:72px;width:936px;top:520px;padding:30px 36px">'
          + lbl("Draft to Maya Ortiz", 22) + f'<div style="font-size:34px;line-height:1.36">{DRAFT}</div></div>'
        + f'<div style="position:absolute;left:76px;top:900px;width:600px">{items}</div>'
        + f'<div style="position:absolute;left:76px;top:1110px;width:640px;font-size:34px;font-weight:700;line-height:1.25">'
          f'Tick checks every draft. You send it. Day60 never sends anything.</div>'
        + f'<div style="position:absolute;right:64px;top:930px">{tick("celebrating", 230)}</div>'
        + foot(bottom=40))))
    # v2 (HQ, Nov 13): cream keylines on ink; the old p05_first_job_6.png stays on disk.
    s.append(("p05_first_job_6_v2", page(
        INK_KEYLINES + counter(6, True)
        + f'<div class="d" style="position:absolute;left:72px;top:170px;width:936px;font-size:130px;color:{CREAM}">'
          f'That\'s day 0.</div>'
        + f'<div style="position:absolute;left:76px;top:360px;width:900px;font-size:42px;font-weight:600;line-height:1.32;color:{CREAM}">'
          f'Day60 drafts the hiring manager\'s day-2 connection note and the day-7 follow-up when they\'re due. You send every one.</div>'
        + f'<div class="d" style="position:absolute;left:72px;top:690px;width:640px;font-size:76px;color:{CREAM}">'
          f'Paste a job link.<br><span class="fill" style="color:{INK}">Get your 4 people.</span></div>'
        + sticker("getday60.com", LIME, 72, 960, 30)
        + f'<div style="position:absolute;right:60px;top:760px">{tick("running", 280)}</div>'
        + spark(900, 120, 64, LIME)
        + foot(dark=True), bg=INK)))
    return s


if __name__ == "__main__":
    # Modes: onejob, redpen, firstjob. Any other argument is a slide name to render alone (e.g. p05_first_job_6_v2).
    # The _v2 reels (HQ, Nov 13) only change the ink end scene; the old mp4s stay on disk.
    args = set(sys.argv[1:])
    names = {a for a in args if a.startswith("p0")}
    want = (args - names) or ({"firstjob"} if names else {"onejob", "redpen", "firstjob"})
    if "onejob" in want:
        make_reel(ONEJOB, os.path.join(WK, "p03_one_job_reel_v2.mp4"), os.path.join(TMP, "onejob"))
    if "redpen" in want:
        make_reel(REDPEN, os.path.join(WK, "p04_red_pen_reel_v2.mp4"), os.path.join(TMP, "redpen"))
    if "firstjob" in want:
        jobs = []
        for name, html in fj_slides():
            if names and name not in names:
                continue
            p = os.path.join(TMP, name + ".html"); open(p, "w").write(html)
            jobs.append({"html": p, "png": os.path.join(WK, name + ".png"), "w": 1080, "h": 1350})
        render(jobs, TMP)
