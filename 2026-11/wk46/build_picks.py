"""Site-pick posts in Day60's design system (HQ "resume" picks, Nov 5).

p15_checker_1-7: /message-checker carousel. A bad and a fixed cold email, both
  invented (sender "Sam", recipient "Dana", company "Northpine"), run through the
  live checker on Nov 5. Real crops in site/: choice cards, Tick's checklist
  (7 to fix, then all 13 pass). The draft itself is set in our own card because
  the site's message box edges are faint.
p16_tick_404: the 404 page ("Tick looked everywhere"), card crop only (no footer).

Crops are re-shot with scratchpad picks/cap.js and p404.js (390px, DSF 3).
Run from repo root: python3 2026-11/wk46/build_picks.py
"""
import html, json, os, subprocess, sys
WK = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(WK))
sys.path.insert(0, os.path.join(ROOT, "design-system"))
from ds import *  # noqa

TMP = os.path.join(WK, "_picks"); os.makedirs(TMP, exist_ok=True)
SITE = os.path.join(WK, "site")
N = 7
jobs = []
EX = (f'<div style="position:absolute;right:72px;top:100px"><span class="sticker" '
      f'style="background:{MUTED};font-size:22px;box-shadow:none">Example · invented message</span></div>')

BAD_SUBJ = "Following up on my application for the Account Executive role at Northpine"
BAD = ("I hope this email finds you well! I wanted to reach out because I recently applied for the Account "
       "Executive position and I am very passionate about sales — I believe I would be a great fit — I have "
       "5 years of experience closing deals and exceeding quota. I'd love to pick your brain sometime. "
       "Looking forward to hearing from you!")
GOOD_SUBJ = "Northpine AE role"
GOOD = ("Hi Dana,\n\nYour team is opening mid-market accounts across Denver this quarter, and the new Account "
        "Executive will own a lot of them. Last year I built a territory like that from zero to $1.2M in signed "
        "contracts, mostly through outbound to operations leaders.\n\nI applied for the role this morning and would "
        "like to show you how I'd plan the first 90 days in that territory. Would a 15-minute call next Tuesday or "
        "Wednesday work for you?\n\nBest,\nSam\n\nIf you're not the right person, a quick 'not me' is a kindness.")


def out(name, body, bg=CREAM):
    p = os.path.join(TMP, name + ".html"); open(p, "w").write(page(body, bg=bg))
    jobs.append({"html": p, "png": os.path.join(WK, name + ".png"), "w": 1080, "h": 1350})


def count(i, dark=False):
    return foot(bottom=56, right=f"{i}/{N}", dark=dark)


def head(n, text, top=200, size=76):
    return (f'<div style="position:absolute;left:72px;top:{top}px;right:72px;display:flex;gap:32px;align-items:center">'
            f'<div class="step d" style="flex:none;width:110px;height:110px;font-size:58px">{n}</div>'
            f'<div class="d" style="font-size:{size}px">{text}</div></div>')


def title(text, top=200, size=88):
    return f'<div class="d" style="position:absolute;left:72px;right:72px;top:{top}px;font-size:{size}px">{text}</div>'


def says(pose, text, top, w=170):
    return (f'<div style="position:absolute;left:72px;right:72px;top:{top}px;display:flex;align-items:flex-end;gap:24px">'
            f'{tick(pose, w, "flex:none")}<div class="bubble left" style="--tail:52px;margin-bottom:{int(w*0.55)}px;font-size:36px">{text}</div></div>')


def shot(fname, top, width=936, left=72):
    src = os.path.join(SITE, fname)
    return (f'<div class="card" style="position:absolute;left:{left}px;top:{top}px;width:{width}px;padding:0;overflow:hidden;background:{WHITE}">'
            f'<img src="file://{src}" style="display:block;width:100%"></div>')


def draft(subj, body, top, size):
    b = html.escape(body).replace("\n", "<br>")
    return (f'<div class="card" style="position:absolute;left:72px;right:72px;top:{top}px;padding:32px 40px;font-size:{size}px;line-height:1.38">'
            f'<div class="lbl" style="font-size:24px;color:{MUTED_TEXT}">Subject</div>'
            f'<div style="font-weight:700;margin-top:6px">{html.escape(subj)}</div>'
            f'<div style="border-top:4px solid {INK};margin:22px 0 20px"></div>{b}</div>')


# 1 cover
out("p15_checker_1",
    f'<div style="position:absolute;left:72px;top:96px"><span class="sticker" style="background:{PINK}">Free tool</span></div>'
    + spark(890, 90, 70) + spark(975, 220, 40, MINT)
    + title('Would Tick let you <span class="fill" style="white-space:nowrap">send it?</span>', 220, 124)
    + f'<div style="position:absolute;left:74px;top:740px;width:560px;font-size:40px;font-weight:700;line-height:1.25">'
      f'One cold email through Day60\'s free message checker. Before and after.</div>'
    + f'<div style="position:absolute;left:72px;top:1000px"><span class="btn" style="font-size:38px;padding:18px 34px">Swipe →</span></div>'
    + f'<div style="position:absolute;right:80px;top:790px">{tick("thinking", 300)}</div>'
    + count(1))

# 2 pick the channel (real crop)
out("p15_checker_2",
    head("01", "Pick what you're sending.", 220)
    + shot("checker_cards.png", 440, 820, 130)
    + says("pointing", "Each one has its own rules.", 1000)
    + count(2))

# 3 the bad draft
out("p15_checker_3",
    EX + head("02", "Paste your draft.", 220)
    + draft(BAD_SUBJ, BAD, 420, 34)
    + says("thinking", "Sound familiar?", 1010, 150)
    + count(3))

# 4 the verdict (real crop)
out("p15_checker_4",
    title('Tick\'s verdict: <span class="fill">7 to fix.</span>', 150, 92)
    + shot("checker_fix.png", 320, 720, 180)
    + says("waiting", "Seven fixes. Each one tells you why.", 1010, 150)
    + count(4))

# 5 the fixed draft
out("p15_checker_5",
    EX + head("03", "Fix it. Check again.", 200)
    + draft(GOOD_SUBJ, GOOD, 380, 28)
    + count(5))

# 6 all pass (real crop)
out("p15_checker_6",
    title('<span class="fill">All 13 rules pass.</span>', 150, 92)
    + shot("checker_pass.png", 300, 660, 210)
    + says("celebrating", "Same ask. Easier to answer.", 1010, 150)
    + count(6))

# 7 CTA (dark)
out("p15_checker_7",
    spark(900, 110, 60, LIME) + spark(960, 980, 50, PINK)
    + f'<div class="d" style="position:absolute;left:72px;right:72px;top:150px;font-size:100px;color:{CREAM}">Check it before<br>you send it.<br><span style="color:{LIME}">Free.</span></div>'
    + f'<div style="position:absolute;left:74px;top:600px;width:620px;font-size:36px;line-height:1.3;color:{CREAM}">'
      f'Tick checks the rules, not the facts. Make sure every detail is true.</div>'
    + f'<div class="card" style="position:absolute;left:72px;top:800px;padding:32px 40px;background:{CREAM};box-shadow:12px 12px 0 {LIME}">'
      f'<div class="d" style="font-size:56px">Message checker</div>'
      f'<div style="font-size:34px;font-weight:700;margin-top:10px">getday60.com/message-checker</div></div>'
    + f'<div class="d" style="position:absolute;left:74px;top:1080px;font-size:40px;color:{CREAM}">Free sprint: link in bio →</div>'
    + f'<div style="position:absolute;right:80px;top:960px">{tick("celebrating", 200)}</div>'
    + count(7, dark=True), bg=D_BG)

# p16 404 (single image, real crop)
out("p16_tick_404",
    f'<div style="position:absolute;left:72px;top:96px"><span class="sticker" style="background:{PINK}">Behind the scenes</span></div>'
    + spark(900, 96, 60) + spark(980, 200, 36, MINT)
    + title('Even our 404 page<br>has a <span class="fill">job to do.</span>', 200, 92)
    + shot("not_found.png", 450, 600, 72)
    + f'<div style="position:absolute;left:712px;right:56px;top:500px;font-size:34px;font-weight:700;line-height:1.3">'
      f'Lost? Tick looked everywhere.<br><br>Then he points you to one thing worth doing: '
      f'<span class="fill" style="white-space:nowrap">a free sprint.</span></div>'
    + foot())

if __name__ == "__main__":
    jf = os.path.join(TMP, "jobs.json"); json.dump(jobs, open(jf, "w"))
    subprocess.run(["node", os.path.join(ROOT, "templates", "render_many.js"), jf], check=True)
