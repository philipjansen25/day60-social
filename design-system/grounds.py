"""Cover grounds (Philip, Nov 13, via HQ): every cover takes its background from the whole palette, not cream.

    from grounds import *
    html = cover_page(body, "ink")            # 1080x1350; cover_page(body, g, 1080, 1920) for a Reel cover
    dial(cx, cy, r, g) · lanes(top, n, gap, g) · confetti(spots) · tape(x, top, h)
    page(INK_KEYLINES + body, bg=INK)        # any inner slide or Reel scene on ink: cream keylines

Text that passes AA on each ground (ratios from tokens.json, HQ Nov 13):
  ink    #16133A  cream text (16.7); pink and mint accents; highlight = lime block, ink text
  lime   #D9FF3F  ink text (15.4); emphasis = white boxed words with an ink border
  cobalt #3B5BFF  white text (5.1) or cream (4.8), never ink text (3.5); lime sticker with ink text sits well
  pink   #FF9BDB  ink text (9.2)
  mint   #6BE3BF  ink text (11.3)
  coral  #FF5C4D  ink text only (5.8), display size; never white text (3.1)

Hard rules baked in: lime is never text on any ground. On ink, Tick, cards, bubbles, stickers and buttons
get a cream keyline (ink outlines vanish there). On lime, Tick gets a white halo and the lime button turns
white. Keep one lime button or sticker per image. Color never carries meaning alone.

Grid rule (HQ, Nov 13): any four Instagram posts in a row have four different grounds; cream at most one
post in five. Muted #F5EBDD reads as cream in the grid, so it counts as cream.
"""
from ds import *  # noqa

GROUNDS = {
    "ink":    {"bg": INK,    "text": CREAM, "soft": D_MUTED_TEXT, "dark": True},
    "cobalt": {"bg": COBALT, "text": WHITE, "soft": WHITE,        "dark": True},
    "lime":   {"bg": LIME,   "text": INK,   "soft": INK,          "dark": False},
    "pink":   {"bg": PINK,   "text": INK,   "soft": INK,          "dark": False},
    "mint":   {"bg": MINT,   "text": INK,   "soft": INK,          "dark": False},
    "coral":  {"bg": CORAL,  "text": INK,   "soft": INK,          "dark": False},
}


def _ring(color, px):
    """Outline around an SVG's painted shape (Tick), made of four hard drop-shadows."""
    return " ".join(f"drop-shadow({x}px {y}px 0 {color})" for x, y in ((px, 0), (-px, 0), (0, px), (0, -px)))


def ground_css(g):
    G = GROUNDS[g]
    t = G["text"]
    css = f".c{{color:{t}}}.foot{{color:{t}!important}}.soft{{color:{G['soft']}!important}}"
    css += ".d:has(.fill){line-height:1.1}"  # a highlight block never covers the descenders of the line above
    if G["dark"]:  # light shapes on a dark ground keep ink text
        css += f".card,.bubble,.sticker,.btn,.fill,.step{{color:{INK}}}"
    if g == "ink":
        css += (f".d60-tick{{filter:{_ring(CREAM, 4)}}}"
                f".card,.bubble{{box-shadow:0 0 0 5px {CREAM},14px 14px 0 5px {CREAM}!important}}"
                f".sticker{{box-shadow:0 0 0 4px {CREAM},8px 8px 0 4px {CREAM}!important}}"
                f".btn{{box-shadow:0 0 0 4px {CREAM},12px 12px 0 4px {CREAM}!important}}"
                f".fill{{color:{INK}}}")
    elif g == "cobalt":
        css += f".fill{{color:{INK}}}"
    elif g == "lime":
        css += (f".d60-tick{{filter:{_ring(WHITE, 7)}}}.foot .d60-tick{{filter:{_ring(WHITE, 3)}}}"
                f".fill{{background:{WHITE};border:5px solid {INK};padding:0 14px}}"
                f".btn{{background:{WHITE}}}")
    else:  # pink, mint, coral: lime highlight keeps an ink edge so it reads as a sticker, not a stain
        css += f".fill{{border:5px solid {INK};padding:0 14px}}"
    return f"<style>{css}</style>"


def cover_page(body, g, w=1080, h=1350):
    return page(ground_css(g) + body, w, h, GROUNDS[g]["bg"])


def foot_g(g, **kw):
    return foot(dark=GROUNDS[g]["dark"], **kw)


def _tone(g):
    """A quiet same-family tone for big background shapes: ink at low opacity, or cream on ink."""
    return (CREAM, 0.09) if g == "ink" else (INK, 0.13)


def dial(cx, cy, r, g, color=None, opacity=None, sw=None):
    """Day60's 60-mark stopwatch dial as a giant background shape, centered at (cx, cy); crops at the edges."""
    col, op = _tone(g)
    col, op = color or col, opacity if opacity is not None else op
    sw = sw or max(10, r // 22)
    s = r + 140
    marks = []
    for k in range(60):
        big = k % 5 == 0
        L = r * (0.16 if big else 0.08)
        marks.append(f'<line x1="0" y1="{-r * 0.86:.1f}" x2="0" y2="{-r * 0.86 + L:.1f}" stroke-width="{sw if big else sw * 0.5:.1f}" '
                     f'transform="rotate({k * 6})"/>')
    return (f'<svg width="{2 * s}" height="{2 * s}" viewBox="{-s} {-s} {2 * s} {2 * s}" '
            f'style="position:absolute;left:{cx - s}px;top:{cy - s}px;opacity:{op}">'
            f'<g fill="none" stroke="{col}" stroke-linecap="round">'
            f'<circle r="{r}" stroke-width="{sw * 1.6:.1f}"/>'
            f'<rect x="{-r * 0.11:.1f}" y="{-r - r * 0.24:.1f}" width="{r * 0.22:.1f}" height="{r * 0.16:.1f}" rx="{r * 0.04:.1f}" stroke-width="{sw:.1f}"/>'
            f'{"".join(marks)}'
            f'<line x1="0" y1="0" x2="0" y2="{-r * 0.62:.1f}" stroke-width="{sw * 1.3:.1f}"/>'
            f'<circle r="{r * 0.05:.1f}" fill="{col}" stroke="none"/></g></svg>')


def lanes(top, n, gap, g, w=1080, color=None, opacity=None, dash=True):
    """Running-track lane lines across the cover, starting at `top`."""
    col, op = _tone(g)
    col, op = color or col, opacity if opacity is not None else op
    lines = "".join(f'<line x1="0" y1="{k * gap}" x2="{w}" y2="{k * gap}"'
                    f'{" stroke-dasharray=\"60 34\"" if dash and 0 < k < n else ""}/>' for k in range(n + 1))
    return (f'<svg width="{w}" height="{n * gap + 12}" viewBox="0 -6 {w} {n * gap + 12}" '
            f'style="position:absolute;left:0;top:{top}px;opacity:{op}"><g stroke="{col}" stroke-width="8" '
            f'stroke-linecap="round">{lines}</g></svg>')


def tape(x, top, h, color=PINK, w=34):
    """Finish tape: a solid ribbon across the lanes, ink-edged like every sticker."""
    return (f'<div style="position:absolute;left:{x}px;top:{top}px;width:{w}px;height:{h}px;background:{color};'
            f'border:4px solid {INK};border-radius:8px;transform:rotate(-4deg)"></div>')


def confetti(spots):
    """spots: (x, y, kind, color, size, rotation); kinds: dot, bar, ring, spark. Ink-edged, accent colors only."""
    out = ""
    for x, y, kind, col, size, rot in spots:
        if kind == "spark":
            out += spark(x, y, size, col)
            continue
        if kind == "dot":
            shape = f'<circle cx="20" cy="20" r="15" fill="{col}" stroke="{INK}" stroke-width="3.5"/>'
        elif kind == "ring":
            shape = f'<circle cx="20" cy="20" r="13" fill="none" stroke="{col}" stroke-width="7"/>'
        else:
            shape = f'<rect x="4" y="13" width="32" height="14" rx="5" fill="{col}" stroke="{INK}" stroke-width="3.5"/>'
        out += (f'<svg viewBox="0 0 40 40" width="{size}" height="{size}" '
                f'style="position:absolute;left:{x}px;top:{y}px;transform:rotate({rot}deg)">{shape}</svg>')
    return out


# Inner slides on ink (HQ, Nov 13): add to the body of any ink page. Tick gets a cream ring; cards, stickers,
# buttons, bubbles and step blocks get a cream outline outside their ink border, so they still read as
# thick-outlined stickers. Outline (not box-shadow) keeps each shape's own hard shadow, e.g. a lime one.
INK_KEYLINES = (f"<style>.d60-tick{{filter:{_ring(CREAM, 4)}}}.foot .d60-tick{{filter:{_ring(CREAM, 2)}}}"
                f".card,.sticker,.btn,.bubble,.step{{outline:4px solid {CREAM};outline-offset:0}}</style>")
