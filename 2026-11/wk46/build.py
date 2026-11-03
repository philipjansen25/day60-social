"""Build week 46 (Nov 8-14, 2026) images: 'What Day60 is / isn't'.

python3 2026-11/wk46/build.py <scratch_dir>
Writes HTML to <scratch_dir>/html, a jobs.json for templates/render_many.js,
and PNGs into this folder (feed) or <scratch_dir>/scenes (Reel scenes).
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'templates'))
from brand import *  # noqa

SCR = sys.argv[1]
os.makedirs(f'{SCR}/html', exist_ok=True)
os.makedirs(f'{SCR}/scenes', exist_ok=True)
jobs = []


def out(name, html, w=1080, h=1350, scene=False, transparent=False):
    hp = f'{SCR}/html/{name}.html'
    open(hp, 'w').write(html)
    png = f'{SCR}/scenes/{name}.png' if scene else f'{HERE}/{name}.png'
    jobs.append({'html': hp, 'png': png, 'w': w, 'h': h, 'transparent': transparent})


def counter(i, n):
    return foot(right=f'{i}/{n}')


# ---------- P01 IG carousel (pinned): What Day60 is / isn't, 7 slides ----------
N = 7
out('p01_is_isnt_1', page(
    spark(880, 96, 64, CORAL) + spark(962, 220, 38, BLUE) +
    f'<div class="pill" style="position:absolute;left:72px;top:96px;background:{CREAM}">THE SHORT VERSION</div>'
    f'<div class="bg" style="position:absolute;left:72px;top:250px;width:930px;font-size:128px;line-height:.98">'
    f'What Day60 <span class="hl">is.</span><br>And what it <span class="hl" style="background:{CORAL}">isn\'t.</span></div>'
    f'<div style="position:absolute;left:74px;top:740px;width:560px;font-size:38px;font-weight:700;line-height:1.25">'
    f'Five slides. No jargon. Save it for the next time someone asks.</div>'
    f'<div class="bg" style="position:absolute;left:74px;top:1060px;font-size:44px">Swipe &rarr;</div>'
    + tick(700, 820, 290) + counter(1, N), bg=LIME))


def is_slide(i, ok, title, body, extra=''):
    lab = ('IT IS', LIME) if ok else ("IT ISN'T", CORAL)
    return page(
        spark(930, 100, 52, BLUE if ok else CORAL) +
        f'<div style="position:absolute;left:72px;top:96px;display:flex;gap:22px;align-items:center">'
        f'{mark(ok)}<div class="pill" style="background:{lab[1]}">{lab[0]}</div></div>'
        f'<div class="bg" style="position:absolute;left:72px;top:250px;width:930px;font-size:104px;line-height:1">{title}</div>'
        f'<div style="position:absolute;left:74px;top:540px;width:880px;font-size:44px;line-height:1.32;font-weight:500">{body}</div>'
        + tick(760, 880, 220) + extra + counter(i, N))


out('p01_is_isnt_2', is_slide(2, True, 'A 60-day job-search sprint.',
    'Pick up to 3 new jobs a day, up to 60 in a sprint. A plan with a start, a finish and a job for every day.'))
out('p01_is_isnt_3', is_slide(3, True, 'The 4 people closest to the hire.',
    'For every job: the hiring manager, their boss, an internal champion and the recruiter. Verified work emails where available.'))
out('p01_is_isnt_4', is_slide(4, True, 'A short note, in your voice.',
    'Tick checks every draft against the writing rules. Then you hit send. Three touches per person, max: day 0, day 2, day 7.'))
out('p01_is_isnt_5', is_slide(5, False, 'An auto-apply bot.',
    'Day60 never applies for you and never sends anything. Every message goes out from you, to one person, on purpose.'))
out('p01_is_isnt_6', is_slide(6, False, 'A LinkedIn hack.',
    'It never logs in to LinkedIn, scrapes it or automates it. No mass messages. No keyword stuffing.'))
out('p01_is_isnt_7', page(
    spark(900, 110, 60, LIME) +
    f'<div class="bg" style="position:absolute;left:72px;top:150px;width:930px;font-size:86px;line-height:1.02;color:{CREAM}">'
    f'Keep your tracker and your résumé tool.</div>'
    f'<div class="bg" style="position:absolute;left:72px;top:440px;width:930px;font-size:86px;line-height:1.02;color:{LIME}">'
    f'Day60 is the part after you find the job.</div>'
    f'<div class="box" style="position:absolute;left:72px;top:800px;padding:28px 36px;background:{CREAM};box-shadow:10px 10px 0 {LIME}">'
    f'<div class="bg" style="font-size:52px">Day60 Sprint. Free.</div>'
    f'<div style="font-size:34px;font-weight:700;margin-top:8px">No card. Nothing to cancel.</div></div>'
    f'<div class="bg" style="position:absolute;left:74px;top:1090px;font-size:44px;color:{CREAM}">Link in bio &rarr;</div>'
    + spark(830, 930, 90, LIME) + spark(950, 1060, 50, PINK) +
    f'<div class="foot"><div class="logo bg" style="color:{CREAM}">{LOGO_SVG}Day60</div>'
    f'<div class="url" style="color:{CREAM}">7/7</div></div>', bg=INK))

# ---------- P02 single card: is / isn't columns (FB pinned + LinkedIn featured) ----------
rows_is = ['A 60-day sprint', 'The 4 people closest to the hire', 'A short note in your voice', 'You hit send']
rows_not = ['An auto-apply bot', 'A LinkedIn login', 'Mass messages', 'Keyword stuffing']


def col(x, title, rows, ok, bgc):
    items = ''.join(f'<div style="display:flex;gap:18px;align-items:center;margin-top:26px;font-size:36px;'
                    f'font-weight:700;line-height:1.15">{mark(ok)}<span>{r}</span></div>' for r in rows)
    return (f'<div class="box" style="position:absolute;left:{x}px;top:330px;width:440px;height:620px;'
            f'padding:34px 30px;background:{bgc}"><div class="bg" style="font-size:62px">{title}</div>{items}</div>')


out('p02_is_isnt_card', page(
    spark(900, 96, 60, CORAL) + spark(975, 210, 36, BLUE) +
    f'<div class="pill" style="position:absolute;left:72px;top:96px;background:{LIME}">DAY60, IN ONE PICTURE</div>'
    f'<div class="bg" style="position:absolute;left:72px;top:190px;font-size:84px">Is. Isn\'t.</div>'
    + col(72, 'It is', rows_is, True, WHITE) + col(560, "It isn't", rows_not, False, WHITE) +
    f'<div class="bg" style="position:absolute;left:72px;top:1010px;width:936px;font-size:48px;line-height:1.05">'
    f'Every other tool makes applying faster. <span style="background:{LIME};padding:0 8px">Day60 gets you to the person who decides.</span></div>'
    + foot()))

# ---------- P03 FB A/B: spray and pray vs prospecting ----------
out('p03_two_ways', page(
    spark(910, 96, 60, BLUE) +
    f'<div class="bg" style="position:absolute;left:72px;top:96px;width:900px;font-size:100px;line-height:.98">Two ways to spend tonight.</div>'
    f'<div class="box" style="position:absolute;left:72px;top:400px;width:936px;padding:34px 40px;background:{WHITE}">'
    f'<div class="pill" style="background:{CORAL};font-size:24px">&#10005; SPRAY AND PRAY</div>'
    f'<div style="font-size:44px;font-weight:700;margin-top:26px;line-height:1.2">Apply to 50 jobs. Refresh your inbox. Wait.</div></div>'
    f'<div class="box" style="position:absolute;left:72px;top:690px;width:936px;padding:34px 40px;background:{LIME}">'
    f'<div class="pill" style="background:{CREAM};font-size:24px">&#10003; PROSPECT</div>'
    f'<div style="font-size:44px;font-weight:700;margin-top:26px;line-height:1.2">Pick 3 jobs. Find the 4 people closest to each hire. Send each a short note about their problem.</div></div>'
    f'<div class="bg" style="position:absolute;left:72px;top:1080px;font-size:52px">Which one is your week?</div>'
    f'<div style="position:absolute;left:74px;top:1150px;font-size:24px;opacity:.8">Illustrative example.</div>'
    + foot()))

# ---------- P04 FB flow: where Day60 fits ----------
steps = [('Find the job', 'your job board', False), ('Tailor your résumé', 'your résumé tool', False),
         ('Track it', 'your tracker', False), ('Reach the people who decide', 'Day60', True)]
flow = ''
for k, (a, b, me) in enumerate(steps):
    y = 300 + k * 205
    bgc = LIME if me else WHITE
    flow += (f'<div class="box" style="position:absolute;left:72px;top:{y}px;width:936px;height:160px;padding:0 36px;'
             f'background:{bgc};display:flex;align-items:center;justify-content:space-between">'
             f'<div style="display:flex;align-items:center;gap:26px"><div class="bg" style="font-size:64px;width:50px">{k+1}</div>'
             f'<div style="font-size:42px;font-weight:700">{a}</div></div>'
             f'<div class="{"bg" if me else ""}" style="font-size:{44 if me else 32}px;font-weight:700;opacity:{1 if me else .75}">{b}</div></div>')
    if k < 3:
        flow += f'<div style="position:absolute;left:150px;top:{y+165}px;font-size:34px;font-weight:700">&darr;</div>'
out('p04_where_it_fits', page(
    spark(910, 96, 60, CORAL) +
    f'<div class="bg" style="position:absolute;left:72px;top:110px;font-size:110px">Where Day60 fits.</div>'
    + flow +
    f'<div style="position:absolute;left:74px;top:1135px;width:930px;font-size:36px;font-weight:700;line-height:1.25">'
    f'Keep your tools. Day60 is the part after you find the job.</div>'
    + foot()))

# ---------- P05 LinkedIn: 722 applicants ----------
out('p05_722', page(
    spark(890, 96, 64, CORAL) + spark(965, 225, 38, BLUE) +
    f'<div class="pill" style="position:absolute;left:72px;top:96px;background:{LIME}">FROM THE HIRING SIDE</div>'
    f'<div class="box bg" style="position:absolute;left:72px;top:250px;padding:0 44px 18px;background:{LIME};font-size:300px;line-height:1">722</div>'
    f'<div class="bg" style="position:absolute;left:72px;top:620px;width:930px;font-size:82px;line-height:1.02">applicants in 24 hours.</div>'
    f'<div style="position:absolute;left:74px;top:760px;width:640px;font-size:42px;font-weight:700;line-height:1.25">'
    f'The ones that got answered: 9 cold calls and 16 emails.</div>'
    f'<div class="bg" style="position:absolute;left:72px;top:1040px;font-size:56px;line-height:1.02">Stop applying.<br>Start prospecting.</div>'
    f'<div style="position:absolute;left:74px;top:1180px;font-size:24px;opacity:.85">Philip\'s 2023 hiring story.</div>'
    + tick(740, 850, 250) + foot()))

# ---------- P06 IG carousel + LinkedIn PDF: 3 touches, 6 slides ----------
N6 = 6
out('p06_three_touches_1', page(
    spark(880, 96, 64, CORAL) + spark(962, 220, 38, BLUE) +
    f'<div class="pill" style="position:absolute;left:72px;top:96px;background:{CREAM}">SAVE THIS</div>'
    f'<div class="bg" style="position:absolute;left:72px;top:250px;width:930px;font-size:150px;line-height:.96">'
    f'3 touches.<br><span class="hl" style="background:{CREAM}">Then stop.</span></div>'
    f'<div style="position:absolute;left:74px;top:700px;width:560px;font-size:40px;font-weight:700;line-height:1.25">'
    f'The follow-up rhythm that\'s persistent, not pushy.</div>'
    f'<div class="bg" style="position:absolute;left:74px;top:1060px;font-size:44px">Swipe &rarr;</div>'
    + tick(700, 820, 290) + counter(1, N6), bg=LIME))


def touch(i, day, title, body):
    return page(
        spark(930, 100, 52, BLUE) +
        f'<div class="box bg" style="position:absolute;left:72px;top:96px;padding:6px 30px 14px;background:{LIME};font-size:76px">{day}</div>'
        f'<div class="bg" style="position:absolute;left:72px;top:300px;width:930px;font-size:100px;line-height:1">{title}</div>'
        f'<div style="position:absolute;left:74px;top:450px;width:880px;font-size:44px;line-height:1.32;font-weight:500">{body}</div>'
        + tick(760, 880, 220) + counter(i, N6))


out('p06_three_touches_2', touch(2, 'Day 0', 'The first note.',
    'Their problem, one line of proof, one easy ask. Short enough to read on a phone between meetings.'))
out('p06_three_touches_3', touch(3, 'Day 2', 'The nudge.',
    'Two lines. Add something new: a number, a link, a sharper question. Never "just following up."'))
out('p06_three_touches_4', touch(4, 'Day 7', 'The last word.',
    'Close the loop kindly and leave the door open. People remember who made it easy to say no.'))
out('p06_three_touches_5', page(
    spark(900, 110, 60, CORAL) +
    f'<div class="bg" style="position:absolute;left:72px;top:200px;width:930px;font-size:130px;line-height:.98">Then stop.</div>'
    f'<div style="position:absolute;left:74px;top:420px;width:880px;font-size:46px;line-height:1.3;font-weight:700">'
    f'Three touches is persistence. Ten is spam.</div>'
    f'<div style="position:absolute;left:74px;top:600px;width:620px;font-size:40px;line-height:1.3;font-weight:500">'
    f'Day60 keeps it to 3 touches per person: day 0, day 2, day 7. Across four people, that\'s plenty of chances to be the one who got answered.</div>'
    + tick(720, 840, 260) + counter(5, N6)))
out('p06_three_touches_6', page(
    spark(900, 110, 60, LIME) +
    f'<div class="bg" style="position:absolute;left:72px;top:170px;width:930px;font-size:96px;line-height:1;color:{CREAM}">'
    f'Four people. Three touches. <span style="color:{LIME}">You send every one.</span></div>'
    f'<div class="box" style="position:absolute;left:72px;top:640px;padding:28px 36px;background:{CREAM};box-shadow:10px 10px 0 {LIME}">'
    f'<div class="bg" style="font-size:52px">Try one job free.</div>'
    f'<div style="font-size:34px;font-weight:700;margin-top:8px">getday60.com/try · No account needed.</div></div>'
    + spark(830, 930, 90, LIME) + spark(950, 1060, 50, PINK) +
    f'<div class="foot"><div class="logo bg" style="color:{CREAM}">{LOGO_SVG}Day60</div>'
    f'<div class="url" style="color:{CREAM}">6/6</div></div>', bg=INK))

# ---------- Reel scenes (1080x1920) ----------
W, H = 1080, 1920


def reel_foot(dark=False):
    if dark:
        return (f'<div class="foot" style="bottom:300px"><div class="logo bg" style="color:{CREAM}">{LOGO_SVG}Day60</div>'
                f'<div class="url" style="color:{CREAM}">getday60.com</div></div>')
    return foot(bottom=300)


def scene(name, body, bg=CREAM):
    out(name, page(body + reel_foot(bg == INK), W, H, bg), W, H, scene=True)


# R2: auto-apply vs Day60 (IG Wed)
scene('r2_s1', spark(860, 260, 70, CORAL) +
      f'<div class="bg" style="position:absolute;left:80px;top:520px;width:920px;font-size:120px;line-height:1">Auto-apply bots make applying faster.</div>')
pile = ''.join(f'<div class="box" style="position:absolute;left:{300+(k%2)*24}px;top:{1180-k*58}px;width:480px;height:110px;'
               f'background:{WHITE};transform:rotate({(-4,3,-2,5,-3,2,-5,4)[k]}deg);box-shadow:6px 6px 0 {INK}"></div>' for k in range(8))
scene('r2_s2', f'<div class="bg" style="position:absolute;left:80px;top:300px;width:920px;font-size:120px;line-height:1">Faster into the same pile.</div>' + pile)
scene('r2_s3', tick(380, 900, 320) +
      f'<div class="bg" style="position:absolute;left:80px;top:420px;width:920px;font-size:130px;line-height:1">Day60 does the other thing.</div>', bg=LIME)
scene('r2_s4', spark(880, 260, 60, BLUE) +
      f'<div class="bg" style="position:absolute;left:80px;top:380px;width:920px;font-size:112px;line-height:1">'
      f'Up to 3 jobs a day.<br><span class="hl">4 people</span> closest to each hire.</div>'
      f'<div style="position:absolute;left:84px;top:900px;width:880px;font-size:46px;font-weight:700;line-height:1.3">'
      f'The hiring manager. Their boss. An internal champion. The recruiter.</div>')
scene('r2_s5', spark(880, 260, 60, CORAL) +
      f'<div class="bg" style="position:absolute;left:80px;top:420px;width:920px;font-size:112px;line-height:1">'
      f'A short note to each, in your voice.</div>'
      f'<div class="box bg" style="position:absolute;left:80px;top:900px;padding:14px 40px 24px;background:{LIME};font-size:100px">You hit send.</div>')
scene('r2_s6', spark(800, 1150, 110, LIME) + spark(950, 1300, 56, PINK) +
      f'<div class="bg" style="position:absolute;left:80px;top:330px;width:920px;font-size:92px;line-height:1.02;color:{CREAM}">'
      f'Every other tool makes applying faster.</div>'
      f'<div class="bg" style="position:absolute;left:80px;top:640px;width:920px;font-size:92px;line-height:1.02;color:{LIME}">'
      f'Day60 gets you to the person who decides.</div>'
      f'<div style="position:absolute;left:84px;top:1110px;font-size:44px;font-weight:700;color:{CREAM};line-height:1.35">'
      f'Day60 Sprint. Free.<br>No card. Link in bio.</div>', bg=INK)

# R3: things Day60 will never do (FB Mon, IG Sat)
nevers = ['Apply for you', 'Send a message without you', 'Log in to your LinkedIn',
          'Mass-message strangers', 'Stuff your résumé with keywords', 'Ask for your card']


def never_scene(k):
    items = ''.join(f'<div style="display:flex;gap:24px;align-items:center;margin-top:30px;font-size:52px;font-weight:700;'
                    f'opacity:{1 if j <= k else 0}">{mark(False)}<span>{t}</span></div>' for j, t in enumerate(nevers))
    return (spark(880, 250, 64, CORAL) +
            f'<div class="bg" style="position:absolute;left:80px;top:330px;width:920px;font-size:104px;line-height:1">'
            f'Things Day60 will <span class="hl" style="background:{CORAL}">never</span> do:</div>'
            f'<div style="position:absolute;left:84px;top:620px;width:920px">{items}</div>')


scene('r3_s0', never_scene(-1))
for k in range(len(nevers)):
    scene(f'r3_s{k+1}', never_scene(k))
scene('r3_s7', tick(700, 1080, 260) +
      f'<div class="pill" style="position:absolute;left:80px;top:300px;background:{LIME}">WHAT IT DOES</div>'
      f'<div class="bg" style="position:absolute;left:80px;top:420px;width:920px;font-size:96px;line-height:1.02">'
      f'Finds the 4 people closest to the hire. Drafts a note to each.</div>'
      f'<div class="box bg" style="position:absolute;left:80px;top:860px;padding:14px 40px 24px;background:{LIME};font-size:88px">You send it.</div>'
      f'<div style="position:absolute;left:84px;top:1130px;font-size:44px;font-weight:700;line-height:1.35">'
      f'Stop applying.<br>Start prospecting.</div>')

# R1: /try demo frame + captions (video composited later with ffmpeg)
VX, VY, VW, VH = 150, 470, 780, 1387  # where the scaled recording sits


def r1_frame(caption, n):
    return page(
        spark(900, 130, 58, CORAL) +
        f'<div class="bg" style="position:absolute;left:80px;top:230px;width:860px;font-size:76px;line-height:1.02">{caption}</div>'
        f'<div style="position:absolute;left:{VX-8}px;top:{VY-8}px;width:{VW+16}px;height:{VH+16}px;'
        f'border:8px solid {INK};border-radius:34px;box-shadow:14px 14px 0 {INK};background:transparent"></div>',
        W, H, 'transparent')


caps = ['Paste any job link.', 'The 4 people closest to the hire. In seconds.', 'Add your details. Day60 drafts the note.']
for n, cap in enumerate(caps):
    out(f'r1_cap{n}', r1_frame(cap, n), W, H, scene=True, transparent=True)
scene('r1_end', tick(700, 1060, 260) +
      f'<div class="pill" style="position:absolute;left:80px;top:300px;background:{CORAL}">NOT AN AUTO-APPLY BOT</div>'
      f'<div class="bg" style="position:absolute;left:80px;top:420px;width:920px;font-size:104px;line-height:1">'
      f'You send every message.</div>'
      f'<div class="box" style="position:absolute;left:80px;top:760px;padding:28px 36px;background:{LIME}">'
      f'<div class="bg" style="font-size:60px">Try one job free.</div>'
      f'<div style="font-size:36px;font-weight:700;margin-top:8px">No account. Link in bio.</div></div>')

json.dump(jobs, open(f'{SCR}/jobs.json', 'w'))
print(len(jobs), 'jobs')
