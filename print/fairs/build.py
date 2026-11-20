"""Career-fair print kit (HQ, Nov 19): handout, QR card and table sign for one event.

Usage:  python3 print/fairs/build.py <slug>        e.g. austin-test
Writes: print/fairs/<slug>/handout.pdf, qr-card.pdf, table-sign.pdf, and a PNG preview of each.

Every QR code opens https://getday60.com/try?utm_source=career_fair&utm_medium=qr&utm_campaign=<slug>.
Before anything is written, the script renders each PDF page back to pixels, decodes every QR code it finds
and fails unless each piece has its codes where expected and each decodes to that exact link. render_pdf.js
also fails a piece with lime text, more or fewer than one lime element, or anything inside the print margin.

Needs: Playwright (preinstalled in the session), poppler-utils (pdftoppm), and pip install segno zxing-cpp pillow.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "design-system"))
import ds  # noqa: E402  (tokens, fonts, Tick)
from ds import CREAM, INK, WHITE, LIME, PINK, MINT, COBALT, CORAL  # noqa: E402

import segno  # noqa: E402
import zxingcpp  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

BASE = "https://getday60.com/try?utm_source=career_fair&utm_medium=qr&utm_campaign="

# The words (HQ, Nov 19). HQ shows Philip these before anything prints. Nothing else that promises anything:
# no result numbers, no prices, no "free forever", no "verified work emails". The handout carries no founder facts.
HEAD_1 = "You met the recruiter."
HEAD_2 = "Now reach the people closest to the hire."
SITE_LINE = ("Day60 helps you identify the four people closest to the hire: the hiring manager, "
             "their boss, an internal champion and the recruiter.")
ROLES = ("Hiring manager", "Their boss", "Internal champion", "Recruiter")
STEP = "Paste a job link. See the 4 people."
ACTION = "Try it free on one job"
ADDRESS = "getday60.com"
STEP_2L = STEP.replace(". ", ".<br>", 1)  # one sentence a line

IN = 96  # CSS px per inch


def qr_svg(url, size_px):
    """The code as filled squares (no hairline seams in print), ink on white, 4-module quiet zone."""
    q = segno.make(url, error="m")
    n = q.symbol_size(border=4)[0]
    d = []
    for y, row in enumerate(q.matrix):
        for x, v in enumerate(row):
            if v:
                d.append(f"M{x + 4} {y + 4}h1v1h-1z")
    return (f'<svg class="qr" viewBox="0 0 {n} {n}" width="{size_px}" height="{size_px}" shape-rendering="crispEdges">'
            f'<rect width="{n}" height="{n}" fill="{WHITE}"/><path fill="{INK}" d="{"".join(d)}"/></svg>')


def logo(tick_w, font_px, gap=None):
    gap = gap if gap is not None else round(font_px * 0.3)
    return (f'<div class="logo d" style="font-size:{font_px}px;gap:{gap}px">'
            f'{ds.tick("waving", tick_w)}<span>Day60</span></div>')


def spark(x, y, size, color=PINK):
    return (f'<svg class="bleed-art" viewBox="0 0 24 24" width="{size}" height="{size}" '
            f'style="position:absolute;left:{x}px;top:{y}px">'
            f'<path d="M12 1l2.6 7.4L22 11l-7.4 2.6L12 21l-2.6-7.4L2 11l7.4-2.6z" '
            f'fill="{color}" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/></svg>')


CSS = ds._font_face() + f"""
@page{{margin:0}}
*{{box-sizing:border-box}}html,body{{margin:0;padding:0}}
body{{color:{INK};font-family:'DM Sans',sans-serif;font-weight:500;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg{{position:relative;overflow:hidden;break-after:page}}
.pg:last-child{{break-after:auto}}
.d{{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;letter-spacing:-.035em;line-height:1}}
.logo{{display:flex;align-items:center}}
.btn{{display:inline-block;background:{LIME};color:{INK};border:solid {INK};font-weight:700;line-height:1.1;white-space:nowrap}}
.card{{background:{WHITE};border:solid {INK}}}
.qrbox{{display:flex;flex-direction:column;align-items:center}}
.addr{{font-weight:700;letter-spacing:.01em;line-height:1}}
"""


def doc(w_in, h_in, pages):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}'
            f'@page{{size:{w_in}in {h_in}in}}</style></head><body>{"".join(pages)}</body></html>')


def page(w_in, h_in, bg, safe_px, body):
    return (f'<div class="pg" data-safe="{safe_px}" style="width:{w_in * IN}px;height:{h_in * IN}px;'
            f'background:{bg}">{body}</div>')


# ---------- 1. Handout: US Letter portrait, office printer (white page, nothing within 0.5 in of the edge) ----------
def handout(url):
    M = 56  # 0.58 in margin; the check allows 0.5 in
    badge = [(COBALT, WHITE), (PINK, INK), (MINT, INK), (CREAM, INK)]
    cards = []
    for i, (role, (bg, fg)) in enumerate(zip(ROLES, badge)):
        met = (f'<div style="position:absolute;right:-14px;top:-14px">{ds.check(40)}</div>' if role == "Recruiter" else "")
        cards.append(
            f'<div class="card" data-shadow="5" style="position:relative;flex:1;border-width:3px;border-radius:18px;'
            f'box-shadow:5px 5px 0 {INK};padding:20px 16px 24px">{met}'
            f'<div class="d" style="width:50px;height:50px;border-radius:50%;background:{bg};color:{fg};border:3px solid {INK};'
            f'display:flex;align-items:center;justify-content:center;font-size:27px;letter-spacing:0">{i + 1}</div>'
            f'<div class="d" style="margin-top:16px;font-size:25px;line-height:1.05;letter-spacing:-.02em">{role}</div></div>')
    body = f"""
<div style="position:absolute;left:{M}px;right:{M}px;top:{M}px;bottom:{M}px;display:flex;flex-direction:column">
  {logo(40, 32)}
  <div class="d" style="margin-top:48px;font-size:60px;line-height:1.02">{HEAD_1}<br>{HEAD_2.replace(" closest", "<br>closest")}</div>
  <div style="margin-top:26px;font-size:21px;line-height:1.42;max-width:660px">{SITE_LINE}</div>
  <div style="margin-top:36px;display:flex;gap:18px;padding-right:5px">{"".join(cards)}</div>
  <div class="card" data-shadow="8" style="margin-top:auto;margin-bottom:8px;margin-right:8px;background:{CREAM};border-width:4px;border-radius:26px;
       box-shadow:8px 8px 0 {INK};padding:30px 28px 30px 34px;display:flex;align-items:center;gap:18px">
    <div style="flex:1">
      <div class="d" style="font-size:38px;line-height:1.05">{STEP_2L}</div>
      <div style="margin-top:26px;display:flex;align-items:center;gap:14px">
        <div class="btn" data-shadow="5" style="font-size:23px;padding:14px 20px;border-width:3px;border-radius:16px;box-shadow:5px 5px 0 {INK}">{ACTION}</div>
      </div>
    </div>
    <div style="display:flex;align-items:flex-end;gap:6px">
      <div style="margin-bottom:36px">{ds.tick("pointing", 72)}</div>
      <div class="qrbox"><div class="card" style="border-width:3px;border-radius:14px;padding:4px;line-height:0">{qr_svg(url, 184)}</div>
        <div class="addr" style="margin-top:10px;font-size:22px">{ADDRESS}</div></div>
    </div>
  </div>
</div>
{spark(736, 64, 34)}{spark(700, 40, 18, MINT)}"""
    return doc(8.5, 11, [page(8.5, 11, WHITE, 48, body)])


# ---------- 2. QR card: 3.5 x 2 in, front and back, 0.125 in bleed (page 3.75 x 2.25 in) ----------
# Trim is 12 px in from each page edge; everything but the ground and sparkles stays 0.125 in inside the trim.
def qr_card(url):
    S = 26  # 24 px = 0.125 in bleed + 0.125 in safe; 2 px spare
    front = f"""
<div style="position:absolute;left:{S}px;top:{S}px">{logo(24, 19)}</div>
<div class="d" style="position:absolute;left:{S}px;bottom:{S}px;width:226px;font-size:19.5px;line-height:1.04">{HEAD_1} {HEAD_2}</div>
<div style="position:absolute;right:{S + 2}px;bottom:{S}px">{ds.tick("running", 62)}</div>
{spark(300, 30, 20)}{spark(282, 58, 11, MINT)}"""
    back = f"""
<div class="qrbox" style="position:absolute;left:{S}px;top:{S}px">
  <div style="line-height:0">{qr_svg(url, 112)}</div>
  <div class="addr" style="margin-top:3px;font-size:12px">{ADDRESS}</div>
</div>
<div style="position:absolute;left:{S + 126}px;right:{S}px;top:{S}px;bottom:{S}px;display:flex;flex-direction:column;justify-content:center">
  <div class="d" style="font-size:18px;line-height:1.06">{STEP_2L}</div>
  <div style="margin-top:12px"><div class="btn" data-shadow="3" style="font-size:12px;padding:7px 10px;border-width:2px;border-radius:9px;box-shadow:3px 3px 0 {INK}">{ACTION}</div></div>
</div>"""
    return doc(3.75, 2.25, [page(3.75, 2.25, CREAM, 24, front), page(3.75, 2.25, WHITE, 24, back)])


# ---------- 3. Table sign: US Letter portrait, read from 6 ft ----------
def table_sign(url):
    M = 52
    body = f"""
<div style="position:absolute;left:{M}px;right:{M}px;top:{M}px;bottom:{M}px;display:flex;flex-direction:column">
  {logo(50, 40)}
  <div class="d" style="margin-top:26px;font-size:62px;letter-spacing:-.03em">{HEAD_1}</div>
  <div class="d" style="margin-top:12px;font-size:96px;line-height:.96">{HEAD_2}</div>
  <div class="d" style="margin-top:30px;font-size:52px;line-height:1.02;letter-spacing:-.025em">{STEP_2L}</div>
  <div style="margin-top:auto;display:flex;align-items:flex-end;gap:22px">
    <div style="flex:1;display:flex;flex-direction:column;align-items:flex-start;padding-bottom:62px;padding-right:8px">
      <div style="align-self:flex-end;margin-right:4px;margin-bottom:8px">{ds.tick("pointing", 112)}</div>
      <div class="btn" data-shadow="7" style="font-size:46px;padding:20px 28px;border-width:4px;border-radius:22px;box-shadow:7px 7px 0 {INK};line-height:1.05">{ACTION.replace(" on ", "<br>on ", 1)}</div>
    </div>
    <div class="qrbox"><div class="card" style="border-width:4px;border-radius:18px;padding:5px;line-height:0">{qr_svg(url, 262)}</div>
      <div class="addr" style="margin-top:12px;font-size:46px;letter-spacing:-.01em">{ADDRESS}</div></div>
  </div>
</div>
{spark(722, 50, 44)}{spark(680, 30, 22, MINT)}"""
    return doc(8.5, 11, [page(8.5, 11, WHITE, 48, body)])


PIECES = [  # name, builder, page size (in), QR codes expected on each page
    ("handout", handout, (8.5, 11), [1]),
    ("qr-card", qr_card, (3.75, 2.25), [0, 1]),
    ("table-sign", table_sign, (8.5, 11), [1]),
]


def pages_png(pdf, dpi, outprefix):
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", pdf, outprefix], check=True)
    d = os.path.dirname(outprefix)
    base = os.path.basename(outprefix)
    return sorted(os.path.join(d, f) for f in os.listdir(d) if f.startswith(base + "-") and f.endswith(".png"))


def decode_check(name, pdf, want, url, tmp):
    errs = []
    for dpi in (300, 150):
        pngs = pages_png(pdf, dpi, os.path.join(tmp, f"chk-{name}-{dpi}"))
        if len(pngs) != len(want):
            errs.append(f"{name}: {len(pngs)} pages, want {len(want)}")
            continue
        for i, (png, n) in enumerate(zip(pngs, want)):
            codes = [r.text for r in zxingcpp.read_barcodes(Image.open(png).convert("L")) if r.format == zxingcpp.BarcodeFormat.QRCode]
            if len(codes) != n:
                errs.append(f"{name} page {i + 1} at {dpi} dpi: {len(codes)} QR codes, want {n}")
            for c in codes:
                if c != url:
                    errs.append(f"{name} page {i + 1} at {dpi} dpi: decodes to {c!r}, want {url!r}")
                else:
                    print(f"  {name} page {i + 1} at {dpi} dpi: decodes to the exact link")
    return errs


def previews(name, pdf, out_png, tmp):
    if name != "qr-card":
        [png] = pages_png(pdf, 150, os.path.join(tmp, f"pv-{name}"))
        shutil.copy(png, out_png)
        return
    # Card: both sides cut to the 3.5 x 2 in trim, front left and back right, on a grey table.
    dpi = 300
    sides = [Image.open(p).convert("RGB") for p in pages_png(pdf, dpi, os.path.join(tmp, "pv-card"))]
    b = round(0.125 * dpi)
    sides = [s.crop((b, b, s.width - b, s.height - b)) for s in sides]
    w, h = sides[0].size
    pad, gap = 60, 60
    sheet = Image.new("RGB", (pad * 2 + w * 2 + gap, pad * 2 + h), "#D9D6CF")
    d = ImageDraw.Draw(sheet)
    for i, s in enumerate(sides):
        x = pad + i * (w + gap)
        sheet.paste(s, (x, pad))
        d.rectangle((x - 1, pad - 1, x + w, pad + h), outline="#9A968C", width=2)
    sheet.save(out_png)


def main():
    if len(sys.argv) != 2 or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", sys.argv[1]) or len(sys.argv[1]) > 40:
        sys.exit("usage: python3 print/fairs/build.py <slug>   (lowercase letters, digits and hyphens, e.g. austin-test)")
    slug = sys.argv[1]
    url = BASE + slug
    out_dir = os.path.join(HERE, slug)
    tmp = tempfile.mkdtemp(prefix="fairs-")
    try:
        jobs = []
        for name, build, (w, h), _ in PIECES:
            html = os.path.join(tmp, f"{name}.html")
            with open(html, "w") as f:
                f.write(build(url))
            jobs.append({"html": html, "pdf": os.path.join(tmp, f"{name}.pdf"), "w": f"{w}in", "h": f"{h}in"})
        with open(os.path.join(tmp, "jobs.json"), "w") as f:
            json.dump(jobs, f)
        r = subprocess.run(["node", os.path.join(HERE, "render_pdf.js"), os.path.join(tmp, "jobs.json")])
        if r.returncode:
            sys.exit("render checks failed; nothing written")
        errs = []
        for (name, _, _, want), job in zip(PIECES, jobs):
            errs += decode_check(name, job["pdf"], want, url, tmp)
        if errs:
            sys.exit("QR check failed; nothing written:\n  " + "\n  ".join(errs))
        os.makedirs(out_dir, exist_ok=True)
        for (name, _, _, _), job in zip(PIECES, jobs):
            shutil.copy(job["pdf"], os.path.join(out_dir, f"{name}.pdf"))
            previews(name, job["pdf"], os.path.join(out_dir, f"{name}.png"), tmp)
        print(f"wrote {os.path.relpath(out_dir, ROOT)}/ for {url}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
