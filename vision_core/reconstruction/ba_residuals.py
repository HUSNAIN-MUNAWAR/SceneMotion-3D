from __future__ import annotations
import numpy as np
import cv2


def project_points(points3d, rvec, tvec, K):
    pts2d, _ = cv2.projectPoints(np.asarray(points3d, dtype=float), np.asarray(rvec, dtype=float).reshape(3,1), np.asarray(tvec, dtype=float).reshape(3,1), np.asarray(K, dtype=float), None)
    return pts2d.reshape(-1, 2)


def pack_params(poses, points, fix_first_pose=True):
    params = []
    start = 1 if fix_first_pose else 0
    for R, t in poses[start:]:
        rvec, _ = cv2.Rodrigues(np.asarray(R, dtype=float))
        params.extend(rvec.ravel().tolist()); params.extend(np.asarray(t, dtype=float).reshape(3).tolist())
    params.extend(np.asarray(points, dtype=float).reshape(-1).tolist())
    return np.asarray(params, dtype=float)


def unpack_params(params, poses_template, point_count, fix_first_pose=True):
    params = np.asarray(params, dtype=float)
    poses = [(np.asarray(R, dtype=float).copy(), np.asarray(t, dtype=float).reshape(3).copy()) for R,t in poses_template]
    idx = 0; start = 1 if fix_first_pose else 0
    for pi in range(start, len(poses)):
        rvec = params[idx:idx+3]; t = params[idx+3:idx+6]; idx += 6
        R, _ = cv2.Rodrigues(rvec.reshape(3,1)); poses[pi] = (R, t)
    points = params[idx:idx+point_count*3].reshape(point_count, 3)
    return poses, points


def reprojection_residuals(params, poses_template, observations, K, point_count, fix_first_pose=True):
    poses, points = unpack_params(params, poses_template, point_count, fix_first_pose)
    residuals = []
    for cam_idx, point_idx, x, y in observations:
        R, t = poses[int(cam_idx)]
        rvec, _ = cv2.Rodrigues(R)
        pred = project_points(points[int(point_idx):int(point_idx)+1], rvec, t, K)[0]
        residuals.extend((pred - np.array([x, y])).tolist())
    return np.asarray(residuals, dtype=float)
