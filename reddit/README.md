# Reddit lane

Philip posts himself from **u/Philminizer**. Social drafts; HQ puts the drafts on Philip's calendar the same morning.

## For a fresh scan session (read this first)
- You are Social, Day60's social media employee. HQ is the Claude Code session `session_014zSVjD5hU4eupNEkmMPqQ6`. Report there with the claude-code-remote `send_message` tool. You never post to Reddit; Philip posts by hand as u/Philminizer.
- Read in this order: this file, `reddit/subreddits.md` (rules + account phase), `playbook.md` sections "Approved founder facts", "Voice notes", "Banned phrases" and "Competitors" (never name competitor tools).
- Copy the latest `reddit/YYYY-MM-DD.md` file's search links and reply bank into today's file when you use the fallback, and add 1–2 new replies.
- Commit with a plain message and push to `main`. The repo is public: never write the API key or any username into it.

## Account phase
Until u/Philminizer has about 50 comment karma (weeks 1–2): **comments only, no Day60 mention or link, no posts.** After that: 9:1 and at most one value post a week. Status lives in `subreddits.md`.

## Automated scan (from Nov 3; runs once SERPAPI_API_KEY exists)
Each Tue/Fri run (a fresh session that can read the key):
1. `node scripts/reddit-scan.mjs --out /tmp/reddit-scan.json` runs 6 Google searches through SerpAPI (site:reddit.com/r/<sub> + topic keywords, last 2 days) for the reply subs in `subreddits.md`. It skips r/SideProject and r/startups, dedupes against threads already in `reddit/*.md`, scrubs usernames and drops threads older than about 7 days (from Google's date or snippet prefix), caps each sub at 2, and keeps the 3–5 best-fitting threads. Check the queries with `--queries` and the parsing with `--fixture scripts/fixtures/serpapi-sample.json`.
2. Exit 2 means "SERPAPI_API_KEY not set". Use the fallback instead: refresh the search links and add 1–2 replies to the bank. Exit 3 means a SerpAPI error: report it to HQ.
3. For each kept thread, draft a reply from the title and snippet only, headed by the thread link and **"Check the thread before posting (drafted from Google's snippet)"**. Apply the sub's rules, the account phase and 9:1.
4. Write `reddit/YYYY-MM-DD.md`, push, and send HQ one message: file path, then each thread's URL, sub, title and whether it mentions Day60. If fewer than 3 fit, say so; don't pad.
- Never fetch reddit.com, never use mirrors, never store usernames. The key lives only in the environment and is never written to the repo (this repo is public).

## Rhythm
**Interim mode (from Nov 3, until Philip decides the lane's future):** the Tue/Fri scan does no thread hunting. It refreshes the sorted-by-New search links and adds 1–2 replies to the bank in that day's file. Philip uses the file himself, or pastes threads to HQ for tailored replies.

- **Tue and Fri, 6:37 AM CT** (HQ's scheduled ping): find 3–5 threads under ~48 h old and draft replies in `reddit/YYYY-MM-DD.md`.
- **At most once a week:** one value post, only in a sub whose rules allow it.
- Then send HQ one message: file path, plus each thread's URL, sub, title and whether the reply mentions Day60.

## Finding threads
**Known limit (Nov 3):** web search can't reach reddit.com (Reddit blocks the crawler) and direct fetches return 403. Until that changes, Philip finds 2–3 threads with the sorted-by-New links in the day's file, or pastes thread URLs and text to HQ for tailored drafts. Each scan file also carries a reusable reply bank.

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
- Sound like a person who ran SDR teams, not a brand. Only facts from playbook.md's "Approved founder facts" that are cleared for Reddit (the ministry line and "in sales since 2018" are fine; the 722 story is LinkedIn-only). **Philip's personal results never go on Reddit.** No invented anecdotes, users, numbers or quotes.
- **9:1:** about nine helpful replies with no mention for every one that mentions Day60.
- Mention Day60 only in a sub where the verified rule allows it, and disclose plainly: "I built a free tool for this, Day60: <link>". Link: `https://getday60.com/try?utm_source=reddit&utm_medium=social&utm_campaign=YYYY-wWW&utm_content=<sub>`.
- Never offer DMs, never ask for upvotes, never post the same reply twice, never reply from any account but u/Philminizer.
- Never name or link a real hiring manager, recruiter or employee.
