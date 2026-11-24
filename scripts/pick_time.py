#!/usr/bin/env python3
"""Pick a post's time: a random minute inside its channel's window for that weekday (playbook §5; Philip, Nov 22).

Usage: python3 scripts/pick_time.py <library id> <linkedin|instagram|facebook> <YYYY-MM-DD> [--taken YYYY-MM-DD HH:MM channel ...]

Rules: Central Time; the minute is never a multiple of 5; any two posts on one day are at least 20 minutes apart
(so no two channels share a minute); a channel never posts at the same clock time two days running. The pick is
seeded by the library id, so a re-run gives the same answer. Times already taken come from library.json (posts still
to post) plus any --taken triples (HQ's own posts in Buffer, which aren't in this repo).
Sources for the windows: Buffer's 2026 best-time studies (median engagement per post), Sprout Social's March 2026
data where Buffer's is thin, and Indeed Hiring Lab's "Timing matters in the job search" (2017) as the tie-breaker.
"""
import datetime, hashlib, json, os, random, sys

H = lambda h, m=0: h * 60 + m
# weekday(): Mon=0 .. Sun=6; [start, end) in minutes after midnight, Central Time
WINDOWS = {
    # Philip, Tue Nov 24, 2026 (via HQ): "All LinkedIn posts should go out between 8am-1pm". Latest 12:59 PM CT, every day.
    "linkedin":  {d: (H(8), H(13)) for d in (6, 0, 1, 2, 3, 4)},
    "instagram": {6: (H(20), H(23)), 0: (H(18), H(21)), 1: (H(15), H(20)), 2: (H(12), H(19)), 3: (H(7), H(10)), 4: (H(21), H(23)), 5: (H(20), H(23))},
    "facebook":  {6: (H(8), H(11)), 0: (H(19), H(23)), 1: (H(7), H(9)), 2: (H(8), H(10)), 3: (H(8), H(11)), 4: (H(6), H(9)), 5: (H(21), H(23))},
}
GAP = 20


def tmin(s):
    h, m = s.split(":")
    return int(h) * 60 + int(m)


def ok(channel, day, m, taken):
    if m % 5 == 0:
        return False
    d = datetime.date.fromisoformat(day)
    for dd, mm, ch in taken:
        dd = datetime.date.fromisoformat(dd)
        if dd == d and abs(mm - m) < GAP:
            return False
        if ch == channel and abs((dd - d).days) == 1 and mm == m:
            return False
    return True


def pick(key, channel, day, taken):
    wd = datetime.date.fromisoformat(day).weekday()
    if wd not in WINDOWS[channel]:
        raise SystemExit(f"{channel} doesn't post on {day} (LinkedIn is Sun to Fri)")
    a, b = WINDOWS[channel][wd]
    cands = [m for m in range(a, b) if m % 5]
    random.Random(int(hashlib.sha256(key.encode()).hexdigest(), 16)).shuffle(cands)
    for m in cands:
        if ok(channel, day, m, taken):
            return "%02d:%02d" % divmod(m, 60)
    raise SystemExit(f"no free time for {key} on {day}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        raise SystemExit(__doc__)
    key, channel, day = sys.argv[1:4]
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lib = json.load(open(os.path.join(root, "library.json")))
    taken = [(p["date"], tmin(p["time"]), p["channel"]) for p in lib
             if p["id"] != key and p["status"] in ("draft", "approved")]
    extra = sys.argv[4:]
    if extra:
        assert extra[0] == "--taken" and (len(extra) - 1) % 3 == 0, "use --taken YYYY-MM-DD HH:MM channel ..."
        taken += [(extra[i], tmin(extra[i + 1]), extra[i + 2]) for i in range(1, len(extra), 3)]
    print(pick(key, channel, day, taken))
