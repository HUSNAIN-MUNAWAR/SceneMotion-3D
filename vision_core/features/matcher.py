from pathlib import Path
import json
import cv2
import numpy as np


def load_feature_npz(path: str | Path):
    data = np.load(path, allow_pickle=True)
    return data["keypoints"].astype(np.float32), data["descriptors"], str(data.get("method", "ORB"))


def match_descriptors(desc1, desc2, method: str = "ORB", ratio: float = 0.75, cross_check: bool = False):
    if desc1 is None or desc2 is None or len(desc1) == 0 or len(desc2) == 0:
        return []
    norm = cv2.NORM_HAMMING if method.upper() in {"ORB", "AKAZE"} else cv2.NORM_L2
    if cross_check:
        matcher = cv2.BFMatcher(norm, crossCheck=True)
        return sorted(matcher.match(desc1, desc2), key=lambda m: m.distance)
    matcher = cv2.BFMatcher(norm, crossCheck=False)
    pairs = matcher.knnMatch(desc1, desc2, k=2)
    good = []
    for pair in pairs:
        if len(pair) < 2:
            continue
        m, n = pair
        if m.distance < ratio * n.distance:
            good.append(m)
    return sorted(good, key=lambda m: m.distance)


def ransac_filter_matches(kp1, kp2, matches, reproj_threshold: float = 3.0):
    if len(matches) < 8:
        return matches, np.ones((len(matches),), dtype=bool), None
    pts1 = np.float32([kp1[m.queryIdx] for m in matches])
    pts2 = np.float32([kp2[m.trainIdx] for m in matches])
    F, mask = cv2.findFundamentalMat(pts1, pts2, cv2.FM_RANSAC, reproj_threshold, 0.99)
    if mask is None:
        return [], np.zeros((len(matches),), dtype=bool), F
    mask = mask.ravel().astype(bool)
    return [m for m, keep in zip(matches, mask) if keep], mask, F


def match_feature_sequence(feature_records: list[dict], keyframe_paths: list[str], output_dir: str | Path, ratio: float = 0.78) -> dict:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    pair_metrics = []
    for i in range(len(feature_records) - 1):
        kp1, desc1, method = load_feature_npz(feature_records[i]["npz"])
        kp2, desc2, _ = load_feature_npz(feature_records[i + 1]["npz"])
        raw = match_descriptors(desc1, desc2, method, ratio=ratio)
        filt, mask, F = ransac_filter_matches(kp1, kp2, raw)
        pair_metrics.append({
            "pair": [i, i + 1],
            "raw_matches": int(len(raw)),
            "filtered_matches": int(len(filt)),
            "inlier_count": int(len(filt)),
            "inlier_ratio": float(len(filt) / max(len(raw), 1)),
        })
        # visualization
        img1 = cv2.imread(keyframe_paths[i]); img2 = cv2.imread(keyframe_paths[i+1])
        if img1 is not None and img2 is not None:
            cv_kp1 = [cv2.KeyPoint(float(x), float(y), 1) for x, y in kp1]
            cv_kp2 = [cv2.KeyPoint(float(x), float(y), 1) for x, y in kp2]
            vis = cv2.drawMatches(img1, cv_kp1, img2, cv_kp2, filt[:80], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            cv2.imwrite(str(output_dir / f"matches_{i:04d}_{i+1:04d}.jpg"), vis)
        np.savez_compressed(output_dir / f"pair_{i:04d}_{i+1:04d}.npz", kp1=kp1, kp2=kp2, matches=np.array([[m.queryIdx, m.trainIdx, m.distance] for m in filt], dtype=np.float32))
    avg_inlier = float(np.mean([m["inlier_ratio"] for m in pair_metrics])) if pair_metrics else 0.0
    avg_matches = float(np.mean([m["filtered_matches"] for m in pair_metrics])) if pair_metrics else 0.0
    payload = {"pairs": pair_metrics, "average_inlier_ratio": avg_inlier, "average_matches": avg_matches}
    (output_dir / "match_metrics.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload
