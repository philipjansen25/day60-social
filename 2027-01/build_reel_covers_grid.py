"""Reel covers for the recycled Reels (HQ, Nov 22: an Instagram Reel cover keeps its key content inside the center
1080x1440, y 240 to 1680, which the profile grid shows).

The Nov 13 covers (2026-11/build_covers.py) put the Day60 footer at y 1800 to 1860, outside that area. These are the same
covers with the footer raised to sit inside it; nothing else changes. New files beside the recycled posts; the old covers
stay where they are.

Run from repo root: python3 2027-01/build_reel_covers_grid.py
"""
import importlib.util, json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "design-system"))
from grounds import foot_g  # noqa: E402

spec = importlib.util.spec_from_file_location("covers", os.path.join(ROOT, "2026-11", "build_covers.py"))
covers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(covers)

FOOT_BOTTOM = 290  # the footer's bottom edge at y 1630, inside 1680
NEW = {  # cover name: (ground, recycled post's folder)
    "p04_one_link_cover": ("mint", "2027-01/wk03"),
    "p03_one_job_cover": ("coral", "2027-01/wk03"),
    "p04_red_pen_cover": ("mint", "2027-01/wk04"),
    "p03_resume_cover": ("cobalt", "2027-01/wk04"),
}
jobs = []
for j in covers.jobs:
    base = os.path.basename(j["png"])
    name = next((n for n in NEW if base == f"{n}_{NEW[n][0]}.png"), None)
    if not name:
        continue
    g, folder = NEW[name]
    html = open(j["html"]).read()
    old, new = foot_g(g), foot_g(g, bottom=FOOT_BOTTOM)
    assert html.count(old) == 1, name
    p = j["html"].replace(".html", "_grid.html")
    open(p, "w").write(html.replace(old, new))
    jobs.append({"html": p, "png": os.path.join(ROOT, folder, f"{name}_{g}_grid.png"), "w": 1080, "h": 1920})
assert len(jobs) == len(NEW), [j["png"] for j in jobs]
jf = os.path.join(covers.TMP, "grid_jobs.json")
json.dump(jobs, open(jf, "w"))
subprocess.run(["node", os.path.join(ROOT, "templates", "render_many.js"), jf], check=True)
print(json.dumps([os.path.relpath(j["png"], ROOT) for j in jobs], indent=1))
