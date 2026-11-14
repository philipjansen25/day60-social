"""Instagram profile-grid preview at phone width (390 px wide, rendered at 2x), newest post top-left.

    python3 templates/grid_preview.py <out.png> <id,id,...oldest first> [--labels] [--live N]

Ids are library.json ids without the week prefix or with it (IG7 or 2026-w46-IG7). Each tile is the post's cover,
cropped to the grid's 3:4 from the center, as Instagram shows it: an image or carousel's first file, a Reel's
cover PNG (listed after the video) or, for a posted Reel, its first frame. --live N marks the oldest N as live
(their current covers, never the new ones). --labels adds the posting order and ground on each tile and a
"Live now" marker, for checking the grid rule; leave it off for the clean picture.
"""
import json, os, subprocess, sys, tempfile
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "design-system"))
from ds import page, INK, CREAM, LIME, COBALT, PINK, MINT, CORAL, MUTED, WHITE  # noqa

args = [a for a in sys.argv[1:] if not a.startswith("--")]
LABELS = "--labels" in sys.argv
LIVE = int(sys.argv[sys.argv.index("--live") + 1]) if "--live" in sys.argv else 0
if LIVE:
    args = [a for a in args if a != str(LIVE)]
out, order = args[0], args[1].split(",")
lib = {p["id"]: p for p in json.load(open(os.path.join(ROOT, "library.json")))}
by_short = {k[9:]: k for k in lib}
TMP = tempfile.mkdtemp(prefix="grid_")
NAMES = {CREAM: "cream", MUTED: "cream", INK: "ink", LIME: "lime", COBALT: "cobalt", PINK: "pink", MINT: "mint", CORAL: "coral"}


def ground(path):
    """Nearest palette color to the cover's top-left corner, the ground the grid reads."""
    px = Image.open(path).convert("RGB").getpixel((6, 6))
    hexes = {c: tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) for c in NAMES}
    return NAMES[min(hexes, key=lambda c: sum((a - b) ** 2 for a, b in zip(hexes[c], px)))]


def cover(p, live):
    fs = p["files"]
    if fs[0]["path"].endswith(".mp4"):
        pngs = [f["path"] for f in fs[1:] if f["path"].endswith(".png")]
        if pngs and not live:
            return os.path.join(ROOT, pngs[0])
        frame = os.path.join(TMP, p["id"] + ".png")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(ROOT, fs[0]["path"]), "-frames:v", "1", frame], check=True)
        return frame
    return os.path.join(ROOT, fs[0]["path"])


tiles = []
for n, pid in enumerate(order, 1):
    p = lib[pid if pid in lib else by_short[pid]]
    live = n <= LIVE
    c = cover(p, live)
    tiles.append({"n": n, "id": p["id"][9:], "src": c, "g": ground(c), "live": live})

S = 2  # 390 px phone width at 2x
W = 390 * S
gap = 2 * S // 2 + 1
tw = (W - 2 * gap) // 3
th = tw * 4 // 3
cells = []
for t in reversed(tiles):  # newest first, left to right
    lab = ""
    if LABELS:
        lab = (f'<span style="position:absolute;left:{6*S}px;bottom:{6*S}px;background:{WHITE};color:{INK};border:{S}px solid {INK};'
               f'border-radius:999px;padding:{1*S}px {5*S}px;font:700 {9*S}px DM Sans,sans-serif">{t["n"]} · {t["id"]} · {t["g"]}'
               f'{" · live" if t["live"] else ""}</span>')
    cells.append(f'<div style="position:relative;width:{tw}px;height:{th}px;overflow:hidden;background:#ddd">'
                 f'<img src="file://{t["src"]}" style="width:100%;height:100%;object-fit:cover;object-position:center;display:block">{lab}</div>')
rows = (len(cells) + 2) // 3
head_h = 54 * S
title = "@getday60 · grid preview" + (" · posting order and grounds" if LABELS else "")
sub = (f"Newest top-left. Top {len(tiles) - LIVE}: next posts, new covers. Below: live now." if LIVE else "Newest top-left.")
body = (f'<div style="position:absolute;left:{14*S}px;top:{10*S}px;font:800 {15*S}px Bricolage Grotesque,sans-serif;letter-spacing:-.02em">{title}</div>'
        f'<div style="position:absolute;left:{14*S}px;top:{31*S}px;font:500 {10.5*S}px DM Sans,sans-serif;color:#5A6972">{sub}</div>'
        f'<div style="position:absolute;left:0;top:{head_h}px;width:{W}px;display:grid;grid-template-columns:repeat(3,{tw}px);gap:{gap}px">'
        + "".join(cells) + "</div>")
if LABELS and LIVE:
    new_rows = (len(tiles) - LIVE + 2) // 3
    y = head_h + new_rows * (th + gap) - gap
    body += f'<div style="position:absolute;left:0;top:{y - 2*S}px;width:{W}px;height:{4*S}px;background:{CORAL}"></div>'
H = head_h + rows * th + (rows - 1) * gap + 12 * S
html = os.path.join(TMP, "grid.html")
open(html, "w").write(page(body, W, H, WHITE))
jf = os.path.join(TMP, "jobs.json")
json.dump([{"html": html, "png": os.path.abspath(out), "w": W, "h": H}], open(jf, "w"))
subprocess.run(["node", os.path.join(ROOT, "templates", "render_many.js"), jf], check=True)
for t in tiles:
    print(t["n"], t["id"], t["g"], "live" if t["live"] else "")
