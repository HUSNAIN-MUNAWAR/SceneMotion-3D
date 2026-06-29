from __future__ import annotations
import cv2
import numpy as np


def verify_loop_pair(image_a: str, image_b: str, min_inliers: int = 30) -> dict:
    a = cv2.imread(image_a, cv2.IMREAD_GRAYSCALE); b = cv2.imread(image_b, cv2.IMREAD_GRAYSCALE)
    if a is None or b is None:
        return {"verified": False, "reason": "image_read_failed", "inliers": 0, "raw_matches": 0}
    orb = cv2.ORB_create(nfeatures=1500)
    k1, d1 = orb.detectAndCompute(a, None); k2, d2 = orb.detectAndCompute(b, None)
    if d1 is None or d2 is None or len(d1) < 8 or len(d2) < 8:
        return {"verified": False, "reason": "too_few_features", "inliers": 0, "raw_matches": 0}
    matches = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).match(d1, d2)
    if len(matches) < 8:
        return {"verified": False, "reason": "too_few_matches", "inliers": 0, "raw_matches": len(matches)}
    pts1 = np.float32([k1[m.queryIdx].pt for m in matches]); pts2 = np.float32([k2[m.trainIdx].pt for m in matches])
    try:
        _, mask = cv2.findFundamentalMat(pts1, pts2, cv2.FM_RANSAC, 3.0, 0.99)
    except cv2.error:
        return {"verified": False, "reason": "fundamental_matrix_failed", "inliers": 0, "raw_matches": len(matches)}
    inliers = int(mask.sum()) if mask is not None else 0
    return {"verified": inliers >= min_inliers, "reason": "ok" if inliers >= min_inliers else "low_geometric_inliers", "inliers": inliers, "raw_matches": len(matches), "inlier_ratio": float(inliers / max(len(matches), 1))}
