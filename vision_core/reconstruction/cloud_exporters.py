from __future__ import annotations
from pathlib import Path
import json
import numpy as np


def export_obj(points: np.ndarray, output_path: str | Path) -> str:
    p = Path(output_path); p.parent.mkdir(parents=True, exist_ok=True)
    pts = np.asarray(points, dtype=float).reshape(-1,3)
    p.write_text(''.join(f'v {x:.6f} {y:.6f} {z:.6f}\n' for x,y,z in pts), encoding='utf-8')
    return str(p)


def save_cloud_metadata(points: np.ndarray, output_path: str | Path, source: str = 'unknown') -> str:
    pts = np.asarray(points, dtype=float).reshape(-1,3)
    meta = {"source": source, "point_count": int(len(pts)), "bounds_min": pts.min(axis=0).tolist() if len(pts) else None, "bounds_max": pts.max(axis=0).tolist() if len(pts) else None}
    p = Path(output_path); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(meta, indent=2), encoding='utf-8')
    return str(p)
