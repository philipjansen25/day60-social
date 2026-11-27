"""Week 50 drafts, Mon Dec 7 to Sun Dec 13, 2026 (Social, Fri Nov 27, for HQ's one-pass approval).

HQ's brief (Nov 27): LinkedIn 6 (Sun to Fri, 8 AM to 12:59 PM CT), Instagram 7, Facebook 7 reusing that week's
Instagram art; Thursday's verdict (more Phil "I tried it" posts, message-craft lessons, Instagram resume-tool posts;
no A/B quiz). About 1 post in 4 is humor. Day60 tagged on LinkedIn. Every Day60 post on LinkedIn and Facebook ends
with the try link; Instagram says "Link in bio".

This module is the one source for these posts: `python3 scripts/library/batch_w50.py` writes their sections into
2026-12/wk50/posts.md (between the BATCH-W50 markers, plus LI-story's section), and gen.py builds their library
entries from those sections via specs(). Art: 2026-12/wk50/build_w50.py; FB-resume's slide 6 from
2026-11/wk47/build_resume.py (p02_resume_builder_6_fb_v3).
"""
import os, re, sys

WEEK = "2026-w50"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
POSTS_MD = os.path.join(ROOT, "2026-12", "wk50", "posts.md")
W = "2026-12/wk50"


def try_link(ch, pid):
    return f"https://getday60.com/try?utm_source={ch}&utm_medium=social&utm_campaign={pid}"


def utm(page, ch, content):
    return f"https://getday60.com/{page}?utm_source={ch}&utm_medium=social&utm_campaign=2026-w50&utm_content={content}"


TAG = ('Tag: Day60 (the first "Day60" in the text, page 144030699; the annotation is in linkedin-company-ids.md). '
       'Other company names stay plain text, with no "@".')

# alt texts (playbook §10c: what each image is for, 125 characters or less)
A_TAILOR = "Tailor it. Don't fake it. Skills the job wants that you can't claim yet stay off. Read every line, add only what's true."
A_ROUNDS = "Final round (round 7 of 9). Ask in the first call how many rounds there are and who makes the final call."
A_KEYWORDS = "Some keywords belong off your resume. The free resume builder lists the ones you can't claim yet. Learn it, then add it."
A_FIRSTLINE = "Your first line is about them: one thing their team is working on. An illustrative example of a first line."
A_STICKY = "Monday's whole plan on a sticky note: pick one job, find the hiring manager, send three lines."

RESUME_SLIDES = [
    ("2026-11/wk47/p02_resume_builder_1_lime_safe.png", "One resume, tailored to one job: how the free resume builder works."),
    ("2026-11/wk47/p02_resume_builder_2_safe.png", "Step 1: Add the job (a link to the posting, not LinkedIn, or the posting itself), then your resume."),
    ("2026-11/wk47/p02_resume_builder_3_safe.png", "Step 2: See what the job wants: its keywords and the 3 problems the role solves."),
    ("2026-11/wk47/p02_resume_builder_4_safe.png", "Step 3: Tailored, with only what's true. Your lines are reworded for the job, with no new skill, number or title."),
    ("2026-11/wk47/p02_resume_builder_5_safe.png", "Step 4: Know the gap before they do. Keywords you can't claim yet stay off your resume."),
    ("2026-11/wk47/p02_resume_builder_6_fb_v3.png", "Read every line, add your email, get a Word file. Free, no account, resume not stored: getday60.com/resume-builder"),
]
EXT_SLIDES = [
    ("2026-11/wk46/p14_ext_steps_1_mint_safe.png", "From a careers page to your sprint in one click: how the free Day60 Chrome extension works, in 3 steps."),
    ("2026-11/wk46/p14_ext_steps_2_safe.png", "Step 1: Open a job on the company's careers page."),
    ("2026-11/wk46/p14_ext_steps_3_safe.png", 'Step 2: Click the Day60 icon and press "Find the 4 people with Day60". It runs only when you click it.'),
    ("2026-11/wk46/p14_ext_steps_4_safe.png", "Step 3: The job opens in Day60 with its link filled in, ready to find the 4 people closest to the hire."),
    ("2026-11/wk46/p14_ext_steps_5_safe.png", "What it never does: read your LinkedIn pages, fill in forms, apply or send messages. It runs only when you click it."),
    ("2026-11/wk46/p14_ext_steps_6_v2_safe.png", "Free in the Chrome Web Store: getday60.com/chrome-extension"),
]

BUF_LI = ["Publishes through Buffer, automatically, on Philip's LinkedIn profile, as a text post.",
          "No first comment: Buffer's plan doesn't allow one (HQ, Nov 19).",
          "Tag Day60: annotation on the first \"Day60\" (page 144030699, linkedin-company-ids.md; Philip, Nov 26)."]
BUF_IG_ONE = ["Publishes through Buffer, automatically, on Instagram at 1080x1350 (no expand step).",
              "The image goes up with its alt text.",
              "No link in the caption; the bio link stays as it is."]
BUF_FB_ONE = ["Publishes through Buffer, automatically, as the Day60 Facebook Page.",
              "The image goes up with its alt text.",
              "The links stay in the text, as written."]
BUF_FB = ["Publishes through Buffer, automatically, as the Day60 Facebook Page.",
          "Images go up in the listed order, each with its alt text.",
          "The links stay in the text, as written."]
DRAFT = "Draft for HQ (Social, Nov 27): week 50 batch, HQ approves in one pass. Nothing in Buffer yet."


def P(pid, ch, date, day, time, title, fmt, text, bullets=(), files=(), notes=(), humor=False, guide=None, lid=None):
    return dict(pid=pid, ch=ch, date=date, day=day, time=time, title=title, fmt=fmt, text=text.strip("\n"),
                bullets=list(bullets), files=list(files), notes=list(notes), humor=humor, guide=guide,
                id=lid or f"{WEEK}-{pid}")


# ---------------------------------------------------------------- LinkedIn
LI = [
P("LI-story", "linkedin", "2026-12-08", "Tue Dec 8", "12:07", "Phil's own job search story", "text", lid="2026-w48-LI-story", text=f"""
ClickUp had an opening for a Sales Development Manager.

I sent them a 13-page plan for building their sales development team, with a 90-day action plan inside.

They hired me as employee #169 to build that team.

The plan wasn't magic. It did one thing an application can't: it showed the people who decide what my first 90 days would look like.

That's the idea I built Day60 around. Before you write, learn what the team is trying to do. Then write to the person who feels the empty seat, about their problem, not your history.

You don't need 13 pages. Three lines about their team will do.

Today, pick one job you want and write down one problem that team is probably trying to solve.

What's the most useful thing you've ever sent with an application?

{try_link("linkedin", "2026-w48-LI-story")}

#jobsearch #careeradvice #hiring
""", bullets=[
    "Drafted Nov 27 (Social, HQ's batch brief): Phil's own job search story, from the founder.ts lines only (playbook §1): the 13-page plan with a 90-day action plan he sent ClickUp for its Sales Development Manager opening, and being hired as employee #169 to build that team. No year, no job-search result numbers.",
    "Replaces the wait for HQ to forward Phil's Nov 9 post (Philip, Nov 8). If HQ has that post, HQ can swap this for a version built on it.",
    "Link: the try link, the body's last line (a founder-lane post about building Day60, playbook §4, HQ Nov 22). This replaces the Nov 19 \"no link\" brief.",
    TAG,
], notes=BUF_LI + ["Phil's founder story from founder.ts lines only; no year, no result numbers.",
                   "[VERIFY] Philip reads the story before approval: it's his own history.", DRAFT]),

P("LI-checker", "linkedin", "2026-12-09", "Wed Dec 9", "08:01", "I ran my email through Tick", "text", text=f"""
I ran a cold email through our own message checker.

Not a good one. An illustrative first draft, the kind most of us write: it opened with "I", ran long, and ended without a question.

Here's how it works. You pick what you're sending: a cold email, a LinkedIn connection note, or the message after they accept. You paste the draft. Tick checks it against 13 rules and tells you what to fix and why.

Two fixes came back first. Don't open with "I". End on one clear question.

One thing it doesn't do: check facts. That part stays with you.

I built Day60 so the message you send is short, true and yours.

Today, paste one message you're about to send into the checker and fix what Tick flags.

What's the line you always end up cutting?

{try_link("linkedin", "2026-w50-LI-checker")}

#jobsearch #networking #careeradvice
""", bullets=[
    "Lane: Phil's founder lane (Wed). A Phil \"I tried it\" post (HQ's verdict, Nov 26). The example email is illustrative; the checker's behavior is from the live page and IG6 (13 rules, three message types, it checks rules, not facts).",
    "[VERIFY] Phil confirms he ran a draft through the checker before approval. Nothing in the post claims a result beyond the checker's own rules.",
    TAG,
], notes=BUF_LI + ["\"I tried it\" post (HQ verdict, Nov 26).", "[VERIFY] Phil confirms he did this before approval.", DRAFT]),

P("LI-findhm", "linkedin", "2026-12-10", "Thu Dec 10", "09:44", "How to find the hiring manager", "text", guide="how-to-find-the-hiring-manager", text=f"""
Most people know they should write to the hiring manager.

The hard part is finding out who that is.

The posting holds more clues than people use. Read it twice: once for the job, once for the people. Look for the team name, a "reports to" line, any names, and the level of the role.

Then check the company's own pages: the team page, announcements, the blog. Search LinkedIn yourself with a short title keyword. Before you write, confirm the person still works there and that their title fits the team.

Not sure which of two people leads the team? Ask the recruiter or someone on the team first. A short question costs less than a message to the wrong person.

Rather skip the digging? Day60 finds the 4 people closest to the hire for you.

Today, pick one job and find its hiring manager's name.

Who's the hardest person to find for the roles you want?

The full guide, with an example start to finish:
{utm("guides/how-to-find-the-hiring-manager", "linkedin", "find-hiring-manager")}

#jobsearch #hiring #careeradvice
""", bullets=[
    "Lane: the Day60 method (Thu). LinkedIn's guide of the week 1, how-to-find-the-hiring-manager (HQ, Nov 19; playbook §5 and §7b): the guide's steps, as Instagram and Facebook ran them in week 49, the guide link as the body's last line (playbook §5: a LinkedIn guide post ends on the guide link; check-library.mjs allows one link line on LinkedIn, so this post has no try link).",
    TAG,
], notes=BUF_LI + ["Guide of the week (LinkedIn): how-to-find-the-hiring-manager.", DRAFT]),

P("LI-asks", "linkedin", "2026-12-11", "Fri Dec 11", "10:06", "Things that are not a question", "text", humor=True, text=f"""
Things that are not a question:

"Let me know your thoughts."
"Looking forward to hearing from you."
"Happy to chat whenever works."
"Just wanted to put this on your radar."

They read as polite. To a busy hiring manager they read as homework: work out what you want, then decide whether to give it.

I've spent my career building teams that reach the people who decide. The rule I'd give any of them: end on a question someone can answer in ten seconds, from their phone.

"Is the team still hiring for this role?"
"Are you the right person to ask about it?"

That's why every first note Day60 drafts ends on one easy question.

Today, open the last message you sent and rewrite its final line as a real question.

What's your favorite non-question?

{try_link("linkedin", "2026-w50-LI-asks")}

#jobsearch #networking #careeradvice
""", bullets=[
    "Lane: Phil's founder lane (Fri), as his view from his sales development work (founder.ts line: \"I've spent my career building teams that reach the people who decide.\"). A short message-craft lesson (HQ's verdict, Nov 26), deadpan.",
    "Humor: the joke is on the non-questions, never on the person writing them. The quoted lines are the \"bad message\" examples being torn down (playbook §11 allows them there).",
    TAG,
], notes=BUF_LI + ["humor (deadpan)", "Message-craft lesson (HQ verdict, Nov 26).", DRAFT]),

P("LI-week", "linkedin", "2026-12-13", "Sun Dec 13", "10:59", "Three jobs, not thirty", "text", text=f"""
This week: three jobs. Not thirty.

Monday: pick three jobs you'd say yes to.
Tuesday: find the hiring manager for the first one.
Wednesday: write them three lines. One problem their team has, one line of proof, one easy question.
Thursday and Friday: do the same for the other two.

That's the week. Every message goes to a person who can say yes.

It's how a Day60 sprint starts: three target jobs a week.

Tonight, write down your three jobs.

Which one is first on your list?

{try_link("linkedin", "2026-w50-LI-week")}

#jobsearch #careeradvice #networking
""", bullets=[
    "Lane: the Sunday plan-your-week lane (playbook §4). One method step per day; \"Start with three target jobs a week\" is the homepage's own line.",
    TAG,
], notes=BUF_LI + ["Sunday plan-your-week lane.", DRAFT]),
]

# ---------------------------------------------------------------- Instagram
IG_TAGS = "#day60 #jobsearch #jobsearchtips #careertips #networking"
IG = [
P("IG-tailor", "instagram", "2026-12-08", "Tue Dec 8", "16:09", "Tailor it, don't fake it", "image",
  files=[(f"{W}/p01_tailor_pink.png", A_TAILOR)], text=f"""
Tailor it. Don't fake it.

The free resume builder tailors your resume to one job, using only what's true. Skills the job wants that you can't claim yet stay off the page, and it tells you which ones they are.

Read every line, add your email, and you get a Word file. Free, no account, and your resume isn't stored: getday60.com/resume-builder

Today: pick one job you want and tailor your resume to it.

Then find the 4 people closest to the hire. Link in bio.

#day60 #jobsearch #resumetips #careertips #jobsearchtips
""", bullets=["Resume-tool post (HQ's verdict, Nov 26). Facts only from the resume builder posts (wk47, wk48) and its #967 email step.",
              "Ground: pink. Week 50's Instagram grounds in order: ink, pink, cobalt, mint, coral, lime, pink (any 4 in a row differ). The lime element: the highlight."],
  notes=BUF_IG_ONE + ["Resume-tool post (HQ verdict, Nov 26).", DRAFT]),

P("IG-rounds", "instagram", "2026-12-09", "Wed Dec 9", "13:03", "Final round, round 7 of 9", "image", humor=True,
  files=[(f"{W}/p02_rounds_cobalt.png", A_ROUNDS)], text=f"""
Final round. (Round 7 of 9.)

Long interview loops happen. You can still plan around them.

In the first call, ask two things: how many rounds there are, and who makes the final call. Then make sure that person knows who you are, instead of meeting you for the first time in round 7.

Today: for one job you're interviewing for, ask the recruiter what the rounds look like.

Day60 finds the 4 people closest to the hire, so you know who decides from day one. Link in bio.

#day60 #jobsearch #interviewtips #careertips #jobsearchtips
""", bullets=["Humor: the joke is on long interview loops (a fair target, playbook §4), and the card ends on a real tip.",
              "Ground: cobalt; the lime element is the sticker."],
  notes=BUF_IG_ONE + ["humor", DRAFT]),

P("IG-keywords", "instagram", "2026-12-11", "Fri Dec 11", "21:07", "Keywords you can't claim yet", "image",
  files=[(f"{W}/p03_keywords_coral.png", A_KEYWORDS)], text=f"""
Some keywords belong off your resume.

If a posting asks for a skill you don't have yet, adding it anyway can lead straight to a hard interview question.

The free resume builder lists those as keywords you can't claim yet, and keeps them off. Learn the skill first, then add it.

Today: find one skill a job you want asks for, and write down how you'll show it, or how you'll learn it.

Free, no account: getday60.com/resume-builder

Day60 finds the 4 people closest to the hire for one job. Link in bio.

#day60 #jobsearch #resumetips #careertips #jobsearchtips
""", bullets=["Resume-tool post (HQ's verdict, Nov 26). \"Keywords you can't claim yet\" is the builder's own label.",
              "Ground: coral, ink text only; the lime element is the highlight."],
  notes=BUF_IG_ONE + ["Resume-tool post (HQ verdict, Nov 26).", DRAFT]),

P("IG-firstline", "instagram", "2026-12-12", "Sat Dec 12", "20:28", "Your first line is about them", "image",
  files=[(f"{W}/p04_first_line_lime.png", A_FIRSTLINE)], text=f"""
Your first line is about them.

Not your degree, not your life story. One thing their team is working on, that you noticed.

Illustrative: "Saw your team is opening a second support office this spring."

Then one line of proof you can help, and one easy question.

Today: rewrite the first line of the next message you send so it's about their team.

Day60 drafts a first note to each of the 4 people closest to the hire. You make it yours and send it. Link in bio.

#day60 #jobsearch #networkingtips #careertips #coverletter
""", bullets=["Message-craft lesson (HQ's verdict, Nov 26). The example first line is illustrative and labeled on the card.",
              "Ground: lime (the whole ground is the lime element; the card is white)."],
  notes=BUF_IG_ONE + ["Message-craft lesson (HQ verdict, Nov 26).", DRAFT]),

P("IG-sticky", "instagram", "2026-12-13", "Sun Dec 13", "21:16", "Plan fits on a sticky note", "image", humor=True,
  files=[(f"{W}/p05_sticky_pink.png", A_STICKY)], text=f"""
Monday's whole plan fits on a sticky note.

1. Pick one job.
2. Find the hiring manager.
3. Send three lines.

Bad handwriting still counts.

Today: write the note tonight and stick it where you'll see it at 9 AM.

Day60 finds the 4 people for one job and drafts a short note to each. Link in bio.

{IG_TAGS}
""", bullets=["Light humor (a one-line card). Sunday evening, for Monday morning.",
              "Ground: pink. No lime on this card."],
  notes=BUF_IG_ONE + ["humor (light)", DRAFT]),
]

# ---------------------------------------------------------------- Facebook (reuses Instagram art only)
SHARE = "Share this with someone who's looking."
FB = [
P("FB-resume", "facebook", "2026-12-07", "Mon Dec 7", "19:46", "Free resume builder for one job", "carousel",
  files=RESUME_SLIDES, text=f"""
If someone you know is tailoring their resume for one job, here's a free tool that helps.

Add the job and the resume. The free resume builder shows what the job wants, tailors the resume using only what's true, and lists the keywords they can't claim yet, so those stay off.

Read every line, add an email, and get a Word file. Free, no account, and the resume isn't stored.

{SHARE}

The resume builder: {utm("resume-builder", "facebook", "resume-builder")}

Today: pick one job and tailor your resume to it.
{try_link("facebook", "2026-w50-FB-resume")}

#jobsearch #day60 #resumetips
""", bullets=["Reuses Instagram's resume builder carousel (IG-resume-r2, Thu Jan 7): wk47 slides 1 to 5 (_safe) and a new slide 6 without \"Link in bio\" (p02_resume_builder_6_fb_v3, the #967 email step). No slide says \"Nothing you add is kept\".",
              "Supersedes the old week 47 FB-resume draft, which never went out.",
              "Alt text (per slide): " + " · ".join(f'{i} "{a}"' for i, (_, a) in enumerate(RESUME_SLIDES, 1))],
  notes=BUF_FB + ["Facebook reuses Instagram art (HQ, Nov 26).", DRAFT]),

P("FB-extsteps", "facebook", "2026-12-08", "Tue Dec 8", "07:26", "The extension in three steps", "carousel",
  files=EXT_SLIDES, text=f"""
If you or someone you know finds jobs on company careers pages, this saves a step.

Open a job on the company's own careers page, click the Day60 icon, and press "Find the 4 people with Day60". The job opens in Day60 with its link filled in, ready to find the 4 people closest to the hire.

It runs only when you click it. It never reads LinkedIn pages, fills in forms, applies or sends messages.

{SHARE}

Free in the Chrome Web Store: {utm("chrome-extension", "facebook", "extension-steps")}

Today: open one job on a company's careers page and give it one click.
{try_link("facebook", "2026-w50-FB-extsteps")}

#jobsearch #day60 #jobsearchtips
""", bullets=["Reuses Instagram's extension carousel (IG5-r2, Thu Dec 10), 6 slides; Facebook hasn't run these slides (FB3 was the extension FAQ). Slide 6 has no \"Link in bio\".",
              "Alt text (per slide): " + " · ".join(f'{i} "{a}"' for i, (_, a) in enumerate(EXT_SLIDES, 1))],
  notes=BUF_FB + ["Facebook reuses Instagram art (HQ, Nov 26).", DRAFT]),

P("FB-tailor", "facebook", "2026-12-09", "Wed Dec 9", "08:23", "Tailor it, don't fake it", "image",
  files=[(f"{W}/p01_tailor_pink.png", A_TAILOR)], text=f"""
Tailor it. Don't fake it.

If you're helping someone with their resume this month, here's the rule worth passing on: tailor it to one job, using only what's true.

The free resume builder works that way. Skills the job wants that they can't claim yet stay off the page, and it says which ones they are. Read every line, add an email, get a Word file. Free, no account, and the resume isn't stored.

{SHARE}

The resume builder: {utm("resume-builder", "facebook", "tailor-it")}

Today: pick one job and tailor the resume to it.
{try_link("facebook", "2026-w50-FB-tailor")}

#jobsearch #day60 #resumetips
""", bullets=["Same card as IG-tailor (Instagram Tue Dec 8)."], notes=BUF_FB_ONE + [DRAFT]),

P("FB-rounds", "facebook", "2026-12-10", "Thu Dec 10", "10:31", "Final round, round 7 of 9", "image", humor=True,
  files=[(f"{W}/p02_rounds_cobalt.png", A_ROUNDS)], text=f"""
Final round. (Round 7 of 9.)

Long interview loops are real, and they're tiring. If you or someone you know is in one, two questions help in the very first call: how many rounds are there, and who makes the final call?

Then make sure that person knows who you are before round 7.

{SHARE}

Today: ask the recruiter what the rounds look like for one job.
{try_link("facebook", "2026-w50-FB-rounds")}

#jobsearch #day60 #interviewtips
""", bullets=["Same card as IG-rounds (Instagram Wed Dec 9)."], notes=BUF_FB_ONE + ["humor", DRAFT]),

P("FB-firstline", "facebook", "2026-12-11", "Fri Dec 11", "08:08", "Your first line is about them", "image",
  files=[(f"{W}/p04_first_line_lime.png", A_FIRSTLINE)], text=f"""
Your first line is about them.

When you write to a hiring manager, skip the life story. Start with one thing their team is working on that you noticed.

Illustrative: "Saw your team is opening a second support office this spring."

Then one line of proof you can help, and one easy question. Short enough to read on a phone.

{SHARE}

Today: rewrite the first line of your next message so it's about their team.
{try_link("facebook", "2026-w50-FB-firstline")}

#jobsearch #day60 #networking
""", bullets=["Same card as IG-firstline (Instagram Sat Dec 12)."], notes=BUF_FB_ONE + [DRAFT]),

P("FB-sticky", "facebook", "2026-12-12", "Sat Dec 12", "22:58", "Plan fits on a sticky note", "image", humor=True,
  files=[(f"{W}/p05_sticky_pink.png", A_STICKY)], text=f"""
Next week's whole plan fits on a sticky note.

1. Pick one job.
2. Find the hiring manager.
3. Send three lines.

Bad handwriting still counts.

If someone you love is looking for work, this is a kind thing to send them this weekend.

{SHARE}

Today: write the note and stick it somewhere you'll see Monday morning.
{try_link("facebook", "2026-w50-FB-sticky")}

#jobsearch #day60 #jobhunting
""", bullets=["Same card as IG-sticky (Instagram Sun Dec 13)."], notes=BUF_FB_ONE + ["humor (light)", DRAFT]),

P("FB-keywords", "facebook", "2026-12-13", "Sun Dec 13", "08:47", "Keywords you can't claim yet", "image",
  files=[(f"{W}/p03_keywords_coral.png", A_KEYWORDS)], text=f"""
Some keywords belong off a resume.

If a posting asks for a skill someone doesn't have yet, adding it anyway can lead straight to a hard interview question.

The free resume builder lists those as keywords you can't claim yet, and keeps them off. Learn the skill first, then add it.

{SHARE}

The resume builder: {utm("resume-builder", "facebook", "keywords")}

Today: find one skill a job you want asks for, and plan how to show it or learn it.
{try_link("facebook", "2026-w50-FB-keywords")}

#jobsearch #day60 #resumetips
""", bullets=["Same card as IG-keywords (Instagram Fri Dec 11)."], notes=BUF_FB_ONE + [DRAFT]),
]

POSTS = LI + IG + FB
NOTES_W50 = {p["id"]: p["notes"] + (["Approved by HQ."] if False else []) for p in POSTS}


def _clock(t):
    h, m = map(int, t.split(":"))
    return f"{(h - 1) % 12 + 1}:{m:02d} {'AM' if h < 12 else 'PM'}"


def section_md(p):
    head = f"### {p['pid']} · {p['day']} · {_clock(p['time'])} · DRAFT (Social, Nov 27) · {p['title'].upper()}"
    lines = [head, "- Status: draft for HQ's one-pass approval (HQ brief, Nov 27). Nothing in Buffer yet."]
    if p["humor"]:
        lines.append("- Humor: yes (about 1 post in 4, playbook §4).")
    lines += [f"- {b}" for b in p["bullets"]]
    if len(p["files"]) == 1:
        lines.append(f"- Image: `{p['files'][0][0]}`")
        lines.append(f"- Alt text: {p['files'][0][1]}")
    elif p["files"]:
        lines.append(f"- Carousel ({len(p['files'])}): " + ", ".join(f"`{f}`" for f, _ in p["files"]) + ". Each 1080x1350.")
    if p["ch"] == "instagram":
        lines.append("- Link: the bio link stays /try. No link in the caption.")
    elif p["guide"]:
        lines.append("- Link: the guide link, the body's last line before the hashtags.")
    else:
        lines.append(f"- Link: `{try_link(p['ch'], p['id'])}`, the body's last line before the hashtags.")
    lines += ["", "```", p["text"], "```", ""]
    return "\n".join(lines)


def specs(entry, one=None):
    import notes as _n
    _n.NOTES.update(NOTES_W50)
    out = []
    for p in POSTS:
        kw = dict(channel=p["ch"], date=p["date"], time=p["time"], status="draft", title=p["title"], format=p["fmt"],
                  files=[{"path": f, "alt": a} for f, a in p["files"]])
        if p["id"] != f"{WEEK}-{p['pid']}":
            kw["id"] = p["id"]
        if p["guide"]:
            kw["guide"] = p["guide"]
        if p["ch"] == "facebook":
            kw["link"] = try_link("facebook", p["id"])
        if p["ch"] == "linkedin":
            kw["link"] = utm("guides/" + p["guide"], "linkedin", "find-hiring-manager") if p["guide"] else try_link("linkedin", p["id"])
        out.append(entry(WEEK, p["pid"], **kw))
    return out


def write_md():
    s = open(POSTS_MD).read()
    # LI-story: replace its old reserved section in place
    story = next(p for p in LI if p["pid"] == "LI-story")
    a = s.index("### LI-story · ")
    b = s.index("\n## ", a)
    s = s[:a] + section_md(story).rstrip("\n") + "\n" + s[b:]
    # the rest: one block between markers at the end
    block = ["<!-- BATCH-W50 START (generated by scripts/library/batch_w50.py; edit there) -->",
             "## Week 50 batch: drafts for HQ (Social, Fri Nov 27)", "",
             "HQ's brief (Nov 27): drafts for Mon Dec 7 to Sun Dec 13, approved in one pass. LinkedIn 6 (Sun to Fri, 8 AM to 12:59 PM CT), "
             "Instagram 7, Facebook 7 reusing the week's Instagram art. Humor: LI-asks; IG-rounds, IG-sticky; FB-rounds, FB-sticky.", ""]
    for p in POSTS:
        if p["pid"] != "LI-story":
            block.append(section_md(p))
    block.append("<!-- BATCH-W50 END -->")
    blk = "\n".join(block) + "\n"
    if "<!-- BATCH-W50 START" in s:
        a = s.index("<!-- BATCH-W50 START"); b = s.index("<!-- BATCH-W50 END -->") + len("<!-- BATCH-W50 END -->\n")
        s = s[:a] + blk + s[b:]
    else:
        s = s.rstrip("\n") + "\n\n" + blk
    open(POSTS_MD, "w").write(s)


def lint():
    bad = []
    for p in POSTS:
        t = p["text"]
        for w in ("—", "résumé", "Résumé", "Philip", "passionate", "leverage", "I hope this finds you well"):
            if w in t:
                bad.append((p["id"], w))
        if p["ch"] == "linkedin":
            if t.count("Day60") != 1:
                bad.append((p["id"], f"Day60 x{t.count('Day60')}"))
            if len(t.split("\n")[0]) >= 60:
                bad.append((p["id"], "hook >= 60"))
            if not p["guide"] and t.split("\n\n")[-2].strip() != try_link("linkedin", p["id"]):
                bad.append((p["id"], "LI try link not last"))
        if p["ch"] == "facebook" and try_link("facebook", p["id"]) not in t.split("\n\n")[-2]:
            bad.append((p["id"], "FB try link not last"))
        if p["ch"] == "instagram" and "Link in bio" not in t:
            bad.append((p["id"], "no Link in bio"))
        if not re.search(r"^#\w+", t.split("\n")[-1]):
            bad.append((p["id"], "no hashtags"))
        for f, a in p["files"]:
            if len(a) > 125:
                bad.append((p["id"], f"alt {len(a)} chars"))
            if not os.path.exists(os.path.join(ROOT, f)):
                bad.append((p["id"], f"missing {f}"))
    return bad


if __name__ == "__main__":
    b = lint()
    print("lint:", b or "ok")
    if not b:
        write_md()
        print("wrote", POSTS_MD)
