from pathlib import Path
import json
import cv2
import numpy as np
from .essential_matrix import estimate_essential
from .quality_checks import evaluate_pose_pair


def recover_pose_from_matches(kp1: np.ndarray, kp2: np.ndarray, matches_arr: np.ndarray, K: np.ndarray, min_inlier_ratio: float = 0.2) -> dict:
    if matches_arr.size == 0 or len(matches_arr) < 8:
        return {"status": "rejected", "reason": "too_few_matches", "match_count": int(len(matches_arr))}
    idx1 = matches_arr[:, 0].astype(int)
    idx2 = matches_arr[:, 1].astype(int)
    pts1 = kp1[idx1]
    pts2 = kp2[idx2]
    E, mask, status = estimate_essential(pts1, pts2, K)
    if status != "ok":
        return {"status": "rejected", "reason": status, "match_count": int(len(matches_arr))}
    inlier_ratio = float(mask.mean()) if len(mask) else 0.0
    try:
        retval, R, t, pose_mask = cv2.recoverPose(E, pts1, pts2, K, mask=mask.astype(np.uint8))
    except cv2.error as exc:
        return {"status": "rejected", "reason": f"recover_pose_failed:{exc}", "match_count": int(len(matches_arr)), "inlier_ratio": inlier_ratio}
    translation_norm = float(np.linalg.norm(t))
    warnings = evaluate_pose_pair(int(len(matches_arr)), inlier_ratio, translation_norm, min_inlier_ratio=min_inlier_ratio)
    if "low_match_count" in warnings or "low_inlier_ratio" in warnings:
        return {"status": "rejected", "reason": ",".join(warnings), "match_count": int(len(matches_arr)), "inlier_ratio": inlier_ratio}
    return {"status": "ok", "R": R.tolist(), "t": t.ravel().tolist(), "match_count": int(len(matches_arr)), "inlier_ratio": inlier_ratio, "warnings": warnings, "pose_inliers": int(retval)}


def estimate_relative_poses(match_dir: str | Path, pair_count: int, K: np.ndarray, min_inlier_ratio: float = 0.2) -> dict:
    match_dir = Path(match_dir)
    results = []
    valid = []
    rejected = []
    for i in range(pair_count):
        p = match_dir / f"pair_{i:04d}_{i+1:04d}.npz"
        if not p.exists():
            continue
        data = np.load(p)
        res = recover_pose_from_matches(data["kp1"], data["kp2"], data["matches"], K, min_inlier_ratio=min_inlier_ratio)
        res["pair"] = [i, i + 1]
        results.append(res)
        if res["status"] == "ok":
            valid.append(res)
        else:
            rejected.append(res)
    payload = {"pairs": results, "valid": valid, "rejected": rejected, "valid_count": len(valid), "rejected_count": len(rejected)}
    (match_dir / "pose_pairs.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload
