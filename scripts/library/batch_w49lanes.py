"""LinkedIn by weekday (Philip, Fri Nov 27, 1:30 PM CT, via HQ), verbatim:
"make sure that LinkedIn posts are about H on Monday and Thursday, Day60 on Tuesday and Friday, and genreating
pipeline best practices on Wednesday and Sunday." and "there should only be one post a day on each platform."

specs(entry, one): the five new H and pipeline drafts (text in 2026-11/wk49/posts.md).
apply(SPECS): runs last in gen.py. Re-dates the Day60 LinkedIn posts onto Tue/Fri, benches the ones that no
longer have a Day60 day in December, and retires the Sunday "plan your week" posts and the Christmas Eve post,
whose text only works on that day."""
import notes

W = "2026-w49"
LI_N = ["Publishes through Buffer, automatically, on Philip's LinkedIn profile, as a text post.",
        "No first comment: Buffer's plan doesn't allow one (HQ, Nov 19).",
        "Inside 8 AM to 12:59 PM CT (Philip, Nov 24)."]
DRAFT = "Approved by HQ (Nov 27), for Philip's weekday rule; HQ moved the H posts' hashtags above the link so the link ends the post."
H_N = ["H day. Entirely professional, H's own words and facts only, from H's newsroom. The article link is the body's last line.",
       "No tags: no verified LinkedIn ID for H Company (its page returned 403 on Nov 27)."]
P_N = ["Pipeline best practices day. No link and no Day60 (playbook §4)."]

NOTES_LANES = {
    f"{W}-LI-firsthour": LI_N + P_N + [DRAFT],
    f"{W}-LI-H-hackathon": LI_N + H_N + [DRAFT, "Source: hcompany.ai newsroom, Nov 25 article, read Nov 27."],
    f"{W}-LI-threads": LI_N + P_N + [DRAFT],
    f"{W}-LI-H-aws": LI_N + H_N + [DRAFT, "Source: hcompany.ai newsroom, Nov 16 release, read Nov 27."],
    f"{W}-LI-nextstep": LI_N + P_N + [DRAFT],
}


def specs(entry, one):
    notes.NOTES.update(NOTES_LANES)
    out = []
    for pid, date, time, title, topic in [
        ("LI-firsthour", "2026-11-29", "08:44", "Protect Monday's first hour", "pipeline"),
        ("LI-H-hackathon", "2026-11-30", "11:14", "H x 42AI hackathon winners", "h"),
        ("LI-threads", "2026-12-02", "11:59", "Thread the account early", "pipeline"),
        ("LI-H-aws", "2026-12-03", "11:19", "H on AWS European Sovereign Cloud", "h"),
        ("LI-nextstep", "2026-12-06", "11:31", "Write the next step first", "pipeline"),
    ]:
        e = entry(W, pid, channel="linkedin", date=date, time=time, title=title, format="text", status="approved")
        e["topic"] = topic
        out.append(e)
    return out


RULE = "Philip's weekday rule (Nov 27): LinkedIn is H on Mon and Thu, Day60 on Tue and Fri, pipeline on Wed and Sun."
# Day60 posts re-dated onto a Tue or Fri in December.
MOVE = {
    "2026-w49-LI-glossary": ("2026-12-04", "08:11", "Moved from Mon Nov 30 to Fri Dec 4 (Buffer post moved Nov 27)."),
    "2026-w50-LI-findhm": ("2026-12-11", "09:44", "Moved from Thu Dec 10 to Fri Dec 11; keeps week 50's guide on LinkedIn."),
    "2026-w52-LI-party": ("2026-12-18", "08:44", "Moved from Wed Dec 23 to Fri Dec 18: holiday-party season, so it runs while it fits."),
    "2026-w53-LI-ooo": ("2026-12-29", "09:03", "Moved from Wed Dec 30 to Tue Dec 29: out-of-office week."),
}
# Evergreen Day60 posts with no December Tue/Fri left: benched on Tue/Fri slots after the paid launch window.
BENCH = {
    "2026-w49-LI-hiringside": ("2027-01-19", "10:18"), "2026-w49-LI-3touch": ("2027-01-22", "11:09"),
    "2026-w50-LI-ats": ("2027-01-26", "11:17"), "2026-w50-LI-asks": ("2027-01-29", "10:06"),
    "2026-w51-LI-person": ("2027-02-02", "09:48"), "2026-w51-LI-resume": ("2027-02-05", "12:02"),
    "2026-w51-LI-stages": ("2027-02-09", "09:39"), "2026-w52-LI-plainnote": ("2027-02-12", "09:46"),
    "2026-w53-LI-nudge": ("2027-02-16", "10:28"), "2026-w53-LI-subject": ("2027-02-19", "10:13"),
    "2026-w49-LI-target": ("2027-02-23", "09:33"), "2026-w50-LI-checker": ("2027-02-26", "08:01"),
    "2026-w51-LI-fourpeople": ("2027-03-02", "09:28"), "2026-w53-LI-extension": ("2027-03-05", "10:53"),
}
# Text written for one day that no longer has a Day60 slot: retired.
RETIRE = {
    "2026-w49-LI-monday": "Sunday plan post; Sunday is now pipeline. Pulled from Buffer Nov 27 (kept there as a draft, 6b0437de433e6368c8a8610c).",
    "2026-w49-LI-week": "Sunday plan post; Sunday is now pipeline.",
    "2026-w50-LI-week": "Sunday plan post; Sunday is now pipeline.",
    "2026-w51-LI-shortweek": "Sunday plan post; Sunday is now pipeline.",
    "2026-w52-LI-onename": "Sunday plan post; Sunday is now pipeline.",
    "2026-w53-LI-plan": "Sunday plan post; Sunday is now pipeline.",
    "2026-w52-LI-lastline": "Christmas Eve text; Thu Dec 24 is an H day.",
}


def apply(SPECS):
    by = {e["id"]: e for e in SPECS}
    for i, (d, t, why) in MOVE.items():
        by[i].update(date=d, time=t)
        by[i]["notes"] += f"\n{RULE} {why}"
    for i, (d, t) in BENCH.items():
        was = f'{by[i]["date"]} {by[i]["time"]}'
        by[i].update(date=d, time=t)
        by[i]["notes"] += (f"\n{RULE} BENCHED: was {was}; no December Tue/Fri left. Parked on a Tue/Fri after the "
                           "paid-launch window. Before it loads, check the wording for paid mode (no \"free sprint\"; "
                           "\"Free sprints end January 5\" comes out). HQ may swap it in earlier.")
    for i, why in RETIRE.items():
        by[i]["status"] = "replaced"
        by[i]["notes"] += f"\n{RULE} RETIRED (Nov 27): {why}"
    # Scheduled in Buffer by HQ at 20:02Z Nov 27 (Social's Buffer writes are paused, HQ Nov 27).
    for i, bid in {"2026-w49-LI-firsthour": "6b09e1de71e8cc12a6c76f18", "2026-w49-LI-H-hackathon": "6b09e1f32ea34800c28e4cc1",
                   "2026-w49-LI-threads": "6b09e1f62ea34800c28e4ef4", "2026-w49-LI-H-aws": "6b09e1fa277f27038a350874",
                   "2026-w49-LI-nextstep": "6b09e1fd585cafb820d9d733"}.items():
        if i in by:
            by[i]["postedVia"] = "buffer"
            by[i]["notes"] += f"\nIn Buffer: scheduled by HQ Nov 27, 20:02Z, post {bid}."
    if "2026-w48-FB-onelink" in by:
        by["2026-w48-FB-onelink"]["notes"] += ("\nEmail promise fixed (HQ, Nov 27): \"Each comes with a short note in your voice, and a verified "
                                               "work email when Day60 finds one. Tick checks every draft.\" HQ saved it to Buffer post 6b0430c3433e6368c8a53c50.")
    for i in ("2026-w49-LI-3touch", "2026-w49-LI-monday"):
        if i in by:
            by[i]["postedVia"] = ""  # pulled from Buffer to a Buffer draft Nov 27; not in the queue
    if "2026-w49-LI-3touch" in by:
        by["2026-w49-LI-3touch"]["notes"] += "\nPulled from Buffer Nov 27 (kept there as a draft, 6b075f60b8e2338b8569eaf3)."
