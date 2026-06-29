import numpy as np

def evaluate_pose_pair(match_count: int, inlier_ratio: float, translation_norm: float, min_matches: int = 20, min_inlier_ratio: float = 0.2) -> list[str]:
    warnings = []
    if match_count < min_matches:
        warnings.append("low_match_count")
    if inlier_ratio < min_inlier_ratio:
        warnings.append("low_inlier_ratio")
    if translation_norm < 1e-6:
        warnings.append("pure_rotation_or_insufficient_parallax")
    return warnings

def trajectory_length(positions: list[list[float]]) -> float:
    if len(positions) < 2:
        return 0.0
    arr = np.asarray(positions, dtype=float)
    return float(np.linalg.norm(np.diff(arr, axis=0), axis=1).sum())
