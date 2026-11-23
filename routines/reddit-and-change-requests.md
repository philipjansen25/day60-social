# Day60 Social: Reddit replies and Philip's change requests (daily 6:15 AM and 1:15 PM CT)

Cron: `CRON_TZ=America/Chicago 15 6,13 * * *` (every day at 6:15 AM and 1:15 PM CT)

Saved Nov 23, 2026 from the old Day60 Social session's routine (prompt last updated 2026-11-22), word for word, for the session that replaces it. One note for the new session: "scratchpad gen.py" in the prompt now means `scripts/library/gen.py` in this repo (see HANDOFF.md).

## Prompt

Start with change requests, every run, alerts or not (Philip, Nov 22, on the Post Library: "I asked for this edit but it hasn't been made. These should be automatic when I need an edit"; HQ's rules, Nov 22). Follow playbook.md §5, "Philip's change requests are automatic". List the Post Library's `log` collection (https://claude.ai/artifact/N91e3iMns547GJyGKAJrfp) with ArtifactData, read only. A request is open when a record has a `changeNote` with no `changeDoneAt`, or a `changeAt` later than its `changeDoneAt`, and that post's section in posts.md has no line "Change request <changeAt> applied". For each open one, get `posts/<id>`.
- If HQ already put the edit there (the record's text differs from library.json and the record changed after `changeAt`): make posts.md and library.json match the record (scratchpad gen.py, then node scripts/check-library.mjs), add the "applied" line and push. If the post is already in Buffer, update the Buffer post to that text the same run.
- Otherwise, if the post isn't posted: write the edit in posts.md. Use Philip's words as he wrote them, with only light fixes, inventing nothing. Rule checks stay on: no link in a LinkedIn body, no career numbers beyond what he writes himself, "Phil" on product surfaces. A founder fact he adds himself counts as confirmed by him. Regenerate library.json, add the "applied" line and push.
- If an edit would break a rule, don't write it. Send it to HQ to decide.
- Send HQ (session_014zSVjD5hU4eupNEkmMPqQ6) one message for the run: one line per edit, the new text, and any edit left for HQ. HQ writes the text, `changeDoneAt` and `changeDone` to the Post Library, and approves a draft. Social never writes `log` or a post's `text` or `status`; it writes only a post's `notes`.
- No open requests: say nothing and go on.

Then the Reddit replies, every day at 6:15 AM and 1:15 PM CT. Philip asked for this on Nov 19: "the reddit process is too much manual work. I need you to highlight the threads that I should post in and then generate the copy for me to post". On Nov 20 he widened it, verbatim: "I want to comment on all alerts going forward." and "Automation allows me to do more, not less". So from Nov 20 every post in an F5Bot alert gets a ready reply. The old limit of 2 posts a day is gone.

git pull day60-social main, then follow reddit/README.md's "Daily run" section.

Read: in Gmail run exactly one search, `from:alerts@f5bot.com newer_than:1d`, and read only those alert emails (the HTML body holds each post's excerpt). Never open a link in an alert, never fetch reddit.com, old.reddit.com, oauth.reddit.com or any Reddit mirror, and never web-search for Reddit posts. You work from the alert's title, subreddit and excerpt only. Turn each F5Bot redirect link into the plain reddit.com thread link by decoding its `u=` value; do not request it.

Write: one reply for every post in those alerts, made for that post. No Day60, no product, no links, no "DM me". 40 to 120 words, plain text, short paragraphs. Open differently each time and vary the shape, so 20 replies posted by one person in one day never read as a template. Answer what the person asked, with one concrete next step they can take today. Where the excerpt is too thin to answer a specific question, write a reply that fits the title and say so in the item's why line ("excerpt thin"). Never invent facts about the poster.

The only posts that get no reply, each listed under `skipped` with a short reason so Philip sees nothing was dropped silently: (a) a company's or a seller's ad or AMA; (b) a post that is not about looking for work or working life at all (a keyword false match); (c) a second copy of a post already on the card; (d) a post a day or more old.

Card: write to the Post Library's meta/reddit (https://claude.ai/artifact/N91e3iMns547GJyGKAJrfp) with ArtifactData: get, then set with if_version, or create it if missing. The card always holds the posts from the last 24 hours of alerts. Keep the reply already written for a post that is still on the card (Philip may have copied it), add the new ones, drop posts whose alert is more than 24 hours old. Order: people asking for help first, freshest first within that; venting and screenshot posts after. Keep the fields the page reads today (date, how, items with id, link, sub, title, why, reply) and add `skipped` (title, sub, reason) and `count`. If the page's Reddit card needs a change to show 20 or more replies well (a count line, a copy button on each, a way to mark one done that stays on his device, the skipped list), make that change and tell HQ what changed. Never write to the log collection. No alerts in the last 24 hours: leave the card as it is and stop.

`how` line on the card: "Newest and most useful first. Open the thread, read it once, copy the reply, paste it as a comment. Leave a few minutes between comments. If Reddit says you're doing that too much, stop for an hour. No Day60, no links."

Commit reddit/days/<date>.md to day60-social main with links, titles, why lines and replies only; keep usernames, email addresses and personal data out of this public repo. Read files in parts (grep -n, then sed -n ranges). About Reddit, message HQ only if the Post Library write fails, or when a run's text from HQ asks for a report.
