"""Notes for library.json: one instruction per line, the step he's most likely to forget first (HQ, Nov 11)."""
LI = ['Tag the Day60 page: where the text says "Day60", type @Day60 and pick the company page (linkedin.com/company/144030699).',
      "Post the first comment yourself right after the post goes live.",
      "No link in the body."]
IG = ["Add each slide's alt text (Instagram app: Advanced settings, then Accessibility).",
      "Upload the slides in the order listed.",
      "No clickable links in the caption; the bio link stays as it is."]
IG_ONE = ["Add the image's alt text (Instagram app: Advanced settings, then Accessibility).",
          "No clickable links in the caption; the bio link stays as it is."]
FB_ONE = ["Add the image's alt text.", "Post as the Day60 Facebook Page in Meta Business Suite.", "The link stays in the text, as written."]
FB_CAR = ["Add each image's alt text.", "Upload the images in the order listed.",
          "Post as the Day60 Facebook Page in Meta Business Suite.", "The link stays in the text, as written."]
D13 = "Draft: waits for Philip's approval on Fri Nov 13."
D25 = "Draft: Philip approves it by Wed Nov 25."
NOT_SCHED = "Not scheduled. Philip schedules it once the Product Hunt launch link exists."
HIST = "History only: don't repost or reuse."
CUT_FB = ["Cut Nov 5: Facebook went down to 2 posts a week.", "Never posted."]


def sent(t):
    return f"Posted through Buffer (sent {t} CT)."


NOTES = {
    "2026-w47-IG-onejob": ["Post as a Reel; the cover is the first frame (it's silent, so no sound to pick).", "No clickable links in the caption; the bio link stays as it is."],
    "2026-w47-IG-redpen": ["Post as a Reel; the cover is the first frame (it's silent, so no sound to pick).", "No clickable links in the caption; the bio link stays as it is."],
    "2026-w47-IG-firstjob": IG,
    "2026-w48-IG-thanks": IG + ["FB-thanks uses the same 6 slides on Thu Nov 26."],
    "2026-w48-IG-which": IG_ONE + ["Reply to A-or-B comments; FB-which uses the same image on Tue Nov 24."],
    "2026-w48-IG-rb-reel": ["Post as a Reel; the cover is the first frame (it's silent, so no sound to pick).", "No clickable links in the caption; the bio link stays as it is."] + ["The caption names getday60.com/resume-builder as plain text; it isn't a link."],
    "2026-w48-FB-which": FB_ONE + ["Same image as IG-which (Mon Nov 23)."],
    "2026-w48-IG-onelink": ["Post as a Reel; the cover is the first frame (it's silent, so no sound to pick).", "No clickable links in the caption; the bio link stays as it is."],
    "2026-w48-FB-thanks": FB_CAR + ["Same 6 slides as IG-thanks (Sun Nov 22).", "10:00 AM on Thanksgiving Day, not the usual 6:00 PM."],
    "2026-w48-IG-shortlist": IG_ONE,
    "2026-w46-LI3-new": ['Upload the PDF as a document and title it "Day60 for Chrome on LinkedIn".'] + LI
                        + ["Document pages have no alt text; the 5 page images are the same slides, for reference only."],
    "2026-w46-IG4": ["Before posting, check getday60.com/try still lets you try one job free (the caption and slide 6 say so)."] + IG,
    "2026-w46-IG6": IG + ["The message-checker link is already in the caption as plain text; the bio link doesn't change."],
    "2026-w46-FB6": ["Post it only if free spots are still open on getday60.com/try; if they're gone, skip it (the image shows a \"Start my free sprint\" button)."] + FB_ONE,
    "2026-w46-IG5": IG,
    "2026-w46-LI1": LI + ["Add the image's alt text when you upload it.",
                          "After it posts, add it to the Featured section of your profile.",
                          "Moved from Mon Nov 16: Day60's LinkedIn days are Tue and Thu."],
    "2026-w47-IG-four": IG,
    "2026-w47-FB-four": FB_CAR + ["Same slides as IG-four, except slide 6 shows the getday60.com sticker in place of \"Link in bio\", which doesn't work on Facebook (HQ, Nov 14)."],
    "2026-w47-LI-thread": LI + ["Text only, no image."],
    "2026-w45-LI-3in100": [sent("8:32 AM"), "Link in the body (week 1 pattern), shortened by LinkedIn.",
                           "Cites a competitor's data, which the rules no longer allow.", HIST],
    "2026-w45-IG-27of39": [sent("12:06 PM"), "The 39/27 figures are retired (Nov 4).", HIST],
    "2026-w45-FB-27of39": [sent("6:02 PM"), "The 39/27 figures are retired (Nov 4).", HIST],
    "2026-w45-LI-four-people": [sent("8:31 AM"), 'Document title: "Every job has 4 people who decide if you get it".', "No first comment."],
    "2026-w45-IG-four-people": [sent("12:09 PM")],
    "2026-w45-FB-four-people": [sent("6:03 PM")],
    "2026-w45-LIX": [sent("11:03 AM"), "Link in the body (week 1 pattern), shortened by LinkedIn.",
                     'HQ tagged the Day60 page on "Day60 icon".', "Its second image was removed in Buffer on Nov 5."],
    "2026-w45-LI-two-messages": [sent("8:31 AM"), "Philip posted the first comment by hand; its link wasn't recorded."],
    "2026-w45-IG-two-messages": [sent("12:07 PM")],
    "2026-w45-FB-two-messages": [sent("6:02 PM")],
    "2026-w45-IGX": [sent("10:05 AM"), "Its third slide was removed in Buffer on Nov 5."],
    "2026-w45-FBX": [sent("11:03 AM")],
    "2026-w46-IG1": [sent("11:03 AM"), "Meant to be pinned to the top of the grid."],
    "2026-w46-IG2": [sent("12:04 PM"), "Reel, 18 s, silent; the cover is the first frame."],
    "2026-w46-FB3": [sent("6:02 PM")],
    "2026-w46-LI2": [sent("8:31 AM"), "Philip posts the first comment by hand."],
    "2026-w46-IG7": IG + ["The date shown is its old slot (Tue Nov 10); Philip set the real date when he scheduled it on Nov 11.",
                          "LI3-new uses the same slides."],
    "2026-w46-IG3": ["Cut Nov 5: Instagram capped at 5, and it repeated IG1's point.", "Never posted."],
    "2026-w46-FB1": CUT_FB, "2026-w46-FB2": CUT_FB, "2026-w46-FB4": CUT_FB, "2026-w46-FB5": CUT_FB,
    "2026-w47-LI-founder": ["Don't post: the ministry lines are on hold until Philip confirms them.",
                            "Replaced by week 48's LI-story (Philip, Nov 8).",
                            "It never had a final date, so it shows on week 47's Tuesday."],
    "2026-w47-IG-resume": IG + ["The caption names getday60.com/resume-builder as plain text; it isn't a link."],
    "2026-w47-FB-resume": FB_CAR + ["Slides 1 to 5 are IG-resume's. Slide 6 is p02_resume_builder_6_fb.png, the same slide without the \"Link in bio\" sticker, and its alt text leaves that out too."],
    "2026-w48-LI-resume": LI + ["Text only, no image."],
    "2026-w48-LI-story": ["Reserved, not drafted: Social writes it after HQ forwards Phil's Nov 9 post.",
                          "Moved to Tue Dec 8: LI-email took Tue Dec 1 (HQ, Nov 18)."] + LI,
    "2026-w49-LI-PH": [NOT_SCHED, "The first comment is a placeholder until the Product Hunt launch link exists."] + LI
                      + ["Add the image's alt text when you upload it."],
    "2026-w49-IG-PH": [NOT_SCHED] + IG_ONE,
    "2026-w49-FB-PH": [NOT_SCHED, "The text needs the Product Hunt launch link, a placeholder until it exists.",
                       "Add the image's alt text.", "Post as the Day60 Facebook Page in Meta Business Suite.",
                       "The links stay in the text, as written."],
    "2026-w49-LI-3touch": ["Copy not written yet (moved from week 47).", "Upload the PDF as a document and give it a title.",
                           "The PDF is the v2 (HQ, Nov 14): slide 6 has cream keylines on Tick and the card. The old PDF stays in the repo."] + LI,
}

# Covers on palette grounds (Philip, Fri Nov 13 via HQ: no more cream covers in the grid). The step he's most
# likely to miss goes first. The old cream covers stay in the repo.
_REEL_OLD = "Post as a Reel; the cover is the first frame (it's silent, so no sound to pick)."
_REEL_NEW = ["Cover: tap Edit cover, then Add from camera roll, and pick the PNG listed after the video. The grid shows its middle.",
             "Post as a Reel; it's silent, so there's no sound to pick."]
for _k in ("2026-w47-IG-onejob", "2026-w47-IG-redpen", "2026-w48-IG-rb-reel", "2026-w48-IG-onelink"):
    _i = NOTES[_k].index(_REEL_OLD)
    NOTES[_k] = NOTES[_k][:_i] + _REEL_NEW + NOTES[_k][_i + 1:]
_SWAP = ("Already scheduled? Before it posts, replace slide 1 with the new {g} cover listed first ({f}) "
         "and slide {n} with {v} (cream keylines on ink{lt}).")
for _k, _g, _f, _n, _v, _lt in (
        ("2026-w46-IG7", "cobalt", "p17_ext_linkedin_1_cobalt.png", 5, "p17_ext_linkedin_5_v2.png", "; no lime text"),
        ("2026-w47-IG-four", "ink", "p01_four_people_1_ink.png", 6, "p01_four_people_6_v2.png", ""),
        ("2026-w47-FB-four", "ink", "p01_four_people_1_ink.png", 6, "p01_four_people_6_fb_v2.png",
         '; getday60.com in place of "Link in bio"')):
    NOTES[_k] = [_SWAP.format(g=_g, f=_f, n=_n, v=_v, lt=_lt)] + NOTES[_k]
NOTES["2026-w46-IG5"] = ["Already scheduled for Sat Nov 14, 10:00 AM: before then, replace slide 6 with p14_ext_steps_6_v2.png "
                         "(the old slide 6 sets a line in lime text) and slide 1 with the new mint cover listed first "
                         "(p14_ext_steps_1_mint.png). If there's time for only one, swap slide 6."] + NOTES["2026-w46-IG5"]
# Ink slides and Reel end scenes rebuilt with cream keylines (HQ, Nov 13). Not yet scheduled, so no swap note.
NOTES["2026-w46-IG2"] = NOTES["2026-w46-IG2"] + [
    "Optional (Philip, Nov 13): a new ink cover is listed after the video. To use it, edit the Reel in the Instagram app, "
    "tap Edit cover, then Add from camera roll."]
# Week 49, HQ brief Nov 18: which person to email, and what to say. Rendered safe from the start (no swap note).
NOTES["2026-w49-LI-email"] = LI + ["Text only, no image."]
NOTES["2026-w49-IG-email"] = IG + ["FB-email uses slides 1 to 5 on Tue Dec 1, with its own slide 6."]
NOTES["2026-w49-FB-email"] = FB_CAR + [
    "Slides 1 to 5 are IG-email's (Mon Nov 30). Slide 6 is p01_which_person_6_fb.png, with getday60.com in place of \"Link in bio\"."]
# Feed safe area (HQ, Nov 16): Instagram may crop a feed post to a square. Every Instagram image or carousel not
# posted yet (dated Nov 17 or later, plus IG7, whose real date is unknown) gets the expand step first.
_EXPAND = "Instagram app: before Next, tap the expand button on the first photo so it shows the full 4:5."
for _k in ("2026-w46-IG7", "2026-w47-IG-four", "2026-w47-IG-firstjob", "2026-w48-IG-thanks", "2026-w48-IG-which",
           "2026-w48-IG-shortlist", "2026-w49-IG-PH", "2026-w49-IG-email"):
    NOTES[_k] = [_EXPAND] + NOTES[_k]
# The four posts Philip scheduled natively, and the Facebook posts that reuse their slides, now list _safe files
# (every word inside the centered square). Philip decides whether to swap them.
_SAFE = ("Already scheduled? These are new files (Nov 16) that keep every word inside the centered square; "
         "to use them, replace every image in the scheduled post before it goes out. The old files stay in the repo.")
for _k in ("2026-w47-IG-firstjob", "2026-w48-IG-thanks", "2026-w48-IG-which", "2026-w48-IG-shortlist",
           "2026-w48-FB-thanks", "2026-w48-FB-which",
           "2026-w47-IG-four", "2026-w47-FB-four", "2026-w47-FB-resume", "2026-w46-IG7",
           "2026-w49-IG-PH", "2026-w49-FB-PH"):
    NOTES[_k] = NOTES[_k][:1] + [_SAFE] + NOTES[_k][1:] if NOTES[_k][:1] == [_EXPAND] else [_SAFE] + NOTES[_k]

# Automatic posting (Philip, Nov 18 via HQ): every post publishes through Buffer or doesn't go out, with no step by
# hand. Posts Philip already scheduled natively keep their old notes as history. These are the posts Buffer will
# publish; their notes say what Buffer needs that the fields don't.
BUF_LI = ["Publishes through Buffer, automatically, on Philip's LinkedIn profile.",
          "Buffer posts the link as the first comment.",
          "Day60 stays untagged until HQ has the Day60 page's LinkedIn details for Buffer."]
BUF_IG = ["Publishes through Buffer, automatically, on Instagram at 1080x1350 (no expand step).",
          "Slides go up in the listed order, each with its alt text.",
          "No link in the caption; the bio link stays as it is."]
BUF_IG_ONE = ["Publishes through Buffer, automatically, on Instagram at 1080x1350 (no expand step).",
              "The image goes up with its alt text.",
              "No link in the caption; the bio link stays as it is."]
BUF_FB = ["Publishes through Buffer, automatically, as the Day60 Facebook Page.",
          "Images go up in the listed order, each with its alt text.",
          "The link stays in the text, as written."]
BUF_FB_ONE = ["Publishes through Buffer, automatically, as the Day60 Facebook Page.",
              "The image goes up with its alt text.",
              "The link stays in the text, as written."]
NOT_SCHED_BUF = "Not scheduled until the Product Hunt launch link exists; then it goes into Buffer for Jan 12."
NOTES["2026-w49-LI-email"] = BUF_LI + ["Text only, no image."]
NOTES["2026-w49-IG-email"] = BUF_IG + ["FB-email uses slides 1 to 5 on Tue Dec 1, with its own slide 6."]
NOTES["2026-w49-FB-email"] = BUF_FB + [
    "Slides 1 to 5 are IG-email's (Mon Nov 30). Slide 6 is p01_which_person_6_fb.png, with getday60.com in place of \"Link in bio\"."]
NOTES["2026-w49-LI-3touch"] = ["Copy not written yet (moved from week 47)."] + BUF_LI + [
    "The PDF goes up as a LinkedIn document with its title.",
    "The PDF is the v2 (HQ, Nov 14): slide 6 has cream keylines on Tick and the card. The old PDF stays in the repo."]
NOTES["2026-w48-LI-story"] = ["Reserved, not drafted: Social writes it after HQ forwards Phil's Nov 9 post.",
                              "Moved to Tue Dec 8: LI-email took Tue Dec 1 (HQ, Nov 18)."] + BUF_LI
NOTES["2026-w49-LI-PH"] = [NOT_SCHED_BUF, "The first comment is a placeholder until the Product Hunt launch link exists."] + BUF_LI + [
    "The image goes up with its alt text."]
NOTES["2026-w49-IG-PH"] = [NOT_SCHED_BUF] + BUF_IG_ONE
NOTES["2026-w49-FB-PH"] = [NOT_SCHED_BUF, "The text needs the Product Hunt launch link, a placeholder until it exists."] + BUF_FB_ONE

# HQ, Nov 19: Buffer's plan can't post a LinkedIn first comment. A LinkedIn post whose point is a link puts it in the
# body's last line; every other post has no link and ends on a next step that doesn't need one. LinkedIn is text only
# (no images or PDFs), and Facebook is quiet until after Dec 31.
BUF_LI2 = ["Publishes through Buffer, automatically, on Philip's LinkedIn profile, as a text post.",
           "No first comment: Buffer's plan doesn't allow one (HQ, Nov 19).",
           "Day60 stays untagged until Buffer has the Day60 page's LinkedIn details."]
NO_LINK = "No link: the post's point is the method, not a page (HQ, Nov 19)."
FB_CUT = "Cut Nov 19 (HQ): Facebook is quiet until after Dec 31."
NOTES["2026-w49-LI-email"] = BUF_LI2 + [NO_LINK,
    "Rewritten Nov 19: it ends on one next step for today, then a question. Waits for HQ's approval."]
NOTES["2026-w49-LI-3touch"] = ["Rewritten Nov 19 as a text post from the week 46 LI3 draft. Waits for HQ's approval."] + BUF_LI2 + [
    NO_LINK, "The v2 PDF is no longer posted (HQ, Nov 19: no LinkedIn PDFs); it stays in the repo."]
NOTES["2026-w48-LI-story"] = ["Reserved, not drafted: Social writes it after HQ forwards Phil's Nov 9 post.",
                              "Moved to Tue Dec 8: LI-email took Tue Dec 1 (HQ, Nov 18)."] + BUF_LI2 + [
    "No link: it ends on one next step a job seeker can take today, then a question (HQ, Nov 19)."]
NOTES["2026-w49-LI-PH"] = [NOT_SCHED_BUF,
                           "The last line's link is a placeholder until the Product Hunt launch link exists."] + BUF_LI2 + [
    "The launch link is the body's last line before the hashtags (HQ, Nov 19: the post's point is the launch page).",
    "Rewritten Nov 19 (text only, link in the last line), so it waits for HQ's approval again. The hero image stays in the repo."]
NOTES["2026-w49-IG-email"] = BUF_IG + ["Waits for HQ's approval."]
NOTES["2026-w49-FB-email"] = [FB_CUT + " Never posted. Its slide 6 file stays in the repo."]
NOTES["2026-w49-FB-PH"] = [FB_CUT + " Approved Nov 11, never posted."]

# Philip, Nov 19 (via HQ), overruling the Facebook pause: Facebook 3 a week, reusing the week's Instagram images.
NOTES["2026-w49-IG-email"] = BUF_IG + ["FB-email uses slides 1 to 5 on Tue Dec 1, with its own slide 6.", "Waits for HQ's approval."]
NOTES["2026-w49-FB-email"] = BUF_FB + [
    "Slides 1 to 5 are IG-email's (Mon Nov 30). Slide 6 is p01_which_person_6_fb.png, with getday60.com in place of \"Link in bio\".",
    "Cut Nov 19 and restored the same day (Philip: Facebook 3 a week). Waits for HQ's approval."]
NOTES["2026-w49-FB-PH"] = [NOT_SCHED_BUF, "The text needs the Product Hunt launch link, a placeholder until it exists."] + BUF_FB_ONE + [
    "Cut Nov 19 and restored the same day (Philip: Facebook 3 a week)."]

# HQ, Nov 19: approvals after the LinkedIn link-rule rewrite.
NOTES["2026-w49-LI-email"] = BUF_LI2 + [NO_LINK, "Approved by HQ on Nov 19, with the new ending (one next step for today, then a question)."]
NOTES["2026-w49-LI-3touch"] = ["Approved by HQ on Nov 19 as written (a text post rewritten from the week 46 LI3 draft)."] + BUF_LI2 + [
    NO_LINK, "The v2 PDF is no longer posted (HQ, Nov 19: no LinkedIn PDFs); it stays in the repo."]
NOTES["2026-w49-LI-PH"] = [NOT_SCHED_BUF,
                           "The last line's link is a placeholder until the Product Hunt launch link exists."] + BUF_LI2 + [
    "The launch link is the body's last line before the hashtags (HQ, Nov 19: the post's point is the launch page).",
    "HQ approved the structure on Nov 19. It stays a draft until the launch link exists; then Social sends HQ the final line. The hero image stays in the repo."]
NOTES["2026-w48-LI-story"] = ["Reserved, not drafted: Social writes it after HQ forwards Phil's Nov 9 post, then sends HQ the copy.",
                              "Moved to Tue Dec 8: LI-email took Tue Dec 1 (HQ, Nov 18)."] + BUF_LI2 + [
    "No link: it ends on one next step a job seeker can take today, then a question (HQ approved this brief change on Nov 19)."]

# HQ, Nov 19: Social writes all 5 LinkedIn posts (Mon, Wed, Fri: Phil's founder lane; Tue, Thu: method and product).
NOTES["2026-w48-LI-thanks"] = BUF_LI2 + [
    "No link: a light Thanksgiving post that doesn't sell (HQ, Nov 19). It ends on one next step for today, then a question.",
    "Waits for HQ's approval."]
NOTES["2026-w49-LI-hiringside"] = BUF_LI2 + [
    "No link: the post's point is the advice, not a page (HQ, Nov 19).",
    "Founder lane (Wed). One founder.ts fact (ClickUp's sales development team, 0 to 32 reps), nothing added.",
    "Waits for HQ's approval."]
NOTES["2026-w49-LI-target"] = BUF_LI2 + [
    NO_LINK,
    "Founder lane (Fri). One founder.ts fact (the Target Account Playbook at Deel) and the approved Huntr stat, word for word.",
    "Waits for HQ's approval."]

# HQ, Nov 19: new founder.ts lines; "land jobs at ClickUp, Deel and Google" is retired.
NOTES["2026-w49-LI-email"] = BUF_LI2 + [NO_LINK,
    "Approved by HQ on Nov 19; then one line changed the same day for HQ's new founder facts (Phil's own founder.ts line replaces \"land jobs at ClickUp, Deel and Google\"). Waits for HQ's approval again."]
NOTES["2026-w49-LI-PH"] = [NOT_SCHED_BUF,
                           "The last line's link is a placeholder until the Product Hunt launch link exists."] + BUF_LI2 + [
    "The launch link is the body's last line before the hashtags (HQ, Nov 19: the post's point is the launch page).",
    "HQ approved the structure on Nov 19. The hook and the Day60 line changed the same day for HQ's new founder facts. It stays a draft until the launch link exists; then Social sends HQ the final line. The hero image stays in the repo."]
NOTES["2026-w49-LI-hiringside"] = BUF_LI2 + [
    "No link: the post's point is the advice, not a page (HQ, Nov 19).",
    "Founder lane (Wed). founder.ts's ClickUp line only (0 to 32 reps), no ARR or other numbers.",
    "Waits for HQ's approval."]

# HQ, Nov 19 (later): founder.ts's proofBar, founderLine and FAQ answer back "land jobs at ClickUp, Deel and Google".
NOTES["2026-w49-LI-email"] = BUF_LI2 + [NO_LINK, "Approved by HQ on Nov 19, with the new ending (one next step for today, then a question)."]
NOTES["2026-w49-LI-PH"] = [NOT_SCHED_BUF,
                           "The last line's link is a placeholder until the Product Hunt launch link exists."] + BUF_LI2 + [
    "The launch link is the body's last line before the hashtags (HQ, Nov 19: the post's point is the launch page).",
    "HQ approved the structure on Nov 19, and the new opening from Phil's \"pile\" line the same day. It stays a draft until the launch link exists; then Social sends HQ the final line. The hero image stays in the repo."]

# Guide of the week 1 (HQ, Nov 19): Instagram and Facebook in week 49, open slots only
NOTES["2026-w49-IG-findhm"] = BUF_IG + [
    "Guide of the week 1 (HQ, Nov 19): how-to-find-the-hiring-manager. The caption says the full guide is at getday60.com/guides.",
    "FB-findhm uses slides 1 to 6 on Thu Dec 3, with its own slide 7.", "Approved by HQ (Nov 19). It goes into Buffer at the top-up that reaches it."]
NOTES["2026-w49-FB-findhm"] = BUF_FB + [
    "Guide of the week 1 (HQ, Nov 19): how-to-find-the-hiring-manager, linked with UTMs.",
    "Slides 1 to 6 are IG-findhm's (Wed Dec 2). Slide 7 is p02_find_hm_7_fb.png, with getday60.com in place of \"Link in bio\".",
    "Approved by HQ (Nov 19). It goes into Buffer at the top-up that reaches it."]

# HQ, Nov 22: Philip's own edit (his Nov 19 change request) applied and approved; notes as the Post Library has them.
NOTES["2026-w49-LI-hiringside"] = ["Publishes through Buffer, automatically, on Philip's LinkedIn profile, as a text post.", "No first comment: Buffer's plan doesn't allow one (HQ, Nov 19).", "Day60 stays untagged until Buffer has the Day60 page's LinkedIn details.", "No link: the post's point is the advice, not a page (HQ, Nov 19).", "Founder lane (Wed). The words are Philip's own edit (his change request, Nov 19), applied with two light tweaks on Nov 22; \"in 18 months\" is his.", "Approved by HQ on Nov 22, with Philip's edit."]

# HQ, Nov 22: the 14 Instagram posts Philip scheduled in the Instagram app were cropped to a square. Each is recycled as a new post (id + "-r2"),
# Buffer only; the originals keep HQ's note as history.
from recycle_def import R as _R, THIS_WEEK as _TW, MOVED as _MV  # noqa: E402
_AHEAD = {"2026-w48-IG-which", "2026-w48-IG-rb-reel", "2026-w48-IG-onelink", "2026-w48-IG-shortlist"}
for _r in _R:
    _o, _n = _r["orig"], _r["orig"] + "-r2"
    NOTES[_o] = [f"Cropped to a square when scheduled in the Instagram app; recycled as {_n}."] + (
        ["Still ahead in the Instagram app on Nov 22: HQ asked Philip to delete it there. Replaced: don't post it; the -r2 copy goes out this week through Buffer."] if _o in _AHEAD else [HIST])
    _rec = (f"Recycled from {_o} (HQ, Nov 22): the original was cropped to a square when it was scheduled in the Instagram app. "
            + ("Same files at Instagram's size, with the original caption word for word (HQ, Nov 22: it was approved and never went out)."
               if _o in _TW else "Same images at Instagram's size; the caption is lightly refreshed."))
    if _o in _TW and _r.get("reel"):
        NOTES[_n] = ["Publishes through Buffer, automatically, on Instagram as a Reel (1080x1920), shared to the feed.",
                     "The video's first second is the cover (cover-first video); Buffer's thumbnailOffset 500 picks it.",
                     "No link in the caption; the bio link stays as it is.", _rec,
                     f"Scheduled in Buffer on Nov 22 (Buffer post {_TW[_o]['buffer']}).",
                     "Approved: it keeps the original's approval (HQ, Nov 22)."]
    elif _r.get("reel"):
        NOTES[_n] = ["Publishes through Buffer, automatically, on Instagram as a Reel (1080x1920) with its cover.",
                     "No link in the caption; the bio link stays as it is.", _rec,
                     "Before Buffer: a Reel goes in only once HQ says yes to it, as a cover-first video (the cover held for the first second) with thumbnailOffset 500.",
                     "Approved: it keeps the original's approval (HQ, Nov 22)."]
    elif _r["status"] == "draft":
        NOTES[_n] = BUF_IG + [_rec, "Slides 1, 5 and 6 say \"holiday\" where the original said Thanksgiving. Waits for HQ's yes to those three slides."]
    else:
        NOTES[_n] = (BUF_IG_ONE if _o in ("2026-w48-IG-which", "2026-w48-IG-shortlist") else BUF_IG) + [_rec] + (
            ([f"Scheduled in Buffer on Nov 22 (Buffer post {_TW[_o]['buffer']})."] if _TW[_o]["buffer"] else
             ["HQ creates it in Buffer from Social's post details (Nov 22)."]) if _o in _TW else []) + (
            [f"Moved up from {_MV[_o]['was']} to {_MV[_o]['day']}, {_MV[_o]['t']} (approved, HQ Nov 22)." if _o != "2026-w46-IG6" else
             f"Moved up from {_MV[_o]['was']} to {_MV[_o]['day']}, {_MV[_o]['t']}, unless HQ approves the Thanksgiving humor card for that slot by Wed Nov 25's run; then it keeps a later date (HQ, Nov 22)."] if _o in _MV else []) + [
            "Approved: it keeps the original's approval (HQ, Nov 22)."]
NOTES["2026-w46-IG4-r2"].insert(-1, "Before it goes into Buffer, HQ confirms getday60.com/try still lets you try one job free with no account (slide 6 says so).")
NOTES["2026-w48-IG-which-r2"].insert(-1, "Reply to A-or-B comments.")

# HQ, Nov 22: IG-email moves up to Mon Nov 23, where this week's natively scheduled posts left gaps.
NOTES["2026-w49-IG-email"] = BUF_IG + [
    "Moved up from Mon Nov 30 to Mon Nov 23 (HQ, Nov 22): this week's Instagram slots lost their natively scheduled posts.",
    "FB-email uses slides 1 to 5 on Tue Dec 1, with its own slide 6.",
    "Approved in the Post Library on Nov 19; its words and slides haven't changed since."]
NOTES["2026-w49-FB-email"] = [x.replace("(Mon Nov 30)", "(Mon Nov 23)") for x in NOTES["2026-w49-FB-email"]]

# Nov 22, night: dates and link lines for the new cadence (Philip via HQ) and the try link rule (HQ)
NOTES["2026-w49-IG-email"] = BUF_IG + [
    "Moved up from Mon Nov 30 to Mon Nov 23 (HQ, Nov 22), then to Fri Nov 27, 9:43 PM (approved, HQ Nov 22): Instagram is one post a day, and Monday went to IG-which-r2.",
    "FB-email uses slides 1 to 5 on Mon Nov 23, with its own slide 6.",
    "Approved in the Post Library on Nov 19; its words and slides haven't changed since."]
NOTES["2026-w49-FB-email"] = BUF_FB + [
    "Slides 1 to 5 are IG-email's (Fri Nov 27). Slide 6 is p01_which_person_6_fb.png, with getday60.com in place of \"Link in bio\".",
    "Moved up from Tue Dec 1 to Mon Nov 23, 8:04 PM (Social, Nov 22), to start Facebook's daily posts.",
    "Ends with the try link (HQ, Nov 22: every Day60 post on Facebook ends with it); it keeps the guide link too.",
    "Approved by HQ (Nov 22) with both links; Philip approved it in the Post Library on Nov 19."]
NOTES["2026-w48-LI-thanks"] = BUF_LI2 + [
    "No link (HQ, Nov 22: a thank-you post shouldn't sell). It ends on one next step for today, then a question.",
    "Approved by HQ (Nov 22), link-free; Philip approved it in the Post Library on Nov 19."]
NOTES["2026-w48-FB-onelink"] = [
    "Publishes through Buffer, automatically, as the Day60 Facebook Page, as a Reel (1080x1920).",
    "The video's first second is the cover (cover-first video); Buffer's thumbnailOffset 500 picks it.",
    "Ends with the try link (HQ, Nov 22). Sat Nov 28, not the same day as IG-onelink-r2 (Wed).",
    "New Nov 22: IG-onelink's approved words and Reel, adapted for Facebook.",
    "Approved by HQ (Nov 22)."]
_NATIVE = "Scheduled natively on Nov 16 (Post Library log): it stays out of Buffer, at the time set then, so it doesn't go out twice."
for _k in ("2026-w48-LI-resume", "2026-w48-FB-which", "2026-w48-FB-thanks"):
    NOTES[_k] = [_NATIVE] + NOTES[_k]

# Nov 23: created in Buffer by Social (HQ, Nov 22, for Philip)
NOTES["2026-w49-FB-email"] = NOTES["2026-w49-FB-email"] + ["In Buffer: scheduled Nov 23 by Social (Buffer post 6b0430b40d00264c1a37d888), Mon Nov 23, 8:04 PM CT. Nothing for Philip to do."]
NOTES["2026-w48-LI-thanks"] = NOTES["2026-w48-LI-thanks"] + ["In Buffer: scheduled Nov 23 by Social (Buffer post 6b0430bb6b6de502825b7bee), Thu Nov 26, 2:39 PM CT. Nothing for Philip to do."]
NOTES["2026-w48-FB-onelink"] = NOTES["2026-w48-FB-onelink"] + ["In Buffer: scheduled Nov 23 by Social (Buffer post 6b0430c3433e6368c8a53c50), Sat Nov 28, 10:54 PM CT, thumbnailOffset 500. Nothing for Philip to do."]

# Nov 23: created or changed in Buffer by the new Social session (HQ brief, Nov 23)
NOTES["2026-w46-IG6-r2"] = NOTES["2026-w46-IG6-r2"] + ["In Buffer: scheduled Nov 23 by Social (Buffer post 6b04350b7e433fe9cacb0420), Thu Nov 26, 9:11 AM CT. If HQ approves the Thanksgiving card for Thursday, Social moves this post to the next open Instagram day. Nothing for Philip to do."]
NOTES["2026-w49-IG-email"] = NOTES["2026-w49-IG-email"] + ["In Buffer: scheduled Nov 23 by Social (Buffer post 6b043514433e6368c8a73713), Fri Nov 27, 9:43 PM CT. Nothing for Philip to do."]
NOTES["2026-w46-IG7-r2"] = NOTES["2026-w46-IG7-r2"] + ["In Buffer: scheduled Nov 23 by Social (Buffer post 6b04351c0d00264c1a39c154), Sun Nov 29, 8:17 PM CT. Nothing for Philip to do."]
NOTES["2026-w48-FB-onelink"] = NOTES["2026-w48-FB-onelink"] + ["Video swapped Nov 23 to the Facebook cut (end sticker getday60.com, HQ approved): p04_one_link_reel_fb_cover.mp4, thumbnailOffset 500."]
