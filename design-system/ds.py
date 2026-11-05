"""Day60 design system for social images (Philip's rule, Nov 5).

Built from the public site (getday60.com): bundled fonts (OFL, licenses beside
them), Tick poses extracted from the prerendered pages, and tokens from
tokens.json (df9b902) as relayed by HQ.

Rules baked in:
- No lime text on cream/white (fill only there, ink text on it). Lime text on ink/navy is fine.
- Coral text uses #C83F19; brand coral #FF5C4D is decoration only.
- Tick is static. No other characters.
- Stickers carry short text, never color alone.
- Invented data only, labeled as an example.

Render with: node templates/render_many.js <jobs.json>
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")

# Light theme
CREAM, INK, WHITE = "#FFF8EC", "#16133A", "#FFFFFF"
LIME = "#D9FF3F"             # no lime text on light backgrounds
COBALT = "#3B5BFF"           # links/progress, white text on it
MUTED, MUTED_TEXT = "#F5EBDD", "#5A6972"
CORAL_TEXT, CORAL = "#C83F19", "#FF5C4D"   # text / decoration only
PINK, MINT = "#FF9BDB", "#6BE3BF"
# Dark surfaces
D_BG, D_CARD, D_MUTED, D_MUTED_TEXT = "#16133A", "#211E49", "#2A2751", "#D4D1E2"

POSES = ("running", "celebrating", "waiting", "waving", "pointing", "thinking")


def _font_face():
    f = lambda n: "file://" + os.path.join(FONT_DIR, n)
    return f"""
@font-face{{font-family:'Bricolage Grotesque';font-weight:200 800;src:url('{f("bricolage-grotesque-latin-a79fdb52d4a5.woff2")}') format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}}
@font-face{{font-family:'Bricolage Grotesque';font-weight:200 800;src:url('{f("bricolage-grotesque-latin-ext-776f6dcaf036.woff2")}') format('woff2');unicode-range:U+0100-02AF,U+0304,U+0308,U+0329,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}}
@font-face{{font-family:'DM Sans';font-weight:100 1000;src:url('{f("dm-sans-latin-ca72d2bcea8f.woff2")}') format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}}
@font-face{{font-family:'DM Sans';font-weight:100 1000;src:url('{f("dm-sans-latin-ext-5d18d31d23ad.woff2")}') format('woff2');unicode-range:U+0100-02AF,U+0304,U+0308,U+0329,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}}
"""


CSS = _font_face() + f"""
*{{box-sizing:border-box}}body{{margin:0}}
.c{{position:relative;overflow:hidden;color:{INK};font-family:'DM Sans',sans-serif;font-weight:500;font-variant-numeric:tabular-nums}}
.d{{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;letter-spacing:-.045em;line-height:.98}}
.lbl{{font-weight:700}}
.card{{background:{WHITE};border:5px solid {INK};border-radius:32px;box-shadow:12px 12px 0 {INK}}}
.muted{{background:{MUTED}}}
.sticker{{display:inline-block;padding:12px 26px;border:4px solid {INK};border-radius:999px;
  font-weight:700;font-size:28px;letter-spacing:.08em;text-transform:uppercase;box-shadow:6px 6px 0 {INK}}}
.btn{{display:inline-block;padding:26px 46px;background:{LIME};color:{INK};border:5px solid {INK};
  border-radius:24px;box-shadow:10px 10px 0 {INK};font-weight:700;font-size:44px}}
.step{{display:inline-flex;align-items:center;justify-content:center;width:120px;height:120px;
  background:{LIME};border:5px solid {INK};border-radius:28px;box-shadow:8px 8px 0 {INK};font-size:64px}}
.fill{{display:inline;background:{LIME};box-decoration-break:clone;-webkit-box-decoration-break:clone;padding:0 12px;border-radius:12px}}
.bubble{{position:relative;background:{WHITE};border:5px solid {INK};border-radius:36px;
  box-shadow:10px 10px 0 {INK};padding:30px 38px;font-size:46px;font-weight:700;line-height:1.15}}
.bubble:after{{content:'';position:absolute;width:44px;height:44px;background:{WHITE};
  border-right:5px solid {INK};border-bottom:5px solid {INK};transform:rotate(45deg)}}
.bubble.down:after{{left:var(--tail,80px);bottom:-27px}}
.bubble.left:after{{left:-27px;top:var(--tail,50px);transform:rotate(135deg)}}
.foot{{position:absolute;left:72px;right:72px;display:flex;justify-content:space-between;align-items:center}}
.logo{{display:flex;align-items:center;gap:18px;font-size:46px}}
.url{{font-size:32px;font-weight:700}}
"""


def tick(pose, w, style=""):
    """Static Tick in one of the site's poses, w px wide."""
    assert pose in POSES, pose
    svg = open(os.path.join(HERE, "tick", f"tick-{pose}.svg")).read()
    h = round(w * 118 / 100)
    svg = svg.replace('width="400" height="472"', f'width="{w}" height="{h}" style="{style}"', 1)
    return svg


def spark(x, y, size, color=PINK):
    return (f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" '
            f'style="position:absolute;left:{x}px;top:{y}px">'
            f'<path d="M12 1l2.6 7.4L22 11l-7.4 2.6L12 21l-2.6-7.4L2 11l7.4-2.6z" '
            f'fill="{color}" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/></svg>')


def check(size=46, ok=True):
    fill = MINT if ok else CORAL
    mark = ('<path d="M12 20.5l5.5 5.5L28.5 14" fill="none" stroke="#16133A" stroke-width="4" '
            'stroke-linecap="round" stroke-linejoin="round"/>' if ok else
            '<path d="M13.5 13.5l13 13M26.5 13.5l-13 13" fill="none" stroke="#16133A" stroke-width="4" stroke-linecap="round"/>')
    return (f'<svg viewBox="0 0 40 40" width="{size}" height="{size}" style="flex:none">'
            f'<circle cx="20" cy="20" r="17" fill="{fill}" stroke="{INK}" stroke-width="3.5"/>{mark}</svg>')


def foot(bottom=60, right="getday60.com", dark=False):
    col = CREAM if dark else INK
    return (f'<div class="foot" style="bottom:{bottom}px;color:{col}"><div class="logo d">'
            f'{tick("waving", 54)}Day60</div><div class="url">{right}</div></div>')


def page(body, w=1080, h=1350, bg=CREAM):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body><div class="c" style="width:{w}px;height:{h}px;background:{bg}">{body}</div></body></html>')
