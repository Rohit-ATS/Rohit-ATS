"""Emit assets/banner-dark.svg and assets/banner-light.svg.

Reads the .npy grids produced by portrait_pipeline.py. Nothing in the SVG is
hand-written - leader dots, text widths and row positions are all computed here, so
editing the SVG by hand will be overwritten on the next run. Edit this file instead.

Layer model inside the portrait frame:

  intro   a full copy of the portrait, split into 60 randomly interleaved groups that
          fade in over ~2s. Random assignment is what makes dots appear everywhere at
          once and thicken together, rather than revealing patch by patch.
  loop    a second full copy, split into 94 spatial drift bands. On each cycle a band
          slides ~42% of the way toward the mark's centroid and fades out, then returns.
  trav    ~1800 dots matched portrait -> mark by optimal transport, so each takes the
          shortest available path. Hidden during the portrait phase: their dots are
          thicker than the dither and would otherwise crowd it.

The two portrait copies cannot be merged. The intro needs a random partition and the
loop needs a spatial one, and a group can only carry one animation.
"""
from __future__ import annotations

import math
import numpy as np
from scipy.optimize import linear_sum_assignment

W, H = 1180, 610
TITLEBAR = 38
LEFT_X, LEFT_W = 20, 433
RIGHT_X, RIGHT_W = 477, 683
PANEL_TOP, PANEL_BOT = 56, 590

CELL = 1.34
PORT_X, PORT_Y = 36.0, 108.0
GRID_W, GRID_H = 300, 340

INTRO_GROUPS = 60
INTRO_FADE = 0.55
INTRO_SPREAD = 2.0
INTRO_END = 3.2

BANDS = 94
DRIFT = 0.42
DRIFT_NOISE = 4.0
N_TRAV = 1800
TRAV_SIZE = 2

HOLD_PORTRAIT, TRANS, HOLD_LOGO = 3.0, 1.3, 2.0
LOOP = HOLD_PORTRAIT + TRANS + HOLD_LOGO + TRANS          # 7.6s
# Explicit uneven keyTimes. Evenly spaced keyframes would force the portrait hold, the
# transition and the logo hold to occupy the same slice of the cycle.
KT = [0.0,
      HOLD_PORTRAIT / LOOP,
      (HOLD_PORTRAIT + TRANS) / LOOP,
      (HOLD_PORTRAIT + TRANS + HOLD_LOGO) / LOOP,
      1.0]
KTS = ";".join(f"{k:.5f}" for k in KT)

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "dark": dict(
        bg="#0A101F", panel="#0D1526", panel2="#0B1220",
        chrome="#22D3EE", chrome_dim="#1B4A5C", rule="#16304A",
        portrait="#A78BFA", mark="#10B981", accent="#10B981",
        label="#5FBBD0", value="#C7D2E4", leader="#1E3A4C",
        title="#7C93AD", live="#FF5F56", pill_bg="#132033", pill_tx="#22D3EE",
    ),
    "light": dict(
        bg="#EEF2F8", panel="#FFFFFF", panel2="#F7F9FC",
        chrome="#0891B2", chrome_dim="#A9CFDC", rule="#DCE5EF",
        portrait="#7C3AED", mark="#059669", accent="#059669",
        label="#0E7490", value="#1E293B", leader="#C3D0DE",
        title="#64748B", live="#E11D48", pill_bg="#E6F6FA", pill_tx="#0E7490",
    ),
}

ROWS = [
    ("Subject",        "Rohit Maruri"),
    ("Role",           "Developer Infrastructure"),
    ("Origin",         "San Francisco Bay Area, CA"),
    ("Education",      "B.S. Computer Science, SFBU"),
    ("Status",         "Building / Shipping / Learning"),
    ("ToolChain",      "VS Code, Git, Docker, Figma, Vercel"),
    None,
    ("Core.Lang",      "Python, TypeScript, SQL / Cypher, C++"),
    ("Core.Frontend",  "React 19, Next.js 16, Tailwind v4, Electron"),
    ("Core.Backend",   "FastAPI, Node, Prisma"),
    ("Core.Database",  "HydraDB, Postgres + pgvector, SQLite"),
    ("Core.Infra",     "Docker, Vercel, Render, GitHub Actions"),
    None,
    ("Grid.Mail",      "rohitmaruriats@gmail.com"),
    ("Grid.Portfolio", "coming soon"),
    ("Grid.LinkedIn",  "in/rohitmaruri"),
    ("Grid.GitHub",    "Rohit-ATS"),
]

# Rows whose value would be a guess are held here instead of shipped: a wrong handle on
# a public profile is worse than a missing row. Currently empty - LinkedIn came from
# GET /users/Rohit-ATS/social_accounts, which returned in/rohitmaruri. The guess it
# replaced was "rohit-maruri", so the hold was doing real work.
PENDING: dict[str, str] = {}
UNVERIFIED: dict[str, str] = {}

ROW_SIZE, HDR_SIZE, LIVE_SIZE, PILL_SIZE = 14, 13, 12, 14
ROW_STEP = 23
ROWS_TOP = 152


def ch(size: float) -> float:
    """Advance width of one monospace cell. Every string is locked with textLength, so
    this only has to be self-consistent - it does not have to match the browser's font."""
    return size * 0.6


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def text(x, y, s, size, fill, *, anchor="start", weight=None, opacity=None, extra="") -> str:
    tl = len(s) * ch(size)
    bits = [f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}"',
            f'font-family="{MONO}" fill="{fill}"',
            f'textLength="{tl:.1f}" lengthAdjust="spacingAndGlyphs"']
    if anchor != "start":
        bits.append(f'text-anchor="{anchor}"')
    if weight:
        bits.append(f'font-weight="{weight}"')
    if opacity is not None:
        bits.append(f'opacity="{opacity}"')
    if extra:
        bits.append(extra)
    return " ".join(bits) + f">{esc(s)}</text>"


# ---------------------------------------------------------------- dot geometry

def runs(pts: np.ndarray) -> list[tuple[int, int, int]]:
    """Merge horizontally adjacent cells into (x, y, length) runs."""
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


def path_d(rs: list[tuple[int, int, int]]) -> str:
    """Relative-move subpath chain. Absolute moves cost ~40% more bytes at this count."""
    parts, cx, cy = [], 0, 0
    for i, (x, y, n) in enumerate(rs):
        parts.append(f"M{x} {y}" if i == 0 else f"m{x - cx} {y - cy}")
        parts.append(f"h{n}v1h-{n}z")
        cx, cy = x, y
    return "".join(parts)


def sample_n(mask: np.ndarray, n: int, seed: int) -> np.ndarray:
    """n points spread evenly over `mask` via a jittered lattice, then trimmed/topped up
    at random. Uniform random sampling alone leaves visible clumps and holes."""
    ys, xs = np.nonzero(mask)
    pts = np.stack([xs, ys], 1).astype(np.float64)
    rng = np.random.default_rng(seed)
    step = max(1.0, math.sqrt(len(pts) / n))
    keys = np.floor(pts / step).astype(np.int64)
    buckets: dict[tuple[int, int], list[int]] = {}
    for i, k in enumerate(map(tuple, keys)):
        buckets.setdefault(k, []).append(i)
    idx = [int(rng.choice(v)) for v in buckets.values()]
    if len(idx) > n:
        idx = list(rng.choice(idx, n, replace=False))
    elif len(idx) < n:
        rest = np.setdiff1d(np.arange(len(pts)), np.array(idx, dtype=int))
        idx += list(rng.choice(rest, n - len(idx), replace=False))
    return pts[np.array(idx, dtype=int)]


def drift_bands(pts: np.ndarray, target: np.ndarray, seed: int):
    """Assign every portrait dot to one of BANDS drift groups.

    The trap: drift is an affine function of position, so quantising it directly
    reproduces a square lattice and the dissolve reads as blocks. Per-dot noise is added
    before grouping to break that. verify.py measures whether it worked."""
    rng = np.random.default_rng(seed)
    c = target.mean(axis=0)
    d = DRIFT * (c - pts) + rng.normal(0, DRIFT_NOISE, pts.shape)
    d0 = d - d.mean(0)
    _, _, vt = np.linalg.svd(d0, full_matrices=False)
    t = d0 @ vt[0]
    edges = np.quantile(t, np.linspace(0, 1, BANDS + 1)[1:-1])
    band = np.searchsorted(edges, t)
    return band, d


# ---------------------------------------------------------------- svg pieces

def portrait_layers(dots: np.ndarray, logo: np.ndarray, c: dict) -> str:
    ys, xs = np.nonzero(dots)
    pts = np.stack([xs, ys], 1)
    rng = np.random.default_rng(20260824)

    # -- intro: 60 randomly interleaved groups -------------------------------
    perm = rng.permutation(len(pts))
    gid = np.empty(len(pts), dtype=int)
    gid[perm] = np.arange(len(pts)) % INTRO_GROUPS
    order = rng.permutation(INTRO_GROUPS)          # fade order, not spatial order

    intro = [f'<g id="intro" fill="{c["portrait"]}" shape-rendering="crispEdges">']
    for slot, g in enumerate(order):
        begin = slot / max(INTRO_GROUPS - 1, 1) * (INTRO_SPREAD - INTRO_FADE)
        d = path_d(runs(pts[gid == g]))
        intro.append(
            f'<path opacity="0" d="{d}">'
            f'<animate attributeName="opacity" values="0;1" begin="{begin:.3f}s"'
            f' dur="{INTRO_FADE}s" fill="freeze"/></path>')
    intro.append(
        f'<animate attributeName="opacity" values="1;0" begin="{INTRO_END}s"'
        f' dur="0.01s" fill="freeze"/></g>')

    # -- loop: 94 spatial drift bands ----------------------------------------
    ly, lx = np.nonzero(logo)
    logo_pts = np.stack([lx, ly], 1).astype(np.float64)
    band, drift = drift_bands(pts.astype(np.float64), logo_pts, seed=99)

    loop = [f'<g id="loop" opacity="0" fill="{c["portrait"]}" shape-rendering="crispEdges">'
            f'<animate attributeName="opacity" values="0;1" begin="{INTRO_END}s"'
            f' dur="0.01s" fill="freeze"/>']
    for b in range(BANDS):
        sel = band == b
        if not sel.any():
            continue
        dx, dy = drift[sel].mean(axis=0)
        d = path_d(runs(pts[sel]))
        loop.append(
            f'<g><path d="{d}"/>'
            f'<animateTransform attributeName="transform" type="translate"'
            f' values="0 0;0 0;{dx:.1f} {dy:.1f};{dx:.1f} {dy:.1f};0 0"'
            f' keyTimes="{KTS}" dur="{LOOP}s" begin="{INTRO_END}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="1;1;0;0;1"'
            f' keyTimes="{KTS}" dur="{LOOP}s" begin="{INTRO_END}s" repeatCount="indefinite"/>'
            f'</g>')
    loop.append("</g>")

    # -- travellers: optimal-transport matched portrait -> mark --------------
    src = sample_n(dots, N_TRAV, seed=5)
    dst = sample_n(logo, N_TRAV, seed=6)
    cost = ((src[:, None, :] - dst[None, :, :]) ** 2).sum(-1)
    ri, ci = linear_sum_assignment(cost)
    src, dst = src[ri], dst[ci]

    trav = [f'<g id="trav" opacity="0" fill="{c["mark"]}" shape-rendering="crispEdges">'
            f'<animate attributeName="opacity" values="0;0;1;1;0;0"'
            f' keyTimes="0;0.42000;0.55000;0.80000;0.95000;1" dur="{LOOP}s"'
            f' begin="{INTRO_END}s" repeatCount="indefinite"/>']
    s = TRAV_SIZE
    for (sx, sy), (tx, ty) in zip(src, dst):
        dx, dy = tx - sx, ty - sy
        trav.append(
            f'<path d="M{sx:.0f} {sy:.0f}h{s}v{s}h-{s}z">'
            f'<animateTransform attributeName="transform" type="translate"'
            f' values="0 0;0 0;{dx:.0f} {dy:.0f};{dx:.0f} {dy:.0f};0 0"'
            f' keyTimes="{KTS}" dur="{LOOP}s" begin="{INTRO_END}s" repeatCount="indefinite"/>'
            f'</path>')
    trav.append("</g>")

    inner = "".join(intro) + "".join(loop) + "".join(trav)
    return (f'<g transform="translate({PORT_X} {PORT_Y}) scale({CELL})">{inner}</g>',
            band, drift, gid)


def info_panel(c: dict) -> str:
    out = []
    out.append(text(RIGHT_X, PANEL_TOP + 22, "SYSTEM.INFO", HDR_SIZE, c["chrome"], weight="bold"))

    # LIVE badge, right-aligned, with the pulse on the dot
    lx = RIGHT_X + RIGHT_W
    out.append(text(lx, PANEL_TOP + 22, "LIVE", LIVE_SIZE, c["live"], anchor="end", weight="bold"))
    out.append(
        f'<circle cx="{lx - 4 * ch(LIVE_SIZE) - 9:.1f}" cy="{PANEL_TOP + 18:.1f}" r="3.4"'
        f' fill="{c["live"]}"><animate attributeName="opacity"'
        f' values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/></circle>')

    # handle pill
    handle = "@Rohit-ATS"
    pw = len(handle) * ch(PILL_SIZE) + 26
    out.append(f'<rect x="{RIGHT_X}" y="{PANEL_TOP + 38}" width="{pw:.1f}" height="28" rx="14"'
               f' fill="{c["pill_bg"]}" stroke="{c["chrome_dim"]}"/>')
    out.append(text(RIGHT_X + 13, PANEL_TOP + 57, handle, PILL_SIZE, c["pill_tx"], weight="bold"))

    y = ROWS_TOP
    for row in ROWS:
        if row is None:
            y += 4
            out.append(f'<rect x="{RIGHT_X}" y="{y - 14:.1f}" width="{RIGHT_W}" height="1"'
                       f' fill="{c["rule"]}"/>')
            y += 14
            continue
        label, value = row
        lw, vw = len(label) * ch(ROW_SIZE), len(value) * ch(ROW_SIZE)
        out.append(text(RIGHT_X, y, label, ROW_SIZE, c["label"]))
        out.append(text(RIGHT_X + RIGHT_W - vw, y, value, ROW_SIZE, c["value"]))

        # dotted leader, computed from the two locked text widths
        g0 = RIGHT_X + lw + 9
        g1 = RIGHT_X + RIGHT_W - vw - 9
        n = int((g1 - g0) // 6)
        if n > 0:
            step = (g1 - g0) / n if n else 0
            d = "".join(f'M{g0 + i * step:.1f} {y - 4:.1f}h1.6' for i in range(n))
            out.append(f'<path d="{d}" stroke="{c["leader"]}" stroke-width="1.6"'
                       f' stroke-linecap="butt" fill="none"/>')
        y += ROW_STEP

    # density legend
    ry = PANEL_BOT - 50
    out.append(f'<rect x="{RIGHT_X}" y="{ry}" width="{RIGHT_W}" height="1" fill="{c["rule"]}"/>')
    out.append(text(RIGHT_X, ry + 22, "DOT.DENSITY", 11, c["label"]))
    out.append(text(RIGHT_X + RIGHT_W - 7 * 16 - 8 - 4 * ch(10), ry + 22, "less", 10, c["title"]))
    for i in range(7):
        op = 0.16 + i * 0.14
        out.append(f'<rect x="{RIGHT_X + RIGHT_W - 7 * 16 + i * 16:.1f}" y="{ry + 12}"'
                   f' width="11" height="11" rx="2" fill="{c["portrait"]}" opacity="{op:.2f}"/>')
    return "".join(out)


def build(theme: str) -> tuple[str, dict]:
    c = THEMES[theme]
    dots = np.load(f"portrait_{theme}.npy")
    logo = np.load("logo_rm.npy")

    port_svg, band, drift, gid = portrait_layers(dots, logo, c)

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}"'
         f' height="{H}" role="img" aria-label="Rohit Maruri - developer infrastructure">',
         f'<title>Rohit Maruri</title>',
         f'<desc>Terminal panel. Left: a dithered portrait that dissolves into an RM '
         f'monogram and back. Right: role, stack and contact readout.</desc>']

    o.append(f'<rect width="{W}" height="{H}" rx="11" fill="{c["bg"]}"/>')
    o.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10.5" fill="none"'
             f' stroke="{c["chrome_dim"]}"/>')

    # title bar
    o.append(f'<path d="M0 11a11 11 0 0 1 11-11h{W - 22}a11 11 0 0 1 11 11v{TITLEBAR - 11}H0z"'
             f' fill="{c["panel2"]}"/>')
    o.append(f'<rect y="{TITLEBAR}" width="{W}" height="1" fill="{c["rule"]}"/>')
    for i, col in enumerate(("#FF5F56", "#FFBD2E", "#27C93F")):
        o.append(f'<circle cx="{24 + i * 20}" cy="{TITLEBAR / 2:.0f}" r="6" fill="{col}"/>')
    o.append(text(W / 2, TITLEBAR / 2 + 4.5, "profile.sh --live", HDR_SIZE, c["title"],
                  anchor="middle"))

    # left panel
    o.append(f'<rect x="{LEFT_X}" y="{PANEL_TOP}" width="{LEFT_W}" height="{PANEL_BOT - PANEL_TOP}"'
             f' rx="7" fill="{c["panel"]}" stroke="{c["chrome_dim"]}"/>')
    o.append(text(LEFT_X + 15, PANEL_TOP + 22, "VISUAL.MAP", 11, c["chrome"], weight="bold"))
    o.append(f'<rect x="{LEFT_X + 15}" y="{PANEL_TOP + 32}" width="{LEFT_W - 30}" height="1"'
             f' fill="{c["rule"]}"/>')
    o.append(port_svg)
    o.append(text(LEFT_X + 15, PANEL_BOT - 14, "300x340 / floyd-steinberg / 1-bit", 10,
                  c["title"], opacity=0.85))

    o.append(info_panel(c))
    o.append("</svg>")

    svg = "".join(o)
    stats = dict(dots=int(dots.sum()), bands=int(len(set(band.tolist()))),
                 intro_groups=int(len(set(gid.tolist()))), travellers=N_TRAV,
                 bytes=len(svg.encode()))
    np.save(f"_band_{theme}.npy", band)
    np.save(f"_gid_{theme}.npy", gid)
    return svg, stats


def main() -> None:
    import os
    os.makedirs("../assets", exist_ok=True)
    for theme in ("dark", "light"):
        svg, st = build(theme)
        path = f"../assets/banner-{theme}.svg"
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"{path}: {st['bytes'] / 1024:8.1f} KB  dots={st['dots']} "
              f"bands={st['bands']} intro={st['intro_groups']} trav={st['travellers']}")

    if UNVERIFIED:
        print("\n  !! DO NOT PUSH - unverified values still in the panel:")
        for k, why in UNVERIFIED.items():
            print(f"     {k} = {dict(r for r in ROWS if r)[k]!r}  ({why})")
    else:
        print(f"\n  {sum(1 for r in ROWS if r)} rows, all values confirmed - safe to push")
    for k, why in PENDING.items():
        print(f"  held back: {k} - {why}")


if __name__ == "__main__":
    main()
