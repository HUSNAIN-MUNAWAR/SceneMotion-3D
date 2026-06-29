from __future__ import annotations
import numpy as np


def relative_pose_error(aligned_est: np.ndarray, gt: np.ndarray, delta: int = 1) -> dict:
    est = np.asarray(aligned_est, dtype=float).reshape(-1,3)
    gt = np.asarray(gt, dtype=float).reshape(-1,3)
    n = min(len(est), len(gt))
    if n <= delta:
        return {"count": 0, "rmse": None, "mean": None, "median": None, "max": None, "errors": []}
    e_rel = est[delta:n] - est[:n-delta]
    g_rel = gt[delta:n] - gt[:n-delta]
    errors = np.linalg.norm(e_rel - g_rel, axis=1)
    return {"count": int(len(errors)), "delta": int(delta), "rmse": float(np.sqrt(np.mean(errors**2))), "mean": float(errors.mean()), "median": float(np.median(errors)), "max": float(errors.max()), "errors": errors.tolist()}
