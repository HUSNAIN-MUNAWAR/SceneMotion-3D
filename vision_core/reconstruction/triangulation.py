import cv2
import numpy as np


def triangulate_pair(kp1: np.ndarray, kp2: np.ndarray, matches_arr: np.ndarray, K: np.ndarray, R: np.ndarray, t: np.ndarray) -> np.ndarray:
    if matches_arr.size == 0 or len(matches_arr) < 2:
        return np.empty((0, 3), dtype=np.float64)
    idx1 = matches_arr[:, 0].astype(int)
    idx2 = matches_arr[:, 1].astype(int)
    pts1 = kp1[idx1].T
    pts2 = kp2[idx2].T
    P1 = K @ np.hstack([np.eye(3), np.zeros((3, 1))])
    def _triangulate(tvec):
        P2 = K @ np.hstack([R, tvec.reshape(3, 1)])
        pts4 = cv2.triangulatePoints(P1, P2, pts1, pts2)
        denom = pts4[3:].copy()
        denom[np.abs(denom) < 1e-9] = 1e-9
        pts3 = (pts4[:3] / denom).T
        finite = np.isfinite(pts3).all(axis=1)
        bounded = np.linalg.norm(pts3, axis=1) < 1e5
        front = pts3[:, 2] > 0
        return pts3[finite & bounded & front]

    pts_pos = _triangulate(t.reshape(3, 1))
    pts_neg = _triangulate(-t.reshape(3, 1))
    return pts_pos if len(pts_pos) >= len(pts_neg) else pts_neg
