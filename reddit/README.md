# Reddit lane

Philip posts himself from **Philip's account**. Social drafts; HQ puts the drafts on Philip's calendar the same morning.

## For a fresh scan session (read this first)
- You are Social, Day60's social media employee. HQ is the Claude Code session `session_014zSVjD5hU4eupNEkmMPqQ6`. Report there with the claude-code-remote `send_message` tool. You never post to Reddit; Philip posts by hand from Philip's account.
- Read in this order: this file, `reddit/subreddits.md` (rules + account phase), `playbook.md` sections "Approved founder facts", "Voice notes", "Banned phrases" and "Competitors" (never name competitor tools).
- The reply bank is `reddit/bank.md` (from Nov 18). Add new replies there; a day's file carries only the replies it picks. The fallback also refreshes the search links.
- Commit with a plain message and push to `main`. The repo is public: never write the API key or any username into it.

## Account phase
Until Philip's account has about 50 comment karma (weeks 1–2): **comments only, no Day60 mention or link, no posts.** After that: 9:1 and at most one value post a week. Status lives in `subreddits.md`.

## Daily run (weekdays, 6:15 AM CT; HQ, Nov 18)
Each weekday Philip gets 2 ready replies, about 4 minutes in all. He posts by hand; nothing posts for him, ever. HQ syncs the day's file to the Post Library's "Reddit today". No Reddit API: Reddit's Responsible Builder Policy needs its approval first, and new access requests closed Oct 31, 2026 (HQ dropped the API plan, Nov 18).

**Current mode: bank.** Alerts mode starts only when HQ says Philip's F5Bot alerts are on. Social then changes this line and tells HQ, and the Tue/Fri scans stop.

1. `git pull`, then read this file, `subreddits.md` and `bank.md`.
2. **Alerts mode:**
   - In Gmail, run exactly one search, `from:f5bot.com newer_than:1d`, and read only what it returns. Open no other mail.
   - From each alert take the post's link, sub, title, snippet and time. Never fetch the link: nothing on our side reads Reddit. Philip reads the thread before he posts.
   - Keep posts in the reply subs of `subreddits.md`, under 24 hours old, that ask something the method answers. Skip megathreads and weekly threads, posts that look locked or already answered, and subs whose rules forbid this kind of advice.
   - Pick the best 2, from different subs when you can, and write a reply to each from its title and snippet. If fewer than 2 fit, fill the rest from bank mode and say so.
3. **Bank mode** (until alerts are on, and on thin days): write 2 fresh replies to common questions the method answers, each a new question or a new wording of a bank one, and add them to `bank.md`.
4. **Every reply:** under 120 words, method first, plain and a little messy: short sentences, no polish, no em dashes, no lists unless the post asks. No Day60, no links, no DMs, no founder facts. It has to read like a person.
5. Write `reddit/YYYY-MM-DD.md` (CT date) like `reddit/2026-11-18.md`: the mode, the New feed link, the 2 replies and the founder-fact check. In alerts mode, head each reply with the post's title, then its link, sub and age, and "Read the thread before posting (drafted from the alert's title and snippet)". Store no snippet text, usernames or email addresses.
6. Commit, push, and send HQ one message: the file path, the mode, and each reply's post link, sub and title (its question in bank mode).
- **Tue and Fri, until alerts run:** the 6:37 AM scan adds its threads under a "## Scan" heading in that day's file and leaves the 6:15 part as it is.

### F5Bot alerts (Philip sets them up by hand)
Free email alerts when a keyword appears on Reddit. Keywords match post titles and links (and comments, which we turn off). Matching ignores case and finds the letters inside longer words. Each keyword gets the same flags, typed in F5Bot's flags field with spaces between them: `no-comments only-subreddit=jobs,jobsearchhacks,careerguidance,resumes,recruitinghell,sales,salesdevelopment,csMajors,cscareerquestions,GetEmployed`.
- `hiring manager`
- `cold email`: leave sales and salesdevelopment out of its list (`only-subreddit=jobs,jobsearchhacks,careerguidance,resumes,recruitinghell,csMajors,cscareerquestions,GetEmployed`), since there it's mostly prospecting
- `no interviews`
- `0 interviews` (titles give a count: "applied to N jobs, 0 interviews")
- `no callbacks`
- `ghosted` (titles say "got ghosted" and "ghosted by" as often as "ghosted after")
- `referral`
- `follow up`
- Caveat: F5Bot relies on its own Reddit access, which may end by March 2027.

## Automated scan (from Nov 3; runs once SERPAPI_API_KEY exists)
Each Tue/Fri run (a fresh session that can read the key):
1. `node scripts/reddit-scan.mjs --out /tmp/reddit-scan.json` runs 6 Google searches through SerpAPI (site:reddit.com/r/<sub> + `inurl:comments` + topic keywords, last 4 days: the default window since HQ, Nov 6; `inurl:comments` since HQ, Nov 10, after 17 of 21 results on Nov 10 were sub front pages or how-to pages) for the reply subs in `subreddits.md`. It skips r/SideProject and r/startups, dedupes against threads already in `reddit/*.md`, scrubs usernames and drops threads older than about 7 days (from Google's date or snippet prefix), caps each sub at 2, and keeps the 3–5 best-fitting threads. Check the queries with `--queries` and the parsing with `--fixture scripts/fixtures/serpapi-sample.json`.
   - **Run it with `--debug <scratchpad>/reddit-scan-debug.json` (HQ, Nov 6).** It writes each dropped result's reason (not-thread-url, already-used, duplicate, off-list-sub, negative-match, no-date, too-old, low-score, per-sub-cap, over-max; off-list-sub means the sub isn't a reply sub in `subreddits.md`, and no-date means neither Google's date nor the snippet gives an age, both since HQ, Nov 17), subreddit, title and age, with no snippets or usernames, and prints the counts per reason. Put those counts in the report to HQ. Never commit the file: the script refuses paths inside the repo except the git-ignored `reddit-scan-debug*.json`.
2. Exit 2 means "SERPAPI_API_KEY not set". Use the fallback instead: refresh the search links and add 1–2 replies to the bank. Exit 3 means a SerpAPI error: report it to HQ.
3. For each kept thread, draft a reply from the title and snippet only, headed by the thread link and **"Check the thread before posting (drafted from Google's snippet)"**. Apply the sub's rules, the account phase and 9:1.
4. Write `reddit/YYYY-MM-DD.md` (if the 6:15 AM run already wrote it, add a "## Scan" section to it instead), push, and send HQ one message: file path, then each thread's URL, sub, title and whether it mentions Day60. If fewer than 3 fit, say so; don't pad.
- Never fetch reddit.com, never use mirrors, never store usernames. The key lives only in the environment and is never written to the repo (this repo is public).

## Rhythm
**From Nov 18:** the weekday 6:15 AM run above. The Tue/Fri scan keeps running, into the same day's file, until F5Bot alerts are on.

- **Tue and Fri, 6:37 AM CT** (HQ's scheduled ping): find 3–5 threads under ~48 h old and draft replies in `reddit/YYYY-MM-DD.md`.
- **At most once a week:** one value post, only in a sub whose rules allow it.
- Then send HQ one message: file path, plus each thread's URL, sub, title and whether the reply mentions Day60.

## Finding threads
**Known limit (Nov 3):** web search can't reach reddit.com (Reddit blocks the crawler) and direct fetches return 403. Until that changes, Philip finds 2–3 threads with the sorted-by-New links in the day's file, or pastes thread URLs and text to HQ for tailored drafts. The reply bank is `reddit/bank.md`.

- Web search with `site:reddit.com` (Reddit blocks direct fetches from our containers). Use the thread URLs search returns; never use mirror sites.
- Topics: no replies to applications; how to reach a hiring manager or recruiter; cold outreach to land a job; LinkedIn messages that get answered; referrals; following up.
- Prefer threads that already rank on Google. Skip locked, archived, or already-answered-to-death threads.
- Search snippets can't show the full thread, so each draft notes what was visible and asks Philip to skim the thread before posting.

## Draft format (one block per thread)
```
### <n>. <thread title>
- URL:
- Sub: r/...   · Age: ~XX h   · Mentions Day60: yes/no
- Rule check: <verified rule quote, or "unverified → no mention">
- Why this thread: <one line>

Reply:
<the reply>
```

## Reply rules
- No hashtags in Reddit replies (exempt from the hashtag rule, per HQ Nov 4).
- Method first: answer the actual question with specifics the person can use today. Short paragraphs, plain words, no headings, no bullet walls, no emoji, no em-dashes, no "Great question!".
- Sound like a sales development leader, not a brand. Only facts from playbook.md's "Approved founder facts" that are cleared for Reddit (the four career facts are fine; the ministry line is on hold until Philip confirms it himself, HQ Nov 6; the 722 story is LinkedIn-only; there is no years-in-sales line). **Philip's personal results never go on Reddit.** No invented anecdotes, users, numbers or quotes.
- **9:1:** about nine helpful replies with no mention for every one that mentions Day60.
- Mention Day60 only in a sub where the verified rule allows it, and disclose plainly: "I built a free tool for this, Day60: <link>". Link: `https://getday60.com/try?utm_source=reddit&utm_medium=social&utm_campaign=YYYY-wWW&utm_content=<sub>`.
- Never offer DMs, never ask for upvotes, never post the same reply twice, never reply from any account but Philip's account.
- Never name or link a real hiring manager, recruiter or employee.
