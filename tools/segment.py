"""Subject/background segmentation for the banner portrait.

The naive approach — threshold on luminance — cannot work on this source. Measured
tones: ceiling 61-81, shirt 90-99, face 127-135, and a bright background patch at 136.
The shirt is *brighter* than the ceiling it sits against, so any global threshold either
eats the shoulders or keeps half the ceiling.

What does work is a gradient-gated flood fill from the border. Background is whatever
the border can reach without crossing a strong edge; the silhouette is a strong edge
everywhere it matters (warm face against cool ceiling, hair against ceiling, shoulder
line against ceiling). Then the usual cleanup: closing, fill holes, largest component.

Writes mask.npy plus diagnostic PNGs so the mask can be checked by eye and by number.
"""
from __future__ import annotations

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

SRC = "portrait_src.png"


def gradient_magnitude(rgb: np.ndarray) -> np.ndarray:
    """Per-channel Sobel, combined. Colour edges matter here, not just luminance ones:
    the face/ceiling boundary is mostly a hue step, and a luma-only gradient misses it."""
    g = np.zeros(rgb.shape[:2], dtype=np.float32)
    for c in range(3):
        ch = ndimage.gaussian_filter(rgb[:, :, c], 1.4)
        gx = ndimage.sobel(ch, axis=1)
        gy = ndimage.sobel(ch, axis=0)
        g = np.maximum(g, np.hypot(gx, gy))
    return g


def border_seeds(h: int, w: int) -> np.ndarray:
    """Background seeds. The shoulders run off the left, right and bottom edges, so only
    the upper part of the side borders is safe to call background."""
    s = np.zeros((h, w), dtype=bool)
    s[0:2, :] = True                      # top edge: always ceiling
    s[0:int(0.60 * h), 0:2] = True        # left edge, above the shoulder
    s[0:int(0.58 * h), w - 2:w] = True    # right edge, above the shoulder
    return s


def flood(passable: np.ndarray, seeds: np.ndarray) -> np.ndarray:
    """Connected component of `passable` that touches `seeds`."""
    lab, n = ndimage.label(passable)
    if n == 0:
        return np.zeros_like(passable)
    hit = np.unique(lab[seeds & passable])
    hit = hit[hit > 0]
    return np.isin(lab, hit)


def build_mask(rgb: np.ndarray, grad_pct: float = 62.0) -> tuple[np.ndarray, dict]:
    h, w = rgb.shape[:2]
    grad = gradient_magnitude(rgb)
    thresh = np.percentile(grad, grad_pct)
    passable = grad < thresh

    seeds = border_seeds(h, w)
    # A seed pixel sitting on an edge would block its own flood; force seeds passable.
    passable = passable | seeds

    bg = flood(passable, seeds)

    # The flood stops at the silhouette but leaves a one-pixel rind of edge pixels
    # unassigned on the background side. Dilate the background back into them.
    bg = ndimage.binary_dilation(bg, iterations=2)

    subject = ~bg
    subject = ndimage.binary_closing(subject, structure=np.ones((7, 7)))
    subject = ndimage.binary_fill_holes(subject)

    lab, n = ndimage.label(subject)
    if n > 1:
        sizes = ndimage.sum(subject, lab, range(1, n + 1))
        subject = lab == (int(np.argmax(sizes)) + 1)

    subject = ndimage.binary_opening(subject, structure=np.ones((5, 5)))
    subject = ndimage.binary_fill_holes(subject)

    stats = {
        "grad_thresh": float(thresh),
        "coverage": float(subject.mean()),
        "components": int(n),
    }
    return subject, stats


def main() -> None:
    im = Image.open(SRC).convert("RGB")
    rgb = np.asarray(im).astype(np.float32)
    mask, stats = build_mask(rgb)
    print("mask stats:", {k: round(v, 4) if isinstance(v, float) else v for k, v in stats.items()})

    np.save("mask.npy", mask)

    # Diagnostic: subject tinted, background dimmed, so leaks are obvious.
    over = rgb.copy()
    over[~mask] *= 0.22
    over[~mask, 2] += 40
    Image.fromarray(np.clip(over, 0, 255).astype(np.uint8)).save("diag_mask.png")
    Image.fromarray((mask * 255).astype(np.uint8)).save("diag_mask_bw.png")

    # Row coverage profile — a leak into the ceiling shows up as a row jumping to ~1.0
    prof = mask.mean(axis=1)
    print("row coverage (every 8%):",
          [round(float(prof[int(f * len(prof))]), 2) for f in np.arange(0, 1.0, 0.08)])


if __name__ == "__main__":
    main()
