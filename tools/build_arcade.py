"""assets/arcade-{dark,light}.svg - a playable-looking Space Invaders divider.

Pixel art in the same idiom as the banner portrait: everything is a 1x1 cell merged into
horizontal path runs with shape-rendering="crispEdges", never a font glyph.

The march is stepped, not eased. Space Invaders moved on a fixed tick and that stutter
is the whole character of it; a smooth translate reads as a slideshow of a spaceship.
"""
from __future__ import annotations

from svgkit import THEMES, svg_open, text

W, H = 1180, 180
CELL = 4
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
    c = THEMES[theme]
    o = [svg_open(W, H, "Space Invaders",
                  "A pixel-art Space Invaders divider: two ranks of invaders marching on "
                  "a fixed tick above a ship that fires back."),
         f'<rect width="{W}" height="{H}" rx="10" fill="{c["bg"]}"/>',
         f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="9.5" fill="none"'
         f' stroke="{c["chrome_dim"]}" opacity="0.7"/>']

    # ---- starfield, deterministic so the file is stable between runs
    seed = 1
    for i in range(70):
        seed = (1103515245 * seed + 12345) % (1 << 31)
        sx = 14 + (seed >> 7) % (W - 28)
        seed = (1103515245 * seed + 12345) % (1 << 31)
        sy = 12 + (seed >> 7) % (H - 24)
        o.append(f'<rect x="{sx}" y="{sy}" width="1.6" height="1.6" fill="{c["dim"]}"'
                 f' opacity="0.5"><animate attributeName="opacity"'
                 f' values="0.12;0.6;0.12" dur="{2.0 + (i % 7) * 0.4:.1f}s"'
                 f' repeatCount="indefinite"/></rect>')

    iw = len(INVADER_A[0]) * CELL
    gap = 64
    cols = 8
    row_w = cols * (iw + gap) - gap
    x_start = (W - row_w) / 2

    # Stepped march: 8 discrete positions out, then back. Same tick for both ranks.
    steps = [f"{v} 0" for v in (0, 9, 18, 27, 36, 27, 18, 9, 0)]
    kt = ";".join(f"{i / (len(steps) - 1):.4f}" for i in range(len(steps)))
    march = (f'<animateTransform attributeName="transform" type="translate"'
             f' values="{";".join(steps)}" keyTimes="{kt}" calcMode="discrete"'
             f' dur="{LOOP}s" repeatCount="indefinite"/>')

    for rank, (rows, colour, y) in enumerate(
            ((INVADER_A, c["mark"], 30), (INVADER_B, c["chrome"], 78))):
        d = sprite_path(rows)
        body = []
        for i in range(cols):
            x = x_start + i * (iw + gap)
            # every invader shares the sprite via <use>, so the path is stored once
            body.append(f'<use href="#inv{rank}" x="{x:.0f}" y="{y}"/>')
        o.append(f'<g fill="{colour}" shape-rendering="crispEdges">{march}'
                 f'{"".join(body)}</g>')
        o.insert(1, f'<defs><path id="inv{rank}" d="{d}"/></defs>')

    # ---- ship, sweeping under the ranks
    sw = len(SHIP[0]) * CELL
    ship_y = H - 44
    o.append(f'<g fill="{c["violet"]}" shape-rendering="crispEdges">'
             f'<animateTransform attributeName="transform" type="translate"'
             f' values="0 0;{W - sw - 120:.0f} 0;0 0" keyTimes="0;0.5;1"'
             f' dur="{LOOP * 2:.1f}s" repeatCount="indefinite"/>'
             f'<path transform="translate(60 {ship_y})" d="{sprite_path(SHIP)}"/></g>')

    # ---- bombs. They fall from the ranks rather than rising from the ship: the x
    # positions are fixed, and a fixed-x shot leaving a ship that is sweeping past
    # reads as a bug rather than as gunfire.
    for i, delay in enumerate((0.0, 1.3, 2.9, 4.1, 5.7, 6.6)):
        x = x_start + 26 + i * (iw + gap) * 1.3
        if x > W - 40:
            continue
        o.append(f'<rect x="{x:.0f}" y="112" width="{CELL}" height="{CELL * 4}"'
                 f' fill="{c["warn"]}" opacity="0">'
                 f'<animate attributeName="y" values="112;{ship_y + 20}" dur="1.15s"'
                 f' begin="{delay}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;1;1;0" dur="1.15s"'
                 f' begin="{delay}s" repeatCount="indefinite"/></rect>')

    o.append(text(20, H - 12, "INSERT COIN", 10, c["title"], opacity=0.75))
    o.append(text(W - 20, H - 12, "hackathons / video games / history", 10, c["title"],
                  anchor="end", opacity=0.75))
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
