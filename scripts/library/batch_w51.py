"""Week 51 (Mon Dec 14 to Sun Dec 20, 2026): drafts for HQ's one-pass approval (Social, Nov 27).

gen.py calls specs(entry, _one). Text comes from 2026-12/wk51/posts.md byte for byte (entry() reads it).
The two Facebook carousels reuse the recycled Instagram slides, with the same alt text, read from library.json.
Notes for every post are added to notes.NOTES here, so gen.py's notes check finds them."""
import json, os
import notes

W = "2026-w51"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DRAFT = "Draft for HQ's one-pass approval (Social, Nov 27)."
HUMOR = "humor"
LI_N = ["Publishes through Buffer, automatically, on Philip's LinkedIn profile, as a text post.",
        "No first comment: Buffer's plan doesn't allow one (HQ, Nov 19).",
        'Tag Day60: the first "Day60" in the text, page 144030699 (Philip, Nov 26; linkedin-company-ids.md).',
        "Inside 8 AM to 12:59 PM CT (Philip, Nov 24)."]
IG_N = ["Publishes through Buffer, automatically, on Instagram at 1080x1350 (no expand step).",
        "The image goes up with its alt text.", "No link in the caption; the bio link stays as it is."]
FB_N = ["Publishes through Buffer, automatically, as the Day60 Facebook Page.",
        "The image goes up with its alt text.", "The link stays in the text, as written.",
        "No Facebook-only creative: the art is Instagram's (HQ, Nov 26)."]
FB_CAR_N = ["Publishes through Buffer, automatically, as the Day60 Facebook Page.",
            "Images go up in the listed order, each with its alt text.", "The link stays in the text, as written.",
            "No Facebook-only creative: the art is Instagram's (HQ, Nov 26)."]
VERIFY = "[VERIFY] Phil confirms he did this before approval (an \"I tried it\" post; no outcome is claimed)."

NOTES_W51 = {
    f"{W}-LI-checker": LI_N + [DRAFT, VERIFY],
    f"{W}-LI-firstline": LI_N + [DRAFT, "Both quoted lines are illustrative."],
    f"{W}-LI-person": LI_N + [DRAFT, "No link: Phil's own view (HQ, Nov 26: his personal posts stay linkless)."],
    f"{W}-LI-resume": LI_N + [DRAFT],
    f"{W}-LI-stages": LI_N + [DRAFT, HUMOR],
    f"{W}-LI-shortweek": LI_N + [DRAFT, "Sunday lane; holiday season from Dec 21 (HQ, Nov 27)."],
    f"{W}-IG-tailor": IG_N + [DRAFT, "Facebook reuses this card Wed Dec 16."],
    f"{W}-IG-gap": IG_N + [DRAFT, "Facebook reuses this card Thu Dec 17."],
    f"{W}-IG-rounds": IG_N + [DRAFT, HUMOR, "Facebook reuses this card Sat Dec 19."],
    f"{W}-IG-firstline": IG_N + [DRAFT, "Both quoted lines are illustrative, and the card says so.", "Facebook reuses this card Sun Dec 20."],
    f"{W}-IG-wishlist": IG_N + [DRAFT, HUMOR, "Facebook reuses this card Fri Dec 18."],
    f"{W}-FB-firstjob": FB_CAR_N + [DRAFT, "Same 6 slides as IG-firstjob-r2 (Thu Dec 17); none says \"Link in bio\"."],
    f"{W}-FB-touches": FB_CAR_N + [DRAFT, "Same 6 slides as IG4-r2 (Mon Dec 14); none says \"Link in bio\"."],
    f"{W}-FB-tailor": FB_N + [DRAFT],
    f"{W}-FB-gap": FB_N + [DRAFT],
    f"{W}-FB-wishlist": FB_N + [DRAFT, HUMOR],
    f"{W}-FB-rounds": FB_N + [DRAFT, HUMOR],
    f"{W}-FB-firstline": FB_N + [DRAFT, "Both quoted lines are illustrative."],
}


def _files_of(lib_id):
    lib = json.load(open(os.path.join(ROOT, "library.json")))
    e = next(p for p in lib if p["id"] == lib_id)
    return [{"path": f["path"], "alt": f["alt"]} for f in e["files"]]


def specs(entry, one):
    notes.NOTES.update(NOTES_W51)
    d = dict(status="draft")
    li = lambda pid, date, time, title: entry(W, pid, channel="linkedin", date=date, time=time, title=title, format="text", **d)
    img = lambda ch, pid, date, time, title, path: entry(W, pid, channel=ch, date=date, time=time, title=title, format="image",
                                                         files=one(W, pid, path), **d)
    car = lambda pid, date, time, title, src: entry(W, pid, channel="facebook", date=date, time=time, title=title,
                                                    format="carousel", files=_files_of(src), **d)
    wk = "2026-12/wk51/"
    return [
        li("LI-checker", "2026-12-14", "09:12", "My draft in the message checker"),
        li("LI-firstline", "2026-12-15", "08:37", "The first line does the work"),
        li("LI-person", "2026-12-16", "09:48", "Nobody calls a company"),
        li("LI-resume", "2026-12-17", "12:02", "Tailor your resume without inventing one"),
        li("LI-stages", "2026-12-18", "09:39", "Five stages of waiting"),
        li("LI-shortweek", "2026-12-20", "11:46", "Plan the short week"),
        img("instagram", "IG-tailor", "2026-12-15", "18:37", "Tailor it. Don't invent it.", wk + "p01_tailor_coral.png"),
        img("instagram", "IG-gap", "2026-12-16", "12:14", "Keyword gap: a to-do list", wk + "p02_keyword_gap_cobalt.png"),
        img("instagram", "IG-rounds", "2026-12-18", "22:34", "Round 7: a quick chat", wk + "p03_seven_rounds_pink.png"),
        img("instagram", "IG-firstline", "2026-12-19", "20:24", "Your first line is about them", wk + "p04_first_line_mint.png"),
        img("instagram", "IG-wishlist", "2026-12-20", "20:18", "Tick's holiday wish list", wk + "p05_wishlist_ink.png"),
        car("FB-firstjob", "2026-12-14", "19:02", "Your first job, step by step", "2026-w47-IG-firstjob-r2"),
        car("FB-touches", "2026-12-15", "08:12", "Three touches, then stop", "2026-w46-IG4-r2"),
        img("facebook", "FB-tailor", "2026-12-16", "08:34", "Tailor it. Don't invent it.", wk + "p01_tailor_coral.png"),
        img("facebook", "FB-gap", "2026-12-17", "08:32", "Keyword gap: a to-do list", wk + "p02_keyword_gap_cobalt.png"),
        img("facebook", "FB-wishlist", "2026-12-18", "06:36", "Tick's holiday wish list", wk + "p05_wishlist_ink.png"),
        img("facebook", "FB-rounds", "2026-12-19", "21:26", "Round 7: a quick chat", wk + "p03_seven_rounds_pink.png"),
        img("facebook", "FB-firstline", "2026-12-20", "09:38", "Your first line is about them", wk + "p04_first_line_mint.png"),
    ]
