from pathlib import Path
import json
from .blur import is_blurry
from .parallax import insufficient_parallax
from .dynamic_scene import dynamic_scene_warning


def evaluate_frame_pair(image_a, image_b, match_metrics: dict | None = None, config: dict | None = None) -> dict:
    config = config or {}; match_metrics = match_metrics or {}
    reasons = []
    ba = is_blurry(image_a, float(config.get('blur_threshold', 45.0))); bb = is_blurry(image_b, float(config.get('blur_threshold', 45.0)))
    if ba['is_blurry'] or bb['is_blurry']: reasons.append('blur')
    par = insufficient_parallax(image_a, image_b, float(config.get('min_parallax_px', 1.2)))
    if par['insufficient_parallax']: reasons.append('low_parallax')
    dyn = dynamic_scene_warning(image_a, image_b, float(config.get('high_motion_px', 100.0)))
    if dyn['dynamic_warning']: reasons.append('dynamic_scene_or_excessive_motion')
    if match_metrics.get('filtered_matches', 99) < int(config.get('min_matches', 20)): reasons.append('low_matches')
    if match_metrics.get('inlier_ratio', 1.0) < float(config.get('min_inlier_ratio', 0.12)): reasons.append('low_inlier_ratio')
    return {"accepted": len(reasons) == 0, "reasons": reasons, "blur_a": ba, "blur_b": bb, "parallax": par, "dynamic": dyn, "match_metrics": match_metrics}


def evaluate_sequence_pairs(keyframe_paths: list[str], pair_metrics: list[dict], output_path: str | Path) -> dict:
    reports = []
    for i in range(max(0, len(keyframe_paths)-1)):
        mm = pair_metrics[i] if i < len(pair_metrics) else {}
        reports.append({"pair": [i, i+1], **evaluate_frame_pair(keyframe_paths[i], keyframe_paths[i+1], mm)})
    counts = {"rejected_pairs_total": sum(not r['accepted'] for r in reports), "rejected_blur": sum('blur' in r['reasons'] for r in reports), "rejected_low_parallax": sum('low_parallax' in r['reasons'] for r in reports), "rejected_low_matches": sum('low_matches' in r['reasons'] for r in reports), "rejected_dynamic_scene": sum('dynamic_scene_or_excessive_motion' in r['reasons'] for r in reports), "rejected_degenerate_motion": sum('low_inlier_ratio' in r['reasons'] for r in reports)}
    payload = {"pairs": reports, **counts}
    p = Path(output_path); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(payload, indent=2), encoding='utf-8')
    return payload
