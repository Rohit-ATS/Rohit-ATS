"""assets/arcade-{dark,light}.svg - a Space Invaders divider.

Pixel art in the same idiom as the banner portrait: every sprite is a grid of 1x1 cells
merged into horizontal path runs with shape-rendering="crispEdges", never a font glyph.

Two things keep it from reading as clip art. The march is stepped rather than eased -
Space Invaders moved on a fixed tick, and that stutter is the whole character of it -
and the sprites carry a bloom, so they sit inside the panel's light rather than on top
of it.
"""
from __future__ import annotations

import design as D
import fonts
from design import SIZE, T

W, H = 1180, 232
CELL = 5
LOOP = 8.0

INVADER_A = [
    "..#.....#..",
    "...#...#...",
    "..#######..",
    ".##.###.##.",
    "###########",
    "#.#######.#",
    "#.#.....#.#",
    "...##.##...",
]
INVADER_B = [
    "..#.....#..",
    "#..#...#..#",
    "#.#######.#",
    "###.###.###",
    "###########",
    ".#########.",
    "..#.....#..",
    ".#.......#.",
]
SHIP = [
    "......#......",
    ".....###.....",
    ".....###.....",
    ".############",
    "#############",
    "#############",
    "#############",
    "#.##.....##.#",
]


def sprite_path(rows: list[str], cell: int = CELL) -> str:
    """Merge each row's runs of '#' into one rect, exactly like the portrait dither."""
    out, cx, cy = [], 0, 0
    first = True
    for y, row in enumerate(rows):
        x = 0
        while x < len(row):
            if row[x] == "#":
                n = 0
                while x + n < len(row) and row[x + n] == "#":
                    n += 1
                px, py = x * cell, y * cell
                out.append(f"M{px} {py}" if first else f"m{px - cx} {py - cy}")
                out.append(f"h{n * cell}v{cell}h-{n * cell}z")
                cx, cy, first = px, py, False
                x += n
            else:
                x += 1
    return "".join(out)


def build(theme: str) -> str:
    c = D.THEMES[theme]
    css, _ = fonts.embed_faces(fonts.charset(
        "ARCADEhackathons / video games / historyINSERT COIN"))

    o = [D.svg_open(W, H, "Space Invaders",
                    "A pixel-art Space Invaders divider: two ranks of invaders marching "
                    "on a fixed tick above a ship, with bombs falling.", css),
         f'<defs><path id="invA" d="{sprite_path(INVADER_A)}"/>'
         f'<path id="invB" d="{sprite_path(INVADER_B)}"/></defs>',
         D.defs(c, glow_colour=c["cyan"]), D.page(W, H, c)]

    o.append(D.eyebrow(44, 40, "ARCADE", c, colour=c["green"]))
    o.append(T(W - 44, 40, "hackathons / video games / history", size=SIZE["micro"],
               fill=c["text3"], anchor="end"))
    o.append(D.rule(44, 56, W - 88, c))

    # ---- starfield. Deterministic LCG so the file is byte-stable between runs.
    seed = 1
    for i in range(58):
        seed = (1103515245 * seed + 12345) % (1 << 31)
        sx = 56 + (seed >> 7) % (W - 112)
        seed = (1103515245 * seed + 12345) % (1 << 31)
        sy = 70 + (seed >> 7) % (H - 100)
        o.append(f'<rect x="{sx}" y="{sy}" width="1.7" height="1.7" fill="{c["text3"]}"'
                 f' opacity="0.4"><animate attributeName="opacity"'
                 f' values="0.1;0.55;0.1" dur="{2.0 + (i % 7) * 0.4:.1f}s"'
                 f' repeatCount="indefinite"/></rect>')

    iw = len(INVADER_A[0]) * CELL
    gap, cols = 78, 7
    x_start = (W - (cols * (iw + gap) - gap)) / 2

    steps = [f"{v} 0" for v in (0, 10, 20, 30, 40, 30, 20, 10, 0)]
    kt = ";".join(f"{i / (len(steps) - 1):.4f}" for i in range(len(steps)))
    march = (f'<animateTransform attributeName="transform" type="translate"'
             f' values="{";".join(steps)}" keyTimes="{kt}" calcMode="discrete"'
             f' dur="{LOOP}s" repeatCount="indefinite"/>')

    for ref, colour, y in (("invA", c["green"], 74), ("invB", c["cyan"], 118)):
        body = "".join(f'<use href="#{ref}" x="{x_start + i * (iw + gap):.0f}" y="{y}"/>'
                       for i in range(cols))
        o.append(f'<g fill="{colour}" shape-rendering="crispEdges" filter="url(#fBloom)"'
                 f' opacity="0.95">{march}{body}</g>')

    # ---- ship. Travel stops well short of the right edge: at full width it drives
    # straight through the caption.
    sw = len(SHIP[0]) * CELL
    ship_y = H - 54
    o.append(f'<g fill="{c["violet"]}" shape-rendering="crispEdges" filter="url(#fBloom)">'
             f'<animateTransform attributeName="transform" type="translate"'
             f' values="0 0;{W - sw - 360:.0f} 0;0 0" keyTimes="0;0.5;1"'
             f' calcMode="spline" keySplines="{D.EASE};{D.EASE}"'
             f' dur="{LOOP * 2:.1f}s" repeatCount="indefinite"/>'
             f'<path transform="translate(80 {ship_y})" d="{sprite_path(SHIP)}"/></g>')

    # ---- bombs fall from the ranks rather than rising from the ship: a fixed-x shot
    # leaving a ship that is sweeping past reads as a bug, not as gunfire.
    for i, delay in enumerate((0.0, 1.4, 2.9, 4.3, 5.8)):
        x = x_start + 24 + i * (iw + gap) * 1.35
        if x > W - 150:
            continue
        o.append(f'<rect x="{x:.0f}" y="166" width="{CELL - 2}" height="{CELL * 3}"'
                 f' rx="1" fill="{c["amber"]}" opacity="0">'
                 f'<animate attributeName="y" values="166;{ship_y + 16}" dur="1.2s"'
                 f' begin="{delay}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;1;1;0" dur="1.2s"'
                 f' begin="{delay}s" repeatCount="indefinite"/></rect>')

    o.append(T(W - 44, H - 22, "INSERT COIN", size=SIZE["micro"], mono=True,
               fill=c["text3"], anchor="end", opacity=0.8))
    o.append("</svg>")
    return "".join(o)


def main() -> None:
    for theme in ("dark", "light"):
        s = build(theme)
        p = f"../assets/arcade-{theme}.svg"
        open(p, "w", encoding="utf-8").write(s)
        print(f"{p}: {len(s.encode()) / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
