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

import design as D
import fonts
from design import SIZE, T, w

W, H = 1180, 462
SQ = 42
BX, BY = 52, 96

PLY = 0.78
HOLD = 3.2

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
    """The Opera Game, drawn as a board worth looking at.

    Piece glyphs are the one place on this profile that uses font text rather than
    paths: at this size the Unicode chess set is unambiguous, and drawing six pieces as
    outlines would add more path data than everything else here combined. The sides are
    told apart by colour rather than by the hollow/filled convention, because hollow
    glyphs render thin and weak against a dark board.
    """
    c = D.THEMES[theme]
    # Neutral squares. These were hardcoded blues and survived the palette
    # swap untouched, which left one panel still tinted.
    light_sq = "#212124" if theme == "dark" else "#ECECE9"
    dark_sq = "#151518" if theme == "dark" else "#DAD9D5"
    # In colour the sides were told apart by hue, which collapses in monochrome.
    # Back to the actual chess convention - one side solid, the other outlined - and it
    # has to invert per theme: on paper the solid piece is the dark one, on a dark
    # ground the solid piece is the light one. Using the text colour for "white" in both
    # themes rendered both armies near-black in the light theme.
    if theme == "dark":
        w_paint = f'fill="{c["text"]}"'
        b_paint = (f'fill="#141416" stroke="{c["text2"]}" stroke-width="1.1"'
                   f' paint-order="stroke"')
    else:
        w_paint = (f'fill="#FFFFFF" stroke="{c["text"]}" stroke-width="1.1"'
                   f' paint-order="stroke"')
        b_paint = f'fill="{c["text"]}"'

    tracks, captured, _ = simulate()
    meta = piece_meta()

    chars = fonts.charset("".join(SAN) + "OFF THE CLOCKMORPHY vs BRUNSWICK & ISOUARD"
                          + "Paris Opera, 1858 seventeen movesabcdefgh12345678"
                          + "both rooks and the queen, given away"
                          + "mate delivered by the only two pieces left on the board"
                          + "morphy opera 1858 .O-#+x")
    css, _ = fonts.embed_faces(chars)

    o = [D.svg_open(W, H, "Morphy's Opera Game, 1858",
                    "A chessboard replaying Paul Morphy's Opera Game: seventeen moves "
                    "ending in a queen sacrifice and mate.", css),
         D.defs(c), D.page(W, H, c)]

    o.append(D.eyebrow(44, 46, "OFF THE CLOCK", c, colour=c["amber"]))
    o.append(T(W - 44, 46, "morphy / opera / 1858", size=SIZE["micro"], mono=True,
               fill=c["text3"], anchor="end"))
    o.append(D.dot_rule(44, 64, W - 88, c))

    # ---- board
    o.append(D.glow(BX + SQ * 4, BY + SQ * 4, 250))
    o.append(D.card(BX - 12, BY - 12, SQ * 8 + 24, SQ * 8 + 24, c, radius=14))
    for r in range(8):
        for f in range(8):
            o.append(f'<rect x="{BX + f * SQ}" y="{BY + r * SQ}" width="{SQ}" height="{SQ}"'
                     f' fill="{light_sq if (r + f) % 2 == 0 else dark_sq}"/>')
    for f in range(8):
        o.append(T(BX + f * SQ + SQ / 2, BY + SQ * 8 + 20, "abcdefgh"[f],
                   size=SIZE["micro"], mono=True, fill=c["text3"], anchor="middle"))
        o.append(T(BX - 16, BY + f * SQ + SQ / 2 + 4, str(8 - f), size=SIZE["micro"],
                   mono=True, fill=c["text3"], anchor="middle"))

    # ---- destination highlight, stepping square to square
    hx, hy, kts = [], [], []
    for ply, mv in enumerate(MOVES):
        x, y = xy(mv[1])
        hx.append(f"{x:.0f}")
        hy.append(f"{y:.0f}")
        kts.append(f"{ply * PLY / LOOP:.4f}")
    hx.append(hx[-1]); hy.append(hy[-1]); kts.append("1")
    o.append(f'<rect x="{hx[0]}" y="{hy[0]}" width="{SQ}" height="{SQ}"'
             f' fill="{c["amber"]}" opacity="0.20">'
             f'<animate attributeName="x" values="{";".join(hx)}" keyTimes="{";".join(kts)}"'
             f' calcMode="discrete" dur="{LOOP}s" repeatCount="indefinite"/>'
             f'<animate attributeName="y" values="{";".join(hy)}" keyTimes="{";".join(kts)}"'
             f' calcMode="discrete" dur="{LOOP}s" repeatCount="indefinite"/></rect>')

    # ---- pieces
    for pid, track in tracks.items():
        p_, col = meta[pid]
        x0, y0 = xy(track[0][1])
        vals, kt = ["0 0"], ["0"]
        cur = track[0][1]
        for t, sq in track[1:]:
            px_, py_ = xy(sq)
            ox, oy = xy(cur)
            vals.append(f"{ox - x0:.0f} {oy - y0:.0f}")
            kt.append(f"{t / LOOP:.4f}")
            vals.append(f"{px_ - x0:.0f} {py_ - y0:.0f}")
            kt.append(f"{min((t + PLY * 0.45) / LOOP, 1.0):.4f}")
            cur = sq
        vals.append(vals[-1]); kt.append("1")
        # Eased, not linear. A piece sliding at constant speed reads as a sprite being
        # dragged; an ease-out reads as a hand putting it down.
        splines = ";".join([D.EASE] * (len(kt) - 1))
        anim = (f'<animateTransform attributeName="transform" type="translate"'
                f' values="{";".join(vals)}" keyTimes="{";".join(kt)}"'
                f' calcMode="spline" keySplines="{splines}"'
                f' dur="{LOOP}s" repeatCount="indefinite"/>')
        fade = ""
        if pid in captured:
            tc = captured[pid] / LOOP
            fade = (f'<animate attributeName="opacity" values="1;1;0;0;1"'
                    f' keyTimes="0;{max(tc - 0.006, 0):.4f};{tc:.4f};0.9990;1"'
                    f' dur="{LOOP}s" repeatCount="indefinite"/>')
        paint = w_paint if col == "w" else b_paint
        glyph = (f'<text x="{x0 + SQ / 2:.0f}" y="{y0 + SQ * 0.73:.0f}" font-size="29"'
                 f' font-family="{PIECE_FONT}" {paint}'
                 f' text-anchor="middle">{GLYPH[p_]}</text>')
        o.append(f"<g>{anim}{fade}{glyph}</g>")

    # ---- move list
    MX = BX + SQ * 8 + 74
    o.append(T(MX, BY + 6, "MORPHY  vs  BRUNSWICK & ISOUARD", size=SIZE["lead"],
               weight=700, fill=c["text"]))
    o.append(T(MX, BY + 28, "Paris Opera, 1858  /  seventeen moves", size=SIZE["small"],
               fill=c["text3"]))
    o.append(D.dot_rule(MX, BY + 44, W - 44 - MX, c))

    rows, MY, MH, COLW = 9, BY + 78, 27, 330
    pos = []
    for i in range(len(SAN)):
        ci, ri = divmod(i, rows)
        pos.append((MX + ci * COLW, MY + ri * MH))

    px, py, pkt = [], [], []
    for ply in range(len(MOVES)):
        x, y = pos[ply // 2]
        px.append(f"{x - 10:.0f}")
        py.append(f"{y - 17:.0f}")
        pkt.append(f"{ply * PLY / LOOP:.4f}")
    px.append(px[-1]); py.append(py[-1]); pkt.append("1")
    o.append(f'<rect x="{px[0]}" y="{py[0]}" width="{COLW - 30}" height="24" rx="6"'
             f' fill="{c["ink"]}" opacity="0.13">'
             f'<animate attributeName="x" values="{";".join(px)}" keyTimes="{";".join(pkt)}"'
             f' calcMode="discrete" dur="{LOOP}s" repeatCount="indefinite"/>'
             f'<animate attributeName="y" values="{";".join(py)}" keyTimes="{";".join(pkt)}"'
             f' calcMode="discrete" dur="{LOOP}s" repeatCount="indefinite"/></rect>')

    for i, san in enumerate(SAN):
        x, y = pos[i]
        o.append(T(x, y, f"{i + 1}.", size=SIZE["small"], mono=True, fill=c["text3"]))
        o.append(T(x + 32, y, san, size=SIZE["small"], mono=True, fill=c["text2"]))

    o.append(T(MX, H - 46, "both rooks and the queen, given away",
               size=SIZE["small"], fill=c["text3"]))
    o.append(T(MX, H - 26, "mate delivered by the only two pieces left on the board",
               size=SIZE["small"], fill=c["text3"]))
    o.append("</svg>")
    return "".join(o)


def main() -> None:
    for theme in ("dark", "light"):
        s = build(theme)
        path = f"../assets/chess-{theme}.svg"
        open(path, "w", encoding="utf-8").write(s)
        print(f"{path}: {len(s.encode()) / 1024:6.1f} KB   loop {LOOP:.1f}s")


if __name__ == "__main__":
    main()
