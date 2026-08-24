"""assets/terminal-{dark,light}.svg - an animated Blast Radius incident session.

This replaces three static screenshots totalling 1.4MB. A screenshot asserts that the
tool has a UI; a session shows what it answers and how long each answer took, which is
the claim the project actually makes. Every latency here is one Blast Radius reports.

One shared 15.4s loop drives everything. Each element's animation runs the full cycle
length with keyTimes marking its own window, so nothing can drift out of sync - the
failure you get from giving each line its own dur and begin.
"""
from __future__ import annotations

import design as D
import fonts
from design import SIZE, T, reveal, type_clip, w

W, H = 1180, 348
FS = 13.5
CW = 0.0          # filled in once the font metrics are available
X0 = 44           # prompt column
XI = 62           # output indent
XR = W - 44       # right edge for latencies
LH = 23
Y0 = 108

LOOP = 15.4
CMD1 = "blast-radius trace event-stream@3.3.6 --depth 5"
CMD2 = "blast-radius fix --lockfile package-lock.json"

# (label, value, latency) - leaders are computed, never written by hand
TRACE = [
    ("resolving versioned graph",      "11,482,391 releases",     None),
    ("traversing REQUIRES depth 5",    "1,247 packages exposed",  "38ms"),
    ("evaluating declared semver",     "903 would have resolved", "12ms"),
    ("osv.dev live lookup",            "GHSA-mh6f-8j2x",          "94ms"),
]


def leader(x0: float, x1: float, y: float, c: dict) -> str:
    """Dotted leader, spaced to fill the gap exactly. Computed from the two measured
    text widths - never written into the SVG by hand."""
    n = int((x1 - x0) // 7)
    if n <= 0:
        return ""
    step = (x1 - x0) / n
    d = "".join(f"M{x0 + i * step:.1f} {y - 4:.1f}h1.6" for i in range(n))
    return f'<path d="{d}" stroke="{c["line"]}" stroke-width="1.5" fill="none"/>'


def prompt_line(y: float, cmd: str, cid: str, c: dict) -> str:
    return (T(X0, y, "$", size=FS, mono=True, weight=700, fill=c["green"])
            + f'<g clip-path="url(#{cid})">'
            + T(X0 + CW * 2, y, cmd, size=FS, mono=True, fill=c["text"]) + '</g>')


def cursor(y: float, n: int, t0: float, t1: float, c: dict) -> str:
    xs, kts = [], []
    for i in range(n + 1):
        xs.append(f"{X0 + CW * 2 + i * CW:.1f}")
        kts.append(f"{(t0 + (t1 - t0) * i / max(n, 1)) / LOOP:.4f}")
    xs.append(xs[-1]); kts.append("1")
    # An explicit starting x matters. With only an animated x, the rect renders at 0
    # until the animation reaches its first keyTime, which parks a stray cursor block
    # against the left edge of the panel for the first third of a second.
    return (f'<rect x="{xs[0]}" y="{y - FS + 2.5:.1f}" width="{CW:.1f}"'
            f' height="{FS:.1f}" rx="1" fill="{c["ink2"]}" opacity="0.9">'
            f'<animate attributeName="x" values="{";".join(xs)}" keyTimes="{";".join(kts)}"'
            f' calcMode="discrete" dur="{LOOP}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.95;0.95;0.1;0.95" dur="1.05s"'
            f' repeatCount="indefinite"/></rect>')


def build(theme: str) -> str:
    global CW
    c = D.THEMES[theme]
    CW = w("M", size=FS, mono=True)

    strings = (CMD1 + CMD2 + "".join(a + b + (m or "") for a, b, m in TRACE)
               + "INCIDENT REPLAYblast-radius --traceBLAST RADIUS$"
               + "1,247 reachable  903 actually vulnerable  4 at depth 1"
               + "safe version 3.3.4overrides block writtenbrief emitted for an agent"
               + "27k lines / 381 tests / MIT / built solo over a hackathon weekend/")
    css, _ = fonts.embed_faces(fonts.charset(strings))

    o = [D.svg_open(W, H, "A Blast Radius incident, replayed",
                    "A terminal running a supply-chain incident: transitive exposure, "
                    "semver resolution, a live OSV lookup and the fix, each carrying the "
                    "latency of the query that produced it.", css),
         D.defs(c),
         "<defs>",
         type_clip("tc1", len(CMD1), CW, X0 + CW * 2, Y0 - FS, FS + 6, LOOP, 0.35, 2.05),
         type_clip("tc2", len(CMD2), CW, X0 + CW * 2, Y0 + LH * 6 - FS, FS + 6, LOOP, 8.6, 10.1),
         "</defs>",
         D.page(W, H, c)]

    o.append(D.eyebrow(44, 46, "INCIDENT REPLAY", c, colour=c["rose"]))
    o.append(T(W - 44, 46, "blast-radius --trace", size=SIZE["micro"], mono=True,
               fill=c["text3"], anchor="end"))
    o.append(D.dot_rule(44, 64, W - 88, c))

    y = Y0
    o.append(prompt_line(y, CMD1, "tc1", c))
    o.append(reveal(cursor(y, len(CMD1), 0.35, 2.05, c), LOOP, 0.1, 2.35))

    for i, (label, value, ms) in enumerate(TRACE):
        yy = y + LH * (i + 1)
        vw = w(value, size=FS, mono=True)
        lat = (w(ms, size=FS, mono=True) + 18) if ms else 0
        vx = XR - lat - vw
        parts = [T(XI, yy, label, size=FS, mono=True, fill=c["text3"]),
                 leader(XI + w(label, size=FS, mono=True) + 10, vx - 10, yy, c),
                 T(vx, yy, value, size=FS, mono=True, fill=c["text2"])]
        if ms:
            parts.append(T(XR, yy, ms, size=FS, mono=True, fill=c["green"], anchor="end"))
        o.append(reveal("".join(parts), LOOP, 2.4 + i * 0.42, 14.3))

    ys = y + LH * 5
    band = [D.glow(XI + 150, ys - 4, 190),
            f'<rect x="{XI - 12}" y="{ys - FS - 5:.1f}" width="{XR - XI + 12}"'
            f' height="{FS + 15:.1f}" rx="7" fill="{c["surf2"]}" stroke="{c["line"]}"/>',
            f'<rect x="{XI - 12}" y="{ys - FS - 5:.1f}" width="3" height="{FS + 15:.1f}"'
            f' rx="1.5" fill="{c["ink"]}"/>',
            T(XI, ys, "BLAST RADIUS", size=FS, mono=True, weight=700, fill=c["ink"])]
    seg_x = XI + w("BLAST RADIUS", size=FS, mono=True, weight=700) + 22
    for txt, col in (("1,247 reachable", c["text"]),
                     ("903 actually vulnerable", c["amber"]),
                     ("4 at depth 1", c["rose"])):
        band.append(T(seg_x, ys, txt, size=FS, mono=True, fill=col))
        seg_x += w(txt, size=FS, mono=True) + 26
    o.append(reveal("".join(band), LOOP, 4.5, 14.3))

    y2 = y + LH * 6
    o.append(reveal(prompt_line(y2, CMD2, "tc2", c), LOOP, 8.45, 14.3))
    o.append(reveal(cursor(y2, len(CMD2), 8.6, 10.1, c), LOOP, 8.35, 10.4))

    y3 = y + LH * 7
    fx = XI
    for i, txt in enumerate(("safe version 3.3.4", "overrides block written",
                             "brief emitted for an agent")):
        if i:
            fx += 4
            o_sep = T(fx, y3, "/", size=FS, mono=True, fill=c["line"])
            fx += w("/", size=FS, mono=True) + 12
        else:
            o_sep = ""
        o.append(reveal(o_sep + T(fx, y3, txt, size=FS, mono=True, fill=c["green"]),
                        LOOP, 10.4, 14.3))
        fx += w(txt, size=FS, mono=True) + 8

    o.append(D.dot_rule(44, H - 46, W - 88, c))
    o.append(T(44, H - 24, "27k lines  /  381 tests  /  MIT  /  built solo over a hackathon weekend",
               size=SIZE["micro"], fill=c["text3"]))
    o.append("</svg>")
    return "".join(o)


def main() -> None:
    for theme in ("dark", "light"):
        s = build(theme)
        p = f"../assets/terminal-{theme}.svg"
        open(p, "w", encoding="utf-8").write(s)
        print(f"{p}: {len(s.encode()) / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
