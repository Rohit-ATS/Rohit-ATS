"""assets/chess-{dark,light}.svg - Morphy's Opera Game, 1858, replayed.

Paris, an opera box, seventeen moves. Morphy gives up both rooks and the queen and mates
with the only pieces he has left. It is the game usually shown to explain that
development and tempo beat material, which is a reasonable thing to have on a profile
that argues the shape of a thing decides what you can do with it.

Moves are given as explicit from/to squares rather than SAN. Parsing SAN needs a legal
move generator to disambiguate, and a generator with a bug produces a board that looks
plausible and is wrong - the worst failure mode available here.

Piece glyphs are the one place on this profile that uses font text rather than paths:
at 30px the Unicode chess set is unambiguous, and drawing six pieces as outlines would
add more path data than the rest of the profile combined. They are NOT locked with
textLength - these glyphs are about one em wide, and forcing them to 0.6em squashes them.
"""
from __future__ import annotations

from svgkit import THEMES, ch, esc, svg_open, text, window

W, H = 1180, 452
BAR = 34
SQ = 46
BX, BY = 34, 58

PLY = 0.82
HOLD = 3.4

GLYPH = {"k": "♚", "q": "♛", "r": "♜",
         "b": "♝", "n": "♞", "p": "♟"}
PIECE_FONT = ("'Segoe UI Symbol','Apple Symbols','Noto Sans Symbols2',"
              "'Noto Sans Symbols 2','DejaVu Sans',sans-serif")

START = {
    "a1": ("r", "w"), "b1": ("n", "w"), "c1": ("b", "w"), "d1": ("q", "w"),
    "e1": ("k", "w"), "f1": ("b", "w"), "g1": ("n", "w"), "h1": ("r", "w"),
    "a8": ("r", "b"), "b8": ("n", "b"), "c8": ("b", "b"), "d8": ("q", "b"),
    "e8": ("k", "b"), "f8": ("b", "b"), "g8": ("n", "b"), "h8": ("r", "b"),
}
for f in "abcdefgh":
    START[f + "2"] = ("p", "w")
    START[f + "7"] = ("p", "b")

# (from, to) per ply. Castling carries the rook move as a third element.
MOVES = [
    ("e2", "e4"), ("e7", "e5"),
    ("g1", "f3"), ("d7", "d6"),
    ("d2", "d4"), ("c8", "g4"),
    ("d4", "e5"), ("g4", "f3"),
    ("d1", "f3"), ("d6", "e5"),
    ("f1", "c4"), ("g8", "f6"),
    ("f3", "b3"), ("d8", "e7"),
    ("b1", "c3"), ("c7", "c6"),
    ("c1", "g5"), ("b7", "b5"),
    ("c3", "b5"), ("c6", "b5"),
    ("c4", "b5"), ("b8", "d7"),
    ("e1", "c1", ("a1", "d1")), ("a8", "d8"),
    ("d1", "d7"), ("d8", "d7"),
    ("h1", "d1"), ("e7", "e6"),
    ("b5", "d7"), ("f6", "d7"),
    ("b3", "b8"), ("d7", "b8"),
    ("d1", "d8"),
]
SAN = [
    "e4 e5", "Nf3 d6", "d4 Bg4", "dxe5 Bxf3", "Qxf3 dxe5", "Bc4 Nf6",
    "Qb3 Qe7", "Nc3 c6", "Bg5 b5", "Nxb5 cxb5", "Bxb5+ Nbd7", "O-O-O Rd8",
    "Rxd7 Rxd7", "Rd1 Qe6", "Bxd7+ Nxd7", "Qb8+ Nxb8", "Rd8#",
]

LOOP = len(MOVES) * PLY + HOLD


def xy(sq: str) -> tuple[float, float]:
    f = ord(sq[0]) - 97
    r = int(sq[1]) - 1
    return BX + f * SQ, BY + (7 - r) * SQ


def simulate():
    """Play the game, recording every piece's track and when each one is captured."""
    board = {sq: [i, p, col] for i, (sq, (p, col)) in enumerate(START.items())}
    tracks = {pid: [(0.0, sq)] for sq, (pid, _, _) in board.items()}
    captured: dict[int, float] = {}

    for ply, mv in enumerate(MOVES):
        src, dst = mv[0], mv[1]
        t = ply * PLY
        if dst in board:                       # capture
            captured[board[dst][0]] = t + PLY * 0.45
            del board[dst]
        moving = board.pop(src)
        board[dst] = moving
        tracks[moving[0]].append((t, dst))
        if len(mv) > 2:                        # castling rook
            rs, rd = mv[2]
            rook = board.pop(rs)
            board[rd] = rook
            tracks[rook[0]].append((t, rd))
    return tracks, captured, {pid: (p, col) for sq, (pid, p, col) in
                              {s: v for s, v in board.items()}.items()}


def piece_meta():
    return {i: (p, col) for i, (sq, (p, col)) in enumerate(START.items())}


def build(theme: str) -> str:
    c = THEMES[theme]
    light_sq = "#1A2740" if theme == "dark" else "#E9EFF7"
    dark_sq = "#101B2E" if theme == "dark" else "#C9D8E8"
    wc = c["value"]
    bc = c["violet"]

    tracks, captured, _ = simulate()
    meta = piece_meta()

    chrome, _ = window(W, H, c, "opera-1858 --replay", titlebar=BAR)
    o = [svg_open(W, H, "Morphy's Opera Game, 1858",
                  "A chessboard replaying Paul Morphy's Opera Game: seventeen moves "
                  "ending in a queen sacrifice and mate."),
         chrome]

    # ---- board
    for r in range(8):
        for f in range(8):
            x, y = BX + f * SQ, BY + r * SQ
            fill = light_sq if (r + f) % 2 == 0 else dark_sq
            o.append(f'<rect x="{x}" y="{y}" width="{SQ}" height="{SQ}" fill="{fill}"/>')
    o.append(f'<rect x="{BX - 0.5}" y="{BY - 0.5}" width="{SQ * 8 + 1}" height="{SQ * 8 + 1}"'
             f' fill="none" stroke="{c["chrome_dim"]}"/>')
    for f in range(8):
        o.append(text(BX + f * SQ + SQ / 2, BY + SQ * 8 + 15, "abcdefgh"[f], 10,
                      c["title"], anchor="middle"))
        o.append(text(BX - 10, BY + f * SQ + SQ / 2 + 4, str(8 - f), 10, c["title"],
                      anchor="middle"))

    # ---- move highlight, jumping to each destination square
    hx, hy, kts = [], [], []
    for ply, mv in enumerate(MOVES):
        x, y = xy(mv[1])
        hx.append(f"{x:.0f}")
        hy.append(f"{y:.0f}")
        kts.append(f"{ply * PLY / LOOP:.4f}")
    hx.append(hx[-1]); hy.append(hy[-1]); kts.append("1")
    o.append(f'<rect width="{SQ}" height="{SQ}" fill="{c["mark"]}" opacity="0.22">'
             f'<animate attributeName="x" values="{";".join(hx)}" keyTimes="{";".join(kts)}"'
             f' calcMode="discrete" dur="{LOOP}s" repeatCount="indefinite"/>'
             f'<animate attributeName="y" values="{";".join(hy)}" keyTimes="{";".join(kts)}"'
             f' calcMode="discrete" dur="{LOOP}s" repeatCount="indefinite"/></rect>')

    # ---- pieces
    for pid, track in tracks.items():
        p, col = meta[pid]
        x0, y0 = xy(track[0][1])
        vals, kt = [], []
        cur = track[0][1]
        vals.append("0 0"); kt.append("0")
        for t, sq in track[1:]:
            px, py = xy(sq)
            ox, oy = xy(cur)
            # hold at the old square until the move starts, then glide over 45% of a ply
            vals.append(f"{ox - x0:.0f} {oy - y0:.0f}"); kt.append(f"{t / LOOP:.4f}")
            vals.append(f"{px - x0:.0f} {py - y0:.0f}")
            kt.append(f"{min((t + PLY * 0.45) / LOOP, 1.0):.4f}")
            cur = sq
        vals.append(vals[-1]); kt.append("1")

        anim = (f'<animateTransform attributeName="transform" type="translate"'
                f' values="{";".join(vals)}" keyTimes="{";".join(kt)}" dur="{LOOP}s"'
                f' repeatCount="indefinite"/>')
        fade = ""
        if pid in captured:
            tc = captured[pid] / LOOP
            fade = (f'<animate attributeName="opacity"'
                    f' values="1;1;0;0;1" keyTimes="0;{max(tc - 0.006, 0):.4f};'
                    f'{tc:.4f};0.9990;1" dur="{LOOP}s" repeatCount="indefinite"/>')
        glyph = (f'<text x="{x0 + SQ / 2:.0f}" y="{y0 + SQ * 0.72:.0f}" font-size="30"'
                 f' font-family="{PIECE_FONT}" fill="{wc if col == "w" else bc}"'
                 f' text-anchor="middle">{GLYPH[p]}</text>')
        o.append(f"<g>{anim}{fade}{glyph}</g>")

    # ---- move list, two columns, with the current move highlighted
    MX, MY, MH = 452, 82, 26
    o.append(text(MX, BY + 4, "MORPHY  vs  DUKE OF BRUNSWICK & COUNT ISOUARD", 12,
                  c["chrome"], weight="bold"))
    o.append(text(MX, BY + 22, "Paris Opera, 1858", 11, c["title"]))

    rows = 9
    pos = []
    for i, san in enumerate(SAN):
        col_i, row_i = divmod(i, rows)
        x = MX + col_i * 350
        y = MY + 34 + row_i * MH
        pos.append((x, y))
        o.append(text(x, y, f"{i + 1:2d}.", 13, c["dim"]))
        o.append(text(x + 30, y, san, 13, c["value"]))

    px, py, pkt = [], [], []
    for ply in range(len(MOVES)):
        x, y = pos[ply // 2]
        px.append(f"{x - 8:.0f}"); py.append(f"{y - 15:.0f}")
        pkt.append(f"{ply * PLY / LOOP:.4f}")
    px.append(px[-1]); py.append(py[-1]); pkt.append("1")
    o.append(f'<rect width="330" height="21" rx="4" fill="{c["violet"]}" opacity="0.14">'
             f'<animate attributeName="x" values="{";".join(px)}" keyTimes="{";".join(pkt)}"'
             f' calcMode="discrete" dur="{LOOP}s" repeatCount="indefinite"/>'
             f'<animate attributeName="y" values="{";".join(py)}" keyTimes="{";".join(pkt)}"'
             f' calcMode="discrete" dur="{LOOP}s" repeatCount="indefinite"/></rect>')

    o.append(text(MX, H - 22, "both rooks and the queen given away", 11, c["title"]))
    o.append(text(MX, H - 8, "mate delivered by the only two pieces left on the board",
                  11, c["title"]))
    o.append("</svg>")
    return "".join(o)


def main() -> None:
    for theme in ("dark", "light"):
        s = build(theme)
        p = f"../assets/chess-{theme}.svg"
        open(p, "w", encoding="utf-8").write(s)
        print(f"{p}: {len(s.encode()) / 1024:6.1f} KB   loop {LOOP:.1f}s")


if __name__ == "__main__":
    main()
