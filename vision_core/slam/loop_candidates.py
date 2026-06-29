from __future__ import annotations
from pathlib import Path
import json
from .keyframe_database import KeyframeDatabase
from .geometric_verification import verify_loop_pair


def detect_loop_candidates(keyframe_paths: list[str], output_dir: str | Path, min_gap: int = 4, similarity_threshold: float = 0.78) -> dict:
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    db = KeyframeDatabase(); candidates = []
    for idx, path in enumerate(keyframe_paths):
        for hit in db.query(path, top_k=4):
            if abs(idx - hit['frame_id']) < min_gap or hit['score'] < similarity_threshold:
                continue
            ver = verify_loop_pair(path, hit['image_path'], min_inliers=25)
            candidates.append({"query_frame": idx, "candidate_frame": hit['frame_id'], "similarity": hit['score'], **ver})
        db.add(idx, path)
    payload = {"candidate_count": len(candidates), "verified_count": sum(1 for c in candidates if c.get('verified')), "candidates": candidates, "note": "Lightweight candidate detection only; this is not a full loop-closure SLAM backend."}
    (out / 'loop_candidates.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
    return payload
