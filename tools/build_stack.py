"""assets/stack-{dark,light}.svg - the stack, by layer.

The banner already carries a flat row of technology chips. This one exists because the
useful question is not "what does he know" but "what goes where", so the columns are the
layers of a system and the order inside each is the order you would meet them.

Content is unchanged from the hand-written version this replaces; only the typesetting
and the surface treatment are new, so it stops being the one panel still wearing the
old flat style.
"""
from __future__ import annotations

import design as D
import fonts
from design import SIZE, T, w

W, H = 1180, 268
PAD = 44

COLUMNS = [
    ("LANGUAGES", "violet", [
        "Python", "TypeScript", "JavaScript", "SQL · Cypher", "Bash"]),
    ("DATA & GRAPH", "cyan", [
        "HydraDB", "PostgreSQL", "pgvector", "SQLite · WAL", "Redis · Prisma"]),
    ("AI & AGENTS", "amber", [
        "Claude API", "MCP servers", "Ollama · local LLM", "Whisper · TTS",
        "Embeddings · RAG"]),
    ("INTERFACE", "green", [
        "React 19", "Next.js 16", "Electron", "Tailwind v4", "Vanilla JS, no build"]),
    ("INFRASTRUCTURE", "rose", [
        "Docker · Compose", "FastAPI", "Render · Vercel", "Supabase", "GitHub Actions"]),
]


def build(theme: str) -> str:
    c = D.THEMES[theme]
    strings = "".join(t + "".join(items) for t, _, items in COLUMNS)
    css, _ = fonts.embed_faces(fonts.charset(
        strings + "THE STACKwhat goes where·"))

    o = [D.svg_open(W, H, "The stack, by layer",
                    "Five columns - languages, data and graph, AI and agents, interface, "
                    "infrastructure - each listing what Rohit ships with at that layer.",
                    css),
         D.defs(c), D.page(W, H, c)]

    o.append(D.eyebrow(PAD, 46, "THE STACK", c))
    o.append(T(W - PAD, 46, "what goes where", size=SIZE["micro"], fill=c["text3"],
               anchor="end"))
    o.append(D.dot_rule(PAD, 64, W - PAD * 2, c))

    colw = (W - PAD * 2) / len(COLUMNS)
    for i, (title, key, items) in enumerate(COLUMNS):
        x = PAD + i * colw
        if i:
            o.append(f'<rect x="{x - 18:.1f}" y="92" width="1" height="{H - 92 - 44}"'
                     f' fill="{c["line"]}"/>')
        o.append(f'<circle cx="{x + 4:.1f}" cy="{104:.1f}" r="3.5" fill="{c[key]}"/>')
        o.append(T(x + 16, 108, title, size=SIZE["tiny"], weight=700, fill=c["text3"],
                   track=0.14))
        for j, item in enumerate(items):
            o.append(T(x, 142 + j * 26, item, size=SIZE["small"], mono=True,
                       fill=c["text2"]))

    o.append("</svg>")
    return "".join(o)


def main() -> None:
    for theme in ("dark", "light"):
        s = build(theme)
        p = f"../assets/stack-{theme}.svg"
        open(p, "w", encoding="utf-8").write(s)
        print(f"{p}: {len(s.encode()) / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
