"""Measurements on the generated banner. Numbers, not impressions.

Two of these exist because the corresponding failure is invisible in a still frame and
easy to talk yourself out of in motion:

  evenness   whether the intro's 60 groups are each scattered over the whole portrait.
             If they are grouped spatially the portrait reveals patch by patch instead
             of shimmering in, which reads as a wipe.
  straight   whether the 94 drift bands accidentally form a square lattice. Drift is an
             affine function of position, so quantising it without added noise
             reproduces a grid exactly, and the dissolve turns blocky.

Both are reported next to a deliberately-broken control, so the number means something.
"""
from __future__ import annotations

import re
import numpy as np
from scipy import ndimage

import build_banner as B


def evenness(pts: np.ndarray, gid: np.ndarray, groups: int, k: int = 4) -> float:
    """Mean total-variation distance between each group's spatial histogram and the
    whole portrait's. 0 = every group mirrors the portrait; 1 = groups are disjoint
    regions."""
    x0, y0 = pts.min(0)
    x1, y1 = pts.max(0) + 1
    cx = np.clip(((pts[:, 0] - x0) / (x1 - x0) * k).astype(int), 0, k - 1)
    cy = np.clip(((pts[:, 1] - y0) / (y1 - y0) * k).astype(int), 0, k - 1)
    cell = cy * k + cx
    q = np.bincount(cell, minlength=k * k).astype(float)
    q /= q.sum()
    tv = []
    for g in range(groups):
        sel = gid == g
        if not sel.any():
            continue
        p = np.bincount(cell[sel], minlength=k * k).astype(float)
        p /= p.sum()
        tv.append(0.5 * np.abs(p - q).sum())
    return float(np.mean(tv))


def straightness(pts: np.ndarray, band: np.ndarray, shape=(340, 300),
                 radius: float = 6.0, flat: float = 0.02) -> float:
    """Fraction of band-boundary cells whose local neighbourhood is collinear.

    Orientation-agnostic on purpose. An earlier version of this only counted
    axis-aligned runs, which made a perfectly straight *diagonal* stripe boundary score
    near zero - it reported the zero-noise control as more organic than the real thing.
    Here each boundary cell's neighbours within `radius` get a PCA: if the smaller
    eigenvalue is under `flat` of the larger, the boundary is locally a straight line."""
    from scipy.spatial import cKDTree

    lab = np.full(shape, -1, dtype=int)
    lab[pts[:, 1].astype(int), pts[:, 0].astype(int)] = band
    idx = ndimage.distance_transform_edt(lab < 0, return_distances=False, return_indices=True)
    lab = lab[idx[0], idx[1]]

    b = np.zeros(shape, dtype=bool)
    dv = lab[:, :-1] != lab[:, 1:]
    dh = lab[:-1, :] != lab[1:, :]
    b[:, :-1] |= dv
    b[:, 1:] |= dv
    b[:-1, :] |= dh
    b[1:, :] |= dh

    ys, xs = np.nonzero(b)
    if len(ys) == 0:
        return 0.0
    P = np.stack([xs, ys], 1).astype(float)
    tree = cKDTree(P)
    straight = 0
    for nb in tree.query_ball_point(P, radius):
        if len(nb) < 6:
            continue
        Q = P[nb] - P[nb].mean(0)
        w = np.linalg.eigvalsh(Q.T @ Q / len(nb))
        if w[1] > 1e-9 and w[0] / w[1] < flat:
            straight += 1
    return straight / len(P)


def check_svg(path: str) -> dict:
    src = open(path, encoding="utf-8").read()
    texts = re.findall(r"<text\b[^>]*>", src)
    unlocked = [t for t in texts if "textLength=" not in t or "lengthAdjust=" not in t]
    kts = set(re.findall(r'keyTimes="([^"]+)"', src))
    loop_kt = [k for k in kts if k.count(";") == 4]
    even = None
    if loop_kt:
        v = [float(x) for x in sorted(loop_kt, key=len)[0].split(";")]
        gaps = np.diff(v)
        even = bool(np.allclose(gaps, gaps[0], atol=1e-3))
    return dict(
        kb=round(len(src.encode()) / 1024, 1),
        texts=len(texts),
        texts_unlocked=len(unlocked),
        crisp_layers=src.count('shape-rendering="crispEdges"'),
        font_glyph_dots=len(re.findall(r"<text[^>]*>[#@*.o]+</text>", src)),
        keytimes_evenly_spaced=even,
        animate_count=src.count("<animate") ,
    )


def main() -> None:
    logo = np.load("logo_rm.npy")
    ly, lx = np.nonzero(logo)
    logo_pts = np.stack([lx, ly], 1).astype(np.float64)

    for theme in ("dark", "light"):
        dots = np.load(f"portrait_{theme}.npy")
        ys, xs = np.nonzero(dots)
        pts = np.stack([xs, ys], 1)
        gid = np.load(f"_gid_{theme}.npy")
        band = np.load(f"_band_{theme}.npy")

        # controls
        spatial_gid = np.zeros(len(pts), int)
        spatial_gid[np.lexsort((pts[:, 0], pts[:, 1]))] = \
            np.arange(len(pts)) * B.INTRO_GROUPS // len(pts)

        saved = B.DRIFT_NOISE
        B.DRIFT_NOISE = 0.0
        grid_band, _ = B.drift_bands(pts.astype(float), logo_pts, seed=99)
        B.DRIFT_NOISE = saved

        e_ok = evenness(pts, gid, B.INTRO_GROUPS)
        e_bad = evenness(pts, spatial_gid, B.INTRO_GROUPS)
        s_ok = straightness(pts, band)
        s_bad = straightness(pts, grid_band)

        print(f"\n=== {theme} ===")
        print(f"  dots {int(dots.sum())}   ink/subject {dots.sum() / np.load('portrait_mask.npy').sum():.3f}")
        print(f"  intro evenness   {e_ok:.3f}   (spatial-grouping control {e_bad:.3f})  lower is better")
        print(f"  band straightness{s_ok:9.3f}   (zero-noise control      {s_bad:.3f})  lower is better")
        for k, v in check_svg(f"../assets/banner-{theme}.svg").items():
            print(f"  {k:<24} {v}")


if __name__ == "__main__":
    main()
