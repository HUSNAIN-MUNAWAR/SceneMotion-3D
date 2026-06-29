from __future__ import annotations
import time
import numpy as np
from scipy.optimize import least_squares
from .ba_residuals import pack_params, reprojection_residuals, unpack_params


def optimize_sliding_window(poses, points3d, observations, K, max_iterations: int = 20, robust_loss: str = 'soft_l1', time_limit_s: float = 5.0) -> dict:
    points = np.asarray(points3d, dtype=float).reshape(-1,3)
    if len(poses) < 2 or len(points) < 3 or len(observations) < 6:
        return {"optimization_success": False, "reason": "Too little data for sliding-window BA", "points": points, "poses": poses, "reprojection_error_before": None, "reprojection_error_after": None}
    x0 = pack_params(poses, points, fix_first_pose=True)
    start = time.perf_counter()
    before_res = reprojection_residuals(x0, poses, observations, K, len(points), True)
    before = float(np.sqrt(np.mean(before_res**2))) if len(before_res) else 0.0
    try:
        res = least_squares(lambda x: reprojection_residuals(x, poses, observations, K, len(points), True), x0, loss=robust_loss, max_nfev=max_iterations, xtol=1e-6, ftol=1e-6, gtol=1e-6)
        if time.perf_counter() - start > time_limit_s:
            return {"optimization_success": False, "reason": "Optimization exceeded soft time limit", "points": points, "poses": poses, "reprojection_error_before": before, "reprojection_error_after": before}
        opt_poses, opt_points = unpack_params(res.x, poses, len(points), True)
        after_res = reprojection_residuals(res.x, poses, observations, K, len(points), True)
        after = float(np.sqrt(np.mean(after_res**2))) if len(after_res) else before
        imp = 0.0 if before <= 1e-12 else max(0.0, (before - after) / before * 100.0)
        return {"optimization_success": bool(res.success), "optimization_iterations": int(res.nfev), "reprojection_error_before": before, "reprojection_error_after": after, "improvement_percent": float(imp), "points": opt_points, "poses": opt_poses, "reason": res.message}
    except Exception as exc:
        return {"optimization_success": False, "reason": str(exc), "points": points, "poses": poses, "reprojection_error_before": before, "reprojection_error_after": before}
