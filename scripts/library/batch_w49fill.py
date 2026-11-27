"""Week 49 fill-ins (Wed Dec 2 to Sun Dec 6, 2026): drafts for HQ (Social, Nov 27).

gen.py calls specs(entry, one). Text comes from 2026-11/wk49/posts.md byte for byte (entry() reads it)."""
import json, os
import notes

W = "2026-w49"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DRAFT = "Approved by HQ (Nov 27); fills an empty slot in the week of Nov 30. Load at Sunday Nov 29 top-up."
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
            "Slide 7 is IG6-r2's with \"Free sprint: link in bio\" painted out (2026-11/wk49/build_fill.py)."]

NOTES_W49F = {
    f"{W}-LI-week": LI_N + [DRAFT, "Follow-up claim uses only the approved wording (playbook §1, HQ Nov 5)."],
    f"{W}-IG-review": IG_N + [DRAFT, HUMOR, "Facebook reuses this card Sun Dec 6."],
    f"{W}-IG-attach": IG_N + [DRAFT, "Facebook reuses this card Fri Dec 4."],
    f"{W}-IG-stronger": IG_N + [DRAFT, "The question on the card is illustrative, labeled \"Example question\".",
                                "Facebook reuses this card Sat Dec 5."],
    f"{W}-FB-checker": FB_CAR_N + [DRAFT, "Same slides and alt text as IG6-r2 (Tue Dec 1)."],
    f"{W}-FB-attach": FB_N + [DRAFT, "Gives way to Philip's priority post if it fits Facebook (HQ, Nov 27)."],
    f"{W}-FB-stronger": FB_N + [DRAFT],
    f"{W}-FB-review": FB_N + [DRAFT, HUMOR],
}


def _checker_files():
    lib = json.load(open(os.path.join(ROOT, "library.json")))
    e = next(p for p in lib if p["id"] == "2026-w46-IG6-r2")
    fs = [{"path": f["path"], "alt": f["alt"]} for f in e["files"]]
    fs[-1]["path"] = "2026-11/wk49/p15_checker_7_fb.png"
    return fs


def specs(entry, one):
    notes.NOTES.update(NOTES_W49F)
    d = dict(status="approved")
    wk = "2026-11/wk49/"
    img = lambda ch, pid, date, time, title, path: entry(W, pid, channel=ch, date=date, time=time, title=title, format="image",
                                                         files=one(W, pid, path), **d)
    return [
        entry(W, "LI-week", channel="linkedin", date="2026-12-06", time="08:17", title="Monday plan: follow-ups first",
              format="text", **d),
        img("instagram", "IG-review", "2026-12-04", "21:22", "Status: under review", wk + "p04_under_review_pink.png"),
        img("instagram", "IG-attach", "2026-12-05", "20:44", "No attachments on a first note", wk + "p05_no_attachments_mint.png"),
        img("instagram", "IG-stronger", "2026-12-06", "21:04", "Your best results, in your head", wk + "p06_make_stronger_cobalt.png"),
        entry(W, "FB-checker", channel="facebook", date="2026-12-02", time="08:58", title="Would Tick let you send it?",
              format="carousel", files=_checker_files(), **d),
        img("facebook", "FB-attach", "2026-12-04", "06:47", "No attachments on a first note", wk + "p05_no_attachments_mint.png"),
        img("facebook", "FB-stronger", "2026-12-05", "21:21", "Your best results, in your head", wk + "p06_make_stronger_cobalt.png"),
        img("facebook", "FB-review", "2026-12-06", "08:51", "Status: under review", wk + "p04_under_review_pink.png"),
    ]
