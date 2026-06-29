from __future__ import annotations
import numpy as np


def voxel_downsample(points: np.ndarray, voxel_size: float = 0.05) -> np.ndarray:
    pts = np.asarray(points, dtype=float).reshape(-1,3)
    if len(pts) == 0 or voxel_size <= 0: return pts
    keys = np.floor(pts / voxel_size).astype(np.int64)
    _, idx = np.unique(keys, axis=0, return_index=True)
    return pts[np.sort(idx)]


def remove_statistical_outliers(points: np.ndarray, z_threshold: float = 2.5) -> np.ndarray:
    pts = np.asarray(points, dtype=float).reshape(-1,3)
    if len(pts) < 6: return pts
    center = np.median(pts, axis=0)
    dist = np.linalg.norm(pts - center, axis=1)
    med = np.median(dist); mad = np.median(np.abs(dist - med)) + 1e-9
    z = 0.6745 * (dist - med) / mad
    return pts[np.abs(z) < z_threshold]


def normalize_for_viewer(points: np.ndarray) -> np.ndarray:
    pts = np.asarray(points, dtype=float).reshape(-1,3)
    if len(pts) == 0: return pts
    center = pts.mean(axis=0); scale = np.max(np.linalg.norm(pts-center, axis=1)) + 1e-9
    return (pts - center) / scale
