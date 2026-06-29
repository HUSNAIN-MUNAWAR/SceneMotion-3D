import cv2
import numpy as np


def estimate_parallax(image_a, image_b) -> dict:
    a = cv2.imread(str(image_a), cv2.IMREAD_GRAYSCALE) if not hasattr(image_a, 'shape') else image_a
    b = cv2.imread(str(image_b), cv2.IMREAD_GRAYSCALE) if not hasattr(image_b, 'shape') else image_b
    if a is None or b is None:
        return {"median_flow": 0.0, "tracked_points": 0}
    pts = cv2.goodFeaturesToTrack(a, maxCorners=300, qualityLevel=0.01, minDistance=8)
    if pts is None or len(pts) < 8:
        return {"median_flow": 0.0, "tracked_points": 0}
    p2, st, _ = cv2.calcOpticalFlowPyrLK(a, b, pts, None)
    good = st.ravel() == 1
    if not good.any():
        return {"median_flow": 0.0, "tracked_points": 0}
    flow = np.linalg.norm(p2[good].reshape(-1,2) - pts[good].reshape(-1,2), axis=1)
    return {"median_flow": float(np.median(flow)), "mean_flow": float(np.mean(flow)), "tracked_points": int(good.sum())}


def insufficient_parallax(image_a, image_b, threshold_px: float = 1.5) -> dict:
    p = estimate_parallax(image_a, image_b)
    return {**p, "insufficient_parallax": p["median_flow"] < threshold_px, "threshold_px": threshold_px}
