"""Week 48 (Sun Nov 22 - Sat Nov 28, Thanksgiving Thu Nov 26). HQ brief, Thu Nov 12: the first action.

p01_thanks_1-6.png       IG-thanks     Sun Nov 22  (FB-thanks reuses it, Thu Nov 26)  "Send one thank-you this week."
p02_which.png            IG-which      Mon Nov 23  (FB-which reuses it, Tue Nov 24)   "Which would you answer?"
p03_resume_reel.mp4      IG-rb-reel    Tue Nov 24  the free résumé builder, as a Reel
p04_one_link_reel.mp4    IG-onelink    Wed Nov 25  "One job link. Four people. One message."
p05_short_list.png       IG-shortlist  Sat Nov 28  "Long weekend. Short list."

Token-built (design-system/ds.py + reel.py). Invented company and people (Northpine), labeled
"Illustrative example". Images Facebook reuses carry no "Link in bio". The résumé Reel's form scene is
the real crop from week 47 (2026-11/wk47/site/resume_builder_form.png).

Run from repo root: python3 2026-11/wk48/build.py [thanks|which|rb|onelink|shortlist ...]
"""
import base64, io, os, sys, tempfile
from PIL import Image
WK = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(WK))
sys.path.insert(0, os.path.join(ROOT, "design-system"))
from reel import *  # noqa
from grounds import INK_KEYLINES  # noqa

TMP = tempfile.mkdtemp(prefix="wk48_")
FOOT = foot()
EX_R = sticker(EXAMPLE, MUTED, 64, 84, 24, right=True)


def rpage(body, bg=CREAM):
    # v2 (HQ, Nov 13): every ink scene gets cream keylines on Tick, cards and stickers.
    return page((INK_KEYLINES if bg == INK else "") + body + foot(dark=(bg == INK)), RW, RH, bg)


def counter(n, total, dark=False):
    return (f'<div style="position:absolute;right:72px;top:84px;font-size:30px;font-weight:700;'
            f'color:{D_MUTED_TEXT if dark else MUTED_TEXT}">{n} / {total}</div>')


def note(text, label="What to say", size=38):
    return (f'<div class="card" style="padding:32px 38px">{lbl(label, 22)}'
            f'<div style="font-size:{size}px;font-weight:600;line-height:1.34">{text}</div></div>')


# ---------- IG-thanks: carousel, 6 slides ----------
def thanks():
    T = 6
    s = []
    s.append(("p01_thanks_1", page(
        sticker("Save this", WHITE, 72, 72) + sticker("Thanksgiving week", PINK, 290, 72)
        + f'<div class="d" style="position:absolute;left:72px;top:210px;width:936px;font-size:126px">Send one <span style="white-space:nowrap">thank-you</span> this week.</div>'
        + f'<div style="position:absolute;left:76px;top:790px;width:560px;font-size:44px;font-weight:700;line-height:1.2">'
          f'3 people in your job search worth thanking, and what to say.</div>'
        + f'<div style="position:absolute;right:60px;top:700px">{tick("celebrating", 320)}</div>'
        + spark(900, 170, 64, WHITE) + FOOT, bg=LIME)))
    people = [("01", "Someone who told you no.", "Instead of leaving you waiting.",
               "Thanks for letting me know about the role. A clear answer helps, and I appreciated it. "
               "If your team hires again, I'd love to hear about it.", False),
              ("02", "Someone who accepted your connection request.", "Name one thing they shared.",
               "Thanks for connecting. Your post about onboarding new customers was the most useful thing I read this month.", True),
              ("03", "Someone who gave you an intro, a referral or advice.", "Say what came of it.",
               "Thank you for the intro to Dana. We talked on Tuesday, and I left with two good ideas. "
               "I'll let you know how it goes.", True)]
    for i, (num, head, sub, text, ex) in enumerate(people, 2):
        size = 84 if len(head) < 30 else 72
        s.append((f"p01_thanks_{i}", page(
            f'<div class="step" style="position:absolute;left:72px;top:72px"><span class="d">{num}</span></div>' + counter(i, T)
            + f'<div class="d" style="position:absolute;left:72px;top:230px;width:936px;font-size:{size}px">{head}</div>'
            + f'<div style="position:absolute;left:76px;top:{430 if size == 84 else 470}px;font-size:38px;font-weight:700;color:{MUTED_TEXT}">{sub}</div>'
            + (sticker(EXAMPLE, PINK, 72, 560, 24) if ex else "")
            + f'<div style="position:absolute;left:72px;width:936px;top:650px">{note(text)}</div>'
            + f'<div style="position:absolute;right:64px;top:1010px">{tick("waving" if i == 2 else "pointing", 170)}</div>'
            + foot(bottom=40))))
    rules = [("Short.", "Two or three sentences."), ("Specific.", "One thing they did or said."),
             ("No ask.", "Not a call, not a referral. Just thanks.")]
    rows = "".join(f'<div style="display:flex;gap:24px;align-items:baseline;margin-bottom:34px">'
                   f'<span class="d" style="flex:none;width:300px;font-size:64px"><span class="fill">{a}</span></span>'
                   f'<span style="font-size:40px;font-weight:600;line-height:1.25">{b}</span></div>' for a, b in rules)
    s.append(("p01_thanks_5", page(
        counter(5, T)
        + f'<div class="d" style="position:absolute;left:72px;top:170px;width:936px;font-size:104px">How to write it.</div>'
        + f'<div style="position:absolute;left:72px;width:936px;top:440px">{rows}</div>'
        + f'<div style="position:absolute;left:76px;top:900px;width:620px;font-size:40px;font-weight:700;line-height:1.25">'
          f'Send it before Thursday. It\'s the easiest message you\'ll send all year.</div>'
        + f'<div style="position:absolute;right:64px;top:880px">{tick("thinking", 220)}</div>'
        + FOOT)))
    # v2 (HQ, Nov 13): cream keylines on ink; the old p01_thanks_6.png stays on disk.
    s.append(("p01_thanks_6_v2", page(
        INK_KEYLINES + counter(6, T, True)
        + f'<div class="d" style="position:absolute;left:72px;top:170px;width:936px;font-size:120px;color:{CREAM}">Happy Thanksgiving.</div>'
        + f'<div style="position:absolute;left:76px;top:460px;width:880px;font-size:46px;font-weight:600;line-height:1.3;color:{CREAM}">'
          f'Next week: one job, one message.</div>'
        + f'<div class="d" style="position:absolute;left:72px;top:640px;width:640px;font-size:76px;color:{CREAM}">'
          f'Paste a job link.<br><span class="fill" style="color:{INK}">Get your 4 people.</span></div>'
        + sticker("getday60.com", LIME, 72, 910, 30)
        + f'<div style="position:absolute;right:60px;top:740px">{tick("celebrating", 280)}</div>'
        + spark(900, 110, 64, LIME) + spark(960, 560, 40, PINK)
        + foot(dark=True), bg=INK)))
    return s


# ---------- IG-which: one image ----------
def which():
    def opt(letter, bg, text):
        return (f'<div class="card" style="padding:34px 38px;display:flex;gap:30px;align-items:center;margin-bottom:40px">'
                f'<div class="d" style="flex:none;width:110px;height:110px;border-radius:50%;border:5px solid {INK};background:{bg};'
                f'display:flex;align-items:center;justify-content:center;font-size:64px;letter-spacing:0">{letter}</div>'
                f'<div style="font-size:42px;font-weight:700;line-height:1.25">"{text}"</div></div>')
    return [("p02_which", page(
        f'<div class="d" style="position:absolute;left:72px;top:110px;width:936px;font-size:112px">Which would you answer?</div>'
        + f'<div style="position:absolute;left:76px;top:370px;width:900px;font-size:36px;font-weight:600;line-height:1.3;color:{MUTED_TEXT}">'
          f'Two ways to end a first message to a hiring manager.</div>'
        + sticker(EXAMPLE, PINK, 72, 470, 24)
        + f'<div style="position:absolute;left:72px;width:936px;top:560px">'
          + opt("A", PINK, "Would you have 30 minutes this week to tell me about opportunities on your team?")
          + opt("B", MINT, "Is onboarding or renewals the bigger fire on your team right now?") + '</div>'
        + f'<div style="position:absolute;left:76px;top:1120px;font-size:40px;font-weight:700">Tell us: A or B?</div>'
        + f'<div style="position:absolute;right:64px;top:1030px">{tick("thinking", 170)}</div>'
        + foot(bottom=40)))]


# ---------- IG-shortlist: one image ----------
def shortlist():
    items = ["Pick one job you'd say yes to.", "Paste its link. See your 4 people.", "Send the hiring manager one short note."]
    rows = "".join(f'<div style="display:flex;gap:28px;align-items:center;margin-bottom:34px">'
                   f'<span style="flex:none;width:70px;height:70px;border:5px solid {INK};border-radius:16px;background:{WHITE}"></span>'
                   f'<span style="font-size:46px;font-weight:700;line-height:1.2">{t}</span></div>' for t in items)
    return [("p05_short_list", page(
        sticker("Holiday weekend", PINK, 72, 72)
        + f'<div class="d" style="position:absolute;left:72px;top:190px;width:936px;font-size:136px">Long weekend.<br>'
          f'<span class="fill">Short list.</span></div>'
        + f'<div class="card" style="position:absolute;left:72px;width:936px;top:560px;padding:46px 46px 16px">{rows}</div>'
        + f'<div style="position:absolute;left:76px;top:1060px;width:600px;font-size:42px;font-weight:700">Then back to the leftovers.</div>'
        + f'<div style="position:absolute;right:64px;top:990px">{tick("waving", 200)}</div>'
        + spark(940, 96, 64) + foot(bottom=40)))]


# ---------- IG-rb-reel: the free résumé builder ----------
RB_URL = "getday60.com/resume-builder"


def chip(text, bg=MINT, x=False):
    icon = check(34, ok=False) if x else ""
    return (f'<span style="display:inline-flex;align-items:center;gap:12px;margin:0 14px 16px 0;padding:10px 22px;'
            f'background:{bg};border:4px solid {INK};border-radius:999px;font-size:32px;font-weight:700">{icon}{text}</span>')


def pair(before, after):
    return (f'<div class="card" style="padding:0;overflow:hidden;margin-bottom:44px">'
            f'<div class="muted" style="padding:24px 36px;border-bottom:4px solid {INK}">{lbl("From the résumé", 22)}'
            f'<div style="font-size:36px;font-weight:500;line-height:1.28">{before}</div></div>'
            f'<div style="padding:24px 36px">{lbl("For this job", 22)}'
            f'<div style="font-size:38px;font-weight:700;line-height:1.28"><span class="fill">{after}</span></div></div></div>')


def rb():
    im = Image.open(os.path.join(ROOT, "2026-11", "wk47", "site", "resume_builder_form.png")).convert("RGB")
    im = im.crop((8, 8, im.width - 8, 930))
    buf = io.BytesIO(); im.save(buf, "PNG")
    src = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    ex = sticker(EXAMPLE, PINK, 72, 420, 24)
    hook = rpage(
        sticker("Free résumé builder", WHITE, 72, 150)
        + f'<div class="d" style="position:absolute;left:72px;right:72px;top:300px;font-size:150px">Tailor your résumé to one job.</div>'
        + f'<div class="d" style="position:absolute;left:72px;right:72px;top:960px;font-size:120px"><span class="fill">No account.</span></div>'
        + f'<div style="position:absolute;right:80px;top:1200px">{tick("thinking", 320)}</div>'
        + spark(900, 210, 70, PINK), bg=CREAM)
    form = rpage(
        step_head("01", "Add the job and your résumé.", 190, 76)
        + ex
        + f'<div class="card" style="position:absolute;left:72px;top:520px;width:640px;padding:0;overflow:hidden">'
          f'<img src="{src}" style="display:block;width:640px"></div>'
        + tick_says("pointing", "A link to the posting (not LinkedIn) or the posting itself.", 1400, 200, 60, 38))
    problems = ["New customers take too long to get started.", "Renewals slip without warning.",
                "Customer feedback reaches the product team late."]
    wants = rpage(
        step_head("02", "See what the job wants.", 190, 80) + ex
        + f'<div class="card" style="position:absolute;left:72px;right:72px;top:520px;padding:38px 44px">'
          f'<div class="d" style="font-size:56px;margin-bottom:6px">What this job wants</div>'
          f'<div style="font-size:30px;color:{MUTED_TEXT};margin-bottom:30px">{JOB} at {COMPANY} (invented)</div>'
          + lbl("Keywords") + "".join(chip(k) for k in ["Customer onboarding", "Renewals", "Account health", "Product feedback"])
          + '<div style="height:18px"></div>' + lbl("3 problems this role solves")
          + "".join(f'<div style="display:flex;gap:20px;align-items:flex-start;font-size:36px;font-weight:600;line-height:1.25;margin-bottom:18px">'
                    f'<span class="d" style="flex:none;width:54px;height:54px;border:4px solid {INK};border-radius:14px;background:{LIME};'
                    f'display:flex;align-items:center;justify-content:center;font-size:32px">{i}</span><span>{t}</span></div>'
                    for i, t in enumerate(problems, 1))
          + '</div>')
    true = rpage(
        step_head("03", "Tailored, with only what's true.", 190, 76) + ex
        + f'<div style="position:absolute;left:72px;right:72px;top:520px">'
          + pair("Trained staff at new accounts on the ordering system.", "Onboarded new accounts and trained their teams.")
          + pair("Ran 60 small-business accounts, renewals included.", "Managed renewals for 60 small-business accounts.")
          + f'<div style="font-size:40px;font-weight:700;line-height:1.28;margin-top:10px">No new skill, number or title.</div></div>')
    gap = rpage(
        step_head("04", "Know the gap before they do.", 190, 76) + ex
        + f'<div class="card" style="position:absolute;left:72px;right:72px;top:520px;padding:38px 44px">'
          f'<div class="d" style="font-size:50px;margin-bottom:26px">Keywords you can\'t claim yet</div>'
          + chip("Account health scores", WHITE, True) + chip("Quarterly business reviews", WHITE, True)
          + f'<div style="font-size:36px;font-weight:500;line-height:1.3;margin-top:8px">In the posting, not in the résumé, so they stay off it.</div></div>'
        + f'<div class="card" style="position:absolute;left:72px;right:72px;top:960px;padding:36px 44px;background:{MINT}">'
          f'<div class="d" style="font-size:48px;margin-bottom:14px">Make it stronger</div>'
          f'<div style="font-size:38px;font-weight:700;line-height:1.25">Have you tracked which accounts might not renew?</div>'
          f'<div style="font-size:26px;font-weight:600;margin-top:12px">Example question</div></div>')
    end = rpage(
        f'<div class="d" style="position:absolute;left:72px;right:72px;top:260px;font-size:140px;color:{CREAM}">'
        f'Read every line.<br><span class="fill" style="color:{INK}">Get a Word file.</span></div>'
        + f'<div style="position:absolute;left:76px;top:760px;width:900px;font-size:50px;font-weight:600;line-height:1.3;color:{CREAM}">'
          f'Free. No account. Nothing you add is kept.</div>'
        + sticker(RB_URL, LIME, 72, 1000, 32) + sticker("Link in bio", WHITE, 72, 1110, 32)
        + f'<div style="position:absolute;right:80px;top:1240px">{tick("celebrating", 300)}</div>'
        + spark(910, 170, 64, LIME), bg=INK)
    return [("rb_hook", hook, 2.6), ("rb_form", form, 3.2), ("rb_wants", wants, 3.8),
            ("rb_true", true, 3.8), ("rb_gap", gap, 3.6), ("rb_end", end, 3.4)]


# ---------- IG-onelink: One job link. Four people. One message. ----------
def onelink():
    def big(text, top=190):
        return f'<div class="d" style="position:absolute;left:72px;right:72px;top:{top}px;font-size:130px">{text}</div>'

    def paste(filled):
        field = (f'<span style="color:{INK}">{JOB_URL}</span>' if filled else
                 f'<span style="color:{MUTED_TEXT}">Paste a job link</span>')
        job = (f'<div class="card" style="margin-top:40px;padding:30px 36px;display:flex;align-items:center;gap:26px">'
               f'<div class="d" style="flex:none;width:96px;height:96px;border:4px solid {INK};border-radius:24px;background:{MINT};'
               f'display:flex;align-items:center;justify-content:center;font-size:54px">N</div>'
               f'<div><div class="d" style="font-size:54px">{JOB}</div>'
               f'<div style="font-size:34px;color:{MUTED_TEXT};margin-top:6px">{COMPANY} · Remote</div></div></div>') if filled else ""
        return rpage(EX_R + big("One job link.")
                     + f'<div style="position:absolute;left:72px;right:72px;top:470px">'
                       f'<div class="card" style="padding:38px">{lbl("Job link", 30, INK)}'
                       f'<div style="border:4px solid {INK};border-radius:20px;padding:26px 28px;font-size:36px;background:{CREAM};'
                       f'white-space:nowrap;overflow:hidden">{field}</div></div>{job}</div>'
                     + f'<div style="position:absolute;right:80px;top:1180px">{tick("pointing", 260)}</div>')

    def people(k):
        rows = "".join(person_row(p, 1.0, True, 28) for p in PEOPLE[:k])
        return rpage(EX_R + big("Four people.")
                     + f'<div style="position:absolute;left:72px;right:72px;top:450px">{rows}</div>')

    draft = ("Hi Maya, your posting says new customers take too long to get started. "
             "At my last job, I onboarded new accounts and trained their teams. "
             "Where do new customers get stuck most: setup or training?")
    checks = "".join(f'<div style="display:flex;gap:18px;align-items:center;font-size:36px;font-weight:700;margin-top:16px">'
                     f'{check(46)}{c}</div>' for c in ["Asks one clear question", "The question comes last", "Fits the length limit", "No links"])
    msg = rpage(EX_R + big("One message.")
                + f'<div class="card" style="position:absolute;left:72px;right:72px;top:450px;padding:36px 40px">'
                  + lbl("Draft to Maya Ortiz · Hiring manager", 24) + f'<div style="font-size:40px;line-height:1.36">{draft}</div></div>'
                + f'<div style="position:absolute;left:76px;top:1010px">{checks}</div>'
                + f'<div style="position:absolute;right:80px;top:1080px">{tick("celebrating", 250)}</div>')
    end = rpage(
        f'<div class="d" style="position:absolute;left:72px;right:72px;top:260px;font-size:170px;color:{CREAM}">You<br>'
        f'<span class="fill" style="color:{INK}">send it.</span></div>'
        + f'<div style="position:absolute;left:76px;top:720px;width:900px;font-size:48px;font-weight:600;line-height:1.3;color:{CREAM}">'
          f'Day60 never logs in to LinkedIn and never sends anything for you.</div>'
        + f'<div class="d" style="position:absolute;left:72px;top:960px;width:900px;font-size:66px;color:{CREAM}">'
          f'Paste a job link. Get your 4 people.</div>'
        + sticker("Link in bio", LIME, 72, 1170, 34)
        + f'<div style="position:absolute;right:80px;top:1260px">{tick("running", 300)}</div>'
        + spark(910, 170, 64, LIME), bg=INK)
    return [("ol_paste0", paste(False), 1.4), ("ol_paste1", paste(True), 2.2),
            ("ol_p1", people(1), 0.7), ("ol_p2", people(2), 0.7), ("ol_p3", people(3), 0.7), ("ol_p4", people(4), 2.6),
            ("ol_msg", msg, 3.6), ("ol_end", end, 3.4)]


def still(slides, names=()):
    jobs = []
    for name, html in slides:
        if names and name not in names:
            continue
        p = os.path.join(TMP, name + ".html"); open(p, "w").write(html)
        jobs.append({"html": p, "png": os.path.join(WK, name + ".png"), "w": 1080, "h": 1350})
    render(jobs, TMP)


if __name__ == "__main__":
    # Modes: thanks, which, rb, onelink, shortlist. Any other argument is a slide name to render alone.
    # The _v2 reels (HQ, Nov 13) only change the ink end scene; the old mp4s stay on disk.
    args = set(sys.argv[1:])
    names = {a for a in args if a.startswith("p0")}
    want = (args - names) or ({"thanks", "which", "shortlist"} if names else {"thanks", "which", "rb", "onelink", "shortlist"})
    if "thanks" in want: still(thanks(), names)
    if "which" in want: still(which(), names)
    if "shortlist" in want: still(shortlist(), names)
    if "rb" in want: make_reel(rb(), os.path.join(WK, "p03_resume_reel_v2.mp4"), os.path.join(TMP, "rb"))
    if "onelink" in want: make_reel(onelink(), os.path.join(WK, "p04_one_link_reel_v2.mp4"), os.path.join(TMP, "onelink"))
    print("tmp:", TMP)
