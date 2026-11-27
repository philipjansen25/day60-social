"""Pick week 51's times in order with scripts/pick_time.py, each pick passed on as taken (Social, Nov 27).
Run from repo root: python3 2026-12/wk51/pick_times.py"""
import subprocess, sys
SLOTS = [
    ("2026-w51-LI-checker", "linkedin", "2026-12-14"),
    ("2026-w51-LI-firstline", "linkedin", "2026-12-15"),
    ("2026-w51-LI-person", "linkedin", "2026-12-16"),
    ("2026-w51-LI-resume", "linkedin", "2026-12-17"),
    ("2026-w51-LI-stages", "linkedin", "2026-12-18"),
    ("2026-w51-LI-shortweek", "linkedin", "2026-12-20"),
    ("2026-w51-IG-tailor", "instagram", "2026-12-15"),
    ("2026-w51-IG-gap", "instagram", "2026-12-16"),
    ("2026-w51-IG-rounds", "instagram", "2026-12-18"),
    ("2026-w51-IG-firstline", "instagram", "2026-12-19"),
    ("2026-w51-IG-wishlist", "instagram", "2026-12-20"),
    ("2026-w51-FB-firstjob", "facebook", "2026-12-14"),
    ("2026-w51-FB-touches", "facebook", "2026-12-15"),
    ("2026-w51-FB-tailor", "facebook", "2026-12-16"),
    ("2026-w51-FB-gap", "facebook", "2026-12-17"),
    ("2026-w51-FB-wishlist", "facebook", "2026-12-18"),
    ("2026-w51-FB-rounds", "facebook", "2026-12-19"),
    ("2026-w51-FB-firstline", "facebook", "2026-12-20"),
]
taken = []
for key, ch, day in SLOTS:
    args = [sys.executable, "scripts/pick_time.py", key, ch, day] + (["--taken"] + taken if taken else [])
    t = subprocess.run(args, capture_output=True, text=True, check=True).stdout.strip().split()[-1]
    print(key, ch, day, t)
    taken += [day, t, ch]
