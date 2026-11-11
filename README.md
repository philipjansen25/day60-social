# day60-social

Day60's social posts (getday60.com): copy, images and the plan.
Buffer is paused (Nov 11): Philip posts by hand from `library.json`. Don't rename or delete a file that a post in `library.json` lists.

- `playbook.md`: Social's playbook (pillars, formats, hashtags, UTMs, voice)
- `library.json`: every planned post (posted, approved, draft, replaced) with its exact text, first comment, link, files in posting order with alt text, and posting notes. Text matches `posts.md` byte for byte; run `node scripts/check-library.mjs` before every push.
- `2026-11/wk1/`: posts for Nov 2, 4 and 6, 2026
- `YYYY-MM/wkWW/`: later weeks, WW = ISO week (e.g. `2026-11/wk46/` for Nov 8–14), with `posts.md`
