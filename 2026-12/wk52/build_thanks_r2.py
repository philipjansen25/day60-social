"""IG-thanks-r2 (Mon Dec 21, 2026): the Thanksgiving thank-you carousel, recycled for holiday week.

HQ, Nov 22: Meta Business Suite cropped the natively scheduled IG-thanks, so it comes back through Buffer.
Same design and slides; three slides lose their Thanksgiving words (needs HQ's yes, since the words change):
  cover    sticker "Thanksgiving week"   -> "Holiday week"
  slide 5  "Send it before Thursday."    -> "Send it before the holidays."
  slide 6  "Happy Thanksgiving."         -> "Happy holidays."
Slides 2 to 4 are the week 48 files, unchanged. The HTML comes from the scripts that made the originals
(2026-11/build_covers.py for the pink cover, 2026-11/wk48/build.py for slides 5 and 6), with only those words swapped.

Run from the repo root: python3 2026-12/wk52/build_thanks_r2.py
"""
import importlib.util, json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # both scripts only collect HTML on import; they render under __main__
    return mod


covers = load("covers48", "2026-11/build_covers.py")
wk48 = load("wk48build", "2026-11/wk48/build.py")
TMP = tempfile.mkdtemp(prefix="thanks_r2_")
jobs = []


def swap(html, pairs, what):
    for a, b in pairs:
        if html.count(a) != 1:
            sys.exit(f"{what}: expected one '{a}'")
        html = html.replace(a, b)
    return html


def job(name, html):
    p = os.path.join(TMP, name + ".html")
    open(p, "w").write(html)
    jobs.append({"html": p, "png": os.path.join(HERE, name + ".png"), "w": 1080, "h": 1350})


cover = next(j for j in covers.jobs if os.path.basename(j["png"]) == "p01_thanks_1_pink.png")
job("p01_thanks_1_pink_holiday", swap(open(cover["html"]).read(), [("Thanksgiving week", "Holiday week")], "cover"))
slides = dict(wk48.thanks())
job("p01_thanks_5_holiday", swap(slides["p01_thanks_5"], [("Send it before Thursday.", "Send it before the holidays.")], "slide 5"))
job("p01_thanks_6_holiday", swap(slides["p01_thanks_6_v2"], [("Happy Thanksgiving.", "Happy holidays.")], "slide 6"))

jf = os.path.join(TMP, "jobs.json")
json.dump(jobs, open(jf, "w"))
subprocess.run(["node", os.path.join(ROOT, "templates", "render_many.js"), jf], check=True)
