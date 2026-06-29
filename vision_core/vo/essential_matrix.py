import cv2
import numpy as np


def estimate_essential(pts1: np.ndarray, pts2: np.ndarray, K: np.ndarray, threshold: float = 1.0):
    if pts1.shape[0] < 8 or pts2.shape[0] < 8:
        return None, np.zeros((pts1.shape[0],), dtype=bool), "too_few_matches"
    E, mask = cv2.findEssentialMat(pts1, pts2, K, method=cv2.RANSAC, prob=0.999, threshold=threshold)
    if E is None or mask is None:
        return None, np.zeros((pts1.shape[0],), dtype=bool), "essential_matrix_failed"
    return E, mask.ravel().astype(bool), "ok"
