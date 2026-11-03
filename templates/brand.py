"""Day60 brand building blocks for social images.

Each function returns an HTML string for one 1080-wide canvas.
Render with: node templates/render_many.js <jobs.json>
"""

FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Bricolage+Grotesque:opsz,wght@12..96,800&'
         'family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,700&display=swap">')

INK, CREAM, LIME, CORAL, BLUE, PINK, WHITE = (
    "#16133A", "#FFF8EC", "#D9FF3F", "#FF5C4D", "#3B5BFF", "#FF9BDB", "#FFFFFF")

CSS = f"""
*{{box-sizing:border-box}}body{{margin:0}}
.c{{position:relative;overflow:hidden;color:{INK};font-family:'DM Sans',sans-serif}}
.bg{{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;letter-spacing:-.045em}}
.pill{{display:inline-block;padding:16px 30px;border:4px solid {INK};border-radius:40px;
  box-shadow:7px 7px 0 {INK};font-weight:700;font-size:26px;letter-spacing:.12em}}
.box{{border:5px solid {INK};border-radius:22px;box-shadow:12px 12px 0 {INK}}}
.hl{{display:inline-block;padding:0 18px 6px;background:{LIME};border:5px solid {INK};
  border-radius:16px;box-shadow:8px 8px 0 {INK}}}
.foot{{position:absolute;left:72px;right:72px;bottom:56px;display:flex;
  justify-content:space-between;align-items:center}}
.logo{{display:flex;align-items:center;gap:20px;font-size:44px}}
.url{{font-size:31px;font-weight:700}}
"""


def spark(x, y, size, color):
    return (f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" '
            f'style="position:absolute;left:{x}px;top:{y}px">'
            f'<path d="M12 1l2.6 7.4L22 11l-7.4 2.6L12 21l-2.6-7.4L2 11l7.4-2.6z" '
            f'fill="{color}" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/></svg>')


def tick(x, y, w, face=LIME):
    h = round(w * 118 / 100)
    return f'''<svg viewBox="0 0 100 118" width="{w}" height="{h}" style="position:absolute;left:{x}px;top:{y}px">
<g stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
<path d="M25 53C12 53 10 43 17 39L25 43M75 52C87 50 89 40 81 36L75 40" fill="none"/>
<path d="M40 83C33 91 23 96 15 94M61 82C72 86 78 83 81 73" fill="none"/>
<path d="M7 93l10 1 5 7-19-1c-3-3 0-7 4-7ZM79 69l10 3 3 7-16-3c-3-3-1-7 3-7Z" fill="{CREAM}"/>
<path d="M46 21h8v10h-8z" fill="{BLUE}"/><path d="M39 13h22v10H39z" fill="{PINK}"/>
<path d="m68 31 9-9 8 8-9 9" fill="{CORAL}"/>
<path d="M50 27c17-1 30 12 30 29s-12 31-29 31S20 75 20 58s12-30 30-31z" fill="{face}"/>
<path d="m29 52 4 1m-6 8h5m-2 9 4-2m3 11 3-4m10 7v-5m12 3-3-5m12-6-5-2m8-8h-5m3-9-5 2" fill="none" stroke-width="1.7"/>
<path d="M27 39c13-5 32-5 46 0l4 10c-17-6-36-6-53 0z" fill="{PINK}" stroke-width="3"/>
<path d="M27 44c15-5 31-5 46 0" fill="none" stroke="{CORAL}" stroke-width="2"/>
<circle cx="42" cy="56" r="1.8" fill="{INK}" stroke="none"/><circle cx="59" cy="56" r="1.8" fill="{INK}" stroke="none"/>
<path d="M44 65c4 4 8 4 12 0" fill="{INK}"/><path d="M51 62v-6m0 6 6-3" fill="none" stroke-width="2"/>
</g></svg>'''


LOGO_SVG = (f'<svg viewBox="0 0 40 44" width="48" height="53"><g stroke="{INK}" stroke-width="3" '
            f'stroke-linejoin="round"><rect x="15" y="2" width="10" height="6" fill="{CORAL}"/>'
            f'<circle cx="20" cy="26" r="16" fill="{LIME}"/><path d="M20 26v-8M20 26l6 4" fill="none" '
            f'stroke-linecap="round"/></g></svg>')


def foot(right="getday60.com", bottom=56):
    return (f'<div class="foot" style="bottom:{bottom}px"><div class="logo bg">{LOGO_SVG}Day60</div>'
            f'<div class="url">{right}</div></div>')


def page(body, w=1080, h=1350, bg=CREAM):
    return (f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{CSS}</style></head>'
            f'<body><div class="c" style="width:{w}px;height:{h}px;background:{bg}">{body}</div></body></html>')


def mark(ok):
    """A round check (ok=True) or cross badge."""
    if ok:
        return (f'<svg viewBox="0 0 40 40" width="46" height="46" style="flex:none"><circle cx="20" cy="20" r="17" '
                f'fill="{LIME}" stroke="{INK}" stroke-width="3.5"/><path d="M12 20.5l5.5 5.5L28.5 14" fill="none" '
                f'stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    return (f'<svg viewBox="0 0 40 40" width="46" height="46" style="flex:none"><circle cx="20" cy="20" r="17" '
            f'fill="{CORAL}" stroke="{INK}" stroke-width="3.5"/><path d="M13.5 13.5l13 13M26.5 13.5l-13 13" fill="none" '
            f'stroke="{INK}" stroke-width="4" stroke-linecap="round"/></svg>')
