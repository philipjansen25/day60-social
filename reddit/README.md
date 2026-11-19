# Reddit lane

**Back on, alerts only (Philip, Nov 19, via HQ):** "the reddit process is too much manual work. I need you to highlight the threads that I should post in and then generate the copy for me to post". Social picks at most 2 threads a weekday from F5Bot alerts, writes one reply for each, and puts them in the Post Library's Reddit card (`meta/reddit`). Philip opens each thread, reads it once, then pastes the reply as a comment, when he chooses. Reddit never goes on his daily list and never through Buffer. (The lane was stopped from Nov 18 to 19; bank mode ended Nov 19.)

## For a run session (read this first)
- You are Social, Day60's social media employee. HQ is the Claude Code session `session_014zSVjD5hU4eupNEkmMPqQ6`. You never post to Reddit; Philip posts by hand from Philip's account.
- Read in this order: this file, `playbook.md` sections "Approved founder facts", "Voice notes", "Banned phrases" and "Competitors" (never name competitor tools). `reddit/bank.md` is a tone reference only: the daily run neither copies from it nor adds to it.
- Commit with a plain message and push to `main`. The repo is public: never write a username, an email address or personal data into it.

## Account phase
Until Philip's account has about 50 comment karma (weeks 1–2): **comments only, no Day60 mention or link, no posts.** After that: at most one value post a week. Status lives in `subreddits.md`. The daily run's replies never mention Day60 or link, in any phase (HQ, Nov 19).

## Daily run (weekdays, 6:15 AM CT; alerts only from Nov 19, HQ)
Source: F5Bot alert emails only. WebSearch refuses reddit.com, Reddit's API isn't open to us, and mirrors are off limits (HQ, Nov 19).

1. `git pull`, then read this file.
2. **Alerts.** In Gmail, run exactly one search, `from:f5bot.com newer_than:1d`, and read only the alert emails it returns. Open no other mail. From each alert take the post's link, sub, title, snippet and time (the alert's time stands in for the post's). Never open a link. Never fetch reddit.com, old.reddit.com, oauth.reddit.com or any Reddit mirror. Never web-search for Reddit posts.
3. **No alerts, or no post worth a reply: write nothing and stop.** No bank fallback, no feed link, no file, no commit, no message.
4. **Pick at most 2 posts, never comments.** Each one must be:
   - in one of the six reply subs: r/jobs, r/jobsearchhacks, r/careerguidance, r/resumes, r/recruitinghell and r/GetEmployed (skip an alert from any other sub; F5Bot may not have filtered it);
   - under about 18 hours old at run time;
   - written by a job seeker who asks something Phil can answer: reaching the hiring manager, cold email, follow-ups, referrals, no interviews or no callbacks, ghosting.
   Skip rants with no question, sales prospecting, requests for a referral at a named company, megathreads, and any post already in `reddit/days/` (grep its link's post id there). When several fit, prefer the clearest question, then the freshest post.
5. **Write one reply per post, made for that post:**
   - The first line answers that post's question.
   - 50 to 120 words, with 1 or 2 steps they can take today, fitted to the details in the title and snippet.
   - Peer voice and short lines, like `bank.md`. No em dashes.
   - No Day60, no links, no DM offers, no emojis or hashtags.
   - No numbers about Phil's career and no job-search result numbers. Founder facts only from founder.ts (the playbook's "Approved founder facts"), and usually none.
   - Never invent details about the poster beyond the snippet.
   - **why** line: `r/<sub> · <N> h old · <what it asks, 10 words or fewer>`.
6. **Post Library** (https://claude.ai/artifact/N91e3iMns547GJyGKAJrfp), with ArtifactData:
   - `get` collection `meta`, doc `reddit` first. If it exists, `set` it pinned with `if_version`; if it doesn't, create it with `set`. Never write to the `log` collection.
   - Shape: `{date: "YYYY-MM-DD" (CT), how: "Open each thread, read it once, then copy the reply and paste it as a comment. No Day60, no links.", items: [{id: "t1" | "t2", link, sub, title, why, reply}]}`.
   - The link is the post's reddit.com URL, without any query string or tracking.
7. **Repo:** commit `reddit/days/YYYY-MM-DD.md` (CT date) with each item's link, title, why line and reply only. No snippets, usernames, email addresses or personal data. Push to `main`.
8. **Message HQ only if the Post Library write fails** (and say why).

### F5Bot alerts (Philip signs up; HQ's Thu list, task 7, Nov 19)
Free email alerts when a keyword appears on Reddit. Keywords match post titles and links (and comments, which we turn off). Matching ignores case and finds the letters inside longer words. Five keywords, each with the same flag string typed in F5Bot's flags field: `no-comments only-subreddit=jobs,jobsearchhacks,careerguidance,resumes,recruitinghell,GetEmployed` (96 characters; F5Bot's free plan caps the box at 150, so sales, salesdevelopment, csMajors and cscareerquestions are out, Nov 19). Philip may fall back to `no-comments` alone, so the run never assumes F5Bot filtered by sub.
- `hiring manager`
- `cold email`
- `no interviews`
- `ghosted`
- `referral`
- Caveat: F5Bot relies on its own Reddit access, which may end by March 2027.

## History (retired)
The Tue/Fri SerpAPI scan, the sorted-by-New feed links, bank mode and the draft format with Day60 mentions under 9:1 are retired (HQ, Nov 19). Their text is in git history before this file's Nov 19 rewrite; `scripts/reddit-scan.mjs` stays in the repo, unused.
