"""assets/constellation-{dark,light}.svg - the four projects as one graph.

Rohit's throughline is that the shape of the data decides which questions you are
allowed to ask, and his flagship is a graph database. So the projects are drawn as a
graph rather than as a list of cards: shared technology is a shared node, and the
clustering is a consequence of the edges, not a decision made by hand.

Positions come from a seeded Fruchterman-Reingold relaxation, so the layout is
reproducible - rerunning this file gives the identical SVG.
"""
from __future__ import annotations

import numpy as np

import design as D
import fonts
from design import SIZE, T, w

W, H = 1180, 424
PAD_X, PAD_TOP, PAD_BOT = 96, 106, 100
CARD_H = 46
CARD_DY = 20

PROJECTS = {
    "blast-radius":    ("Python", "FastAPI", "HydraDB", "SQLite", "Docker", "Supabase"),
    "meridian":        ("TypeScript", "Next.js", "React", "Postgres", "Vercel"),
    "vivedly-ai":      ("TypeScript", "Electron", "React", "SQLite", "Ollama"),
    "semantic-cache":  ("TypeScript", "Postgres", "pgvector", "Python", "Docker"),
}
HUB_META = {
    "blast-radius":   ("27k lines", "381 tests"),
    "meridian":       ("20k lines", "15 views"),
    "vivedly-ai":     ("11k lines", "5-tier memory"),
    "semantic-cache": ("4.8k lines", "2 SDKs"),
}


def layout(seed: int = 12) -> tuple[dict, list, dict]:
    hubs = list(PROJECTS)
    techs = sorted({t for v in PROJECTS.values() for t in v})
    nodes = hubs + techs
    idx = {n: i for i, n in enumerate(nodes)}
    edges = [(idx[h], idx[t]) for h, ts in PROJECTS.items() for t in ts]

    n = len(nodes)
    rng = np.random.default_rng(seed)
    pos = rng.normal(0, 1.0, (n, 2))
    # hubs start spread apart so the relaxation does not have to break a symmetry
    for i, h in enumerate(hubs):
        a = 2 * np.pi * i / len(hubs)
        pos[idx[h]] = [np.cos(a) * 1.7, np.sin(a) * 1.7]

    k = 1.0
    deg = np.bincount(np.array(edges).ravel(), minlength=n).astype(float)
    for step in range(420):
        disp = np.zeros_like(pos)
        d = pos[:, None, :] - pos[None, :, :]
        dist = np.linalg.norm(d, axis=2) + 1e-9
        rep = (k * k / dist)[:, :, None] * d / dist[:, :, None]
        np.fill_diagonal(dist, np.inf)
        disp += rep.sum(axis=1)
        for a, b in edges:
            dd = pos[a] - pos[b]
            dl = np.linalg.norm(dd) + 1e-9
            f = (dl * dl / k) * dd / dl
            disp[a] -= f
            disp[b] += f
        # hubs carry more mass, so labels do not get flung to the rim
        disp /= (1.0 + 2.4 * (np.arange(n) < len(hubs)))[:, None]
        t = 0.16 * (1 - step / 420) + 0.008
        dl = np.linalg.norm(disp, axis=1, keepdims=True) + 1e-9
        pos += disp / dl * np.minimum(dl, t)

    lo, hi = pos.min(0), pos.max(0)
    pos = (pos - lo) / (hi - lo)
    pos[:, 0] = PAD_X + pos[:, 0] * (W - 2 * PAD_X)
    pos[:, 1] = PAD_TOP + pos[:, 1] * (H - PAD_TOP - PAD_BOT)
    return {n_: pos[i] for i, n_ in enumerate(nodes)}, edges, idx


def card_rect(P, name):
    x, y = P[name]
    meta = "  ·  ".join(HUB_META[name])
    bw = max(w(name, size=SIZE["body"], weight=700),
             w(meta, size=SIZE["tiny"], mono=True)) + 30
    bx = min(max(x - bw / 2, 10), W - bw - 10)
    return bx, y + CARD_DY, bw, CARD_H


def declutter(P, hubs, iters: int = 80):
    """Push technology nodes out from under the hub label cards.

    The force-directed layout knows about nodes, not about the label card each hub
    carries. Three technology nodes ended up geometrically inside a card, and since the
    cards are drawn last they simply swallowed them - present in the file, invisible on
    the page. Choosing to draw the card above instead does not help when the node is in
    the middle of where the card has to go, so the node moves instead."""
    P = {k: list(v) for k, v in P.items()}
    techs = [n for n in P if n not in hubs]

    def tech_box(t):
        """Dot plus the label centred 14px above it. Testing the dot alone is not
        enough: the label is wider than the dot and sits higher, so a node can clear a
        card while its name still lands on top of one."""
        tx, ty = P[t]
        lw = w(t, size=SIZE["tiny"], weight=500)
        return (min(tx - 7, tx - lw / 2 - 4), ty - 26,
                max(14.0, lw + 8), 33.0)

    def overlaps(a, b, m=6):
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        return (ax - m < bx + bw and ax + aw + m > bx
                and ay - m < by + bh and ay + ah + m > by)

    for _ in range(iters):
        moved = False
        for h in hubs:
            card = card_rect(P, h)
            cx0, cy0 = card[0] + card[2] / 2, card[1] + card[3] / 2
            for t in techs:
                if overlaps(tech_box(t), card):
                    tx, ty = P[t]
                    dx, dy = tx - cx0, ty - cy0
                    n = max((dx * dx + dy * dy) ** 0.5, 1e-6)
                    P[t] = [tx + dx / n * 11, ty + dy / n * 11]
                    moved = True
        if not moved:
            break
    for t in techs:
        P[t][0] = min(max(P[t][0], 52), W - 52)
        P[t][1] = min(max(P[t][1], PAD_TOP - 20), H - 34)
    return {k: tuple(v) for k, v in P.items()}


def build(theme: str) -> str:
    """The graph, drawn as light rather than as a wireframe.

    Straight hairlines between dots is what a debug view of a graph looks like. Curving
    each edge and running a pulse along it turns the same data into something with
    direction and life, and the hubs carry a glow so the eye finds the four projects
    before it finds the twelve dependencies."""
    c = D.THEMES[theme]
    P, edges, idx = layout()
    names = list(P)
    hubs = list(PROJECTS)
    P = declutter(P, hubs)

    chars = fonts.charset("".join(names) + "".join("".join(v) for v in HUB_META.values())
                          + "THE WORK, AS A GRAPHshared technology is a shared node "
                          + "the clustering follows from the edges/lines tests views SDKs memory-tier")
    css, _ = fonts.embed_faces(chars)

    o = [D.svg_open(W, H, "Rohit Maruri's projects drawn as one graph",
                    "Four projects as hub nodes and their shared technologies as the "
                    "nodes between them; the clustering follows from the shared edges.",
                    css),
         D.defs(c), D.page(W, H, c)]

    o.append(D.eyebrow(44, 46, "THE WORK, AS A GRAPH", c))
    o.append(T(W - 44, 46, "shared technology is a shared node", size=SIZE["micro"],
               fill=c["text3"], anchor="end"))
    o.append(D.dot_rule(44, 64, W - 88, c))

    # a soft light behind each hub, painted first so everything else sits on top
    for h in hubs:
        o.append(D.glow(P[h][0], P[h][1], 168))

    # ---- edges: quadratic curves bowed away from the midpoint
    for n_, (a, b) in enumerate(edges):
        (x1, y1), (x2, y2) = P[names[a]], P[names[b]]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        L = max((dx * dx + dy * dy) ** 0.5, 1e-6)
        bow = 0.13 * L
        cxp, cyp = mx - dy / L * bow, my + dx / L * bow
        d = f"M{x1:.1f} {y1:.1f}Q{cxp:.1f} {cyp:.1f} {x2:.1f} {y2:.1f}"
        o.append(f'<path d="{d}" fill="none" stroke="{c["line"]}" stroke-width="1.1"/>')
        delay = (n_ * 0.31) % 4.4
        o.append(f'<circle r="2.1" fill="{c["ink2"]}" opacity="0">'
                 f'<animateMotion path="{d}" dur="2.4s" begin="{delay:.2f}s"'
                 f' repeatCount="indefinite" calcMode="spline" keyPoints="0;1"'
                 f' keyTimes="0;1" keySplines="{D.EASE}"/>'
                 f'<animate attributeName="opacity" values="0;0.9;0.9;0" dur="2.4s"'
                 f' begin="{delay:.2f}s" repeatCount="indefinite"/></circle>')

    # ---- technology nodes
    for name in names[len(hubs):]:
        x, y = P[name]
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.4" fill="{c["ink2"]}"/>')
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="none"'
                 f' stroke="{c["ink2"]}" stroke-width="1" opacity="0.22"/>')
        o.append(T(x, y - 14, name, size=SIZE["tiny"], weight=500, fill=c["text2"],
                   anchor="middle"))

    # ---- project hubs
    for i, name in enumerate(hubs):
        x, y = P[name]
        meta = "  ·  ".join(HUB_META[name])
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="20" fill="none"'
                 f' stroke="{c["ink"]}" stroke-width="1.2" opacity="0.45">'
                 f'<animate attributeName="r" values="12;34;34" dur="3.4s"'
                 f' begin="{i * 0.85:.1f}s" repeatCount="indefinite"'
                 f' calcMode="spline" keyTimes="0;0.7;1" keySplines="{D.EASE};0 0 1 1"/>'
                 f'<animate attributeName="opacity" values="0.5;0;0" dur="3.4s"'
                 f' begin="{i * 0.85:.1f}s" repeatCount="indefinite"/></circle>')
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8.5" fill="{c["ink"]}"'
                 f' filter="url(#fBloom)"/>')

        tw = max(w(name, size=SIZE["body"], weight=700),
                 w(meta, size=SIZE["tiny"], mono=True))
        bw, bh = tw + 30, 46
        bx = min(max(x - bw / 2, 10), W - bw - 10)

        by = y + CARD_DY
        o.append(D.card(bx, by, bw, bh, c, radius=10))
        o.append(T(bx + 15, by + 20, name, size=SIZE["body"], weight=700, fill=c["text"]))
        o.append(T(bx + 15, by + 36, meta, size=SIZE["tiny"], mono=True, fill=c["text3"]))

    o.append("</svg>")
    return "".join(o)


def main() -> None:
    for theme in ("dark", "light"):
        s = build(theme)
        p = f"../assets/constellation-{theme}.svg"
        open(p, "w", encoding="utf-8").write(s)
        print(f"{p}: {len(s.encode()) / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
