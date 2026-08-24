"""Design tokens and primitives shared by every panel.

The first version of this profile failed for a reason worth writing down: five panels
all wearing the same terminal chrome, flat fills with a 1px border, one typeface, and
five accent colours competing. Each piece was fine and the page read as a template.

What this module changes:

  depth        surfaces are gradients with a hairline highlight along the top edge and a
               soft shadow beneath, not flat rectangles with a stroke. A 1px line of
               white at 6% is most of the difference between "box" and "surface".
  type         a geometric display face for names and numerals, monospace only for data.
               Widths come from the real font metrics, so nothing is stretched to fit.
  restraint    one primary accent (violet), one secondary (cyan), and a four-step
               neutral ramp. Amber and rose appear only where a value means something.
  light        a radial glow sits behind the focal element of a panel and nothing else,
               so every panel has exactly one place the eye goes first.
"""
from __future__ import annotations

import fonts

DISPLAY = "Space Grotesk"
MONO = "JetBrains Mono"

# 8pt rhythm, and a type scale with real jumps in it - adjacent sizes that differ by
# 1-2px read as a mistake rather than as hierarchy.
SP = 8
SIZE = dict(micro=10, tiny=11, small=12.5, body=14, lead=17, sub=22, head=30, hero=44, mega=62)

THEMES = {
    "dark": dict(
        bg="#070B14", bg2="#0A101E", surf="#0F1828", surf2="#142138",
        line="#1D2C46", hair="#FFFFFF", hair_op=0.06,
        text="#E8EFF9", text2="#A3B4CC", text3="#61748E",
        violet="#A78BFA", violet2="#7C5CE6", cyan="#38BDF8", cyan2="#0EA5E9",
        amber="#FBBF24", rose="#FB7185", green="#34D399",
        shadow="#000000", shadow_op=0.55, grain_op=0.035,
    ),
    "light": dict(
        bg="#F6F8FC", bg2="#FFFFFF", surf="#FFFFFF", surf2="#F4F7FB",
        line="#DEE7F2", hair="#FFFFFF", hair_op=0.9,
        text="#0B1220", text2="#48586E", text3="#8595AC",
        violet="#6D3FE0", violet2="#8B5CF6", cyan="#0284C7", cyan2="#0369A1",
        amber="#B45309", rose="#E11D48", green="#059669",
        shadow="#0F172A", shadow_op=0.10, grain_op=0.02,
    ),
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def w(s: str, *, size=SIZE["body"], weight=400, mono=False, track=0.0) -> float:
    """Rendered width in px, from the embedded face's own advance widths."""
    return fonts.width(s, MONO if mono else DISPLAY, weight, size, track)


def T(x, y, s, *, size=SIZE["body"], weight=400, mono=False, fill="#fff",
      anchor="start", track=0.0, opacity=None, extra="") -> str:
    fam = f"'{MONO}',ui-monospace,monospace" if mono else f"'{DISPLAY}',system-ui,sans-serif"
    bits = [f'<text x="{x:.1f}" y="{y:.1f}"',
            f'font-family="{fam}" font-size="{size}" font-weight="{weight}" fill="{fill}"']
    if anchor != "start":
        bits.append(f'text-anchor="{anchor}"')
    if track:
        bits.append(f'letter-spacing="{track}em"')
    if opacity is not None:
        bits.append(f'opacity="{opacity}"')
    if extra:
        bits.append(extra)
    return " ".join(bits) + f">{esc(s)}</text>"


def defs(c: dict, *, glow_colour: str | None = None, grain=True) -> str:
    """Gradients and filters every panel draws from."""
    g = glow_colour or c["violet"]
    o = ['<defs>',
         f'<linearGradient id="gSurf" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="{c["surf2"]}"/>'
         f'<stop offset="1" stop-color="{c["surf"]}"/></linearGradient>',
         f'<linearGradient id="gPage" x1="0" y1="0" x2="0.35" y2="1">'
         f'<stop offset="0" stop-color="{c["bg2"]}"/>'
         f'<stop offset="1" stop-color="{c["bg"]}"/></linearGradient>',
         f'<linearGradient id="gAccent" x1="0" y1="0" x2="1" y2="0">'
         f'<stop offset="0" stop-color="{c["violet"]}"/>'
         f'<stop offset="1" stop-color="{c["cyan"]}"/></linearGradient>',
         f'<linearGradient id="gHair" x1="0" y1="0" x2="1" y2="0">'
         f'<stop offset="0" stop-color="{c["hair"]}" stop-opacity="0"/>'
         f'<stop offset="0.5" stop-color="{c["hair"]}" stop-opacity="{c["hair_op"]}"/>'
         f'<stop offset="1" stop-color="{c["hair"]}" stop-opacity="0"/></linearGradient>',
         f'<radialGradient id="gGlow">'
         f'<stop offset="0" stop-color="{g}" stop-opacity="0.34"/>'
         f'<stop offset="0.55" stop-color="{g}" stop-opacity="0.09"/>'
         f'<stop offset="1" stop-color="{g}" stop-opacity="0"/></radialGradient>',
         f'<filter id="fSoft" x="-30%" y="-30%" width="160%" height="160%">'
         f'<feDropShadow dx="0" dy="10" stdDeviation="18" flood-color="{c["shadow"]}"'
         f' flood-opacity="{c["shadow_op"]}"/></filter>',
         f'<filter id="fBloom" x="-60%" y="-60%" width="220%" height="220%">'
         f'<feGaussianBlur stdDeviation="7" result="b"/>'
         f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>']
    if grain:
        # Film grain. Flat digital gradients band visibly on wide panels; a trace of
        # noise breaks the banding and is most of what separates "rendered" from "shot".
        o.append('<filter id="fGrain" x="0" y="0" width="100%" height="100%">'
                 '<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3"'
                 ' stitchTiles="stitch" result="n"/>'
                 '<feColorMatrix in="n" type="saturate" values="0"/></filter>')
    o.append('</defs>')
    return "".join(o)


def page(W: int, H: int, c: dict, *, radius=16, grain=True) -> str:
    o = [f'<rect width="{W}" height="{H}" rx="{radius}" fill="url(#gPage)"/>']
    if grain:
        o.append(f'<rect width="{W}" height="{H}" rx="{radius}" filter="url(#fGrain)"'
                 f' opacity="{c["grain_op"]}"/>')
    o.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="{radius - 0.5}"'
             f' fill="none" stroke="{c["line"]}"/>')
    return "".join(o)


def glow(cx: float, cy: float, r: float) -> str:
    return f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="url(#gGlow)"/>'


def card(x, y, cw, chh, c, *, radius=12, shadow=True, hairline=True, fill="url(#gSurf)") -> str:
    """A surface, not a box: vertical gradient, a shadow under it, and a hairline of
    light along the top edge where a real bevel would catch it."""
    o = []
    if shadow:
        o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw:.1f}" height="{chh:.1f}"'
                 f' rx="{radius}" fill="{c["bg"]}" filter="url(#fSoft)" opacity="0.9"/>')
    o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw:.1f}" height="{chh:.1f}"'
             f' rx="{radius}" fill="{fill}" stroke="{c["line"]}"/>')
    if hairline:
        o.append(f'<rect x="{x + radius:.1f}" y="{y + 0.5:.1f}" width="{cw - radius * 2:.1f}"'
                 f' height="1" fill="url(#gHair)"/>')
    return "".join(o)


def chip(x, y, label, c, *, size=SIZE["small"], accent=None, pad=11, height=26) -> tuple[str, float]:
    """A pill. Returns (markup, width) so callers can flow them into rows."""
    tw = w(label, size=size, mono=True, weight=400)
    cw = tw + pad * 2
    col = accent or c["text2"]
    o = (f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw:.1f}" height="{height}" rx="{height / 2:.0f}"'
         f' fill="{c["surf2"]}" stroke="{c["line"]}"/>'
         + T(x + pad, y + height / 2 + size * 0.36, label, size=size, mono=True, fill=col))
    return o, cw


def flow_chips(x, y, items, c, maxw, *, gap=7, line_h=33, accents=None) -> tuple[str, float]:
    """Lay chips left to right, wrapping at maxw. Returns (markup, height used)."""
    o, cx, cy = [], x, y
    for i, label in enumerate(items):
        acc = (accents or {}).get(label)
        m, cw = chip(cx, cy, label, c, accent=acc)
        if cx + cw > x + maxw and cx > x:
            cx, cy = x, cy + line_h
            m, cw = chip(cx, cy, label, c, accent=acc)
        o.append(m)
        cx += cw + gap
    return "".join(o), cy + line_h - y


def rule(x, y, length, c, *, opacity=1.0) -> str:
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{length:.1f}" height="1"'
            f' fill="{c["line"]}" opacity="{opacity}"/>')


def eyebrow(x, y, label, c, *, colour=None) -> str:
    """Small caps label with a short accent tick - marks a section without a heading."""
    col = colour or c["violet"]
    return (f'<rect x="{x:.1f}" y="{y - 7:.1f}" width="3" height="10" rx="1.5" fill="{col}"/>'
            + T(x + 11, y, label, size=SIZE["tiny"], weight=700, fill=c["text3"], track=0.16))


def svg_open(W: int, H: int, label: str, desc: str, font_css: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}"'
            f' height="{H}" role="img" aria-label="{esc(label)}">'
            f'<title>{esc(label)}</title>'
            f'<desc>{esc(desc)} Typeset in {fonts.LICENSE}.</desc>{font_css}')


def type_clip(cid: str, n: int, cw: float, x: float, y: float, h: float,
              loop: float, t0: float, t1: float) -> str:
    """A clip rect that widens one character at a time - a real typewriter reveal.

    calcMode="discrete" is the point. Interpolating width linearly slides a soft edge
    across the glyphs and reads as a wipe; stepping by exactly one advance width reads
    as typing.

    The animation spans the WHOLE loop rather than just the typing window, so every
    panel element shares one cycle length and they cannot drift apart. Outside
    [t0, t1] the width simply holds - full until the end, then back to zero."""
    vals, kts = ["0"], ["0"]
    for i in range(1, n + 1):
        vals.append(f"{i * cw:.1f}")
        kts.append(f"{(t0 + (t1 - t0) * i / n) / loop:.4f}")
    vals += [f"{n * cw:.1f}", "0"]
    kts += ["0.9990", "1"]
    return (f'<clipPath id="{cid}"><rect x="{x:.1f}" y="{y:.1f}" width="0" height="{h:.1f}">'
            f'<animate attributeName="width" values="{";".join(vals)}"'
            f' keyTimes="{";".join(kts)}" calcMode="discrete" dur="{loop}s"'
            f' repeatCount="indefinite"/></rect></clipPath>')


def reveal(inner: str, loop: float, t_on: float, t_off: float, fade: float = 0.22) -> str:
    """Wrap markup so it fades in at t_on and out at t_off, on the shared loop."""
    k = [0.0, t_on / loop, (t_on + fade) / loop, t_off / loop,
         min((t_off + fade) / loop, 1.0), 1.0]
    k = [min(max(v, 0.0), 1.0) for v in k]
    for i in range(1, len(k)):
        k[i] = max(k[i], k[i - 1])
    kt = ";".join(f"{v:.4f}" for v in k)
    return (f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0;0"'
            f' keyTimes="{kt}" dur="{loop}s" repeatCount="indefinite"/>{inner}</g>')


EASE = "0.22 0.61 0.36 1"     # a real ease-out; linear motion is the tell of a generated file
