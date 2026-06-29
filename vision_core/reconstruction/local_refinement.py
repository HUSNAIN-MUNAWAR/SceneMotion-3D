import numpy as np


def lightweight_local_refinement(points: np.ndarray) -> dict:
    """Educational placeholder-safe refinement.

    This removes extreme outliers based on median absolute deviation. It is not full bundle adjustment.
    """
    points = np.asarray(points, dtype=float).reshape(-1, 3)
    if len(points) < 10:
        return {"points": points, "note": "Too few points for refinement; returned unchanged.", "method": "none"}
    med = np.median(points, axis=0)
    dist = np.linalg.norm(points - med, axis=1)
    mad = np.median(np.abs(dist - np.median(dist))) + 1e-9
    keep = dist < np.median(dist) + 4.0 * mad
    return {"points": points[keep], "removed": int((~keep).sum()), "method": "mad_outlier_filter", "note": "Educational local cleanup, not full bundle adjustment."}
