"""Week 52 drafts, Mon Dec 21 to Sun Dec 27, 2026 (Social, Nov 27; HQ's brief of Nov 27, drafts ahead to Jan 3).

Holiday week: lighter and kind, never about being laid off or out of work. The text of each post lives in
2026-12/wk52/posts.md (gen.py reads it byte for byte); this file holds the hand-set fields.
Art: 2026-12/wk52/build_holiday.py. FB-thanks-holiday reuses IG-thanks-r2's holiday slides.
"""
W = "2026-w52"
D = "2026-12/wk52"
THANKS_FILES = [
    (f"{D}/p01_thanks_1_pink_holiday.png", "Holiday week: send one thank-you. 3 people in your job search worth thanking, and what to say."),
    ("2026-11/wk48/p01_thanks_2_safe.png", "Thank someone who told you no instead of leaving you waiting: a clear answer helps, and you appreciated it."),
    ("2026-11/wk48/p01_thanks_3_safe.png", "Thank someone who accepted your connection request, and name one thing they shared."),
    ("2026-11/wk48/p01_thanks_4_safe.png", "Thank someone who gave you an intro, a referral or advice, and say what came of it."),
    (f"{D}/p01_thanks_5_holiday.png", "How to write it: short, specific, and no ask. Send it before the holidays."),
    (f"{D}/p01_thanks_6_holiday.png", "Happy holidays. Next week: one job, one message. Paste a job link to get your 4 people at getday60.com"),
]


def specs(entry, one):
    li = lambda pid, date, time, title: entry(W, pid, channel="linkedin", date=date, time=time, status="draft",
                                               title=title, format="text")
    ig = lambda pid, date, time, title, png: entry(W, pid, channel="instagram", date=date, time=time, status="draft",
                                                    title=title, format="image", files=one(W, pid, f"{D}/{png}"))
    fb = lambda pid, date, time, title, png: entry(W, pid, channel="facebook", date=date, time=time, status="draft",
                                                    title=title, format="image", files=one(W, pid, f"{D}/{png}"))
    return [
        li("LI-checker", "2026-12-21", "11:49", "My note, through the checker"),
        li("LI-holidaynote", "2026-12-22", "09:17", "Holiday notes get read in January"),
        li("LI-party", "2026-12-23", "08:44", "Sales development habits for holiday parties"),
        li("LI-lastline", "2026-12-24", "08:28", "Christmas Eve: read your last line"),
        li("LI-christmas", "2026-12-25", "08:01", "Merry Christmas from Phil"),
        li("LI-january", "2026-12-27", "08:34", "Three jobs for January"),
        ig("IG-quietresume", "2026-12-22", "19:37", "Tailor your resume to one job", "p02_quiet_resume_mint.png"),
        ig("IG-wishlist", "2026-12-23", "16:12", "Holiday wish list: a reply", "p03_wish_list_ink.png"),
        ig("IG-table", "2026-12-24", "07:16", "Skip \"Any luck yet?\"", "p04_holiday_table_coral.png"),
        ig("IG-christmas", "2026-12-25", "21:24", "Today's only task: rest", "p05_merry_christmas_cobalt.png"),
        ig("IG-returns", "2026-12-26", "21:23", "Returns desk: 40 applications, unopened", "p06_returns_desk_lime.png"),
        ig("IG-threejobs", "2026-12-27", "21:26", "Three jobs, not thirty", "p07_three_jobs_pink.png"),
        fb("FB-quietresume", "2026-12-21", "20:51", "Tailor your resume to one job", "p02_quiet_resume_mint.png"),
        entry(W, "FB-thanks-holiday", channel="facebook", date="2026-12-22", time="08:27", status="draft",
              title="Holiday week: send one thank-you", format="carousel",
              files=[{"path": p, "alt": a} for p, a in THANKS_FILES]),
        fb("FB-table", "2026-12-23", "09:11", "Skip \"Any luck yet?\"", "p04_holiday_table_coral.png"),
        fb("FB-wishlist", "2026-12-24", "10:11", "Holiday wish list: a reply", "p03_wish_list_ink.png"),
        entry(W, "FB-christmas", channel="facebook", date="2026-12-25", time="06:59", status="draft",
              title="Merry Christmas from Day60", format="text"),
        fb("FB-threejobs", "2026-12-26", "22:24", "Three jobs, not thirty", "p07_three_jobs_pink.png"),
        fb("FB-returns", "2026-12-27", "09:51", "Returns desk: 40 applications, unopened", "p06_returns_desk_lime.png"),
    ]
