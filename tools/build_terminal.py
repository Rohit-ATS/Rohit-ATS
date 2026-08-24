"""assets/terminal-{dark,light}.svg - an animated Blast Radius incident session.

This replaces three static screenshots totalling 1.4MB. A screenshot asserts that the
tool has a UI; a session shows what it answers and how long each answer took, which is
the claim the project actually makes. Every latency here is one Blast Radius reports.

One shared 15.4s loop drives everything. Each element's animation runs the full cycle
length with keyTimes marking its own window, so nothing can drift out of sync - the
failure you get from giving each line its own dur and begin.
"""
from __future__ import annotations

from svgkit import THEMES, ch, esc, reveal, svg_open, text, type_clip, window

W, H = 1180, 268
BAR = 34
FS = 13.5
CW = ch(FS)
X0 = 26          # prompt column
XI = 42          # output indent
XR = W - 26      # right edge for latencies
LH = 22
Y0 = 62

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
    n = int((x1 - x0) // 6)
    if n <= 0:
        return ""
    step = (x1 - x0) / n
    d = "".join(f"M{x0 + i * step:.1f} {y - 4:.1f}h1.7" for i in range(n))
    return f'<path d="{d}" stroke="{c["leader"]}" stroke-width="1.6" fill="none"/>'


def prompt_line(y: float, cmd: str, cid: str, c: dict) -> str:
    """A typed command: green $, then the command revealed through its clip, then a
    block cursor stepping along behind the last character."""
    o = [text(X0, y, "$", FS, c["good"], weight="bold")]
    body = text(X0 + CW * 2, y, cmd, FS, c["value"])
    o.append(f'<g clip-path="url(#{cid})">{body}</g>')
    return "".join(o)


def cursor(y: float, n: int, t0: float, t1: float, c: dict) -> str:
    """Block cursor: x steps one advance per character, opacity blinks independently."""
    xs, kts = [], []
    for i in range(n + 1):
        xs.append(f"{X0 + CW * 2 + i * CW:.1f}")
        kts.append(f"{(t0 + (t1 - t0) * i / max(n, 1)) / LOOP:.4f}")
    xs.append(xs[-1]); kts.append("1")
    return (f'<rect y="{y - FS + 2.5:.1f}" width="{CW:.1f}" height="{FS:.1f}"'
            f' fill="{c["chrome"]}" opacity="0.85">'
            f'<animate attributeName="x" values="{";".join(xs)}" keyTimes="{";".join(kts)}"'
            f' calcMode="discrete" dur="{LOOP}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.9;0.9;0.15;0.9" dur="1.05s"'
            f' repeatCount="indefinite"/></rect>')


def build(theme: str) -> str:
    c = THEMES[theme]
    chrome, _ = window(W, H, c, "blast-radius --incident", titlebar=BAR)
    o = [svg_open(W, H,
                  "Blast Radius incident session",
                  "A terminal replaying a supply-chain incident: transitive exposure, "
                  "semver resolution, a live OSV lookup, and the fix - each with the "
                  "latency of the query that produced it."),
         "<defs>",
         type_clip("tc1", len(CMD1), CW, X0 + CW * 2, Y0 - FS, FS + 6, LOOP, 0.35, 2.05),
         type_clip("tc2", len(CMD2), CW, X0 + CW * 2, Y0 + LH * 6 - FS, FS + 6, LOOP, 8.6, 10.1),
         "</defs>", chrome]

    # ---- command 1
    y = Y0
    o.append(prompt_line(y, CMD1, "tc1", c))
    o.append(reveal(cursor(y, len(CMD1), 0.35, 2.05, c), LOOP, 0.1, 2.35))

    # ---- trace output
    for i, (label, value, ms) in enumerate(TRACE):
        yy = y + LH * (i + 1)
        t_on = 2.4 + i * 0.42
        lw = len(label) * CW
        vw = len(value) * CW
        lat_w = (len(ms) * CW + 14) if ms else 0
        vx = XR - lat_w - vw
        parts = [text(XI, yy, label, FS, c["dim"]),
                 leader(XI + lw + 8, vx - 8, yy, c),
                 text(vx, yy, value, FS, c["chrome"])]
        if ms:
            parts.append(text(XR, yy, ms, FS, c["good"], anchor="end"))
        o.append(reveal("".join(parts), LOOP, t_on, 14.3))

    # ---- summary band
    ys = y + LH * 5
    summary = [
        f'<rect x="{XI - 10}" y="{ys - FS - 3:.1f}" width="{XR - XI + 10}" height="{FS + 11:.1f}"'
        f' rx="4" fill="{c["violet"]}" opacity="0.10"/>',
        text(XI, ys, "BLAST RADIUS", FS, c["violet"], weight="bold"),
        text(XI + 14 * CW, ys, "1,247 reachable", FS, c["value"]),
        text(XI + 31 * CW, ys, "903 actually vulnerable", FS, c["warn"]),
        text(XI + 56 * CW, ys, "4 at depth 1", FS, c["bad"]),
    ]
    o.append(reveal("".join(summary), LOOP, 4.5, 14.3))

    # ---- command 2 + result
    y2 = y + LH * 6
    # The $ for the second command is revealed with it. Drawn unconditionally it sits
    # there from the first frame, which reads as a stray prompt under the output.
    o.append(reveal(prompt_line(y2, CMD2, "tc2", c), LOOP, 8.45, 14.3))
    o.append(reveal(cursor(y2, len(CMD2), 8.6, 10.1, c), LOOP, 8.35, 10.4))

    y3 = y + LH * 7
    fix = [text(XI, y3, "safe version 3.3.4", FS, c["good"]),
           text(XI + 19 * CW, y3, "/", FS, c["dim"]),
           text(XI + 21 * CW, y3, "overrides block written", FS, c["good"]),
           text(XI + 45 * CW, y3, "/", FS, c["dim"]),
           text(XI + 47 * CW, y3, "brief emitted for an agent", FS, c["good"])]
    o.append(reveal("".join(fix), LOOP, 10.4, 14.3))

    o.append(text(X0, H - 14, "27k lines / 381 tests / MIT / built solo over a hackathon weekend",
                  10.5, c["title"], opacity=0.8))
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
