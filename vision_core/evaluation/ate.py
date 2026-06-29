from __future__ import annotations
import numpy as np


def absolute_trajectory_error(aligned_est: np.ndarray, gt: np.ndarray) -> dict:
    est = np.asarray(aligned_est, dtype=float).reshape(-1,3)
    gt = np.asarray(gt, dtype=float).reshape(-1,3)
    n = min(len(est), len(gt))
    if n == 0:
        return {"count": 0, "rmse": None, "mean": None, "median": None, "max": None, "errors": []}
    errors = np.linalg.norm(est[:n] - gt[:n], axis=1)
    return {"count": int(n), "rmse": float(np.sqrt(np.mean(errors**2))), "mean": float(errors.mean()), "median": float(np.median(errors)), "max": float(errors.max()), "errors": errors.tolist()}
