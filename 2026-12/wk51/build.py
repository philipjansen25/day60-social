"""Week 51 Instagram cards, drafts for HQ (Social, Nov 27; HQ's Thursday verdict: more resume-tool posts,
message craft, about 1 in 4 humor). None says "Link in bio", so Facebook reuses each card as it is.

2026-12/wk51/p01_one_bullet_coral.png     IG-bullet    Tue Dec 15  resume builder: one bullet, one result
2026-12/wk51/p02_word_file_cobalt.png     IG-wordfile  Wed Dec 16  resume builder: add your email, get a Word file
2026-12/wk51/p03_dear_team_pink.png       IG-dearteam  Fri Dec 18  humor: "Dear Hiring Team" reaches no one
2026-12/wk51/p04_phone_screen_mint.png    IG-phonetest Sat Dec 19  message craft: the phone-screen test
2026-12/wk51/p05_wishlist_ink.png         IG-wishlist  Sun Dec 20  humor, seasonal: Tick's holiday wish list

Replaced Nov 27 (main thread) so week 51 doesn't repeat week 50's angles.
Grid: Mon cream (IG4-r2), Tue coral, Wed cobalt, Thu lime (IG-firstjob-r2), Fri pink, Sat mint, Sun ink:
any 4 in a row differ. One lime element per card; lime is never text.

Run from repo root: python3 2026-12/wk51/build.py [names to render, default all]
"""
import json, os, subprocess, sys, tempfile
WK = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(WK))
sys.path.insert(0, os.path.join(ROOT, "design-system"))
from grounds import *  # noqa

TMP = tempfile.mkdtemp(prefix="wk51_")
jobs = []


def out(name, html):
    p = os.path.join(TMP, name + ".html"); open(p, "w").write(html)
    jobs.append({"html": p, "png": os.path.join(WK, name + ".png"), "w": 1080, "h": 1350})


def at(x, y, html, right=False):
    return f'<div style="position:absolute;{"right" if right else "left"}:{x}px;top:{y}px">{html}</div>'


def stk(text, bg, x, y, size=28):
    return at(x, y, f'<span class="sticker" style="background:{bg};font-size:{size}px">{text}</span>')


RB = "getday60.com/resume-builder"

# IG-bullet · coral (ink text only). The lime highlight is the one lime element.
g = "coral"
out("p01_one_bullet_coral", cover_page(
    stk("Free resume builder", WHITE, 72, 72)
    + f'<div class="d" style="position:absolute;left:72px;right:72px;top:200px;font-size:132px">One bullet, one result.</div>'
    + f'<div class="card muted" style="position:absolute;left:72px;top:500px;width:640px;padding:24px 34px;'
      f'font-size:32px;font-weight:600;line-height:1.3"><div class="lbl" style="font-size:24px;letter-spacing:.06em">FROM THE RESUME</div>'
      f'Trained staff at new accounts on the ordering system.</div>'
    + f'<div class="card" style="position:absolute;left:72px;top:720px;width:640px;padding:24px 34px;'
      f'font-size:32px;font-weight:700;line-height:1.3"><div class="lbl" style="font-size:24px;letter-spacing:.06em">FOR THIS JOB</div>'
      f'Onboarded new accounts and trained their teams.</div>'
    + f'<div style="position:absolute;left:74px;top:930px;width:640px;font-size:34px;font-weight:700;line-height:1.3">'
      f'No new skill, number or title.<br><span class="fill" style="color:{INK}">Only what\'s true.</span></div>'
    + f'<div style="position:absolute;left:74px;top:1060px;font-size:26px;font-weight:700">Illustrative example</div>'
    + at(40, 600, tick("pointing", 250), right=True)
    + spark(900, 110, 60, WHITE) + spark(990, 220, 34, INK)
    + foot_g(g, right=RB), g))

# IG-wordfile · cobalt (white text). The lime sticker is the one lime element.
g = "cobalt"
out("p02_word_file_cobalt", cover_page(
    stk("Free resume builder", LIME, 72, 72)
    + f'<div class="d c" style="position:absolute;left:72px;right:72px;top:200px;font-size:124px">Add your email. Get a Word file.</div>'
    + f'<div class="card" style="position:absolute;left:72px;top:640px;width:620px;padding:32px 38px;'
      f'font-size:42px;font-weight:700;line-height:1.3">Free. No account. Your resume isn\'t stored.</div>'
    + f'<div class="c" style="position:absolute;left:74px;top:900px;width:600px;font-size:38px;font-weight:600;line-height:1.3">'
      f'One job, one tailored resume, one file you can edit.</div>'
    + at(56, 620, tick("celebrating", 290), right=True)
    + spark(900, 110, 60, WHITE) + spark(990, 220, 34, PINK)
    + foot_g(g, right=RB), g))

# IG-dearteam · pink, humor. The lime highlight is the one lime element.
g = "pink"
out("p03_dear_team_pink", cover_page(
    stk("Mailbag", WHITE, 72, 72)
    + f'<div class="d" style="position:absolute;left:72px;right:72px;top:200px;font-size:130px">“Dear Hiring Team,”</div>'
    + f'<div style="position:absolute;left:74px;top:520px;width:600px;font-size:44px;font-weight:700;line-height:1.24">'
      f'People on the Hiring Team who think it\'s for them: zero.</div>'
    + f'<div class="card" style="position:absolute;left:72px;top:820px;width:620px;padding:32px 38px;'
      f'font-size:42px;font-weight:700;line-height:1.4">Write to one person,<br>'
      f'<span class="fill" style="color:{INK}">by name.</span></div>'
    + at(56, 600, tick("pointing", 290), right=True)
    + spark(900, 110, 64, WHITE) + spark(990, 230, 36, INK)
    + foot_g(g), g))

# IG-phonetest · mint. The lime highlight is the one lime element.
g = "mint"
out("p04_phone_screen_mint", cover_page(
    stk("Message craft", WHITE, 72, 72)
    + f'<div class="d" style="position:absolute;left:72px;right:72px;top:200px;font-size:112px">The phone-screen test.</div>'
    + f'<div style="position:absolute;left:74px;top:520px;width:600px;font-size:44px;font-weight:700;line-height:1.24">'
      f'Read your message on your phone. If you have to scroll, cut it.</div>'
    + f'<div class="card" style="position:absolute;left:72px;top:820px;width:620px;padding:32px 38px;'
      f'font-size:42px;font-weight:700;line-height:1.3">A first note fits on one screen. '
      f'<span class="fill" style="color:{INK}">No scrolling.</span></div>'
    + at(56, 600, tick("pointing", 290), right=True)
    + spark(900, 110, 60, WHITE) + spark(990, 220, 34, INK)
    + foot_g(g), g))

# IG-wishlist · ink, humor, seasonal. The lime highlight is the one lime element.
g = "ink"
out("p05_wishlist_ink", cover_page(
    stk("Holiday edition", PINK, 72, 72)
    + f'<div class="d c" style="position:absolute;left:72px;right:72px;top:200px;font-size:122px">Tick\'s holiday<br>wish list</div>'
    + f'<div class="card" style="position:absolute;left:72px;top:560px;width:640px;padding:36px 42px;'
      f'font-size:44px;font-weight:700;line-height:1.5">1. Short notes.<br>'
      f'2. <span class="fill" style="color:{INK}">One easy question.</span><br>'
      f'3. Never “just following up.”</div>'
    + f'<div class="c" style="position:absolute;left:74px;top:960px;width:600px;font-size:38px;font-weight:600;line-height:1.3">'
      f'Your next message can tick all three.</div>'
    + at(60, 620, tick("celebrating", 290), right=True)
    + spark(900, 110, 64, PINK) + spark(990, 230, 36, MINT)
    + foot_g(g), g))

if __name__ == "__main__":
    only = sys.argv[1:]
    if only:
        jobs = [j for j in jobs if os.path.basename(j["png"])[:-4] in only]
    jf = os.path.join(TMP, "jobs.json"); json.dump(jobs, open(jf, "w"))
    subprocess.run(["node", os.path.join(ROOT, "templates", "render_many.js"), jf], check=True)
