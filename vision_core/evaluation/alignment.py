from __future__ import annotations
import numpy as np


def sim3_umeyama(source: np.ndarray, target: np.ndarray, with_scale: bool = True) -> dict:
    """Align source positions to target positions using Umeyama Sim(3)/SE(3).

    This is intended for evaluation only in monocular VO: it does not recover metric scale at runtime.
    """
    X = np.asarray(source, dtype=float).reshape(-1, 3)
    Y = np.asarray(target, dtype=float).reshape(-1, 3)
    if len(X) != len(Y) or len(X) < 3:
        raise ValueError('Need at least three paired 3D points for Sim(3) alignment')
    mu_x = X.mean(axis=0); mu_y = Y.mean(axis=0)
    Xc = X - mu_x; Yc = Y - mu_y
    cov = (Yc.T @ Xc) / len(X)
    U, D, Vt = np.linalg.svd(cov)
    S = np.eye(3)
    if np.linalg.det(U) * np.linalg.det(Vt) < 0:
        S[-1, -1] = -1
    R = U @ S @ Vt
    var_x = np.mean(np.sum(Xc**2, axis=1))
    scale = float(np.trace(np.diag(D) @ S) / max(var_x, 1e-12)) if with_scale else 1.0
    t = mu_y - scale * R @ mu_x
    aligned = (scale * (R @ X.T)).T + t
    return {"scale": scale, "rotation": R, "translation": t, "aligned": aligned, "note": "Sim(3) scale is evaluation-only for monocular VO."}
