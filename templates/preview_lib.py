"""Preview page for a date range, built from library.json (the copy Philip posts from).

    python3 templates/preview_lib.py 2026-11-15 2026-11-28 <out_dir> [ids of new posts, comma-separated]

Reads <out_dir>/head.html (the page's header, if any) and writes <out_dir>/index.html and copies every image, PDF page and Reel the posts use to
<out_dir>/assets/<week folder>/<file>, so the folder publishes as one artifact (files map: the assets/ tree).
Single light theme on purpose: posts are previewed on cream, like the brand kit.
"""
import html, json, os, re, shutil, sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
start, end, out = sys.argv[1], sys.argv[2], sys.argv[3]
NEW = set(sys.argv[4].split(",")) if len(sys.argv) > 4 and sys.argv[4] else set()
lib = json.load(open(os.path.join(ROOT, "library.json")))
posts = [p for p in lib if start <= p["date"] <= end and p["status"] != "replaced"]
posts.sort(key=lambda p: (p["date"], p["time"], {"linkedin": 0, "instagram": 1, "facebook": 2}[p["channel"]]))
os.makedirs(os.path.join(out, "assets"), exist_ok=True)
files = {}


def asset(path):
    rel = "assets/" + path.replace("2026-11/", "")
    dst = os.path.join(out, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(os.path.join(ROOT, path), dst)
    files[rel] = dst
    return rel


esc = lambda t: html.escape(t, quote=True)


def fmt(t):
    t = esc(t)
    t = re.sub(r"(https://getday60\.com/\S+)", r'<span class="lnk">\1</span>', t)
    t = re.sub(r"(?<![\w&;/])(#\w+)", r'<span class="tag">\1</span>', t)
    return t.replace("\n", "<br>")


def media(p):
    fs = [f for f in p["files"] if not f["path"].endswith(".pdf")]
    if not fs:
        return ""
    if fs[0]["path"].endswith(".mp4"):
        covers = [f["path"] for f in fs[1:] if f["path"].endswith(".png")]  # a Reel's cover PNG, listed after the video
        poster = f' poster="{asset(covers[0])}"' if covers else ""
        return (f'<div class="media vid"><video src="{asset(fs[0]["path"])}"{poster} controls muted playsinline loop '
                f'preload="metadata" aria-label="{esc(fs[0]["alt"])}"></video></div>')
    if len(fs) > 1:
        imgs = "".join(f'<img src="{asset(f["path"])}" alt="{esc(f["alt"])}" loading="lazy">' for f in fs)
        return f'<div class="media car"><div class="track" tabindex="0">{imgs}</div><div class="hint">{len(fs)} slides · swipe</div></div>'
    return f'<div class="media"><img src="{asset(fs[0]["path"])}" alt="{esc(fs[0]["alt"])}" loading="lazy"></div>'


CH = {"linkedin": ("li", "P", "Phil (LinkedIn profile)", "LinkedIn"),
      "instagram": ("ig", "D", "getday60", "Instagram"),
      "facebook": ("fb", "D", "Day60 Page", "Facebook")}


def when(p):
    d = date.fromisoformat(p["date"])
    h, m = map(int, p["time"].split(":"))
    t = f"{(h - 1) % 12 + 1}:{m:02d} {'AM' if h < 12 else 'PM'}"
    return d.strftime("%a %b ") + str(d.day), t


def card(p):
    cls, av, name, plat = CH[p["channel"]]
    day, t = when(p)
    pid = p["id"][9:]
    status = "New draft" if p["id"] in NEW else p["status"].capitalize()
    pin = f'<span class="pin {"new" if p["id"] in NEW else p["status"]}">{status}</span>'
    extra = ""
    if p["firstComment"]:
        extra += f'<div class="fc"><b>First comment</b> <span class="lnk">{esc(p["firstComment"])}</span></div>'
    det = []
    alts = [f for f in p["files"] if f["alt"]]
    if alts:
        det.append("<div class=\"ml\"><b>Alt text</b> " + " · ".join(
            (f"{i}. " if len(alts) > 1 else "") + esc(f["alt"]) for i, f in enumerate(alts, 1)) + "</div>")
    if p["link"] and p["channel"] != "linkedin":
        det.append(f'<div class="ml"><b>Link</b> {esc(p["link"])}</div>')
    det.append('<div class="ml"><b>Posting notes</b><ul>' + "".join(f"<li>{esc(n)}</li>" for n in p["notes"].split("\n")) + "</ul></div>")
    return (f'<article class="post" id="{esc(p["id"])}"><div class="chip"><span class="id">{esc(pid)}</span>{esc(day)} · {t} · {plat} {pin}</div>'
            f'<div class="frame {cls}"><div class="ph"><div class="av">{av}</div><div><div class="pn">{name}</div>'
            f'<div class="ps">{esc(p["title"])}</div></div><span class="pl">{plat}</span></div>'
            f'{media(p) if p["channel"] != "linkedin" else ""}<div class="cap">{fmt(p["text"]) or "<i>Copy not written yet.</i>"}</div>'
            f'{media(p) if p["channel"] == "linkedin" else ""}{extra}</div>'
            f'<details><summary>Alt text, link and posting notes</summary>{"".join(det)}</details></article>')


rows = "".join(
    f'<tr class="{"isnew" if p["id"] in NEW else ""}"><td>{" ".join(when(p))}</td><td>{CH[p["channel"]][3]}</td>'
    f'<td><a href="#{esc(p["id"])}">{esc(p["id"][9:])}</a></td><td>{esc(p["title"])}</td>'
    f'<td>{"New draft" if p["id"] in NEW else p["status"].capitalize()}</td></tr>' for p in posts)
weeks = {}
for p in posts:
    d = date.fromisoformat(p["date"])
    wk = (d.toordinal() - date(2026, 11, 15).toordinal()) // 7
    weeks.setdefault(wk, []).append(p)
sections = ""
for wk, ps in weeks.items():
    s = date.fromordinal(date(2026, 11, 15).toordinal() + 7 * wk)
    e = date.fromordinal(s.toordinal() + 6)
    sections += (f'<section id="w{wk}"><h2>Week of {s.strftime("%b")} {s.day} <small>Sun {s.strftime("%b")} {s.day} to Sat {e.strftime("%b")} {e.day}</small></h2>'
                 f'<div class="grid">{"".join(card(p) for p in ps)}</div></section>')

tpl = open(os.path.join(ROOT, "templates", "preview_lib_tpl.html")).read()
head = open(os.path.join(out, "head.html")).read() if os.path.exists(os.path.join(out, "head.html")) else ""
page = tpl.replace("{{HEAD}}", head).replace("{{ROWS}}", rows).replace("{{SECTIONS}}", sections)
open(os.path.join(out, "index.html"), "w").write(page)
json.dump(files, open(os.path.join(out, "files.json"), "w"), indent=1)
print(len(posts), "posts,", len(files), "files")
