import numpy as np
import cv2
from vision_core.reconstruction.sliding_window_ba import optimize_sliding_window
from vision_core.reconstruction.ba_residuals import project_points


def test_sliding_window_ba_synthetic_runs():
    K = np.array([[400,0,160],[0,400,120],[0,0,1]], dtype=float)
    poses = [(np.eye(3), np.zeros(3)), (np.eye(3), np.array([0.15,0,0]))]
    pts = np.array([[x, y, 4.0 + 0.2*x] for x in [-0.5,0,0.5] for y in [-0.2,0.2]], dtype=float)
    obs = []
    for ci, (R,t) in enumerate(poses):
        rvec,_ = cv2.Rodrigues(R)
        proj = project_points(pts, rvec, t, K)
        for pi, (x,y) in enumerate(proj):
            obs.append((ci, pi, float(x), float(y)))
    noisy = pts + np.random.default_rng(1).normal(0, 0.01, pts.shape)
    result = optimize_sliding_window(poses, noisy, obs, K, max_iterations=8)
    assert 'reprojection_error_before' in result
    assert result['reprojection_error_after'] is not None
