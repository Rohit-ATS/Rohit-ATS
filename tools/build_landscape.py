"""assets/landscape-{dark,light}.svg - the Bay, rendered in the same dots.

A decorative band needs a reason to exist or it is filler. This one is the place the
work happens: the coordinates in the corner are San Francisco Bay, and the panel sits
in the README as the break between the engineering and the off-hours half.

Everything is the same material as the portrait - ridges that dissolve upward into
scattered cells, grass as tapering columns of dots. Dropping a photograph or a stock
gradient landscape here would put two aesthetics on one page again.

Depth comes from three things, in order of how much they do:
  atmosphere   distant ridges are lighter and lower-contrast than near ones
  haze         a warm band at the horizon, so silhouettes have something to sit against
  parallax     the far ridge drifts slower than the near one
"""
from __future__ import annotations

import design as D
import fonts
import nature as N
from design import SIZE, T

W, H = 1180, 320
HORIZON = 214
PLACE = "SAN FRANCISCO BAY"
COORDS = "37.7749° N   122.4194° W"


def build(theme: str) -> str:
    c = D.THEMES[theme]
    dark = theme == "dark"
    css, _ = fonts.embed_faces(fonts.charset(PLACE + COORDS + "°NW."))

    sky_top = "#04070E" if dark else "#EAF0F8"
    sky_haze = "#2A1D52" if dark else "#DCE6F4"
    far = c["violet"] if dark else "#9FB0CC"
    mid = "#2A2150" if dark else "#7387A8"
    near = "#0A0A16" if dark else "#48586E"
    # Light mode grows on a mid-slate ground, so the blades have to be
    # lighter than the earth rather than darker - the dark-theme greens
    # disappear into it entirely.
    blade_a = c["green"] if dark else "#93E3BC"
    blade_b = c["cyan"] if dark else "#B9DCF0"

    o = [D.svg_open(W, H, "San Francisco Bay, drawn in dots",
                    "A dithered landscape: ridge lines dissolving into scattered cells, "
                    "an aurora, and a foreground of swaying grass.", css),
         D.defs(c),
         f'<defs><linearGradient id="gSky" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="{sky_top}"/>'
         f'<stop offset="0.72" stop-color="{sky_top}"/>'
         f'<stop offset="1" stop-color="{sky_haze}"/></linearGradient>'
         f'<clipPath id="landClip"><rect width="{W}" height="{H}" rx="18"/></clipPath>'
         f'</defs>',
         f'<g clip-path="url(#landClip)">',
         f'<rect width="{W}" height="{HORIZON + 30}" fill="url(#gSky)"/>',
         f'<rect y="{HORIZON + 28}" width="{W}" height="{H - HORIZON - 28}"'
         f' fill="{near}"/>']

    # No stars in the light theme: it is a daytime sky, and specks in it read as dirt
    # on the panel rather than as a constellation.
    if dark:
        o.append(N.stars(0, 8, W, HORIZON - 70, n=80, seed=9, colour=c["text2"]))
    o.append(N.moon(946, 62, 15, colour=c["text"] if dark else "#FFF6E0"))
    o.append(N.aurora(0, 10, W, HORIZON - 40, c,
                      colours=[c["violet"], c["cyan"], c["green"]], seed=5))

    # ---- three ridges. Parallax: the far one drifts least.
    # Each mass is darker and taller than the one behind it. When the bodies sit at
    # similar lightness the middle one reads as a flat slab rather than as a hill,
    # because only its crest carries any information.
    for i, (yb, hgt, col, op, seed, drift, dur) in enumerate((
            (HORIZON - 4, 64, far, 0.24, 3, 10, 46),
            (HORIZON + 16, 62, mid, 0.82, 11, 18, 34),
            (HORIZON + 46, 50, near, 1.0, 23, 30, 26))):
        band = N.ridge(-40, yb, W + 80, hgt, seed=seed, colour=col, opacity=op,
                       band=20, pitch=4, freq=1.6 + i * 0.9)
        o.append(f'<g>{band}<animateTransform attributeName="transform"'
                 f' type="translate" values="0 0;{drift} 0;0 0" dur="{dur}s"'
                 f' calcMode="spline" keyTimes="0;0.5;1"'
                 f' keySplines="{D.EASE};{D.EASE}" repeatCount="indefinite"/></g>')

    # ---- the verge, two passes so the front row reads taller than the back
    o.append(N.grass(-30, H - 22, W + 60, blades=240, h_min=8, h_max=20,
                     colour=blade_b, opacity=0.3, sway_frac=0.22, seed=41, uid="gb"))
    o.append(N.grass(-30, H + 14, W + 60, blades=300, h_min=16, h_max=46,
                     colour=blade_a, colour2=blade_b, opacity=0.62, sway_frac=0.35,
                     seed=7, uid="gf"))
    o.append("</g>")

    # Type sits in the sky, not on the verge. Grass grows through anything placed at
    # the foot of the panel, and a caption behind blades is unreadable.
    o.append(T(44, 46, PLACE, size=SIZE["tiny"], weight=700, mono=True,
               fill=c["text2"], track=0.24))
    o.append(T(W - 44, 46, COORDS, size=SIZE["tiny"], mono=True,
               fill=c["text3"], anchor="end"))
    o.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="17.5"'
             f' fill="none" stroke="{c["line"]}"/>')
    o.append("</svg>")
    return "".join(o)


def main() -> None:
    for theme in ("dark", "light"):
        s = build(theme)
        p = f"../assets/landscape-{theme}.svg"
        open(p, "w", encoding="utf-8").write(s)
        print(f"{p}: {len(s.encode()) / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
