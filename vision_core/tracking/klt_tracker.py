import cv2
import numpy as np


def track_klt_points(image_a, image_b, max_corners: int = 500) -> dict:
    a = cv2.imread(str(image_a), cv2.IMREAD_GRAYSCALE) if not hasattr(image_a, 'shape') else image_a
    b = cv2.imread(str(image_b), cv2.IMREAD_GRAYSCALE) if not hasattr(image_b, 'shape') else image_b
    if a is None or b is None:
        return {"tracked_count": 0, "points_a": [], "points_b": []}
    pts = cv2.goodFeaturesToTrack(a, maxCorners=max_corners, qualityLevel=0.01, minDistance=7)
    if pts is None:
        return {"tracked_count": 0, "points_a": [], "points_b": []}
    p2, st, err = cv2.calcOpticalFlowPyrLK(a, b, pts, None)
    good = st.ravel() == 1
    pa = pts[good].reshape(-1,2); pb = p2[good].reshape(-1,2)
    return {"tracked_count": int(len(pa)), "points_a": pa.tolist(), "points_b": pb.tolist(), "mean_error": float(np.mean(err[good])) if err is not None and good.any() else None}
