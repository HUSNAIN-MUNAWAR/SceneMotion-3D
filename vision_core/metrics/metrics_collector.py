from pathlib import Path
import json
import numpy as np


def collect_warnings(metrics: dict) -> list[str]:
    warnings = []
    if metrics.get("selected_keyframes", 0) < 2:
        warnings.append("Too few keyframes for reliable visual odometry.")
    if metrics.get("average_keypoints_per_keyframe", 0) < 80:
        warnings.append("Low feature count; low texture, blur, or poor lighting may affect results.")
    if metrics.get("average_matches_per_pair", 0) < 20:
        warnings.append("Low match count; trajectory and triangulation may be weak.")
    if metrics.get("average_inlier_ratio", 0) < 0.25:
        warnings.append("Low inlier ratio; repeated patterns or moving objects may be present.")
    if metrics.get("mean_reprojection_error", 0) > 5:
        warnings.append("High reprojection error; camera intrinsics or pose estimates may be inaccurate.")
    if metrics.get("intrinsics_source") == "estimated":
        warnings.append("Camera intrinsics are approximate. Use calibration JSON for better geometry.")
    warnings.append("Monocular trajectory uses relative scale only unless external scale is provided.")
    return sorted(set(warnings))


def save_metrics(metrics: dict, output_path: str | Path) -> dict:
    metrics = dict(metrics)
    metrics["warnings"] = collect_warnings(metrics)
    Path(output_path).write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics
