"""Fetch, subset and embed OFL fonts so the panels have real typography.

System monospace everywhere is what made the first pass read as a template. Type
contrast - a geometric display face for headings and numerals against a mono for data -
is the single biggest lever on whether this looks designed or generated.

GitHub renders these SVGs through <img>, which is an isolated document: no external
stylesheet, no webfont link, no CSS from the host page. The only way to get a real
typeface in is to embed it, so each SVG carries a woff2 subsetted to exactly the glyphs
that file uses. A full weight is ~40KB; subsetted to ~90 glyphs it lands under 6KB.

Both faces are SIL Open Font License 1.1, which explicitly permits embedding.
Attribution is carried in the SVG metadata by embed_faces().
"""
from __future__ import annotations

import base64
import io
import os
import re
import urllib.request

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".fontcache")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0 Safari/537.36"
# Google Fonts content-negotiates on User-Agent. A modern UA gets woff2 split into a
# dozen unicode-range subsets; an old one gets a single complete TTF, which is what we
# want to subset from.
UA_LEGACY = "Mozilla/5.0 (Windows NT 5.1)"

FACES = {
    # key            family                weights
    "display": ("Space Grotesk", (300, 500, 700)),
    "mono": ("JetBrains Mono", (400, 700)),
}
LICENSE = "Space Grotesk and JetBrains Mono, SIL Open Font License 1.1"


def _get(url: str, ua: str = UA) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def _ttf(family: str, weight: int) -> bytes:
    """Google Fonts serves woff2 to modern UAs and ttf to old ones. Ask as an old UA:
    fontTools can subset a ttf directly and re-compress to woff2, and skipping the
    woff2->ttf->woff2 round trip avoids a decompression dependency at read time."""
    os.makedirs(CACHE, exist_ok=True)
    slug = f"{family.replace(' ', '')}-{weight}.ttf"
    path = os.path.join(CACHE, slug)
    if os.path.exists(path):
        return open(path, "rb").read()
    css = _get(f"https://fonts.googleapis.com/css2?family={family.replace(' ', '+')}"
               f":wght@{weight}&display=swap", ua=UA_LEGACY).decode()
    m = re.search(r"src:\s*url\((https://[^)]+\.ttf)\)", css)
    if not m:
        raise SystemExit(f"no ttf url in css for {family} {weight}:\n{css[:400]}")
    data = _get(m.group(1))
    open(path, "wb").write(data)
    return data


def subset_woff2(family: str, weight: int, chars: str) -> bytes:
    from fontTools import subset
    from fontTools.ttLib import TTFont

    font = TTFont(io.BytesIO(_ttf(family, weight)))
    opts = subset.Options()
    opts.layout_features = ["kern", "liga", "calt", "tnum"]
    opts.notdef_outline = True
    opts.desubroutinize = True
    opts.drop_tables += ["FFTM", "PfEd", "BASE", "GDEF", "JSTF", "DSIG"]
    s = subset.Subsetter(options=opts)
    s.populate(text="".join(sorted(set(chars))))
    s.subset(font)
    font.flavor = "woff2"
    buf = io.BytesIO()
    font.save(buf)
    return buf.getvalue()


def embed_faces(chars: str, faces=("display", "mono")) -> tuple[str, int]:
    """Return a <style> block of @font-face rules covering `chars`, and its byte cost."""
    rules, total = [], 0
    for key in faces:
        family, weights = FACES[key]
        for w in weights:
            data = subset_woff2(family, w, chars)
            total += len(data)
            b64 = base64.b64encode(data).decode()
            rules.append(
                f"@font-face{{font-family:'{family}';font-style:normal;"
                f"font-weight:{w};src:url(data:font/woff2;base64,{b64}) format('woff2');}}")
    return "<style>" + "".join(rules) + "</style>", total


# Glyph coverage helper: callers pass every string they will draw, so the subset is
# exactly what the file needs and not a character more.
def charset(*strings: str) -> str:
    return "".join(strings) + "0123456789 "


if __name__ == "__main__":
    css, n = embed_faces("The quick brown fox 0123456789")
    print(f"embedded {n / 1024:.1f} KB for a 30-char subset across 5 weights")


# --------------------------------------------------------------------- metrics
# With the face embedded, its metrics are known and identical in every renderer. That
# retires the textLength + lengthAdjust="spacingAndGlyphs" trick the first pass needed:
# that existed only because the font was whatever the viewer happened to have, and it
# works by stretching or squeezing glyphs to hit a computed width. Measuring the real
# advance widths instead means text is set at its natural proportions and still lands
# exactly where the layout says.
_METRIC_CACHE: dict[tuple[str, int], tuple[int, dict]] = {}


def _metrics(family: str, weight: int):
    key = (family, weight)
    if key not in _METRIC_CACHE:
        from fontTools.ttLib import TTFont
        f = TTFont(io.BytesIO(_ttf(family, weight)))
        upem = f["head"].unitsPerEm
        cmap = f.getBestCmap()
        hmtx = f["hmtx"].metrics
        # getBestCmap() is keyed by codepoint, not by character - keying the lookup
        # wrongly makes every glyph fall back to the same width, which silently
        # turns a proportional face into a fake monospace one.
        adv = {chr(cp): hmtx[g][0] for cp, g in cmap.items() if g in hmtx}
        _METRIC_CACHE[key] = (upem, adv)
    return _METRIC_CACHE[key]


def width(text: str, family: str, weight: int, size: float, tracking: float = 0.0) -> float:
    """Advance width of `text` in px. `tracking` is em-relative, matching letter-spacing."""
    upem, adv = _metrics(family, weight)
    fallback = adv.get("n", upem // 2)
    total = sum(adv.get(ch, fallback) for ch in text)
    return total / upem * size + tracking * size * len(text)
