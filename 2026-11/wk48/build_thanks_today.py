"""FB-thanks through Buffer on Thanksgiving Day (HQ, Nov 23: Philip deleted the natively scheduled copy).

The post now goes out on Thu Nov 26 itself, so slide 5's "Send it before Thursday." reads wrong.
One swap, from the HTML of the original (2026-11/wk48/build.py), the way 2026-12/wk52/build_thanks_r2.py does it:
  slide 5  "Send it before Thursday."  ->  "Send it today."
Slides 1 to 4 and 6 stay the week 48 files.

Run from the repo root: python3 2026-11/wk48/build_thanks_today.py
"""
import importlib.util, json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
spec = importlib.util.spec_from_file_location("wk48build", os.path.join(HERE, "build.py"))
wk48 = importlib.util.module_from_spec(spec); spec.loader.exec_module(wk48)
html = dict(wk48.thanks())["p01_thanks_5"]
a, b = "Send it before Thursday.", "Send it today."
if html.count(a) != 1:
    sys.exit("slide 5: expected one '%s'" % a)
TMP = tempfile.mkdtemp(prefix="thanks_today_")
p = os.path.join(TMP, "p01_thanks_5_today.html"); open(p, "w").write(html.replace(a, b))
jf = os.path.join(TMP, "jobs.json")
json.dump([{"html": p, "png": os.path.join(HERE, "p01_thanks_5_today.png"), "w": 1080, "h": 1350}], open(jf, "w"))
subprocess.run(["node", os.path.join(ROOT, "templates", "render_many.js"), jf], check=True)
