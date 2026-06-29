import numpy as np


def project_points(points: np.ndarray, K: np.ndarray, R: np.ndarray, t: np.ndarray) -> np.ndarray:
    if len(points) == 0:
        return np.empty((0, 2))
    X = (R @ points.T + t.reshape(3, 1)).T
    z = np.maximum(X[:, 2:3], 1e-9)
    uvw = (K @ X.T).T
    return uvw[:, :2] / z


def reprojection_error(points: np.ndarray, observed: np.ndarray, K: np.ndarray, R: np.ndarray, t: np.ndarray) -> dict:
    if len(points) == 0 or len(observed) == 0:
        return {"mean": 0.0, "max": 0.0, "count": 0}
    pred = project_points(points, K, R, t)
    n = min(len(pred), len(observed))
    err = np.linalg.norm(pred[:n] - observed[:n], axis=1)
    return {"mean": float(err.mean()) if n else 0.0, "max": float(err.max()) if n else 0.0, "count": int(n)}
