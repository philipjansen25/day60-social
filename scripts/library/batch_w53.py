"""Week 53 drafts (Mon Dec 28, 2026 to Sun Jan 3, 2027), Social, Nov 27, for HQ's one-pass approval.

Text, alt text and links come from 2026-12/wk53/posts.md (the "December batch" section).
Called from gen.py: SPECS += specs(entry, _one)."""
W = "2026-w53"
D = "2026-12/wk53"


def specs(entry, one):
    li = lambda pid, date, time, title: entry(W, pid, channel="linkedin", date=date, time=time, status="draft",
                                               title=title, format="text")
    img = lambda ch, pid, date, time, title, f: entry(W, pid, channel=ch, date=date, time=time, status="draft",
                                                      title=title, format="image", files=one(W, pid, f"{D}/{f}"))
    return [
        li("LI-extension", "2026-12-28", "10:29", "I tried our Chrome extension"),
        li("LI-nudge", "2026-12-29", "10:28", "Your follow-up needs one new thing"),
        li("LI-ooo", "2026-12-30", "10:42", "Holiday out-of-office replies, decoded"),
        li("LI-subject", "2026-12-31", "10:13", "Short subject lines get opened"),
        li("LI-newyear", "2027-01-01", "12:09", "Happy New Year"),
        li("LI-plan", "2027-01-03", "08:14", "January: start small"),
        img("instagram", "IG-ooo", "2026-12-28", "20:03", "Out of office until Jan 4", "p01_out_of_office_cobalt.png"),
        img("instagram", "IG-keywords", "2026-12-29", "17:58", "Keywords you can claim", "p02_keywords_mint.png"),
        img("instagram", "IG-yearlist", "2026-12-30", "13:54", "Three things you did this year", "p03_year_list_coral.png"),
        img("instagram", "IG-lastcall", "2026-12-31", "07:04", "Last call for the year", "p04_last_call_ink.png"),
        img("instagram", "IG-newyear", "2027-01-01", "21:42", "Happy New Year. Rest today.", "p05_new_year_pink.png"),
        img("instagram", "IG-five", "2027-01-02", "20:32", "One job at a time", "p06_one_job_lime.png"),
        img("instagram", "IG-readline", "2027-01-03", "21:56", "Read every line", "p07_read_every_line_mint.png"),
        img("facebook", "FB-yearlist", "2026-12-28", "19:07", "Three things you did this year", "p03_year_list_coral.png"),
        img("facebook", "FB-ooo", "2026-12-29", "07:24", "Out of office until Jan 4", "p01_out_of_office_cobalt.png"),
        img("facebook", "FB-lastcall", "2026-12-30", "08:59", "Last call for the year", "p04_last_call_ink.png"),
        img("facebook", "FB-newyear", "2026-12-31", "10:42", "Happy New Year. Rest.", "p05_new_year_pink.png"),
        img("facebook", "FB-five", "2027-01-01", "07:52", "One job at a time", "p06_one_job_lime.png"),
        img("facebook", "FB-readline", "2027-01-02", "22:57", "Read every line", "p07_read_every_line_mint.png"),
        img("facebook", "FB-keywords", "2027-01-03", "10:07", "Keywords you can claim", "p02_keywords_mint.png"),
    ]
