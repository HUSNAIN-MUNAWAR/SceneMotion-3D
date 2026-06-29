from pathlib import Path
import json
import cv2
import numpy as np


def laplacian_variance(gray: np.ndarray) -> float:
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())


def _hist_similarity(gray_a: np.ndarray, gray_b: np.ndarray) -> float:
    ha = cv2.calcHist([gray_a], [0], None, [32], [0, 256])
    hb = cv2.calcHist([gray_b], [0], None, [32], [0, 256])
    cv2.normalize(ha, ha)
    cv2.normalize(hb, hb)
    return float(cv2.compareHist(ha, hb, cv2.HISTCMP_CORREL))


def select_keyframes(frame_paths: list[str], output_dir: str | Path, interval: int = 2, max_keyframes: int = 20, min_sharpness: float = 20.0, duplicate_threshold: float = 0.985, min_motion_delta: float = 2.0) -> dict:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    selected = []
    stats = []
    prev_gray = None
    for i, fp in enumerate(frame_paths):
        if i % max(1, interval) != 0:
            continue
        img = cv2.imread(fp)
        if img is None:
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        sharpness = laplacian_variance(gray)
        duplicate_score = _hist_similarity(gray, prev_gray) if prev_gray is not None else 0.0
        motion_delta = float(cv2.absdiff(gray, prev_gray).mean()) if prev_gray is not None else 999.0
        accepted = sharpness >= min_sharpness and (duplicate_score < duplicate_threshold or motion_delta >= min_motion_delta)
        if accepted:
            out = output_dir / f"keyframe_{len(selected):04d}.jpg"
            cv2.imwrite(str(out), img)
            selected.append(str(out))
            prev_gray = gray
        stats.append({"frame": fp, "sharpness": sharpness, "duplicate_score": duplicate_score, "motion_delta": motion_delta, "accepted": accepted})
        if len(selected) >= max_keyframes:
            break
    if not selected and frame_paths:
        img = cv2.imread(frame_paths[0])
        if img is not None:
            out = output_dir / "keyframe_0000.jpg"
            cv2.imwrite(str(out), img)
            selected.append(str(out))
            stats.append({"frame": frame_paths[0], "sharpness": 0.0, "duplicate_score": 0.0, "accepted": True, "fallback": True})
    meta = {"keyframe_paths": selected, "count": len(selected), "stats": stats}
    (output_dir / "metadata.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta
