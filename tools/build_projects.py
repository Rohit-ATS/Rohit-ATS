"""assets/projects-{dark,light}.svg - five shipped projects as one panel.

The README used to spend a full screen per project: a header, a prose argument, a
four-row table, a terminal screenshot. Read top to bottom that is a chapter each, and a
visitor deciding in fifteen seconds never reaches the third one.

This panel is the compression. One row per project, and every row answers the same three
questions in the same three places, so the eye compares across rows instead of reading
each one from scratch:

  left      what it is called, and the one sentence that says why it exists
  under     what it is built out of, as one mono run rather than a row of chips
  right     the number that is checkable - tests, evals, the invariant it enforces

Motion is a single scanner: a lit segment walks the left rail down the five rows on a
shared loop, and the row it is level with brightens. One animation with one meaning,
rather than five things blinking for decoration. Rows also arrive staggered on first
paint and then hold - an intro that replays forever is a distraction on a profile.
"""
from __future__ import annotations

import design as D
import fonts
from design import SIZE, T, w

W = 1180
PAD = 44
ROW_H = 98
TOP = 96                      # first row's top edge
NAME_X = PAD + 40             # name column, clear of the rail and the index
LOOP = 9.0                    # one pass of the scanner over all five rows

# (name, accent key, one-line reason it exists, what it's made of, the checkable number)
# Every row carries the same accent on purpose. Five different colours down a list is
# five competing focal points; the scanner is what says which row to look at.
ROWS = [
    ("LexisGuide", "ink",
     "Reads the legal notice you were sent and finds the deadline buried in it.",
     "React 19 · FastAPI on Lambda · Bedrock Nova · DynamoDB · Solidity on Base",
     ["LexHack 2026", "router + specialist agents", "SHA-256 audit trail"]),
    ("DOCKET", "ink",
     "The agent that reads city hall so a volunteer neighborhood group doesn't have to.",
     "Next.js 15 · Strands Agents on Bedrock AgentCore · Aurora DSQL · S3 Vectors",
     ["81 tests", "19/20 citations valid", "5/5 correct refusals"]),
    ("FORGE", "ink",
     "Ships the feature, then audits itself and proves the hole is actually closed.",
     "Python 3.14 · FastAPI · OpenTelemetry · SQLite · pytest",
     ["17 live checks", "two independent verifications", "stops at the PR"]),
    ("Airlock", "ink",
     "Proves an irreversible production change on a shadow copy before anyone approves it.",
     "TypeScript · Next.js 15 · Postgres shadow branches · MCP server · hash-chain ledger",
     ["201 tests / 24 suites", "pre == post_rollback", "MIT"]),
    ("Semantic Output Cache", "ink",
     "Exact-match caches never hit on LLM traffic. This one keys on meaning instead.",
     "PostgreSQL · pgvector · Redis as accelerator, not dependency · JS + Python SDKs",
     ["cosine threshold", "key hashes only", "circuit breaker"]),
]

H = TOP + ROW_H * len(ROWS) + 54
RAIL_X = PAD + 13
RAIL_TOP = TOP + 10
RAIL_H = ROW_H * len(ROWS) - 20

EYEBROW = "SELECTED WORK"
ASIDE = "one row each · the number on the right is checkable"
FOOT = "Every repository is public, MIT, and has its tests in it."


def scanner(c: dict) -> str:
    """A lit segment walking the rail, plus the faint track it walks on.

    The segment is 1/5 of the rail and moves in five discrete steps rather than
    sliding: it is indexing rows, and a smooth slide would read as decoration that
    happens to be vertical."""
    seg = RAIL_H / len(ROWS)
    kts = ";".join(f"{i / len(ROWS):.4f}" for i in range(len(ROWS))) + ";1"
    ys = ";".join(f"{RAIL_TOP + i * seg:.1f}" for i in range(len(ROWS)))
    ys += f";{RAIL_TOP:.1f}"
    return (f'<rect x="{RAIL_X:.1f}" y="{RAIL_TOP:.1f}" width="1.5" height="{RAIL_H:.1f}"'
            f' rx="0.75" fill="{c["line"]}"/>'
            f'<rect x="{RAIL_X - 0.5:.1f}" y="{RAIL_TOP:.1f}" width="2.5"'
            f' height="{seg - 18:.1f}" rx="1.25" fill="{c["ink"]}" opacity="0.85"'
            f' filter="url(#fBloom)">'
            f'<animate attributeName="y" values="{ys}" keyTimes="{kts}"'
            f' calcMode="discrete" dur="{LOOP}s" repeatCount="indefinite"/></rect>')


def row(i: int, c: dict) -> str:
    name, key, line, stack, facts = ROWS[i]
    ry = TOP + i * ROW_H
    acc = c[key]
    o = []

    # The row the scanner is level with lifts out of the page: its plate appears and
    # its accent dot swells. keyTimes are the scanner's own steps, so they cannot drift.
    n = len(ROWS)
    kt = ";".join(f"{v:.4f}" for v in
                  [0, i / n, i / n + 0.004, (i + 1) / n - 0.004, (i + 1) / n, 1])
    plate = (f'<rect x="{PAD - 10:.1f}" y="{ry + 2:.1f}" width="{W - PAD * 2 + 20:.1f}"'
             f' height="{ROW_H - 14:.1f}" rx="10" fill="{c["surf"]}" opacity="0">'
             f'<animate attributeName="opacity" values="0;0;0.75;0.75;0;0"'
             f' keyTimes="{kt}" dur="{LOOP}s" repeatCount="indefinite"/></rect>')
    o.append(plate)

    o.append(f'<circle cx="{RAIL_X + 0.7:.1f}" cy="{ry + 26:.1f}" r="3" fill="{acc}">'
             f'<animate attributeName="r" values="3;3;5;5;3;3" keyTimes="{kt}"'
             f' dur="{LOOP}s" repeatCount="indefinite"/></circle>')

    o.append(T(PAD + 2, ry + 62, f"0{i + 1}", size=SIZE["micro"], mono=True,
               fill=c["text3"], track=0.06))
    o.append(T(NAME_X, ry + 30, name, size=SIZE["sub"], weight=500, fill=c["text"]))
    o.append(T(NAME_X, ry + 54, line, size=SIZE["small"], fill=c["text2"]))
    o.append(T(NAME_X, ry + 76, stack, size=SIZE["micro"], mono=True, fill=c["text3"]))

    # Facts stack up at the right edge, right-aligned, smallest thing on the row that is
    # still a number. The first one carries the accent because it is the claim.
    for j, f in enumerate(facts):
        o.append(T(W - PAD, ry + 28 + j * 18, f, size=SIZE["micro"], mono=True,
                   fill=acc if j == 0 else c["text3"], anchor="end"))

    if i:
        o.append(D.dot_rule(NAME_X, ry - 8, W - PAD - NAME_X, c, fade=False))

    # Staggered arrival, then freeze. 90ms apart is enough to read as a sequence and
    # short enough that the whole panel has settled before a visitor has scrolled to it.
    return (f'<g opacity="0" transform="translate(0,6)">'
            f'<animate attributeName="opacity" to="1" dur="0.5s"'
            f' begin="{0.15 + i * 0.09:.2f}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate"'
            f' from="0 6" to="0 0" dur="0.5s" begin="{0.15 + i * 0.09:.2f}s"'
            f' keySplines="{D.EASE}" calcMode="spline" fill="freeze"/>'
            f'{"".join(o)}</g>')


def build(theme: str) -> str:
    c = D.THEMES[theme]
    strings = "".join(n + l + s + "".join(f) for n, _, l, s, f in ROWS)
    css, _ = fonts.embed_faces(fonts.charset(strings + EYEBROW + ASIDE + FOOT + "/·=×"))

    o = [D.svg_open(W, H, "Five shipped projects",
                    "LexisGuide, DOCKET, FORGE, Airlock and Semantic Output Cache - one "
                    "row each, with what it is for, what it is built out of, and the "
                    "test or evaluation number that can be checked in the repository.",
                    css),
         D.defs(c), D.page(W, H, c),
         D.glow(PAD + 220, TOP + 20, 340),
         D.eyebrow(PAD, 48, EYEBROW, c),
         T(W - PAD, 48, ASIDE, size=SIZE["micro"], fill=c["text3"], anchor="end"),
         D.dot_rule(PAD, 66, W - PAD * 2, c),
         scanner(c)]

    o += [row(i, c) for i in range(len(ROWS))]
    o.append(T(PAD, H - 22, FOOT, size=SIZE["micro"], mono=True, fill=c["text3"]))
    o.append("</svg>")
    return "".join(o)


def main() -> None:
    for theme in ("dark", "light"):
        s = build(theme)
        p = f"../assets/projects-{theme}.svg"
        open(p, "w", encoding="utf-8").write(s)
        print(f"{p}: {len(s.encode()) / 1024:6.1f} KB  ({W}x{H})")


if __name__ == "__main__":
    main()
