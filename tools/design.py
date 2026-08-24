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
# Real jumps. Adjacent sizes 1-2px apart read as a mistake; these read as hierarchy.
SIZE = dict(micro=9.5, tiny=11, small=12.5, body=14.5, lead=17, sub=24,
            head=34, hero=52, mega=104)

THEMES = {
    "dark": dict(
        bg="#04070E", bg2="#070C16", surf="#0B1220", surf2="#101A2C",
        line="#1B2942", hair="#FFFFFF", hair_op=0.07,
        text="#F4F7FD", text2="#98AAC6", text3="#55688A",
        violet="#B79CFF", violet2="#8B6BF5", cyan="#43D2FF", cyan2="#0EA5E9",
        amber="#FFC53D", rose="#FF7A8A", green="#3DDC97",
        shadow="#000000", shadow_op=0.6, grain_op=0.04,
    ),
    "light": dict(
        bg="#F4F7FC", bg2="#FFFFFF", surf="#FFFFFF", surf2="#F2F6FB",
        line="#D9E3F0", hair="#FFFFFF", hair_op=0.9,
        text="#060B14", text2="#42536B", text3="#8294AD",
        violet="#5B2FD6", violet2="#7C4DEF", cyan="#0284C7", cyan2="#0369A1",
        amber="#A35A00", rose="#D6103C", green="#03875E",
        shadow="#0F172A", shadow_op=0.12, grain_op=0.02,
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
         f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
         f'<pattern id="pDot" width="9" height="9" patternUnits="userSpaceOnUse">'
         f'<circle cx="4.5" cy="4.5" r="0.9" fill="{c["text2"]}"/></pattern>']
    if grain:
        # Film grain. Flat digital gradients band visibly on wide panels; a trace of
        # noise breaks the banding and is most of what separates "rendered" from "shot".
        o.append('<filter id="fGrain" x="0" y="0" width="100%" height="100%">'
                 '<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3"'
                 ' stitchTiles="stitch" result="n"/>'
                 '<feColorMatrix in="n" type="saturate" values="0"/></filter>')
    o.append('</defs>')
    return "".join(o)


def page(W: int, H: int, c: dict, *, radius=18, grain=True, dots=True) -> str:
    """Page ground: gradient, a faint dot field, grain, then the border.

    The dot field is the thing that ties the panels to the portrait. Every panel is
    then literally made of the same marks, which is what stops the page reading as a
    dashboard sitting next to a piece of art."""
    o = [f'<rect width="{W}" height="{H}" rx="{radius}" fill="url(#gPage)"/>']
    if dots:
        o.append(f'<rect width="{W}" height="{H}" rx="{radius}" fill="url(#pDot)"'
                 f' opacity="0.05"/>')
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


# ===================================================================== halftone
# The portrait is a dot field. Everything else was vector cards and pills, which is two
# unrelated aesthetics on one page and the main reason the first passes read as a
# template. These primitives push the dot back out into the rest of the layout so the
# whole profile is made of one material.

def dotgrid(W: int, H: int, c: dict, *, pitch: int = 9, r: float = 0.9,
            opacity: float = 0.05, radius: int = 18) -> str:
    """A faint field of dots behind everything, as a <pattern>.

    Costs one tile no matter how large the panel, and gives flat backgrounds a texture
    to sit on. Without it a wide dark rectangle is visibly just a rectangle."""
    return (f'<pattern id="pDot" width="{pitch}" height="{pitch}"'
            f' patternUnits="userSpaceOnUse">'
            f'<circle cx="{pitch / 2:.1f}" cy="{pitch / 2:.1f}" r="{r}"'
            f' fill="{c["text2"]}"/></pattern>'
            f'<rect width="{W}" height="{H}" rx="{radius}" fill="url(#pDot)"'
            f' opacity="{opacity}"/>')


# 5x7 cells, the classic dot-matrix set. Read as rows of bits, MSB left.
_DIGITS = {
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ",": ("00000", "00000", "00000", "00000", "00110", "00110", "01100"),
    "d": ("00001", "00001", "01101", "10011", "10001", "10011", "01101"),
}
DIGIT_W, DIGIT_H = 5, 7


def dot_number(x: float, y: float, value: str, *, pitch: float = 9.0,
               r: float = 3.3, fill: str = "#fff", gap: float = 2.0,
               dim: str | None = None) -> tuple[str, float]:
    """Draw `value` as dot-matrix glyphs. Returns (markup, width).

    Same material as the portrait, at a scale where it reads as a scoreboard rather
    than as a font. `dim` paints the unlit cells, which is what makes it look like a
    real display instead of floating dots."""
    o, cx = [], x
    for chn in value:
        rows = _DIGITS.get(chn)
        if rows is None:
            cx += pitch * 2
            continue
        for ry, row in enumerate(rows):
            for rx, bit in enumerate(row):
                px = cx + rx * pitch
                py = y + ry * pitch
                if bit == "1":
                    o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r:.1f}"'
                             f' fill="{fill}"/>')
                elif dim:
                    o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r * 0.42:.1f}"'
                             f' fill="{dim}"/>')
        cx += DIGIT_W * pitch + gap * pitch
    return "".join(o), cx - x - gap * pitch + pitch


def dot_number_width(value: str, *, pitch: float = 9.0, gap: float = 2.0) -> float:
    n = sum(1 for chn in value if chn in _DIGITS)
    return n * (DIGIT_W * pitch + gap * pitch) - gap * pitch + pitch


def dot_bar(x: float, y: float, length: float, frac: float, c: dict, *,
            pitch: float = 8.0, r: float = 2.6, fill: str = "#fff",
            begin: float = 0.0) -> str:
    """A bar drawn as a run of dots that light up left to right. A solid rounded rect
    is the generic dashboard bar; this one is made of the same stuff as the portrait."""
    n = max(int(length // pitch), 1)
    lit = int(round(n * frac))
    if frac > 0:
        lit = max(lit, 1)   # 0.7% must not render as an entirely unlit row
    o = []
    for i in range(n):
        cx = x + i * pitch
        if i < lit:
            o.append(f'<circle cx="{cx:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}"'
                     f' opacity="0"><animate attributeName="opacity" values="0;1"'
                     f' dur="0.28s" begin="{begin + i * 0.016:.3f}s" fill="freeze"/></circle>')
        else:
            o.append(f'<circle cx="{cx:.1f}" cy="{y:.1f}" r="{r * 0.45:.1f}"'
                     f' fill="{c["line"]}"/>')
    return "".join(o)


def dot_rule(x: float, y: float, length: float, c: dict, *, pitch: float = 7.0,
             r: float = 1.35, fade: bool = True) -> str:
    """A divider that dissolves toward its right end, instead of a hairline that stops."""
    n = max(int(length // pitch), 1)
    o = []
    for i in range(n):
        op = 1.0 - (i / n) ** 1.6 if fade else 1.0
        if op < 0.04:
            continue
        o.append(f'<circle cx="{x + i * pitch:.1f}" cy="{y:.1f}" r="{r}"'
                 f' fill="{c["line"]}" opacity="{op:.2f}"/>')
    return "".join(o)
