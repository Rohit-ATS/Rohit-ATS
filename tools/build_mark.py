"""assets/mark-{dark,light}.svg - the 120px glyph at the top of the profile.

LexisGuide opens with a leaf that draws itself: the outline strokes on, the fill flashes
in behind it, a vein runs through, and the whole thing resets. The mark says what the
product is about before a word is read, and it does it in four seconds with two paths.

This is the same device with a different subject. A leaf is the wrong noun here; what
these projects have in common is a dependency graph - one node, the things it reaches,
and the question of what happens when you touch it. So the glyph is a small directed
graph that draws itself edge by edge, lights its nodes, and then sends one pulse from
the root out to the leaves: exactly the traversal every one of the five projects is
built around.

No <image>, no raster, no font - three paths and a stylesheet, which is why it is under
2 KB and renders identically everywhere GitHub serves it.
"""
from __future__ import annotations

# viewBox is 32x32 to match the LexisGuide flourish it sits beside in spirit; at 120px
# on the page a 32-unit grid keeps every stroke on a half-pixel.
CYCLE = 4.2          # one full draw/hold/erase, in seconds
EDGE_LEN = 46        # measured path length, for the dash offsets

NODES = [(16, 6), (7, 17), (25, 17), (11, 27), (21, 27)]
EDGES = ["M16 6 7 17", "M16 6 25 17", "M7 17 11 27", "M25 17 21 27"]

INK = {"dark": "#5CC79F", "light": "#00674F"}
PULSE = {"dark": "#FFFDF5", "light": "#FFFDF5"}
HALO = {"dark": "#2F8A5E", "light": "#2F8A5E"}


def build(theme: str) -> str:
    ink, pulse, halo = INK[theme], PULSE[theme], HALO[theme]

    css = f"""
    .e {{ stroke-dasharray: {EDGE_LEN}; stroke-dashoffset: {EDGE_LEN};
         animation: draw {CYCLE}s ease-in-out infinite; }}
    .n {{ opacity: 0; animation: pop {CYCLE}s ease-in-out infinite; }}
    .p {{ opacity: 0; animation: pulse {CYCLE}s ease-in-out infinite; }}
    @keyframes draw {{
      0%   {{ stroke-dashoffset: {EDGE_LEN}; }}
      38%  {{ stroke-dashoffset: 0; }}
      86%  {{ stroke-dashoffset: 0; }}
      100% {{ stroke-dashoffset: {EDGE_LEN}; }}
    }}
    @keyframes pop {{
      0%, 22% {{ opacity: 0; transform: scale(0.4); }}
      44%     {{ opacity: 1; transform: scale(1); }}
      86%     {{ opacity: 1; transform: scale(1); }}
      100%    {{ opacity: 0; transform: scale(0.4); }}
    }}
    @keyframes pulse {{
      0%, 46% {{ opacity: 0; }}
      58%     {{ opacity: 1; }}
      76%     {{ opacity: 1; }}
      100%    {{ opacity: 0; }}
    }}"""

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="140" height="140"'
         f' viewBox="0 0 32 32" role="img"'
         f' aria-label="A dependency graph drawing itself: a root node, its edges, and a'
         f' pulse travelling out to the leaves">'
         f'<title>Rohit Maruri</title><style>{css}</style>']

    # Edges first so the nodes cap them cleanly. Staggered begins make it draw outward
    # from the root rather than all four at once, which is the whole point of a traversal.
    for i, d in enumerate(EDGES):
        delay = 0.10 * (0 if i < 2 else 1)
        o.append(f'<path class="e" d="{d}" fill="none" stroke="{ink}" stroke-width="1.4"'
                 f' stroke-linecap="round" style="animation-delay:{delay}s"/>')

    for i, (x, y) in enumerate(NODES):
        r = 3.1 if i == 0 else 2.2
        delay = 0.0 if i == 0 else (0.12 if i < 3 else 0.24)
        o.append(f'<circle class="n" cx="{x}" cy="{y}" r="{r}" fill="{ink}"'
                 f' style="animation-delay:{delay}s;transform-origin:{x}px {y}px"/>')

    # The pulse: a ring leaving the root and a bright dot arriving at each leaf. This is
    # the beat that makes it read as a system rather than as a logo.
    o.append(f'<circle class="p" cx="16" cy="6" r="5.6" fill="none" stroke="{halo}"'
             f' stroke-width="0.9" opacity="0"/>')
    for i, (x, y) in enumerate(NODES[3:]):
        o.append(f'<circle class="p" cx="{x}" cy="{y}" r="1.1" fill="{pulse}"'
                 f' style="animation-delay:{0.08 * i:.2f}s"/>')

    o.append("</svg>")
    return "".join(o)


def main() -> None:
    for theme in ("dark", "light"):
        s = build(theme)
        p = f"../assets/mark-{theme}.svg"
        open(p, "w", encoding="utf-8").write(s)
        print(f"{p}: {len(s.encode()) / 1024:5.2f} KB")


if __name__ == "__main__":
    main()
