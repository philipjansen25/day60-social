"""Build library.json entries from posts.md (text byte for byte) plus hand-set fields.

Usage, from anywhere: python3 scripts/library/gen.py  (writes library.json at the repo root from SPECS,
merged with any entries already there whose id isn't in SPECS). notes.py and recycle_def.py, beside it, hold
the notes and the recycled ("-r2") posts. Then run: node scripts/check-library.mjs"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)
WEEK_DIR = {"2026-w45": "2026-11/wk1"}


def week_dir(week):
    if week in WEEK_DIR:
        return WEEK_DIR[week]
    y, wk = week[:4], f"wk{week[-2:]}"
    for d in sorted(x for x in os.listdir(".") if re.fullmatch(r"\d{4}-\d{2}", x)):
        if (d[:4] == y or d == f"{int(y) - 1}-12") and os.path.exists(os.path.join(d, wk, "posts.md")):
            return f"{d}/{wk}"
    raise KeyError(week)


def section(week, pid):
    lines = open(os.path.join(week_dir(week), "posts.md")).read().split("\n")
    for i, l in enumerate(lines):
        if l.startswith("### "):
            hid = re.sub(r"\s*\(.*?\)$", "", l[4:].split(" · ")[0])
            if hid == pid:
                j = i + 1
                while j < len(lines) and not lines[j].startswith("### ") and not lines[j].startswith("## "):
                    j += 1
                return lines[i:j]
    raise KeyError(f"{week} {pid}")


def text_of(sec):
    try:
        a = next(i for i, l in enumerate(sec) if l.startswith("```"))
    except StopIteration:
        return ""
    b = next(i for i in range(a + 1, len(sec)) if sec[i].startswith("```"))
    return "\n".join(sec[a + 1:b])


def bullet(sec, prefix):
    for l in sec:
        if l.startswith("- " + prefix):
            return l[2 + len(prefix):].strip()
    return None


def alts(raw):
    out = []
    for item in raw.split(" · "):
        item = re.sub(r"^\d+ ", "", item.strip())
        if item.startswith('"') and item.endswith('"') and item.count('"') == 2:
            item = item[1:-1]
        out.append(item)
    return out


def files(folder, stem, n, alt_list, ext="png"):
    assert len(alt_list) == n, (stem, len(alt_list), n)
    return [{"path": f"{folder}/{stem}_{k}.{ext}", "alt": alt_list[k - 1]} for k in range(1, n + 1)]


BIO = "https://getday60.com/try?utm_source=instagram&utm_medium=social&utm_campaign=bio"
LI_TAG = ('Tag the Day60 page: where the text says "Day60", type @Day60 and pick the company page '
          '(linkedin.com/company/144030699). No link in the body. Post the first comment yourself right after the post goes live.')
IG_BASE = ("Post as a carousel, slides in the order listed. Add each slide's alt text (in the Instagram app: "
           "Advanced settings, then Accessibility). Captions can't hold clickable links; the bio link stays as it is.")
FB_BASE = ("Post on the Day60 Facebook Page in Meta Business Suite. The link stays in the text, as written. "
           "Add each image's alt text.")


def entry(week, pid, **kw):
    sec = section(week, pid)
    e = {"id": kw.get("id", f"{week}-{pid}"), "week": week, "channel": kw["channel"], "topic": "day60",
         "date": kw["date"], "time": kw["time"], "status": kw["status"], "title": kw["title"],
         "format": kw["format"], "text": text_of(sec), "firstComment": "", "link": "",
         "files": kw.get("files", []), "notes": kw.get("notes", ""), "postedVia": kw.get("postedVia", "")}
    if kw["channel"] == "linkedin":
        fc = bullet(sec, "First comment:") or ""
        e["firstComment"] = kw.get("firstComment", fc)
    if "link" in kw:
        e["link"] = kw["link"]
    elif kw["channel"] == "facebook":
        e["link"] = bullet(sec, "Link:") or ""
    elif kw["channel"] == "instagram":
        e["link"] = BIO
    if kw.get("guide"):  # guide of the week (HQ, Nov 19): the slug HQ counts guide readers against
        e["guide"] = kw["guide"]
    return e


W46, W47 = "2026-w46", "2026-w47"
F46, F47 = "2026-11/wk46", "2026-11/wk47"
s46 = lambda pid: section(W46, pid)
s47 = lambda pid: section(W47, pid)

ig7_alts = alts(bullet(s46("IG7"), "Alt text (per slide):"))
fb3_alts = alts(bullet(s46("FB3"), "Alt text (per slide):"))
four_alts = alts(bullet(s47("IG-four"), "Alt text (per slide):"))

FB1_ALT = "Day60 in one picture. It is: a 60-day sprint, the 4 people closest to the hire, a short note in your voice, you hit send. It isn't: an auto-apply bot, a LinkedIn login, mass messages, keyword stuffing."
SPECS = [
    entry(W46, "LI3-new", channel="linkedin", date="2026-11-12", time="08:30", status="approved",
          title="Day60 for Chrome on LinkedIn", format="document",
          files=[{"path": f"{F46}/p17_ext_linkedin.pdf", "alt": "Day60 for Chrome on LinkedIn"}]
                + files(F46, "p17_ext_linkedin", 5, ig7_alts),
          notes=LI_TAG + ' Upload the PDF as a document and give it the title "Day60 for Chrome on LinkedIn" '
                '(LinkedIn asks for a title, and document pages have no alt text). The 5 page images are the same '
                'slides, for reference only.'),
    entry(W46, "IG4", channel="instagram", date="2026-11-12", time="19:00", status="approved",
          title="Three touches, then stop", format="carousel",
          files=files(F46, "p06_three_touches", 6, alts(bullet(s46("IG4"), "Alt text (per slide):"))),
          notes=IG_BASE + " Before posting, check getday60.com/try still lets you try one job free (the caption and slide 6 say so)."),
    entry(W46, "IG6", channel="instagram", date="2026-11-13", time="12:00", status="approved",
          title="Would Tick let you send it", format="carousel",
          files=files(F46, "p15_checker", 7, alts(bullet(s46("IG6"), "Alt text (per slide):"))),
          link=bullet(s46("IG6"), "Link (bio stays /try; this goes in the caption as text):"),
          notes=IG_BASE + " The message-checker link is already in the caption as plain text; it isn't clickable, "
                "and the bio link doesn't change."),
    entry(W46, "FB6", channel="facebook", date="2026-11-13", time="18:00", status="approved",
          title="Even our 404 page works", format="image",
          files=[{"path": f"{F46}/p16_tick_404.png",
                  "alt": bullet(s46("FB6"), "Alt text:")}],
          notes=FB_BASE + " One image. Before posting, check getday60.com/try still offers the free sprint with no card; if it doesn't, ask HQ for a new last line."),
    entry(W46, "IG5", channel="instagram", date="2026-11-14", time="10:00", status="approved",
          title="The extension in three steps", format="carousel",
          files=files(F46, "p14_ext_steps", 6, alts(bullet(s46("IG5"), "Alt text (per slide):"))),  # own alts since Nov 15
          notes=IG_BASE),
    entry(W46, "LI1", channel="linkedin", date="2026-11-17", time="08:30", status="approved",
          title="What Day60 is and isn't", format="image",
          files=[{"path": f"{F46}/p02_is_isnt_card.png", "alt": bullet(s46("LI1"), "Alt text:")}],
          notes=LI_TAG + " Add the image's alt text when you upload it. After it posts, add it to the Featured "
                "section of your profile. Moved from Mon Nov 16 (Day60's LinkedIn days are Tue and Thu)."),
    entry(W47, "IG-four", channel="instagram", date="2026-11-17", time="12:00", status="approved",
          title="Every job has 4 people", format="carousel",
          files=files(F47, "p01_four_people", 6, four_alts),
          notes=IG_BASE + " Draft: waits for Philip's approval on Fri Nov 13."),
    entry(W47, "FB-four", channel="facebook", date="2026-11-18", time="18:00", status="approved",
          title="Four people who decide", format="carousel",
          files=files(F47, "p01_four_people", 6, alts(bullet(s47("FB-four"), "Alt text (per slide):"))),
          notes=FB_BASE + " Upload the 6 images in the order listed (same slides as IG-four). "
                "Draft: waits for Philip's approval on Fri Nov 13."),
    entry(W47, "LI-thread", channel="linkedin", date="2026-11-19", time="08:30", status="approved",
          title="Most job searches are single-threaded", format="text",
          notes=LI_TAG + " Text only, no image. Draft: waits for Philip's approval on Fri Nov 13."),
]


# ---------------------------------------------------------------- backfill (everything else)
W45, W48, W49 = "2026-w45", "2026-w48", "2026-w49"
F1 = "2026-11/wk1"
s45 = lambda pid: section(W45, pid)
s49 = lambda pid: section(W49, pid)
W02 = "2027-w02"
s02 = lambda pid: section(W02, pid)
HIST = " History only: don't repost or reuse."


def posted(sent):
    return "Posted through Buffer (sent " + sent + " CT)."


alt27 = alts(bullet(s45("IG-27of39"), "Alt text:"))[0]
alt2m = bullet(s45("IG-two-messages"), "Alt text:")
alt4p = alts(bullet(s45("IG-four-people"), "Alt text (per slide):"))
ONE_CLICK = "media/chrome-extension/screenshot-0-one-click.png"
alt_one_click = bullet(s45("FBX"), "Alt text:")
igx_alts = alts(bullet(s45("IGX"), "Alt text:"))
ph_alt = bullet(s02("IG-PH"), "Alt text:")
REEL_ALT = ("Reel: paste a job link, Day60 finds the 4 people closest to the hire, Tick checks the message, you send it. "
            "Invented company and people, labeled.")

BACKFILL = [
    # week 45 (Nov 1-7): sent before the plan tracked them, plus the extension launch set
    entry(W45, "LI-3in100", channel="linkedin", date="2026-11-02", time="08:32", status="posted", postedVia="buffer",
          title="About 3 in 100", format="image", firstComment="",
          files=[{"path": f"{F1}/p01_li_3in100.png", "alt": bullet(s45("LI-3in100"), "Alt text:")}],
          notes=posted("8:32 AM") + " Link in the body (week 1 pattern), shortened by LinkedIn. Cites a competitor's data, which the rules no longer allow." + HIST),
    entry(W45, "IG-27of39", channel="instagram", date="2026-11-02", time="12:06", status="posted", postedVia="buffer",
          title="39 applications, 27 interviews", format="image", link="",
          files=[{"path": f"{F1}/p01_27of39.png", "alt": alt27}],
          notes=posted("12:06 PM") + " The 39/27 figures are retired (Nov 4)." + HIST),
    entry(W45, "FB-27of39", channel="facebook", date="2026-11-02", time="18:02", status="posted", postedVia="buffer",
          title="39 applications, 27 interviews", format="image",
          files=[{"path": f"{F1}/p01_27of39.png", "alt": alt27}],
          notes=posted("6:02 PM") + " The 39/27 figures are retired (Nov 4)." + HIST),
    entry(W45, "LI-four-people", channel="linkedin", date="2026-11-04", time="08:31", status="posted", postedVia="buffer",
          title="Every job has four people", format="document", firstComment="",
          files=[{"path": f"{F1}/p02_four_people_linkedin.pdf", "alt": "Every job has 4 people who decide if you get it"}]
                + files(F1, "p02_four_people", 6, alt4p),
          notes=posted("8:31 AM") + ' Document title: "Every job has 4 people who decide if you get it". No first comment.'),
    entry(W45, "IG-four-people", channel="instagram", date="2026-11-04", time="12:09", status="posted", postedVia="buffer",
          title="Meet the four people", format="carousel", link="",
          files=files(F1, "p02_four_people", 6, alt4p), notes=posted("12:09 PM")),
    entry(W45, "FB-four-people", channel="facebook", date="2026-11-04", time="18:03", status="posted", postedVia="buffer",
          title="Reach more of the four", format="carousel",
          files=files(F1, "p02_four_people", 6, alt4p), notes=posted("6:03 PM")),
    entry(W45, "LIX", channel="linkedin", date="2026-11-05", time="11:03", status="posted", postedVia="buffer",
          title="The Chrome extension is live", format="image", firstComment="",
          link=bullet(s45("LIX"), "Link:"),
          files=[{"path": ONE_CLICK, "alt": bullet(s45("LIX"), "Alt text 1:")}],
          notes=posted("11:03 AM") + " Link in the body (week 1 pattern; LinkedIn shortened it). HQ tagged the Day60 page on \"Day60 icon\". Its second image was removed in Buffer on Nov 5."),
    entry(W45, "LI-two-messages", channel="linkedin", date="2026-11-06", time="08:31", status="posted", postedVia="buffer",
          title="Two messages, same job", format="image", firstComment="",
          files=[{"path": f"{F1}/p03_two_messages.png", "alt": alt2m}],
          notes=posted("8:31 AM") + " Philip posted the first comment by hand; its link wasn't recorded."),
    entry(W45, "IG-two-messages", channel="instagram", date="2026-11-06", time="12:07", status="posted", postedVia="buffer",
          title="Which one would you answer", format="image", link="",
          files=[{"path": f"{F1}/p03_two_messages.png", "alt": alt2m}], notes=posted("12:07 PM")),
    entry(W45, "FB-two-messages", channel="facebook", date="2026-11-06", time="18:02", status="posted", postedVia="buffer",
          title="Almost everyone sends A", format="image",
          files=[{"path": f"{F1}/p03_two_messages.png", "alt": alt2m}], notes=posted("6:02 PM")),
    entry(W45, "IGX", channel="instagram", date="2026-11-07", time="10:05", status="posted", postedVia="buffer",
          title="One click into Day60", format="carousel", link="",
          files=[{"path": "2026-11/wk46/p10_chrome_extension.png", "alt": igx_alts[0]},
                 {"path": f"{F1}/p11_ext_one_click.png", "alt": igx_alts[1]}],
          notes=posted("10:05 AM") + " Its third slide was removed in Buffer on Nov 5."),
    entry(W45, "FBX", channel="facebook", date="2026-11-07", time="11:03", status="posted", postedVia="buffer",
          title="Saves a lot of copy-pasting", format="image",
          files=[{"path": ONE_CLICK, "alt": alt_one_click}], notes=posted("11:03 AM")),
    # week 46 (Nov 8-14): posted before the pause
    entry(W46, "IG1", channel="instagram", date="2026-11-08", time="11:03", status="posted", postedVia="buffer",
          title="Is and isn't carousel", format="carousel",
          files=files(F46, "p01_is_isnt", 7, alts(bullet(s46("IG1"), "Alt text (per slide):"))),
          notes=posted("11:03 AM") + " Meant to be pinned to the top of the grid."),
    entry(W46, "IG2", channel="instagram", date="2026-11-09", time="12:04", status="posted", postedVia="buffer",
          title="How it works Reel", format="video",
          files=[{"path": f"{F46}/p13_how_it_works_reel.mp4", "alt": REEL_ALT}],
          notes=posted("12:04 PM") + " Reel, 18 s, silent; cover is the first frame."),
    entry(W46, "FB3", channel="facebook", date="2026-11-10", time="18:02", status="posted", postedVia="buffer",
          title="Extension FAQ, five questions", format="carousel",
          files=files(F46, "p14_ext_steps", 6, fb3_alts), notes=posted("6:02 PM")),
    entry(W46, "LI2", channel="linkedin", date="2026-11-11", time="08:31", status="posted", postedVia="buffer",
          title="722 applicants in 24 hours", format="image",
          files=[{"path": f"{F46}/p05_722.png", "alt": bullet(s46("LI2"), "Alt text:")}],
          notes=posted("8:31 AM") + " Philip posts the first comment by hand."),
    # week 46: gated draft and cut posts
    entry(W46, "IG7", channel="instagram", date="2026-11-10", time="12:00", status="approved",
          title="Extension LinkedIn steps carousel", format="carousel",
          link=bullet(s46("IG7"), "Link in bio stays /try. Caption link for reference:"),
          files=files(F46, "p17_ext_linkedin", 5, ig7_alts),
          notes="Gated draft, not planned: Instagram is at 5 a week, so it runs only if Philip picks the Instagram post it replaces. "
                "The date is its old slot. LI3-new uses the same slides."),
    entry(W46, "IG3", channel="instagram", date="2026-11-11", time="12:00", status="replaced",
          title="Faster applying, same pile", format="video",
          files=[{"path": f"{F46}/p08_faster_vs_decides_reel.mp4", "alt": ""}],
          notes="Cut Nov 5 (Instagram capped at 5; it repeated IG1's point). Never posted."),
    entry(W46, "FB1", channel="facebook", date="2026-11-08", time="19:00", status="replaced",
          title="Day60 in plain English", format="image",
          files=[{"path": f"{F46}/p02_is_isnt_card.png", "alt": FB1_ALT}],  # replaced post keeps LI1's old alt
          notes="Cut Nov 5 (Facebook down to 2 posts a week). Never posted."),
    entry(W46, "FB2", channel="facebook", date="2026-11-09", time="18:00", status="replaced",
          title="What it never sends", format="video",
          files=[{"path": f"{F46}/p09_never_do_reel.mp4", "alt": ""}],
          notes="Cut Nov 5 (Facebook down to 2 posts a week). Never posted."),
    entry(W46, "FB4", channel="facebook", date="2026-11-12", time="18:00", status="replaced",
          title="Paste a job link Reel", format="video",
          files=[{"path": f"{F46}/p13_how_it_works_reel.mp4", "alt": REEL_ALT}],
          notes="Cut Nov 5 (Facebook down to 2 posts a week). Never posted."),
    entry(W46, "FB5", channel="facebook", date="2026-11-14", time="11:00", status="replaced",
          title="Where Day60 fits", format="image",
          files=[{"path": f"{F46}/p04_where_it_fits.png", "alt": bullet(s46("FB5"), "Alt text:")}],
          notes="Cut Nov 5 (Facebook down to 2 posts a week). Never posted."),
    # week 47: replaced
    entry(W47, "LI-founder", channel="linkedin", date="2026-11-17", time="08:30", status="replaced",
          title="Before sales, the ministry story", format="text", firstComment="",
          link=bullet(s47("LI-founder"), "Link:"),
          notes="Replaced by week 48's LI-story (Philip, Nov 8); it never had a final date, so it shows on week 47's Tuesday. Don't post: the ministry lines are on hold until Philip confirms them."),
    entry(W47, "IG-resume", channel="instagram", date="2026-11-15", time="11:00", status="draft",
          title="One resume, tailored to one job", format="carousel",
          link="https://getday60.com/resume-builder?utm_source=instagram&utm_medium=social&utm_campaign=2026-w47&utm_content=resume-builder",
          files=files(F47, "p02_resume_builder", 6, alts(bullet(s47("IG-resume"), "Alt text (per slide):")))),
    entry(W47, "FB-resume", channel="facebook", date="2026-11-20", time="18:00", status="draft",
          title="Free resume builder for one job", format="carousel",
          files=[dict(f, path=f["path"].replace("_6.png", "_6_fb.png")) for f in files(F47, "p02_resume_builder", 6, alts(bullet(s47("FB-resume"), "Alt text (per slide):")))]),
    entry(W48, "LI-resume", channel="linkedin", date="2026-11-24", time="08:30", status="draft", postedVia="native",
          title="I tailored my own resume", format="text"),
    # week 48
    # Moved to Tue Dec 8 (week 50) when LI-email took Tue Dec 1 (HQ, Nov 18).
    entry("2026-w50", "LI-story", id="2026-w48-LI-story", channel="linkedin", date="2026-12-08", time="12:07", status="draft",
          title="Phil's own job search story", format="text",  # no link (HQ, Nov 19)
          notes="Reserved, not drafted: Social writes it after HQ forwards Phil's Nov 9 post. Moved to Tue Dec 8: LI-email took Tue Dec 1. "
                + LI_TAG),
    # week 49
    # Rewritten Nov 19 (HQ): text only, the launch link in the last line, so it waits for HQ's approval again.
    entry(W02, "LI-PH", id="2026-w49-LI-PH", channel="linkedin", date="2027-01-12", time="08:21", status="draft",
          title="Product Hunt launch day", format="text",
          notes=LI_TAG + " Add the image's alt text when you upload it. The first comment is a placeholder until the Product Hunt launch link exists. Draft."),
    entry(W02, "IG-PH", id="2026-w49-IG-PH", channel="instagram", date="2027-01-12", time="07:53", status="approved",
          title="Product Hunt launch day", format="image",
          files=[{"path": "product-hunt/ig_launch_day.png", "alt": ph_alt}],
          notes="Add the image's alt text (in the Instagram app: Advanced settings, then Accessibility). Captions can't hold clickable links; the bio link stays as it is. Draft."),
    entry(W02, "FB-PH", id="2026-w49-FB-PH", channel="facebook", date="2027-01-12", time="07:28", status="approved",  # cut Nov 19, restored the same day (Philip: Facebook 3 a week)
          title="Product Hunt launch day", format="image",
          link="https://getday60.com/try?utm_source=facebook&utm_medium=social&utm_campaign=2027-w02&utm_content=product-hunt",
          files=[{"path": "product-hunt/ig_launch_day.png", "alt": ph_alt}],
          notes=FB_BASE + " The text also needs the Product Hunt launch link, a placeholder until it exists. Draft."),
    # A text post from Nov 19 (HQ: no more LinkedIn PDFs, no link). The v2 PDF stays in the repo.
    entry(W49, "LI-3touch", channel="linkedin", date="2026-12-03", time="12:54", status="approved",  # HQ, Nov 19
          title="Follow up three times, then stop", format="text",
          notes="Copy not written yet (moved from week 47). " + LI_TAG + " Upload the PDF as a document and give it a title."),
]
SPECS += BACKFILL

# HQ brief, Thu Nov 12: the first action. Week 47's last 3 Instagram slots and week 48's Instagram and Facebook.
F48 = "2026-11/wk48"
s48 = lambda pid: section("2026-w48", pid)


def one_alt(sec):
    a = bullet(sec, "Alt text:")
    return a[1:-1] if a.startswith('"') and a.endswith('"') and a.count('"') == 2 else a


def video(path, sec):
    return [{"path": path, "alt": one_alt(sec)}]


FIRST_ACTION = [
    entry(W47, "IG-onejob", channel="instagram", date="2026-11-18", time="12:00", status="draft",
          title="Start with one job", format="video",
          files=video(f"{F47}/p03_one_job_reel.mp4", s47("IG-onejob"))),
    entry(W47, "IG-redpen", channel="instagram", date="2026-11-19", time="19:00", status="draft",
          title="Cut your first message", format="video",
          files=video(f"{F47}/p04_red_pen_reel.mp4", s47("IG-redpen"))),
    entry(W47, "IG-firstjob", channel="instagram", date="2026-11-21", time="10:00", status="draft",
          title="Your first job, step by step", format="carousel",
          files=files(F47, "p05_first_job", 6, alts(bullet(s47("IG-firstjob"), "Alt text (per slide):")))),
    entry("2026-w48", "IG-thanks", channel="instagram", date="2026-11-22", time="11:00", status="draft",
          title="Send one thank-you this week", format="carousel",
          files=files(F48, "p01_thanks", 6, alts(bullet(s48("IG-thanks"), "Alt text (per slide):")))),
    entry("2026-w48", "IG-which", channel="instagram", date="2026-11-23", time="12:00", status="draft",
          title="Which would you answer?", format="image",
          files=[{"path": f"{F48}/p02_which.png", "alt": one_alt(s48("IG-which"))}]),
    entry("2026-w48", "IG-rb-reel", channel="instagram", date="2026-11-24", time="12:00", status="draft",
          title="The resume builder, as a Reel", format="video",
          files=video(f"{F48}/p03_resume_reel.mp4", s48("IG-rb-reel"))),
    entry("2026-w48", "FB-which", channel="facebook", date="2026-11-24", time="18:00", status="draft", postedVia="native",
          title="Which last line would you answer?", format="image",
          files=[{"path": f"{F48}/p02_which.png", "alt": one_alt(s48("IG-which"))}]),
    entry("2026-w48", "IG-onelink", channel="instagram", date="2026-11-25", time="12:00", status="draft",
          title="One link, four people", format="video",
          files=video(f"{F48}/p04_one_link_reel.mp4", s48("IG-onelink"))),
    entry("2026-w48", "FB-thanks", channel="facebook", date="2026-11-26", time="10:00", status="draft", postedVia="native",
          title="Thanksgiving: send one thank-you", format="carousel",
          files=files(F48, "p01_thanks", 6, alts(bullet(s48("IG-thanks"), "Alt text (per slide):")))),
    entry("2026-w48", "IG-shortlist", channel="instagram", date="2026-11-28", time="10:00", status="draft",
          title="Long weekend, short list", format="image",
          files=[{"path": f"{F48}/p05_short_list.png", "alt": one_alt(s48("IG-shortlist"))}]),
]
SPECS += FIRST_ACTION

# Covers on palette grounds (Philip, Fri Nov 13 via HQ: "too much cream" in the Instagram grid).
# Source: 2026-11/build_covers.py. Carousels and images swap slide 1; Reels list the cover PNG after the video.
# Facebook posts that reuse an Instagram cover take the same file. The old cream covers stay on disk.
_C46, _C47, _C48 = "2026-11/wk46/", "2026-11/wk47/", "2026-11/wk48/"
COVER = {
    "2026-w46-IG7": _C46 + "p17_ext_linkedin_1_cobalt.png",
    "2026-w46-IG5": _C46 + "p14_ext_steps_1_mint.png",
    "2026-w47-IG-resume": _C47 + "p02_resume_builder_1_lime.png",
    "2026-w47-FB-resume": _C47 + "p02_resume_builder_1_lime.png",
    "2026-w47-IG-four": _C47 + "p01_four_people_1_ink.png",
    "2026-w47-FB-four": _C47 + "p01_four_people_1_ink.png",
    "2026-w47-IG-onejob": _C47 + "p03_one_job_cover_coral.png",
    "2026-w47-IG-redpen": _C47 + "p04_red_pen_cover_mint.png",
    "2026-w47-IG-firstjob": _C47 + "p05_first_job_1_lime.png",
    "2026-w48-IG-thanks": _C48 + "p01_thanks_1_pink.png",
    "2026-w48-FB-thanks": _C48 + "p01_thanks_1_pink.png",
    "2026-w48-IG-which": _C48 + "p02_which_ink.png",
    "2026-w48-FB-which": _C48 + "p02_which_ink.png",
    "2026-w48-IG-rb-reel": _C48 + "p03_resume_cover_cobalt.png",
    "2026-w48-IG-onelink": _C48 + "p04_one_link_cover_mint.png",
    "2026-w48-IG-shortlist": _C48 + "p05_short_list_coral.png",
    "2026-w46-IG2": _C46 + "p13_how_it_works_cover_ink.png",  # published Reel: optional swap
}
_spec_ids = {e["id"] for e in SPECS}
assert set(COVER) <= _spec_ids, set(COVER) - _spec_ids
for e in SPECS:
    c = COVER.get(e["id"])
    if c and e["format"] == "video" and e["status"] in ("draft", "approved"):
        # Alt text rule (Philip, Nov 15): the video keeps an empty alt; the cover carries what the Reel is for.
        e["files"] = [dict(e["files"][0], alt="")] + [{"path": c, "alt": e["files"][0]["alt"]}]
    elif c and e["format"] == "video":
        e["files"] = e["files"] + [{"path": c, "alt": ""}]
    elif c:
        e["files"] = [{"path": c, "alt": e["files"][0]["alt"]}] + e["files"][1:]

# Ink slides v2 (HQ, Nov 13): lime is never text, and on ink Tick, cards and stickers get a cream keyline.
# Unpublished posts point at the _v2 files; the old files stay on disk (LI3-new, live, keeps p17_ext_linkedin_5.png).
_V2 = {"p14_ext_steps_6.png", "p17_ext_linkedin_5.png", "p01_four_people_6.png", "p02_resume_builder_6.png",
       "p02_resume_builder_6_fb.png", "p05_first_job_6.png", "p01_thanks_6.png", "p03_one_job_reel.mp4",
       "p04_red_pen_reel.mp4", "p03_resume_reel.mp4", "p04_one_link_reel.mp4"}
_V2_IDS = {"2026-w46-IG7", "2026-w46-IG5", "2026-w47-IG-resume", "2026-w47-FB-resume", "2026-w47-IG-four",
           "2026-w47-FB-four", "2026-w47-IG-onejob", "2026-w47-IG-redpen", "2026-w47-IG-firstjob", "2026-w48-IG-thanks",
           "2026-w48-FB-thanks", "2026-w48-IG-rb-reel", "2026-w48-IG-onelink"}
assert _V2_IDS <= _spec_ids, _V2_IDS - _spec_ids
_v2_hits = set()
for e in SPECS:
    if e["id"] in _V2_IDS:
        for f in e["files"]:
            d, b = f["path"].rsplit("/", 1)
            if b in _V2:
                stem, ext = b.rsplit(".", 1)
                f["path"] = f"{d}/{stem}_v2.{ext}"
                _v2_hits.add(b)
assert _v2_hits == _V2, _V2 - _v2_hits
# FB-four's slide 6 for Facebook (HQ, Nov 14): getday60.com sticker in place of "Link in bio".
_fb4 = next(e for e in SPECS if e["id"] == "2026-w47-FB-four")
assert _fb4["files"][5]["path"].endswith("/p01_four_people_6_v2.png"), _fb4["files"][5]
_fb4["files"][5] = dict(_fb4["files"][5], path=_fb4["files"][5]["path"].replace("_6_v2.png", "_6_fb_v2.png"))

# Feed safe area (HQ, Nov 16): the four Instagram posts Philip scheduled natively, and the Facebook posts that reuse
# their slides, point at _safe files (rendered with every word inside y 150 to 1200). The old files stay on disk.
_SAFE_IDS = {"2026-w47-IG-firstjob", "2026-w48-IG-thanks", "2026-w48-FB-thanks", "2026-w48-IG-which",
             "2026-w48-FB-which", "2026-w48-IG-shortlist",
             # HQ, Nov 16 (second message): the rest of the natively scheduled feed posts.
             "2026-w47-IG-four", "2026-w47-FB-four", "2026-w47-FB-resume", "2026-w46-IG7",
             "2026-w49-IG-PH", "2026-w49-FB-PH"}  # HQ, Nov 16 (third message): the launch-day image
assert _SAFE_IDS <= _spec_ids, _SAFE_IDS - _spec_ids
for e in SPECS:
    if e["id"] in _SAFE_IDS:
        for f in e["files"]:
            assert f["path"].endswith(".png"), f
            f["path"] = f["path"][:-4] + "_safe.png"
            assert os.path.exists(os.path.join(ROOT, f["path"])), f["path"]

# HQ brief, Wed Nov 18: a post going around says to email the person who posted the job, but not which person or
# what to say. Week 49's answer: the 4 people. Rendered inside the feed safe area from the start (2026-11/wk49/build.py).
F49 = "2026-11/wk49"
s49 = lambda pid: section(W49, pid)


def _which_person(pid, last):
    a = alts(bullet(s49(pid), "Alt text (per slide):"))
    assert len(a) == 6, (pid, len(a))
    paths = [f"{F49}/p01_which_person_1_ink.png"] + [f"{F49}/p01_which_person_{k}.png" for k in range(2, 6)] + [f"{F49}/{last}"]
    for x in paths:
        assert os.path.exists(os.path.join(ROOT, x)), x
    return [{"path": x, "alt": a[k]} for k, x in enumerate(paths)]


SPECS += [
    entry(W49, "LI-email", channel="linkedin", date="2026-12-01", time="08:46", status="approved",  # HQ, Nov 19 (line swapped and restored the same day)
          title="Which person to email first", format="text"),
    entry(W49, "IG-email", channel="instagram", date="2026-11-27", time="21:43", status="approved", postedVia="buffer",  # moved up (HQ, Nov 22); Post Library approval, Nov 19
          title="Email the person. But which one?", format="carousel",
          files=_which_person("IG-email", "p01_which_person_6.png")),
    entry(W49, "FB-email", channel="facebook", date="2026-11-23", time="20:04", status="approved", postedVia="buffer",  # cut Nov 19, restored the same day
          title="Which person to email first", format="carousel",
          files=_which_person("FB-email", "p01_which_person_6_fb.png")),
]

# HQ, Nov 19: Social writes all 5 LinkedIn posts. Mon, Wed, Fri are Phil's founder lane; Thanksgiving gets a light post.
SPECS += [
    entry(W48, "LI-thanks", channel="linkedin", date="2026-11-26", time="09:47", status="approved", postedVia="buffer",
          title="Thanksgiving: one thank-you today", format="text"),
    entry(W49, "LI-hiringside", channel="linkedin", date="2026-12-02", time="11:36", status="approved",
          title="Three things from the hiring side", format="text"),
    entry(W49, "LI-target", channel="linkedin", date="2026-12-04", time="09:07", status="draft",
          title="Run your search like target accounts", format="text"),
]



def _find_hm(pid, last):
    a = alts(bullet(s49(pid), "Alt text (per slide):"))
    assert len(a) == 7, (pid, len(a))
    paths = [f"{F49}/p02_find_hm_1_lime.png"] + [f"{F49}/p02_find_hm_{k}.png" for k in range(2, 7)] + [f"{F49}/{last}"]
    for x in paths:
        assert os.path.exists(os.path.join(ROOT, x)), x
    return [{"path": x, "alt": a[k]} for k, x in enumerate(paths)]


# Guide of the week 1 (HQ, Nov 19): Instagram and Facebook in week 49; LinkedIn on Thu Dec 10 (week 50)
SPECS += [
    entry(W49, "IG-findhm", channel="instagram", date="2026-12-02", time="15:27", status="approved",  # HQ, Nov 19, at 5848cd8
          title="How to find the hiring manager", format="carousel", guide="how-to-find-the-hiring-manager",
          files=_find_hm("IG-findhm", "p02_find_hm_7.png")),
    entry(W49, "FB-findhm", channel="facebook", date="2026-12-03", time="08:31", status="approved",  # HQ, Nov 19, at 5848cd8
          title="How to find the hiring manager", format="carousel", guide="how-to-find-the-hiring-manager",
          files=_find_hm("FB-findhm", "p02_find_hm_7_fb.png")),
]

# Recycled Instagram posts (HQ, Nov 22): the 14 posts Philip scheduled in the Instagram app were cropped to a square. Each gets a new copy, id =
# the original's + "-r2", filed in the week it now runs: the same images at 1080x1350 (the _safe renders, inside the 3:4
# grid), a lightly refreshed caption, Buffer only. The originals stay as history: posted (native), or replaced if still ahead.
from recycle_def import R as _R, SWAP as _SWAP, THANKS as _THANKS, THIS_WEEK as _TW  # noqa: E402
_by = {e["id"]: e for e in SPECS}
_BUF_NOV23 = {"2026-w46-IG6", "2026-w46-IG7"}  # created in Buffer by Social, Nov 23 (HQ brief)
_AHEAD = {"2026-w48-IG-which", "2026-w48-IG-rb-reel", "2026-w48-IG-onelink", "2026-w48-IG-shortlist"}
for r in _R:
    o = _by[r["orig"]]
    fs = []
    for f in o["files"]:
        p, a = _SWAP.get(f["path"], f["path"]), f["alt"]
        if p in _THANKS:
            p, a = _THANKS[p]
        assert os.path.exists(os.path.join(ROOT, p)), p
        fs.append({"path": p, "alt": a})
    e = entry(r["week"], r["pid"], id=r["orig"] + "-r2", channel="instagram", date=r["date"], time=r["time"],
              status=r["status"], title=r["title"], format=o["format"], files=fs,
              postedVia="buffer" if (_TW.get(r["orig"], {}).get("buffer") or r["orig"] in _BUF_NOV23) else "")
    assert e["text"] == r["cap"], r["pid"]
    sec = section(r["week"], r["pid"])
    if o["format"] == "carousel":
        assert alts(bullet(sec, "Alt text (per slide):")) == [f["alt"] for f in fs], r["pid"]
    elif o["format"] == "image":
        assert bullet(sec, "Alt text:") == fs[0]["alt"], r["pid"]
    else:
        assert bullet(sec, "Alt text (cover):") == fs[1]["alt"], r["pid"]
    SPECS.append(e)
    o["status"] = "replaced" if r["orig"] in _AHEAD else "posted"
    o["postedVia"] = "native"

# FB-onelink (Nov 22): IG-onelink's approved words and Reel, adapted for Facebook; new, for HQ
_fo = section("2026-w48", "FB-onelink")
SPECS.append(entry("2026-w48", "FB-onelink", channel="facebook", date="2026-11-28", time="22:54", status="approved", postedVia="buffer",
                   title="One link, four people", format="video",
                   files=[{"path": "2026-11/wk48/p04_one_link_reel_fb_cover.mp4", "alt": ""},
                          {"path": "2027-01/wk03/p04_one_link_cover_mint_grid.png", "alt": bullet(_fo, "Alt text (cover):")}]))

# Drafts for HQ, Nov 23 (Social): Facebook this week, the Thanksgiving card, the first Sunday LinkedIn post, humor
def _one(week, pid, path, label="Alt text:"):
    assert os.path.exists(os.path.join(ROOT, path)), path
    return [{"path": path, "alt": bullet(section(week, pid), label)}]


SPECS += [
    entry(W48, "FB-onejob", channel="facebook", date="2026-11-25", time="09:36", status="approved", postedVia="buffer",
          title="Start with one job", format="video",
          files=[{"path": "2026-11/wk47/p03_one_job_reel_fb_cover.mp4", "alt": ""}]
                + _one(W48, "FB-onejob", "2027-01/wk03/p03_one_job_cover_coral_grid.png", "Alt text (cover):")),
    entry(W48, "IG-thanksgiving", channel="instagram", date="2026-11-26", time="08:11", status="approved", postedVia="buffer",
          title="Pass the stuffing", format="image",
          files=_one(W48, "IG-thanksgiving", "2026-11/wk48/p06_pass_the_stuffing_pink.png")),
    entry(W48, "FB-blackfriday", channel="facebook", date="2026-11-27", time="07:57", status="approved", postedVia="buffer",
          title="Black Friday deal", format="text"),
    entry(W49, "FB-shortlist", channel="facebook", date="2026-11-29", time="09:34", status="approved", postedVia="buffer",
          title="Long weekend, short list", format="image",
          files=_one(W49, "FB-shortlist", "2026-11/wk48/p05_short_list_coral_safe.png")),
    entry(W49, "LI-monday", channel="linkedin", date="2026-11-29", time="11:52", status="approved", postedVia="buffer",
          title="Monday plan: one note by 10", format="text"),
    entry(W49, "LI-glossary", channel="linkedin", date="2026-11-30", time="09:13", status="approved", postedVia="buffer",
          title="Job posting glossary", format="text"),
    entry(W49, "IG-breaking", channel="instagram", date="2026-11-30", time="20:27", status="approved", postedVia="buffer",
          title="Hiring manager answers cold email", format="image",
          files=_one(W49, "IG-breaking", "2026-11/wk49/p02_breaking_lime.png")),
    entry(W49, "FB-breaking", channel="facebook", date="2026-12-01", time="07:34", status="approved", postedVia="buffer",
          title="Hiring manager answers cold email", format="image",
          files=_one(W49, "FB-breaking", "2026-11/wk49/p02_breaking_lime.png")),
]

# HQ idea, Nov 24: "The ATS didn't reject you" (drafts for HQ)
SPECS += [
    entry("2026-w50", "LI-ats", channel="linkedin", date="2026-12-07", time="11:17", status="approved",
          title="The ATS probably didn't reject you", format="text"),
    entry(W49, "FB-ats", channel="facebook", date="2026-11-30", time="19:08", status="approved",
          title="The robot didn't reject you", format="image",
          files=_one(W49, "FB-ats", "2026-11/wk49/p03_ats_coral.png")),
    entry(W49, "IG-ats", channel="instagram", date="2026-12-03", time="09:44", status="approved",
          title="The robot didn't reject you", format="image",
          files=_one(W49, "IG-ats", "2026-11/wk49/p03_ats_coral.png")),
]

# HQ, Nov 23: Philip deleted his native copies of LI-resume and FB-thanks; both go out through Buffer.
for _e in SPECS:
    if _e["id"] == "2026-w48-LI-resume":
        _e.update(time="12:43", status="approved", postedVia="buffer", firstComment="")
    elif _e["id"] == "2026-w48-FB-which":
        _e.update(time="08:36", status="approved", postedVia="buffer")
    elif _e["id"] == "2026-w48-FB-thanks":
        _e.update(time="10:23", status="approved", postedVia="buffer")
        _e["files"] = [dict(f, path="2026-11/wk48/p01_thanks_5_today.png", alt=f["alt"].replace("Send it before Thursday.", "Send it today."))
                       if f["path"].endswith("p01_thanks_5_safe.png") else f for f in _e["files"]]

# Buffer top-up Wed Nov 25 (Social): scheduled in Buffer.
_BUF_NOV25 = {"2026-w49-FB-ats", "2026-w49-IG-findhm", "2026-w49-IG-ats", "2026-w49-LI-email", "2026-w49-LI-3touch", "2026-w49-FB-findhm"}
for _e in SPECS:
    if _e["id"] in _BUF_NOV25:
        _e.update(postedVia="buffer")

from batch_w52 import specs as _b52; SPECS += _b52(entry, _one)  # noqa: E402  (December batch, week 52)
from notes import NOTES  # noqa: E402
_missing = [e["id"] for e in SPECS if e["id"] not in NOTES]
assert not _missing, _missing
for e in SPECS:
    e["notes"] = "\n".join(NOTES[e["id"]])

if __name__ == "__main__":
    out = os.path.join(ROOT, "library.json")
    old = json.load(open(out)) if os.path.exists(out) else []
    ids = {e["id"] for e in SPECS}
    allp = [e for e in old if e["id"] not in ids] + SPECS
    allp.sort(key=lambda e: (e["date"], e["time"], e["id"]))
    open(out, "w").write(json.dumps(allp, indent=2, ensure_ascii=False) + "\n")
    print(len(allp), "posts")
