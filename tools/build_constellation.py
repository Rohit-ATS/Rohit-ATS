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

from svgkit import THEMES, ch, esc, svg_open, text, window

W, H = 1180, 440
BAR = 34
PAD_X, PAD_TOP, PAD_BOT = 78, 74, 46

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


def build(theme: str) -> str:
    c = THEMES[theme]
    P, edges, idx = layout()
    names = list(P)
    hubs = list(PROJECTS)

    chrome, _ = window(W, H, c, "the work, as a graph", titlebar=BAR)
    o = [svg_open(W, H, "Rohit Maruri's projects drawn as a graph",
                  "Four projects as hub nodes, their shared technologies as the nodes "
                  "between them. Clustering follows from the shared edges."),
         chrome]

    # ---- edges, with a pulse travelling along each
    for n_, (a, b) in enumerate(edges):
        pa, pb = P[names[a]], P[names[b]]
        o.append(f'<line x1="{pa[0]:.1f}" y1="{pa[1]:.1f}" x2="{pb[0]:.1f}" y2="{pb[1]:.1f}"'
                 f' stroke="{c["chrome_dim"]}" stroke-width="1" opacity="0.55"/>')
        delay = (n_ * 0.37) % 5.0
        o.append(f'<circle r="2.4" fill="{c["mark"]}" opacity="0">'
                 f'<animate attributeName="cx" values="{pa[0]:.1f};{pb[0]:.1f}" dur="2.2s"'
                 f' begin="{delay:.2f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="cy" values="{pa[1]:.1f};{pb[1]:.1f}" dur="2.2s"'
                 f' begin="{delay:.2f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;0.95;0.95;0" dur="2.2s"'
                 f' begin="{delay:.2f}s" repeatCount="indefinite"/></circle>')

    # ---- tech nodes
    for name in names[len(hubs):]:
        x, y = P[name]
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.2" fill="{c["chrome"]}"'
                 f' opacity="0.85"/>')
        o.append(text(x, y - 10, name, 10.5, c["label"], anchor="middle"))

    # ---- project hubs
    for i, name in enumerate(hubs):
        x, y = P[name]
        lines = HUB_META[name]
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="{c["violet"]}">'
                 f'<animate attributeName="r" values="9;11.5;9" dur="3.1s"'
                 f' begin="{i * 0.8:.1f}s" repeatCount="indefinite"/></circle>')
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="none"'
                 f' stroke="{c["violet"]}" stroke-width="1.4" opacity="0.5">'
                 f'<animate attributeName="r" values="9;26;26" dur="3.1s"'
                 f' begin="{i * 0.8:.1f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0.55;0;0" dur="3.1s"'
                 f' begin="{i * 0.8:.1f}s" repeatCount="indefinite"/></circle>')
        w = max(len(name), len(" / ".join(lines))) * ch(12) + 18
        bx = min(max(x - w / 2, 6), W - w - 6)
        o.append(f'<rect x="{bx:.1f}" y="{y + 14:.1f}" width="{w:.1f}" height="34" rx="6"'
                 f' fill="{c["panel"]}" stroke="{c["violet"]}" opacity="0.96"/>')
        o.append(text(bx + 9, y + 28, name, 12, c["violet"], weight="bold"))
        o.append(text(bx + 9, y + 42, " / ".join(lines), 10.5, c["title"]))

    o.append(text(26, H - 16,
                  "shared technology is a shared node / the clustering is a consequence "
                  "of the edges, not a layout decision", 10.5, c["title"], opacity=0.85))
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
