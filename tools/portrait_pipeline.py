"""Portrait -> dot-grid pipeline. Source of truth for the banner artwork.

Produces, from tools/portrait_src.png:
    portrait_dark.npy    bool 340x300 - dots draw the LIT subject (dark theme)
    portrait_light.npy   bool 340x300 - dots draw the DARK parts   (light theme)
    logo_rm.npy          bool 340x300 - the RM monogram mark

Two deliberate deviations from the master prompt, both forced by this source photo:

1. Segmentation is a traced silhouette, not a colour-distance threshold. Measured tones
   make a threshold impossible: ceiling 61-81, shirt 90-99, face 127-135, and a bright
   background patch at 136. The shirt is BRIGHTER than the ceiling behind it. A
   gradient-gated flood fill was tried first (see segment.py) and ate into the hair
   while still keeping ceiling at the sides, at every parameter setting swept.

2. Light mode masks the background out too. The prompt says light mode keeps the
   background, which is right for a photo shot against a bright wall. This one is shot
   against a dark metal ceiling, so "dots draw the dark parts" would render the ceiling
   as the densest area on the panel - a muddy dark block with a faint face in it. Light
   mode therefore uses the same silhouette and inverts the tone map instead: dark ink on
   an empty panel.
"""
from __future__ import annotations

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from scipy import ndimage

SRC = "portrait_src.png"
GRID_W, GRID_H = 300, 340
TARGET_DOTS = 17000

# Silhouette traced against a 50px coordinate grid over the 600x680 source
# (tools/diag_grid.png). Normalised so it survives a change of source resolution.
_TRACE_REF = (600.0, 680.0)
_TRACE = [
    (200, 10), (175, 40), (150, 75), (125, 110), (105, 145), (92, 185), (88, 215),
    (95, 240), (112, 258), (124, 272), (130, 300), (136, 332), (142, 362), (151, 398),
    (164, 430), (181, 456), (200, 478), (206, 492), (200, 508),
    (176, 534), (140, 556), (96, 581), (46, 606), (0, 630),
    (0, 680), (460, 680), (600, 596),
    (586, 576), (546, 551), (500, 528), (456, 506), (416, 488), (391, 476),
    (378, 464), (372, 448), (369, 438), (378, 418), (390, 394), (400, 364), (408, 330),
    (415, 300), (420, 274),
    (432, 254), (445, 229), (452, 199), (450, 169), (440, 139), (428, 109), (410, 74),
    (385, 44), (350, 20), (310, 7), (260, 4), (215, 9),
]


def silhouette(w: int, h: int) -> np.ndarray:
    sx, sy = w / _TRACE_REF[0], h / _TRACE_REF[1]
    poly = [(x * sx, y * sy) for x, y in _TRACE]
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).polygon(poly, fill=255)
    a = np.asarray(m) > 127
    a = ndimage.binary_closing(a, structure=np.ones((5, 5)))
    a = ndimage.binary_fill_holes(a)
    lab, n = ndimage.label(a)
    if n > 1:
        sizes = ndimage.sum(a, lab, range(1, n + 1))
        a = lab == int(np.argmax(sizes)) + 1
    return a


def tone(img: Image.Image, mask: np.ndarray) -> np.ndarray:
    """Grayscale -> autocontrast(cutoff=1) over the subject only -> 1.3x -> unsharp.

    Autocontrast is computed on the masked region alone. Run over the whole frame it
    would be dominated by background it is about to discard, and the subject would come
    out flat."""
    g = img.convert("L")
    a = np.asarray(g).astype(np.float32)

    sub = a[mask]
    # cutoff=1 on the shadow end. The highlight end is held back to 99.5: this face is
    # evenly lit and a 99 clip drives the cheeks to solid ink, losing all modelling.
    lo, hi = np.percentile(sub, [1.0, 99.5])
    a = np.clip((a - lo) / max(hi - lo, 1e-6), 0, 1) * 255.0

    g = Image.fromarray(a.astype(np.uint8))
    g = ImageEnhance.Contrast(g).enhance(1.3)
    g = g.filter(ImageFilter.UnsharpMask(radius=3, percent=140, threshold=0))
    return np.asarray(g).astype(np.float32) / 255.0


def floyd_steinberg(ink: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """1-bit Floyd-Steinberg, serpentine order, mask-aware.

    Error is never diffused into a cell outside the mask, and error that has nowhere
    left to go is dropped rather than piling up. That is the hard clear at the mask
    edge - without it the silhouette grows a bright fringe of stranded error."""
    h, w = ink.shape
    e = ink.astype(np.float64).copy()
    out = np.zeros((h, w), dtype=bool)
    for y in range(h):
        left_to_right = (y % 2 == 0)
        xs = range(w) if left_to_right else range(w - 1, -1, -1)
        fwd = 1 if left_to_right else -1
        for x in xs:
            if not mask[y, x]:
                e[y, x] = 0.0
                continue
            old = e[y, x]
            new = 1.0 if old >= 0.5 else 0.0
            out[y, x] = new > 0.5
            err = old - new
            for dx, dy, f in ((fwd, 0, 7 / 16), (-fwd, 1, 3 / 16), (0, 1, 5 / 16), (fwd, 1, 1 / 16)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and mask[ny, nx]:
                    e[ny, nx] += err * f
    return out


def dither(ink: np.ndarray, mask: np.ndarray, target: int) -> tuple[np.ndarray, float]:
    """Solve for the gamma that lands the dot count on target, then dither once at it.

    Error diffusion conserves mean ink to within a fraction of a percent, so the total
    of the shaped ink predicts the dot count directly. Thresholding as a proxy instead
    overshoots by ~12% here, because it counts a cell as full or empty when the dither
    will render it as a local density."""
    lo, hi = 0.30, 4.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if (np.clip(ink, 0, 1) ** mid)[mask].sum() > target:
            lo = mid
        else:
            hi = mid
    gamma = (lo + hi) / 2
    return floyd_steinberg(np.clip(ink, 0, 1) ** gamma, mask), gamma


# RM mark geometry, in grid cells on the 300x340 grid. Explicit rather than derived
# from canvas fractions, so the letters provably fit inside the frame.
MARK = dict(frame=(52, 92, 248, 288), radius=26, stroke=5, cap=96)


def build_logo_rm() -> np.ndarray:
    """RM monogram inside a rounded bracket frame, rasterised onto the portrait grid."""
    S = 4  # supersample, then threshold - keeps the letterform edges clean
    W, H = GRID_W * S, GRID_H * S
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)

    x0, y0, x1, y1 = (v * S for v in MARK["frame"])
    d.rounded_rectangle([x0, y0, x1, y1], radius=MARK["radius"] * S,
                        outline=255, width=MARK["stroke"] * S)

    font = None
    for path in (r"C:\Windows\Fonts\ariblk.ttf", r"C:\Windows\Fonts\arialbd.ttf"):
        try:
            font = ImageFont.truetype(path, MARK["cap"] * S)
            break
        except OSError:
            continue
    if font is None:
        raise SystemExit("no heavy sans font found")

    box = d.textbbox((0, 0), "RM", font=font)
    tw, th = box[2] - box[0], box[3] - box[1]
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    d.text((cx - tw / 2 - box[0], cy - th / 2 - box[1]), "RM", fill=255, font=font)

    small = im.resize((GRID_W, GRID_H), Image.LANCZOS)
    return np.asarray(small) > 110


def main() -> None:
    img = Image.open(SRC).convert("RGB")
    full_mask = silhouette(*img.size)

    grid_img = img.resize((GRID_W, GRID_H), Image.LANCZOS)
    mask = np.asarray(Image.fromarray((full_mask * 255).astype(np.uint8))
                      .resize((GRID_W, GRID_H), Image.LANCZOS)) > 127

    lum = tone(grid_img, mask)

    dark, g_dark = dither(lum, mask, TARGET_DOTS)                 # bright -> dot
    light, g_light = dither(1.0 - lum, mask, TARGET_DOTS)         # dark  -> dot
    logo = build_logo_rm()

    np.save("portrait_dark.npy", dark)
    np.save("portrait_light.npy", light)
    np.save("logo_rm.npy", logo)
    np.save("portrait_mask.npy", mask)

    print(f"grid          {GRID_W}x{GRID_H} = {GRID_W * GRID_H} cells")
    print(f"mask coverage {mask.mean():.3f}  ({int(mask.sum())} cells)")
    print(f"dark dots     {int(dark.sum()):6d}  gamma {g_dark:.3f}  ink/subject {dark.sum() / mask.sum():.3f}")
    print(f"light dots    {int(light.sum()):6d}  gamma {g_light:.3f}  ink/subject {light.sum() / mask.sum():.3f}")
    print(f"logo dots     {int(logo.sum()):6d}")

    # Eyeball renders at 3x so the dither can be judged before it reaches the SVG.
    for name, arr, fg, bg in (("diag_dark.png", dark, (167, 139, 250), (10, 16, 31)),
                              ("diag_light.png", light, (124, 58, 237), (255, 255, 255)),
                              ("diag_logo.png", logo, (16, 185, 129), (10, 16, 31))):
        rgb = np.zeros((GRID_H, GRID_W, 3), dtype=np.uint8)
        rgb[:] = bg
        rgb[arr] = fg
        Image.fromarray(rgb).resize((GRID_W * 3, GRID_H * 3), Image.NEAREST).save(name)


if __name__ == "__main__":
    main()
