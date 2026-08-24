"""Shared pieces for the generated panels.

Palette and text helpers live here so every panel on the profile is provably the same
visual language - one place to change a hue, one definition of how text gets locked.

Text is always emitted with textLength + lengthAdjust="spacingAndGlyphs". GitHub renders
these SVGs on machines whose monospace font we cannot predict; without the lock, columns
that line up here drift apart there.
"""
from __future__ import annotations

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "dark": dict(
        bg="#0A101F", panel="#0D1526", panel2="#0B1220",
        chrome="#22D3EE", chrome_dim="#1B4A5C", rule="#16304A",
        portrait="#A78BFA", mark="#10B981", accent="#10B981",
        label="#5FBBD0", value="#C7D2E4", leader="#1E3A4C",
        title="#7C93AD", live="#FF5F56", pill_bg="#132033", pill_tx="#22D3EE",
        dim="#4A5F78", warn="#FBBF24", bad="#FF5F56", good="#10B981",
        grid="#2D3343", violet="#A78BFA",
    ),
    "light": dict(
        bg="#EEF2F8", panel="#FFFFFF", panel2="#F7F9FC",
        chrome="#0891B2", chrome_dim="#A9CFDC", rule="#DCE5EF",
        portrait="#7C3AED", mark="#059669", accent="#059669",
        label="#0E7490", value="#1E293B", leader="#C3D0DE",
        title="#64748B", live="#E11D48", pill_bg="#E6F6FA", pill_tx="#0E7490",
        dim="#94A3B8", warn="#B45309", bad="#E11D48", good="#059669",
        grid="#E2E8F0", violet="#7C3AED",
    ),
}


def ch(size: float) -> float:
    """Advance width of one monospace cell. Only has to be self-consistent, because
    textLength forces the rendered width to match whatever we compute here."""
    return size * 0.6


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size, fill, *, anchor="start", weight=None, opacity=None,
         extra="", lock=True) -> str:
    bits = [f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}"',
            f'font-family="{MONO}" fill="{fill}"']
    if lock and s:
        bits.append(f'textLength="{len(s) * ch(size):.1f}" lengthAdjust="spacingAndGlyphs"')
    if anchor != "start":
        bits.append(f'text-anchor="{anchor}"')
    if weight:
        bits.append(f'font-weight="{weight}"')
    if opacity is not None:
        bits.append(f'opacity="{opacity}"')
    if extra:
        bits.append(extra)
    return " ".join(bits) + f">{esc(s)}</text>"


def window(w: int, h: int, c: dict, title: str, *, titlebar: int = 34) -> tuple[str, str]:
    """Terminal chrome matching the banner: rounded frame, traffic lights, centred title.
    Returns (open_markup, close_markup) so callers fill the body between them."""
    o = [f'<rect width="{w}" height="{h}" rx="11" fill="{c["bg"]}"/>',
         f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="10.5" fill="none"'
         f' stroke="{c["chrome_dim"]}"/>',
         f'<path d="M0 11a11 11 0 0 1 11-11h{w - 22}a11 11 0 0 1 11 11v{titlebar - 11}H0z"'
         f' fill="{c["panel2"]}"/>',
         f'<rect y="{titlebar}" width="{w}" height="1" fill="{c["rule"]}"/>']
    for i, col in enumerate(("#FF5F56", "#FFBD2E", "#27C93F")):
        o.append(f'<circle cx="{22 + i * 19}" cy="{titlebar / 2:.0f}" r="5.5" fill="{col}"/>')
    o.append(text(w / 2, titlebar / 2 + 4.2, title, 12, c["title"], anchor="middle"))
    return "".join(o), ""


def svg_open(w: int, h: int, label: str, desc: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}"'
            f' height="{h}" role="img" aria-label="{esc(label)}">'
            f'<title>{esc(label)}</title><desc>{esc(desc)}</desc>')


def type_clip(cid: str, n: int, cw: float, x: float, y: float, h: float,
              loop: float, t0: float, t1: float) -> str:
    """A clip rect that widens one character at a time - a real typewriter reveal.

    calcMode="discrete" is the point. Interpolating width linearly slides a soft edge
    across the glyphs and reads as a wipe; stepping by exactly one advance width reads
    as typing.

    The animation spans the WHOLE loop rather than just the typing window, so every
    panel element shares one cycle length and they cannot drift apart. Outside
    [t0, t1] the width simply holds - full until the end, then back to zero."""
    vals, kts = ["0"], ["0"]
    for i in range(1, n + 1):
        vals.append(f"{i * cw:.1f}")
        kts.append(f"{(t0 + (t1 - t0) * i / n) / loop:.4f}")
    vals += [f"{n * cw:.1f}", "0"]
    kts += ["0.9990", "1"]
    return (f'<clipPath id="{cid}"><rect x="{x:.1f}" y="{y:.1f}" width="0" height="{h:.1f}">'
            f'<animate attributeName="width" values="{";".join(vals)}"'
            f' keyTimes="{";".join(kts)}" calcMode="discrete" dur="{loop}s"'
            f' repeatCount="indefinite"/></rect></clipPath>')


def reveal(inner: str, loop: float, t_on: float, t_off: float, fade: float = 0.22) -> str:
    """Wrap markup so it fades in at t_on and out at t_off, on the shared loop."""
    k = [0.0, t_on / loop, (t_on + fade) / loop, t_off / loop,
         min((t_off + fade) / loop, 1.0), 1.0]
    k = [min(max(v, 0.0), 1.0) for v in k]
    for i in range(1, len(k)):
        k[i] = max(k[i], k[i - 1])
    kt = ";".join(f"{v:.4f}" for v in k)
    return (f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0;0"'
            f' keyTimes="{kt}" dur="{loop}s" repeatCount="indefinite"/>{inner}</g>')
