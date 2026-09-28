"""assets/typing-{dark,light}.svg - the line under the name that types itself.

LexisGuide gets this effect from readme-typing-svg.demolab.com. It looks right, and it
is the one thing on that README with a third-party host in front of it - the same class
of dependency that already cost this profile its streak card: the service recomputes per
distinct URL, a cold render can take longer than GitHub's camo proxy waits, camo 504s,
caches the failure, and the line renders as alt text for the next hour.

So it is generated here instead, into the repository GitHub is already serving. Same
effect, one less host between a visitor and the page.

The reveal is a clip rect that steps one character width at a time - calcMode="discrete"
is load-bearing. Interpolating the width smoothly slides a soft edge across the glyphs
and reads as a wipe; stepping by exactly one advance width reads as typing. Widths come
from the embedded face's own metrics, so the caret lands on the glyph edge rather than
near it.
"""
from __future__ import annotations

import design as D
import fonts
from design import SIZE, T, w

W, H = 760, 54
SIZE_PX = 21
LINES = [
    "I build infrastructure for agents that touch production.",
    "The shape of the data decides which questions you can ask.",
    "No mocked data. Measured, not claimed.",
    "Five shipped this year. Every one of them has its tests.",
]

TYPE = 1.5           # seconds spent typing a line
HOLD = 1.6           # seconds it stays complete
ERASE = 0.45         # seconds spent deleting it
SLOT = TYPE + HOLD + ERASE
LOOP = SLOT * len(LINES)


def line(i: int, text: str, c: dict) -> str:
    """One line: a clipped run of type plus a caret that sits at the clip's edge."""
    t0 = i * SLOT
    tw = w(text, size=SIZE_PX, serif=True)
    cw = tw / len(text)                       # mean advance; the clip steps by this
    x0 = (W - tw) / 2
    base = H / 2 + SIZE_PX * 0.34
    cid = f"c{i}"

    # Type forward, then delete backward. Both are discrete steps on the same shared
    # loop, so the caret cannot drift away from the text it belongs to.
    n = len(text)
    vals, kts = ["0"], ["0.0000"]
    for k in range(1, n + 1):
        vals.append(f"{k * cw:.2f}")
        kts.append(f"{(t0 + TYPE * k / n) / LOOP:.5f}")
    vals.append(f"{n * cw:.2f}")
    kts.append(f"{(t0 + TYPE + HOLD) / LOOP:.5f}")
    for k in range(n - 1, -1, -1):
        vals.append(f"{k * cw:.2f}")
        kts.append(f"{(t0 + TYPE + HOLD + ERASE * (n - k) / n) / LOOP:.5f}")
    vals.append("0")
    kts.append("1.0000")

    clip = (f'<clipPath id="{cid}"><rect x="{x0:.1f}" y="0" width="0" height="{H}">'
            f'<animate attributeName="width" values="{";".join(vals)}"'
            f' keyTimes="{";".join(kts)}" calcMode="discrete" dur="{LOOP}s"'
            f' repeatCount="indefinite"/></rect></clipPath>')

    body = (f'<g clip-path="url(#{cid})">'
            + T(x0, base, text, size=SIZE_PX, serif=True, fill=c["ink"]) + '</g>')

    # The caret rides the same value list, so it is always exactly at the end of what
    # has been typed. x is animated, not the whole group, to keep it on the pixel grid.
    caret = (f'<rect y="{base - SIZE_PX * 0.82:.1f}" width="1.6"'
             f' height="{SIZE_PX * 1.02:.1f}" fill="{c["ink2"]}" x="{x0:.1f}">'
             f'<animate attributeName="x"'
             f' values="{";".join(f"{x0 + float(v) + 2:.2f}" for v in vals)}"'
             f' keyTimes="{";".join(kts)}" calcMode="discrete" dur="{LOOP}s"'
             f' repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="1;1;0;0;1"'
             f' keyTimes="0;0.45;0.5;0.95;1" dur="1.05s" repeatCount="indefinite"/></rect>')

    # Outside its own slot the line is not merely empty - it is absent, so four
    # overlapping carets never appear at once.
    on = ";".join(["0", "0", "1", "1", "0", "0"])
    kt = ";".join(f"{v:.5f}" for v in
                  [0, t0 / LOOP, (t0 + 0.001) / LOOP,
                   (t0 + SLOT - 0.001) / LOOP, (t0 + SLOT) / LOOP, 1])
    return (f'{clip}<g opacity="0"><animate attributeName="opacity" values="{on}"'
            f' keyTimes="{kt}" dur="{LOOP}s" repeatCount="indefinite"/>'
            f'{body}{caret}</g>')


def build(theme: str) -> str:
    c = D.THEMES[theme]
    css, _ = fonts.embed_faces(fonts.charset("".join(LINES)), faces=("serif",))

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}"'
         f' height="{H}" role="img" aria-label="{D.esc(" ".join(LINES))}">'
         f'<title>{D.esc(LINES[0])}</title>'
         f'<desc>Four lines typing themselves in sequence. Typeset in {fonts.LICENSE}.'
         f'</desc>{css}']
    o += [line(i, t, c) for i, t in enumerate(LINES)]
    o.append("</svg>")
    return "".join(o)


def main() -> None:
    for theme in ("dark", "light"):
        s = build(theme)
        p = f"../assets/typing-{theme}.svg"
        open(p, "w", encoding="utf-8").write(s)
        print(f"{p}: {len(s.encode()) / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
