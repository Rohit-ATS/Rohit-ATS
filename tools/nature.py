"""Landscape drawn in the same material as everything else.

A photographic sky or a stock grass texture would fight the dot field and the dithered
portrait - two aesthetics on one page again, which is the exact mistake the last pass
was about. So the hills, the grass and the sky are built from the same marks: a crest
that dissolves upward into scattered dots, blades that are tapering columns of dots.

Everything here is seeded, so a rebuild produces byte-identical output.
"""
from __future__ import annotations

import numpy as np

from design import EASE


def _fbm(n: int, seed: int, octaves: int = 5, persistence: float = 0.5,
         freq: float = 2.0) -> np.ndarray:
    """Value noise summed over octaves, normalised to [0,1].

    The smoothstep on the interpolant is what stops a ridge looking like a sawtooth -
    linear interpolation between control points gives visible straight facets."""
    rng = np.random.default_rng(seed)
    y = np.zeros(n)
    amp, f = 1.0, freq
    for _ in range(octaves):
        k = max(int(f), 1)
        ctrl = rng.random(k + 2)
        x = np.linspace(0, k, n)
        i = np.floor(x).astype(int)
        t = x - i
        t = t * t * (3 - 2 * t)
        y += amp * (ctrl[i] * (1 - t) + ctrl[i + 1] * t)
        amp *= persistence
        f *= 2
    y -= y.min()
    return y / (y.max() or 1.0)


def ridge(x0: float, y_base: float, width: float, height: float, *, seed: int = 1,
          colour: str = "#fff", opacity: float = 1.0, band: float = 30.0,
          pitch: float = 4.0, octaves: int = 5, freq: float = 2.0) -> str:
    """A hill: solid below the crest, dissolving into scattered dots above it.

    The dissolve is the point. A hard silhouette edge reads as vector clip art; a crest
    that breaks into dots is the same 1-bit material as the portrait."""
    n = max(int(width // pitch), 2)
    prof = _fbm(n, seed, octaves=octaves, freq=freq)
    crest = y_base - prof * height

    pts = " ".join(f"{x0 + i * pitch:.1f},{crest[i]:.1f}" for i in range(n))
    o = [f'<polygon points="{x0:.1f},{y_base:.1f} {pts} '
         f'{x0 + (n - 1) * pitch:.1f},{y_base:.1f}" fill="{colour}"'
         f' opacity="{opacity:.3f}"/>']

    rng = np.random.default_rng(seed * 7919 + 13)
    rows = max(int(band // pitch), 1)
    d = []
    # Integer coordinates and a single-letter cell. At ~600 cells per ridge the
    # difference between "M123.4 45.6h2.5v2.5h-2.5z" and "M123 45h3v3h-3z" is a third
    # of the file, and at this size no one can see the half pixel.
    sq = max(int(round(pitch * 0.62)), 2)
    for i in range(n):
        for r in range(1, rows + 1):
            if rng.random() < (1.0 - r / (rows + 1)) ** 2.6:
                d.append(f'M{int(x0 + i * pitch)} {int(crest[i] - r * pitch)}'
                         f'h{sq}v{sq}h-{sq}z')
    if d:
        o.append(f'<path d="{"".join(d)}" fill="{colour}" opacity="{opacity:.3f}"'
                 f' shape-rendering="crispEdges"/>')
    return "".join(o)


def grass(x0: float, y_base: float, width: float, *, seed: int = 2, blades: int = 180,
          h_min: float = 14.0, h_max: float = 46.0, colour: str = "#fff",
          colour2: str | None = None, opacity: float = 0.9, sway_frac: float = 0.45,
          density_bias: float = 1.0, uid: str = "g") -> str:
    """Blades as tapering columns of dots, placed from a small set of templates.

    Emitting every blade's circles inline costs ~540 bytes each, so a full-width verge
    ran to 127KB on its own. Ten templates in <defs> and a <use> per blade brings that
    under 30KB with no visible loss of variety, because scale and lean already differ
    per placement.

    Only a fraction sway. Every blade moving at once looks like a screensaver, and the
    animation is most of the cost per blade.

    The sway is additive="sum" on purpose: an animateTransform without it REPLACES the
    static translate that positions the blade, which drops the whole verge to the
    origin.
    """
    rng = np.random.default_rng(seed)

    templates = []
    for tid in range(10):
        h = h_min + (tid / 9) * (h_max - h_min)
        lean = (rng.random() - 0.5) * h * 0.55
        # 2.4px spacing, not 4.6: at the wider pitch a blade reads as a
        # dotted line rather than as a blade.
        n = max(int(h / 2.4), 4)
        marks = []
        for i in range(n):
            t = i / (n - 1)
            px = (2 * (1 - t) * t) * (lean * 0.45) + (t * t) * lean
            py = -t * h
            marks.append(f'<circle cx="{px:.1f}" cy="{py:.1f}"'
                         f' r="{1.35 * (1 - t) + 0.35:.1f}"/>')
        templates.append(f'<g id="{uid}{tid}">{"".join(marks)}</g>')

    o = [f'<defs>{"".join(templates)}</defs>']
    body = []
    # Stratified placement: one blade per cell of an even lattice, jittered within its
    # cell. Uniform random over the whole width clumps and leaves bare patches, which
    # on a verge reads as a rendering fault rather than as nature.
    cell = width / blades
    for k in range(blades):
        bx = int(x0 + (k + 0.5 + (rng.random() - 0.5) * 1.5) * cell)
        tid = int(rng.random() ** 0.8 * 10) % 10
        col = colour if (colour2 is None or rng.random() < 0.62) else colour2
        use = f'<use href="#{uid}{tid}"/>'
        if rng.random() < sway_frac:
            a = 1.6 + rng.random() * 2.6
            dur = 3.4 + rng.random() * 3.0
            use += (f'<animateTransform attributeName="transform" type="rotate"'
                    f' additive="sum" values="{-a:.1f};{a:.1f};{-a:.1f}"'
                    f' dur="{dur:.1f}s" begin="{-rng.random() * dur:.1f}s"'
                    f' repeatCount="indefinite"/>')
        body.append(f'<g transform="translate({bx} {int(y_base)})" fill="{col}">'
                    f'{use}</g>')
    o.append(f'<g opacity="{opacity:.2f}">{"".join(body)}</g>')
    return "".join(o)


def aurora(x: float, y: float, width: float, height: float, c: dict, *,
           colours=None, bands: int = 3, seed: int = 5) -> str:
    """Soft drifting light. Cheap depth for a sky that would otherwise be a flat fill."""
    rng = np.random.default_rng(seed)
    cols = colours or [c["violet"], c["cyan"], c["green"]]
    o = ["<defs>"]
    for i in range(bands):
        col = cols[i % len(cols)]
        o.append(f'<radialGradient id="gAur{i}">'
                 f'<stop offset="0" stop-color="{col}" stop-opacity="0.30"/>'
                 f'<stop offset="0.6" stop-color="{col}" stop-opacity="0.08"/>'
                 f'<stop offset="1" stop-color="{col}" stop-opacity="0"/>'
                 f'</radialGradient>')
    o.append("</defs>")
    for i in range(bands):
        cx = x + width * (0.18 + 0.64 * rng.random())
        rx = width * (0.15 + 0.14 * rng.random())
        drift = 26 + rng.random() * 40
        dur = 15 + rng.random() * 12
        o.append(f'<ellipse cx="{cx:.0f}" cy="{y + height * 0.40:.0f}" rx="{rx:.0f}"'
                 f' ry="{height * 0.62:.0f}" fill="url(#gAur{i})">'
                 f'<animateTransform attributeName="transform" type="translate"'
                 f' values="0 0;{drift:.0f} -10;0 0" dur="{dur:.0f}s"'
                 f' calcMode="spline" keyTimes="0;0.5;1" keySplines="{EASE};{EASE}"'
                 f' repeatCount="indefinite"/></ellipse>')
    return "".join(o)


def moon(cx: float, cy: float, r: float, *, colour: str = "#fff") -> str:
    return (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r * 3.6:.0f}"'
            f' fill="url(#gGlow)" opacity="0.8"/>'
            f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.1f}" fill="{colour}"'
            f' opacity="0.9" filter="url(#fBloom)"/>')


def stars(x: float, y: float, width: float, height: float, *, n: int = 90,
          seed: int = 9, colour: str = "#fff") -> str:
    rng = np.random.default_rng(seed)
    o = []
    for _ in range(n):
        sx = x + rng.random() * width
        sy = y + (rng.random() ** 1.7) * height    # denser toward the top of the sky
        dur = 2.2 + rng.random() * 3.4
        o.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}"'
                 f' r="{0.6 + rng.random() * 1.1:.2f}" fill="{colour}" opacity="0.5">'
                 f'<animate attributeName="opacity" values="0.12;0.7;0.12"'
                 f' dur="{dur:.1f}s" begin="{-rng.random() * dur:.2f}s"'
                 f' repeatCount="indefinite"/></circle>')
    return "".join(o)
