"""assets/banner-{dark,light}.svg - the hero.

The portrait animation is unchanged and still carries the whole idea: dots arrive
everywhere at once and thicken into a face, hold, then drift apart and reassemble as an
RM monogram. What changed is everything around it.

The first version framed it as a terminal window - traffic lights, a title bar, and
fifteen identical dotted-leader rows. That is a lot of chrome saying nothing, and a wall
of evenly weighted text has no focal point. This one is laid out like an identity card:
one large name, one accent rule, a role, and the stack as chips rather than as rows.
Hierarchy does the work the leader dots were pretending to do.

Text is set in an embedded Space Grotesk / JetBrains Mono subset and positioned from the
real advance widths, so nothing is stretched with textLength to hit a guessed width.

Layer model inside the portrait frame (unchanged, and load-bearing):

  intro   a full copy of the portrait split into 60 randomly interleaved groups that
          fade in over ~2s. Random assignment is what makes dots arrive everywhere at
          once rather than revealing the face patch by patch.
  loop    a second full copy split into 94 spatial drift bands. Each band slides ~42%
          toward the mark's centroid and fades, then returns.
  trav    ~1800 dots matched portrait -> mark by optimal transport, so each takes the
          shortest available path.

The two portrait copies cannot be merged: the intro needs a random partition and the
loop needs a spatial one, and a group can carry only one animation.
"""
from __future__ import annotations

import math
import numpy as np
from scipy.optimize import linear_sum_assignment

import design as D
import fonts
from design import SIZE, T, w

W, H = 1180, 620

# The portrait runs large and bleeds off the right edge. A face cropped by the frame
# reads as a photograph placed in a layout; a face floating inside a bordered card reads
# as a thumbnail, which is what the previous version looked like.
PORT_X, PORT_Y = 720.0, 30.0
CELL = 1.75
GRID_W, GRID_H = 300, 340

LX, LW = 64, 616                      # the type column

INTRO_GROUPS, INTRO_FADE, INTRO_SPREAD, INTRO_END = 60, 0.55, 2.0, 3.2
BANDS, DRIFT, DRIFT_NOISE = 94, 0.42, 4.0
N_TRAV, TRAV_SIZE = 1800, 2

HOLD_PORTRAIT, TRANS, HOLD_LOGO = 3.0, 1.3, 2.0
LOOP = HOLD_PORTRAIT + TRANS + HOLD_LOGO + TRANS
# Explicit uneven keyTimes. Evenly spaced keyframes force the portrait hold, the
# transition and the logo hold to occupy the same slice of the cycle.
KT = [0.0, HOLD_PORTRAIT / LOOP, (HOLD_PORTRAIT + TRANS) / LOOP,
      (HOLD_PORTRAIT + TRANS + HOLD_LOGO) / LOOP, 1.0]
KTS = ";".join(f"{k:.5f}" for k in KT)

NAME = "ROHIT MARURI"
ROLE = "Developer Infrastructure"
META = "B.S. Computer Science  ·  San Francisco Bay University"
BIO = ["I build the tool when the popular one is the wrong shape",
       "for the question."]
STATUS = "OPEN TO INTERNSHIPS"
# Set as two run-on lines of small caps rather than as pills. A row of rounded chips
# is the single most template-looking element available, and it wastes the width.
STACK = ["PYTHON · TYPESCRIPT · HYDRADB · POSTGRESQL · PGVECTOR · SQLITE · REDIS",
         "FASTAPI · REACT 19 · NEXT.JS 16 · ELECTRON · DOCKER · VERCEL · GH ACTIONS"]
REACH = "rohitmaruriats@gmail.com   ·   in/rohitmaruri   ·   github.com/Rohit-ATS"
EDGE = "PROFILE — MMXXVI"
CAPTION = "300 × 340 · floyd–steinberg · 1-bit"


# ---------------------------------------------------------------- dot geometry

def runs(pts: np.ndarray) -> list[tuple[int, int, int]]:
    if len(pts) == 0:
        return []
    order = np.lexsort((pts[:, 0], pts[:, 1]))
    p = pts[order]
    out, sx, sy, n = [], int(p[0, 0]), int(p[0, 1]), 1
    for x, y in p[1:]:
        if y == sy and x == sx + n:
            n += 1
        else:
            out.append((sx, sy, n))
            sx, sy, n = int(x), int(y), 1
    out.append((sx, sy, n))
    return out


def path_d(rs) -> str:
    parts, cx, cy = [], 0, 0
    for i, (x, y, n) in enumerate(rs):
        parts.append(f"M{x} {y}" if i == 0 else f"m{x - cx} {y - cy}")
        parts.append(f"h{n}v1h-{n}z")
        cx, cy = x, y
    return "".join(parts)


def sample_n(mask, n, seed):
    ys, xs = np.nonzero(mask)
    pts = np.stack([xs, ys], 1).astype(np.float64)
    rng = np.random.default_rng(seed)
    step = max(1.0, math.sqrt(len(pts) / n))
    buckets: dict[tuple[int, int], list[int]] = {}
    for i, k in enumerate(map(tuple, np.floor(pts / step).astype(np.int64))):
        buckets.setdefault(k, []).append(i)
    idx = [int(rng.choice(v)) for v in buckets.values()]
    if len(idx) > n:
        idx = list(rng.choice(idx, n, replace=False))
    elif len(idx) < n:
        rest = np.setdiff1d(np.arange(len(pts)), np.array(idx, dtype=int))
        idx += list(rng.choice(rest, n - len(idx), replace=False))
    return pts[np.array(idx, dtype=int)]


def drift_bands(pts, target, seed):
    """Drift is affine in position, so quantising it directly rebuilds a square lattice
    and the dissolve reads as blocks. Per-dot noise before grouping breaks that;
    verify.py measures whether it worked."""
    rng = np.random.default_rng(seed)
    d = DRIFT * (target.mean(axis=0) - pts) + rng.normal(0, DRIFT_NOISE, pts.shape)
    d0 = d - d.mean(0)
    _, _, vt = np.linalg.svd(d0, full_matrices=False)
    t = d0 @ vt[0]
    return np.searchsorted(np.quantile(t, np.linspace(0, 1, BANDS + 1)[1:-1]), t), d


def portrait_layers(dots, logo, c):
    ys, xs = np.nonzero(dots)
    pts = np.stack([xs, ys], 1)
    rng = np.random.default_rng(20260824)

    perm = rng.permutation(len(pts))
    gid = np.empty(len(pts), dtype=int)
    gid[perm] = np.arange(len(pts)) % INTRO_GROUPS
    order = rng.permutation(INTRO_GROUPS)

    intro = [f'<g id="intro" fill="{c["ink"]}" shape-rendering="crispEdges">']
    for slot, g in enumerate(order):
        begin = slot / max(INTRO_GROUPS - 1, 1) * (INTRO_SPREAD - INTRO_FADE)
        intro.append(f'<path opacity="0" d="{path_d(runs(pts[gid == g]))}">'
                     f'<animate attributeName="opacity" values="0;1" begin="{begin:.3f}s"'
                     f' dur="{INTRO_FADE}s" fill="freeze"/></path>')
    intro.append(f'<animate attributeName="opacity" values="1;0" begin="{INTRO_END}s"'
                 f' dur="0.01s" fill="freeze"/></g>')

    ly, lx = np.nonzero(logo)
    logo_pts = np.stack([lx, ly], 1).astype(np.float64)
    band, drift = drift_bands(pts.astype(np.float64), logo_pts, seed=99)

    loop = [f'<g id="loop" opacity="0" fill="{c["ink"]}" shape-rendering="crispEdges">'
            f'<animate attributeName="opacity" values="0;1" begin="{INTRO_END}s"'
            f' dur="0.01s" fill="freeze"/>']
    for b in range(BANDS):
        sel = band == b
        if not sel.any():
            continue
        dx, dy = drift[sel].mean(axis=0)
        loop.append(
            f'<g><path d="{path_d(runs(pts[sel]))}"/>'
            f'<animateTransform attributeName="transform" type="translate"'
            f' values="0 0;0 0;{dx:.1f} {dy:.1f};{dx:.1f} {dy:.1f};0 0" keyTimes="{KTS}"'
            f' dur="{LOOP}s" begin="{INTRO_END}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="{KTS}"'
            f' dur="{LOOP}s" begin="{INTRO_END}s" repeatCount="indefinite"/></g>')
    loop.append("</g>")

    src, dst = sample_n(dots, N_TRAV, 5), sample_n(logo, N_TRAV, 6)
    ri, ci = linear_sum_assignment(((src[:, None, :] - dst[None, :, :]) ** 2).sum(-1))
    src, dst = src[ri], dst[ci]

    trav = [f'<g id="trav" opacity="0" fill="{c["ink2"]}" shape-rendering="crispEdges">'
            f'<animate attributeName="opacity" values="0;0;1;1;0;0"'
            f' keyTimes="0;0.42000;0.55000;0.80000;0.95000;1" dur="{LOOP}s"'
            f' begin="{INTRO_END}s" repeatCount="indefinite"/>']
    s = TRAV_SIZE
    for (sx, sy), (tx, ty) in zip(src, dst):
        trav.append(
            f'<path d="M{sx:.0f} {sy:.0f}h{s}v{s}h-{s}z">'
            f'<animateTransform attributeName="transform" type="translate"'
            f' values="0 0;0 0;{tx - sx:.0f} {ty - sy:.0f};{tx - sx:.0f} {ty - sy:.0f};0 0"'
            f' keyTimes="{KTS}" dur="{LOOP}s" begin="{INTRO_END}s"'
            f' repeatCount="indefinite"/></path>')
    trav.append("</g>")

    inner = "".join(intro) + "".join(loop) + "".join(trav)
    return (f'<g transform="translate({PORT_X} {PORT_Y}) scale({CELL})">{inner}</g>',
            band, gid)


# ---------------------------------------------------------------------- layout

def build(theme: str) -> tuple[str, dict]:
    c = D.THEMES[theme]
    dots = np.load(f"portrait_{theme}.npy")
    logo = np.load("logo_rm.npy")

    chars = fonts.charset(NAME + ROLE + META + STATUS + CAPTION + EDGE + REACH
                          + "".join(BIO) + "".join(STACK) + "STACKVISUAL.MAP")
    css, font_bytes = fonts.embed_faces(chars)

    port, band, gid = portrait_layers(dots, logo, c)

    o = [D.svg_open(W, H, "Rohit Maruri — developer infrastructure",
                    "A dithered portrait that dissolves into an RM monogram, set beside "
                    "a name, role, stack and contact details.", css),
         D.defs(c),
         D.page(W, H, c)]

    # the panel's one light source, behind the face
    o.append(D.glow(PORT_X + GRID_W * CELL * 0.42, PORT_Y + GRID_H * CELL * 0.40, 360))

    # Portrait: clipped to the page so the bleed stays clean at the rounded corner, and
    # masked so the bottom dissolves into the background. Without the mask the shoulders
    # are simply sliced off by the frame, which reads as a crop accident rather than as
    # a bleed.
    o.append(f'<defs><clipPath id="pageClip"><rect width="{W}" height="{H}" rx="18"/>'
             f'</clipPath>'
             f'<linearGradient id="gFade" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="#fff" stop-opacity="1"/>'
             f'<stop offset="0.74" stop-color="#fff" stop-opacity="1"/>'
             f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
             f'<mask id="mFade"><rect width="{W}" height="{H}" fill="url(#gFade)"/></mask>'
             f'</defs>')
    o.append(f'<g clip-path="url(#pageClip)"><g mask="url(#mFade)">{port}</g>')

    # A verge under the portrait, so the face dissolves downward into grass rather than
    # just fading out. Same marks, so the handover is invisible. It is kept to the right
    # of x=610: grass growing through the contact line would be unreadable.
    o.append('</g>')

    # ---- edition mark, running up the far left margin
    o.append(f'<g transform="translate(30 {H - 56}) rotate(-90)">'
             + T(0, 0, EDGE, size=SIZE["micro"], weight=700, mono=True,
                 fill=c["text3"], track=0.4) + '</g>')

    # ---- availability
    o.append(f'<circle cx="{LX + 4}" cy="{68}" r="4" fill="{c["green"]}">'
             f'<animate attributeName="opacity" values="1;0.2;1" dur="2.6s"'
             f' calcMode="spline" keyTimes="0;0.5;1" keySplines="{D.EASE};{D.EASE}"'
             f' repeatCount="indefinite"/></circle>')
    o.append(T(LX + 18, 72, STATUS, size=SIZE["tiny"], weight=700, mono=True,
               fill=c["green"], track=0.22))

    # ---- the name, at a size that is actually the first thing you see
    o.append(T(LX - 4, 196, "ROHIT", size=SIZE["mega"], weight=300,
               fill=c["text"], track=-0.02))
    o.append(T(LX - 4, 290, "MARURI", size=SIZE["mega"], weight=300,
               fill=c["text"], track=-0.02))
    o.append(D.dot_rule(LX, 320, 330, c, pitch=8, r=1.7))

    o.append(T(LX, 360, ROLE.upper(), size=SIZE["body"], weight=700,
               fill=c["ink"], track=0.24))
    o.append(T(LX, 386, META, size=SIZE["small"], fill=c["text3"]))

    for i, line in enumerate(BIO):
        o.append(T(LX, 428 + i * 24, line, size=SIZE["lead"], weight=300,
                   fill=c["text2"]))

    # ---- stack, as text rather than as pills
    o.append(D.eyebrow(LX, 502, "STACK", c, colour=c["ink2"]))
    for i, line in enumerate(STACK):
        o.append(T(LX, 528 + i * 21, line, size=SIZE["tiny"], mono=True,
                   fill=c["text2"], track=0.06))

    o.append(D.dot_rule(LX, 566, LW - 40, c, pitch=8, r=1.5))
    o.append(T(LX, 592, REACH, size=SIZE["small"], mono=True, fill=c["text3"]))

    o.append("</svg>")
    svg = "".join(o)
    np.save(f"_band_{theme}.npy", band)
    np.save(f"_gid_{theme}.npy", gid)
    return svg, dict(bytes=len(svg.encode()), fonts=font_bytes, dots=int(dots.sum()),
                     bands=int(len(set(band.tolist()))), bottom=600)


def main() -> None:
    import os as _os
    _os.makedirs("../assets", exist_ok=True)
    for theme in ("dark", "light"):
        svg, st = build(theme)
        p = f"../assets/banner-{theme}.svg"
        open(p, "w", encoding="utf-8").write(svg)
        print(f"{p}: {st['bytes'] / 1024:7.1f} KB (fonts {st['fonts'] / 1024:4.1f} KB)"
              f"  dots={st['dots']} bands={st['bands']}")


if __name__ == "__main__":
    main()
