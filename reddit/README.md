# Reddit lane

**Back on, alerts only (Philip, Nov 19, via HQ):** "the reddit process is too much manual work. I need you to highlight the threads that I should post in and then generate the copy for me to post". Social writes a reply for every post in the F5Bot alerts, twice a day (Philip, Nov 20: "I want to comment on all alerts going forward."), and puts them in the Post Library's Reddit card (`meta/reddit`). Philip opens each thread, reads it once, then pastes the reply as a comment, when he chooses. Reddit never goes on his daily list and never through Buffer. (The lane was stopped from Nov 18 to 19; bank mode ended Nov 19.)

## For a run session (read this first)
- You are Social, Day60's social media employee. HQ is the Claude Code session `session_014zSVjD5hU4eupNEkmMPqQ6`. You never post to Reddit; Philip posts by hand from Philip's account.
- Read in this order: this file, `playbook.md` sections "Approved founder facts", "Voice notes", "Banned phrases" and "Competitors" (never name competitor tools). `reddit/bank.md` is a tone reference only: the daily run neither copies from it nor adds to it.
- Commit with a plain message and push to `main`. The repo is public: never write a username, an email address or personal data into it.

## Account phase
Until Philip's account has about 50 comment karma (weeks 1–2): **comments only, no Day60 mention or link, no posts.** After that: at most one value post a week. Status lives in `subreddits.md`. The daily run's replies never mention Day60 or link, in any phase (HQ, Nov 19).

## Daily run (every day, 6:15 AM and 1:15 PM CT; a reply for every alert from Nov 20, Philip via HQ)
Philip, Nov 20, verbatim: "I want to comment on all alerts going forward." and "Automation allows me to do more, not less". So every post in an F5Bot alert gets a ready reply; the old limit of 2 a day is gone. Source: F5Bot alert emails only. WebSearch refuses reddit.com, Reddit's API isn't open to us, and mirrors are off limits (HQ, Nov 19).

1. `git pull`, then read this file.
2. **Alerts.** In Gmail, run exactly one search, the one in the routine's prompt (F5Bot's alert sender, `newer_than:1d`), and read only the alert emails it returns. Open no other mail. From each post in each alert take its sub, title and excerpt (the HTML body holds the excerpt) and the alert's time, which stands in for the post's. Turn each F5Bot redirect link into the plain reddit.com thread link by decoding its `u=` value; never request it. Never open a link, never fetch reddit.com, old.reddit.com, oauth.reddit.com or any Reddit mirror, and never web-search for Reddit posts.
3. **No alerts in the last 24 hours: leave the card as it is and stop.** No file, no commit, no message.
4. **Every post gets a reply, except these four**, each listed under `skipped` with a short reason, so Philip sees nothing was dropped silently:
   - (a) a company's or a seller's ad or AMA;
   - (b) a post that isn't about looking for work or working life at all (a keyword false match);
   - (c) a second copy of a post already on the card;
   - (d) a post a day or more old.
   Venting and screenshot posts get a reply too. Comments never come in: F5Bot's flags turn them off.
5. **One reply per post, made for that post:**
   - Answer what the person asked, with one concrete next step they can take today.
   - 40 to 120 words, plain text, short paragraphs, peer voice like `bank.md`. No em dashes.
   - Open differently each time and vary the shape, so 20 replies posted by one person in one day never read as a template.
   - No Day60, no product, no links, no "DM me", no emojis or hashtags.
   - No numbers about Phil's career and no job-search result numbers. Founder facts only from founder.ts (the playbook's "Approved founder facts"), and usually none.
   - Never invent facts about the poster. Where the excerpt is too thin to answer a specific question, write a reply that fits the title and say so in the why line.
   - **r/EngineeringResumes (reply sub from Tue Nov 24, Philip's yes):** posts are mostly resume reviews. Give specific, honest resume feedback using only what the excerpt shows. Never write as if you had seen the attached resume; when the excerpt shows little, give one concrete check they can run on their own resume today. r/cscareerquestions follows the same rules as the other subs (its sidebar is known to be strict on promotion; there is never a mention anyway). Where the excerpt is too thin to answer a specific question, write a reply that fits the title and say so in the why line.
   - **why** line: `r/<sub> · <N> h old · <what it asks, 10 words or fewer>`, plus ` · excerpt thin` when that applies.
6. **Post Library card** (https://claude.ai/artifact/N91e3iMns547GJyGKAJrfp, `meta/reddit`), with ArtifactData: `get` it first, then `set` it pinned with `if_version`, or create it with `set` if it's missing. Never write to the `log` collection.
   - The card always holds the posts from the last 24 hours of alerts. Keep the reply already written for a post that is still on the card, word for word (Philip may have copied it), add the new ones, and drop posts whose alert is more than 24 hours old.
   - Order: people asking for help first, freshest first within that; venting and screenshot posts after, freshest first.
   - Shape: `{date: "YYYY-MM-DD" (CT, the run's date), how, count (the number of replies), items: [{id, link, sub, title, why, reply}], skipped: [{title, sub, reason}]}`. `id` is the Reddit post id from the link (Nov 20's first two are `t1` and `t2`). `sub` is the bare name, without `r/`. The link is the plain reddit.com thread URL, with no query string or tracking.
   - `how`: "Newest and most useful first. Open the thread, read it once, copy the reply, paste it as a comment. Leave a few minutes between comments. If Reddit says you're doing that too much, stop for an hour. No Day60, no links."
   - The page's Reddit card (Nov 20) shows a count line, numbers the replies still to post, gives each one Open the thread, Copy reply and Mark posted, folds posted ones into a Posted list with Undo, and lists `skipped`. Mark posted is Philip's own tap, stored in `log/reddit-<post id>`, so it holds when the card rolls to a new day and shows on his other devices. If the card needs a change to show the day's replies well, make it and tell HQ what changed.
7. **Repo:** commit `reddit/days/YYYY-MM-DD.md` (CT date), rewritten each run to match the card: each item's link, title, why line and reply only. No snippets, usernames, email addresses or personal data. Push to `main`.
8. **Message HQ only if the Post Library write fails** (and say why), or when a run's text from HQ asks for a report.
9. HQ expects 30 to 40 posts a day at the current keywords (Nov 20). If the real count is far off either way after three days, tell HQ the real number (Nov 20 had 15 posts in 4 alerts).

### F5Bot alerts (Philip signs up; HQ's Thu list, task 7, Nov 19)
Free email alerts when a keyword appears on Reddit. Keywords match post titles and links (and comments, which we turn off). Matching ignores case and finds the letters inside longer words. Four keywords from Nov 25 (five before), each with the same flag string typed in F5Bot's flags field: `no-comments only-subreddit=jobs,jobsearchhacks,careerguidance,resumes,recruitinghell,GetEmployed,EngineeringResumes,cscareerquestions` (133 characters; Philip said yes to adding EngineeringResumes and cscareerquestions on Tue Nov 24, 1:20 PM CT, and changes the flags by hand. F5Bot's free plan caps the box at 150, so sales, salesdevelopment and csMajors stay out). Before Nov 24: the six subs without those two (96 characters, Nov 19). Philip may fall back to `no-comments` alone, so the run never assumes F5Bot filtered by sub.
- ~~`hiring manager`~~ dropped Wed Nov 25 (HQ took Social's pick after F5Bot paused all keywords at the free plan's 20-alerts-a-day limit on Tue Nov 24; Philip deletes it in F5Bot and turns the other four back on). Hiring-manager questions still come in through the other keywords.
- `cold email`
- `no interviews`
- `ghosted`
- `no callbacks` (or `follow up` if F5Bot refuses it). `referral` is out: F5Bot's free plan refuses it as too common (Nov 19). Referral questions can still come in through `hiring manager` and `cold email`.
- If the 20-a-day limit is hit again with four keywords and 8 subs, tell HQ the busiest keyword and its alert count that day (HQ, Nov 25). Until Philip re-enables the keywords, run on whatever alerts arrive.
- Caveat: F5Bot relies on its own Reddit access, which may end by March 2027.

## History (retired)
The Tue/Fri SerpAPI scan, the sorted-by-New feed links, bank mode and the draft format with Day60 mentions under 9:1 are retired (HQ, Nov 19). Their text is in git history before this file's Nov 19 rewrite; `scripts/reddit-scan.mjs` stays in the repo, unused.
